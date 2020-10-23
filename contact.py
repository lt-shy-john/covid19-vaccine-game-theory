import random
import networkx as nx
from matplotlib import pyplot as plt

import person

class ContactNwk:

    def __init__(self, people):
        self.people = people
        self.group_no = None
        self.network = None  # Graph to show partner topology
        # From now network is defined by modes 50 - 59.
        self.nwk_graph = nx.Graph(self.network)

        # Probability to change bonds
        self.l0 = 0.5
        self.l1 = 0.5

    def set_dedault_edge_list(self):
        '''
        Generate edge list and set Contact.network. By default edge list is in disjoint pairs.
        '''
        temp_roster = self.people
        random.shuffle(temp_roster)
        self.network = list(zip(temp_roster[:len(temp_roster)//2],temp_roster[len(temp_roster)//2:]))
        if len(self.people) % 2 == 1:
            self.network.append((self.people[-1], None))

    def show_nwk(self):
        pos = nx.random_layout(self.nwk_graph)
        labels = {}
        for node in self.nwk_graph.nodes:
            if type(node) == person.Person:
                labels[node] = node.id
        nx.draw(self.nwk_graph, pos=pos,with_labels=False)
        nx.draw_networkx_labels(self.nwk_graph,pos=pos,labels=labels,font_size=16)
        plt.show()

    def update_nwk(self):
        '''
        Replaced by other update_nwk methods based on their type.
        '''
        print('Warning: This code still uses an obselete method: Contact.update_nwk(). ')
        pass

    def update_random_nwk(self):
        '''
        At each time, contact clusters changed.
        '''
        for s_node in self.nwk_graph.nodes():
            for t_node in self.nwk_graph.nodes():
                seed = random.randint(0,10000)/10000
                # Bond
                if seed < self.l1 and ((s_node.id,t_node.id) not in self.network or (t_node.id,s_node.id) not in self.network):
                    self.nwk_graph.add_edge(s_node.id,t_node.id)

                # De-bond
                if seed < self.l0:
                    if (s_node.id,t_node.id) in self.network:
                        self.nwk_graph.remove_edge(s_node.id,t_node.id)
                    elif (t_node.id,s_node.id) in self.network:
                        self.nwk_graph.remove_edge(t_node.id,s_node.id)
