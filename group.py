import random

import write


class Group:
    def __init__(self, people, group_size=3):
        self.name = None   # Group name not defined until set_group()
        self.people = people
        self.size = group_size
        self.roster = {}

        self.set_population()
        self.set_roster()

    def set_population(self):
        '''
        Initially we assign group numbers according to their id.
        '''
        for person in self.people:
            person.group_no = len(self.people) // self.size

    def set_roster(self):
        for i in len(self.people) // self.size:
            self.roster[i] = []

    def update_group(self):
        '''
        Permutate everyone into another group.
        '''
        for group_no, members in self.roster.items():
            for member in members:
                self.roster[group_no].remove(member)
                dest_group = random.randint(0,len(self.people) // self.size)
                self.roster[dest_group].append(member)

                swap_out = self.roster[dest_group][random.randint(0,len(self.roster[dest_group]))]
                self.roster[dest_group].remove(swap_out)
                self.roster[group_no].append(swap_out)

    def update(self, filename):
        '''
        Update opinion using majority Rule
        '''
        # self.inflexible_prework()
        for group_no, members in self.roster.items():
            total_opinion = 0
            for member in members:
                total_opinion += member.opinion
            if total_opinion > len(members):
                for member in members:
                    member.opinion = 1
            else:
                for member in members:
                    member.opinion = 0
        # Further update due to group concensus.
        # self.inflexible()
        # self.balance()

        if filename != '':
            write.WriteOpinion(self, filename)
        self.update_group()

    def inflexible_prework(self):
        '''
        Store opinions of inflexibles.
        '''
        for i in range(len(self.people)):
            if self.people[i].personality == 1:
                if self.people[i].opinion == 1:
                    self.people[i].meta_opinion = 1
                else:
                    self.people[i].meta_opinion = 0

    def inflexible(self):
        '''
        Restore opinions of inflexibles.
        '''
        for i in range(len(self.people)):
            if self.people[i].meta_opinion == 1:
                self.people[i].opinion = 1
            elif self.people[i].meta_opinion == 0:
                self.people[i].opinion = 0
            self.people[i].meta_opinion = None  # They will forget their deep believe until next round.


    def balance(self):
        for i in range(len(self.people)):
            if self.people[i].personality == 2:
                # print('Before: {} - o:{}'.format(self.people[i].id, self.people[i].opinion))
                self.people[i].swap_opinion()
                # print('After: {} - o:{}'.format(self.people[i].id, self.people[i].opinion))
        # print('')
