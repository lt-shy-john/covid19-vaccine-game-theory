# Import libraries
import sys
import time
import re
import os

# Import class files
from person import Person
from group import Group
from vaccine import Vaccine
from simulation import Simulation
import mode
from contact import ContactNwk
import customLogger

'''
Main code

- cmd functions
- main loop
'''


def parse_arg(args):
    '''
    Parse system arguments.
    '''
    if type(args) != list:
        args = args.split()
    cmd = {}

    cmd['N'] = args[2]
    cmd['T'] = args[3]
    cmd['alpha'] = args[4]
    cmd['beta'] = args[5]
    cmd['gamma'] = args[6]
    cmd['phi'] = args[7]
    cmd['delta'] = args[8]

    def subls_modes(ls):
        for arg in ls:
            if not re.match(r'--\d', arg) and '=' not in arg:
                return
            yield arg

    def sub_ls_mode(ls):
        if re.match(r'--\d', ls[0]):
            ls = ls[1:]
        for arg in ls:
            if re.match(r'--\d', arg):
                return
            yield arg

    for i in range(len(args)):
        if args[i] == '-import' or args[i] == '--i':
            if args[i + 1][0] == '-' or args[i + 1][0:2] == '--':
                root.info("Invalid setting file name specified. ")
            else:
                # print(os.getcwd())  # To debug when file cannot be fetched.
                cmd['import setting'] = args[i + 1]
        if args[i] == '-test_rate':
            cmd['test rate'] = args[i + 1]
        if args[i] == '-immune_time':
            cmd['immune time'] = args[i + 1]
        if args[i] == '-m':
            cmd['modes'] = {}
            modes_tmp = list(subls_modes(args[i + 1:]))
            # print(modes_tmp)
            for i in range(len(modes_tmp)):
                if re.match(r'--\d', modes_tmp[i]):
                    cmd['modes'][modes_tmp[i][2:]] = list(sub_ls_mode(modes_tmp[i:]))
        if args[i] == '-verbose' or args[i] == '--v':
            if args[i + 1] in ['debug', 'info', 'error']:
                cmd['logger_level'] = args[i + 1]
            else:
                cmd['logger_level'] = 'info'
        if args[i] == '-f':
            if args[i + 1] == 'run':
                raise ValueError('Invalid file name: "run". ')
            if not(args[i + 1][0] == '-' or args[i + 1][0:2] == '--'):
                cmd['filename'] = args[i + 1]
        if args[i] == 'run':
            cmd['express'] = True

    return cmd


def setting(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode):
    info = input('Information about the parameters? [y/n] ').lower()
    print()
    if info == 'y':
        info_summ()
    print('Leave blank if not changing the value(s).')
    N_temp = input('N >>> ')
    N = set_correct_para(N_temp, N, pos=True)
    T_temp = input('T >>> ')
    T = set_correct_para(T_temp, T, pos=True)
    alpha_temp = input('alpha >>> ')
    alpha = set_correct_epi_para(alpha_temp, alpha)
    beta_temp = input('beta >>> ')
    beta = set_correct_epi_para(beta_temp, beta)
    gamma_temp = input('gamma >>> ')
    gamma = set_correct_epi_para(gamma_temp, gamma)
    phi_temp = input('phi >>> ')
    phi = set_correct_epi_para(phi_temp, phi)
    delta_temp = input('delta >>> ')
    delta = set_correct_epi_para(delta_temp, delta)
    cmd = input('Other parameters? [y/n] ')
    if cmd == 'y':
        N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode = setting_other(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode)
    population = Person.make_population(N)
    return N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode


def setting_other(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode):
    print('Adoption parameters \n')
    alpha_V_temp = input('Vaccine: ')
    alpha_V = set_correct_epi_para(alpha_V_temp, alpha_V)
    alpha_T_temp = input('Treatment: ')
    alpha_T = set_correct_epi_para(alpha_T_temp, alpha_T)
    print('\nTransmission parameters \n')
    pass
    print('\nWear-off parameters \n')
    phi_V_temp = input('Vaccine: ')
    phi_V = set_correct_epi_para(phi_V_temp, phi_V)
    phi_T_temp = input('Treatment: ')
    phi_T = set_correct_epi_para(phi_T_temp, phi_T)
    print('\nInfection related')
    immune_time_temp = input('Immune time (days): ')
    immune_time = set_correct_epi_para(immune_time_temp, immune_time)
    print('\nTesting parameters \n')
    test_rate_temp = input('COVID-19: ')
    test_rate = set_correct_epi_para(test_rate_temp, test_rate)
    if 1 in modes:
        print('\nYou have initiated mode 1 \n')
    if 51 in modes or 52 in modes or 53 in modes or 54 in modes:
        print('\nYou have created contact network \n')
        print('\nNetwork parameters \n')
    if 21 in modes:
        group_size_temp = input('Group size: ')
        group_size = set_correct_para(group_size_temp, group_size, pos=True)
    cmd = input('Verbose mode? [y/n]')
    if cmd == 'y':
        verbose_mode = True
    elif cmd == 'n':
        verbose_mode = False
    return N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode


def summary():
    root.info('N: {}'.format(N))
    root.info('T: {}'.format(T))
    root.info('===== SIR Rate =====')
    root.info('alpha: {}'.format(alpha))
    root.info('beta: {}'.format(beta))
    root.info('gamma: {}'.format(gamma))
    root.info('phi: {}'.format(phi))
    root.info('delta: {}'.format(delta))
    cmd = input('Show other epidemic parameters? [y/n] ')
    if cmd == 'y':
        root.info('alpha_V = {}'.format(alpha_V))
        root.info('alpha_T = {}'.format(alpha_T))
        root.info('immune time = {}'.format(immune_time))
        root.info('test rate: {}'.format(test_rate))
    print()
    info = input('Information about the parameters? [y/n] ').lower()
    if info == 'y':
        info_summ()
    print()
    if len(modes) > 0:
        info = input('There are customised settings. View them? [y/n] ')
        if info == 'y':
            for mode in modes.values():
                print(mode.__dict__)
    print()


