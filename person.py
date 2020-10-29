'''
Model Opinion Dynamics and separate them into groups of 3
'''

import numpy as np
import random

class Person:
    id = 0 # Initial population

    def __init__(self, personality = 0):
        Person.id += 1  # Name of the person.
        self.id = Person.id

        self.opinion = 1 #random.choices([0, 1], weights = [2, 8], k = 1)[0]
        self.meta_opinion = None

        self.location = 0
        '''
        0 - City
        1 - Rural
        '''

        # Bounded rationality
        self.rV_BR = random.randint(0,1000)/1000
        self.lambda_BR = random.randint(0,1000)/1000

        self.occupation = 0
        '''
        0 - Not specified
        1 - Essential workers
        '''

        self.wealth = 1000

        self.group_no = None

        # Personality
        '''
        0 - Normal
        1 - Inflexible
        2 - Balancer
        '''
        self.personality = personality

        # Epidemic state
        self.suceptible = 0 #int(round(random.uniform(0, 1), 0))   # 0 means without disease, 1 means infected
        self.exposed    = 0
        self.vaccinated = 0 # Assume all 0 (None of them took vaccine).
        self.removed    = 0 # 0 means not in R compartment, 1 is.

        self.infection_clock = 0

        # Travelling overseas
        self.overseas = None
        self.A = None
        self.rS_overseas = None
        self.rI_overseas = None

        # Demographics
        self.age = None
        self.gender = None  # 0 means male, 1 means female 

        self.compartment_history = []
        self.check_history = []

    def make_population(N):
        population = []
        for i in range(N):
            population.append(Person())
        return population

    def set_age(self):
        age = random.choices(np.linspace(0, 90, 10), weights = [14.5, 16.2, 15.5, 18.9, 14.1, 10.1, 7.4, 2.2, 1, 0.1], k = 1)[0]
        age += random.randint(0,9)
        self.age = age

    def set_gender(self):
        self.gender = random.choices([0, 1], weights = [5, 5], k = 1)[0]

    def swap_opinion(self):
        if self.opinion == 0:
            self.opinion = 1
        else:
            self.opinion = 0