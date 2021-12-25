import sys, os
import numpy
import random

from unittest import TestCase
from person import Person

# Fetch the files from root level
sys.path.append(os.path.abspath(os.path.join('..')))

class TestPerson(TestCase):

    def test_make_population(self):
        '''Test the make_population() create a list of people'''
        N = random.randint(1, 100)
        population = Person.make_population(N)

        # Assert the length is N
        self.assertEqual(len(population), N)

    def test_set_age(self):
        self.person = Person()

        self.person.set_age()

        # Assert the age is an integer
        self.assertEqual(type(self.person.age), int)


    def test_set_gender(self):
        self.person = Person()

        self.person.set_gender()

        # Assert the age is an integer
        self.assertEqual(type(self.person.gender), int)
        # Assigned gender is random
        self.assertTrue(self.person.gender == 0 or self.person.gender == 1)

    def test_swap_opinion_0(self):
        self.person = Person()
        self.person.opinion = 1

        self.person.swap_opinion()

        self.assertEqual(self.person.opinion, 0)

    def test_swap_opinion_1(self):
        self.person = Person()
        self.person.opinion = 0

        self.person.swap_opinion()

        self.assertEqual(self.person.opinion, 1)
