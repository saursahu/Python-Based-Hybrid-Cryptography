from django.db import models

# Create your models here.
class File(models.Model):

    fileName=models.CharField(max_length=30)
    fileType=models.CharField(max_length=10)
    File = models.FileField(upload_to = 'Media/File')

    def __str__(self):
        return self.fileName