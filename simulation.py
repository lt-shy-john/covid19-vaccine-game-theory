import numpy as np

from person import Person
from epidemic import Epidemic
from contact import ContactNwk
import customLogger
import write

import random
import os
import networkx as nx
import logging


class Simulation:
    def __init__(self, N, T, people, contact_nwk, info_nwk, alpha, beta, gamma, phi, delta, filename, alpha_V, alpha_T,
                 beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2,
                 beta_II2, beta_RI2, beta_VI2, tau, immune_time, vaccine_ls, verbose_mode, verbose_level, root,
                 groups_of=3):
        self.N = N
        self.groups_of = groups_of
        self.people = people   # List of people objects
        self.vaccine_ls = vaccine_ls
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
        self.verbose_level = verbose_level
        self.logger = root
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
        self.logger.debug(f'Modes loading to Epidemic class: {self.modes}. ')
        self.epidemic = Epidemic(self.alpha, self.beta, self.gamma, self.phi, self.delta, self.people, self.test_rate,
                            self.immune_time, self.vaccine_ls, self.contact_nwk, self.verbose_mode, self.logger,
                            self.modes, self.filename)
        self.epidemic.set_other_alpha_param(self.alpha_V, self.alpha_T)
        self.epidemic.set_other_beta_param(self.beta_SS, self.beta_II, self.beta_RR, self.beta_VV, self.beta_IR, self.beta_SR, self.beta_SV, self.beta_PI, self.beta_IV, self.beta_RV, self.beta_SI2, self.beta_II2, self.beta_RI2, self.beta_VI2)
        self.logger.debug(f'Modes loaded to Epidemic class: {self.epidemic.mode}. ')
        self.logger.info('beta = {}, alpha = {}, gamma = {}, phi = {}, lambda = {}'.format(self.epidemic.infection, self.epidemic.vaccinated, self.epidemic.recover, self.epidemic.resus, self.epidemic.test_rate))
        self.logger.info('=========== t = 0 ============\n')
        self.logger.info('N = {}'.format(len(self.people)))
        self.logger.info('S = {}, I = {}, V = {}, R = {}'.format(self.epidemic.S, self.epidemic.I, self.epidemic.V, self.epidemic.R))
        self.epidemic.get_states()

        # Contact network adj matrix
        if any(i in self.modes for i in [5, 51, 52, 53, 54]):
            pass # Commented out since it produces large files
            # if self.filename != '':
            #     path = os.path.abspath(os.getcwd()) + "\\" + self.filename + '-contact_nwk'
            #     if self.verbose_mode:
            #         print('Creating a new folder for contact network adjacency matrix at ' + path + '.')
            #     os.mkdir(path)

        # Intimacy game
        if 20 in self.modes:
            self.logger.debug('Calculating theta for intimacy game... ')
            self.modes[20].set_perceived_infection(self.beta, self.verbose_mode)

        if self.filename != '':
            write.WriteStates(self.epidemic, self.filename)
        for t in range(self.T):
            self.logger.info('=========== t = {} ============\n'.format(t+1))
            self.logger.info('N = {}'.format(len(self.people)))
            self.logger.info('S = {}, I = {}, V = {}, R = {}'.format(self.epidemic.S, self.epidemic.I, self.epidemic.V, self.epidemic.R))
            # Overseas travel
            if 2 in self.modes:
                self.logger.debug('!!! Overseas travel alert !!!')
                self.modes[2].returnOverseas()
                self.modes[2].make_decision()

            # Intimacy game
            if 20 in self.modes:
                self.logger.debug('Calculating payoffs (intimacy game)... ')
                self.modes[20].IntimacyGame(self.beta, self.verbose_mode)

            # Contact network update
            if any(i in self.modes for i in [5, 51, 52, 53, 54]):
                pass # Have to comment out adj matrix functionality as it produces a large file.
                # if self.filename != '':
                #     path = os.path.abspath(os.getcwd()) + "\\" + self.filename + '-contact_nwk'
                #     if self.verbose_mode:
                #         print('Adding a new adjacency matrix into ' + path + '.')
                #     if os.path.exists(path):
                #         A = nx.convert_matrix.to_numpy_array(self.contact_nwk.nwk_graph)
                #         np.savetxt(path + "\\" + self.filename + '-contact_nwk' + "adj_matrix_" + str(t).zfill(self.T%10) + '.txt', A, fmt="%d")


            # Info network update
            if any(i in self.modes for i in [21, 22, 23, 24]):
                if any(i in self.modes for i in [22, 23]):
                    self.info_nwk.inflexible_prework()
                self.logger.debug('Opinion (before)')
                for group_no, group in self.info_nwk.roster.items():
                    self.logger.debug(f'{group_no}: {[x.opinion for x in group]}')
                self.info_nwk.update()
                if any(i in self.modes for i in [22, 23]):
                    self.info_nwk.inflexible()
                if 24 in self.modes:
                    self.info_nwk.balance(self.verbose_mode)
                self.logger.debug('Opinion (after)')
                for group_no, group in self.info_nwk.roster.items():
                    self.logger.debug(f'{group_no}: {[x.opinion for x in group]}')
                if any(i in self.modes for i in [22, 23, 24]) and self.filename != '':
                    write.WriteOpinionPersonality(self, self.filename)
                elif self.filename != '':
                    write.WriteOpinion(self, self.filename)
                # Permutate members into groups
                self.info_nwk.update_group()
            # Epidemic network update
            self.epidemic.next(self.filename)

            if 2 in self.modes:
                self.modes[2].writeTravelHistory()

        self.logger.info('\n=========== Result ============\n')
        self.logger.info('There are {} people infected.'.format(self.epidemic.I))
        self.logger.info('There are {} people vaccinated.'.format(self.epidemic.V))
        print()

        # Return any data
        if self.filename != '':
            self.logger.info('Data stored in \'{}.csv\''.format(self.filename))
            write.WriteCompartmentHistory(self, self.filename)
            self.logger.info('Compartment history exported in \'{}-compartment.csv\''.format(self.filename))
            write.WriteTestingHistory(self, self.filename)
            self.logger.info('COVID-19 testing records exported in \'{}-testing.csv\''.format(self.filename))
            if 2 in self.modes:
                write.writeTravelHistory(self, self.filename)
                self.logger.info('Travel history exported in \'{}-travel.csv\''.format(self.filename))
            if self.alpha > 0 or 15 in self.modes:
                write.writeVaccinePassport(self, self.filename)
                self.logger.info('Vaccine history exported in \'{}-vaccination.csv\''.format(self.filename))
            if any(i in self.modes for i in [22, 23, 24]):
                self.logger.info('Population personality and information network details exported in \'{}-opinion.csv\''.format(self.filename))
            elif 21 in self.modes:
                self.logger.info('Information network details exported in \'{}-opinion.csv\''.format(self.filename))
            if any(i in self.modes for i in [51, 52, 53, 54]) and self.contact_nwk.update_rule != None:
                self.logger.info('Average degree history exported in \'{}-nwk-deg.csv\', \'{}-nwk-deg_I.csv\' and \'{}-nwk-deg_S.csv\''.format(self.filename,self.filename,self.filename))
                self.logger.info('Assortativity history exported in \'{}-assort-deg.csv\''.format(self.filename))
            write.WriteSummary(self, self.filename)
            self.logger.info('Summary exported in \'{}-summary.txt\'\n'.format(self.filename))

