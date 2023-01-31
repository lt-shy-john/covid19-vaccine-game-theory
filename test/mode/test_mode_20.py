from unittest import TestCase

from person import Person
from contact import ContactNwk
from mode import Mode05
from mode import Mode02
from mode import Mode20
import customLogger


class TestMode20(TestCase):
    def setUp(self) -> None:
        N = 6
        self.logger = customLogger.gen_logging('', 'debug')
        self.population = [Person() for x in range(N)]
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
        print(self.mode[20].theta, self.mode[20].local_infection_p)
        self.fail()

    def test_set_perceived_infection_overseas(self):
        # Arrange
        global_infection = 2
        self.mode[2] = Mode02(self.population, 0.14, self.logger)

        # Act
        self.mode[20].set_perceived_infection(global_infection)

        # Assert
        self.fail()

    def test_event_vaccinated(self):
        # Arrange

        # Act
        self.mode[20].event_vaccinated()

        # Assert
        self.fail()

    def test_event_vaccinated_mixed(self):
        # Arrange

        # Act
        self.mode[20].event_vaccinated_mixed()

        # Assert
        self.fail()

    def test_event_vaccinated_dfs(self):
        # Arrange
        self.mode[20].assign_costs()
        i = 0
        print("Self:", self.population[i].id, "Neighbour:", [p.id for p in self.contact_nwk.nwk_graph.neighbors(self.population[i])])

        # Act
        self.mode[20].event_vaccinated_dfs(i)

        # Assert
        print(self.mode[20].theta, self.mode[20].local_infection_p)

    def test_event_infected(self):
        # Arrange

        # Act
        self.mode[20].event_infected()

        # Assert
        self.fail()

    def test_event_infected_dfs(self):
        # Arrange

        # Act
        self.mode[20].event_infected_dfs()

        # Assert
        self.fail()

    def test_event_infected_mixed(self):
        # Arrange

        # Act
        self.mode[20].event_infected_mixed()

        # Assert
        self.fail()

    def test_get_payoff(self):
        # Arrange

        # Act
        self.mode[20].get_payoff()

        # Assert
        self.fail()

    def test_FDProb(self):
        # Arrange

        # Act
        self.mode[20].FDProb()

        # Assert
        self.fail()

    def test_get_infected_neighbours_number(self):
        # Arrange

        # Act
        self.mode[20].get_infected_neighbours_number()

        # Assert
        self.fail()

    def test_intimacy_game(self):
        # Arrange

        # Act
        self.mode[20].IntimacyGame()

        # Assert
        self.fail()