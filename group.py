import random

import write


class Group:
    def __init__(self, people, group_size=3):
        self.people = people
        self.size = group_size
        self.roster = {}

        self.set_population()
        self.set_roster()

    def set_population(self):
        '''
        Initially we assign group numbers according to their id.
        '''
        for i in range(len(self.people)):
            self.people[i].group_no = i // self.size

    def set_roster(self):
        for i in range((len(self.people) // self.size)+1):
            self.roster[i] = []
        for i in range(len(self.people)):
            self.roster[self.people[i].group_no].append(self.people[i])

    def update_group(self, verbose_mode=False):
        '''
        Permutate everyone into another group.
        '''
        # print(self.roster)
        for group_no, members in self.roster.items():
            for member in members:
                if verbose_mode == True:
                    print(f'{member.id} is in Group {group_no}')
                self.roster[group_no].remove(member)
                dest_group = random.randint(0,len(self.people) // self.size)
                if verbose_mode == True:
                    print(f'They should be moved to Group {dest_group}')
                    print(f'This group has currently have members: {[p.id for p in self.roster[dest_group]]}. ')
                self.roster[dest_group].append(member)
                if verbose_mode == True:
                    print(f'This group has currently now have members: {[p.id for p in self.roster[dest_group]]}. ')

                swap_out = self.roster[dest_group][random.randint(0,len(self.roster[dest_group])-1)]
                if verbose_mode == True:
                    print(f'Group {dest_group} will remove {swap_out.id}. ')
                self.roster[dest_group].remove(swap_out)
                self.roster[group_no].append(swap_out)
                if verbose_mode == True:
                    print(f'Group {dest_group} now have {[p.id for p in self.roster[dest_group]]}. \n\n')

    def update(self, verbose_mode=False):
        '''
        Update opinion using majority Rule
        '''
        # self.inflexible_prework()
        for group_no, members in self.roster.items():
            total_opinion = 0
            for member in members:
                total_opinion += member.opinion
            if verbose_mode == True:
                print(f'Group {group_no} has total opinion of {total_opinion}. ')
            if total_opinion > len(members)//2:
                for member in members:
                    member.opinion = 1
            else:
                for member in members:
                    member.opinion = 0
        # Further update due to group concensus.
        # self.inflexible()
        # self.balance()



    def inflexible_prework(self):
        '''
        Store opinions of inflexibles.
        '''
        for i in range(len(self.people)):
            if self.people[i].personality == 1:
                self.people[i].meta_opinion = 1
            elif self.people[i].personality == 2:
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


    def balance(self, verbose_mode=False):
        for i in range(len(self.people)):
            if self.people[i].personality == 2:
                if verbose_mode == True:
                    print('Before: {} - o:{}'.format(self.people[i].id, self.people[i].opinion))
                self.people[i].swap_opinion()
                if verbose_mode == True:
                    print('After: {} - o:{}'.format(self.people[i].id, self.people[i].opinion))
        # print('')
