from django.db import models


# Create your models here.
class DaumData(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField()
    specific_id = models.CharField(max_length=15, null=True)

    # admin계정에서 바로 제목으로 볼수있게
    def __str__(self):
        return self.title
