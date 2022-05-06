import random

import pandas as pd

from person import Person
from group import Group
from vaccine import Vaccine
from contact import ContactNwk
from epidemic import Epidemic
import customLogger

from mode import Mode01
from mode import Mode02
from mode import Mode04
from mode import Mode05
from mode import Mode07
from mode import Mode08
from mode import Mode10
from mode import Mode11
from mode import Mode15
from mode import Mode20
from mode import Mode21
from mode import Mode22
from mode import Mode23
from mode import Mode24
from mode import Mode51
from mode import Mode52
from mode import Mode53
from mode import Mode54
from mode import Mode501
from mode import Mode505

from unittest import mock, TestCase
import networkx as nx


class TestEpidemic(TestCase):
    def setUp(self) -> None:
        N = 50
        self.logger = customLogger.gen_logging('', None)
        self.population = [Person() for x in range(N)]
        self.contact_nwk = ContactNwk(self.population, False, self.logger)
        self.contact_nwk.set_default_edge_list()
        self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)
        self.epidemic = Epidemic(0, 0.14, 0.05, 0.000005, 0.000005, self.population, 0.5, 20, {}, self.contact_nwk,
                                 False, self.logger)

    def test_get_states(self):
        self.epidemic.get_states()

        # Assert
        # By default, 4 people infected initially
        self.assertEqual(self.epidemic.I, 4)
        self.assertEqual(self.epidemic.U, 4)
        self.assertEqual(self.epidemic.E, 0)
        self.assertEqual(self.epidemic.R, 0)
        self.assertEqual(self.epidemic.S, len(self.population) - 4)

    def test_write_history(self):
        # Arrange
        used_flag_V = 1
        used_flag_R = 1
        for people in self.population:
            if people.suceptible == 0:
                if used_flag_V != 0:
                    people.vaccinated = 1
                    used_flag_V -= 1
            if people.suceptible == 0 and people.vaccinated == 0:
                if used_flag_R != 0:
                    people.removed = 1
                    used_flag_R -= 1

        self.epidemic.get_states()
        print(f'S: {self.epidemic.S}, I: {self.epidemic.I}, V:{self.epidemic.V}, R:{self.epidemic.R}')

        # Act
        self.epidemic.write_history()

        # Assert
        for person in self.population:
            if person.vaccinated == 1:
                self.assertEqual(person.compartment_history, ['V'])
            elif person.suceptible == 1 and person.exposed == 0:
                self.assertEqual(person.compartment_history, ['E'])
            elif person.suceptible == 1 and person.exposed == 1:
                self.assertEqual(person.compartment_history, ['I'])
            elif person.removed == 1:
                self.assertEqual(person.compartment_history, ['R'])
            else:
                self.assertEqual(person.compartment_history, ['S'])


    @mock.patch('epidemic.Epidemic.start_epidemic')
    def test_set_epidemic(self, test_epidemic_start_epidemic):
        self.epidemic.set_epidemic(1)
        test_epidemic_start_epidemic.assert_called_once()

    @mock.patch('epidemic.Epidemic.kill_epidemic')
    def test_set_epidemic_0(self, test_epidemic_kill_epidemic):
        self.epidemic.set_epidemic(0)
        test_epidemic_kill_epidemic.assert_called_once()

    @mock.patch('epidemic.Epidemic.kill_epidemic')
    def test_set_epidemic_invalid_mode_number(self, test_epidemic_kill_epidemic):
        self.epidemic.set_epidemic(2)
        test_epidemic_kill_epidemic.assert_called_once()

    @mock.patch('epidemic.Epidemic.kill_epidemic')
    def test_set_epidemic_negative_invalid_mode_number(self, test_epidemic_kill_epidemic):
        self.epidemic.set_epidemic(-1)
        test_epidemic_kill_epidemic.assert_called_once()

    def test_start_epidemic(self):
        # Act
        self.epidemic.start_epidemic()

        # Assert
        self.epidemic.get_states()
        self.assertEqual(self.epidemic.I, 4)

    def test_start_epidemic_init_infect(self):
        # Act
        self.epidemic.start_epidemic(10)

        # Assert
        self.epidemic.get_states()
        self.assertEqual(self.epidemic.I, 10)

    @mock.patch('mode.Mode505.set_infection')
    def test_start_epidemic_mode505_nwk(self, mock_505_set_infection):
        # Act
        # Load mode
        mode = {505: Mode505(self.population, self.logger, self.contact_nwk)}
        self.epidemic.load_modes(mode)
        self.assertTrue(505 in self.epidemic.mode)

        # Act
        self.epidemic.start_epidemic()
        mock_505_set_infection.assert_called_once()

    '''
    The following is an integration test
    '''
    # def test_start_epidemic_mode505(self):
    #     # Arrange
    #     # Load mode
    #     mode = {505: Mode505(self.population, self.logger, None)}
    #     self.epidemic.load_modes(mode)
    #
    #     # Assert ValueError should be raised
    #     with self.assertRaises(ValueError):
    #         self.epidemic.start_epidemic()

    @mock.patch('mode.Mode505.set_infection')
    def test_start_epidemic_mode505_501(self, mock_505_set_infection):
        # Act
        # Load mode
        mode = {501: Mode501(self.population, self.logger, self.contact_nwk), 505: Mode505(self.population, self.logger, self.contact_nwk)}
        self.epidemic.load_modes(mode)
        self.assertTrue(501 in self.epidemic.mode)
        self.assertTrue(505 in self.epidemic.mode)

        # Act
        self.epidemic.start_epidemic()
        mock_505_set_infection.assert_called_once()

    def test_kill_epidemic(self):
        # Arrange
        self.population[0].suceptible = 1
        self.population[1].suceptible = 1
        self.population[2].suceptible = 1

        # Act
        self.epidemic.kill_epidemic()

        # Assert
        for person in self.population:
            if person.suceptible == 1:
                self.fail()


    def test_load_modes(self):
        # Arrange
        test_mode = {999: []}

        # Act
        self.epidemic.load_modes(test_mode)

        # Assert
        self.assertTrue(999 in self.epidemic.mode)

    def test_set_pro_ag(self):
        # Arrange
        for person in self.population:
            person.opinion = random.randint(0, 1)

        # Act
        self.epidemic.set_pro_ag()

        # Assert
        self.assertEqual(self.epidemic.Pro + self.epidemic.Ag, 1)

    @mock.patch('random.randint')
    def test_vaccinate(self, mock_random_randint):
        mock_random_randint.return_value = 0
        self.epidemic.vaccinated = 0.3 # Original value is 0
        self.population[0].suceptible = 0

        self.epidemic.vaccinate()

        # Assert
        self.assertEqual(self.population[0].vaccinated, 1)

    def test_vaccinate_mode04(self):
        # Arrange
        # Load mode
        mode = {4: Mode04(self.population, 0.5, self.logger)}
        self.epidemic.load_modes(mode)
        self.epidemic.mode[4].set_lambda(0.01)
        self.epidemic.mode[4].QRE()
        self.assertTrue(4 in self.epidemic.mode)

        # Act
        self.epidemic.vaccinate()

        # Assert
        for person in self.population:
            self.assertEqual(len(person.vaccine_history), 1)

    @mock.patch('random.randint', return_value=0)
    @mock.patch('mode.Mode15.check_multi_dose_vaccine', return_value=True)
    @mock.patch('mode.Mode15.take_multi_dose_vaccine')
    @mock.patch('mode.Mode15.write_vaccine_history')
    def test_vaccinate_mode15(self, mock_random_randint, mock_check_multi_dose_vaccine, mock_take_multi_dose_vaccine, mock_write_vaccine_history):
        # Arrange
        mode = {15: Mode15(self.population, self.logger)}
        self.epidemic.load_modes(mode)

        test_vaccine = Vaccine(efficacy=1, alpha=0.3)
        mock_take_multi_dose_vaccine.return_value = test_vaccine

        # Act
        self.epidemic.vaccinate()

    # @mock.patch('random.randint', return_value=0)
    # @mock.patch('mode.Mode15.check_multi_dose_vaccine', return_value=True)
    # @mock.patch('mode.Mode15.check_recent_vaccine', return_value=None)
    # @mock.patch('mode.Mode15.check_next_vaccine')
    # @mock.patch('mode.Mode15.take_multi_dose_vaccine')
    def test_vaccinate_mode15_opinion(self):
        # Arrange
        test_info_nwk = Group(self.population, self.logger)
        test_info_nwk.propro = 0.5
        test_info_nwk.agpro = 0.5
        test_info_nwk.set_opinion()

        mode = {15: Mode15(self.population, self.logger), 21: Mode21(self.population, test_info_nwk, self.logger), 52: Mode52(self.population, self.logger, self.contact_nwk)}
        self.epidemic.load_modes(mode)
        self.epidemic.vaccine_ls = [Vaccine(name="Test", efficacy=1, alpha=0.3)]

        self.epidemic.mode[21].set_personality()

        # Act
        self.epidemic.vaccinate()

        # Assert
        # self.fail()

    def test_generate_vaccine_dose_count_record(self):
        # Arrange
        self.epidemic.vaccine_ls = [Vaccine(name="Test", efficacy=1, alpha=0.3)]

        # Act
        self.epidemic.generate_vaccine_dose_count_record()

        # Assert
        self.assertIsNotNone(self.epidemic.current_vaccine_dose_count)
        print(self.epidemic.current_vaccine_dose_count)

    def test_generate_vaccine_dose_count_record_multiple_vaccine(self):
        # Arrange
        self.epidemic.vaccine_ls = [Vaccine(name="Test_01", efficacy=1, alpha=0.3), Vaccine(name="Test_02", efficacy=1, alpha=0.3)]

        # Act
        self.epidemic.generate_vaccine_dose_count_record()

        # Assert
        self.assertIsNotNone(self.epidemic.current_vaccine_dose_count)
        print(self.epidemic.current_vaccine_dose_count)
        self.assertEqual(len(self.epidemic.current_vaccine_dose_count), 2)

    def test_vaccine_dose_taken(self):
        # Arrange
        vaccine_name = "Test"
        vaccine_label = vaccine_name + ':0'
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, efficacy=1, alpha=0.3)]
        self.epidemic.generate_vaccine_dose_count_record()  # Generate the record in Epidemic.generate_vaccine_dose_count_record() first

        # Act
        self.epidemic.vaccine_dose_taken(self.epidemic.vaccine_ls[0])

        # Assert
        self.assertEqual(self.epidemic.current_vaccine_dose_count[vaccine_label], 1)

    def test_vaccine_dose_taken_multiple_vaccine(self):
        # Arrange
        vaccine_name_01 = "Test01"
        vaccine_label = vaccine_name_01 + ':1'
        vaccine_name_02 = "Test02"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name_01, dose=1, efficacy=1, alpha=0.3), Vaccine(name=vaccine_name_01, dose=2, efficacy=1, alpha=0.3), Vaccine(name=vaccine_name_02, efficacy=1, alpha=0.3)]
        self.epidemic.generate_vaccine_dose_count_record()  # Generate the record in Epidemic.generate_vaccine_stock_record() first
        print(self.epidemic.current_vaccine_dose_count)

        # Act
        self.epidemic.vaccine_dose_taken(self.epidemic.vaccine_ls[0])

        # Assert
        print(self.epidemic.current_vaccine_dose_count)
        self.assertEqual(self.epidemic.current_vaccine_dose_count[vaccine_label], 1)

    def test_generate_vaccine_stock_record(self):
        # Arrange
        self.epidemic.vaccine_ls = [Vaccine(name="Test", efficacy=1, alpha=0.3)]

        # Act
        self.epidemic.generate_vaccine_stock_record()

        # Assert
        self.assertIsNotNone(self.epidemic.vaccine_stocktake)
        self.assertEqual(len(self.epidemic.vaccine_stocktake), 1)

    def test_vaccine_stock_taken(self):
        # Arrange
        vaccine_name = "Test"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, efficacy=1, alpha=0.3)]
        self.epidemic.generate_vaccine_stock_record()  # Generate the record in Epidemic.generate_vaccine_stock_record() first

        # Act
        self.epidemic.vaccine_stock_taken(self.epidemic.vaccine_ls[0])

        # Assert
        print(self.epidemic.vaccine_stocktake)
        self.assertEqual(self.epidemic.vaccine_stocktake[0][vaccine_name], 1)

    def test_vaccine_stock_taken_multiple_vaccine(self):
        # Arrange
        vaccine_name = "Test"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3), Vaccine(name=vaccine_name, dose=2, efficacy=1, alpha=0.3)]
        self.epidemic.generate_vaccine_stock_record()  # Generate the record in Epidemic.generate_vaccine_stock_record() first

        # Act
        self.epidemic.vaccine_stock_taken(self.epidemic.vaccine_ls[0])

        # Assert
        print(self.epidemic.vaccine_stocktake)
        self.assertEqual(self.epidemic.vaccine_stocktake[0][vaccine_name], 1)

    def test_generate_vaccine_dose_quota_records(self):
        # Arrange
        N = len(self.population)
        vaccine_name = "Test"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3)]

        # Act
        self.epidemic.generate_vaccine_dose_quota_records(N, self.epidemic.vaccine_ls)

        # Assert
        self.assertEqual(len(self.epidemic.vaccine_dose_quota), 1)
        self.assertEqual(self.epidemic.vaccine_dose_quota[vaccine_name + ":1"], N * self.epidemic.vaccine_ls[0].alpha_V)

    def test_generate_vaccine_dose_quota_records_multiple_doses(self):
        # Arrange
        N = len(self.population)
        vaccine_name = "Test"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3),
                                    Vaccine(name=vaccine_name, dose=2, efficacy=1, alpha=0.8)]

        # Act
        self.epidemic.generate_vaccine_dose_quota_records(N, self.epidemic.vaccine_ls)

        # Assert
        print(self.epidemic.vaccine_dose_quota)
        self.assertEqual(len(self.epidemic.vaccine_dose_quota), 2)
        self.assertEqual(self.epidemic.vaccine_dose_quota[vaccine_name + ":1"], N * self.epidemic.vaccine_ls[0].alpha_V)
        self.assertEqual(self.epidemic.vaccine_dose_quota[vaccine_name + ":2"],
                         N * self.epidemic.vaccine_ls[0].alpha_V * self.epidemic.vaccine_ls[1].alpha_V)

    def test_generate_vaccine_dose_quota_records_multiple_vaccine(self):
        # Arrange
        N = len(self.population)
        vaccine_name_01 = "Test_01"
        vaccine_name_02 = "Test_02"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name_01, dose=1, efficacy=1, alpha=0.3),
                                    Vaccine(name=vaccine_name_02, dose=1, efficacy=1, alpha=0.8)]

        # Act
        self.epidemic.generate_vaccine_dose_quota_records(N, self.epidemic.vaccine_ls)

        # Assert
        print(self.epidemic.vaccine_dose_quota)
        self.assertEqual(len(self.epidemic.vaccine_dose_quota), 2)
        self.assertEqual(self.epidemic.vaccine_dose_quota[vaccine_name_01 + ":1"],
                         N * self.epidemic.vaccine_ls[0].alpha_V)
        self.assertEqual(self.epidemic.vaccine_dose_quota[vaccine_name_02 + ":1"],
                         N * self.epidemic.vaccine_ls[1].alpha_V)

    def test_update_multi_dose_quota(self):
        # Arrange
        vaccine_name = "Test_01"
        vaccine_name_alt = "Test_02"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3),
                                    Vaccine(name=vaccine_name, dose=2, efficacy=1, alpha=0.8),
                                    Vaccine(name=vaccine_name_alt, dose=1, efficacy=1, alpha=0.8)]

        # Act
        mul_factor_01 = self.epidemic.update_multi_dose_quota(self.epidemic.vaccine_ls[1])
        mul_factor_02 = self.epidemic.update_multi_dose_quota(self.epidemic.vaccine_ls[2])

        # Assert
        self.assertEqual(mul_factor_01, self.epidemic.vaccine_ls[0].alpha_V * self.epidemic.vaccine_ls[1].alpha_V)
        self.assertEqual(mul_factor_02, self.epidemic.vaccine_ls[2].alpha_V)

    def test_vaccine_dose_record(self):
        # Arrange
        N = len(self.population)
        vaccine_name = "Test"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3)]
        self.epidemic.generate_vaccine_dose_quota_records(N, self.epidemic.vaccine_ls)

        # Act
        self.epidemic.vaccine_dose_record(self.epidemic.vaccine_ls[0])

        # Assert
        self.assertEqual(self.epidemic.vaccine_dose_quota[self.epidemic.vaccine_ls[0].brand+":"+str(self.epidemic.vaccine_ls[0].dose)], N * self.epidemic.vaccine_ls[0].alpha_V - 1)

    def test_vaccine_dose_flag_true(self):
        # Arrange
        N = len(self.population)
        vaccine_name = "Test_01"
        vaccine_name_alt = "Test_02"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3),
                                    Vaccine(name=vaccine_name, dose=2, efficacy=1, alpha=0.8),
                                    Vaccine(name=vaccine_name_alt, dose=1, efficacy=1, alpha=0.8)]
        self.epidemic.generate_vaccine_dose_quota_records(N, self.epidemic.vaccine_ls)

        # Act
        flag = self.epidemic.vaccine_dose_flag(self.epidemic.vaccine_ls[1])

        # Assert
        self.assertEqual(flag, True)

    def test_vaccine_dose_flag_false(self):
        # Arrange
        N = len(self.population)
        vaccine_name = "Test_01"
        vaccine_name_alt = "Test_02"
        self.epidemic.vaccine_ls = [Vaccine(name=vaccine_name, dose=1, efficacy=1, alpha=0.3)]
        self.epidemic.generate_vaccine_dose_quota_records(N, self.epidemic.vaccine_ls)
        self.epidemic.vaccine_dose_quota[self.epidemic.vaccine_ls[0].brand+":"+str(self.epidemic.vaccine_ls[0].dose)] = 0

        # Act
        flag = self.epidemic.vaccine_dose_flag(self.epidemic.vaccine_ls[0])

        # Assert
        self.assertEqual(flag, False)

    def test_vaccinate_mode20(self):
        self.fail()

    def test_vaccinate_mode21(self):
        self.fail()

    def test_vaccinate_mode22(self):
        self.fail()

    def test_vaccinate_mode23(self):
        self.fail()

    def test_vaccinate_mode24(self):
        self.fail()

    @mock.patch('random.randint', return_value = 0)
    def test_removed(self, mock_random_randint):
        self.epidemic.removed()

        self.assertEqual(self.population[0].removed, 1)

    def test_removed_mode07(self):
        self.fail()

    def test_removed_mode08(self):
        self.fail()

    def test_social_contact(self):
        self.fail()

    def test_overseas_infect(self):
        self.fail()

    @mock.patch('random.randint', return_value=0)
    def test_infect(self, mock_random_randint):
        for person in self.population:
            if person.id == 20:
                person.vaccinated = 1
            elif person.id == 31:
                person.removed = 1
            elif person.id == 33:
                person.suceptible = 1
                continue
            person.suceptible = 0

        self.epidemic.infect()

        for person in self.population:
            if person.id == 20:
                self.assertEqual(person.suceptible, 0)
            elif person.id == 31:
                self.assertEqual(person.suceptible, 0)
            elif person.id == 33:
                self.assertEqual(person.suceptible, 1)
            else:
                self.assertEqual(person.suceptible, 1)

    def test_infect_mode01(self):
        self.fail()

    def test_infect_mode07(self):
        self.fail()

    def test_infect_mode08(self):
        self.fail()

    def test_infect_mode11(self):
        self.fail()

    def test_infect_mode20(self):
        self.fail()

    def test_infect_nwk(self):
        self.fail()

    def test_infect_nwk_with_overseas_travel(self):
        self.fail()

    def test_infection_clock(self):
        self.population[0].suceptible = 1
        self.population[0].infection_clock = 15

        self.epidemic.infection_clock(0)

        self.assertEqual(self.population[0].exposed, 1)

    def test_infection_clock_JIT(self):
        self.population[0].suceptible = 1
        self.population[0].infection_clock = 14

        self.epidemic.infection_clock(0)

        self.assertEqual(self.population[0].exposed, 0)

    def test_infection_clock_not_sufficient_time(self):
        self.population[0].suceptible = 1

        self.epidemic.infection_clock(0)

        self.assertEqual(self.population[0].exposed, 0)

    def test_infected(self):
        self.population[0].suceptible = 1

        self.epidemic.infected()

        self.assertEqual(self.population[0].infection_clock, 1)

    def test_infected_not_I(self):
        self.population[0].suceptible = 0

        self.epidemic.infected()

        self.assertEqual(self.population[0].infection_clock, 0)

    @mock.patch('random.randint', return_value=0)
    def test_recovery(self, mock_random_randint):
        self.population[0].suceptible = 1

        self.epidemic.recovery()

        self.assertEqual(self.population[0].suceptible, 0)

    def test_recovery_mode11(self):
        self.fail()

    def test_immune(self):
        # Testing someone recover after certain days
        print(f'Immune time is {self.epidemic.immune_time} days. ')

        # Arrange
        self.population[0].suceptible = 1
        self.population[0].compartment_history = ['I'] * self.epidemic.immune_time
        self.population[0].compartment_history.append('S')

        # Act
        self.epidemic.immune()

        # Assert
        self.assertEqual(self.population[0].suceptible, 0)
        self.assertEqual(self.population[0].exposed, 0)

    def test_immune_mode10(self):
        self.fail()

    def test_immune_mode15(self):
        self.fail()

    @mock.patch('random.randint', return_value=0)
    def test_wear_off(self, mock_random_randint):
        # Arrange
        self.population[0].vaccinated = 1

        # Act
        self.epidemic.wear_off()

        # Assert
        self.assertEqual(self.population[0].vaccinated, 0)

    def test_wear_off_mode10(self):
        self.fail()

    def test_wear_off_mode15(self):
        self.fail()

    def test_testing(self):
        self.epidemic.testing()

        # Assert
        for person in self.population:
            if len(person.test_history) != 1:
                self.fail()
