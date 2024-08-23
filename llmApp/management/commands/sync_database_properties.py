import requests
import json
import logging
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from llmApp.models import PropertySummary
from requests.exceptions import RequestException

# Set up logging
logger = logging.getLogger(__name__)


def get_ollama_response(prompt):
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'gemma2:2b',
            'prompt': prompt
        }, stream=True)

        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_line = line.decode('utf-8').strip()
                    json_data = json.loads(json_line)

                    full_response += json_data.get('response', '')

                    if json_data.get('done', False):
                        break
                except ValueError as e:
                    logger.error(f"Error decoding JSON: {e}")
                    continue

        return full_response or None

    except RequestException as e:
        logger.error(f"Error connecting to Ollama API: {e}")
        return None


class Command(BaseCommand):
    help = 'Process properties from django_db and update summaries'

    def handle(self, *args, **options):
        try:
            with connections['django_db'].cursor() as cursor:
                cursor.execute(
                    'SELECT property_id, title, description FROM "properties_property"')
                properties = cursor.fetchall()

                if not properties:
                    logger.info("No properties found to process.")
                    return

                for property_id, title, description in properties:
                    try:
                        self.process_property(
                            cursor, property_id, title, description)
                    except Exception as e:
                        logger.error(
                            f"Error processing property {property_id}: {e}")
                        continue

        except Exception as e:
            logger.error(f"Error accessing database: {e}")

        logger.info("Processing completed.")

    def process_property(self, cursor, property_id, title, description):
        rewrite_prompt = f"Rewrite the following property details:\nTitle: {title}\nDescription: {description}"
        rewritten_text = get_ollama_response(rewrite_prompt)

        if not rewritten_text:
            logger.warning(f"Skipping property {property_id} due to API error")
            return

        new_title, new_description = rewritten_text.split('\n', 1)

        with transaction.atomic():
            cursor.execute("""
                UPDATE "properties_property"
                SET title = %s, description = %s
                WHERE property_id = %s
            """, [new_title, new_description, property_id])

            summary_text = self.generate_summary(
                cursor, property_id, new_title, new_description)

            if summary_text:
                PropertySummary.objects.create(
                    property_id=property_id, summary=summary_text)
            else:
                logger.warning(
                    f"Skipping summary for property {property_id} due to API error")

    def generate_summary(self, cursor, property_id, title, description):
        cursor.execute("""
            SELECT
                (SELECT STRING_AGG(name, ', ') FROM "properties_amenity" WHERE id IN 
                (SELECT amenity_id FROM "properties_property_amenities" WHERE property_id = %s)) AS amenities
        """, [property_id])

        amenities = cursor.fetchone()[0] or ""
        summary_prompt = f"Generate a summary using the following details:\nTitle: {title}\nDescription: {description}\nAmenities: {amenities}"

        return get_ollama_response(summary_prompt)
