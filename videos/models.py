from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from users.models import Membership
from courses.models import Course, Subject


class Video(models.Model):
    slug = models.SlugField()
    title = models.CharField(_('title'), max_length=100)
    description = models.CharField(_('description'), max_length=5000)
    thumbnail = models.ImageField(
        default='defualt-video.jpg', upload_to='video_pics')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL)
    likes = models.BigIntegerField(_('likes'))
    dislikes = models.BigIntegerField(_('dislikes'))
    view_count = models.BigIntegerField(_('views'))
    date_uploaded = models.DateTimeField(
        _('upload date'), default=timezone.now)
    allowed_memberships = models.ForeignKey(
        Membership, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.SET_NULL)
    subjects = models.ForeignKey(Subject, on_delete=models.SET_NULL)


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    children = models.ForeignKey(
        'self', related_name='children', null=True, blank=True, on_delete=models.PROTECT)
    likes = models.BigIntegerField(_('likes'))
    dislikes = models.BigIntegerField(_('dislikes'))
    date_uploaded = models.DateTimeField(_('post date'), default=timezone.now)
