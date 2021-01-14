import random
import numpy as np

from contact import ContactNwk
import person
import write

class Epidemic:

    def __init__ (self, vaccinated, infection, recover, resus, remove, people, test_rate, immune_time, contact_nwk, verbose_mode, start=True):
        '''Initial elements

        Attributes
        ----------

        epidemic - int
            Flag epidemic starts or ends.

        people - People
            Agents for simulation
        '''
        self.epidemic = 0   # Whether an epidemic occured or not.
        self.people = people
        self.contact_nwk = contact_nwk
        self.mode = {}  # Dict of modes loaded. Values are mode objects

        try:
            if vaccinated >= 0 and vaccinated <= 1:
                self.vaccinated = vaccinated   # Probability to get vaccinated
            else:
                raise ValueError
            if infection >= 0 and infection <= 1:
                self.infection = infection
            else:
                raise ValueError
            if recover >= 0 and recover <= 1:
                self.recover = recover  # Recovery rate
            else:
                raise ValueError
            if remove >= 0 and remove <= 1:
                self.remove = remove  # Recovery rate
            else:
                raise ValueError
            if resus >= 0 and resus <= 1:
                self.resus = resus
            else:
                raise ValueError
            if test_rate >= 0 and test_rate <= 1:
                self.test_rate = test_rate
            else:
                raise ValueError

            self.immune_time = immune_time

            # Customised lifestyle rate. Call set_other_alpha_param() to set values.
            self.alpha_V = self.vaccinated
            self.alpha_T = self.vaccinated

            # Customised infection rate
            # self.infection_SS = 0.0
            # self.infection_II = 0.0
            # self.infection_II2 = 0.0
            # self.infection_RR = 0.01
            # self.infection_VV = 0.0
            # self.infection_IR = 0.01
            # self.infection_SR = 0.01
            # self.infection_SV = 0.01
            # self.infection_PI = 0.01
            # self.infection_IV = 0.01
            # self.infection_RV = 0.01
            # self.infection_SI2 = self.infection
            # self.infection_RI2 = 0.01
            # self.infection_VI2 = 0.01
            # self.infection_condom = 0.01
            # self.check_beta()

            # Auxillary parameter
            self.verbose_mode = verbose_mode


            '''Compartment statics

            Number of agents within a compartment.

            Attributes
            ----------
            S: int
                Number of people not infected (susceptible).
            U: int
                Number of people with COVID-19 symptoms observed.
            E: int
                Number of people with COVID-19 symptoms observed, assumed quarantined.
            I: int
                Sum of people in E and U. Number of infected agents.
            V: int
                Number of people taken PrEP
            R: int
                Number of people removed.
            Pro: int
                Number of agents willing to accept vaccine
            Ag: int
                Number of agents against of taking vaccine
            dS: int
                Difference of suceptible compartment at different times
            dI: int
                Difference of infected compartment at different times
            dV: int
                Difference of vaccinated (PrEP) compartment at different times
            '''
            self.S = len(self.people)
            self.U = 0
            self.E = 0
            self.I = self.U + self.E
            self.V = 0
            self.R = 0
            self.Pro = 0
            self.Ag = 0
            self.dS = -self.vaccinated*self.S*self.Pro - (1-self.vaccinated)*self.infection*self.S*self.I*self.Pro - self.infection*self.S*self.I*self.Ag + self.recover*self.I + self.resus*self.V
            self.dI = (1-self.vaccinated)*self.infection*self.S*self.I*self.Pro + self.infection*self.S*self.I*self.Ag - self.recover*self.I
            self.dV = self.vaccinated*self.S*self.Pro - self.resus*self.V

            if start == True:
                self.set_epidemic(1)
                # Write longitudinal social network data
                if (51 in self.mode or 52 in self.mode or 53 in self.mode or 54 in self.mode) and self.contact_nwk.update_rule != None:
                    if filename != '':
                        write.WriteNetworkAvgDegree(self.contact_nwk.nwk_graph, filename)
                        write.WriteNetworkAvgDegree_I(self.contact_nwk.nwk_graph, filename)
                        write.WriteNetworkAvgDegree_S(self.contact_nwk.nwk_graph, filename)
                        write.WriteNetworkAssortativity(self.contact_nwk.nwk_graph, filename)


        except ValueError:
            print('Check your parameters if they are probabilities.')

    def set_other_alpha_param(self, alpha_V, alpha_T):
        self.alpha_V = alpha_V
        self.alpha_T = alpha_T

    def set_other_beta_param(self, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2):
        self.infection_SS = beta_SS
        self.infection_II = beta_II
        self.infection_RR = beta_RR
        self.infection_VV = beta_VV
        self.infection_IR = beta_IR
        self.infection_SR = beta_SR
        self.infection_SV = beta_SV
        self.infection_PI = beta_PI
        self.infection_IV = beta_IV
        self.infection_RV = beta_RV



    def get_states(self):
        '''
            Get number of people who are in S, I or V state.
        '''
        self.S = 0
        self.I = 0
        self.U = 0
        self.E = 0
        self.V = 0
        self.R = 0
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                self.V += 1
                continue
            elif self.people[i].suceptible == 1 and self.people[i].removed == 0:
                self.U += 1
                continue
            elif self.people[i].exposed == 1 and self.people[i].removed == 0:
                self.E += 1
                continue
            elif self.people[i].removed == 1:
                self.R += 1
                continue
            self.S += 1
        self.I = self.U + self.E
        return self.S, self.I, self.U, self.E, self.V, self.R

    def write_history(self):
        '''Write compartment history of everyone.'''
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                self.people[i].compartment_history.append('V')
                continue
            elif (self.people[i].suceptible == 0 and self.people[i].vaccinated == 0):
                self.people[i].compartment_history.append('S')
                continue
            elif (self.people[i].suceptible == 1 and self.people[i].exposed == 0):
                self.people[i].compartment_history.append('E')
                continue
            elif (self.people[i].suceptible == 1 and self.people[i].exposed == 1):
                self.people[i].compartment_history.append('I')
                continue
            elif self.people[i].removed == 1:
                self.people[i].compartment_history.append('R')
                continue

    def set_epidemic(self, mode):
        '''
        Set either the environment to be disease-free or not.
        '''
        try:
            if mode > 1 or mode < 0:
                raise ValueError
        except ValueError:
            print('Mode must be either 1 or 0')
            pass
        if mode == 1:
            self.epidemic = 1
            Epidemic.start_epidemic(self)
        else:
            self.epidemic = 0
            Epidemic.kill_epidemic(self)

    def start_epidemic(self, initial_infection=4):
        '''
        Start an epidemic
        '''
        if len(self.people) < initial_infection:
            initial_infection = len(self.people)
        # Pick first 4 people/ random number of people (1-5) infected initially
        for i in range(initial_infection):
            self.people[i].suceptible = 1

    def kill_epidemic(self):
        for i in range(len(self.people)):
            self.people[i].suceptible = 0

    def load_modes(self, modes):
        self.mode.update(modes)

    def set_pro_ag(self):
        '''
        Return the proportion of people who pro or against vaccination.
        '''
        pro = 0
        ag = 0
        for i in range(len(self.people)):
            if self.people[i].opinion == 1:
                pro += 1
            else:
                ag += 1
        self.Pro = pro/(len(self.people))
        self.Ag = ag/(len(self.people))

        # Resume temp variables
        ag = 0
        pro = 0

    def vaccinate(self):
        for i in range(len(self.people)):
            seed = random.randint(0,10000)/10000
            if 4 in self.mode:
                if self.verbose_mode == True:
                    print(self.mode[4].P_Alpha[i])
                if seed < self.mode[4].P_Alpha[i] and self.people[i].vaccinated == 0:
                    if self.verbose_mode == True:
                        print(f'{self.people[i].id} has decided to take vaccine. ')
                    self.people[i].vaccinated = 1
                continue
            if 20 in self.mode:
                theta = self.mode[20].set_perceived_infection(self.I/len(self.people))
                continue
            if 21 in self.mode:
                person = self.people[i]
                seed = random.randint(0,10000)/10000
                if person.opinion == 1 and seed < self.alpha_V:
                    if self.verbose_mode == True:
                        print(f'***, {seed} <= {self.alpha_V}')
                    person.vaccinated = 1
                continue
            if self.people[i].suceptible == 1:
                continue

            if seed < self.vaccinated and self.people[i].vaccinated == 0:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} has decided to take vaccine. ')
                self.people[i].vaccinated = 1

    def removed(self):
        '''
        A person is removed from population.
        '''
        delta_pp = np.ones(len(self.people))
        for i in range(len(self.people)):
            if any(i in self.mode for i in [7, 8]):
                # Fetch all parameters:
                if 7 in self.mode:
                    delta_pp[i] = np.multiply(self.mode[7].delta_age[int(self.people[i].age//10)], delta_pp[i])
                if 8 in self.mode:
                    delta_pp[i] = np.multiply(self.mode[8].delta_gender[self.people[i].gender], delta_pp[i])
                if 11 in self.mode:
                    if self.people[i].vaccinated == 1:
                        delta_pp[i] = np.multiply(self.mode[11].delta_V, delta_pp[i])
                if self.verbose_mode == True:
                    print(f'Delta for {self.people[i].id} is {beta_pp[i]}. ')


        for i in range(len(self.people)):
            if self.people[i].suceptible != 1:
                continue
            seed = random.randint(0,1000)/1000
            if any(i in self.mode for i in [7, 8]):
                if seed < delta_pp[i]:
                    self.people[i].removed = 1

            if seed < self.remove:
                self.people[i].removed = 1

    def infect(self):
        '''
        Mechanism of infection.
        '''

        # Network contact controlled by Epidemic.social_contact()
        if any(i in self.mode for i in [51, 52, 53, 53]):
            if self.verbose_mode == True:
                print('Social contact applies to infection. ')
            self.social_contact()

            for i in range(len(self.people)):
                if self.people[i].overseas != None and 2 in self.mode:
                    self.overseas_infect(i)
            return

        # Creating customised infection parameter for each person.
        beta_pp = np.ones(len(self.people))
        for i in range(len(self.people)):
            if any(i in self.mode for i in [1, 7, 8, 11]):
                # Fetch all parameters:
                if 1 in self.mode:
                    beta_pp[i] = np.multiply(self.mode[1].betas[self.people[i].location], beta_pp[i])
                if 7 in self.mode:
                    beta_pp[i] = np.multiply(self.mode[7].beta_age[int(self.people[i].age//10)], beta_pp[i])
                if 8 in self.mode:
                    beta_pp[i] = np.multiply(self.mode[8].beta_gender[self.people[i].gender], beta_pp[i])
                if 11 in self.mode:
                    if self.people[i].vaccinated == 1:
                        beta_pp[i] = np.multiply(self.mode[11].beta_V, beta_pp[i])

        for i in range(len(self.people)):
            '''
            Infect (or not)
            '''
            if self.people[i].suceptible == 1:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} has already been infected and will not be infected. ')
                continue  # Skip
            if self.people[i].removed == 1 :
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} is removed and will not be infected. ')
                continue  # Skip

            if 11 not in self.mode and self.people[i].vaccinated == 1:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} is vaccinated and will not be infected. ')
                continue

            seed = random.randint(0,1000)/1000
            '''
            Customised infection from modes (excl. network contact)
            '''
            if any(i in self.mode for i in [1, 7, 8]):
                if self.verbose_mode == True:
                    print(f'Beta for {self.people[i].id} is {beta_pp[i]}. ')
                if seed < beta_pp[i]:
                    self.people[i].suceptible = 1
                continue
            if self.people[i].overseas != None and 2 in self.mode:
                self.overseas_infect(i)
                continue
            elif self.people[i].overseas == None and 2 in self.mode:
                # Check if person is isolated back home.
                if self.mode[2].is_isolated_local(i, self.verbose_mode):
                    continue

            '''
            Normal infection event
            '''
            if seed < self.infection:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} is infected. ')
                self.people[i].suceptible = 1

    def social_contact(self):
        '''
        Simulate social contacts.
        '''
        for edge in self.contact_nwk.network:
            # This is edge of People objects.
            # Conditions where disease will not spread (SS, VV, RR)
            if self.verbose_mode == True:
                print('{}/ {}'.format(self.contact_nwk.network.index(edge), len(self.contact_nwk.network)))
            if edge[0].suceptible == 0 and edge[1].suceptible == 0:
                if self.verbose_mode == True:
                    print(f'Both ends are not infected. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            # The following will not apply if mode 11 has been activated, skips this condition.
            if (edge[0].vaccinated == 1 and edge[1].vaccinated == 1) and 11 not in self.mode:
                if self.verbose_mode == True:
                    print(f'Both ends are vaccinated. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            elif edge[0].vaccinated == 1 and 11 not in self.mode:
                if self.verbose_mode == True:
                    print(f'{edge[0].id} are vaccinated. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            elif edge[1].vaccinated == 1 and 11 not in self.mode:
                if self.verbose_mode == True:
                    print(f'{edge[1].id} are vaccinated. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            if edge[0].removed == 1 or edge[1].removed == 1:
                if self.verbose_mode == True:
                    print(f'One of the contacts are removed. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            if edge[0].exposed == 1 or edge[1].exposed == 1:
                if self.verbose_mode == True:
                    print(f'One of the contacts are quarantined. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            if self.verbose_mode == True:
                print(edge[0].id, edge[1].id)
                print('  ', edge[0].suceptible, edge[1].suceptible)

            # Infect (or not)
            seed = random.randint(0,100000)/100000
            if seed < self.infection:
                edge[0].suceptible = 1
                edge[1].suceptible = 1
                if self.verbose_mode == True:
                    print(f'{edge[0].id}-{edge[1].id} pair is infected.')

    def overseas_infect(self, i):
        '''
        People infect from overseas.
        '''

        if self.verbose_mode == True:
            print(f'\t{self.people[i].id} is in overseas. ', end='')

        if self.mode[2].is_isolated_overseas(i):
            if self.verbose_mode == True:
                print('(Isolated)')
            return
        if self.verbose_mode == True:
            print('... ', end='')
        seed = random.randint(0,1000)/1000
        if self.verbose_mode == True:
            print(f'\t{seed}, β: {self.people[i].overseas[list(self.people[i].overseas.keys())[0]]}, {seed < self.people[i].overseas[list(self.people[i].overseas.keys())[0]]}', end='')

        if self.people[i].suceptible == 1:
            if self.verbose_mode == True:
                print('(Infected*)')
        elif seed < self.people[i].overseas[list(self.people[i].overseas.keys())[0]]:
            if self.verbose_mode == True:
                print('(Infected)')
            self.people[i].suceptible = 1
        else: print()

    def infection_clock(self, i):
        if self.people[i].infection_clock > 14:
            self.people[i].exposed = 1

    def infected(self):
        '''
        Once a person was infected for 14 days, their symptoms are exposed.

        If the person is tested, we may put them into E compartment.
        '''
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1 and self.people[i].removed == 0:
                self.people[i].infection_clock += 1
            else:
                self.people[i].infection_clock = 0

            self.infection_clock(i)

    def recovery(self):
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if 11 in self.mode:
                if seed < self.mode[11].gamma_V:
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
            if seed < self.recover:
                self.people[i].suceptible = 0
                self.people[i].exposed = 0

    def immune(self):
        '''
        Assume there is a period of immunity since recovery.
        '''
        if self.immune_time == 0:
            return
        for i in range(len(self.people)):
            recent = self.people[i].compartment_history[-self.immune_time:]
            for j in range(len(recent)-1):
                if len(recent) < 2:
                    continue
                if recent[j] == 'I' and recent[j+1] == 'S':
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
                    continue

    def wear_off(self):
        '''
        Vaccine may wear off.
        '''
        if 10 in self.mode:
            if self.mode[10].type == 1:
                return # Patients will not have their vaccine wear-off.
            elif self.mode[10].type == 2:
                for i in range(len(self.people)):
                    # See people are unlikely to leave V compartment.
                    recent = self.people[i].compartment_history[-366//4:]
                    for j in range(len(recent)-1):
                        if len(recent) < 2:
                            continue
                        if recent[j] == 'S' and recent[j+1] == 'V':
                            # Maintain V state and iterate to next person
                            self.people[i].vaccinated = 1
                            continue
                    # Else
                    seed = random.randint(0,100000)/100000
                    if self.people[i].vaccinated == 1 and seed <= self.resus:
                        self.people[i].vaccinated = 0
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if self.people[i].vaccinated == 1 and seed <= self.resus:
                self.people[i].vaccinated = 0

    def testing(self):
        '''
        COVID-19 testing and people who are in the E compartment will become I.
        '''
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if seed < self.test_rate:
                if self.people[i].suceptible == 1:
                    self.people[i].exposed = 1
                self.people[i].test_history.append(1)
                continue
            self.people[i].test_history.append(0)

    def __iter__(self):
        return self

    def next(self, filename):
        '''
        At each iteration, there will be:
        * Calculate S, I, V and proportion of pro and against vaccine.
        * Each person interacts with another.
        * Write the data files.

        Parameter:
        - filename: File name for csv output.
        '''

        self.get_states()
        self.set_pro_ag()
        self.wear_off()
        self.testing()
        self.infect()
        self.removed()
        self.recovery()
        self.vaccinate()
        self.infected()
        self.immune()
        if 51 in self.mode or 52 in self.mode or 53 in self.mode or 54 in self.mode:
            if self.contact_nwk.update_rule == 'random':
                self.contact_nwk.update_random_nwk()
                if filename != '':
                    write.WriteNetworkAvgDegree(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_I(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_S(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAssortativity(self.contact_nwk.nwk_graph, filename)
            elif self.contact_nwk.update_rule == 'XBS':
                self.contact_nwk.update_xulvi_brunet_sokolov()
                if filename != '':
                    write.WriteNetworkAvgDegree(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_I(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_S(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAssortativity(self.contact_nwk.nwk_graph, filename)
            self.contact_nwk.update_nwk()

        self.get_states()
        self.write_history()
        if filename != '':
            write.WriteStates(self, filename)
