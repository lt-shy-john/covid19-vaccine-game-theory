from person import Person
import random
import networkx as nx

class Mode:
    def __init__(self, people, code):
        self.code = code
        # Flag to alert setting has been loaded.
        self.flag = ' '   # If loaded then has value 'X'.
        # Population objects
        self.people = people

    def raise_flag(self):
        '''
        If loaded then has value 'X'.
        '''
        self.flag = 'X'

    def drop_flag(self):
        '''
        If settings unloaded then mute the flagged icon.
        '''
        self.flag = ' '

'''
=======================================================

Individual mode settings

=======================================================
'''


'''
01: Living in city/ rural
'''
class Mode01(Mode):
    '''
    Attributes
    ----------
    weight: {city, rural}
        Proportion of residents in city and rural respectively.
    betas: {city, rural}
        The infection rate while living in city or rural environment.
    '''

    def __init__(self, people, betas=[0.5,0.5]):
        super().__init__(people,1)
        self.weight = [4,6]
        self.betas = betas

    def set_weight(self, c, r):
        self.weight = [c,r]
        self.check_weight_integrity()

    def check_weight_integrity(self):
        if sum(self.weight) > 1:
            print('Warning: Weights too much. Set uniform proportion for city and suburban proportion. ')
            self.weight[0] = self.weight[1] = 5
        elif sum(self.weight) < 1:
            print('Warning: Weights too less. Proportion of rural residents is set to complement of city proportion. ')
            self.weight[1] = 1 - self.weight[0]

    def assign_regions(self):
        for person in self.people:
            person.location = random.choices(list(range(2)), weights = self.weight, k=1)[0]

    def __call__(self):
        '''
        When mode 1 is created.
        '''
        beta_city, beta_rural = self.betas[0], self.betas[1]
        prop_city, prop_rural = self.weight[0], self.weight[1]

        print('-------------------------')
        print('You are creating mode 1. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        beta_city_temp = input('City >>> ')
        beta_city = self.set_correct_epi_para(beta_city_temp, beta_city)
        self.set_beta(0, beta_city)
        beta_rural_temp = input('Rural >>> ')
        beta_rural = self.set_correct_epi_para(beta_rural_temp, beta_rural)
        self.set_beta(1, beta_rural)

        print('\nPlease set proportional parameter below. ')
        prop_city_temp = input('City >>> ')
        prop_city = self.set_correct_epi_para(prop_city_temp, prop_city)
        prop_rural_temp = input('Rural >>> ')
        prop_rural = self.set_correct_epi_para(prop_rural_temp, prop_rural)
        prop_city, prop_rural = self.weight[0], self.weight[1]
        print('{}: {}, {}: {}'.format(self.betas[0], self.betas[1], self.weight[0], self.weight[1]))
        print('We are assigning the population to regions.')
        self.assign_regions()
        self.raise_flag()
        print('\nMode 1 equipped. \n')

    def set_beta(self, idx, value):
        '''
        Set infection rate for each region.

        Arguments
        ---------
        idx: int
            The index according to Mode01.betas.
        '''
        self.betas[idx] = value

    def correct_epi_para(self, p):
        '''
        Convert epidemic parameters into floats.

        Parameters
        - p: Epidemic rate, positive decimal less than 1.
        '''
        try:
            p_num = float(p)
            if p_num < 0 or p_num > 1:
                p_num = 0
                print('Please check your inputs and change them in SETTING.')
            return p_num
        except ValueError:
            p_num = 0
            print('Please check your inputs and change them in SETTING.')
            return p_num

    def set_correct_epi_para(self, p, P):
        '''
        Convert the parameters into integers. If input is blank then do nothing.

        Parameters:
        p -- string input.
        P -- original value.
        pos -- If the parameter is positive number.
        '''
        if p == '':
            return P
        else:
            return self.correct_epi_para(p)

    def infect_01(self, idx, p):
        '''
        Model different infection rate due to residence.
        '''
        if self.people[idx].location == 0 and p < self.betas[0]:
            self.people[idx].suceptible = 1
        elif self.people[idx].location == 1 and p < self.betas[1]:
            self.people[idx].suceptible = 1


'''
02: Travel from overseas
'''
class Mode02(Mode):
    def __init__(self, people):
        super().__init__(people,2)
        self.overseas = {'Some Places': 0}
        self.rS = 1
        self.rI = 1

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 2. ')
        print('-------------------------\n')
        print('Please set the parameters below. ')
        self.raise_flag()

    def create_setting(self):
        '''
        Assign values to population
        '''
        pass

    def make_decision(self):
        '''
        Make decision based on circumstances in each time step.
        '''
        pass

    def get_Mode02E1(self, i):
        '''
        Utility function for someone (i-th person) decides to travel
        '''
        return -self.people[i].A * self.beta * self.rI

    def get_Mode02E0(self, i):
        '''
        Utility function for someone (i-th person) decides not to travel
        '''
        return -self.rS

'''
04: Bounded rationality of vaccine
'''
class Mode04(Mode):
    def __init__(self, people):
        super().__init__(people,4)

    def __call__(self):
        self.raise_flag()

'''
05: Edit partner network
'''
class Mode05(Mode):
    def __init__(self, people, g):
        super().__init__(people,5)
        self.g = g   # Import from ContactNwk object. Graph of social network
        self.data = None # User requests to change social network topology


    def view_network(self):
        '''
        Import graph from main.py and view them.
        '''
        try:
            self.g.show_nwk()
        except NameError:
            print('Topology will be generated after the first run.')
            pass

    def read_data(self):
        # Parse data stream
        self.data = self.data.split()
        for i in range(len(self.data)):
            self.data[i] = self.data[i].split('-')
            # print(self.data[i][0],self.data[i][1])
        tmp_container = []
        for i in range(len(self.data)):
            # print(self.data[i])
            for j in range(len(self.people)):
                if self.people[j].id == int(self.data[i][0]) or self.people[j].id == int(self.data[i][1]):
                    tmp_container.append(self.people[j])
                    # print(tmp_container)
                if len(tmp_container) == 2:
                    if self.g.network == None:
                        self.g.network = []
                    self.g.network.append(tuple(tmp_container))
                    self.g.nwk_graph.add_edges_from([tuple(tmp_container)])
                    tmp_container = []
                    print('Added')
                    break
        self.data = None

    def __call__(self):
        print('-------------------------')
        print('You are editing mode 5. ')
        print('-------------------------\n')
        cmd = None
        while cmd != 'y':
            print('Please review the contact network.')
            self.view_network()

            print('Input the agents you wished to connect... ')
            print('Agents are linked by "-" and pairs separated by space.')
            self.data = input('> ')
            self.read_data()
            if self.data != '':
                self.raise_flag()

            cmd = input('Do you want to leave? [y/n]')
            if cmd == 'y':
                return

'''
06: Risk compensation (%)
'''
class Mode06(Mode):
    '''
    Attributes
    ----------
    condom_rate: iterable of floats
        Frequency of condoms. Highest, median and lowest.
    '''

    def __init__(self, people, contact_nwk):
        super().__init__(people,6)
        self.contact_nwk = contact_nwk
        # Proportion of condom usage groups.
        self.condom_proportion = [0.34, 0.33, 0.33]
        # Frequency of replacing condoms.
        self.condom_rate = [0.85, 0.5, 0.03]
        # Each agent has their own risk compensation (i.e. replacement of condoms)


    def set_condom_rate(self, h, m, l=0):
        try:
            self.condom_rate[0] = float(h)
            self.condom_rate[1] = float(m)
            self.condom_rate[2] = float(l)

            # Sort the list to descending order
            self.condom_rate.sort(reverse=True)

            # Check sum if they are normalised
            if sum(self.condom_rate) < 1:
                print('Sum of condom rate is less than 1. Please check your inputs.')
                self.condom_rate[1] = 1 - self.condom_rate[0]
                self.condom_rate[2] = 0
            elif sum(self.condom_rate) > 1:
                print('Sum of condom rate is greater than 1. Please check your inputs.')
                self.condom_rate = [0.8, 0.15, 0.05]

        except ValueError:
            print('Wrong data type. Please check your data')

    def set_population(self):
        '''
        Set whom uses condom and their habits.

        parameter
        ---------
        input: iterable, optional
            Define frequency and their condom use.

        Notes
        -----
        0 represents infrequent use of condom, 1 means user group lies in the median and 2 has the highest frequency.

        '''
        for person in self.people:
            person.condom_group = random.choices(list(range(3)), weights = self.condom_proportion, k=1)[0]

    def infect_condom_use(self, beta, sex_rate):
        '''
        Sexual intercourse when condom involved. Overide the normal `Epidemic.infect()` function.

        Parameters
        ----------
        sex_rate: float
            From epidemic class. Represents population frequency of making sexual intercourse.
        '''


        for pair in self.contact_nwk.network:
            sex_seed = random.randint(0,1000)/1000
            if sex_seed > sex_rate:
                # Not making sex
                pair[0].condom_history.append(0)
                pair[1].condom_history.append(0)
                continue
            condom_seed = random.randint(0,1000)/1000
            seed = random.randint(0,1000)/1000
            condom_rate = max(self.condom_rate[pair[0].condom_group], self.condom_rate[pair[1].condom_group])
            if condom_seed > condom_rate and seed < beta:
                if pair[0].suceptible == 0 and pair[0].vaccinated == 0 and (pair[1].suceptible == 1 or pair[1].reinfected == 1 or pair[1].recovered == 1):
                    pair[0].suceptible = 1
                if pair[1].suceptible == 0 and pair[1].vaccinated == 0 and (pair[0].suceptible == 1 or pair[0].reinfected == 1 or pair[0].recovered == 1):
                    pair[1].suceptible = 1
                # Both party could be infected, so not `elif`.

                # Write their history (no condom)
                pair[0].condom_history.append(0)
                pair[1].condom_history.append(0)
                # Debug check (copy this to other parts if needed)
                # print('Condom history: {}: {} and {}: {}'.format(pair[0].id, pair[0].condom_history, pair[1].id, pair[1].condom_history))
            else:
                # Write their history (wore condom)
                pair[0].condom_history.append(1)
                pair[1].condom_history.append(1)


    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

    def __call__(self):
        try:
            self.set_population()
            # self.set_condom_rate()
        except ValueError:
            pass
        self.raise_flag()

'''
10: Type of vaccine (One-off/ Seasonal/ Chemoprophylaxis)
'''
class Mode10(Mode):
    def __init__(self, people, phi, beta):
        super().__init__(people,10)
        self.modes = ['One-off', 'Seasonal', 'Chemoprophylaxis']

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 10. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        print('1. One-off')
        print('2. Seasonal')
        print('3. Chemoprophylaxis')
        cmd = input('Please choose one option: ')
        if cmd == '1':
            phi = 1
            return phi
        elif cmd == '2':
            pass
        elif cmd == '3':
            pass

'''
21: Intimacy game
'''
class Mode21(Mode):
    def __init__(self, people, contact_nwk):
        super().__init__(people,21)
        self.contact_nwk = contact_nwk
        self.r = 0.5
        self.rI = 0.8

        # Trust factor of population
        self.m = 1
        self.mu = 2

    def mate(self, pair):

        if len(pair) > 1:
            i = random.randint(0,len(pair)-1)  # Who is making the request
            self.mu = 2
        else:
            return None
        for j in range(len(pair)):
            if i == j:
                continue # Skip the person is deciding
            # [Distrust, Abuse, Honour trust]
            self.m = 1
            Ej = [1,1,1]
            Mj = [-self.rI,self.infection*self.rI,(1-self.infection)*self.r]
            Kj = [self.m * (1 - self.infection) * self.r, self.m * self.infection * self.rI, self.m * (1-self.infection) * self.r]
            max_utility = 0
            option = None
            for k in range(3):
                if Ej[k]+Mj[k]+Kj[k] > max_utility:
                    max_utility = Ej[k]+Mj[k]+Kj[k]
                    option = k
            if option == 0:
                return None
            # print(pair[j].id, max_utility, option)
            if option == 2 and (pair[i].suceptible == 1 and pair[i].recovered == 0) or (pair[i].reinfected == 1 and pair[i].recovered == 0):
                option = 1
            if option == 1 or option == 2:
                return option

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

'''
31: Include on demand PrEP.
'''
class Mode31(Mode):
    def __init__(self, people):
        super().__init__(people,31)

        # Proportion of agents that takes on demand PrEP
        self.p = 0

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

    def set_p(self, p):
        if p > 1:
            self.p = 1
        elif p < 0:
            self.p = 0
        else:
            self.p = p

    def init_on_demand_PrEP(self, person_id):
        '''
        Allow the specific agent start on demand PrEP.

        Parameter:
        self - Mode31 object.
        person_id - id of the person instance.
        '''
        self.people[person_id].on_demand = 1
        self.people[person_id].vaccinated = 0

    def mate(self, person_id, start=None):
        '''
        If the agent made sex in the time step, a mark is made to the agent to decide if the agent is suceptible if forgot to take on-demand PrEP with in 48 hours.

        Values of mated_marker:
        None - Does not have sex before/ Last sex more than 2 days ago.
        1 - Had sex 1 day ago.
        2 - Had sex 2 days ago.

        Values of Person.on_demand:
        0 - Not on on-demand PrEP
        1 - Taking on-demand PrEP
        '''
        marker = self.people[person_id].mated_marker  # Make code neater
        if start != None and marker == None:
            marker = 0
            self.people[person_id].on_demand = 1
        elif marker == 0:
            marker += 1  # become 1
        elif marker == 1:
            marker += 1  # become 2
        elif marker == 2:
            marker = None
        # At the end reassign the values back to the attributes
        self.people[person_id].mated_marker = marker

    def forget_medication(self,person_id):
        '''
        Allow the specific agent start on demand PrEP.

        Parameter:
        self - Instance of mode 31.
        person_id - id of the person instance.
        '''
        self.people[person_id].on_demand = 0
        self.people[person_id].vaccinated = 0

    def __call__(self):
        is_on = 0
        for i in range(len(self.people)):
            if self.people[i].on_demand != None:
                self.mate(self.people[i].id-1)  # Increase the marker
                is_on = 1
        if is_on == 0:
            # If everyone is not taking on-demand PrEP, drop the flag
            self.drop_flag()
        else:
            self.raise_flag()

'''
51: Erdos-Renyi topology
'''
class Mode51(Mode):
    def __init__(self, people, contact_nwk):
        super().__init__(people,51)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.p = 0.1  # Pairing probability

    def set_network(self):
        self.contact_nwk.nwk_graph = nx.generators.random_graphs.erdos_renyi_graph(len(self.people), self.p)

        # Relabel nodes to People objects
        mapping = {node: self.people[node] for node in self.contact_nwk.nwk_graph}
        self.contact_nwk.nwk_graph = nx.relabel_nodes(self.contact_nwk.nwk_graph, mapping)

        # Random pair people with no partners with other partners
        for node in self.contact_nwk.nwk_graph.nodes:
            if self.contact_nwk.nwk_graph.degree(node) == 0:
                random_node = random.choice(list(self.contact_nwk.nwk_graph.nodes()))
                self.contact_nwk.nwk_graph.add_edge(node, random_node)

        # Add edge list to contact_nwk.network
        self.contact_nwk.network = [e for e in self.contact_nwk.nwk_graph.edges]

    def set_p(self, p):
        if p > 1:
            self.p = 1
        elif p < 0:
            self.p = 0
        else:
            self.p = p

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 51. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        try:
            p_temp = float(input('p >>> '))
        except ValueError:
            print('Invalid data type for p, set p as 1. ')
            p_temp = 1
        self.set_p(p_temp)
        self.set_network()
        self.raise_flag()
        print('E-R graph settings done.')


'''
52: Preferential attachment.
'''
class Mode52(Mode):
    def __init__(self, people, contact_nwk=None):
        super().__init__(people,52)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.m = 1  # Pairing probability

    def set_network(self):
        '''
        Setup the network and nwk_graph
        '''
        self.contact_nwk.nwk_graph = nx.generators.random_graphs.barabasi_albert_graph(len(self.people), self.m)

        # Relabel nodes to People objects
        mapping = {node: self.people[node] for node in self.contact_nwk.nwk_graph}
        self.contact_nwk.nwk_graph = nx.relabel_nodes(self.contact_nwk.nwk_graph, mapping)

        # Add edge list to contact_nwk.network
        self.contact_nwk.network = [e for e in self.contact_nwk.nwk_graph.edges]

    def set_m(self, m):
        if m < 1:
            self.m = 1
        else:
            self.m = m

    def __call__(self):
        '''
        Setting mode 52 into model. If other network modes have set, they are dropped by `main.py`.
        '''
        print('-------------------------')
        print('You are creating mode 52. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        try:
            m_temp = int(input('m >>> '))
        except ValueError:
            print('Invalid data type for m, set m as 1. ')
            m_temp = 1
        self.set_m(m_temp)
        self.set_network()
        self.raise_flag()
        print('Preferential attachment graph settings done.')

'''
53: Small world network
'''
class Mode53(Mode):
    def __init__(self, people, contact_nwk=None):
        super().__init__(people,53)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.k = 1  # k neighbours are joined
        self.p = 1  # Rewiring probability

    def set_network(self):
        '''
        Setup the network and nwk_graph
        '''
        self.contact_nwk.nwk_graph = nxgenerators.random_graphs.watts_strogatz_graph(len(self.people), self.k, self.p)

        # Relabel nodes to People objects
        mapping = {node: self.people[node] for node in self.contact_nwk.nwk_graph}
        self.contact_nwk.nwk_graph = nx.relabel_nodes(self.contact_nwk.nwk_graph, mapping)

        # Add edge list to contact_nwk.network
        self.contact_nwk.network = [e for e in self.contact_nwk.nwk_graph.edges]

    def set_k(self, m):
        if m < 1:
            self.k = 1
        else:
            self.k = m

    def set_p(self, p):
        if p > 1:
            self.p = 1
        elif p < 0:
            self.p = 0
        else:
            self.p = p

    def __call__(self):
        '''
        Setting mode 53 into model. If other network modes have set, they are dropped by `main.py`.
        '''
        print('-------------------------')
        print('You are creating mode 53. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        try:
            k_temp = int(input('k >>> '))
        except ValueError:
            print('Invalid data type for m, set m as 1. ')
            k_temp = 1
        self.set_k(k_temp)
        try:
            p_temp = int(input('p >>> '))
        except ValueError:
            print('Invalid data type for p, set m as 1. ')
            p_temp = 1
        self.set_p(p_temp)
        self.set_network()
        self.raise_flag()
        print('Watts-Strogatz graph settings done.')

'''
54: Lattice network
'''
class Mode54(Mode):
    def __init__(self, people, contact_nwk=None):
        super().__init__(people,54)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.m = 1  # Nunber of rows
        self.n = len(self.people)//self.m  # Nunber of columns

    def set_network(self):
        '''
        Setup the network and nwk_graph
        '''
        self.contact_nwk.nwk_graph = nx.generators.lattice.grid_2d_graph(len(self.people), self.m, self.n)

        # Relabel nodes to People objects
        mapping = {node: self.people[node] for node in self.contact_nwk.nwk_graph}
        self.contact_nwk.nwk_graph = nx.relabel_nodes(self.contact_nwk.nwk_graph, mapping)

        # Add edge list to contact_nwk.network
        self.contact_nwk.network = [e for e in self.contact_nwk.nwk_graph.edges]

    def set_dim(self, m):
        if m < 1:
            self.m = 1
        else:
            self.m = m
        self.n = len(self.people)//self.m

    def __call__(self):
        '''
        Setting mode 52 into model. If other network modes have set, they are dropped by `main.py`.
        '''
        print('-------------------------')
        print('You are creating mode 54. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        try:
            m_temp = int(input('m >>> '))
        except ValueError:
            print('Invalid data type for m, set m as 1. ')
            m_temp = 1
        self.set_dim(m_temp)
        self.set_network()
        self.raise_flag()
        print('Preferential attachment graph settings done.')
