from unittest import TestCase

from person import Person
from mode import Mode43
import customLogger

class TestMode43(TestCase):
    def setUp(self) -> None:
        N = 5
        self.logger = customLogger.gen_logging('', None)
        self.population = [Person() for x in range(N)]
        self.mode = {43: Mode43(self.population, self.logger, None)}

    def test_correct_instructions_format(self):
        # Arrange
        self.mode[43].instructions = {'V': 0, '1I': 0, '2V': 0, 'V3': 0, '2V1I':0, '2I1V': 0}

        # Act
        self.mode[43].correct_instructions_format()

        # Assert
        for k in self.mode[43].instructions.keys():
            self.assertTrue(k in ['V', 'I', '2V', '3V', '2V1I', '1V2I'], k)

    def test_count_vaccine_taken(self):
        # Arrange
        self.population[0].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        self.population[2].vaccine_history = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        self.population[3].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[4].vaccine_history = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        results = []

        # Act
        for i in range(len(self.population)):
            results.append(self.mode[43].count_vaccine_taken(i))

        # Assert
        for i in range(len(self.population)):
            self.assertEqual(results[i], sum(self.population[i].vaccine_history))

    def test_count_vaccine_taken_brand(self):
        '''
        Test when instructions specifically looks for a particular brand.
        '''
        # Arrange
        self.population[0].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 0, 0, 'Sample:1', 0, 'Sample:2', 0, 0, 0]
        self.population[2].vaccine_history = [0, 0, 0, 0, 'Sample:1', 0, 0, 0, 0, 0]
        self.population[3].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[4].vaccine_history = ['Sample:1', 0, 0, 0, 0, 0, 0, 0, 0, 0]

        results = []
        expected = [0, 2, 1, 0, 1]

        # Act
        for i in range(len(self.population)):
            results.append(self.mode[43].count_vaccine_taken(i))

        # Assert
        for i in range(len(self.population)):
            self.assertEqual(results[i], expected[i])

    def test_count_infected_times(self):
        # Arrange
        self.population[0].compartment_history = ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
        self.population[1].compartment_history = ['E', 'E', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[2].compartment_history = ['S', 'E', 'E', 'I', 'S', 'E', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[3].compartment_history = ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                                                  'E']
        self.population[4].compartment_history = ['E', 'I', 'S', 'E', 'I', 'S', 'E', 'S', 'S', 'E', 'S', 'S', 'S', 'S',
                                                  'S']

        actual = []
        expected = [0, 1, 2, 1, 4]

        # Act
        for i in range(len(self.population)):
            actual.append(self.mode[43].count_infected_times(i))

        # Assert
        for i in range(len(self.population)):
            self.assertEqual(actual[i], expected[i])

    def test_get_immune_time(self):
        # Arrange
        self.mode[43].instructions = {'V': 0, '1I': 0, '2V': 0, 'V3': 0, '2V1I':0, '2I1V': 0}

        self.population[0].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        self.population[2].vaccine_history = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        self.population[3].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[4].vaccine_history = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.population[0].compartment_history = ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[1].compartment_history = ['E', 'E', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[2].compartment_history = ['S', 'E', 'E', 'I', 'S', 'E', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[3].compartment_history = ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                                                  'E']
        self.population[4].compartment_history = ['E', 'I', 'S', 'E', 'I', 'S', 'E', 'S', 'S', 'E', 'S', 'S', 'S', 'S',
                                                  'S']

        results = []
        expected = []

        # Act
        for i in range(len(self.population)):
            results.append(self.mode[43].get_immune_time(i))

        # Assert
        self.fail()

    def test_get_immune_time_vaccine_brand(self):
        '''
        Test when instructions specifically looks for a particular brand.
        '''
        # Arrange
        self.mode[43].instructions = {'V': 0, '1I': 0, '2V': 0, 'V3': 0, '2V1I':0, '2I1V': 0}

        self.population[0].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[1].vaccine_history = [0, 0, 0, 0, 'Sample:1', 0, 'Sample:2', 0, 0, 0]
        self.population[2].vaccine_history = [0, 0, 0, 0, 'Sample:1', 0, 0, 0, 0, 0]
        self.population[3].vaccine_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.population[4].vaccine_history = ['Sample:1', 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.population[0].compartment_history = ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[1].compartment_history = ['E', 'E', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[2].compartment_history = ['S', 'E', 'E', 'I', 'S', 'E', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S',
                                                  'S']
        self.population[3].compartment_history = ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                                                  'E']
        self.population[4].compartment_history = ['E', 'I', 'S', 'E', 'I', 'S', 'E', 'S', 'S', 'E', 'S', 'S', 'S', 'S',
                                                  'S']

        results = []
        expected = []

        # Act
        for i in range(len(self.population)):
            results.append(self.mode[43].get_immune_time(i))

        # Assert
        self.fail()