import requests
import json
import logging
import re
import time
from django.core.management.base import BaseCommand
from llmApp.models import PropertySummary
from requests.exceptions import RequestException
from properties.models import Property

class Command(BaseCommand):
    help = 'Re-write property titles and descriptions using the Lemma model from Ollama'

    def api_call_with_retry(self, url, json_data, max_retries=3, delay=1):
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=json_data, timeout=30)
                response.raise_for_status()
                return response
            except RequestException as e:
                if attempt == max_retries - 1:
                    raise
                self.stdout.write(self.style.WARNING(
                    f"API call failed (attempt {attempt + 1}/{max_retries}): {e}"))
                time.sleep(delay)

    def clean_text(self, text):
        # Remove any non-alphanumeric characters except spaces and basic punctuation
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        # Remove extra whitespace
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    def extract_title(self, text):
        # Look for a line starting with "Title:" or just take the first line
        lines = text.split('\n')
        for line in lines:
            if line.lower().startswith("title:"):
                return self.clean_text(line.split(":", 1)[1].strip())
        return self.clean_text(lines[0]) if lines else ""

    def handle(self, *args, **kwargs):
        properties = Property.objects.all()
        failed_properties = []

        for prop in properties:
            try:
                # Prepare the prompt to rewrite the title and description
                prompt = f"Rewrite the following property information. Provide a concise and appealing title on the first line, prefixed with 'Title:', followed by a detailed description:\n\nCurrent Title: {prop.title[:500]}\nCurrent Description: {prop.description[:1000]}"

                # Interact with the Ollama API
                response = self.api_call_with_retry(
                    "http://localhost:11434/api/generate",
                    {"model": "gemma2:2b", "prompt": prompt},
                )

                # Handle NDJSON content type
                if response.headers.get('Content-Type') == 'application/x-ndjson':
                    rewritten_text = ''
                    for line in response.iter_lines():
                        if line:
                            try:
                                json_line = line.decode('utf-8')
                                data = json.loads(json_line)
                                rewritten_text += data.get('response', '') + '\n'
                            except ValueError as e:
                                self.stdout.write(self.style.ERROR(f"JSON decoding error in line: {e}"))
                                continue
                else:
                    self.stdout.write(self.style.ERROR(f"Unexpected content type: {response.headers.get('Content-Type')}"))
                    continue

                # Extract and clean the rewritten title and description
                rewritten_title = self.extract_title(rewritten_text)
                rewritten_description = '\n'.join(rewritten_text.split('\n')[1:]).strip()

                # Update the property with the new title and description
                prop.title = rewritten_title or prop.title  # Fallback to original title if extraction fails
                prop.description = rewritten_description or prop.description  # Fallback to original description if empty
                prop.save()

                # Prepare a prompt to generate a summary
                summary_prompt = f"Generate a summary for the following property information:\n\n{rewritten_title}\n{rewritten_description[:1000]}\nLocation: {', '.join(str(l) for l in prop.locations.all())}\nAmenities: {', '.join(str(a) for a in prop.amenities.all())}"

                # Request the summary from the Ollama API
                summary_response = self.api_call_with_retry(
                    "http://localhost:11434/api/generate",
                    {"model": "gemma2:2b", "prompt": summary_prompt},
                )

                # Handle NDJSON content type for summary
                if summary_response.headers.get('Content-Type') == 'application/x-ndjson':
                    summary_text = ''
                    for line in summary_response.iter_lines():
                        if line:
                            try:
                                json_line = line.decode('utf-8')
                                data = json.loads(json_line)
                                summary_text += data.get('response', '') + '\n'
                            except ValueError as e:
                                self.stdout.write(self.style.ERROR(f"JSON decoding error in line: {e}"))
                                continue
                else:
                    self.stdout.write(self.style.ERROR(f"Unexpected content type: {summary_response.headers.get('Content-Type')}"))
                    continue

                # Create or update the PropertySummary record
                PropertySummary.objects.update_or_create(
                    property=prop,
                    defaults={'summary': summary_text.strip()},
                )

                # Add a small delay to avoid overwhelming the API
                time.sleep(0.5)

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error processing property ID {prop.property_id}: {str(e)}"))
                failed_properties.append(prop.property_id)

        if failed_properties:
            self.stdout.write(self.style.WARNING(
                f"Failed to process the following property IDs: {', '.join(map(str, failed_properties))}"))

        self.stdout.write(self.style.SUCCESS(
            'Successfully re-written properties and generated summaries.'))