def show_nwk():
    if contact_nwk.network != None:
        contact_nwk.show_nwk()
    else:
        print('Topology is not set, use command "MODE" to initiate them.')


def info_summ():
    root.info('N - Number of simulated agents.')
    root.info('T - Time steps/ period of simulation.')
    root.info('Alpha - Adoption of vaccination/ PrEP (willingness).')
    root.info('Beta - Infection rate.')
    root.info('Gamma - Recovery rate.')
    root.info('Delta - Removal rate.')
    root.info('Phi - Protection wear off rate.')
    root.info('Delta - Removal rate.')
    root.info('Tau - COVID-19 Testing rate. ')


def help():
    root.info('LOOK - View partner network.')
    root.info('MODE - Change mode settings.')
    root.info('RUN/ START - Start the simulation.')
    root.info('SETTING - Set simulation settings.')
    root.info('OTHER SETTING - Set auxiliary simulation parameters.')
    root.info('SUMMARY - Print the simulation parameters.')
    root.info('QUIT/ Q - Quit the software.')


def usage():
    root.info('Usage: python3 main.py [(N) (T) (α) (β) (γ) (φ) (δ)] ...\n\
    [-m  <modes_config>] [-f (filename)] [-verbose | --v] [run]\n')
    root.info('-immune_time \t Immune time after recovered, in days.')
    root.info('-test_rate \t COVID-19 testing rate.')
    root.info('-m \t\t Mode')
    root.info('    --1 \t Living in city/ rural.')
    root.info('    --2 \t Travelled back from overseas.')
    root.info('    --4 \t Bounded rationality of vaccine.')
    root.info('    --5 \t Edit contact network.')
    root.info('    --7 \t Age distribution.')
    root.info('    --8 \t Gender distribution.')
    root.info('    --10 \t Type of vaccine.')
    root.info('    --11 \t Stop transmissability/ reduce severity.')
    root.info('    --12 \t Cost of vaccine.')
    root.info('    --13 \t Accessibility to vaccine.')
    root.info('    --14 \t Side effects of vaccine.')
    root.info('    --15 \t Advanced vaccine options.')
    root.info('    --20 \t Intimacy game.')
    root.info('    --21 \t Local majority rule.')
    root.info('    --22 \t Stubbon to take vaccine.')
    root.info('    --23 \t Stubbon to against vaccine.')
    root.info('    --24 \t Contrary to social groups.')
    root.info('    --31 \t Medication incorporated.')
    root.info('    --41 \t Game of social distancing.')
    root.info('    --42 \t Moral hazard of treatment.')
    root.info('    --51 \t Erdos-Renyi topology.')
    root.info('    --52 \t Preferential attachment.')
    root.info('    --53 \t Small world network.')
    root.info('    --54 \t Lattice network.')
    root.info('    --501 \t Initial infection by number.')
    root.info('    --505 \t Initial infection by degree.')
    root.info('-f \t\t Export file name.')
    root.info('-h \t\t Usage.')
    root.info('run \t\t Run simulation, last argument.')


def correct_bool_para(b):
    '''
    Convert the parameters into boolean.

    Parameters
    ----------
    b: bool
        Input.
    '''
    try:
        if b == 'True':
            b_bool = True
        elif b == 'False':
            b_bool = False
        else:
            raise ValueError ('Invalid boolean input. Please check your inputs. Default: True')
        return b_bool
    except ValueError:
        b_bool = True
        return b_bool


def set_correct_bool_para(b, B):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if b == '':
        return B
    else:
        return correct_bool_para(b)


def correct_para(p, pos=False):
    '''
    Convert the parameters into integers.

    Parameters
    p -- input.
    - pos: If the parameter is positive number.
    '''
    try:
        p_num = int(p)
        if pos == True and p_num < 1:
            p_num = 1
        return p_num
    except ValueError:
        p_num = 1
        return p_num


def set_correct_para(p, P, pos=False):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if p == '':
        return P
    else:
        return correct_para(p, pos=False)


def correct_epi_para(p):
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

def set_correct_epi_para(p, P):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if p == '':
        return P
    else:
        return correct_epi_para(p)

def set_mode(mode):
    cmd = ''
    while cmd != 'y':
        root.info('Select the following options:')
        root.info('01: Living in city/ rural [{}]'.format(mode01.flag))
        root.info('02: Travel from overseas [{}]'.format(mode02.flag))
        root.info('04: Bounded rationality of vaccine [{}]'.format(mode04.flag))
        root.info('05: Edit contact network')
        root.info('07: Age distribution [{}]'.format(mode07.flag))
        root.info('08: Gender population [{}]'.format(mode08.flag))
        root.info('10: Type of vaccine [{}]'.format(mode10.flag))
        root.info('11: Stop transmissability/ reduce severity [{}]'.format(mode11.flag))
        root.info('12: Cost of vaccine []')
        root.info('13: Accessibility to vaccine []')
        root.info('14: Side effects of vaccine []')
        root.info('15: Advanced vaccine options [{}]'.format(mode15.flag))
        root.info('20: Imitation game [{}]'.format(mode20.flag))
        root.info('21: Local majority rule [{}]'.format(mode21.flag))
        root.info('22: Stubbon to take vaccine[{}]'.format(mode22.flag))
        root.info('23: Stubbon to against vaccine[{}]'.format(mode23.flag))
        root.info('24: Contrary to social groups[{}]'.format(mode24.flag))
        root.info('31: Medication incorporated [{}]'.format(mode31.flag))
        root.info('41: Game of social distancing []')
        root.info('42: Moral hazard of treatment []')
        root.info('51: Erdos-Renyi topology [{}]'.format(mode51.flag))
        root.info('52: Preferential attachment [{}]'.format(mode52.flag))
        root.info('53: Small world topology [{}]'.format(mode53.flag))
        root.info('54: Lattice network [{}]'.format(mode54.flag))
        root.info('501: Initial infection by number [{}]'.format(mode501.flag))
        root.info('505: Initial infection by degree [{}]'.format(mode505.flag))
        root.info('Input number codes to change the options.')
        mode_input = input('> ')
        root.debug(mode_input)
        mode = mode_settings(mode_input, mode)
        cmd = input('Return to main menu? [y/n] ')
    return mode

