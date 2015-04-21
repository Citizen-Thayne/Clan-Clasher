from django.test import TestCase
from ClanClasher.models import *

class ClanTestCase(TestCase):
    def setUp(self):
        self.leader = Chief.objects.create(name='Test Leader', level=10)
        self.clan = Clan.objects.create(name="Test Clan", leader=self.leader)
        self.leader.clan = self.clan
        self.leader.save()
        self.member = Chief.objects.create(name='Test Member', level=7, clan=self.clan)
        self.loner = Chief.objects.create(name='Test Loner', level=8)


    def test_createClan_creates_a_clan(self):
        leader = Chief.objects.create(name='NewLeader', level=10)
        leader.startClan(name='New Clan')
        clan = Clan.objects.get(id=leader.clan.id)
        self.assertIsNotNone(clan)

    def test_createClan_while_in_clan_throws_exception(self):
        leader = Chief.objects.create(name='RepeatChief', level=10)
        leader.startClan(name='My Clan')
        with self.assertRaises(ValueError):
            leader.startClan(name='Some other clan')

    def test_joinClan_adds_chief_to_clan(self):
        newMember = Chief.objects.create(name='New Guy', level=5)
        newMember.joinClan(clan=self.clan)
        self.assertIsNotNone(newMember.clan)

    def test_leaveClan_removes_chief_from_clan(self):
        self.assertIsNotNone(self.member.clan)
        self.member.leaveClan()
        self.assertIsNone(self.member.clan)

    def test_leaveClan_when_not_in_clan_raises_exception(self):
        self.assertIsNone(self.loner.clan)
        with self.assertRaises(ValueError):
            self.loner.leaveClan()

    def test_disbandClan_deletes_a_clan(self):
        self.member.clan = self.clan
        self.member.save()
        self.assertIsNotNone(self.leader.clan)
        self.assertIsNotNone(self.member.clan)
        self.leader.disbandClan()
        member = Chief.objects.get(id=self.member.id)
        self.assertIsNone(self.leader.clan)
        self.assertIsNone(member.clan)

    def test_disbandClan_when_not_leader_raises_exception(self):
        with self.assertRaises(ValueError):
            self.member.disbandClan()

    def test_disbandClan_when_not_member_raises_exception(self):
        with self.assertRaises(ValueError):
            self.loner.disbandClan()