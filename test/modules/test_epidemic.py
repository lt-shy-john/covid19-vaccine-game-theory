import random

from person import Person
from vaccine import Vaccine
from contact import ContactNwk
from epidemic import Epidemic
import customLogger

from mode import Mode01
from mode import Mode02
from mode import Mode04
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
        logger = customLogger.gen_logging('', False, None)
        self.population = [Person() for x in range(N)]
        self.contact_nwk = ContactNwk(self.population, False, logger)
        self.contact_nwk.set_default_edge_list()
        self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)
        self.epidemic = Epidemic(0, 0.14, 0.05, 0.000005, 0.000005, self.population, 0.5, 20, {}, self.contact_nwk, False, logger)

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
        self.fail()

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
        self.fail()

    def test_start_epidemic_mode501(self):
        self.fail()

    def test_start_epidemic_mode501_505(self):
        self.fail()

    def test_start_epidemic_mode505(self):
        self.fail()

    def test_start_epidemic_mode505_501(self):
        self.fail()

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
        self.fail()

    def test_vaccinate_mode15(self):
        self.fail()

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

    def test_removed(self):
        self.fail()

    def test_removed_mode07(self):
        self.fail()

    def test_removed_mode08(self):
        self.fail()

    def test_social_contact(self):
        self.fail()

    def test_overseas_infect(self):
        self.fail()

    def test_infect(self):
        self.fail()

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
        self.fail()

    def test_infected(self):
        self.fail()

    def test_recovery(self):
        self.fail()

    def test_recovery_mode11(self):
        self.fail()

    def test_immune(self):
        self.fail()

    def test_immune_mode10(self):
        self.fail()

    def test_immune_mode15(self):
        self.fail()

    def test_wear_off(self):
        self.fail()

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
