from django.db import models

# Create your models here.

#Represent Category Model
class Category(models.Model):
    name=models.CharField(max_length=128, unique=True)

    class meta:
        verbose_name_plural= 'Categories'

    def __str__(self):  #For Python 2, use __unicode__ too
            return self.name


#Represent Page Model
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self): #For Python 2, use __unicode__ too
        return self.title
