import random


class Group:
    def __init__(self, people, logger, group_size=3):
        self.people = people
        self.size = group_size

        self.propro = None
        self.agpro = None

        self.roster = {}

        self.set_population()
        self.set_roster()

        self.logger = logger

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

    def get_prop(self):
        return self.propro / (self.propro + self.agpro)

    def set_pro(self, propro_temp):
        if propro_temp >= 1:
            self.propro = self.correct_para(propro_temp)
        elif 0 <= propro_temp < 1:
            self.logger.info("Treating input (Against vaccine) as decimal proportion. ")
            self.propro = self.correct_epi_para(propro_temp) * 100

    def set_ag(self, ag_temp):
        if ag_temp >= 1:
            self.agpro = self.correct_para(ag_temp)
        elif 0 <= ag_temp < 1:
            self.logger.info("Treating input (Against vaccine) as decimal proportion. ")
            self.agpro = self.correct_epi_para(ag_temp) * 100

    def set_opinion(self):
        for person in self.people:
            seed = random.randint(0, 1000) / 1000
            if seed < self.get_prop():
                person.opinion = 1
            else:
                person.opinion = 0
            self.logger.debug(f'{person.id} has opinion of {person.opinion}. ')

    def update_group(self):
        '''
        Permutate everyone into another group.
        '''
        # print(self.roster)
        for group_no, members in self.roster.items():
            for member in members:
                self.logger.debug(f'{member.id} is in Group {group_no}')
                self.roster[group_no].remove(member)
                dest_group = random.randint(0,len(self.people) // self.size)
                self.logger.debug(f'They should be moved to Group {dest_group}')
                self.logger.debug(f'This group has currently have members: {[p.id for p in self.roster[dest_group]]}. ')
                self.roster[dest_group].append(member)
                self.logger.debug(f'This group has currently now have members: {[p.id for p in self.roster[dest_group]]}. ')
                member.group_no = dest_group

                swap_out = self.roster[dest_group][random.randint(0,len(self.roster[dest_group])-1)]
                self.logger.debug(f'Group {dest_group} will remove {swap_out.id}. ')
                self.roster[dest_group].remove(swap_out)
                self.roster[group_no].append(swap_out)
                self.logger.debug(f'Group {dest_group} now have {[p.id for p in self.roster[dest_group]]}. \n\n')
                swap_out.group_no = dest_group

    def update(self):
        '''
        Update opinion using majority Rule
        '''
        for group_no, members in self.roster.items():
            total_opinion = 0
            for member in members:
                total_opinion += member.opinion
            self.logger.debug(f'Group {group_no} has total opinion of {total_opinion}. ')
            if total_opinion > len(members)//2:
                for member in members:
                    member.opinion = 1
                self.logger.debug(f'\tGroup {group_no}: {[{member.id: member.opinion} for member in members]}')
            else:
                for member in members:
                    member.opinion = 0
                self.logger.debug(f'\tGroup {group_no}: {[{member.id: member.opinion} for member in members]}')

    def inflexible_prework(self):
        '''
        Store opinions of inflexibles.
        '''
        for i in range(len(self.people)):
            if self.people[i].personality == 1:
                self.people[i].meta_opinion = 1
                self.logger.debug(f'{self.people[i].id}: {self.people[i].meta_opinion}')
            elif self.people[i].personality == 2:
                self.people[i].meta_opinion = 0
                self.logger.debug(f'{self.people[i].id}: {self.people[i].meta_opinion}')

    def inflexible(self):
        '''
        Restore opinions of inflexibles.
        '''
        for i in range(len(self.people)):
            if self.people[i].meta_opinion == 1:
                self.people[i].opinion = 1
            elif self.people[i].meta_opinion == 0:
                self.people[i].opinion = 0
                self.logger.debug(f'   *{self.people[i].id}: {self.people[i].opinion}')
            self.people[i].meta_opinion = None  # They will forget their deep believe until next round.

    def balance(self):
        for i in range(len(self.people)):
            if self.people[i].personality == 3:
                self.logger.debug('Before: {} - o:{}'.format(self.people[i].id, self.people[i].opinion))
                self.people[i].swap_opinion()
                self.logger.debug('After: {} - o:{}'.format(self.people[i].id, self.people[i].opinion))