def mode_settings(cmd, logger, mode=None):
    if type(cmd) == list:
        logger.warning("Using legacy method to change modes, please check code to make sure settings are stored in dict form. ")
        return legacy_mode_settings(cmd, mode)
    elif type(cmd) == dict:
        return change_mode(cmd, mode)


def change_mode(cmd, mode):
    pass


def legacy_mode_settings(cmd, mode):
    cmd = cmd.split(' ')
    if cmd == ['']:
        # If empty response, then leave prematurely.
        return mode
    rv_modes = []
    if '-dp' in cmd:
        removal_idx = cmd.index('-dp')
    root.info('Adding: ')
    if '-dp' in cmd:
        root.debug(cmd[:removal_idx])
        root.debug('Removing')
        root.debug(cmd[removal_idx+1:])

        rv_modes = cmd[removal_idx+1:]
        cmd = cmd[:removal_idx]
    else:
        print(cmd)
    if len(cmd) > 0 and '-dp' not in cmd:
        for i in range(len(cmd)):
            try:
                int(cmd[i])
            except ValueError:
                root.info('Wrong data type for mode, please check your inputs.')
                continue
            if int(cmd[i]) == 1:
                mode01()
                if mode01.flag == 'X':
                    mode[1] = mode01
                else:
                    mode.pop(1)
            elif int(cmd[i]) == 2:
                mode02()
                if mode02.flag == 'X':
                    mode[2] = mode02
                else:
                    mode.pop(2)
            elif int(cmd[i]) == 4:
                mode04()
                if mode04.flag == 'X':
                    mode[4] = mode04
                else:
                    mode.pop(4)
            elif int(cmd[i]) == 5:
                mode05()
                if mode05.flag == 'X':
                    mode[5] = mode05
                else:
                    mode.pop(5)
            elif int(cmd[i]) == 7:
                mode07()
                if mode07.flag == 'X':
                    mode[7] = mode07
                else:
                    mode.pop(7)
            elif int(cmd[i]) == 8:
                mode08()
                if mode08.flag == 'X':
                    mode[8] = mode08
                else:
                    mode.pop(8)
            elif int(cmd[i]) == 10:
                mode10()
                if mode10.flag == 'X':
                    mode[10] = mode10
                else:
                    mode.pop(10)
            elif int(cmd[i]) == 11:
                mode11()
                if mode11.flag == 'X':
                    mode[11] = mode11
                else:
                    mode.pop(10)
            elif int(cmd[i]) == 15:
                mode15(alpha, beta, gamma, delta, phi)
                if mode15.flag == 'X':
                    mode[15] = mode15
                else:
                    mode.pop(10)
            elif int(cmd[i]) == 20:
                mode20()
                if mode20.flag == 'X':
                    mode[20] = mode20
                else:
                    mode.pop(21)
            elif int(cmd[i]) == 21:
                mode21()
                if mode21.flag == 'X':
                    mode[21] = mode21
                else:
                    mode.pop(21)
            elif int(cmd[i]) == 22:
                if check_main_mode_opinion(modes,22) == True:
                    mode22()
                if mode22.flag == 'X':
                    mode[22] = mode22
                else:
                    mode.pop(22)
            elif int(cmd[i]) == 23:
                if check_main_mode_opinion(modes,23) == True:
                    mode23()
                if mode23.flag == 'X':
                    mode[23] = mode23
                else:
                    mode.pop(23)
            elif int(cmd[i]) == 24:
                if check_main_mode_opinion(modes,24) == True:
                    mode24()
                if mode24.flag == 'X':
                    mode[24] = mode24
                else:
                    mode.pop(24)
            elif int(cmd[i]) == 31:
                mode31()
                if mode31.flag == 'X':
                    mode[31] = mode31
                else:
                    mode.pop(31)
            elif int(cmd[i]) == 51:
                if (mode52.flag == 'X'):
                    print('Mode 52 has been activated. Mode 51 unable to start.')
                    break
                elif (mode53.flag == 'X'):
                    print('Mode 53 has been activated. Mode 51 unable to start.')
                    break
                elif (mode54.flag == 'X'):
                    print('Mode 54 has been activated. Mode 51 unable to start.')
                    break
                mode51()
                if mode51.flag == 'X':
                    mode[51] = mode51
                else:
                    mode.pop(51)
            elif int(cmd[i]) == 52:
                if (mode51.flag == 'X'):
                    print('Mode 51 has been activated. Mode 52 unable to start.')
                    break
                elif (mode53.flag == 'X'):
                    print('Mode 53 has been activated. Mode 51 unable to start.')
                    break
                elif (mode54.flag == 'X'):
                    print('Mode 54 has been activated. Mode 51 unable to start.')
                    break
                mode52()
                if mode52.flag == 'X':
                    mode[52] = mode52
                else:
                    mode.pop(52)
            elif int(cmd[i]) == 501:
                mode501()
                if mode501.flag == 'X':
                    mode[501] = mode501
                else:
                    mode.pop(501)
            elif int(cmd[i]) == 505:
                mode505()
                if mode505.flag == 'X':
                    mode[505] = mode505
                else:
                    mode.pop(505)
    # Remove modes (Check if the modes itself overwrites basic settings)
    if len(rv_modes) > 0:
        for mode_opt in rv_modes:
            try:
                print(mode[int(mode_opt)].flag)
                mode[int(mode_opt)].drop_flag()
            except KeyError:
                continue
            except ValueError:
                continue
    return mode


