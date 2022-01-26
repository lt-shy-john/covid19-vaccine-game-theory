from unittest import TestCase

import subprocess
from pathlib import Path

import csv
import pandas as pd

class IntegrationTests(TestCase):
    def setUp(self) -> None:
        self.path = Path(__file__).parents[2]

    def test_basic(self):
        argument = f"py {str(self.path.joinpath('main.py'))} 10 3 0 0.14 0.05 0 0.000005 --v -f basic run"
        result = subprocess.run(argument.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        print(result.stdout)

        with open('basic-summary.txt', 'r') as f:
            content = f.readlines()
            summary = []
            i = 0
            while i < len(content):
                if content[i] != '\n':
                    summary.append(content[i].strip())
                i += 1

        self.assertTrue('N: 10 people' in summary)
        self.assertTrue('T: 3 days' in summary)

        self.assertTrue('Alpha: 0.0' in summary)
        self.assertTrue('Beta: 0.14' in summary)
        self.assertTrue('Gamma: 0.05' in summary)
        self.assertTrue('Delta: 5e-06' in summary)
        self.assertTrue('Phi: 0.0' in summary)
        self.assertTrue('Tau: 0.5' in summary)
        self.assertTrue('Immune time: 60 days' in summary)
        self.assertTrue('Test rate: 0.5' in summary)

    def test_write_summary_contains_vaccine(self):
        argument = f"py {str(self.path.joinpath('main.py'))} 10 2 0 0.14 0.05 0 0.000005 --i settings/vaccine_settings.txt -m --15 *f=1 --v debug -f test_write_summary_contains_vaccine run"
        result = subprocess.run(argument, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        print(result.stdout)
        # self.fail()

        with open('test_write_summary_contains_vaccine-summary.txt', 'r') as f:
            content = f.readlines()
            summary = []
            i = 0
            while i < len(content):
                if content[i] != '\n':
                    summary.append(content[i].strip())
                i += 1

        # [print(line) for line in summary]

        self.assertTrue('# Vaccine' in summary)
        self.assertTrue('dose: 1' in summary)
        self.assertTrue('dose: 2' in summary)

    def test_write_infected_degree(self):
        N = 50
        T = 200
        argument = f"py {str(self.path.joinpath('main.py'))} {N} {T} 0 0.14 0.05 0 0.000005 --i settings/vaccine_settings.txt -m --52 *m=3 *p=0.1 *a=1 --501 *Ii=4 --505 *m=1 --15 *f=1 --v debug -f test_write_infected_degree run"
        result = subprocess.run(argument, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        print(result.stdout)
        with open('test_write_infected_degree-nwk-deg_S.csv') as degS:
            csv_S = csv.reader(degS)
            deg_S = []
            for row in csv_S:
                deg_S.append(row)

        with open('test_write_infected_degree-nwk-deg_I.csv') as degI:
            csv_I = csv.reader(degI)
            deg_I = []
            for row in csv_I:
                deg_I.append(row)

        for t in range(max(len(deg_S), len(deg_I))):
            self.assertEqual(len(deg_S[t])-1 + len(deg_I[t])-1, N, f'Occured at t = {t}.')
        self.assertEqual(t, T)


    def test_write_vaccinated_cap(self):
        N = 50
        T = 200
        argument = f"py {str(self.path.joinpath('main.py'))} {N} {T} 0 0.14 0.05 0 0.000005 --i settings/vaccine_settings.txt -m --52 *m=3 *p=0.1 *a=1 --501 *Ii=4 --505 *m=1 --15 *f=1 --v debug -f test_write_vaccinated_cap run"
        result = subprocess.run(argument, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        # print(result.stdout)

        alpha_settings = []
        with open('settings/vaccine_settings.txt') as settings:
            lines = settings.readlines()
            for line in lines:
                if line[:7] == 'alpha: ':
                    alpha_settings.append(float(line[7:]))
        cap = alpha_settings[0]

        df_V = pd.read_csv('test_write_vaccinated_cap.csv',header=None,usecols=[2],names=['V'])

        if df_V.query('V > @cap * @N').shape[0] > 0:
            self.fail(df_V.query('V > @cap * @N'))


    def test_write_vaccinated_cap_lg(self):
        '''
        First vaccine has lower adoption rate than second. The first one has set the cap to second.
        '''
        N = 50
        T = 200
        argument = f"py {str(self.path.joinpath('main.py'))} {N} {T} 0 0.14 0.05 0 0.000005 --i settings/vaccine_settings_02.txt -m --52 *m=3 *p=0.1 *a=1 --501 *Ii=4 --505 *m=1 --15 *f=1 --v debug -f test_write_vaccinated_cap_lg run"
        result = subprocess.run(argument, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        # print(result.stdout)

        alpha_settings = []
        with open('settings/vaccine_settings_02.txt') as settings:
            lines = settings.readlines()
            for line in lines:
                if line[:7] == 'alpha: ':
                    alpha_settings.append(float(line[7:]))
        cap = alpha_settings[0]

        df_V = pd.read_csv('test_write_vaccinated_cap_lg.csv',header=None,usecols=[2],names=['V'])

        if df_V.query('V > @cap * @N').shape[0] > 0:
            self.fail(df_V.query('V > @cap * @N'))

