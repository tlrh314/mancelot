from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify

from tinymce.models import HTMLField


class Store(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, max_length=255, unique=True)
    info = HTMLField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, max_length=255, unique=True)
    info = HTMLField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CeceLabel(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, max_length=255, unique=True)
    info = HTMLField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, max_length=255, unique=True)
    info = HTMLField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, max_length=255, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategory"
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
