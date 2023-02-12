import random
from unittest import mock, TestCase

from person import Person
from contact import ContactNwk
from mode import Mode05
from mode import Mode20
import customLogger


class TestMode20(TestCase):
    def setUp(self) -> None:
        N = 6
        self.logger = customLogger.gen_logging('', 'debug')
        self.population = [Person() for x in range(N)]
        for i in range(len(self.population)):
            # Reset IDs
            self.population[i].id = i+1
        self.contact_nwk = ContactNwk(self.population, False, self.logger)
        self.mode = {5: Mode05(self.population, self.contact_nwk, self.logger), 20: Mode20(self.population, self.contact_nwk, 0.14, self.logger)}
        self.mode[5].read_data("1-2 1-3 2-4 2-5 3-5 3-6")

    def test_set_perceived_infection(self):
        # Arrange
        self.population[0].suceptible = 1
        global_infection = 1

        # Act
        self.mode[20].set_perceived_infection(global_infection)

        # Assert
        expected_theta = [0, 1, 1, 0, 0, 0]
        expected_local_infection_p = [0, 1, 1, 0, 0, 0]
        expected_global_infection_p = [1, 0, 0, 1, 1, 1]
        assert expected_theta == self.mode[20].theta.tolist()
        assert expected_local_infection_p == self.mode[20].local_infection_p.tolist()
        assert expected_global_infection_p == self.mode[20].global_infection_p.tolist()

    @mock.patch('random.choice')
    def test_event_vaccinated_mixed(self, mock_random_choice):
        # Arrange
        self.mode[20].assign_costs()
        idx = 0

        for i in range(len(self.population)):
            # Mock cost as 1
            self.population[i].cV = 0

        mock_random_choice.return_value = self.population[1]

        # Act
        self.mode[20].event_vaccinated_mixed(idx)

        # Assert
        for i in range(len(self.population)):
            if self.mode[20].kV * self.mode[20].sV == self.population[i].cV:
                return
        self.fail()

    def test_event_vaccinated_dfs(self):
        # Arrange
        '''
        Note:
            * Assume id 1 just vaccinated, add vaccination costs to others
        '''
        self.mode[20].assign_costs()
        idx = self.population.index([_ for _ in self.population if _.id == 1][0])
        print("Self:", self.population[idx].id, ", Neighbour:", [p.id for p in self.contact_nwk.nwk_graph.neighbors(self.population[idx])])

        for i in range(len(self.population)):
            # Mock cost as 1
            self.population[i].cV = 0

        # Act
        self.mode[20].event_vaccinated_dfs(idx)

        # Assert
        actual = [p.cV for p in self.population]
        exp_add_C = self.mode[20].kV*self.mode[20].sV
        expected = [0, exp_add_C, exp_add_C, exp_add_C ** 2, exp_add_C ** 2, exp_add_C ** 2]
        self.assertEqual(expected, actual)

    def test_event_infected_dfs(self):
        # Arrange
        '''
        Note:
            * Assume id 1 just infected, add infection costs to others
        '''
        self.mode[20].assign_costs()
        idx = self.population.index([_ for _ in self.population if _.id == 1][0])
        print("Self:", self.population[idx].id, ", Neighbour:",
              [p.id for p in self.contact_nwk.nwk_graph.neighbors(self.population[idx])])

        for i in range(len(self.population)):
            # Mock cost as 1
            self.population[i].cI = 0

        # Act
        self.mode[20].event_infected_dfs(idx)

        # Assert
        actual = [p.cI for p in self.population]
        exp_add_C = self.mode[20].kI * self.mode[20].sI
        expected = [0, exp_add_C, exp_add_C, exp_add_C ** 2, exp_add_C ** 2, exp_add_C ** 2]
        self.assertEqual(expected, actual)

    @mock.patch('random.choice')
    def test_event_infected_mixed(self, mock_random_choice):
        # Arrange
        self.mode[20].assign_costs()
        idx = 0

        for i in range(len(self.population)):
            # Mock cost as 1
            self.population[i].cI = 0

        mock_random_choice.return_value = self.population[1]

        # Act
        self.mode[20].event_infected_mixed(idx)

        # Assert
        for i in range(len(self.population)):
            if self.mode[20].kI * self.mode[20].sI == self.population[i].cI:
                return
        self.fail()

    def test_get_payoff(self):
        # Arrange
        idx = 1
        self.population[idx].cV = 0
        self.population[idx].cI = 0

        # Act
        result = self.mode[20].get_payoff(idx)

        # Assert
        self.assertEqual(0, result)

    @mock.patch('mode.Mode20.get_payoff')
    def test_FDProb(self, mock_get_payoff):
        # Arrange
        idx = 1
        mock_get_payoff.return_value = 0
        # Act
        result = self.mode[20].FDProb(idx)

        # Assert
        self.assertEqual(0.5 , result)

    def test_get_infected_neighbours_number_no_infection(self):
        # Arrange
        idx = 1

        # Act
        result = self.mode[20].get_infected_neighbours_number(idx)

        # Assert
        self.assertEqual(0, result)

    def test_get_infected_neighbours_number_some_infection(self):
        # Arrange
        idx = 1
        neighbour = random.choice(list(self.contact_nwk.nwk_graph.neighbors(self.population[idx])))
        neighbour.suceptible = 1

        # Act
        result = self.mode[20].get_infected_neighbours_number(idx)

        # Assert
        self.assertEqual(1, result)
