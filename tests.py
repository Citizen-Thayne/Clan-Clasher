from django.test import TestCase

from ClanClasher.models import *


def mock_clan(name, member_count=50, ):
    leader = Chief.objects.create(name='Leader', level=10)
    members = []
    for x in range(1, member_count):
        members.append(Chief.objects.create(name='Chief #{}'.format(x), level=5))
    clan = Clan.create_clan(name=name, leader=leader, members=members)
    return clan


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
        with self.assertRaises(Exception):
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
        with self.assertRaisesMessage(Exception, 'Must be leader of clan to disband it'):
            self.member.disband_clan()

    def test_disband_clan_when_not_member_raises_exception(self):
        with self.assertRaises(Exception):
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
        roster = self.clan.chief_set.all()
        self.assertEqual(len(roster), 6)
        self.assertIn(self.leader, roster)

    def test_create_clan_with_no_leader_and_no_members_creates_empty_clan(self):
        clan = Clan.create_clan(name='Empty Clan')
        self.assertIsNotNone(clan)
        self.assertIsNone(clan.leader)
        self.assertEqual(len(clan.chief_set.all()), 0)

    def test_create_clan_with_leader_and_no_members_creates_clan(self):
        leader = Chief.objects.create(name='Leader', level=10)
        clan = Clan.create_clan(name='Leaders Only', leader=leader)
        self.assertIsNotNone(clan)
        self.assertIsNotNone(clan.leader)
        self.assertEqual(len(clan.chief_set.all()), 1)

    def test_create_clan_with_leader_and_members_creates_clan(self):
        leader = Chief.objects.create(name='Leader', level=10)
        members = [
            Chief(name='Chief 1', level=6),
            Chief(name='Chief 2', level=6),
            Chief(name='Chief 3', level=6),
            Chief(name='Chief 4', level=6),
            Chief(name='Chief 5', level=6),
        ]

        clan = Clan.create_clan(name='Full Party', leader=leader, members=members)
        self.assertIsNotNone(clan)
        self.assertIsNotNone(clan.leader)
        self.assertEqual(len(clan.chief_set.all()), 6)

    def test_create_clan_with_members_and_no_leader_raises_exception(self):
        name = "Leaderless"
        members = [Chief(name='Bob', level=3)]
        with self.assertRaisesMessage(Exception, 'Cannot create a clan with members but no leader.'):
            Clan.create_clan(name=name, members=members)

    def test_filter_members(self):
        clan = mock_clan('Mock Clan')
        outsider = Chief.objects.create(name='outsider', level=4)
        all_chiefs = Chief.objects.all()
        insiders = self.clan.filter_members(all_chiefs)
        self.assertEqual(set(insiders), set(self.clan.chief_set.all()))
        self.assertNotIn(outsider, insiders)


class ClanManagerTestCase(TestCase):
    def setUp(self):
        self.clanA = mock_clan(name='A', member_count=2)
        self.clanB = mock_clan(name='B', member_count=4)
        self.clanC = mock_clan(name='C', member_count=10)

    def test_organize_by_clan(self):
        chiefs = Chief.objects.filter(clan__in=[self.clanA, self.clanB, self.clanC])
        self.assertEqual(len(chiefs), 16)
        clans = Clan.objects.organize_by_clan(chiefs)
        self.assertEqual(len(clans[self.clanA]), 2)
        self.assertEqual(len(clans[self.clanB]), 4)
        self.assertEqual(len(clans[self.clanC]), 10)


class WarTestCase(TestCase):
    def setUp(self):
        # Attacking Clan
        self.attack_leader = Chief.objects.create(name='Attacker Leader', level=10)
        self.attack_members = [
            Chief(name='Attacker 1', level=8),
            Chief(name='Attacker 2', level=8),
            Chief(name='Attacker 3', level=8),
            Chief(name='Attacker 4', level=8),
            Chief(name='Attacker 5', level=8),
            Chief(name='Attacker 6', level=8),
            Chief(name='Attacker 7', level=8),
            Chief(name='Attacker 8', level=8),
            Chief(name='Attacker 9', level=8),
            Chief(name='Attacker 10', level=8),
            Chief(name='Attacker 11', level=8),
        ]
        self.attack_clan = Clan.create_clan(name="Attack", leader=self.attack_leader,
                                            members=self.attack_members)

    def test_start_war_with_invalid_roster_count_raises_exception(self):
        war_roster = self.attack_members[0:1]
        with self.assertRaisesMessage(Exception, 'Invalid roster size'):
            self.current_war = self.attack_clan.start_war(
                'Defending Clan',
                timezone.now(),
                roster=war_roster
            )
        self.assertIsNone(self.attack_clan.get_current_war())

    def test_start_war_with_valid_params_starts_war(self):
        war_roster = self.attack_members[0:9]
        war_roster.append(self.attack_leader)
        opponent_name = 'Opponent'
        start_time = timezone.now()

        self.assertEqual(len(war_roster), 10)
        war = self.attack_clan.start_war(
            opponent_name=opponent_name,
            start_time=start_time,
            roster=war_roster
        )
        self.assertEqual(war.opponent.name, 'Opponent')
        self.assertEqual(war.start_time, start_time)
        self.assertEqual(war.owner, self.attack_clan)

    def test_current_war_returns_war_when_there_is_a_current_war(self):
        self.current_war = self.attack_clan.start_war('Defending Clan', timezone.now(),
                                                      roster=self.attack_members[0:10])
        self.assertEqual(self.current_war, self.attack_clan.get_current_war())

    def test_current_war_returns_None_when_there_is_no_current_war(self):
        peaceful_clan = Clan.objects.create(name="Peaceful")
        self.assertIsNone(peaceful_clan.get_current_war())


class WarRankTestCase(TestCase):
    def setUp(self):
        self.attack_clan = mock_clan(10)
        self.war = self.attack_clan.start_war(
            opponent_name='Opponent',
            start_time=timezone.now(),

        )