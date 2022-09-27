from vaccine import Vaccine
from contact import ContactNwk
from person import Person

import random
import math
import networkx as nx
import numpy as np


class Mode:
    def __init__(self, people, code, name, logger):
        self.code = code
        self.name = name
        # Flag to alert setting has been loaded.
        self.flag = ' '  # If loaded then has value 'X'.
        # Population objects
        self.people = people
        self.logger = logger

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
        P -- original/ default value.
        pos -- If the parameter is positive number.
        '''
        if p == '':
            return P
        else:
            return self.correct_para(p, pos=False)

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

    def __init__(self, people, logger, betas=[0.5, 0.5]):
        super().__init__(people, 1, 'Living in city/ rural', logger)
        self.weight = [4, 6]
        self.betas = betas

    def set_weight(self, c, r):
        self.weight = [c, r]
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
            person.location = random.choices(list(range(2)), weights=self.weight, k=1)[0]

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
    '''
    Travel from overseas

    Attributes
    ----------
    overseas : dict
        The list of overseas destination, and their transmission rate as values.
    rS : float
        Reward of not going overseas.
    rI : float
        Reward of going overseas.
    overseasIsolation: dict
        The list of overseas destination, and whether they have social isolation policies upon arrival as values (boolean).
    localIsolation: bool
        If local area has social isolation policies upon arrival.
    isolationPeriod: int
        Social isolation period when arriving a new place.
    '''

    def __init__(self, people, main_beta, logger):
        super().__init__(people, 2, 'Travel from overseas', logger)
        self.overseas = {'Some Places': 0.14}
        self.travel_prob = 0.00012
        self.rS = 1
        self.rI = 1
        self.beta = main_beta

        # Isolation parameters
        self.overseasIsolation = {'Some Places': True}
        self.localIsolation = True
        self.isolationPeriod = 14

        # Return parameters
        self.return_prob = {'Some Places': 0.0001}

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 2. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set the parameters below. ')
        self.logger.info('\nPlease set travel probability below. ')
        travel_prob_temp = input('p >>> ')
        self.travel_prob = super().set_correct_epi_para(travel_prob_temp, self.travel_prob)
        self.logger.info('\nPlease set new destination below. ')
        self.logger.info('(If none, please press enter)')
        new_dest_name = None
        while new_dest_name != '':
            new_dest_name = input('>>> ')
            if new_dest_name == '':
                continue
            beta_new_dest_temp = input('β >>> ')
            beta_new_dest = super().set_correct_epi_para(beta_new_dest_temp, 0.5)
            self.create_destination(new_dest_name, beta_new_dest)
            self.logger.debug(f'{new_dest_name} created. ')
        self.logger.info('Please set outward travel probability. ')
        travel_prob_temp = input('P(T) >>> ')
        self.travel_prob = super().set_correct_epi_para(travel_prob_temp, self.travel_prob)
        self.logger.info('Please set reward for healthy below. ')
        r_S_temp = input('rS >>> ')
        self.rS = super().set_correct_para(r_S_temp, self.rS)
        self.logger.info('Please set reward for infection below. ')
        r_I_temp = input('rI >>> ')
        self.rI = super().set_correct_para(r_I_temp, self.rI)
        self.create_setting()
        self.logger.info('Setting applied to population. ')
        self.raise_flag()
        self.logger.info('Mode 2 equipped. ')

    def create_setting(self):
        '''
        Assign values to population
        '''
        for people in self.people:
            people.A = 1  # Aware the destination has pandemic.

    def create_destination(self, new_dest_name, beta):
        '''
        When calling instance, an option to create more destinations.
        '''
        if new_dest_name == '':
            return
        self.overseasIsolation[new_dest_name] = beta
        self.logger.debug(f'Created new overseas destination {new_dest_name} wih transmission rate {beta}. ')

    def make_decision(self):
        '''
        Make decision based on circumstances in each time step.
        '''
        self.logger.debug('Starting method Mode02.make_decision()... ')
        for person in self.people:
            # If person is symptomatic, they cannot leave.
            if person.suceptible == 1 and person.exposed == 1:
                self.logger.debug(f'\t{person.id} is symptomatic, they cannot travel overseas. ')
                continue
            # The person needs to decide to go overseas by now.
            if person.overseas != None:
                continue  # The person is in overseas already
            # The person has just been back from overseas.
            if person.overseas == None:
                travel_history = person.travel_history
                if len(travel_history) == 0:
                    continue  # Catch where at t = 0, no travel history exists.
                if travel_history[-1] == ':isolate':
                    # Most recent travel history has not been written, so last element comes from day before.
                    self.logger.debug(f'{person.id} has just been back from overseas. Not thinking about travelling. ')
                    continue

            # Decide
            seed = random.randint(0, 1000) / 1000
            self.logger.debug(f'\tPerson {person.id}. Seed: {seed}. Probability to travel: {self.travel_prob}. (seed <  prob: {seed < self.travel_prob})')
            if seed >= self.travel_prob:
                continue

            # The person considers the place to visit.
            destination = random.choice(list(self.overseas))
            U_I = self.get_Mode02E0(self.people.index(person))
            U_S = self.get_Mode02E1(self.people.index(person))

            # Make decision
            self.logger.debug(f"\tTravel decision: U_I: {U_I} U_S: {U_S} U_I > U_S: {U_I > U_S}")
            if U_I < U_S:
                person.overseas = {destination: self.overseas[destination]}
                self.logger.debug(f'\t{person.id} decided travel to {list(person.overseas.keys())[0]}. ')
            else:
                self.logger.debug(f'\t{person.id} decided not travel. ')

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

    def is_isolated_overseas(self, i, verbose=False):
        '''
        Isolation while overseas, unable to contact with disease.
        '''
        if not self.overseasIsolation[list(self.people[i].overseas.keys())[0]]:
            return False
        if len(self.people[i].travel_history) < 1:
            return False  # Simulation immature to isolate people overseas

        if type(self.people[i].travel_history[-1]) != str:
            return False  # The person is not in overseas.

        if 'isolate' in self.people[i].travel_history[-1]:
            self.logger.debug(f'\t{self.people[i].id} is quarantined overseas. ')
            return True
        else:
            return False

    def is_isolated_local(self, i):
        '''
        Isolation while back from overseas, unable to contact with disease.
        '''
        self.logger.debug(f'Starting method Mode02.is_isolated_local() for person {self.people[i].id}...')
        if not self.localIsolation:
            self.logger.debug('Local place does not require isolation upon return. ')
            return False
        if len(self.people[i].travel_history) < 1:
            self.logger.debug('\tTravel history too short to be determined. ')
            return False

        if self.people[i].overseas != None:
            self.logger.debug('\tThe person is in overseas. ')
            return False

        days_back_in_local = 0
        for t in reversed(range(len(self.people[i].travel_history))):
            if t == 0:
                self.logger.debug('\tThe person has never been travelling, no local isolation required. ')
                return False
            elif type(self.people[i].travel_history[t]) == str and not self.people[i].travel_history[t] == ":isolate":
                break
            days_back_in_local += 1

        self.logger.debug(f'\tPerson is back since {days_back_in_local} days. ')
        if days_back_in_local <= self.isolationPeriod:
            self.logger.debug(f'\tPerson is quarantined locally. ({days_back_in_local} <= {self.isolationPeriod})')
            return True
        else:
            self.logger.debug(f'\tPerson does not require to be quarantined locally anymore. ({days_back_in_local} > {self.isolationPeriod})')
            return False

    def returnOverseas(self):
        '''
        Come back from overseas. Option for 14 days isolation.
        '''
        self.logger.debug('Starting method Mode02.returnOverseas()...')
        for person in self.people:
            if person.overseas == None:
                self.logger.debug(f'\tPerson {person.id} is not subject to overseas isolation (At local). ')
                continue
            if list(person.overseas.keys())[0] + ':isolate' in person.travel_history[-1]:
                self.logger.debug(f'\tPerson {person.id} is isolated ovserseas. ')
                continue
            if list(person.overseas.keys())[0] + ':hospitalised' in person.travel_history[-1]:
                self.logger.debug(f'\tPerson {person.id} is hospitalised ovserseas. ')
                continue

            seed = random.randint(0, 1000) / 1000
            if seed < self.return_prob[list(person.overseas.keys())[0]]:
                self.logger.debug(f'\tPerson {person.id} is returning from overseas. ({seed} < {self.return_prob[list(person.overseas.keys())[0]]})')
                person.overseas = None

    def writeRecentTravelHistory(self, person, verbose=False):
        '''
        Find the experience from last overseas travel.

        parameters
        ----------
        person: Person
            The person to be checked.
        verbose: bool (default=False)
            Verbose mode, for debugging.

        note
        ----
        Use this function if the person is known to be in overseas.
        '''
        self.logger.debug(f'\t== Recent travel history of {person.id} ==')
        recent_travel_history = []
        recent_destination = list(person.overseas.keys())[0]
        for i in reversed(range(len(person.travel_history))):
            if len(recent_travel_history) > 0 and recent_destination not in str(recent_travel_history[-1]):
                break
            recent_travel_history.append(person.travel_history[i])
        self.logger.debug(f'\t   {recent_travel_history}')
        return recent_travel_history

    def writeTravelHistory(self):
        '''
        At each iteration, record where the person went.
        '''
        for person in self.people:
            self.logger.debug(f'Writing person {person.id} travel history...')

            if person.overseas == None and self.is_isolated_local(self.people.index(person)):
                self.logger.debug(f'\t{person.id} is quarantined back in local. ')
                person.travel_history.append(':isolate')
                continue
            elif person.overseas == None:
                self.logger.debug(f'\t{person.id} remains at local. ')
                person.travel_history.append(0)
                continue

            recent_travel_history = self.writeRecentTravelHistory(person)
            if len(recent_travel_history) > self.isolationPeriod and person.overseas != None:
                self.logger.debug(f'\t{person.id} is travelling in {list(person.overseas.keys())[0]}. ')
                person.travel_history.append(list(person.overseas.keys())[0])
            else:
                person.travel_history.append(list(person.overseas.keys())[0] + ':isolate')
                self.logger.debug(f'\t{person.id} is quarantined in {list(person.overseas.keys())[0]}. ')
                continue

            if person.suceptible == 1 and person.exposed == 1 and person.overseas != None:
                self.logger.debug(f'\t{person.id} has been infected in {list(person.overseas.keys())[0]}. ')
                person.travel_history.append(list(person.overseas.keys())[0] + ':hospitalised')


'''
04: Bounded rationality of vaccine
'''


class Mode04(Mode):
    def __init__(self, people, alpha, logger):
        super().__init__(people, 4, 'Bounded rationality of vaccine', logger)
        self.alpha = alpha
        self.P_Alpha = []

        # Other parameters are stored within the person

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 4. ')
        self.logger.info('-------------------------\n')
        if self.alpha == 0:
            self.logger.warn(
                'Adoption parameter is 0, mode4 will not work under this. Please reset adoption parameter first. ')
            return
        self.logger.info('Please set rationality parameter below. ')
        lambda_BR = self.people[0].lambda_BR
        lambda_BR_temp = input('Lambda >>> ')
        lambda_BR = super().set_correct_para(lambda_BR_temp, lambda_BR, pos=True)
        self.set_lambda(lambda_BR)
        self.logger.info('Assigning parameters to population. ')
        self.QRE()
        self.raise_flag()
        self.logger.info('\nMode 4 equipped. \n')

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
        self.P_Alpha = np.divide(np.exp(utility_fn), (np.add(np.exp(utility_fn), np.exp(disutility_fn))),
                                 out=np.ones_like(utility_fn), where=(utility_fn != np.inf))
        self.logger.debug('Calculated QRE: ')
        self.logger.debug('QRE: ')
        self.logger.debug('U =',utility_fn)
        self.logger.debug('-U =',disutility_fn)
        self.logger.debug('p =',self.P_Alpha)
        self.logger.debug('')


'''
05: Edit partner network
'''


class Mode05(Mode):
    def __init__(self, people, g, logger):
        super().__init__(people, 5, 'Edit contact network', logger)
        self.g = g  # Import from ContactNwk object. Graph of social network
        self.data = None  # User requests to change social network topology

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
        self.logger.info('-------------------------')
        self.logger.info('You are editing mode 5. ')
        self.logger.info('-------------------------\n')
        cmd = None
        while cmd != 'y':
            self.logger.info('Please review the contact network.')
            self.view_network()

            self.logger.info('Input the agents you wished to connect... ')
            self.logger.info('Agents are linked by "-" and pairs separated by space.')
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

    def __init__(self, people, beta, delta, logger):
        super().__init__(people, 7, 'Age distribution', logger)
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
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 7. ')
        self.logger.info('-------------------------\n')
        # 0 - 9, 10 - 19, 20 - 29, 30 - 39, 40 - 49, 50 - 59, 60 - 69, 70 - 79, 80 - 89, 90 - 99

        # Infection
        self.logger.info('Please set infection parameter for each age brackets below. ')
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
        self.logger.info('Please set removal parameter for each age brackets below. ')
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

        self.logger.info('You may edit the proportion of each brackets in person.py. ')
        self.set_population()
        self.raise_flag()
        self.logger.info('\nMode 7 equipped. \n')


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

    def __init__(self, people, beta, delta, logger):
        super().__init__(people, 8, 'Gender population', logger)
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
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 8. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set infection parameter for each age brackets below. ')
        beta0_temp = input('Male >>> ')
        self.beta_gender[0] = super().set_correct_epi_para(beta0_temp, self.beta_gender[0])
        beta1_temp = input('Female >>> ')
        self.beta_gender[1] = super().set_correct_epi_para(beta1_temp, self.beta_gender[1])
        self.logger.info('Please set removal parameter for each age brackets below. ')
        delta0_temp = input('Male >>> ')
        self.delta_gender[0] = super().set_correct_epi_para(delta0_temp, self.delta_gender[0])
        delta1_temp = input('Female >>> ')
        self.delta_gender[1] = super().set_correct_epi_para(delta1_temp, self.delta_gender[1])
        self.logger.info('You may edit the proportion of each brackets in person.py. ')
        self.set_population()
        self.raise_flag()
        self.logger.info('\nMode 8 equipped. \n')


'''
10: Type of vaccine (One-off/ Seasonal/ Chemoprophylaxis)
'''


class Mode10(Mode):
    def __init__(self, people, phi, beta, logger):
        super().__init__(people, 10, 'Type of vaccine (One-off/ Seasonal/ Chemoprophylaxis)', logger)
        self.types = ['One-off', 'Seasonal', 'Chemoprophylaxis']
        self.type = None

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 10. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set infection parameter below. ')
        for i in range(len(self.types)):
            self.logger.debug(f'Id: {i + 1} Vaccine type: {self.types[i]}')
        cmd = input('Please choose one option: ')
        if cmd == '1':
            self.type = 1
        elif cmd == '2':
            self.type = 2
        elif cmd == '3':
            self.type = 3
        self.raise_flag()
        self.logger.info('\nMode 10 equipped. \n')

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
    def __init__(self, people, logger):
        super().__init__(people, 11, 'Stop transmissability/ reduce severity', logger)
        self.types = ['Stop transmissability', 'Reduce severity']
        self.type = None

        self.beta_V = None
        self.gamma_V = None
        self.delta_V = None

    def __call__(self, beta, gamma, delta):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 11. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set infection parameter below. ')
        for i in range(len(self.types)):
            print(f'{i + 1}. {self.types[i]}')
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
        self.logger.info('\nMode 11 equipped. \n')

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
            self.logger.warn('Your setting implies vaccine may cause higher tranmissibility. ')

    def check_gamma(self, gamma):
        if gamma > self.gamma_V:
            self.logger.warn('Your setting implies vaccine may cause lower effectiveness. ')

    def check_delta(self, delta):
        if delta > self.delta_V:
            self.logger.warn('Your setting implies vaccine may cause higher death rate. ')


'''
12: Vaccine cost/ supply
'''


class Mode12(Mode):
    def __init__(self, people, logger):
        super().__init__(people, 12, 'Vaccine cost/ supply', logger)


    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 12. ')
        self.logger.info('-------------------------\n')

'''
15: Advanced vaccine options
'''


class Mode15(Mode):
    def __init__(self, people, logger):
        super().__init__(people, 15, 'Advanced vaccine options', logger)
        self.vaccine_doses = None

    def __call__(self, vaccine_ls, alpha, beta, gamma, delta, phi):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 15. ')
        self.logger.info('-------------------------\n')
        if vaccine_ls == []:
            self.logger.info('To initiate mode 15, you will need to create the vaccines available first. ')
            self.logger.info('Create new vaccine?')
            cmd = input('[y/n]>>> ')
            if cmd == 'y':
                self.create_vaccine_type(alpha, beta, gamma, delta, phi)
        else:
            self.raise_flag()
            self.logger.info('\nMode 15 equipped. \n')

    def create_vaccine_type(self, alpha, beta, gamma, delta, phi):
        self.logger.info('Please set new vaccine name below. ')
        name = input('>>> ')
        self.logger.info('Please set vaccine dose number below. ')
        dose = input('>>> ')
        dose = super().set_correct_para(dose, 1, pos=True)
        self.logger.info('Please set vaccine adoption rate below. ')
        new_alpha_temp = input('>>> ')
        alpha = super().set_correct_epi_para(new_alpha_temp, alpha)
        self.logger.info('Please set vaccine type below. ')
        vaccine_type = input('>>> ')
        if int(vaccine_type) < 1 or int(vaccine_type > 3):
            self.logger.info('Invalid vaccine type, reverting to 1')
            vaccine_type = 1
        self.logger.info('Please set vaccine cost number below. ')
        cost = input('>>> ')
        cost = super().set_correct_para(cost, 0, pos=True)
        self.logger.info('Please set vaccine efficacy number below. ')
        efficacy = input('>>> ')
        efficacy = super().set_correct_epi_para(efficacy, 1)
        self.logger.info('Please specify whether the vaccine stop transmissability/ reduce severity below. ')
        cmd = input('Please choose one option [1/2]: ')
        if cmd == '1':
            self.type = 1
            new_beta_temp = input('Beta >>> ')
            beta = super().set_correct_epi_para(new_beta_temp, beta)
        elif cmd == '2':
            self.type = 2
            new_gamma_temp = input('Gamma >>> ')
            gamma = super().set_correct_epi_para(new_gamma_temp, gamma)
            new_delta_temp = input('Delta >>> ')
            delta = super().set_correct_epi_para(new_delta_temp, delta)

        new_vaccine = Vaccine(name, dose, vaccine_type, cost, efficacy, alpha, beta, gamma, delta, phi)
        self.vaccine_doses.append(new_vaccine)
        self.check_multi_dose_vaccine(self.vaccine_doses)
        return new_vaccine

    def check_multi_dose_vaccine(self, vaccine_ls):
        '''
        Returns a flag if there is a vaccine that requires multiple doses (w/ vaccine name)

        parameter
        ---------
        vaccine_ls: list
            List of vaccines from main code

        returns
        -------
        True if multiple vaccines (or doses) are considered.
        '''

        vaccine_dose_count = {}
        for vaccine in vaccine_ls:
            if vaccine.brand not in vaccine_dose_count:
                vaccine_dose_count[vaccine.brand] = 1
            else:
                vaccine_dose_count[vaccine.brand] += 1
        self.vaccine_doses = vaccine_dose_count

        for counts in vaccine_dose_count.values():
            if counts > 1:
                return True


    def check_latest_dose(self, vaccine_ls, brand):
        '''
        How many boosters in a vaccine brand.
        '''
        latest = 1
        for vaccine in vaccine_ls:
            if vaccine.brand != brand:
                continue
            if vaccine.dose > latest:
                latest = vaccine.dose
        return latest

    def check_recent_vaccine(self, i, vaccine_ls):
        '''
        Check the last vaccine taken of a person.

        parameter
        ---------
        i: str
            Index of the person enquired
        vaccine_ls: list
            List of vaccines used in this simulation
        '''
        vaccine_used = None
        self.logger.debug(f"Checking last vaccine from {self.people[i].id}")
        for t in range(len(self.people[i].vaccine_history)-1, -1, -1):
            if self.people[i].vaccine_history[t] == 1:
                vaccine_used = "1"
                self.logger.debug(f"\t Checked: Used normal vaccine. ")
                break
            elif self.people[i].vaccine_history[t] != 0:
                vaccine_used = self.people[i].vaccine_history[t]
                self.logger.debug(f"\t Checked: Used {vaccine_used}. ")
                break
        # No vaccination history, signal to take first one
        if vaccine_used == None:
            self.logger.debug("\t Checked: No vaccination history. ")
            return None
        # Choosing which vaccine (object) taken
        for vaccine in vaccine_ls:
            parsed_vaccine_used = vaccine_used.split(":")
            parsed_vaccine_used_brand = parsed_vaccine_used[0]
            parsed_vaccine_used_dose = int(parsed_vaccine_used[1])
            latest_vaccine = self.check_latest_dose(vaccine_ls, parsed_vaccine_used_brand)

            if parsed_vaccine_used_brand == vaccine.brand:
                self.logger.debug(f"\tFound vaccine {vaccine.brand}...")
                if latest_vaccine == parsed_vaccine_used_dose and parsed_vaccine_used_dose == vaccine.dose:
                    self.logger.debug(f"\tTaking last booster again (Excpected: {latest_vaccine}, Actual: {vaccine.dose}).")
                    vaccine_used = vaccine
                    return vaccine_used
                elif vaccine.dose >= parsed_vaccine_used_dose and latest_vaccine >= parsed_vaccine_used_dose:
                    self.logger.debug(f"\tCurrently taking {vaccine.dose}-th booster.")
                    vaccine_used = vaccine
                    return vaccine_used
        return None

    def check_next_vaccine(self, i, vaccine_ls, last_vaccine_taken):
        '''

        Parameters
        ----------
        i: int
            Index number in population list.
        vaccine_ls: list of Vaccine
            List of vaccines available.
        last_vaccine_taken: Vaccine
            Last vaccine taken.

        Returns
        -------
        vaccine: Vaccine
            The vaccine to-be taken, if there is one.
        '''
        self.logger.debug(last_vaccine_taken)
        if last_vaccine_taken == None:
            for vaccine in vaccine_ls:
                if vaccine.dose == 1:
                    self.logger.debug(f'Found first vaccine for {self.people[i].id}: {vaccine.brand}:{vaccine.dose}. ')
                return vaccine
        self.logger.debug(f'**{last_vaccine_taken.brand}:{last_vaccine_taken.dose}, {type(last_vaccine_taken.dose)}')
        for vaccine in vaccine_ls:
            self.logger.debug(f'{vaccine.brand}:{vaccine.dose}, {type(vaccine.dose)}')
            if (last_vaccine_taken.dose + 1) == vaccine.dose:
                self.logger.debug(f'Found next vaccine for {self.people[i].id}: {vaccine.brand}:{vaccine.dose}. ')
                return vaccine
        self.logger.debug(f'No vaccines required for {self.people[i].id}. ')
        return None

    def write_vaccine_history(self, i, vaccine, verbose=False):
        if vaccine == None:
            self.people[i].vaccine_history.append(0)
            return
        if self.vaccine_doses[vaccine.brand] > 1:
            self.people[i].vaccine_history.append(vaccine.brand + ":" + str(vaccine.dose))
        else:
            self.people[i].vaccine_history.append(vaccine.brand)

    def take_multi_dose_vaccine(self, i, vaccine_ls):
        # If person first time, then return
        # Need to find from the person history (not compartment) as vaccines have efficacy.
        # V compartmemt implies immunity.
        vaccine_taken_flag = False
        for t in range(len(self.people[i].vaccine_history)):
            if self.people[i].vaccine_history[t] != 0:
                vaccine_taken_flag = True
        if not vaccine_taken_flag:
            # Find vaccine of first dose
            for vaccine in vaccine_ls:
                if vaccine.dose == 1:
                    vaccine_used = vaccine
                    break
            # Take the vaccine
            seed = random.randint(0, 10000) / 10000
            if seed < vaccine_used.alpha_V:
                self.people[i].vaccinated = 1
                self.logger.debug(
                    f"Person {self.people[i].id} took vaccine {vaccine_used.brand}:{vaccine_used.dose}. ({seed} < {vaccine_used.alpha_V})")
                return vaccine_used
            else:
                self.logger.debug(f"Person {self.people[i].id} did not take vaccine {vaccine_used.brand}:{vaccine_used.dose}. ({seed} >= {vaccine_used.alpha_V})")
                return None

        # Check which vaccine is taken (and take the next booster)
        self.logger.debug(f"Person {self.people[i].id} is seeking to take next dose of vaccine.")
        for t in range(len(self.people[i].vaccine_history)-1, -1, -1):
            if type(self.people[i].vaccine_history[t]) == str:
                vaccine_brand = self.people[i].vaccine_history[t].split(":")[0]
                vaccine_dose = int(self.people[i].vaccine_history[t].split(":")[1])
                days_before = len(self.people[i].vaccine_history) - t
                self.logger.debug(f"\tRecent vaccine taken at day {t} (Length: {len(self.people[i].vaccine_history)}). ")
                break
        self.logger.debug(f'\tBrand: {vaccine_brand}, Dose: {vaccine_dose}, Days taken: {days_before-1} days. ')

        vaccine_used = None
        for vaccine in vaccine_ls:
            # Find next dose
            if vaccine_brand == vaccine.brand and vaccine_dose + 1 == vaccine.dose:
                vaccine_used = vaccine
                break
        if vaccine_used == None:
            return None
        # Check when the vaccine is taken (and if it is the time to take the second dose)
        # e.g. ls[-1] means day before, ls[-2] means 2 days before. This is possible when the current history is yet appended to ls.
        if days_before < vaccine_used.days_to_next_dose:
            self.logger.debug(f'Vaccine taken {days_before} days before. {vaccine_used.days_to_next_dose} days to next dose. ')
            self.logger.debug(f"Person {i+1} has taken vaccine recently. Need to wait for another {vaccine_used.days_to_next_dose - days_before} days. ")
            return None

        # Take the (next) vaccine
        seed = random.randint(0, 10000) / 10000
        if seed < vaccine_used.alpha_V:
            # Efficacy
            seed_e = random.randint(0, 10000) / 10000
            if seed_e < vaccine_used.efficacy:
                self.logger.debug(f'{self.people[i].id} has taken vaccine {vaccine_used.brand} dose {vaccine_used.dose} with efficacy {vaccine_used.efficacy} and wear-off rate {vaccine_used.phi_V}.')
                self.people[i].vaccinated = 1
                return vaccine_used
        return None


'''
20: Intimacy game
'''


class Mode20(Mode):
    def __init__(self, people, contact_nwk, beta, logger):
        super().__init__(people, 20, 'Intimacy game', logger)
        self.contact_nwk = contact_nwk
        self.beta = beta
        self.local_infection_p = np.ones(len(self.people))  # The proportion, not number of cases.
        self.theta = np.ones(len(self.people))

        # Weights on local and global pereption
        self.rho = 1
        self.ProbV = np.ones(len(self.people))

        # Payoff of each person based on:
        # * cV (cost of vaccination), or cI (cost of infection)
        # * Vaccinated or not
        # * Information spread
        self.cV = 1
        self.cI = 1
        self.cV_ls = np.ones(len(self.people)) * self.cV
        self.cV_ls = np.ones(len(self.people)) * self.cI
        # Increament of perceived risk
        self.kV = 0.6
        self.kI = 0.7
        # Spread of information
        self.sV = 0.8
        self.sI = 0.8
        # Prob advere event
        self.pV = 0.5
        self.pI = 0.5

    def set_rho(self, rho_temp):
        self.rho = super().correct_epi_para(rho_temp)

    def set_cV(self, cV_temp):
        self.cV = super().correct_epi_para(cV_temp)
        self.cV_ls = np.ones(len(self.people)) * self.cV

    def set_cI(self, cI_temp):
        self.cI = super().correct_epi_para(cI_temp)
        self.cV_ls = np.ones(len(self.people)) * self.cI

    def set_kV(self, kV_temp):
        self.kV = super().correct_epi_para(kV_temp)

    def set_kI(self, kI_temp):
        self.kI = super().correct_epi_para(kI_temp)

    def set_sV(self, sV_temp):
        self.sV = super().correct_epi_para(sV_temp)

    def set_sI(self, sI_temp):
        self.sI = super().correct_epi_para(sI_temp)

    def set_pV(self, pV_temp):
        self.pV = super().correct_epi_para(pV_temp)

    def set_pI(self, pI_temp):
        self.pI = super().correct_epi_para(pI_temp)

    def set_perceived_infection(self, global_infection, verbose=False):
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
            # If contact network exists
            for i in range(len(self.people)):
                for neighbour in self.contact_nwk.nwk_graph.neighbors(self.people[i]):
                    try:
                        if neighbour.suceptible == 1:
                            local_infection[i] += 1
                    except nx.exception.NetworkXError:
                        continue
                if verbose:
                    print(
                        f'{self.people[i].id} has {local_infection[i]} out {len(list(self.contact_nwk.nwk_graph.neighbors(self.people[i])))} contacts infected. ')
            self.local_infection_p = local_infection / len(self.people)
            self.theta = np.add(self.local_infection_p * self.rho,
                                np.ones(len(self.people)) * global_infection * (1 - self.rho))
        else:
            self.theta *= global_infection
            self.local_infection_p *= global_infection

    def assign_costs(self):
        '''
        Assign Mode20.cV and Mode20.cI to each person as initial values.
        '''
        for person in self.people:
            person.cV = self.cV
            person.cI = self.cI

    def event_vaccinated(self, i, verbose=False):
        if verbose:
            print(f'{self.people[i].id} is vaccinated, passing info to others... ')
        incr_cV = np.ones(len(self.people))

        # Adverse event
        seed = random.randint(0, 10000) / 10000
        if seed < self.pV:
            if self.contact_nwk != None:
                self.event_vaccinated_dfs(i, verbose)
            else:
                self.event_vaccinated_mixed(i, verbose)

    def event_vaccinated_mixed(self, i, verbose=False):
        '''
        Randomly pick neighbours and implement adverse event to them.
        '''
        other_person = random.choice(self.people)
        other_person += self.kV * self.sV

    def event_vaccinated_dfs(self, i, verbose=False):
        '''
        Run a DFS to all neigbours.
        '''
        visited = []
        layered_ls = []
        d = 1
        while len(visited) < len(self.contact_nwk.nwk_graph.nodes):
            layer = set(nx.algorithms.traversal.depth_first_search.dfs_preorder_nodes(self.contact_nwk.nwk_graph,
                                                                                      source=self.people[i],
                                                                                      depth_limit=d))
            # print(layer)
            layered_ls.append(layer)
            layered_ls[-1] = layered_ls[-1].difference(visited)

            # Add costs to vaccination
            for n in layered_ls[-1]:
                if n == self.people[i]:
                    continue
                n.cV += (self.kV * self.sV) ** d
                # print(n.cV+(d-1))
            d += 1

            # Fulfill visited ls
            for n in layer:
                visited.append(n)
        # return layered_ls

    def event_infected(self, i, verbose=False):
        self.logger.debug(f'{self.people[i].id} is infected, passing info to others... ')
        incr_cI = np.ones(len(self.people))

        # Adverse event
        seed = random.randint(0, 10000) / 10000
        if seed < self.pI:
            if self.contact_nwk != None:
                self.event_infected_dfs(i, verbose)
            else:
                self.event_infected_mixed(i, verbose)

    def event_infected_dfs(self, i, verbose=False):
        '''
        Run a DFS to all neigbours.
        '''
        visited = []
        layered_ls = []
        d = 1
        while len(visited) < len(self.contact_nwk.nwk_graph.nodes):
            layer = set(nx.algorithms.traversal.depth_first_search.dfs_preorder_nodes(self.contact_nwk.nwk_graph,
                                                                                      source=self.people[i],
                                                                                      depth_limit=d))
            # print(layer)
            layered_ls.append(layer)
            layered_ls[-1] = layered_ls[-1].difference(visited)

            # Add costs to vaccination
            for n in layered_ls[-1]:
                if n == self.people[i]:
                    continue
                n.cI += (self.kI * self.sI) ** d
                # print(n.cV+(d-1))
            d += 1

            # Fulfill visited ls
            for n in layer:
                visited.append(n)

    def event_infected_mixed(self, i, verbose=False):
        '''
        Randomly pick neighbours and implement adverse event to them.
        '''
        other_person = random.choice(self.people)
        other_person += self.kI * self.sI

    def get_payoff(self, i):
        self.people[i].payoff_V = -self.people[i].cV
        self.people[i].payoff_I = -self.people[i].cI * self.theta[i]
        return self.people[i].payoff_V - self.people[i].payoff_I

    def FDProb(self, i, verbose=False):
        '''
        Compute the probability from Fermi-Dirac distro
        '''
        if verbose:
            payoff = self.get_payoff(i)
            self.logger.debug(f'\tPayoff of {self.people[i].id} is {payoff}.')
        return 1 / (1 + math.exp(self.get_payoff(i)))

    def get_infected_neighbours_number(self, i):
        count = 0
        for neighbour in self.contact_nwk.nwk_graph.neighbors(self.people[i]):
            if neighbour.suceptible == 1:
                count += 1
        return count

    def IntimacyGame(self, beta, verbose=False):
        '''
        Simulate intimacy game of each time step.
        '''
        self.set_perceived_infection(beta)

        for i in range(len(self.people)):
            self.FDProb(i, verbose)

        for i in range(len(self.people)):
            if self.contact_nwk != None:
                if self.people[i].suceptible == 1:
                    self.event_infected(i, verbose)
                elif self.people[i].vaccinated == 1:
                    self.event_vaccinated(i, verbose)
            else:
                if self.people[i].suceptible == 1:
                    self.event_infected_mixed(i, verbose)
                elif self.people[i].vaccinated == 1:
                    self.event_vaccinated_mixed(i, verbose)


'''
21: Local Majority Rule
'''


class Mode21(Mode):
    def __init__(self, people, info_nwk, logger):
        super().__init__(people, 21, 'Local Majority Rule', logger)
        self.info_nwk = info_nwk

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 21. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set proportion of initial opinion below. ')
        propro_temp = input('Pro >>> ')
        self.info_nwk.propro = super().correct_para(propro_temp)
        agpro_temp = input('Ag >>> ')
        self.info_nwk.agpro = super().correct_para(agpro_temp)
        self.info_nwk.set_opinion()
        self.logger.info('All population has been assigned with their opinion. ')
        self.set_personality()
        self.logger.info('All population has been assigned with default personality. ')
        # Roster has been set already.
        self.raise_flag()
        self.logger.info('\nMode 21 equipped. \n')

    def set_personality(self):
        for person in self.people:
            person.personality = 0


'''
22: Stubbon to take vaccine
'''


class Mode22(Mode):
    def __init__(self, people, info_nwk, logger):
        super().__init__(people, 22, 'Stubbon to take vaccine', logger)
        self.info_nwk = info_nwk
        self.InflexProProportion = None

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 22. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set proportion of stubbon of pro-vaccine below. ')
        propro_temp = input('Pro >>> ')
        self.assign_personality(propro_temp)
        self.raise_flag()
        self.logger.info('\nMode 22 equipped. \n')

    def assign_personality(self, p):
        '''
        Assign some people with stubbon to take vaccine personality.
        '''

        self.logger.debug(f'Starting method Mode23.assign_personality()... ')
        p = super().set_correct_epi_para(p, 0)
        self.InflexProProportion = p
        self.logger.debug(f'Assigning stubbon to against vaccine personality. p = {self.InflexProProportion}')
        count = 0
        for person in self.people:
            if person.personality == 0:
                seed = random.randint(0, 1000) / 1000
                if seed < p:
                    person.personality = 1
                    person.opinion = 1
                    self.logger.debug(f'{person.id} is stubbonly pro-vaccine. ')
                    count += 1
        self.logger.debug(f'{count} people are stubbonly pro-vaccine. ')


'''
23: Stubbon to against vaccine
'''


class Mode23(Mode):
    def __init__(self, people, info_nwk, logger):
        super().__init__(people, 23, 'Stubbon to against vaccine', logger)
        self.info_nwk = info_nwk
        self.InflexAgProportion = None

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 23. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set proportion of stubbon of anti-vaccine below. ')
        agpro_temp = input('Pro >>> ')
        self.assign_personality(agpro_temp)
        self.raise_flag()
        self.logger.info('\nMode 23 equipped. \n')

    def assign_personality(self, p):
        '''
        Assign some people with stubbon to against vaccine personality.
        '''
        count0 = 0
        count1 = 0
        if type(self.people[0].personality) != int:
            for person in self.people:
                seed = random.randint(0, 1000) / 1000
                if seed < self.info_nwk.get_prop():
                    person.opinion = 1
                    count1 += 1
                else:
                    person.opinion = 0
                    count0 += 1
        self.logger.debug(f'Assigned {count1} pro and {count0} against vaccine to {len(self.people)} people. ')

        p = super().set_correct_epi_para(p, 0)
        self.InflexAgProportion = p
        self.logger.debug(f'Assigning stubbon to against vaccine personality. (p = {p})')
        count = 0
        for person in self.people:
            seed = random.randint(0, 1000) / 1000
            self.logger.debug(f'Assigning personlity for {person.id}. Seed: {seed}, p = {p}. ')
            if seed < p:
                person.personality = 2
                person.opinion = 0
                self.logger.debug(f'{person.id} is stubbonly against vaccine. ')
                count += 1
        self.logger.debug(f'{count} people are stubbonly against vaccine. ')


'''
24: Contrary to social groups
'''


class Mode24(Mode):
    def __init__(self, people, info_nwk, logger):
        super().__init__(people, 24, 'Contrary to social groups', logger)
        self.info_nwk = info_nwk
        self.BalancerProportion = None

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 24. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set proportion of contrarian below. ')
        balpro_temp = input('Pro >>> ')
        self.assign_personality(balpro_temp)
        self.assign_personality()
        self.raise_flag()
        self.logger.info('\nMode 24 equipped. \n')

    def assign_personality(self, p):
        '''
        Assign people with balancer personality.
        '''
        p = super().set_correct_epi_para(p, 0)
        self.BalancerProportion = p
        self.logger.debug(f'Assigning balancer personality. p = {self.BalancerProportion}')
        count = 0
        for person in self.people:
            if person.personality == 0:
                seed = random.randint(0, 1000) / 1000
                if seed < p:
                    person.personality = 3
                    self.logger.debug(f'{person.id} is balancer. ')
                    count += 1
        self.logger.debug(f'{count} people are balancers. ')


'''
31: Medication incorporated
'''


class Mode31(Mode):
    def __init__(self, people, logger):
        super().__init__(people, 31, 'Medication incorporated', logger)

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 31. ')
        self.logger.info('-------------------------\n')
        self.raise_flag()
        self.logger.info('\nMode 31 equipped. \n')


'''
43: Advanced immunity period settings
'''

class Mode43(Mode):
    def __init__(self, people, logger, instructions):
        super().__init__(people, 43, 'Advanced immunity period settings', logger)
        self.instructions = instructions

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 43. ')
        self.logger.info('-------------------------\n')

        # Loop all possible instructions
        cmd = ''
        while cmd != '':
            tmp_instructions = input('Enter instructions:')
            tmp_immunity_period = input('Enter immunity period:')

            # Check format and append
            self.instructions[self.correct_instructions_format(tmp_instructions)] = self.correct_para(tmp_immunity_period, pos=True)

            cmd = input('Continue? [y/n]')
            if cmd == '' or cmd.lower() == 'n':
                break

        self.raise_flag()
        self.logger.info('\nMode 43 equipped. \n')

    def correct_instructions_format(self):
        '''
        Correct the format to 'nVmI' where n and m are integers. So that Mode43.is_immuned() can read easily.

        Also '1V' -> 'V' or '1I' -> 'I'.

        'default is 'V' but no need to change.
        '''

        import re

        for k, v in list(self.instructions.items()):
            # Check V and I
            if k == 'V' or k == 'I':
                self.logger.debug(f'Read "{k}" as immune time instructions successfully. ')
                continue

            # Check if only have alphabets (or numbers), then correct it
            if re.match('(^\w$)|(^\d$)', k):
                self.logger.warn(f'{k} is not a valid instruction and will be deleted. ')
                del self.instructions[k]
                continue

            # V|I (w/ number)
            if re.match('^\d+\w$', k):
                if re.match('^1(V|I)', k):
                    self.logger.debug(f'Correcting "{k}" without the redundant "1" in front. ')
                    new_key = k[-1] # The last char must be correct
                    self.instructions[new_key] = v
                    del self.instructions[k]
                elif re.match('^\d+(V|I)$', k):
                    self.logger.debug(f'Read "{k}" as immune time instructions successfully. ')
                else:
                    self.logger.warn(f'{k} is not a valid instruction and will be deleted. ')
                    del self.instructions[k]
                continue

            if re.match('^(V|I)\d+$', k):
                new_key = re.findall('\d+', k)[0] + re.findall('(V|I)+', k)[0]
                self.logger.warn(f'{k} is not a valid instruction and will be corrected as "{new_key}". ')
                self.instructions[new_key] = v
                del self.instructions[k]
                self.logger.debug(f'Created {k} into instructions. ')
                continue

            # V&I (w/ number)
            if re.match('^\d+\w\d+\w$', k):
                if re.match('^\d+V\d+I$', k):
                    self.logger.debug(f'Read "{k}" as immune time instructions successfully. ')
                elif re.match('^\d+I\d+V$', k):
                    new_key = re.findall('\d+', k)[1] + 'V' + re.findall('\d+', k)[0] + 'I'
                    self.logger.warn(f'{k} is not a valid instruction and will be corrected as "{new_key}". ')
                    self.instructions[new_key] = v
                    del self.instructions[k]
                    self.logger.debug(f'Created {k} into instructions. ')
                else:
                    self.logger.warn(f'{k} is not a valid instruction and will be deleted. ')
                    del self.instructions[k]
                continue

            # If the conditions are not catched, then delete them
            self.logger.warn(f'{k} is not a valid instruction and will be deleted. ')
            del self.instructions[k]


    def count_vaccine_taken(self, i, brand=None):
        '''
        Count the number of vaccines taken for person i

        Parameters
        ----------
        i: int
            Person ID (In the self.population list)
        brand: str or list
            Brand of interest

        Returns
        -------
        vaccine_taken: int
            Number of vaccines taken at count
        '''
        t = 0
        vaccine_taken = 0
        while t < len(self.people[i].vaccine_history):
            if self.people[i].vaccine_history[t] != 0:
                vaccine_taken += 1
            t += 1

        return vaccine_taken

    def count_infected_times(self, i):
        '''
        Count the number of times being infected taken for person i

        Parameters
        ----------
        i: int
            Person ID (In the self.population list)

        Returns
        -------
        infected_times: int
            Number of infection at count
        '''
        t = 0
        infected_times = 0

        # Day 0
        if len(self.people[i].compartment_history) == 0:
            return 0

        # Day 1
        if self.people[i].compartment_history[t] == 'E':
            infected_times += 1
        t += 1

        # From next day
        while t < len(self.people[i].compartment_history):
            if self.people[i].compartment_history[t] == 'E' and (self.people[i].compartment_history[t-1] == 'S' or self.people[i].compartment_history[t-1] == 'V'):
                infected_times += 1
            elif self.people[i].compartment_history[t] == 'R':
                break
            t += 1

        return infected_times

    def get_immune_time(self, i):
        '''
        Check if the person immuned based on Mode43.instructions.

        Parameters
        ----------
        i: int
            Person ID (In the self.population list)

        Returns
        -------
        immune_time: int (or None)
            If the person is immuned from transmission.
        '''

        # Check how many vaccines taken and how many times been infected
        vaccine_taken = self.count_vaccine_taken(i)
        infected_times = self.count_infected_times(i)

        # Lookup to Mode43.instructions
        # ================================================
        #
        # If person has taken one vaccine and no prior infection, check 'V' or default
        # If person has taken two vaccines and no prior infection, check '2V' (If only '2VnI' exists, then no immunity)
        # If person has been infected, check 'I'
        # If person has been infected and instruction says '2V1I', nothing happens.
        #
        # ================================================

        self.logger.debug(f'Person {i} has taken {vaccine_taken} vaccines and infected {infected_times} times. ')

        v_counter = vaccine_taken
        i_counter = infected_times

        while v_counter > 0:
            while i_counter >= 0:
                if i_counter == 0:
                    target_instruction = f'{v_counter}V'
                else:
                    target_instruction = f'{v_counter}V{i_counter}I'
                self.logger.debug(f'Checking rule {target_instruction}. ')
                if target_instruction in self.instructions:
                    return self.instructions[target_instruction]
                i_counter -= 1
            v_counter -= 1

        # Check if '0' exists
        if '0' in self.instructions:
            self.logger.debug(f'Checking rule "0". ')
            return self.instructions['0']

        self.logger.debug('No suitable instructions found, referring to default instructions. ')

'''
51: Erdos-Renyi topology
'''


class Mode51(Mode):
    def __init__(self, people, contact_nwk, logger):
        super().__init__(people, 51, 'Erdos-Renyi topology', logger)
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

    def set_pupdate(self, p):
        '''
        Set probability to update network
        '''
        if p > 1:
            self.contact_nwk.PUpdate = 1
        elif p < 0:
            self.contact_nwk.PUpdate = 0
        else:
            self.contact_nwk.PUpdate = p

    def set_l0(self, l0):
        '''
        Set probability to debond
        '''
        if l0 > 1:
            self.contact_nwk.l0 = 1
        elif l0 < 0:
            self.contact_nwk.l0 = 0
        else:
            self.contact_nwk.l0 = l0

    def set_l1(self, l1):
        '''
        Set probability to rebond
        '''
        if l1 > 1:
            self.contact_nwk.l1 = 1
        elif l1 < 0:
            self.contact_nwk.l1 = 0
        else:
            self.contact_nwk.l1 = l1

    def __call__(self):
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 51. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set infection parameter below. ')
        try:
            p_temp = float(input('p >>> '))
        except ValueError:
            print('Invalid data type for p, set p as 1. ')
            p_temp = 1
        self.set_p(p_temp)
        cmd = input('Longitudinal social network? [y/n] ')
        if cmd == 'y':
            self.logger.info('Default rule: independent update. ')
            cmd_update_rule = input('Change? [y/n] ')
            if cmd_update_rule == 'y':
                self.contact_nwk.update_rule = 'XBS'
                pUpd_temp = float(input('p >>> '))
                pUpd = super().set_correct_epi_para(pUpd_temp, self.contact_nwk.PUpdate)
                self.set_pupdate(pUpd)
            else:
                self.contact_nwk.update_rule = 'random'
                l0_temp = float(input('l0 >>> '))
                l0 = super().set_correct_epi_para(l0_temp, self.contact_nwk.l0)
                self.set_p(l0)
        self.set_network()
        self.raise_flag()
        self.logger.info('E-R graph settings done.')


'''
52: Preferential attachment
'''


class Mode52(Mode):
    def __init__(self, people, logger, contact_nwk=None):
        super().__init__(people, 52, 'Preferential attachment', logger)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.m = 1  # No. of new edges linked

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

    def set_pupdate(self, p):
        '''
        Set probability to update network
        '''
        if p > 1:
            self.contact_nwk.PUpdate = 1
        elif p < 0:
            self.contact_nwk.PUpdate = 0
        else:
            self.contact_nwk.PUpdate = p

    def set_l0(self, l0):
        '''
        Set probability to debond
        '''
        if l0 > 1:
            self.contact_nwk.l0 = 1
        elif l0 < 0:
            self.contact_nwk.l0 = 0
        else:
            self.contact_nwk.l0 = l0

    def set_l1(self, l1):
        '''
        Set probability to rebond
        '''
        if l1 > 1:
            self.contact_nwk.l1 = 1
        elif l1 < 0:
            self.contact_nwk.l1 = 0
        else:
            self.contact_nwk.l1 = l1

    def set_m(self, m):
        if m < 1:
            self.m = 1
        else:
            self.m = m

    def __call__(self):
        '''
        Setting mode 52 into model. If other network modes have set, they are dropped by `main.py`.
        '''
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 52. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set connection parameter below. ')
        try:
            m_temp = int(input('m >>> '))
        except ValueError:
            print('Invalid data type for m, set m as 1. ')
            m_temp = 1
        self.set_m(m_temp)

        cmd = input('Longitudinal social network? [y/n] ')
        if cmd == 'y':
            self.logger.info('Default rule: Xulvi-Brunet Sokolov. ')
            cmd_update_rule = input('Change? [y/n] ')
            if cmd_update_rule == 'y':
                self.contact_nwk.update_rule = 'random'
                l0_temp = float(input('l0 >>> '))
                l0Upd = super().set_correct_epi_para(l0_temp, self.contact_nwk.l0)
                self.set_l0(l0Upd)
                l1_temp = float(input('l1 >>> '))
                l1Upd = super().set_correct_epi_para(l1_temp, self.contact_nwk.l1)
                self.set_l1(l1Upd)
            else:
                self.contact_nwk.update_rule = 'XBS'
                pUpd_temp = float(input('p >>> '))
                pUpd = super().set_correct_epi_para(pUpd_temp, self.contact_nwk.PUpdate)
                self.set_pupdate(pUpd)
        self.set_network()
        self.raise_flag()
        self.logger.info('Preferential attachment graph settings done.')


'''
53: Small world network
'''


class Mode53(Mode):
    def __init__(self, people, logger, contact_nwk=None):
        super().__init__(people, 53, 'Small world network', logger)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.k = 1  # k neighbours are joined
        self.p = 1  # Rewiring probability

    def set_network(self):
        '''
        Setup the network and nwk_graph
        '''
        self.contact_nwk.nwk_graph = nx.generators.random_graphs.watts_strogatz_graph(len(self.people), self.k, self.p)

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

    def set_pupdate(self, p):
        '''
        Set probability to update network
        '''
        if p > 1:
            self.contact_nwk.PUpdate = 1
        elif p < 0:
            self.contact_nwk.PUpdate = 0
        else:
            self.contact_nwk.PUpdate = p

    def set_l0(self, l0):
        '''
        Set probability to debond
        '''
        if l0 > 1:
            self.contact_nwk.l0 = 1
        elif l0 < 0:
            self.contact_nwk.l0 = 0
        else:
            self.contact_nwk.l0 = l0

    def set_l1(self, l1):
        '''
        Set probability to rebond
        '''
        if l1 > 1:
            self.contact_nwk.l1 = 1
        elif l1 < 0:
            self.contact_nwk.l1 = 0
        else:
            self.contact_nwk.l1 = l1

    def __call__(self):
        '''
        Setting mode 53 into model. If other network modes have set, they are dropped by `main.py`.
        '''
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 53. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set infection parameter below. ')
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
        '''
        Set update rule
        '''
        cmd = input('Longitudinal social network? [y/n] ')
        if cmd == 'y':
            self.logger.info('Default rule: independent update. ')
            cmd_update_rule = input('Change? [y/n] ')
            if cmd_update_rule == 'y':
                self.contact_nwk.update_rule = 'XBS'
                pUpd_temp = float(input('p >>> '))
                pUpd = super().set_correct_epi_para(pUpd_temp, self.contact_nwk.PUpdate)
                self.set_pupdate(pUpd)
            else:
                self.contact_nwk.update_rule = 'random'
                l0_temp = float(input('l0 >>> '))
                l0Upd = super().set_correct_epi_para(l0_temp, self.contact_nwk.l0)
                self.set_l0(l0Upd)
                l1_temp = float(input('l1 >>> '))
                l1Upd = super().set_correct_epi_para(l1_temp, self.contact_nwk.l1)
                self.set_l1(l1Upd)
        self.set_network()
        self.raise_flag()
        self.logger.info('Watts-Strogatz graph settings done.')


'''
54: Lattice network
'''


class Mode54(Mode):
    def __init__(self, people, logger, contact_nwk=None):
        super().__init__(people, 54, 'Lattice network', logger)
        # Initially set partner living in the same region.
        self.contact_nwk = contact_nwk
        self.m = 1  # Nunber of rows
        self.n = len(self.people) // self.m  # Nunber of columns

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
        self.n = len(self.people) // self.m

    def set_pupdate(self, p):
        '''
        Set probability to update network
        '''
        if p > 1:
            self.contact_nwk.PUpdate = 1
        elif p < 0:
            self.contact_nwk.PUpdate = 0
        else:
            self.contact_nwk.PUpdate = p

    def set_l0(self, l0):
        '''
        Set probability to debond
        '''
        if l0 > 1:
            self.contact_nwk.l0 = 1
        elif l0 < 0:
            self.contact_nwk.l0 = 0
        else:
            self.contact_nwk.l0 = l0

    def set_l1(self, l1):
        '''
        Set probability to rebond
        '''
        if l1 > 1:
            self.contact_nwk.l1 = 1
        elif l1 < 0:
            self.contact_nwk.l1 = 0
        else:
            self.contact_nwk.l1 = l1

    def __call__(self):
        '''
        Setting mode 52 into model. If other network modes have set, they are dropped by `main.py`.
        '''
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 54. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set infection parameter below. ')
        try:
            m_temp = int(input('m >>> '))
        except ValueError:
            print('Invalid data type for m, set m as 1. ')
            m_temp = 1
        self.set_dim(m_temp)
        '''
        Set update rule
        '''
        cmd = input('Longitudinal social network? [y/n] ')
        if cmd == 'y':
            self.logger.info('Default rule: independent update. ')
            cmd_update_rule = input('Change? [y/n] ')
            if cmd_update_rule == 'y':
                self.contact_nwk.update_rule = 'XBS'
                pUpd_temp = float(input('p >>> '))
                pUpd = super().set_correct_epi_para(pUpd_temp, self.contact_nwk.PUpdate)
                self.set_pupdate(pUpd)
            else:
                self.contact_nwk.update_rule = 'random'
                l0_temp = float(input('l0 >>> '))
                l0Upd = super().set_correct_epi_para(l0_temp, self.contact_nwk.l0)
                self.set_l0(l0Upd)
                l1_temp = float(input('l1 >>> '))
                l1Upd = super().set_correct_epi_para(l1_temp, self.contact_nwk.l1)
                self.set_l1(l1Upd)
        self.set_network()
        self.raise_flag()
        self.logger.info('Preferential attachment graph settings done.')


'''
501: Initial infection by number
'''


class Mode501(Mode):
    def __init__(self, people, logger, contact_nwk=None):
        super().__init__(people, 501, 'Initial infection by number', logger)
        self.contact_nwk = contact_nwk
        self.init_infection = 4

    def __call__(self):
        '''
        Setting mode 501 into model.
        '''
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 501. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set initial infection number below. ')
        Ii_temp = input('>>> ')
        self.init_infection = super().set_correct_para(Ii_temp, self.init_infection)
        self.raise_flag()
        self.logger.info('\nMode 501 equipped. \n')

    def set_init_infection(self, Ii):
        return self.correct_para(Ii, pos=True)


'''
505: Initial infection by degree
'''


class Mode505(Mode):
    def __init__(self, people, logger, contact_nwk):
        super().__init__(people, 505, 'Initial infection by degree', logger)
        if type(contact_nwk) == ContactNwk and type(contact_nwk.nwk_graph) == nx.Graph:
            self.contact_nwk = contact_nwk
        else: raise ValueError('Unable to read contact network. ')
        self.modes = ['Hub', 'Leaf']
        self.mode = None

    def __call__(self):
        '''
        Setting mode 505 into model.
        '''
        self.logger.info('-------------------------')
        self.logger.info('You are creating mode 505. ')
        self.logger.info('-------------------------\n')
        self.logger.info('Please set initial infection mode below. ')
        self.logger.info('0\tInfect by leaf')
        self.logger.info('1\tInfect by hub')
        mode_505_temp = input('>>> ')
        try:
            if int(mode_505_temp) == 1:
                self.mode = 'Hub'
            elif int(mode_505_temp) == 0:
                self.mode = 'Leaf'
        except ValueError:
            if mode_505_temp.lower() == 'hub':
                self.mode = 'Hub'
            elif mode_505_temp.lower() == 'leaf':
                self.mode = 'Leaf'
        self.raise_flag()
        self.logger.info('\nMode 505 equipped. \n')

    def set_infection(self, init_infection=4):
        if self.mode == 'Hub':
            for person_deg in sorted(self.contact_nwk.nwk_graph.degree, key=lambda x: x[1], reverse=True)[
                              :init_infection]:
                person_deg[0].suceptible = 1
        elif self.mode == 'Leaf':
            for person_deg in sorted(self.contact_nwk.nwk_graph.degree, key=lambda x: x[1])[:init_infection]:
                person_deg[0].suceptible = 1
