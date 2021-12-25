from person import Person
from contact import ContactNwk
import customLogger

from unittest import mock, TestCase
import networkx as nx

class TestContactNwk(TestCase):
    def setUp(self) -> None:
        N = 2
        self.population = [Person() for x in range(N)]
        self.contact_nwk = ContactNwk(self.population, False, customLogger.gen_logging('', False, None))

    def test_set_default_edge_list(self):
        self.contact_nwk.set_default_edge_list()
        self.assertNotEqual(self.contact_nwk.network, None)
        self.assertEqual(len(self.contact_nwk.network), len(self.population)//2)  # Assert that they are in pairs

    def test_set_default_edge_list_odd_numbered_population(self):
        # Reset the before method
        N = 3
        self.population = [Person() for x in range(N)]
        self.contact_nwk = ContactNwk(self.population, False, customLogger.gen_logging('', False, None))

        self.contact_nwk.set_default_edge_list()
        self.assertNotEqual(self.contact_nwk.network, None)
        self.assertEqual(len(self.contact_nwk.network), (len(self.population)//2) + 1)  # Assert that they are in pairs

    @mock.patch('networkx.draw')
    @mock.patch('networkx.draw_networkx_labels')
    @mock.patch('matplotlib.pyplot.show')
    def test_show_nwk(self, mock_nx_draw, mock_nx_nx_labels, mock_plt_show):
        self.contact_nwk.set_default_edge_list()
        self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)

        self.contact_nwk.show_nwk()  # In fact no nodes are shown since they are not initiated at the start

    def test_update_nwk_remove_nodes(self):
        # The method name reflects the method may have more functionalities added in the future
        self.contact_nwk.set_default_edge_list()
        self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)

        for node in self.contact_nwk.nwk_graph.nodes:
            node.removed = 1

        self.contact_nwk.update_nwk()

        self.assertEqual(self.contact_nwk.nwk_graph.number_of_nodes(), 0)

    @mock.patch('random.randint', return_value=1) # I do not want to shuffle the temp list since the randomness part of the tested functionality
    def test_update_xulvi_brunet_sokolov_no_updates(self, mock_random_randint):
        N = 5
        self.population = [Person() for x in range(N)]
        self.contact_nwk = ContactNwk(self.population, False, customLogger.gen_logging('', False, None))
        self.contact_nwk.PUpdate = 0

        self.contact_nwk.set_default_edge_list()
        self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)

        old_nwk_ls =  self.contact_nwk.network

        self.contact_nwk.update_xulvi_brunet_sokolov()

        self.assertEqual(old_nwk_ls, self.contact_nwk.network)


    @mock.patch('random.randint', return_value=0) # I do not want to shuffle the temp list since the randomness part of the tested functionality
    def test_update_xulvi_brunet_sokolov_assortative(self, mock_random_randint):
        @mock.patch('random.randint',
                    return_value=1)  # I do not want to shuffle the temp list since the randomness part of the tested functionality
        def test_update_xulvi_brunet_sokolov_no_updates(self, mock_random_randint):
            N = 5
            self.population = [Person() for x in range(N)]
            self.contact_nwk = ContactNwk(self.population, False, customLogger.gen_logging('', False, None))
            self.contact_nwk.PUpdate = 0
            self.contact_nwk.assort = True  # Test if assortative update then next step will see higher assortativity

            self.contact_nwk.set_default_edge_list()
            self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)

            old_assortativeness = nx.degree_assortativity_coefficient(self.contact_nwk.nwk_graph)

            self.contact_nwk.update_xulvi_brunet_sokolov()

            self.assertTrue(old_assortativeness < nx.degree_assortativity_coefficient(self.contact_nwk.nwk_graph))

    # def test_update_random_nwk(self):
    #     self.contact_nwk.set_default_edge_list()
    #     self.contact_nwk.nwk_graph = nx.Graph(self.contact_nwk.network)
    #
    #     self.contact_nwk.update_random_nwk()
