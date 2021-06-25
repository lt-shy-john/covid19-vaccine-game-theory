from person import Person
from epidemic import Epidemic
from contact import ContactNwk
import write

import random


class Simulation:
    def __init__(self, N, T, people, contact_nwk, info_nwk, alpha, beta, gamma, phi, delta, filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2, tau, immune_time, verbose_mode, groups_of=3):
        self.N = N
        self.groups_of = groups_of
        self.people = people   # List of people objects
        self.contact_nwk = contact_nwk
        self.info_nwk = info_nwk
        self.groups = None
        self.T = T

        # Adoption rate
        self.alpha = alpha
        self.alpha_V = alpha_V
        self.alpha_T = alpha_T

        # Infection rate
        self.beta = beta
        self.beta_SS = beta_SS
        self.beta_II = beta_II
        self.beta_RR = beta_RR
        self.beta_VV = beta_VV
        self.beta_IR = beta_IR
        self.beta_SR = beta_SR
        self.beta_SV = beta_SV
        self.beta_PI = beta_PI
        self.beta_IV = beta_IV
        self.beta_RV = beta_RV
        self.beta_SI2 = beta_SI2
        self.beta_II2 = beta_II2
        self.beta_RI2 = beta_RI2
        self.beta_VI2 = beta_VI2

        # Recovery rate
        self.gamma = gamma
        self.immune_time = immune_time

        # Wear off rate
        self.phi = phi

        # Testing rate
        self.test_rate = tau

        # Removal rate
        self.delta = delta

        # Auxiliary parameters
        self.verbose_mode = verbose_mode
        self.filename = filename
        self.modes = {}

    def load_modes(self,modes):
        '''Load mode objects into epidemic class, as defined in the main code.

        parameters
        ----------

        modes - dict:
            Keys are integer mode code with the corresponding mode objects
        '''
        self.modes = modes

    def __call__(self, modes=None, start=True):
        FILENAME_STATES = ''
        epidemic = Epidemic(self.alpha, self.beta, self.gamma, self.phi, self.delta, self.people, self.test_rate, self.immune_time, self.contact_nwk, self.verbose_mode, self.modes, self.filename, start)
        epidemic.set_other_alpha_param(self.alpha_V, self.alpha_T)
        epidemic.set_other_beta_param(self.beta_SS, self.beta_II, self.beta_RR, self.beta_VV, self.beta_IR, self.beta_SR, self.beta_SV, self.beta_PI, self.beta_IV, self.beta_RV, self.beta_SI2, self.beta_II2, self.beta_RI2, self.beta_VI2)
        print('After:',epidemic.mode)
        print('beta = {}, alpha = {}, gamma = {}, phi = {}, lambda = {}'.format(epidemic.infection, epidemic.vaccinated, epidemic.recover, epidemic.resus, epidemic.test_rate))
        print('=========== t = 0 ============\n')
        print('N = {}'.format(len(self.people)))
        print('S = {}, I = {}, V = {}, R = {}'.format(epidemic.S, epidemic.I, epidemic.V, epidemic.R))
        epidemic.get_states()

        # Intimacy game
        if 20 in self.modes:
            if self.verbose_mode:
                print('Calculating theta for intimacy game... ')
            self.modes[20].set_perceived_infection(self.beta, self.verbose_mode)

        if self.filename != '':
            write.WriteStates(epidemic, self.filename)
        for t in range(self.T):
            print('=========== t = {} ============\n'.format(t+1))
            print('N = {}'.format(len(self.people)))
            print('S = {}, I = {}, V = {}, R = {}'.format(epidemic.S, epidemic.I, epidemic.V, epidemic.R))
            # Overseas travel
            if 2 in self.modes:
                if self.verbose_mode:
                    print('!!! Overseas travel alert !!!')
                self.modes[2].returnOverseas(self.verbose_mode)
                self.modes[2].make_decision(self.verbose_mode)

            # Intimacy game
            if 20 in self.modes:
                if self.verbose_mode:
                    print('Calculating payoffs (intimacy game)... ')
                self.modes[20].IntimacyGame(self.beta, self.verbose_mode)

            # Info network update
            if 21 in self.modes:
                if any(i in self.modes for i in [22, 23]):
                    self.info_nwk.inflexible_prework()
                if self.verbose_mode == True:
                    print('Opinion (before)')
                    for group_no, group in self.info_nwk.roster.items():
                        print(f'{group_no}:', [x.opinion for x in group])
                self.info_nwk.update(self.verbose_mode)
                if any(i in self.modes for i in [22, 23]):
                    self.info_nwk.inflexible()
                if 24 in self.modes:
                    self.info_nwk.balance(self.verbose_mode)
                if self.verbose_mode == True:
                    print('Opinion (after)')
                    for group_no, group in self.info_nwk.roster.items():
                        print(f'{group_no}:', [x.opinion for x in group])
                if any(i in self.modes for i in [22, 23, 24]) and self.filename != '':
                    write.WriteOpinionPersonality(self, self.filename)
                elif self.filename != '':
                    write.WriteOpinion(self, self.filename)
                # Permutate members into groups
                self.info_nwk.update_group(self.verbose_mode)
            # Epidemic network update
            epidemic.next(self.filename)

            if 2 in self.modes:
                self.modes[2].writeTravelHistory(self.verbose_mode)

        print('\n=========== Result ============\n')
        print('There are {} people infected.'.format(epidemic.I))
        print('There are {} people vaccinated.'.format(epidemic.V))
        print()
        if self.filename != '':
            print('Data stored in \'{}.csv\''.format(self.filename))
            write.WriteCompartmentHistory(self, self.filename)
            print('Compartment history exported in \'{}-compartment.csv\''.format(self.filename))
            write.WriteTestingHistory(self, self.filename)
            print('COVID-19 testing records exported in \'{}-testing.csv\''.format(self.filename))
            if 2 in self.modes:
                write.writeTravelHistory(self, self.filename)
                print('Travel history exported in \'{}-travel.csv\''.format(self.filename))
            if any(i in self.modes for i in [22, 23, 24]):
                print('Population personality and information network details exported in \'{}-opinion.csv\''.format(self.filename))
            elif 21 in self.modes:
                print('Information network details exported in \'{}-opinion.csv\''.format(self.filename))
            if any(i in self.modes for i in [51, 52, 53, 54]) and self.contact_nwk.update_rule != None:
                print('Average degree history exported in \'{}-nwk-deg.csv\', \'{}-nwk-deg_I.csv\' and \'{}-nwk-deg_S.csv\''.format(self.filename,self.filename,self.filename))
                print('Assortativity history exported in \'{}-assort-deg.csv\''.format(self.filename))
            write.WriteSummary(self, self.filename)
            print('Summary exported in \'{}-summary.txt\''.format(self.filename))
            print()

        # Return any data
