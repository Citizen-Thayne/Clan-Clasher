from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from datetime import datetime
from django.utils import timezone

class ClanManager(models.Manager):
    def create_clan(self, name, leader=None, members=None):
        if name is None:
            raise ValueError
        if leader is None and members is not None:
            raise Exception('Cannot create a clan with members but no leader.')
        clan = Clan(name=name, leader=leader)
        clan.save()
        if leader:
            leader.clan = clan
            leader.save()
        if members is not None:
            for member in members:
                member.join_clan(clan)
                member.save()
        return clan


class Clan(models.Model):
    name = models.CharField(max_length=32)
    leader = models.ForeignKey('Chief', related_name='leader', null=True)

    def get_absolute_url(self):
        return reverse('clan_detail', kwargs={'pk': self.pk})

    def getRoster(self):
        return list(Chief.objects.filter(clan=self.id))

    def __str__(self):
        return self.name

    def start_war(self, opponent_name, finish_time):
        if finish_time < timezone.now():
            raise Exception("Finish time must not be sooner than current time")
        if self.is_in_war():
            raise Exception("Cannot start a war while currently in one")
        opponent = Clan.objects.create_clan(name=opponent_name)
        return War.objects.create(owner=self, opponent=opponent, finish_time=finish_time)

    def is_in_war(self):
        if self.get_current_war() is None:
            return False
        else:
            return True

    def get_current_war(self):
        try:
            return War.objects.get(owner=self, finish_time__gte=datetime.now())
        except ObjectDoesNotExist:
            return None

    objects = ClanManager()

    def get_current_opponent(self):
        current_war = self.get_current_war()
        if current_war is not None:
            return current_war.opponent
        else:
            return None



class Chief(models.Model):
    name = models.CharField(max_length=32)
    level = models.IntegerField(choices=((x, x) for x in range(3, 11)))
    clan = models.ForeignKey(Clan, null=True)

    def get_absolute_url(self):
        return reverse('chief_detail', kwargs={'pk': self.pk})

    def start_clan(self, name):
        if self.clan is not None:
            raise ValueError("Cannot start Clan while a member of a clan")
        clan = Clan.objects.create(name=name, leader=self)
        self.clan = clan

    def disband_clan(self):
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

    def join_clan(self, clan):
        if clan is None:
            raise ValueError("Clan cannot be none")
        self.clan = clan

    def leave_clan(self):
        if self.clan is None:
            raise ValueError("Cannot leave clan when not in a clan")
        self.clan = None

    def __str__(self):
        return self.name


class War(models.Model):
    owner = models.ForeignKey(Clan, related_name='owner')
    opponent = models.ForeignKey(Clan, related_name='opponent')
    finish_time = models.DateTimeField()

class WarRankManager(models.Manager):
    def get_war_roster(clan, war):
        return WarRank.objects.get(chief.clan=clan, war=war)
class WarRank(models.Model):
    chief = models.ForeignKey(Chief)
    war = models.ForeignKey(War)
    rank = models.SmallIntegerField()


class WarAttack(models.Model):
    attacker_war_rank = models.ForeignKey(WarRank, related_name='attacker')
    defender_war_rank = models.ForeignKey(WarRank, related_name='defender')


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

    def create_superuser(self, email, password):
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
