from django.db import models

# Create your models here.

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    product_code = models.CharField(max_length=50, blank=True)
    product_description = models.CharField(max_length=255, blank=True)
    factory = models.CharField(max_length=50, blank=True)
    operation_code = models.CharField(max_length=50, blank=True)
    operation_description = models.CharField(max_length=255, blank=True)
    machine_number = models.CharField(max_length=50, blank=True)
    machine_description = models.CharField(max_length=255, blank=True)
    operator_code = models.CharField(max_length=50, blank=True)
    operator_name = models.CharField(max_length=255, blank=True)
    additional_details = models.TextField(blank=True)
    


