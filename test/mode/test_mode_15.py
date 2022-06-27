from unittest import TestCase

from person import Person
from vaccine import Vaccine
from mode import Mode15
import customLogger

class TestMode15(TestCase):
    def setUp(self) -> None:
        N = 5
        self.logger = customLogger.gen_logging('', None)
        self.population = [Person() for x in range(N)]
        self.mode = {15: Mode15(self.population, self.logger)}

    def test_create_vaccine_type(self):
        self.fail()

    def test_check_multi_dose_vaccine(self):
        self.fail()

    def test_check_latest_dose(self):
        self.fail()

    def test_check_recent_vaccine_one_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3)]
        self.population[0].vaccine_history = [0, 0, 'Test_01:1', 0, 0, 0, 0, 0]

        # Act
        recent_vaccine = self.mode[15].check_recent_vaccine(0, self.vaccine_ls)

        # Assert
        self.assertEqual(recent_vaccine, self.vaccine_ls[0])

    def test_check_recent_vaccine_two_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3),
                                    Vaccine(name="Test_01", dose=2, efficacy=0, alpha=0.3)]
        self.population[0].vaccine_history = [0, 0, 'Test_01:1', 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 'Test_01:1', 'Test_01:2', 0, 0, 0, 0]

        # Act
        recent_vaccine_0 = self.mode[15].check_recent_vaccine(0, self.vaccine_ls)
        recent_vaccine_1 = self.mode[15].check_recent_vaccine(1, self.vaccine_ls)

        # Assert
        self.assertEqual(recent_vaccine_0, self.vaccine_ls[0])
        self.assertEqual(recent_vaccine_1, self.vaccine_ls[1])

    def test_check_recent_vaccine_three_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=2, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=3, efficacy=0, alpha=0.3)]
        self.population[0].vaccine_history = [0, 0, 'Test_01:1', 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 'Test_01:1', 'Test_01:2', 0, 0, 0, 0]
        self.population[2].vaccine_history = [0, 'Test_01:1', 0, 'Test_01:2', 'Test_01:3', 0, 0, 0]

        # Act
        recent_vaccine_0 = self.mode[15].check_recent_vaccine(0, self.vaccine_ls)
        recent_vaccine_1 = self.mode[15].check_recent_vaccine(1, self.vaccine_ls)
        recent_vaccine_2 = self.mode[15].check_recent_vaccine(2, self.vaccine_ls)

        # Assert
        self.assertEqual(recent_vaccine_0, self.vaccine_ls[0])
        self.assertEqual(recent_vaccine_1, self.vaccine_ls[1])
        self.assertEqual(recent_vaccine_2, self.vaccine_ls[2])

    def test_check_recent_vaccine_four_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=2, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=3, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=4, efficacy=0, alpha=0.3)]
        self.population[0].vaccine_history = [0, 0, 'Test_01:1', 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 'Test_01:1', 'Test_01:2', 0, 0, 0, 0]
        self.population[2].vaccine_history = [0, 'Test_01:1', 0, 'Test_01:2', 'Test_01:3', 0, 0, 0]
        self.population[3].vaccine_history = [0, 'Test_01:1', 0, 'Test_01:2', 'Test_01:3', 'Test_01:4', 0, 0]

        # Act
        recent_vaccine_0 = self.mode[15].check_recent_vaccine(0, self.vaccine_ls)
        recent_vaccine_1 = self.mode[15].check_recent_vaccine(1, self.vaccine_ls)
        recent_vaccine_2 = self.mode[15].check_recent_vaccine(2, self.vaccine_ls)
        recent_vaccine_3 = self.mode[15].check_recent_vaccine(3, self.vaccine_ls)

        # Assert
        self.assertEqual(recent_vaccine_0, self.vaccine_ls[0])
        self.assertEqual(recent_vaccine_1, self.vaccine_ls[1])
        self.assertEqual(recent_vaccine_2, self.vaccine_ls[2])
        self.assertEqual(recent_vaccine_3, self.vaccine_ls[3])

    def test_check_next_vaccine_one_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3)]

        # Act
        next_vaccine_0 = self.mode[15].check_next_vaccine(0, self.vaccine_ls, None)
        next_vaccine_1 = self.mode[15].check_next_vaccine(0, self.vaccine_ls, self.vaccine_ls[0])

        # Assert
        self.assertEqual(self.vaccine_ls[0], next_vaccine_0)
        self.assertEqual(None, next_vaccine_1)

    def test_check_next_vaccine_two_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=2, efficacy=0, alpha=0.3)]

        # Act
        next_vaccine_0 = self.mode[15].check_next_vaccine(0, self.vaccine_ls, self.vaccine_ls[0])
        next_vaccine_1 = self.mode[15].check_next_vaccine(1, self.vaccine_ls, self.vaccine_ls[1])

        # Assert
        self.assertEqual(self.vaccine_ls[1], next_vaccine_0)
        self.assertEqual(None, next_vaccine_1)

    def test_check_next_vaccine_three_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=2, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=3, efficacy=0, alpha=0.3)]

        # Act
        next_vaccine_0 = self.mode[15].check_next_vaccine(0, self.vaccine_ls, self.vaccine_ls[0])
        next_vaccine_1 = self.mode[15].check_next_vaccine(1, self.vaccine_ls, self.vaccine_ls[1])
        next_vaccine_2 = self.mode[15].check_next_vaccine(1, self.vaccine_ls, self.vaccine_ls[2])

        # Assert
        self.assertEqual(self.vaccine_ls[1], next_vaccine_0)
        self.assertEqual(self.vaccine_ls[2], next_vaccine_1)
        self.assertEqual(None, next_vaccine_2)

    def test_check_next_vaccine_four_dose(self):
        # Arrange
        self.vaccine_ls = [Vaccine(name="Test_01", dose=1, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=2, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=3, efficacy=0, alpha=0.3),
                           Vaccine(name="Test_01", dose=4, efficacy=0, alpha=0.3)]

        # Act
        next_vaccine_0 = self.mode[15].check_next_vaccine(0, self.vaccine_ls, self.vaccine_ls[0])
        next_vaccine_1 = self.mode[15].check_next_vaccine(1, self.vaccine_ls, self.vaccine_ls[1])
        next_vaccine_2 = self.mode[15].check_next_vaccine(1, self.vaccine_ls, self.vaccine_ls[2])
        next_vaccine_3 = self.mode[15].check_next_vaccine(1, self.vaccine_ls, self.vaccine_ls[3])

        # Assert
        self.assertEqual(self.vaccine_ls[1], next_vaccine_0)
        self.assertEqual(self.vaccine_ls[2], next_vaccine_1)
        self.assertEqual(self.vaccine_ls[3], next_vaccine_2)
        self.assertEqual(None, next_vaccine_3)

    def test_write_vaccine_history(self):
        self.fail()

    def test_take_multi_dose_vaccine(self):
        self.fail()