def check_main_mode_opinion(modes, code):
    if 21 not in modes:
        print(f'Warning: Mode 21 is requried for activating mode {code}.')
        print('Please return to settings to activate this mode first. ')
        return False
    return True


def find_mode(code, mode_master_list):
    for mode in mode_master_list:
        if mode.code == code:
            return mode

'''
(Semi) Express Mode: Reading pre-formatted setting files
'''
def read_settings(filename):
    '''
    Read and parse pre-filled settings file.
    '''
    root.debug("Reading filename")
    with open(filename, 'r') as settings_f:
        settings_text = settings_f.readlines()
    root.info('Read settings successfully')

    l1_flags = []
    l2_flags = []

    for i in range(len(settings_text)):
        if settings_text[i].split(" ")[0] == '#':
            l1_flags.append(i)
        elif settings_text[i].split(" ")[0] == '##':
            l2_flags.append(i)


    vaccines = []
    # Parse vaccine creation
    for idx in l2_flags:
        parsed_line = settings_text[idx].split(' ')
        if parsed_line[0] == '##' and parsed_line[1] == 'Vaccine\n':
            vaccine_contents = settings_text[idx+1:idx+12]
            vaccines.append(parse_vaccine_setting(vaccine_contents))
    root.debug('Custom vaccines created')

    return vaccines


def parse_vaccine_setting(contents):
    param = {'name': None, 'dose': None, 'days': None, 'vaccine_type': None, 'cost': None, 'efficacy': None, 'alpha': None, 'beta': None, 'gamma': None, 'delta': None, 'phi': None}
    i = 0
    for k, v in param.items():
        try:
            if k == 'dose' or k == 'days' or k == 'vaccine_type':
                param[k] = int(contents[i].split(':')[1].strip())
            elif k == 'cost' or k == 'efficacy' or k == 'alpha' or k == 'beta' or k == 'gamma' or k == 'delta' or k == 'phi':
                param[k] = float(contents[i].split(':')[1].strip())
            else:
                param[k] = contents[i].split(':')[1].strip()
        except IndexError:
            root.info(f'There are no param {k} specified.')
        except ValueError:
            root.info(f'{k} has invalid parameters, changing to None. ')
            param[k] = None
        i += 1
    return Vaccine(**param)


def export(filename):
    print('Coming soon')


root = customLogger.gen_logging('', None)

root.info('  ==========================================  \n\n')
root.info('  Agent Based Modelling: COVID-19 SUEP Model  \n\n')
root.info('  ==========================================  \n')

# Express mode: Call usage information
if len(sys.argv) == 2 and (sys.argv[1] == '-help' or sys.argv[1] == '-h'):
    usage()
    quit()

if len(sys.argv) == 1:
    N = input('Number of people (N): ')
    N = correct_para(N, pos=True)
    T = input('Simulation time (T): ')
    T = correct_para(T)
    alpha = input('Adoption rate (alpha): ')
    alpha = correct_epi_para(alpha)
    beta = input('Infection rate (beta): ')
    beta = correct_epi_para(beta)
    gamma = input('Recovery rate (gamma): ')
    gamma = correct_epi_para(gamma)
    phi = input('Rate to resuscept (phi): ')
    phi = correct_epi_para(phi)
    delta = input('Removal rate (delta): ')
    delta = correct_epi_para(delta)
elif len(sys.argv) > 1:
    root.info('Using pre-defined inputs. ')
    try:
        N = correct_para(sys.argv[1], pos=True)
        T = correct_para(sys.argv[2])
        alpha = correct_epi_para(sys.argv[3])
        beta = correct_epi_para(sys.argv[4])
        gamma = correct_epi_para(sys.argv[5])
        phi = correct_epi_para(sys.argv[6])
        delta = correct_epi_para(sys.argv[7])
    except:
        print('Exception encountered. Leaving program...')
        print('Usage: python3 main.py [(N) (T) (α) (β) (γ) (φ) (δ)] ...\n[-m <modes_config>] [-f (filename)] [run]\n')
        quit()
print()

'''
Set initial variables
'''
alpha_V = alpha
alpha_T = alpha
beta_SS = 0.0
beta_II = 0.0
beta_RR = 0.01
beta_VV = 0.0
beta_IR = 0.01
beta_SR = 0.01
beta_SV = 0.01
beta_PI = 0.01
beta_IV = 0.01
beta_RV = 0.01
beta_SI2 = beta
beta_II2 = 0.0
beta_RI2 = beta_IR
beta_VI2 = beta_IV
phi_V = phi
phi_T = 0.95
test_rate = 0.5
immune_time = 60
group_size = 3

