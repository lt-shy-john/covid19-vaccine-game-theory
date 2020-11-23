from person import Person

import random
import networkx as nx
import numpy as np

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

    def correct_para(self, p, pos=False):
        '''
        Convert the parameters into integers.

        Parameters
        p: int
            input.
        pos: boolean
            If the parameter is positive number.
        '''
        try:
            p_num = int(p)
            if pos == True and p_num < 1:
                p_num = 1
            return p_num
        except ValueError:
            p_num = 1
            return p_num

    def set_correct_para(self, p, P, pos=False):
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
            return correct_para(p, pos=False)

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
        beta_city = super().set_correct_epi_para(beta_city_temp, beta_city)
        self.set_beta(0, beta_city)
        beta_rural_temp = input('Rural >>> ')
        beta_rural = super().set_correct_epi_para(beta_rural_temp, beta_rural)
        self.set_beta(1, beta_rural)

        print('\nPlease set proportional parameter below. ')
        prop_city_temp = input('City >>> ')
        prop_city = super().set_correct_epi_para(prop_city_temp, prop_city)
        prop_rural_temp = input('Rural >>> ')
        prop_rural = super().set_correct_epi_para(prop_rural_temp, prop_rural)
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
    def __init__(self, people, alpha):
        super().__init__(people,4)
        self.alpha = alpha
        self.P_Alpha = []

        # Other parameters are stored within the person

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 4. ')
        print('-------------------------\n')
        if self.alpha == 0:
            print('Warning: Adoption parameter is 0, mode4 will not work under this. Please reset adoption parameter first. ')
            return
        print('Please set rationality parameter below. ')
        lambda_BR = self.people[0].lambda_BR
        lambda_BR_temp = input('Lambda >>> ')
        lambda_BR = super().set_correct_para(lambda_BR_temp, lambda_BR, pos=True)
        self.set_lambda(lambda_BR)
        print('Assigning parameters to population. ')
        self.QRE()
        self.raise_flag()
        print('\nMode 4 equipped. \n')

    def set_lambda(self, lambda_input):
        '''
        Set rationality parameter for each person.

        parameter
        ---------
        lambda_input: float
            A initial value fixed for all people.
        '''
        for person in self.people:
            person.lambda_BR = lambda_input

    def QRE(self):
        '''
        Return a list of probability to adaopt vaccine with size of population.
        '''
        utility_fn = [self.alpha * person.lambda_BR * person.rV_BR for person in self.people]
        disutility_fn = [self.alpha * person.lambda_BR * person.rI_BR for person in self.people]
        self.P_Alpha = np.exp(utility_fn)/(sum(np.exp(utility_fn), np.exp(disutility_fn)))


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
07: Age distribution
'''
class Mode07(Mode):
    '''
    Attributes
    ----------
    beta: iterable of floats (0 to 1)
        Transmission rate of different age brackets.

    Note
    ----
    Age brackets: 0 - 9, 10 - 19, 20 - 29, 30 - 39, 40 - 49, 50 - 59, 60 - 69, 70 - 79, 80 - 89, 90 - 99.

    '''

    def __init__(self, people, beta, delta):
        super().__init__(people,7)
        self.beta_age = [beta for x in range(10)]
        self.delta_age = [delta for x in range(10)]

    def set_population(self):
        '''
        Set age of a population.

        parameter
        ---------
        input: iterable, optional
            Define frequency and their condom use.

        '''
        for person in self.people:
            person.set_age()



    def __call__(self):
        print('-------------------------')
        print('You are creating mode 7. ')
        print('-------------------------\n')
        # 0 - 9, 10 - 19, 20 - 29, 30 - 39, 40 - 49, 50 - 59, 60 - 69, 70 - 79, 80 - 89, 90 - 99

        # Infection
        print('Please set infection parameter for each age brackets below. ')
        beta0_temp = input('0 - 9 >>> ')
        self.beta_age[0] = super().set_correct_epi_para(beta0_temp, self.beta_age[0])
        beta1_temp = input('10 - 19 >>> ')
        self.beta_age[1] = super().set_correct_epi_para(beta1_temp, self.beta_age[1])
        beta2_temp = input('20 - 29 >>> ')
        self.beta_age[2] = super().set_correct_epi_para(beta2_temp, self.beta_age[2])
        beta3_temp = input('30 - 39 >>> ')
        self.beta_age[3] = super().set_correct_epi_para(beta3_temp, self.beta_age[3])
        beta4_temp = input('40 - 49 >>> ')
        self.beta_age[4] = super().set_correct_epi_para(beta4_temp, self.beta_age[4])
        beta5_temp = input('50 - 59 >>> ')
        self.beta_age[5] = super().set_correct_epi_para(beta5_temp, self.beta_age[5])
        beta6_temp = input('60 - 69 >>> ')
        self.beta_age[6] = super().set_correct_epi_para(beta6_temp, self.beta_age[6])
        beta7_temp = input('70 - 79 >>> ')
        self.beta_age[7] = super().set_correct_epi_para(beta7_temp, self.beta_age[7])
        beta8_temp = input('80 - 89 >>> ')
        self.beta_age[8] = super().set_correct_epi_para(beta8_temp, self.beta_age[8])
        beta9_temp = input('90 - 99 >>> ')
        self.beta_age[9] = super().set_correct_epi_para(beta9_temp, self.beta_age[9])

        # Removal
        print('Please set removal parameter for each age brackets below. ')
        delta0_temp = input('0 - 9 >>> ')
        self.delta_age[0] = super().set_correct_epi_para(delta0_temp, self.delta_age[0])
        delta1_temp = input('10 - 19 >>> ')
        self.delta_age[1] = super().set_correct_epi_para(delta1_temp, self.delta_age[1])
        delta2_temp = input('20 - 29 >>> ')
        self.delta_age[2] = super().set_correct_epi_para(delta2_temp, self.delta_age[2])
        delta3_temp = input('30 - 39 >>> ')
        self.delta_age[3] = super().set_correct_epi_para(delta3_temp, self.delta_age[3])
        delta4_temp = input('40 - 49 >>> ')
        self.delta_age[4] = super().set_correct_epi_para(delta4_temp, self.delta_age[4])
        delta5_temp = input('50 - 59 >>> ')
        self.delta_age[5] = super().set_correct_epi_para(delta5_temp, self.delta_age[5])
        delta6_temp = input('60 - 69 >>> ')
        self.delta_age[6] = super().set_correct_epi_para(delta6_temp, self.delta_age[6])
        delta7_temp = input('70 - 79 >>> ')
        self.delta_age[7] = super().set_correct_epi_para(delta7_temp, self.delta_age[7])
        delta8_temp = input('80 - 89 >>> ')
        self.delta_age[8] = super().set_correct_epi_para(delta8_temp, self.delta_age[8])
        delta9_temp = input('90 - 99 >>> ')
        self.delta_age[9] = super().set_correct_epi_para(delta9_temp, self.delta_age[9])

        print('You may edit the proportion of each brackets in person.py. ')
        self.set_population()
        self.raise_flag()
        print('\nMode 7 equipped. \n')

'''
08: Gender distribution
'''
class Mode08(Mode):
    '''
    Attributes
    ----------
    beta: iterable of floats (0 to 1)
        Transmission rate of different age brackets.

    Note
    ----
    0 is male, 1 is female.

    '''

    def __init__(self, people, beta, delta):
        super().__init__(people,8)
        self.beta_gender = [beta for x in range(2)]
        self.delta_gender = [delta for x in range(2)]

    def set_population(self):
        '''
        Set age of a population.

        parameter
        ---------
        input: iterable, optional
            Define frequency and their condom use.

        '''
        for person in self.people:
            person.set_gender()


    def __call__(self):
        print('-------------------------')
        print('You are creating mode 8. ')
        print('-------------------------\n')
        print('Please set infection parameter for each age brackets below. ')
        beta0_temp = input('Male >>> ')
        self.beta_gender[0] = super().set_correct_epi_para(beta0_temp, self.beta_gender[0])
        beta1_temp = input('Female >>> ')
        self.beta_gender[1] = super().set_correct_epi_para(beta1_temp, self.beta_gender[1])
        print('Please set removal parameter for each age brackets below. ')
        delta0_temp = input('Male >>> ')
        self.delta_gender[0] = super().set_correct_epi_para(delta0_temp, self.delta_gender[0])
        delta1_temp = input('Female >>> ')
        self.delta_gender[1] = super().set_correct_epi_para(delta1_temp, self.delta_gender[1])
        print('You may edit the proportion of each brackets in person.py. ')
        self.set_population()
        self.raise_flag()
        print('\nMode 8 equipped. \n')

'''
10: Type of vaccine (One-off/ Seasonal/ Chemoprophylaxis)
'''
class Mode10(Mode):
    def __init__(self, people, phi, beta):
        super().__init__(people,10)
        self.types = ['One-off', 'Seasonal', 'Chemoprophylaxis']
        self.type = None

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 10. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        for i in range(len(self.types)):
            print(f'{i+1}. {self.types[i]}')
        cmd = input('Please choose one option: ')
        if cmd == '1':
            self.type = 1
        elif cmd == '2':
            self.type = 2
        elif cmd == '3':
            self.type = 3
        self.raise_flag()
        print('\nMode 10 equipped. \n')

    def check_input(self, cmd):
        '''
        Check from express mode if user has input an integer the corresponds to an existing mode.
        '''
        try:
            cmd = int(cmd)
            if cmd > 0 and cmd <= 3:
                return cmd
        except ValueError:
            print('Invalid vaccine type specified. ')


'''
11: Stop transmissability/ reduce severity
'''
class Mode11(Mode):
    def __init__(self, people):
        super().__init__(people,11)
        self.types = ['Stop transmissability', 'Reduce severity']
        self.type = None

        self.beta_V = None
        self.gamma_V = None
        self.delta_V = None

    def __call__(self, beta, gamma, delta):
        print('-------------------------')
        print('You are creating mode 11. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        for i in range(len(self.types)):
            print(f'{i+1}. {self.types[i]}')
        cmd = input('Please choose one option: ')
        if cmd == '1':
            self.type = 1
            new_beta_temp = input('Beta >>> ')
            self.beta_V = super().set_correct_epi_para(new_beta_temp, self.beta_V)
        elif cmd == '2':
            self.type = 2
            new_gamma_temp = input('Gamma >>> ')
            self.gamma_V = super().set_correct_epi_para(new_gamma_temp, self.gamma_V)
            new_delta_temp = input('Delta >>> ')
            self.delta_V = super().set_correct_epi_para(new_delta_temp, self.delta_V)
        self.raise_flag()
        print('\nMode 11 equipped. \n')

    def check_input(self, cmd):
        '''
        Check from express mode if user has input an integer the corresponds to an existing mode.
        '''
        try:
            cmd = int(cmd)
            if cmd > 0 and cmd <= 2:
                return cmd
        except ValueError:
            print('Invalid vaccine type specified. ')

    def check_beta(self, beta):
        if beta < self.beta_V:
            print('Warning: Your setting implies vaccine may cause higher tranmissibility. ')
    def check_gamma(self, gamma):
        if gamma > self.gamma_V:
            print('Warning: Your setting implies vaccine may cause lower effectiveness. ')
    def check_delta(self, delta):
        if delta > self.delta_V:
            print('Warning: Your setting implies vaccine may cause higher death rate. ')

'''
20: Intimacy game
'''
class Mode20(Mode):
    def __init__(self, people, contact_nwk, beta):
        super().__init__(people,20)
        self.contact_nwk = contact_nwk
        self.rV = 1
        self.rI = -1
        self.beta = beta
        self.local_infection_p = np.ones(len(self.people))  # The proportion, not number of cases.
        self.theta = np.ones(len(self.people))

        # Weights on local and global pereption
        self.rho = 1

        self.ProbV = np.ones(len(self.people))

    def set_perceived_infection(self, global_infection):
        # Clear objects
        self.theta = np.ones(len(self.people))
        self.local_infection_p = np.ones(len(self.people))

        # Start
        local_infection = np.zeros(len(self.people))
        if self.people[0].location != None:
            for i in range(len(self.people)):
                if self.people[i].location == 0:
                    pass
                else:
                    pass
            return
        if self.contact_nwk.network != None:
            for i in range(len(self.people)):
                for neighbour in self.contact_nwk.nwk_graph.neighbours(self.people[i]):
                    local_infection[i] += 1
            print(f'There are {local_infection[i]} people infected around {self.people[i].id}. ')
            self.local_infection_p = local_infection/len(self.people)
            self.theta = np.add(self.local_infection_p * self.rho, np.ones(len(self.people)) * global_infection * (1-self.rho))
        else:
            pass

'''
21: Local Majority Rule
'''
class Mode21(Mode):
    def __init__(self, people, info_nwk):
        super().__init__(people,21)
        self.info_nwk = info_nwk
        self.propro = None
        self.agpro = None

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 21. ')
        print('-------------------------\n')
        print('Please set proportion of initial opinion below. ')
        propro_temp = input('Pro >>> ')
        self.propro = super().correct_para(propro_temp)
        agpro_temp = input('Ag >>> ')
        self.agpro = super().correct_para(agpro_temp)
        self.set_opinion()
        print('All population has been assigned with their opinion. ')
        self.set_personality()
        print('All population has been assigned with default personality. ')
        # Roster has been set already.
        self.raise_flag()
        print('\nMode 21 equipped. \n')

    def get_prop(self):
        return self.propro/(self.propro+self.agpro)

    def set_pro(self, propro_temp):
        self.propro = super().correct_para(propro_temp)

    def set_ag(self, ag_temp):
        self.agpro = super().correct_para(ag_temp)

    def set_opinion(self):
        for person in self.people:
            seed = random.randint(0,1000)/1000
            if seed < self.get_prop():
                person.opinion = 1
            else:
                person.opinion = 0

    def set_personality(self):
        for person in self.people:
            person.personality = 0

'''
22: Stubbon to take vaccine
'''
class Mode22(Mode):
    def __init__(self, people, info_nwk):
        super().__init__(people,22)
        self.info_nwk = info_nwk
        self.InflexProProportion = None

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 22. ')
        print('-------------------------\n')
        print('Please set proportion of stubbon of pro-vaccine below. ')
        propro_temp = input('Pro >>> ')
        self.assign_personality(propro_temp)
        self.raise_flag()
        print('\nMode 22 equipped. \n')

    def assign_personality(self, p):
        '''
        Assign some people with stubbon to take vaccine personality.
        '''
        p = super().set_correct_epi_para(p, 0)
        for person in self.people:
            if person.personality == 0:
                seed = random.randint(0,1000)/1000
                if seed < p:
                    person.personality = 1
                    person.opinion = 1

'''
23: Stubbon to against vaccine
'''
class Mode23(Mode):
    def __init__(self, people, info_nwk):
        super().__init__(people,23)
        self.info_nwk = info_nwk
        self.InflexAgProportion = None

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 23. ')
        print('-------------------------\n')
        print('Please set proportion of stubbon of anti-vaccine below. ')
        agpro_temp = input('Pro >>> ')
        self.assign_personality(agpro_temp)
        self.raise_flag()
        print('\nMode 23 equipped. \n')

    def assign_personality(self, p):
        '''
        Assign some people with stubbon to against vaccine personality.
        '''
        p = super().set_correct_epi_para(p, 0)
        for person in self.people:
            if person.personality == 0:
                seed = random.randint(0,1000)/1000
                if seed < p:
                    person.personality = 2
                    person.opinion = 0

'''
24: Contrary to social groups
'''
class Mode24(Mode):
    def __init__(self, people, info_nwk):
        super().__init__(people,24)
        self.info_nwk = info_nwk
        self.BalancerProportion = None

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 24. ')
        print('-------------------------\n')
        print('Please set proportion of contrarian below. ')
        balpro_temp = input('Pro >>> ')
        self.assign_personality(balpro_temp)
        self.assign_personality()
        self.raise_flag()
        print('\nMode 24 equipped. \n')

    def assign_personality(self, p):
        '''
        Assign people with balancer personality.
        '''
        p = super().set_correct_epi_para(p, 0)
        for person in self.people:
            if person.personality == 0:
                seed = random.randint(0,1000)/1000
                if seed < p:
                    person.personality = 3

'''
31: Medication incorporated
'''
class Mode31(Mode):
    def __init__(self, people):
        super().__init__(people,31)


    def __call__(self):
        print('-------------------------')
        print('You are creating mode 31. ')
        print('-------------------------\n')
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

    def set_p(self, p):
        '''
        Set probability to update network
        '''
        if p > 1:
            self.contact_nwk.PUpdate = 1
        elif p < 0:
            self.contact_nwk.PUpdate = 0
        else:
            self.contact_nwk.PUpdate = p

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
        pUpd_temp = float(input('p >>> '))
        pUpd = super().set_correct_epi_para(pUpd_temp, self.contact_nwk.PUpdate)
        self.set_p(pUpd)
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
