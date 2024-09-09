from django.db import models

# Create your models here.
class Patent(models.Model):
    patent_id                   = models.CharField(max_length=100)
    title                       = models.TextField()
    assignee                    = models.CharField(max_length=255, null=True)
    inventor                    = models.TextField(null=True)
    priority_date               = models.DateField(null=True)
    filing_date                 = models.DateField(null=True)
    publication_date            = models.DateField(null=True)
    grant_date                  = models.DateField(null=True)
    result_link                 = models.URLField(null=True)
    representative_figure_link  = models.URLField(null=True)
