from person import Person
from contact import ContactNwk
from simulation import Simulation
import customLogger

from mode import Mode01

from unittest import mock, TestCase

class TestSimulation(TestCase):
    def setUp(self) -> None:
        N = 50
        T = 10
        self.population = [Person() for x in range(N)]
        self.logger = customLogger.gen_logging('', None)
        self.contact_nwk = ContactNwk(self.population, False, self.logger)
        alpha, beta, gamma, delta, phi = (0, 0.14, 0.05, 0.000005, 0)
        test_rate = 0.0001
        immune_time = 180
        vaccine_available = None
        vaccine_cap_filename = None
        verbose_mode = False
        self.simulation = Simulation(N, T, self.population, self.contact_nwk, None, alpha, 0.14, 0.05, 0, 0.000005, None, alpha, alpha,
                                     beta, beta, beta, beta, beta, beta, beta, beta, beta, beta, beta, beta, beta, beta,
                                     test_rate, immune_time, vaccine_available, vaccine_cap_filename,
                                     verbose_mode, self.logger, 'info')

    def test_load_modes(self):
        # Arrange
        modes = {1: Mode01(self.population, self.logger, [0, 0])}

        # Act
        self.simulation.load_modes(modes)

        # Assert
        self.assertTrue(len(self.simulation.modes) == 1)
