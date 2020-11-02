# Import libraries
import sys
import time

# Import class files
from person import Person
from simulation import Simulation
import mode
from contact import ContactNwk

'''
Main code

- cmd functions
- main loop
'''
def setting(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T, test_rate, immune_time):
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
    cmd = input('Other parameters? [y/n]')
    if cmd == 'y':
        N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate = setting_other(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate)
    population = Person.make_population(N)
    return N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time

def setting_other(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time):
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
    return N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time

def summary():
    print('N: {}'.format(N))
    print('T: {}'.format(T))
    print('===== SIR Rate =====')
    print('alpha: {}'.format(alpha))
    print('beta: {}'.format(beta))
    print('gamma: {}'.format(gamma))
    print('phi: {}'.format(phi))
    print('delta: {}'.format(delta))
    cmd = input('Show other epidemic paremeters? [y/n] ')
    if cmd == 'y':
        print('alpha_V = {}'.format(alpha_V))
        print('alpha_T = {}'.format(alpha_T))
        print('immune time = {}'.format(immune_time))
        print('test rate: {}'.format(test_rate))
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
    print('N - Number of simulated agents.')
    print('T - Time steps/ period of simulation.')
    print('Alpha - Adoption of vaccination/ PrEP (willingness).')
    print('Beta - Infection rate.')
    print('Gamma - Recovery rate.')
    print('Delta - Removal rate.')
    print('Phi - Protection wear off rate.')
    print('Delta - Removal rate.')
    print('Tau - COVID-19 Testing rate. ')

def help():
    print('LOOK - View partner network.')
    print('MODE - Change mode settings.')
    print('RUN/ START - Start the simulation.')
    print('SETTING - Set simulation settings.')
    print('OTHER SETTING - Set auxillary simulation parameters.')
    print('SUMMARY - Print the simulation parameters.')
    print('QUIT/ Q - Quit the software.')

def usage():
    print('Usage: python3 main.py (N) (T) (alpha) (beta) (gamma) (phi) (delta) ...\n\
    [-m  <modes_config>] [-f (filename)] [run]\n')
    print('-immune_time \t Immune time after recovered, in days.')
    print('-test_rate \t COVID-19 testing rate.')
    print('-m \t\t Mode')
    print('    --1 \t Living in city/ rural.')
    print('    --2 \t Travelled back from overseas.')
    print('    --4 \t Bounded rationality of vaccine.')
    print('    --5 \t Edit contact network.')
    print('    --7 \t Age distribution.')
    print('    --8 \t Gender distribution.')
    print('    --10 \t Type of vaccine.')
    print('    --11 \t Stop transmissability/ reduce severity.')
    print('    --12 \t Cost of vaccine.')
    print('    --13 \t Accessibility to vaccine.')
    print('    --14 \t Side effects of vaccine.')
    print('    --20 \t Intimacy game.')
    print('    --21 \t Local majority rule.')
    print('    --22 \t Stubbon to take vaccine.')
    print('    --23 \t Stubbon to against vaccine.')
    print('    --24 \t Contrary to social groups.')
    print('    --31 \t Medication incorporated.')
    print('    --41 \t Moral hazard of social distancing.')
    print('    --42 \t Moral hazard of treatment.')
    print('    --51 \t Erdos-Renyi topology.')
    print('    --52 \t Preferential attachment.')
    print('    --53 \t Small world network.')
    print('    --54 \t Lattice network.')
    print('-f \t\t Export file name.')
    print('-h \t\t Usage.')
    print('run \t\t Run simulation, last argument.')

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
        print('Select the following options:')
        print('01: Living in city/ rural [{}]'.format(mode01.flag))
        print('02: Travel from overseas [{}]'.format(mode02.flag))
        print('04: Bounded rationality of vaccine [{}]'.format(mode04.flag))
        print('05: Edit contact network')
        print('07: Age distribution [{}]'.format(mode07.flag))
        print('08: Gender population [{}]'.format(mode08.flag))
        print('10: Type of vaccine [{}]'.format(mode10.flag))
        print('11: Stop transmissability/ reduce severity []')
        print('12: Cost of vaccine []')
        print('13: Accessibility to vaccine []')
        print('14: Side effects of vaccine []')
        print('20: Imitation game [{}]'.format(mode21.flag))
        print('21: Local majority rule [{}]'.format(mode21.flag))
        print('22: Stubbon to take vaccine []')
        print('23: Stubbon to against vaccine []')
        print('24: Contrary to social groups []')
        print('31: Medication incorporated [{}]'.format(mode31.flag))
        print('32: Population on demand PrEP had planned sex. []')
        print('41: Moral hazard of social distancing []')
        print('42: Moral hazard of treatment []')
        print('51: Erdos-Renyi topology [{}]'.format(mode51.flag))
        print('52: Preferential attachment [{}]'.format(mode52.flag))
        print('53: Small world topology [{}]'.format(mode53.flag))
        print('54: Lattice network [{}]'.format(mode54.flag))
        print('Input number codes to change the options.')
        mode_input = input('> ')
        print(mode_input)
        mode = mode_settings(mode_input, mode)
        cmd = input('Return to main menu? [y/n] ')
    return mode

