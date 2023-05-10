from unittest import mock, TestCase
from group import Group
from person import Person
import customLogger

import copy


class TestGroup(TestCase):
    def setUp(self) -> None:
        N = 10
        self.population = [Person() for x in range(N)]
        self.info_nwk = Group(self.population, customLogger.gen_logging('', None))

    def test_set_population(self):
        self.info_nwk.set_population()

        # Assert everyone has assigned with group number
        for person in self.population:
            self.assertNotEqual(person.group_no, None)

    def test_set_roster(self):
        self.info_nwk.set_roster()

        self.assertTrue(0 in self.info_nwk.roster)
        self.assertTrue(1 in self.info_nwk.roster)
        self.assertTrue(2 in self.info_nwk.roster)
        self.assertTrue(3 in self.info_nwk.roster)
        self.assertFalse(4 in self.info_nwk.roster)

    def test_set_roster_no_population(self):
        # Replace setUp step
        self.population = []
        self.info_nwk = Group(self.population, None)

        self.info_nwk.set_roster()
        self.assertEqual(self.info_nwk.roster, {0: []})

    def test_get_prop(self):
        with mock.patch('group.Group.correct_para') as mock_correct_para:
            test_agpro = 50
            mock_correct_para.return_value = test_agpro / 100
            self.info_nwk.set_ag(test_agpro)
        with mock.patch('group.Group.correct_para') as mock_correct_para:
            test_propro = 50
            mock_correct_para.return_value = test_propro / 100
            self.info_nwk.set_pro(test_propro)
        self.assertEqual(0.5, self.info_nwk.get_prop())

    def test_get_prop_decimal_proportion(self):
        self.info_nwk.set_ag(0.5)
        self.info_nwk.set_pro(0.5)

        # Assert
        self.assertEqual(0.5, self.info_nwk.get_prop())

    def test_set_pro(self):
        test_propro = 50

        with mock.patch('group.Group.correct_para') as mock_correct_para:
            mock_correct_para.return_value = test_propro
            self.info_nwk.set_pro(test_propro)
        self.assertEqual(self.info_nwk.propro, 50)

    def test_set_pro_decimal_proportion(self):
        test_propro = 0.5

        with mock.patch('group.Group.correct_epi_para') as mock_correct_epi_para:
            mock_correct_epi_para.return_value = test_propro # Parse the decimal is the proportion, so multiply by 100
            self.info_nwk.set_pro(test_propro)
        self.assertEqual(self.info_nwk.propro, 50)

    def test_set_ag(self):
        test_agpro = 50
        with mock.patch('group.Group.correct_para') as mock_correct_para:
            mock_correct_para.return_value = test_agpro
            self.info_nwk.set_ag(test_agpro)
        self.assertEqual(self.info_nwk.agpro, 50)

    def test_set_ag_decimal_proportion(self):
        test_agpro = 0.5

        with mock.patch('group.Group.correct_epi_para') as mock_correct_epi_para:
            mock_correct_epi_para.return_value = test_agpro
            self.info_nwk.set_ag(test_agpro)
        self.assertEqual(self.info_nwk.agpro, 50)

    def test_set_opinion(self):
        self.info_nwk.set_ag(50)
        self.info_nwk.set_pro(50)
        self.info_nwk.set_opinion()

        for person in self.population:
            self.assertTrue(person.opinion == 0 or person.opinion == 1)

    def test_update_group(self):
        self.assertTrue(self.info_nwk.roster != {})
        old_roster = copy.deepcopy(self.info_nwk.roster)

        self.info_nwk.update_group()

        for group_name, group in self.info_nwk.roster.items():
            if old_roster[group_name] != group:
                return

        # If none of the groups have changed, then fail the test.
        self.fail()

    def test_inflexible_prework(self):
        self.population[0].personality = 1
        self.population[1].personality = 2

        self.info_nwk.set_ag(50)
        self.info_nwk.set_pro(50)
        self.info_nwk.set_opinion()
        self.info_nwk.inflexible_prework()

        self.assertEqual(self.population[0].meta_opinion, 1)
        self.assertEqual(self.population[1].meta_opinion, 0)

    def test_update(self):
        # Regenerate population
        N = 12
        self.population = [Person() for x in range(N)]
        self.info_nwk = Group(self.population, customLogger.gen_logging('', None))

        self.info_nwk.set_ag(50)
        self.info_nwk.set_pro(50)
        '''
            Set opinion by hand
    
            - Group 0 has all 0s => [0, 0, 0]
            - Group 1 has all 1s => [1, 1, 1]
            - Group 2 has [1, 1, 0] => [1, 1, 1]
            - Group 3 has [0, 0, 1] => [0, 0, 0]
        '''
        test_group_0_opinions = [0, 0, 0]
        for group_name, members in self.info_nwk.roster.items():
            # print(group_name)
            for person in members:
                if group_name == 0:
                    person.opinion = 0
                elif group_name == 1:
                    person.opinion = 1
                elif group_name == 2:
                    if members.index(person) == self.info_nwk.size-1:
                        person.opinion = 0
                    else: person.opinion = 1
                elif group_name == 3:
                    if members.index(person) == self.info_nwk.size-1:
                        person.opinion = 1
                    else: person.opinion = 0
            #     print(person.opinion, end=', ')
            # print()
        self.info_nwk.update()

        # Assert


    def test_update_with_personality(self):
        self.population[0].personality = 1
        self.population[1].personality = 2

        self.info_nwk.set_ag(50)
        self.info_nwk.set_pro(50)

        self.info_nwk.set_opinion()
        self.info_nwk.update()

        # Assert

    def test_inflexible(self):
        # Regenerate population
        N = 2
        self.population = [Person() for x in range(N)]
        self.info_nwk = Group(self.population, customLogger.gen_logging('', None))

        self.population[0].personality = 1
        self.population[1].personality = 2
        self.info_nwk.inflexible_prework()

        self.assertEqual(self.population[0].meta_opinion, 1)
        self.assertEqual(self.population[1].meta_opinion, 0)

        self.info_nwk.inflexible()
        self.assertEqual(self.population[0].opinion, 1)
        self.assertEqual(self.population[1].opinion, 0)
        self.assertEqual(self.population[0].meta_opinion, None)
        self.assertEqual(self.population[1].meta_opinion, None)

    def test_balance(self):
        # Regenerate population
        N = 3
        self.population = [Person() for x in range(N)]
        self.info_nwk = Group(self.population, customLogger.gen_logging('',None))

        self.population[0].personality = 3
        self.population[0].opinion = 0
        self.population[1].opinion = 1
        self.population[2].opinion = 1

        self.info_nwk.balance()

        self.assertEqual(self.population[0].opinion, 1)
        self.assertEqual(self.population[1].opinion, 1)
        self.assertEqual(self.population[2].opinion, 1)
