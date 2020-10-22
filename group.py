import random

import write


class Group:

    def __init__(self):
        self.name = None   # Group name not defined until set_group()
        self.size = 0

    def get_people(self, people):
        self.people = people

    def set_group(self, size):
        self.size = size
        # print('There are {} people.'.format(len(self.people)))
        for i in range(len(self.people)):
            self.people[i].group_no = i // self.size
            # print('{}: Group {}'.format(i, self.people[i].group_no))
        self.get_number_of_groups()
        # print('There are {} groups.'.format(self.no_of_groups+1))   # len() means +1 of the last index of the list.

    def update_group(self,size):
        '''
        Permutate everyone into another group.
        '''
        self.size = size
        swap_id = []
        for i in range(len(self.people)):
            swap_id.append(self.people[i].group_no)
        random.shuffle(swap_id)
        for i in range(len(self.people)):
            self.people[i].group_no = swap_id[i]
        # self.get_number_of_groups()
        # print('There are {} groups.'.format(self.no_of_groups))


    def get_number_of_groups(self):
        self.no_of_groups = 0
        for i in range(len(self.people)):
            if self.people[i].group_no > self.no_of_groups:
                self.no_of_groups = self.people[i].group_no
        return self.no_of_groups

    def get_members(self, group_no):
        '''
        Get a list of people in the group. Remember group numbers starts from 0 to n-1

        o - opinion state.
        s - infected or not.
        '''
        # print('You are enquiring Group {}: '.format(group_no))
        counter = 0
        roster = [[],[],[]]
        for i in range(len(self.people)):
            if self.people[i].group_no == group_no:
                counter += 1
                roster[0].append(i)
                roster[1].append(self.people[i].opinion)
                roster[2].append(self.people[i].suceptible)
                # print('id: {}, o: {}, s: {}'.format(i, self.people[i].opinion, self.people[i].suceptible))
        # print('There are {} members in the group. \n'.format(counter))
        roster.append(counter)   # Get the number people in the group to the roster
        # print(roster)
        return roster

    def update(self, groups_of, filename):
        self.inflexible_prework()
        group_roster = []
        counter_flag = []   # How many 0 opinions in a group (i.e. group_roster[i][1]).
        result_flag = []
        o_state_update = []
        for i in range(self.no_of_groups+1):    # The length of group_roster is 1 plus than the number of groups.
            group_roster.append(self.get_members(i))

        '''
        Majority Rule
        '''
        # print(group_roster)
        for i in range(len(group_roster)):
            for j in range(1,len(group_roster[i])-2):   # The last element in group_roster is the total number of members.
                counter = 0 # Count how many 0's.
                for k in range(len(group_roster[i][j])):
                    if group_roster[i][j][k] == 0:
                        counter += 1
            counter_flag.append(counter)
        # print('')
        # print('counter of 0\'s:', counter_flag)
        # print(' ')
        for i in range(len(counter_flag)):
            # print('counter_flag[{}]: {}'.format(i, counter_flag[i]), type(counter_flag[i]))
            # print('len(group_roster[{}][1])//2: {}'.format(i, len(group_roster[i][1])//2), type(len(group_roster[i][1])//2))
            # print(counter_flag[i] > (len(group_roster[i][1])//2))
            if counter_flag[i] > (len(group_roster[i][1])//2):
                result_flag.append(0)
            else:
                result_flag.append(1)
        # print(result_flag)

        # print(' ')
        for i in range(len(group_roster)):
            # print('It is meant to be {}'.format(result_flag[i]))
            # print(group_roster[i][1])
            for j in range(len(group_roster[i][1])):
                group_roster[i][1][j] = result_flag[i]
                o_state_update.append(result_flag[i])
            # print('After:', group_roster[i][1])

        for i in range(len(self.people)):
            self.people[i].opinion = o_state_update[i]
        print('')

        self.inflexible()
        self.balance()
        self.update_group(groups_of)
        write.WriteOpinion(self, filename)

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
