import csv
import networkx as nx
import datetime

def WriteStates(obs, filename):
    '''
        Write everyone's infected state into a .csv file.
    '''
    filename = str(filename)+'.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([obs.S, obs.I, obs.V, obs.R])

def WriteCompartmentHistory (obs, filename):
    '''
        Write everyone's compartment state into a .csv file.
    '''
    filename = str(filename)+'-compartment.csv'
    for i in range(len(obs.people)):
        with open(filename, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(obs.people[i].compartment_history)

def WriteOpinion(obs, filename):
    '''
        Write everyone's opinion and infected state into a .csv file.
    '''
    filename = str(filename)+'-opinion.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for i in range(len(obs.people)):
            writer.writerow([obs.people[i].group_no, obs.people[i].id, obs.people[i].opinion])

def WriteOpinionPersonality(obs, filename):
    '''
        Write everyone's opinion into a .csv file. Their personality are flagged as well.

        Coulmns
        - Group number of the agent
        - Agent name
        - Agent's personality
            - 0 means normal
            - 1 means inflexible (pro-vaccine)
            - 2 means inflexible (against)
            - 3 means balancer
        - Agent's opinion at time step
    '''
    filename = str(filename)+'-opinion.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for i in range(len(obs.people)):
            writer.writerow([obs.people[i].group_no, obs.people[i].id, obs.people[i].opinion, obs.people[i].personality])

def WriteNetwork(graph_obj, filename):
    export_graph = graph_obj
    mapping = {}
    for node in graph_obj.nodes:
        mapping[node] = node.id
    export_graph = nx.relabel_nodes(export_graph, mapping)
    nx.write_graphml(export_graph, filename+'.graphml')

def WriteNetworkData(obs):
    '''
    Save basic network information.

    Parameters
    ----------
    obs: Simulation
        Accepts Simulation object
    filename: str
        File name for export
    '''
    text = []

    text.append('=============================\n\n')
    text.append('Condom usage\n\n')
    text.append('=============================\n\n')
    text.append('# Basic data\n\n')
    text.append('Number of agents (N): {}\n\n'.format(len(obs.N)))

def WriteTestingHistory(obs, filename):
    filename = str(filename)+'-testing.csv'
    for i in range(len(obs.people)):
        with open(filename, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(obs.people[i].test_history)

def WriteSummary(obs, filename):
    '''
    Write simulation summary.

    Parameters
    ----------
    obs: Simulation
        Accepts Simulation object
    filename: str
        File name for export
    '''
    with open('{}-summary.txt'.format(filename), 'w') as f:
        contents = [' ========================================== \n\n',' ',' Agent Based Modelling: COVID-19 SEIP Model \n\n',' ',' ========================================== \n']
        contents.append('\n\nThis simulation was performed on {}.\n\n'.format(datetime.datetime.now().strftime('%H:%M:%S, %d/ %m/ %Y (%z)')))
        contents.append('Simulation name: {}\n\n'.format(filename))
        contents.append('# Summary\n')
        contents.append('N: {} people\n'.format(len(obs.N)))
        contents.append('T: {} days\n'.format(obs.T))
        contents.append('\n## Epidemiology\n')
        contents.append('Alpha: {}\n'.format(obs.alpha))
        if any(i in obs.modes for i in [1, 7, 8]):
            contents.append('Beta: *\n')
        else:
            contents.append('Beta: {}\n'.format(obs.beta))
        contents.append('Gamma: {}\n'.format(obs.gamma))
        if any(i in obs.modes for i in [7, 8]):
            contents.append('Delta: *\n')
        else:
            contents.append('Delta: {}\n'.format(obs.delta))
        contents.append('Phi: {}\n'.format(obs.phi))
        contents.append('Tau: {}\n'.format(obs.test_rate))
        contents.append('Immune time: {} days \n'.format(obs.immune_time))
        if any(i in obs.modes for i in [7, 8]):
            contents.append('\n# Demographics \n')
            if 7 in obs.modes:
                age_backets = ['0 - 9', '10 - 19', '20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69', '70 - 79', '80 - 89', '90 - 99']
                contents.append('\n## Age factor\n')
                contents.append('\nAge group  Beta   Delta ')
                contents.append('\n---------  ----   ----- \n')
                for i in range(len(age_backets)):
                    contents.append('{}    {}  {}\n'.format(age_backets[i], obs.modes[7].beta_age[i], obs.modes[7].delta_age[i]))
            if 8 in obs.modes:
                gender = ['Male', 'Female']
                contents.append('\n## Gender factor\n')
                contents.append('\nGender  Beta   Delta ')
                contents.append('\n------  ----   ----- \n')
                for i in range(len(gender)):
                    contents.append('{}   {} {}\n'.format(gender[i], obs.modes[8].beta_gender[i], obs.modes[8].delta_gender[i]))
        if 1 in obs.modes:
            contents.append('\n# City and Rural Compartment \n')
            contents.append('Proportion living in city, {} \n'.format(obs.modes[1].weight[0]))
            contents.append('Proportion living in rural area, {} \n'.format(obs.modes[1].weight[1]))
            contents.append('\n## Transmission parameter \n')
            contents.append('City: {} \n'.format(obs.modes[1].betas[0]))
            contents.append('Rural: {} \n'.format(obs.modes[1].betas[1]))
        if any(i in obs.modes for i in [4, 21]):
            contents.append('\n# Game Theoretical Option \n')
            if 4 in obs.modes:
                contents.append('\n## Bounded Rationality \n')
                contents.append('Alpha: {}\n'.format(obs.alpha))
                contents.append('Rationality parameter: \n')
                contents.append('Append mode: Fixed \n')
                contents.append('N: {} people\n'.format(len(obs.N)))
                contents.append('Value: {} \n'.format(obs.people[0].lambda_BR))
                contents.append('P(V): {} \n'.format(obs.modes[4].P_Alpha[0]))
        if any(i in obs.modes for i in [1, 7, 8]):
            contents.append('# Notes\n')
            contents.append('* Epidemic parameter controlled by optional modes. Consult the relevant modes for more information. \n')
        f.writelines(contents)
