from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class ClanManager(models.Manager):
    @staticmethod
    def organize_by_clan(chiefs):
        '''
        Returns a dictionary where key is a clan and value is list of 
        chiefs that are in chiefs arg and that clan
        '''
        clans = {}
        for chief in chiefs:
            clans.setdefault(chief.clan, []).append(chief)
        return clans


class Clan(models.Model):
    name = models.CharField(max_length=32)
    leader = models.ForeignKey('Chief', related_name='leader', null=True)

    @staticmethod
    def create_clan(name, leader=None, members=None):
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

    def get_absolute_url(self):
        return reverse('clan_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def start_war(self, opponent_name, start_time, roster, size):
        if start_time < timezone.now() - timedelta(days=1):
            raise Exception("Start time must be more than a day ago")
        if self.is_in_war():
            raise Exception("Cannot start a war while currently in one")
        if len(roster) not in range(10, 55, 5):
            raise Exception("Invalid roster size")

        opponent = Clan.create_clan(name=opponent_name)
        war = War.objects.create(owner=self, opponent=opponent, start_time=start_time, size=size)
        for i, member in enumerate(roster):
            if member is not None:
                WarRank.objects.create(chief=member, rank=i + 1, war=war)

        return war

    def is_in_war(self):
        if self.get_current_war() is None:
            return False
        else:
            return True

    def get_current_war(self):
        try:
            return War.objects.get(owner=self, start_time__gt=datetime.now() - timedelta(days=1))
        except ObjectDoesNotExist:
            return None

    objects = ClanManager()

    def get_current_opponent(self):
        current_war = self.get_current_war()
        if current_war is not None:
            return current_war.opponent
        else:
            return None

    def filter_members(self, chiefs):
        '''
        Takes a list of chiefs and checks if they are 
        members of this clan. 
        Returns the list of chiefs that are
        '''
        clans = Clan.objects.organize_by_clan(chiefs)
        return clans[self]


class ChiefManager(models.Manager):
    pass


class Chief(models.Model):
    name = models.CharField(max_length=32)
    level = models.IntegerField(choices=((x, x) for x in range(3, 11)))
    clan = models.ForeignKey(Clan, null=True)
    objects = ChiefManager()

    def get_absolute_url(self):
        return reverse('chief_detail', kwargs={'pk': self.pk})

    def start_clan(self, name):
        if self.clan is not None:
            raise ValueError("Cannot start Clan while a member of a clan")
        clan = Clan.objects.create(name=name, leader=self)
        self.clan = clan

    def disband_clan(self):
        if self.clan is None:
            raise Exception("Must be in clan and leader to disband clan")
        if self.clan.leader is not self:
            raise Exception("Must be leader of clan to disband it")
        members = self.clan.chief_set.all()
        for member in members:
            member.clan = None
            member.save()
        self.clan.delete()
        self.clan = None
        self.save()

    def join_clan(self, clan):
        self.clan = clan

    def leave_clan(self):
        if self.clan is None:
            raise Exception("Cannot leave a clan when not a member of one")
        self.clan = None

    def __str__(self):
        return self.name


class War(models.Model):
    owner = models.ForeignKey(Clan, related_name='owner')
    opponent = models.ForeignKey(Clan, related_name='opponent')
    start_time = models.DateTimeField()
    size = models.SmallIntegerField(choices=[(x, x) for x in range(10, 55, 5)])

    def get_war_roster(self):
        war_ranks = WarRank.objects.filter(war=self)
        member_list = [None] * self.size
        for war_rank in war_ranks:
            member_list[war_rank.rank - 1] = war_rank.chief
        return member_list


class WarRank(models.Model):
    chief = models.ForeignKey(Chief)
    war = models.ForeignKey(War)
    rank = models.SmallIntegerField()
    # objects = WarRankManager()


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