def mode_settings(cmd, mode=None):
    cmd = cmd.split(' ')
    if cmd == ['']:
        # If empty response, then leave prematurely.
        return mode
    rv_modes = []
    if '-dp' in cmd:
        removal_idx = cmd.index('-dp')
    print('Adding: ')
    if '-dp' in cmd:
        print(cmd[:removal_idx])
        print('Removing')
        print(cmd[removal_idx+1:])

        rv_modes = cmd[removal_idx+1:]
        cmd = cmd[:removal_idx]
    else:
        print(cmd)
    if len(cmd) > 0 and '-dp' not in cmd:
        for i in range(len(cmd)):
            try:
                int(cmd[i])
            except ValueError:
                print('Wrong data type for mode, please check your inputs.')
                continue
            if int(cmd[i]) == 1:
                mode01()
                if mode01.flag == 'X':
                    mode[1] = mode01
                else:
                    mode.pop(1)
            elif int(cmd[i]) == 2:
                mode02.set_proportion()
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
            elif int(cmd[i]) == 21:
                mode21()
                if mode21.flag == 'X':
                    mode[21] = mode21
                else:
                    mode.pop(21)
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
                mode51()
                if mode51.flag == 'X':
                    mode[51] = mode51
                else:
                    mode.pop(51)
            elif int(cmd[i]) == 52:
                if (mode51.flag == 'X'):
                    print('Mode 51 has been activated. Mode 52 unable to start.')
                    break
                mode52()
                if mode52.flag == 'X':
                    mode[52] = mode52
                else:
                    mode.pop(52)
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

def find_mode(code, mode_master_list):
    for mode in mode_master_list:
        if mode.code == code:
            return mode

def export(filename):
    print('Coming soon')

print('  ==========================================  \n\n')
print('  Agent Based Modelling: COVID-19 SUEP Model  \n\n')
print('  ==========================================  ')
print()
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
    print('Using pre-defined inputs. ')
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
        print('Usage: python3 main.py (N) (T) (alpha) (beta) (gamma) (phi) (delta) ...\n[-m <modes_config>] [-f (filename)] [run]\n')
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

population = Person.make_population(N)
contact_nwk = ContactNwk(population)
filename = ''  # Default file name to export (.csv). Change when use prompt 'export' cmd.

mode_master_list = []
# All objects should add into mode_master_list
mode01 = mode.Mode01(population)
mode02 = mode.Mode02(population)
mode04 = mode.Mode04(population, alpha)
mode05 = mode.Mode05(population, contact_nwk)
mode07 = mode.Mode07(population, beta, delta)
mode08 = mode.Mode08(population, beta, delta)
mode10 = mode.Mode10(population, phi, beta)
mode20 = mode.Mode20(population, contact_nwk)
mode21 = mode.Mode21(population, contact_nwk)
mode31 = mode.Mode31(population)
mode51 = mode.Mode51(population, contact_nwk)
mode52 = mode.Mode52(population, contact_nwk)
mode53 = mode.Mode53(population, contact_nwk)
mode54 = mode.Mode54(population, contact_nwk)

mode_master_list = [mode01, mode02, mode04, mode05, mode07, mode08,
mode10,
mode20, mode21,
mode31,
mode51, mode52, mode53, mode54]


modes = {}

'''
Express mode

Loads the settings prior to the run. Optional keyword 'run' to run the simulation automatically.
'''

