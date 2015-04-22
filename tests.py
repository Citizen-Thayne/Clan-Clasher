from django.test import TestCase

from ClanClasher.models import *


class ChiefTestCase(TestCase):
    def setUp(self):
        self.leader = Chief.objects.create(name='Test Leader', level=10)
        self.clan = Clan.objects.create(name="Test Clan", leader=self.leader)
        self.leader.clan = self.clan
        self.leader.save()
        self.member = Chief.objects.create(name='Test Member', level=7, clan=self.clan)
        self.loner = Chief.objects.create(name='Test Loner', level=8)


    def test_create_clan_creates_a_clan(self):
        leader = Chief.objects.create(name='NewLeader', level=10)
        leader.start_clan(name='New Clan')
        clan = Clan.objects.get(id=leader.clan.id)
        self.assertIsNotNone(clan)

    def test_create_clan_while_in_clan_throws_exception(self):
        leader = Chief.objects.create(name='RepeatChief', level=10)
        leader.start_clan(name='My Clan')
        with self.assertRaises(ValueError):
            leader.start_clan(name='Some other clan')

    def test_join_clan_adds_chief_to_clan(self):
        newMember = Chief.objects.create(name='New Guy', level=5)
        newMember.join_clan(clan=self.clan)
        self.assertIsNotNone(newMember.clan)

    def test_leave_clan_removes_chief_from_clan(self):
        self.assertIsNotNone(self.member.clan)
        self.member.leave_clan()
        self.assertIsNone(self.member.clan)

    def test_leave_clan_when_not_in_clan_raises_exception(self):
        self.assertIsNone(self.loner.clan)
        with self.assertRaises(ValueError):
            self.loner.leave_clan()

    def test_disband_clan_deletes_a_clan(self):
        self.member.clan = self.clan
        self.member.save()
        self.assertIsNotNone(self.leader.clan)
        self.assertIsNotNone(self.member.clan)
        self.leader.disband_clan()
        member = Chief.objects.get(id=self.member.id)
        self.assertIsNone(self.leader.clan)
        self.assertIsNone(member.clan)

    def test_disband_clan_when_not_leader_raises_exception(self):
        with self.assertRaises(ValueError):
            self.member.disband_clan()

    def test_disband_clan_when_not_member_raises_exception(self):
        with self.assertRaises(ValueError):
            self.loner.disband_clan()


class ClanTestCase(TestCase):
    def setUp(self):
        self.leader = Chief.objects.create(name='Chief Leader', level=10)
        self.leader.start_clan(name='Test Clan')
        self.leader.save()
        self.clan = self.leader.clan

        Chief.objects.bulk_create([
            Chief(name='Chief 1', level=6, clan=self.clan),
            Chief(name='Chief 2', level=6, clan=self.clan),
            Chief(name='Chief 3', level=6, clan=self.clan),
            Chief(name='Chief 4', level=6, clan=self.clan),
            Chief(name='Chief 5', level=6, clan=self.clan),
        ])

    def test_getRoster_returns_complete_clan_roster(self):
        roster = self.clan.getRoster()
        self.assertEqual(len(roster), 6)
        self.assertIn(self.leader, roster)

    def test_create_clan_with_no_leader_and_no_members_creates_empty_clan(self):
        clan = Clan.objects.create_clan(name='Empty Clan')
        self.assertIsNotNone(clan)
        self.assertIsNone(clan.leader)
        self.assertEqual(len(clan.getRoster()),0)

    def test_create_clan_with_leader_and_no_members_creates_clan(self):
        leader = Chief.objects.create(name='Leader', level=10)
        clan = Clan.objects.create_clan(name='Leaders Only', leader=leader)
        self.assertIsNotNone(clan)
        self.assertIsNotNone(clan.leader)
        self.assertEqual(len(clan.getRoster()),1)

    def test_create_clan_with_leader_and_members_creates_clan(self):
        leader = Chief.objects.create(name='Leader', level=10)
        members = [
            Chief(name='Chief 1', level=6),
            Chief(name='Chief 2', level=6),
            Chief(name='Chief 3', level=6),
            Chief(name='Chief 4', level=6),
            Chief(name='Chief 5', level=6),
        ]

        clan = Clan.objects.create_clan(name='Full Party', leader=leader, members=members)
        self.assertIsNotNone(clan)
        self.assertIsNotNone(clan.leader)
        self.assertEqual(len(clan.getRoster()),6)


class WarTestCase(TestCase):
    def setUp(self):
        #Attacking Clan
        members = [
            Chief(name='Attacker Leader', level=10),
            Chief(name='Attacker 1', level=8),
            Chief(name='Attacker 2', level=8),
            Chief(name='Attacker 3', level=8),
            Chief(name='Attacker 4', level=8),
            Chief(name='Attacker 5', level=8),
            Chief(name='Attacker 6', level=8),
        ]