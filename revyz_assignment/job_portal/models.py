from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=100)
    tech_skills = models.ManyToManyField('TechSkill', related_name='candidates')
    resume = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TechSkill(models.Model):
    name = models.CharField(max_length=100)
