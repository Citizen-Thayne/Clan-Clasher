from django.contrib.auth.models import  AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models


class Clan(models.Model):
    name = models.CharField(max_length=32)


class Chief(models.Model):
    name = models.CharField(max_length=32)
    level = models.IntegerField(choices=((x, x) for x in range(3, 11)))
    clan = models.ForeignKey(Clan, null=True)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = 'user'
    objects = MyUserManager()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    chief = models.ForeignKey(Chief)
    user = models.OneToOneField(MyUser, related_name='profile')


# def create_profile(sender, instance, created, **kwargs):
# if created:
# Profile.objects.create(user=instance)
#
# post_save.connect(create_profile, sender=User)

