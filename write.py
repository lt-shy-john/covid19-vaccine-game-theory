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
    filename = str(filename)+'.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for i in range(len(obs.people)):
            writer.writerow([obs.people[i].group_no, obs.people[i].id, obs.people[i].opinion])

    # for i in range(len(obs)):
        # print('{} - o: {}, s: {}'.format(obs[i].id, obs[i].opinion, obs[i].suceptible))

def WriteOpinionPersonality(obs, filename):
    '''
        Write everyone's opinion into a .csv file. Their personality are flagged as well.

        Coulmns
        - Group number of the agent
        - Agent name
        - Agent's personality
            - 0 means normal
            - 1 means inflexible
            - 2 means balancer
        - Agent's opinion at time step
    '''
    filename_template = filename
    for i in range(len(obs.people)):
        filename = str(filename_template)+' '+str(i)+'.csv'
        with open(filename, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow([obs.people[i].group_no, obs.people[i].id, obs.people[i].personality, obs.people[i].opinion])
        filename = ''

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
        contents.append('N, {} people\n'.format(len(obs.N)))
        contents.append('T, {} days\n'.format(obs.T))
        contents.append('\n## Epidemiology\n')
        contents.append('Alpha, {}\n'.format(obs.alpha))
        contents.append('Beta, {}\n'.format(obs.beta))
        contents.append('Gamma, {}\n'.format(obs.gamma))
        contents.append('Delta, {}\n'.format(obs.delta))
        contents.append('Phi, {}\n'.format(obs.phi))
        contents.append('Tau, {}\n'.format(obs.test_rate))
        f.writelines(contents)