verbose_mode = False  # Need to put here for initiating other objects (nwk and person if needed).
population = Person.make_population(N)
contact_nwk = ContactNwk(population, verbose_mode, root)
info_nwk = Group(population, root, group_size)
vaccine_available = [Vaccine('Default', 1, 28, None, 0, 0.99, alpha, beta, gamma, delta, phi)]
filename = ''  # Default file name to export (.csv). Change when use prompt 'export' cmd.

mode_master_list = []
# All objects should add into mode_master_list
mode01 = mode.Mode01(population, root)
mode02 = mode.Mode02(population, beta, root)
mode04 = mode.Mode04(population, alpha, root)
mode05 = mode.Mode05(population, contact_nwk, root)
mode07 = mode.Mode07(population, beta, delta, root)
mode08 = mode.Mode08(population, beta, delta, root)
mode10 = mode.Mode10(population, phi, beta, root)
mode11 = mode.Mode11(population, root)
mode15 = mode.Mode15(population, root)
mode20 = mode.Mode20(population, contact_nwk, beta, root)
mode21 = mode.Mode21(population, info_nwk, root)
mode22 = mode.Mode22(population, info_nwk, root)
mode23 = mode.Mode23(population, info_nwk, root)
mode24 = mode.Mode24(population, info_nwk, root)
mode31 = mode.Mode31(population, root)
mode51 = mode.Mode51(population, contact_nwk, root)
mode52 = mode.Mode52(population, root, contact_nwk)
mode53 = mode.Mode53(population, root, contact_nwk)
mode54 = mode.Mode54(population, root, contact_nwk)
mode501 = mode.Mode501(population, root, contact_nwk)
mode505 = mode.Mode505(population, root, contact_nwk)

mode_master_list = [mode01, mode02, mode04, mode05, mode07, mode08,
mode10, mode11, mode15,
mode20, mode21, mode22, mode23, mode24,
mode31,
mode51, mode52, mode53, mode54,
mode501, mode505]


modes = {}

'''
Express mode

Loads the settings prior to the run. Optional keyword 'run' to run the simulation automatically.
'''

settings = parse_arg(sys.argv)
if 'logger_level' in settings:
    logging_level = ['debug', 'info', 'warning', 'error', 'critical']
    if type(settings['logger_level']) == str:
        if settings['logger_level'].lower() in logging_level:
            root.info("Logging level detected: " + settings['logger_level'])
            verbose_level = settings['logger_level']
        else:
            verbose_level = 'info'
    else:
        verbose_level = 'info'

    # Write log to file is filename exists
    if 'filename' in settings:
        root = customLogger.gen_logging(settings['filename'], verbose_level)
    else:
        root = customLogger.gen_logging('', verbose_level)
if 'immune time' in settings:
    immune_time_temp = settings['immune time']
    immune_time = set_correct_para(immune_time_temp, immune_time, pos=True)
if 'test rate' in settings:
    test_rate_temp = settings['test rate']
    test_rate = set_correct_epi_para(test_rate_temp, test_rate)
if 'import setting' in settings:
    try:
        vaccine_available = read_settings(settings['import setting'])
        root.debug(f'Vaccine read from setting: {[x.__dict__ for x in vaccine_available]}')
    except FileNotFoundError as fnfe:
        root.error(fnfe)
        root.error(f'Current directory: {os.getcwd()}')
if 'modes' in settings:
    pass

