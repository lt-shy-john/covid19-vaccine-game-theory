import sys, os
import random

from unittest import TestCase
from person import Person

# Fetch the files from root level
sys.path.append(os.path.abspath(os.path.join('..')))

class TestPersonInit(TestCase):
    def before(self):
        self.person = Person()


class TestMakePopulation(TestCase):
    def test_make_population(self):
        '''Test the make_population() create a list of people'''
        N = random.randint(1, 100)
        population = Person.make_population(N)

        # Assert the length is N
        self.assertEqual(len(population), N)

class TestSetAge(TestPersonInit):
    def test_set_age(self):
        self.person.set_age()

        # Assert the age is an integer
        self.assertEqual(type(self.person.age), int)
    #
    # def test_set_gender(self):
    #     self.fail()
    #
    # def test_swap_opinion(self):
    #     self.fail()
