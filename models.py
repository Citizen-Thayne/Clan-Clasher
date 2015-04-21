from django.contrib.auth.models import  AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models


class Clan(models.Model):
    name = models.CharField(max_length=32)
    leader = models.ForeignKey('Chief', related_name='leader')

    def get_absolute_url(self):
        return reverse('clan_detail', kwargs={'pk': self.pk })

    def getRoster(self):
        return list(Chief.objects.filter(clan=self.id))

    def __str__(self):
        return self.name


class Chief(models.Model):
    name = models.CharField(max_length=32)
    level = models.IntegerField( choices=((x, x) for x in range(3, 11)))
    clan = models.ForeignKey(Clan, null=True)
    # war_rank = models.SmallIntegerField(choices=((x,x)) for x in range(3,50)

    def get_absolute_url(self):
        return reverse('chief_detail',kwargs={'pk':self.pk})

    def startClan(self, name):
        if self.clan is not None:
            raise ValueError("Cannot start Clan while a member of a clan")
        clan = Clan.objects.create(name=name, leader=self)
        self.clan = clan

    def disbandClan(self):
        if self.clan is None:
            raise ValueError("Must be in clan and leader to disband clan")
        if self.clan.leader is not self:
            raise ValueError("Must be leader of clan to disband it")
        members = self.clan.getRoster()
        for member in members:
            member.clan = None
            member.save()
        self.clan.delete()
        self.clan = None
        self.save()


    def joinClan(self,clan):
        if clan is None:
            raise ValueError("Clan cannot be none")
        self.clan = clan

    def leaveClan(self):
        if self.clan is None:
            raise ValueError("Cannot leave clan when not in a clan")
        self.clan = None

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password):
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
