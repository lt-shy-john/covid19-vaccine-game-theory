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
        self.assort = True

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

    def update_xulvi_brunet_sokolov(self):
        '''
        Update the network. In ContactNwk().
        '''
        deg_ls = dict(self.nwk_graph.degree)  # Need this in the loop.

        tmp_edge_ls = [e for e in self.nwk_graph.edges]
        random.shuffle(tmp_edge_ls)
        edge_pairs_idx = 0
        while edge_pairs_idx < len(tmp_edge_ls):
            if edge_pairs_idx == len(tmp_edge_ls)-1:
                break
            pair_nodes = [*tmp_edge_ls[edge_pairs_idx], *tmp_edge_ls[edge_pairs_idx+1]]
            edge_pairs_idx += 2

            # Sort by degree
            pair_nodes_dict = dict([(x, deg_ls[x]) for x in pair_nodes])
            pair_nodes_sorted = sorted(pair_nodes_dict, key=pair_nodes_dict.get, reverse=True)

            if self.assort == True:
                # Rebond then debond
                self.nwk_graph.remove_edge(pair_nodes[0], pair_nodes[1])
                self.nwk_graph.remove_edge(pair_nodes[2], pair_nodes[3])
                if len(pair_nodes_sorted) == 4:
                    self.nwk_graph.add_edge(pair_nodes_sorted[0], pair_nodes_sorted[1])
                    self.nwk_graph.add_edge(pair_nodes_sorted[2], pair_nodes_sorted[3])
                else:
                    self.nwk_graph.add_edge(pair_nodes_sorted[0], pair_nodes_sorted[1])
                    self.nwk_graph.add_edge(pair_nodes_sorted[1], pair_nodes_sorted[2])
            else:
                # Rebond then debond
                self.nwk_graph.remove_edge(pair_nodes[0], pair_nodes[1])
                self.nwk_graph.remove_edge(pair_nodes[2], pair_nodes[3])
                if len(pair_nodes_sorted) == 4:
                    self.nwk_graph.add_edge(pair_nodes_sorted[0], pair_nodes_sorted[3])
                    self.nwk_graph.add_edge(pair_nodes_sorted[1], pair_nodes_sorted[2])
                else:
                    self.nwk_graph.add_edge(pair_nodes_sorted[0], pair_nodes_sorted[2])

        # Add edge list to contact_nwk.network
        self.network = [e for e in self.nwk_graph.edges]


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

        # Add edge list to contact_nwk.network
        self.contact_nwk.network = [e for e in self.contact_nwk.nwk_graph.edges]