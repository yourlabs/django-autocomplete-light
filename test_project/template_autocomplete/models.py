from django.db import models


class TemplatedChoice(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return self.name


class TestModel(models.Model):
	choices = models.ManyToManyField(TemplatedChoice)

	def __unicode__(self):
		return u', '.join(self.choices.values_list('name', flat=True))