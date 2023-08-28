from django.db import models

class Operation(models.Model):
    question = models.CharField(max_length=100)
    answer = models.FloatField()

    def __str__(self):
        return f"{self.question} = {self.answer}"
