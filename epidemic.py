import random
import numpy as np

from contact import ContactNwk
from vaccine import Vaccine
import person
import write

class Epidemic:

    def __init__(self, vaccinated, infection, recover, resus, remove, people, test_rate, immune_time, vaccine_ls,
                 contact_nwk, verbose_mode, logger, modes=[], filename=None, vaccine_cap_filename=None, start=True):
        '''Initial elements

        Attributes
        ----------

        epidemic - int
            Flag epidemic starts or ends.

        people - People
            Agents for simulation
            :param logger:

        Parameters
        ----------
        vaccine_cap_filename
        '''
        self.epidemic = 0   # Whether an epidemic occured or not.
        self.people = people
        self.contact_nwk = contact_nwk
        self.vaccine_ls = vaccine_ls
        self.vaccine_cap_filename = vaccine_cap_filename
        self.vaccine_stocktake = []
        self.current_vaccine_dose_count = {}
        self.vaccine_dose_quota = {}
        self.vaccine_daily_quota = {}
        self.vaccine_supply_generator = None
        if vaccine_cap_filename != None:
            self.generate_vaccine_supply_cap()
        self.filename = filename
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
            self.logger = logger

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
                self.load_modes(modes)
                self.set_epidemic(1)
                # Write longitudinal social network data
                if (5 in self.mode or 51 in self.mode or 52 in self.mode or 53 in self.mode or 54 in self.mode) and self.contact_nwk.update_rule != None:
                    if self.filename != '':
                        write.WriteNetworkAvgDegree(self.contact_nwk.nwk_graph, filename)
                        write.WriteNetworkAvgDegree_I(self.contact_nwk.nwk_graph, filename)
                        write.WriteNetworkAvgDegree_S(self.contact_nwk.nwk_graph, filename)
                        # write.WriteNodeBetweeness(self.contact_nwk.nwk_graph, filename)
                        # write.WriteNodeBetweeness_I(self.contact_nwk.nwk_graph, filename)
                        # write.WriteNodeBetweeness_S(self.contact_nwk.nwk_graph, filename)
                        write.WriteNetworkAssortativity(self.contact_nwk.nwk_graph, filename)
                if any(m in self.mode for m in [12, 15]):
                    self.generate_vaccine_dose_quota_records(len(self.people))


        except ValueError:
            self.loger.error('Check your parameters if they are probabilities.')

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

    def get_V_states(self):
        '''
        Get number of people who are in V state. Not changing the attributes here unless in
        '''
        V = 0
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                V += 1
        return V

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
            elif self.people[i].suceptible == 0 and self.people[i].vaccinated == 0 and self.people[i].removed == 0:
                self.people[i].compartment_history.append('S')
                continue
            elif self.people[i].suceptible == 1 and self.people[i].exposed == 0:
                self.people[i].compartment_history.append('E')
                continue
            elif self.people[i].suceptible == 1 and self.people[i].exposed == 1:
                self.people[i].compartment_history.append('I')
                continue
            elif self.people[i].removed == 1:
                self.people[i].compartment_history.append('R')
                continue

    def generate_vaccine_dose_count_record(self):
        '''
        At start of day, either create the current_vaccine_dose_count or restart the counts.
        '''
        self.logger.debug('Restarting (empty) vaccine does count dictionary. ')
        self.current_vaccine_dose_count = {vaccine.brand + ":" + str(vaccine.dose): 0 for vaccine in self.vaccine_ls}

    def vaccine_dose_taken(self, vaccine_taken):
        '''

        Parameters
        ----------
        vaccine_taken: Vaccine
            The vaccine taken by the person
        '''
        self.current_vaccine_dose_count[vaccine_taken.brand + ":" + str(vaccine_taken.dose)] += 1


    def generate_vaccine_stock_record(self):
        '''
        Add a new dictionary for the vaccine_stocktake.
        '''
        self.logger.debug('Appending (empty) vaccine stocktake list. ')
        self.vaccine_stocktake.append({vaccine.brand: 0 for vaccine in self.vaccine_ls})

    def vaccine_stock_taken(self, vaccine_taken):
        '''
        Update if a person take a vaccine on a particular day, by brand.

        Parameters
        ----------
        vaccine_taken: Vaccine
            The vaccine taken by the person
        '''
        self.vaccine_stocktake[-1][vaccine_taken.brand] += 1

    def generate_vaccine_dose_quota_records(self, N):
        '''
        Generate Epidemic.vaccine_dose_quota_records().

        Parameters
        ----------
        N: int
            Population
        vaccine_ls: list
            List of available vaccines.
        '''
        self.vaccine_dose_quota = {vaccine.brand+":"+str(vaccine.dose): self.update_multi_dose_quota(vaccine) * N for vaccine in self.vaccine_ls}

    def update_multi_dose_quota(self, vaccine):
        '''
        If there are any new doses detected in the line, then shall multiply the quota from previous doses.

        Parameters
        ----------
        vaccine: Vaccine
            Vaccine that needs to have its quote updated.

        Examples
        --------
        update_multi_dose_quota(self, vaccine_3) => quota[vaccine_3] * vaccine_2.alpha * vaccine_1.alpha
        '''
        if vaccine.dose == 1:
            return vaccine.alpha_V
        for other in self.vaccine_ls:
            if other.brand == vaccine.brand and other.dose == vaccine.dose - 1:
                return vaccine.alpha_V * self.update_multi_dose_quota(other)

    def vaccine_dose_record(self, vaccine_taken):
        '''
        Remove quota when a vaccine dose is taken

        Parameters
        ----------
        vaccine_taken: Vaccine
            The vaccine taken by the person
        '''
        self.vaccine_dose_quota[vaccine_taken.brand+":"+str(vaccine_taken.dose)] -= 1

    def vaccine_dose_flag(self, vaccine_taken):
        '''
        Determine if can take vaccine booster dose before quota (Defined by dose adoption rate).

        Parameters
        ----------
        vaccine_taken: Vaccine
            The vaccine taken by the person

        Return
        ------
        True (Can take) or false (Over quota)
        '''
        if self.vaccine_dose_quota[vaccine_taken.brand+":"+str(vaccine_taken.dose)] > 0:
            return True
        else:
            return False

    def generate_vaccine_supply_cap(self):
        '''
        Create an iterator from supply cap specification.
        '''

        import pandas as pd # If other places imports pandas then delete this.
        df_vaccine_supply = pd.read_csv(self.vaccine_cap_filename)

        self.vaccine_supply_generator = df_vaccine_supply.iterrows()

    def get_vaccine_supply_cap(self):
        '''
        Check if person can take vaccine due to supply.

        Returns
        -------
        The vaccine cap as specified or 0 if the file has insufficient rows.
        '''
        try:
            self.vaccine_daily_quota = next(self.vaccine_supply_generator)[1].to_dict()
            self.logger.debug(f'Current vaccine supply: {self.vaccine_daily_quota}')
        except StopIteration:
            self.logger.warning('No vaccine supply details, will set to 0. ')
            self.vaccine_daily_quota = {vaccine.brand: 0 for vaccine in self.vaccine_ls}
            self.logger.debug(f'Current vaccine supply: {self.vaccine_daily_quota}')

    def vaccine_supply_record(self, vaccine_taken):
        '''
        Remove quota when a vaccine dose is taken

        Parameters
        ----------
        vaccine_taken: Vaccine
            The vaccine taken by the person
        '''
        self.vaccine_daily_quota[vaccine_taken.brand] -= 1

    def set_epidemic(self, mode):
        '''
        Set either the environment to be disease-free or not.
        '''
        try:
            if mode > 1 or mode < 0:
                raise ValueError
        except ValueError:
            self.logger.error('Mode must be either 1 or 0. Now killing the simulation and the pandemic. ')
        if mode == 1:
            self.epidemic = 1
            if 501 in self.mode:
                Epidemic.start_epidemic(self, self.mode[501].init_infection)
            else:
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
        # Pick first 4 people/ random number of people (defined by mode 501) infected initially
        if 505 in self.mode:
            if 501 in self.mode:
                self.mode[505].set_infection(self.mode[501].init_infection)
            else:
                self.mode[505].set_infection()
            return
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
        self.logger.debug('Starting Epidemic.vaccine().')
        if self.alpha_V == 0 and any(m in self.mode for m in [4, 10, 15, 20, 21, 22, 23, 24]):
            self.logger.warning('One of more modes cannot take affect to change vaccination due to α = 0. ')

        for person in self.people:
            next_vaccine = None

            # Already vaccinated
            if person.vaccinated == 1:
                self.logger.debug(f'Person {person.id} has already been vaccinated. ')
                continue

            # Mode 12
            pass

            # Opinions
            if person.personality == 2:
                self.logger.debug(f'Person does not want to take vaccine')
                continue
            elif person.opinion == 0:
                continue

            # Find alpha for each person
            idx = self.people.index([p for p in self.people if p.id == person.id][0])
            self.logger.debug(f'Person {person.id} is {idx}th person in the self.people')
            if self.alpha_V != None:
                vaccinated_theshold = self.alpha_V
            else:
                vaccinated_theshold = self.vaccinated

            # Mode 15, extract current vaccine
            if 15 in self.mode:
                self.logger.debug(f'Mode 15 activated for {person.id}.')
                has_vaccine_doses = self.mode[15].check_multi_dose_vaccine(self.vaccine_ls)
                if has_vaccine_doses:
                    last_vaccine = self.mode[15].check_recent_vaccine(idx, self.vaccine_ls)
                    next_vaccine = self.mode[15].check_next_vaccine(idx, self.vaccine_ls, last_vaccine)
                    if next_vaccine == None:
                        continue
                    self.logger.debug(
                        f'{person.id} may take vaccine {next_vaccine.brand}:{next_vaccine.dose}. (α = {next_vaccine.alpha_V}) ')
                    # Check if in cap
                    if len(self.vaccine_daily_quota) > 0 and self.vaccine_daily_quota[next_vaccine.brand] == 0:
                        self.logger.debug(f'{next_vaccine.brand} is out of stock. ')
                        continue
                    if not self.vaccine_dose_flag(next_vaccine):
                        self.logger.debug(
                            f'Person {person.id} will not take vaccine {next_vaccine.brand} dose {next_vaccine.dose} due to cap. ')
                        continue
                    vaccinated_theshold *= next_vaccine.alpha_V

            # Mode 20
            if 20 in self.mode:
                self.logger.debug(f'Mode 20 activated to broadcast message from {person.id}.')
                vaccinated_theshold *= self.mode[20].FDProb(idx)

            # Mode 10
            if 10 in self.mode:
                self.logger.debug(f'Mode 10 activated for {person.id}.')
            # Mode 4
            if 4 in self.mode:
                self.logger.debug(f'Mode 4 activated for {person.id}.')
                self.logger.debug(f'\tPerson {person.id} has adoption probability of α = {self.mode[4].P_Alpha[idx]}. ')
                vaccinated_theshold *= self.mode[4].P_Alpha[idx]
            self.logger.debug(f'Person {person.id} has vaccination rate {vaccinated_theshold}. ')

            # Vaccinate
            seed = random.randint(0, 10000) / 10000
            if seed < vaccinated_theshold:
                self.logger.debug(f'{person.id} has decided to take vaccine. ')
                person.vaccinated = 1
                person.vaccine_history.append(1)

                # Mode 20
                if 20 in self.mode:
                    self.mode[20].event_vaccinated(person=person)
                if next_vaccine is not None:
                    if len(self.vaccine_stocktake) > 0 and len(self.current_vaccine_dose_count) > 0:
                        self.vaccine_stock_taken(next_vaccine)
                        self.vaccine_dose_taken(next_vaccine)
                        self.vaccine_dose_record(next_vaccine)
                    if len(self.vaccine_daily_quota) > 0:
                        self.vaccine_supply_record(next_vaccine)
                    self.logger.debug(
                        f'Person {person.id} has taken the vaccine {next_vaccine.brand} dose {next_vaccine.dose}. ')
                if 15 in self.mode:
                    self.mode[15].write_vaccine_history(idx, next_vaccine)
            else:
                self.logger.debug(f'{person.id} has decided not to take vaccine (α = {vaccinated_theshold}). ')
                person.vaccine_history.append(0)


    def vaccine_clock(self, i):
        '''
        Trace the person's vaccination history and advise

        Returns
        -------
        True if vaccine was taken within 14 days, else false.
        '''
        self.logger.debug(f'Starting method Epidemic.vaccine_clock() for person {i}...')
        for t in range(len(self.people[i].vaccine_history)-1, max(len(self.people[i].vaccine_history)-15, 0), -1):
            if self.people[i].vaccine_history[t] != 0:
                return True
        return False


    def removed(self):
        '''
        A person is removed from population.
        '''
        delta_pp = np.ones(len(self.people))
        for i in range(len(self.people)):
            if any(m in self.mode for m in [7, 8]):
                # Fetch all parameters:
                if 7 in self.mode:
                    delta_pp[i] = np.multiply(self.mode[7].delta_age[int(self.people[i].age//10)], delta_pp[i])
                if 8 in self.mode:
                    delta_pp[i] = np.multiply(self.mode[8].delta_gender[self.people[i].gender], delta_pp[i])
                if 11 in self.mode:
                    if self.people[i].vaccinated == 1:
                        delta_pp[i] = np.multiply(self.mode[11].delta_V, delta_pp[i])
                self.logger.debug(f'Delta for {self.people[i].id} is {delta_pp[i]}. ')


        for i in range(len(self.people)):
            if self.people[i].suceptible != 1:
                continue
            seed = random.randint(0,10000)/10000
            if any(m in self.mode for m in [7, 8]):
                if seed < delta_pp[i]:
                    self.people[i].removed = 1
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
                    self.people[i].vaccinated = 0

            if seed < self.remove:
                self.people[i].removed = 1
                self.people[i].suceptible = 0
                self.people[i].exposed = 0
                self.people[i].vaccinated = 0


    def infect(self):
        '''
        Mechanism of infection.
        '''

        self.logger.debug('Starting method Epidemic.infect()...')

        # Intimacy game
        # if 20 in self.mode:
        #     self.logger.debug('Applying intimacy game in infection. ')
        #     for i in range(len(self.people)):
        #         threshold = 1 - (1 - self.infection) ** (self.mode[20].get_infected_neighbours_number(i))
        #         seed = random.randint(0,1000)/1000
        #
        #         if seed < threshold:
        #             self.people[i].suceptible = 1
        #             continue

        # Network contact controlled by Epidemic.social_contact()
        if any(m in self.mode for m in [51, 52, 53, 53]):
            self.logger.debug('Social contact applies to infection. ')
            self.social_contact()

            for i in range(len(self.people)):
                if self.people[i].overseas != None and 2 in self.mode:
                    self.overseas_infect(i)
                elif self.people[i].overseas == None and 2 in self.mode:
                    # Check if person is isolated back home.
                    if self.mode[2].is_isolated_local(i):
                        continue
            return

        # Creating customised infection parameter for each person.
        beta_pp = np.ones(len(self.people))
        for i in range(len(self.people)):
            if any(m in self.mode for m in [1, 7, 8, 11]):
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
                self.logger.debug(f'{self.people[i].id} has already been infected and will not be infected. ')
                continue  # Skip
            if self.people[i].removed == 1 :
                self.logger.debug(f'{self.people[i].id} is removed and will not be infected. ')
                continue  # Skip
            if 11 not in self.mode and self.people[i].vaccinated == 1 and not self.vaccine_clock(i):
                self.logger.debug(f'{self.people[i].id} is vaccinated and will not be infected. ')
                continue  # Skip

            seed = random.randint(0,1000)/1000
            '''
            Customised infection from modes (excl. network contact)
            '''
            if any(m in self.mode for m in [1, 7, 8]):
                self.logger.debug(f'Beta for {self.people[i].id} is {beta_pp[i]}. ')
                if seed < beta_pp[i]:
                    self.people[i].suceptible = 1
                continue
            if self.people[i].overseas != None and 2 in self.mode:
                self.overseas_infect(i)
                continue
            elif self.people[i].overseas == None and 2 in self.mode:
                # Check if person is isolated back home.
                if self.mode[2].is_isolated_local(i):
                    continue

            '''
            Normal infection event
            '''
            if seed < self.infection:
                self.logger.debug(f'{self.people[i].id} is infected. ')
                self.people[i].suceptible = 1
                if 20 in self.mode:
                    self.mode[20].event_infected(i=i)

    def social_contact(self):
        '''
        Simulate social contacts.
        '''

        self.logger.debug('Starting method Epidemic.social_contact()...')
        for edge in self.contact_nwk.network:
            # This is edge of People objects.
            # Conditions where disease will not spread (SS, VV, RR)
            self.logger.debug(f'Edge {self.contact_nwk.network.index(edge)}/ {len(self.contact_nwk.network)} ({round(self.contact_nwk.network.index(edge)/ len(self.contact_nwk.network), 4)})')
            if edge[0].suceptible == 0 and edge[1].suceptible == 0:
                self.logger.debug(f'Both ends are not infected. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            # The following will not apply if mode 11 has been activated, skips this condition.
            if (edge[0].vaccinated == 1 and edge[1].vaccinated == 1) and 11 not in self.mode and not self.vaccine_clock(self.people.index(edge[1])):
                self.logger.debug(f'Both ends are vaccinated. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            elif edge[0].vaccinated == 1 and 11 not in self.mode and not self.vaccine_clock(self.people.index(edge[1])):
                self.logger.debug(f'{edge[0].id} are vaccinated. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            elif edge[1].vaccinated == 1 and 11 not in self.mode and not self.vaccine_clock(self.people.index(edge[1])):
                self.logger.debug(f'{edge[1].id} are vaccinated. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            if edge[0].removed == 1 or edge[1].removed == 1:
                self.logger.debug(f'One of the contacts are removed. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            if edge[0].exposed == 1 or edge[1].exposed == 1:
                self.logger.debug(f'One of the contacts are hospitalised. Skip ({edge[0].id}, {edge[1].id}). ')
                continue
            self.logger.debug('Checked:')
            self.logger.debug(f'   {edge[0].id}\t{edge[1].id}')
            self.logger.debug(f'S: {edge[0].suceptible}\t{edge[1].suceptible}')

            # Infect (or not)
            seed = random.randint(0,100000)/100000
            if seed < self.infection:
                edge[0].suceptible = 1
                edge[1].suceptible = 1
                self.logger.debug(f'{edge[0].id}-{edge[1].id} pair is transmitted. ({seed} < {self.infection})')
            else:
                self.logger.debug(f'{edge[0].id}-{edge[1].id} pair is not transmitted. ({seed} >= {self.infection})')

    def overseas_infect(self, i):
        '''
        People infect from overseas.
        '''

        self.logger.debug(f'Starting method Epidemic.overseas_infect() for person {i}...')
        if self.mode[2].is_isolated_overseas(i,self.verbose_mode):
            self.logger.debug(f'\t{self.people[i].id} is in overseas. (Isolated)')
            return
        self.logger.debug(f'\t{self.people[i].id} is in overseas... ')
        seed = random.randint(0,1000)/1000

        if self.people[i].suceptible == 1:
            self.logger.debug(f'\t{seed}, β: {self.people[i].overseas[list(self.people[i].overseas.keys())[0]]}, {seed < self.people[i].overseas[list(self.people[i].overseas.keys())[0]]} (Infected*)')
        elif 11 not in self.mode and self.people[i].vaccinated == 1 and not self.vaccine_clock(i):
            self.logger.debug(f'\t{self.people[i].id} is protected by vaccine while overseas. ')
        elif seed < self.people[i].overseas[list(self.people[i].overseas.keys())[0]]:
            self.logger.debug(f'\t{seed}, β: {self.people[i].overseas[list(self.people[i].overseas.keys())[0]]}, {seed < self.people[i].overseas[list(self.people[i].overseas.keys())[0]]} (Infected)')
            self.people[i].suceptible = 1
        else: self.logger.debug(f'{self.people[i].id} is not infected from overseas. ')

    def infection_clock(self, i):
        self.logger.debug(f'Starting method Epidemic.infection_clock() for person {i}...')
        if self.people[i].infection_clock > 14:
            self.logger.debug(f'Person {self.people[i].id} has been infected for {self.people[i].infection_clock} days and will be hospitalised. ')
            self.people[i].exposed = 1

    def infected(self):
        '''
        Once a person was infected for 14 days, their symptoms are exposed.

        If the person is tested, we may put them into E compartment.
        '''

        self.logger.debug('Starting method Epidemic.infected()...')
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1 and self.people[i].removed == 0:
                self.people[i].infection_clock += 1
                self.logger.debug(f'{self.people[i].id} has been infected for {self.people[i].infection_clock} days. ')
            else:
                self.people[i].infection_clock = 0
                self.logger.debug(f'{self.people[i].id} infection history is reset. ')

            self.infection_clock(i)

    def recovery(self):
        self.logger.debug('Starting method Epidemic.recovery()...')
        for i in range(len(self.people)):
            if self.people[i].removed != 0:
                continue
            seed = random.randint(0,100000)/100000
            if 11 in self.mode:
                if seed < self.mode[11].gamma_V:
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
            if seed < self.recover:
                self.people[i].suceptible = 0
                self.people[i].exposed = 0
                self.logger.debug(f'{self.people[i].id} recovered. ({seed} < {self.recover})')

    def immune(self):
        '''
        Assume there is a period of immunity since recovery.
        '''

        self.logger.debug('Starting method Epidemic.immune()...')
        if self.immune_time == 0:
            return
        for i in range(len(self.people)):
            if 43 in self.mode:
                try:
                    recent = self.people[i].compartment_history[-self.mode[43].get_immune_time(i):] if self.mode[43].get_immune_time(i) > 0 else []
                except TypeError:
                    # This is when Mode43().get_immune_time() refers to default instructions.
                    recent = self.people[i].compartment_history[-self.immune_time:] if self.immune_time > 0 else []
            else:
                recent = self.people[i].compartment_history[-self.immune_time:] if self.immune_time > 0 else []
            for t in range(len(recent)-1):
                if len(recent) < 2:
                    break
                if recent[t] == 'I' and recent[t+1] == 'S':
                    # When someone was recovered during this period, then they will not be infected again (during this period)
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
                    break

    def wear_off(self):
        '''
        Vaccine may wear off.
        '''
        self.logger.debug('Starting method Epidemic.wear_off()...')
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
                    if self.people[i].vaccinated == 1 and seed < self.resus:
                        self.people[i].vaccinated = 0
                        self.people[i].vaccine = None
        if 15 in self.mode:
            self.logger.debug('Applying advanced vaccine options in vaccine wear off. ')
            # Find recent vaccine taken
            for i in range(len(self.people)):
                vaccine_used = self.mode[15].check_recent_vaccine(i, self.vaccine_ls)
                if vaccine_used != None:
                    self.logger.debug(f"Recent vaccine for {self.people[i].id}: {vaccine_used.brand}:{vaccine_used.dose}, Efficacy: {vaccine_used.efficacy}, Wear-off rate: {vaccine_used.phi_V}")
                else:
                    self.logger.debug(f"No vaccine taken from {self.people[i].id}")
                seed = random.randint(0, 100000) / 100000
                if self.people[i].vaccinated == 1 and seed < vaccine_used.phi_V:
                    self.logger.debug(f"Wear off for {self.people[i].id}: {seed}, {vaccine_used.phi_V}")
                    self.people[i].vaccinated = 0
                    self.people[i].vaccine = None
            return
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if self.people[i].vaccinated == 1 and seed < self.resus:
                self.people[i].vaccinated = 0
                self.people[i].vaccine = None
                self.logger.debug(f"Wear off for {self.people[i].id}: {seed}, {self.resus}")

    def testing(self):
        '''
        COVID-19 testing and people who are in the E compartment will become I.
        '''

        self.logger.debug('Starting method Epidemic.testing()...')
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if seed < self.test_rate:
                if self.people[i].suceptible == 1:
                    self.people[i].exposed = 1
                    self.logger.debug(f'{self.people[i].id} has been tested COVID and hospitalised. ({seed} < {self.test_rate})')
                self.people[i].test_history.append(1)
                continue
            self.logger.debug(f'{self.people[i].id} did not went to COVID testing. ({seed} >= {self.test_rate})')
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
                self.logger.debug('Entering contact network updates...(Ind)')
                self.contact_nwk.update_random_nwk()
                if filename != '':
                    write.WriteNetworkAvgDegree(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_I(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_S(self.contact_nwk.nwk_graph, filename)
                    # write.WriteNodeBetweeness(self.contact_nwk.nwk_graph, filename)
                    # write.WriteNodeBetweeness_I(self.contact_nwk.nwk_graph, filename)
                    # write.WriteNodeBetweeness_S(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAssortativity(self.contact_nwk.nwk_graph, filename)
            elif self.contact_nwk.update_rule == 'XBS':
                self.logger.debug('Entering contact network updates...(XBS)')
                self.contact_nwk.update_xulvi_brunet_sokolov()
                if filename != '':
                    write.WriteNetworkAvgDegree(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_I(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAvgDegree_S(self.contact_nwk.nwk_graph, filename)
                    # write.WriteNodeBetweeness(self.contact_nwk.nwk_graph, filename)
                    # write.WriteNodeBetweeness_I(self.contact_nwk.nwk_graph, filename)
                    # write.WriteNodeBetweeness_S(self.contact_nwk.nwk_graph, filename)
                    write.WriteNetworkAssortativity(self.contact_nwk.nwk_graph, filename)
            self.contact_nwk.update_nwk()

        self.get_states()
        self.write_history()
        if filename != '':
            write.WriteStates(self, filename)
