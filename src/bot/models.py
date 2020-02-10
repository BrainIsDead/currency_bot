from django.db import models
from jsonfield import JSONField

class Rates(models.Model):
    data = JSONField()
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return(str(self.timestamp))