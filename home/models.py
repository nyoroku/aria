from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone

from django.db import models


class Latest(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField()
    slug = models.SlugField(unique_for_date='created', default='latest')
    photo = ProcessedImageField(upload_to='latest', processors=[ResizeToFill(539, 303)],
                                          format='JPEG',
                                          options={'quality': 100}, blank=True)

    class Meta:
        ordering = ('-created',)




    def get_absolute_url(self):
        return reverse('home:news', args=[self.created.year,
                                          self.created.strftime('%m'),
                                          self.created.strftime('%d'),
                                          self.slug])


class DisplayAdvert(models.Model):
    created = models.DateTimeField(default=timezone.now())
    title = models.CharField(max_length=50, blank=True)
    body = models.TextField()
    location = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = ProcessedImageField(upload_to='latest', processors=[ResizeToFill(1920, 598)],
                                format='JPEG',
                                options={'quality': 100}, blank=True)