for i in range(len(sys.argv)):
    try:
        if sys.argv[i] == '-m':
            for j in range(i+1,len(sys.argv)):
                # Skip at other options
                if sys.argv[j][:2] == '--':
                    mode_flag = int(sys.argv[j][2:])
                    root.debug('Loading mode: {}'.format(mode_flag))

                    # Activate modes with no options needed
                    if mode_flag == 21:
                        info_nwk.set_roster()
                        info_nwk.set_population()
                        mode21.raise_flag()
                        if mode21.flag == 'X':
                            modes[21] = mode21
                        else:
                            mode.pop(21)
                    elif mode_flag == 51:
                        if 52 in modes:
                            root.debug('Mode 52 has been activated. Ignore mode 51. ')
                            break
                        elif 53 in modes:
                            root.debug('Mode 53 has been activated. Ignore mode 52. ')
                            break
                        elif 54 in modes:
                            root.debug('Mode 54 has been activated. Ignore mode 52. ')
                            break
                        mode51()
                        if mode51.flag == 'X':
                            modes[51] = mode51
                        else:
                            modes.pop(51)

                    # Loop through config values
                    for k in range(j+1,len(sys.argv)):
                        if sys.argv[k][0] == '-' and sys.argv[k][1].isalpha():
                            break
                        if sys.argv[k][:2] == '--':
                            break

                        # Set up individual modes
                        if mode_flag == 1:
                            # Placeholder
                            if sys.argv[k][:3] == '*b=':
                                mode01_b_config = sys.argv[k][3:].split(',')
                                b_c = float(mode01_b_config[0])
                                b_r = float(mode01_b_config[1])
                                mode01.set_beta(0,b_c)
                                mode01.set_beta(1,b_r)
                            elif sys.argv[k][:3] == '*p=':
                                mode01_p_config = sys.argv[k][3:].split(',')
                                w_c = float(mode01_p_config[0])
                                w_r = float(mode01_p_config[1])
                                mode01.set_weight(w_c, w_r)

                            mode01.assign_regions()
                            mode01.raise_flag()
                            if mode01.flag == 'X':
                                modes[1] = mode01
                            else:
                                mode.pop(1)
                        elif mode_flag == 2:
                            if sys.argv[k][:4] == '*rI=':
                                r_I_temp = mode02.rI
                                r_I_config = sys.argv[k][4:]
                                mode02.rI = set_correct_para(r_I_config, r_I_temp)
                            elif sys.argv[k][:4] == '*rS=':
                                r_S_temp = mode02.rI
                                r_S_config = sys.argv[k][4:]
                                mode02.rS = set_correct_para(r_S_config, r_S_temp)
                            elif sys.argv[k][:4] == '*lI=':
                                localIsolation_temp = True
                                localIsolation_config = sys.argv[k][4:]
                                mode02.localIsolation = set_correct_bool_para(localIsolation_config, localIsolation_temp)
                            elif sys.argv[k][:3] == '*i=':
                                mode02_isolation_period_config = sys.argv[k][3:]
                                mode02.isolationPeriod = set_correct_para(mode02_isolation_period_config, mode02.isolationPeriod, pos=True)
                            mode02.create_setting()
                            mode02.raise_flag()
                            if mode02.flag == 'X':
                                modes[2] = mode02
                            else:
                                mode.pop(2)
                        elif mode_flag == 4:
                            if sys.argv[k][:3] == '*l=':
                                lambda_BR = population[0].lambda_BR
                                mode04_l_config = sys.argv[k][3:]
                                lambda_BR = set_correct_para(mode04_l_config, lambda_BR, pos=True)
                                mode04.set_lambda(lambda_BR)
                            mode04.QRE()
                            mode04.raise_flag()
                            if mode04.flag == 'X':
                                modes[4] = mode04
                            else:
                                mode.pop(4)
                        elif mode_flag == 7:
                            if sys.argv[k][:3] == '*b=':
                                mode07_b_config = sys.argv[k][3:].split(',')
                                mode07.beta_age = [float(x) for x in mode07_b_config]
                            elif sys.argv[k][:3] == '*d=':
                                mode07_d_config = sys.argv[k][3:].split(',')
                                mode07.delta_age = [float(x) for x in mode07_d_config]
                            mode07.set_population()
                            mode07.raise_flag()
                            if mode07.flag == 'X':
                                modes[7] = mode07
                            else:
                                modes.pop(7)
                        elif mode_flag == 8:
                            if sys.argv[k][:3] == '*b=':
                                mode08_b_config = sys.argv[k][3:].split(',')
                                mode08.beta_gender = [float(x) for x in mode08_b_config]
                            elif sys.argv[k][:3] == '*d=':
                                mode08_d_config = sys.argv[k][3:].split(',')
                                mode08.delta_gender = [float(x) for x in mode08_d_config]
                            mode08.set_population()
                            mode08.raise_flag()
                            if mode08.flag == 'X':
                                modes[8] = mode08
                            else:
                                modes.pop(8)
                        elif mode_flag == 10:
                            if sys.argv[k][:6] == '*mode=':
                                modes[10].type = modes[10].check_input(sys.argv[k][6:])
                            if mode10.flag == 'X':
                                modes[10] = mode10
                            else:
                                modes.pop(10)
                        elif mode_flag == 11:
                            if sys.argv[k][:6] == '*mode=':
                                modes[11].type = modes[11].check_input(sys.argv[k][6:])
                            elif sys.argv[k][:3] == '*b=':
                                mode11_b_config = sys.argv[k][3:]
                                mode11.beta_V = set_correct_para(mode11_b_config, mode11.beta_V)
                                mode11.check_beta()
                            elif sys.argv[k][:3] == '*g=':
                                mode11_g_config = sys.argv[k][3:]
                                mode11.gamma_V = set_correct_para(mode11_g_config, mode11.gamma_V)
                                mode11.check_gamma()
                            elif sys.argv[k][:3] == '*d=':
                                mode11_d_config = sys.argv[k][3:]
                                mode11.delta_V = set_correct_para(mode11_d_config, mode11.delta_V)
                                mode11.check_delta()
                            if mode11.flag == 'X':
                                modes[11] = mode11
                            else:
                                modes.pop(11)
                        elif mode_flag == 15:
                            root.debug('Express mode: Activating mode 15. ')
                            if sys.argv[k][:3] == '*f=':
                                mode15.raise_flag()
                            mode15.raise_flag()
                            if mode15.flag == 'X':
                                modes[15] = mode15
                            else:
                                modes.pop(15)
                        elif mode_flag == 20:
                            if sys.argv[k][:4] == '*cV=':
                                cV_temp = sys.argv[k][4:]
                                mode20.set_cV(cV_temp)
                            elif sys.argv[k][:4] == '*cI=':
                                cI_temp = sys.argv[k][4:]
                                mode20.set_cI(cI_temp)
                            elif sys.argv[k][:4] == '*kV=':
                                kV_temp = sys.argv[k][4:]
                                mode20.set_kV(kV_temp)
                            elif sys.argv[k][:4] == '*kI=':
                                kI_temp = sys.argv[k][4:]
                                mode20.set_kI(kI_temp)
                            elif sys.argv[k][:4] == '*sV=':
                                sV_temp = sys.argv[k][4:]
                                mode20.set_sV(sV_temp)
                            elif sys.argv[k][:4] == '*sI=':
                                sI_temp = sys.argv[k][4:]
                                mode20.set_sI(sI_temp)
                            elif sys.argv[k][:4] == '*pV=':
                                pV_temp = sys.argv[k][4:]
                                mode20.set_pV(pV_temp)
                            elif sys.argv[k][:4] == '*pI=':
                                pI_temp = sys.argv[k][4:]
                                mode20.set_pI(pI_temp)
                            elif sys.argv[k][:3] == '*r=':
                                rho_temp = sys.argv[k][3:]
                                mode20.set_rho(rho_temp)
                            mode20.assign_costs()
                            mode20.raise_flag()
                            if mode20.flag == 'X':
                                modes[20] = mode20
                            else:
                                modes.pop(20)
                        elif mode_flag == 21:
                            root.debug('Express mode: Activating mode 21. ')
                            if sys.argv[k][:3] == '*+=':
                                mode21_pro_config = sys.argv[k][3:]
                                mode21.info_nwk.set_pro(mode21_pro_config)
                            elif sys.argv[k][:3] == '*-=':
                                mode21_ag_config = sys.argv[k][3:]
                                mode21.info_nwk.set_ag(mode21_ag_config)
                            if mode21.info_nwk.propro != None and mode21.info_nwk.agpro != None:
                                mode21.info_nwk.set_opinion()
                                mode21.set_personality()
                                mode21.raise_flag()
                                if mode21.flag == 'X':
                                    modes[21] = mode21
                                else:
                                    modes.pop(21)
                        elif mode_flag == 22:
                            root.debug('Express mode: Activating mode 22. ')
                            if sys.argv[k][:3] == '*p=':
                                mode22_pro_config = sys.argv[k][3:]
                                root.debug(f'Proportion of stubbonly support vaccination are {mode22_pro_config}. ')
                                mode22.assign_personality(mode22_pro_config)
                            elif sys.argv[k][:3] == '*+=':
                                mode22_pro_config = sys.argv[k][3:]
                                root.debug(f'Proportion of pro-vaccine is {mode22_pro_config}. ')
                                mode22.info_nwk.set_pro(mode22_pro_config)
                            elif sys.argv[k][:3] == '*-=':
                                mode22_ag_config = sys.argv[k][3:]
                                root.debug(f'Proportion of against vaccine is {mode22_ag_config}. ')
                                mode22.info_nwk.set_ag(mode22_ag_config)
                            if mode22.info_nwk.propro != None and mode22.info_nwk.agpro != None and mode22.InflexProProportion != None:
                                mode22.info_nwk.set_opinion()
                                mode22.raise_flag()
                                if mode22.flag == 'X':
                                    modes[22] = mode22
                                else:
                                    modes.pop(22)
                        elif mode_flag == 23:
                            root.debug('Express mode: Activating mode 23. ')
                            if sys.argv[k][:3] == '*p=':
                                mode23_ag_config = sys.argv[k][3:]
                                root.debug(f'Proportion of stubbonly against vaccination are {mode23_ag_config}. ')
                                mode23.assign_personality(mode23_ag_config)
                                root.debug('Assigned personality to the population. ')
                            elif sys.argv[k][:3] == '*+=':
                                mode23_pro_config = sys.argv[k][3:]
                                root.debug(f'Proportion of pro-vaccine is {mode23_pro_config}. ')
                                mode23.info_nwk.set_pro(mode23_pro_config)
                            elif sys.argv[k][:3] == '*-=':
                                mode23_ag_config = sys.argv[k][3:]
                                root.debug(f'Proportion of against vaccine is {mode23_ag_config}. ')
                                mode23.info_nwk.set_ag(mode23_ag_config)
                            if mode23.info_nwk.propro != None and mode23.info_nwk.agpro != None and mode23.InflexAgProportion != None:
                                mode23.info_nwk.set_opinion()
                                mode23.raise_flag()
                                if mode23.flag == 'X':
                                    modes[23] = mode23
                                else:
                                    modes.pop(23)
                        elif mode_flag == 24:
                            root.debug('Express mode: Activating mode 24. ')
                            if sys.argv[k][:3] == '*p=':
                                mode24_pro_config = sys.argv[k][3:]
                                mode24.assign_personality(mode24_pro_config)
                            elif sys.argv[k][:3] == '*+=':
                                mode24_pro_config = sys.argv[k][3:]
                                mode24.info_nwk.set_pro(mode24_pro_config)
                            elif sys.argv[k][:3] == '*-=':
                                mode24_ag_config = sys.argv[k][3:]
                                mode24.info_nwk.set_ag(mode24_ag_config)
                            if mode24.info_nwk.propro != None and mode24.info_nwk.agpro != None:
                                mode24.info_nwk.set_opinion()
                                mode24.raise_flag()
                                if mode24.flag == 'X':
                                    modes[24] = mode24
                                else:
                                    modes.pop(24)
                        elif mode_flag == 52:
                            root.debug('Express mode: Activating mode 52. ')
                            if 51 in modes:
                                root.debug('Mode 51 has been activated. Ignore mode 52. ')
                                break
                            elif 53 in modes:
                                root.debug('Mode 53 has been activated. Ignore mode 52. ')
                                break
                            elif 54 in modes:
                                root.debug('Mode 54 has been activated. Ignore mode 52. ')
                                break

                            if sys.argv[k][:3] == '*m=':
                                mode52_m_config = int(sys.argv[k][3:])
                                mode52.set_m(mode52_m_config)
                                root.debug(f'Set number of connections m = {mode52.m}. ')
                            elif sys.argv[k][:3] == '*p=':
                                contact_nwk.update_rule = 'XBS'
                                mode52_p_config = float(sys.argv[k][3:])
                                mode52.set_pupdate(mode52_p_config)
                                root.debug(f'Probability of updates p = {contact_nwk.PUpdate}. ')
                            elif sys.argv[k][:3] == '*a=':
                                contact_nwk.update_rule = 'XBS'
                                mode52_assort = int(sys.argv[k][3:])
                                if mode52_assort == 1:
                                    contact_nwk.assort = True
                                elif mode52_assort == 0:
                                    contact_nwk.assort = False
                                root.debug(f'Update rule: XBS. ')
                            elif sys.argv[k][:3] == '*l=':
                                contact_nwk.update_rule = 'random'
                                mode52_l_config = [int(x) for x in sys.argv[k][3:].split(',')]
                                mode52.set_l0(mode52_l_config[0])
                                mode52.set_l1(mode52_l_config[1])
                                root.debug(f'Update rule: random. ')
                            mode52.set_network()
                            root.debug(f'Preferential attachment is created. ')
                            mode52.raise_flag()
                            if mode52.flag == 'X':
                                modes[52] = mode52
                            else:
                                mode.pop(52)
                        elif mode_flag == 501:
                            root.debug('Express mode: Activating mode 501. ')
                            if sys.argv[k][:4] == '*Ii=':
                                Ii_temp = sys.argv[k][4:]
                                mode501.init_infection = mode501.set_init_infection(Ii_temp)
                            mode501.raise_flag()
                            if mode501.flag == 'X':
                                modes[501] = mode501
                            else:
                                mode.pop(501)
                        elif mode_flag == 505:
                            root.debug('Express mode: Activating mode 505. ')
                            if sys.argv[k][:3] == '*m=':
                                mode_505 = sys.argv[k][3:]
                                try:
                                    if int(mode_505) == 1:
                                        mode_tmp = 'Hub'
                                    elif int(mode_505) == 0:
                                        mode_tmp = 'Leaf'
                                except ValueError:
                                    if mode_505.lower() == 'hub':
                                        mode_tmp = 'Hub'
                                    elif mode_505.lower() == 'leaf':
                                        mode_tmp = 'Leaf'
                            mode505.raise_flag()
                            if mode505.flag == 'X':
                                modes[505] = mode505
                                modes[505].mode = mode_tmp
                            else:
                                mode.pop(505)
                        else:
                            print('Warning: Mode not detected. ')


                        # elif mode_flag == 999:
                        #     # There are 3 args with last one characters
                        #     seven_config(*[int(data) if data.isnumeric() else data for data in config])
                    continue
                if sys.argv[j][0] == '-' and sys.argv[j][1].isalpha():
                    break
                if sys.argv[j] == 'run':
                    break
                # print(mode_flag, '*'+str(argv[j]))
    except ValueError as ve:
        root.info('Invalid input. Check your arguments. ')
        root.debug(ve)
        continue
    except IndexError:
        break

    # Check file name to export
    try:
        if sys.argv[i] == '-f':
            if sys.argv[i+1] == 'run':
                raise ValueError
            filename = sys.argv[i+1]
    except ValueError:
        print('No file name provided. Please check your inputs.')
        continue
    except IndexError:
        break


