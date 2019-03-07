# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=50)
    show_time = models.CharField(max_length=30)
    type = models.CharField(max_length=30)