from django.db import models
import uuid

# Create your models here.


class ServiceModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class catalogueModel(models.Model):
    service = models.ForeignKey(
        ServiceModel, on_delete=models.SET_NULL, related_name="service", null=True, blank=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"


class ProductModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    catalogue = models.ForeignKey(
        catalogueModel, on_delete=models.SET_NULL, related_name="catalogue", null=True, blank=True)
    name = models.CharField(max_length=255)
    description_intro = models.TextField(blank=True, null=True)
    description_body = models.TextField(blank=True, null=True)
    description_conclusion = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="product_image/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.catalogue.name}"