# Check if mode exists
for i in range(len(sys.argv)):
    try:
        if sys.argv[i] == '-immune_time':
            immune_time_temp = sys.argv[i+1]
            immune_time = set_correct_para(immune_time_temp, immune_time, pos=True)
        elif sys.argv[i] == '-test_rate':
            test_rate_temp = sys.argv[i+1]
            test_rate = set_correct_para(test_rate_temp, test_rate, pos=True)
        elif sys.argv[i] == '-m':
            for j in range(i+1,len(sys.argv)):
                # Skip at other options
                if sys.argv[j][:2] == '--':
                    mode_flag = int(sys.argv[j][2:])
                    print('Loading mode: {}'.format(mode_flag))

                    # Activate modes with no options needed
                    if mode_flag == 4:
                        mode04()
                    elif mode_flag == 51:
                        if 52 in modes:
                            print('Mode 52 has been activated. Ignore mode 51. ')
                            break
                        mode51()
                        if mode51.flag == 'X':
                            modes[51] = mode51
                        else:
                            modes.pop(51)
                    # elif mode_flag == 52:
                    #     if 51 in modes:
                    #         print('Mode 51 has been activated. Ignore mode 52. ')
                    #         break
                    #     mode52()
                    #     if mode52.flag == 'X':
                    #         modes[52] = mode52
                    #     else:
                    #         mode.pop(52)

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
                                mode.pop(7)
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
                                mode.pop(8)
                        elif mode_flag == 52:
                            if 51 in modes:
                                print('Mode 51 has been activated. Ignore mode 52. ')
                                break
                            if sys.argv[k][:3] == '*m=':
                                mode52_m_config = int(sys.argv[k][3:])
                                mode52.set_m(mode52_m_config)
                            mode52.set_network()
                            mode52.raise_flag()
                            if mode52.flag == 'X':
                                modes[52] = mode52
                            else:
                                mode.pop(52)


                        # elif mode_flag == 999:
                        #     # There are 3 args with last one characters
                        #     seven_config(*[int(data) if data.isnumeric() else data for data in config])
                    continue
                if sys.argv[j][0] == '-' and sys.argv[j][1].isalpha():
                    break
                if sys.argv[j] == 'run':
                    break
                # print(mode_flag, '*'+str(argv[j]))
    except ValueError:
        print('Invalid input. Check your arguments. ')
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

if sys.argv[-1] == 'run':
    print('===== Simulation Running =====')
    current_run = Simulation(population, T, population, contact_nwk, alpha, beta, gamma, phi, delta, filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2, test_rate, immune_time)
    # Load modes
    current_run.load_modes(modes)
    if len(modes) > 0:
        print('\nMode objects loaded.\n')
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
        N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time = setting(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time)
        population = Person.make_population(N)
    elif cmd == 'other setting':
        print('Leave blank if not changing the value(s).')
        N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time = setting_other(N, T, alpha, beta, gamma, phi, delta, alpha_V, alpha_T, phi_V, phi_T, test_rate, immune_time)
    elif cmd == 'summary':
        summary()
    elif cmd == 'look':
        show_nwk()
    elif cmd == 'help':
        help()
    elif cmd == 'start' or cmd == 'run':
        print('===== Simulation Running =====')
        current_run = Simulation(population, T, population, contact_nwk, alpha, beta, gamma, phi, delta, filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_SI2, beta_II2, beta_RI2, beta_VI2, test_rate, immune_time)
        # Load modes
        current_run.load_modes(modes)
        if len(modes) > 0:
            print('\nMode objects loaded.\n')
        # Run
        current_run()
        print('=====  Simulation Ended  =====')
    elif cmd == 'mode':
        modes = set_mode(modes)
    elif cmd == 'export':
        filename = input('File name: ')
    elif cmd == 'thank you':
        print('  ==========================================  \n\n')
        print('  Agent Based Modelling: COVID-19 SEIP Model  \n\n')
        print('  ==========================================  ')
        time.sleep(3)
        print('\n\nAuthor: Shing Hin (John) Yeung\n')
        time.sleep(1)
        print('This software code comes from Masters in Complex Systems a Capstone Project. \n')
        time.sleep(1)
        print('It aims for modelling human choice upon vaccine adoption and therefore predict the epidemic. \n\n')
        time.sleep(1)
        print('The author would like to thank you to many people who conrtibuted to this project. \n')
        time.sleep(1)
        print('Dr Shailendra Sawleshwarkar')
        print('A/ Prof Iryna Zablotska-Manos')
        print('Dr Samit Bhattacharyya')
        time.sleep(3)
        print('\n\nPrimary supervisor')
        print('Dr Mahendrarajah Piraveenan\n')
        time.sleep(3)
        print('This study dedicates to the humanity that strives in the COVID-19 pandemic. \n\n\n')
        time.sleep(1)
        print('==== Thank you ====')
    elif cmd == 'quit' or cmd == 'q':
        print('See you!')
        quit()
    else:
        print('Invalid input. Please check your command again.')
        cmd = input('Commands [y/n]')
        if cmd == 'y':
            usage()
    print('')
