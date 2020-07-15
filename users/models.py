from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from courses.models import Course, Subject


MEMBERSHIP_CHOICES = (
    ('Professional', 'pro'),
    ('Personal', 'prs'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class ProfileManager(BaseUserManager):

    def create_user(self, email, username, first_name, password=None, **kwargs):
        if not email:
            raise ValueError(_('Your Email must be set'))
        if not username:
            raise ValueError(_('Your Username must be set'))
        if not first_name:
            raise ValueError(_('Your First Name must be set'))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Speruser must have is_staff=True'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Speruser must have is_superuser=True'))
        return self.create_user(email, username, first_name, password, **kwargs)


class Profile(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    first_name = models.CharField(max_length=73)
    last_name = models.CharField(max_length=73)
    interests = models.ForeignKey(Subject, on_delete=models.CASCADE)
    courses = models.ForeignKey(Course, on_delete=models.PROTECT)
    date_of_birth = models.DateField(max_length=8, blank=True, null=True)
    is_educator = models.BooleanField(default=False)
    is_learner = models.BooleanField(default=False)
    # followers = models.ForeignKey('self', related_name='followers', null=True, blank=True, on_delete=models.PROTECT)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL)

    stripe_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = ProfileManager()

    def __str__(self, *args, **kwargs):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def is_staff(self):
        return self.is_admin


class Contact(models.Model):

    # The user who created the relationship
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rel_from_set')

    # The user being followed
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rel_to_set')

    created = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Suscription(models.Model):
    user_membership = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sripe_suscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.username
