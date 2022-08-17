# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from places.fields import PlacesField
from address.models import AddressField
from address.models import Address
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse

from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from smart_selects.db_fields import ChainedForeignKey


class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)


class Type(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    picture = ProcessedImageField(upload_to='agents', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clothes:type-detail', args=[self.created.year,
                                                    self.created.strftime('%m'),
                                                    self.created.strftime('%d'),
                                                    self.slug])


class Edit(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    picture = ProcessedImageField(upload_to='agents', processors=[ResizeToFill(1920, 586)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    def get_absolute_url(self):
        return reverse('clothes:edit-detail', args=[self.created.year,
                                                       self.created.strftime('%m'),
                                                       self.created.strftime('%d'),
                                                       self.slug])

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    picture = ProcessedImageField(upload_to='shops', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    def get_absolute_url(self):
        return reverse('clothes:shop-detail', args=[self.created.year,
                                                    self.created.strftime('%m'),
                                                    self.created.strftime('%d'),
                                                    self.slug])

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    picture = ProcessedImageField(upload_to='brand', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    def get_absolute_url(self):
        return reverse('clothes:brand-detail', args=[self.created.year,
                                                           self.created.strftime('%m'),
                                                           self.created.strftime('%d'),
                                                           self.slug])

    def __str__(self):
        return self.name


class Nav(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    picture = ProcessedImageField(upload_to='navs', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    created = models.DateField(default=datetime.now)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
    nav = models.ForeignKey(Nav)
    picture = ProcessedImageField(upload_to='categories', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    class Meta:
        ordering = ('name',)

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('clothes:category-detail', args=[self.created.year,
                                                    self.created.strftime('%m'),
                                                    self.created.strftime('%d'),
                                                    self.slug])

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    created = models.DateField(default=datetime.now)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
    category = models.ForeignKey(Category)
    picture = ProcessedImageField(upload_to='subcategories', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)

    class Meta:
        ordering = ('name',)

        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def get_absolute_url(self):
        return reverse('clothes:subcategory-detail', args=[self.created.year,
                                                        self.created.strftime('%m'),
                                                        self.created.strftime('%d'),
                                                        self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    type = models.ForeignKey(Type)
    edit = models.ForeignKey(Edit)
    tags = TaggableManager(blank=True)
    brand = models.ForeignKey(Brand)
    shop = models.ForeignKey(Shop)
    category = models.ForeignKey(Category,
                                 related_name='products')
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=False,
        sort=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    picture = ProcessedImageField(upload_to='products', processors=[ResizeToFill(200, 200)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    pick = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, related_name='products')

    class Meta:
        ordering = ('name',)

        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clothes:product-detail', args=[self.created.year,
                                                    self.created.strftime('%m'),
                                                    self.created.strftime('%d'),
                                                    self.slug])


class Image(models.Model):
    color = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    image = ProcessedImageField(upload_to='product_images', processors=[ResizeToFill(1000, 600)],
                                format='JPEG',
                                options={'quality': 100})
    product = models.ForeignKey(Product, related_name='images')

    class Meta:
        ordering = ('-date_added',)


class Feature(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='product_features')

    class Meta:
        ordering = ('-date_added',)


class Size(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='product_sizes')

    class Meta:
        ordering = ('-date_added',)


