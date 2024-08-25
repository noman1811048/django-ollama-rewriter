from django.db import models
from properties.models import Property

class PropertySummary(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property Summary"
        verbose_name_plural = "Property Summaries"

    def __str__(self):
        return f"Summary for Property {self.property.title}"