if 'express' in settings and settings['express'] == True:
    root.info('===== Simulation Running =====')
    current_run = Simulation(population, T, population, contact_nwk, info_nwk, alpha, beta, gamma, phi, delta, filename,
                             alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI,
                             beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2, test_rate, immune_time,
                             vaccine_available, verbose_mode, 'info', root)
    # Load modes
    current_run.load_modes(modes)
    if len(modes) > 0:
        root.debug('modes', current_run.modes)
        root.debug('\nMode objects loaded.\n')
    # Run
    current_run()
    print('=====  Simulation Ended  =====')
    print('\nSee you!')
    quit()

'''
Normal mode
'''

while True:
    cmd = input('>>> ').lower()
    if cmd == 'setting':
        N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode = setting(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode)
        population = Person.make_population(N)
    elif cmd == 'other setting':
        root.info('Leave blank if not changing the value(s).')
        N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode = setting_other(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time, group_size, verbose_mode)
    elif cmd == 'summary':
        summary()
    elif cmd == 'look':
        show_nwk()
    elif cmd == 'help':
        help()
    elif cmd == 'start' or cmd == 'run':
        root.info('===== Simulation Running =====')
        current_run = Simulation(population, T, population, contact_nwk, info_nwk, alpha, beta, gamma, phi, delta,
                                 filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR,
                                 beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2, test_rate,
                                 immune_time, vaccine_available, verbose_mode, 'info', root)
        # Load modes
        current_run.load_modes(modes)
        if len(modes) > 0:
            root.debug('Mode objects loaded.')
            root.debug(modes)
        # Run
        current_run()
        print('=====  Simulation Ended  =====')
    elif cmd == 'mode':
        modes = set_mode(modes)
    elif cmd == 'export':
        filename = input('File name: ')
    elif cmd == 'thank you':
        root.info('  ==========================================  \n\n')
        root.info('  Agent Based Modelling: COVID-19 SEIP Model  \n\n')
        root.info('  ==========================================  ')
        time.sleep(3)
        root.info('\n\nAuthor: Shing Hin (John) Yeung\n')
        time.sleep(1)
        root.info('This software code comes from Masters in Complex Systems a Capstone Project. \n')
        time.sleep(1)
        root.info('It aims for modelling human choice upon vaccine adoption and therefore predict the epidemic. \n\n')
        time.sleep(1)
        root.info('The author would like to thank you to many people who conrtibuted to this project. \n')
        time.sleep(1)
        root.info('Dr Shailendra Sawleshwarkar')
        root.info('A/ Prof Iryna Zablotska-Manos')
        root.info('Dr Samit Bhattacharyya')
        time.sleep(3)
        root.info('\n\nPrimary supervisor')
        root.info('Dr Mahendrarajah Piraveenan\n')
        time.sleep(3)
        root.info('This study dedicates to the society that strives in the COVID-19 pandemic. \n\n\n')
        time.sleep(1)
        root.info('==== Thank you ====')
    elif cmd == 'quit' or cmd == 'q':
        root.info('See you!')
        quit()
    else:
        root.info('Invalid input. Please check your command again.')
        cmd = input('Commands [y/n]')
        if cmd == 'y':
            usage()
    print('')
