from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext as _
import users.models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='educator')[0]


class Course(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=133)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    date_created = models.DateTimeField(
        _('Day Created'), default=timezone.now())
    subjects = models.ForeignKey(
        Subject, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=133)
    children = models.ForeignKey(
        'self', on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return self.name
