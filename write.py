import csv
import networkx as nx
import datetime

def writeTravelHistory(obs, filename):
    '''
        Write everyone's travel history into a .csv file.
    '''
    filename = str(filename)+'-travel.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for i in range(len(obs.people)):
            writer.writerow(obs.people[i].travel_history)


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


def writeVaccinePassport(obs, filename):
    '''
    Write vaccination record per person.

    parameter
    ---------
    obs: Simulation
        Accepts Simulation object
    filename: str
        File name for export
    '''
    filename = str(filename) + '-vaccination.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for i in range(len(obs.people)):
            writer.writerow(obs.people[i].vaccine_history)


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

        Note
        ----
        Columns
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


def WriteNetworkAvgDegree(graph_obj, filename):
    '''
    Argument
    --------
    graph_obj: Graph
        The graph to be calculated.
    filename: str
        Output filename.
    '''
    filename = filename+'-nwk-deg.csv'
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow([2 * graph_obj.number_of_edges()/graph_obj.number_of_nodes()])


def WriteNetworkAvgDegree_I(graph_obj, filename):
    '''
    Argument
    --------
    graph_obj: Graph
        The graph to be calculated.
    filename: str
        Output filename.
    '''
    filename = filename+'-nwk-deg_I.csv'
    deg_I = {}
    for node in graph_obj.nodes():
        if node.suceptible == 1:
            deg_I[node] = graph_obj.degree[node]
    content = [v for v in deg_I.values()]
    try: content.append(sum(content)/len(content))
    except ZeroDivisionError: content.append(0)
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(content)


def WriteNetworkAvgDegree_S(graph_obj, filename):
    '''
    Argument
    --------
    graph_obj: Graph
        The graph to be calculated.
    filename: str
        Output filename.

    Note
    ----
    This include the average degree of people whom vaccinated.
    '''
    filename = filename+'-nwk-deg_S.csv'
    deg_S = {}
    for node in graph_obj.nodes():
        if node.suceptible == 0 and node.removed == 0:
            deg_S[node] = graph_obj.degree[node]
    content = [v for v in deg_S.values()]
    try: content.append(sum(content)/len(content))
    except ZeroDivisionError: content.append(0)
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(content)


def WriteNetworkAssortativity(graph_obj, filename):
    '''
    Argument
    --------
    graph_obj: Graph
        The graph to be calculated.
    filename: str
        Output filename.
    '''
    filename = filename+'-nwk-assort.csv'
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow([nx.degree_assortativity_coefficient(graph_obj)])


def WriteNodeBetweeness(graph_obj, filename):
    '''
    Write node betweeness.

    Parameters
    ----------
    graph_obj: Graph
        The graph to be calculated.
    filename: str
        Output filename.
    '''
    filename = filename + '-nwk-btwn.csv'
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow([v for k, v in nx.algorithms.centrality.betweenness_centrality(graph_obj).items()])


def WriteNodeBetweeness_I(graph_obj, filename):
    '''
        Write node betweeness of the infected.

        Parameters
        ----------
        graph_obj: Graph
            The graph to be calculated.
        filename: str
            Output filename.
    '''
    filename = filename + '-nwk-btwn_I.csv'
    btwn_I = {}
    btwn = nx.algorithms.centrality.betweenness_centrality(graph_obj)
    for node in graph_obj.nodes():
        if node.suceptible == 1 and node.removed == 0:
            btwn_I[node] = btwn[node]
    content = [b for b in btwn_I.values()]
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(content)


def WriteNodeBetweeness_S(graph_obj, filename):
    '''
        Write node betweeness of the susceptible.

        Parameters
        ----------
        graph_obj: Graph
            The graph to be calculated.
        filename: str
            Output filename.
    '''
    filename = filename + '-nwk-btwn_S.csv'
    btwn_S = {}
    btwn = nx.algorithms.centrality.betweenness_centrality(graph_obj)
    for node in graph_obj.nodes():
        if node.suceptible == 0 and node.removed == 0:
            btwn_S[node] = btwn[node]
    content = [b for b in btwn_S.values()]
    with open(filename, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(content)


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
        contents = [' ========================================== \n\n',' ',' Agent Based Modelling: COVID-19 SEIP Model \n\n',' ','========================================== \n']
        contents.append('\n\nThis simulation was performed on {}.\n\n'.format(datetime.datetime.now().strftime('%H:%M:%S, %d/ %m/ %Y')))
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
        contents.append('Test rate: {} \n'.format(obs.test_rate))
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
        if 15 in obs.modes:
            contents.append('\n# Vaccine \n')
            contents.append('\nCustom vaccine parameters: \n\n')
            for vaccine in obs.epidemic.vaccine_ls:
                # Not to check type as it will show what went wrong. Let the epidemic class to handle this.
                for k,v in vaccine.__dict__.items():
                    contents.append(f'{k}: {v}\n')
                contents.append('\n')
        if any(i in obs.modes for i in [5, 51, 52, 53, 54, 501, 505]):
            contents.append('\n# Network Topology \n')
            if 51 in obs.modes:
                nwk_type = "Erdos-Renyi"
            elif 52 in obs.modes:
                nwk_type = "Barabasi-Albert"
            elif 53 in obs.modes:
                nwk_type = "Watts-Strogatz"
            elif 54 in obs.modes:
                nwk_type = "Lattice"
            else:
                nwk_type = "Custom"
            contents.append('Type: {}\n\n'.format(nwk_type))
            contents.append('\n## Basic Network Quantities \n')
            contents.append('Nodes: {}\n'.format(obs.contact_nwk.nwk_graph.number_of_nodes()))
            contents.append('Edges: {}\n'.format(obs.contact_nwk.nwk_graph.number_of_edges()))
            contents.append('Avg degree: {}\n'.format(2 * obs.contact_nwk.nwk_graph.number_of_edges()/obs.contact_nwk.nwk_graph.number_of_nodes()))
            contents.append('Assortativity: {}\n'.format(nx.degree_assortativity_coefficient(obs.contact_nwk.nwk_graph)))
            if obs.contact_nwk.update_rule != None:
                contents.append('\n## Longitudinal network \n')
                if obs.contact_nwk.update_rule == 'random':
                     contents.append('Type: Independent\n')
                     contents.append('Probability to bond (l0): {}\n'.format(obs.contact_nwk.l0))
                     contents.append('Probability to debond (l1): {}\n'.format(obs.contact_nwk.l1))
                elif obs.contact_nwk.update_rule == 'XBS':
                    contents.append('Type: XBS\n')
                    contents.append('Rewire probability: {}\n'.format(obs.contact_nwk.PUpdate))
                    contents.append(f'Rewire type: {"Assortative" if obs.contact_nwk.assort else "Disassortative"}\n')
                contents.append('Average degree per time step stored in "{}-nwk-deg.csv"\n'.format(obs.filename))
                contents.append('Assortativity information per time step stored in "{}-nwk-assort.csv"\n'.format(obs.filename))
            if any(i in obs.modes for i in [501, 505]):
                contents.append('\n## Initial Infection \n')
                if 501 in obs.modes:
                    contents.append('Initial infection: {}\n\n'.format(obs.modes[501].init_infection))
                if 505 in obs.modes:
                    contents.append('By: {}\n\n'.format(obs.modes[505].mode))
        if 2 in obs.modes:
            contents.append('\n# Overseas travel \n')
            contents.append('  Location\tBeta\tIsolation\tReturn prob\t\n')
            contents.append('  --------\t----\t---------\t-----------\n')
            for loc, b in obs.modes[2].overseas.items():
                contents.append(f'  {loc}\t{b}\t{obs.modes[2].overseasIsolation[loc]}\t{obs.modes[2].return_prob[loc]} \n')
            contents.append(f'Isolation period: {obs.modes[2].isolationPeriod} \n')
            contents.append('\n## Local implementation \n')
            if obs.modes[2].localIsolation:
                contents.append(f'Isolation period: {obs.modes[2].isolationPeriod} \n')
            else:
                contents.append(f'Isolation period: 0 \n')
            contents.append('\n## Game Theoretical Attributes \n')
            contents.append(f'rI: {obs.modes[2].rI} \n')
            contents.append(f'rS: {obs.modes[2].rS} \n\n')
            contents.append(f'Travel prob: {obs.modes[2].travel_prob} \n')
            contents.append(f'Return prob: \n')
            contents.append('  Location\tReturn prob\n')
            for loc, b in obs.modes[2].overseas.items():
                contents.append(f'  {loc}\t{obs.modes[2].return_prob[loc]} ')

        if any(m in obs.modes for m in [21, 22, 23, 24]):
            contents.append('\n# Opinion Dynamics \n')
            contents.append(f'\nGroup size: {obs.info_nwk.size}\n')
            if 21 in obs.modes:
                contents.append('Local majority rule in place. ')

            if any(m in obs.modes for m in [22, 23, 24]):
                contents.append('\n## Personality \n')
                if 22 in obs.modes:
                    contents.append('Stubbonly support vaccination')
                    contents.append(f'\n\tProportion: {obs.modes[22].InflexProProportion}\n')
                if 23 in obs.modes:
                    contents.append('Stubbonly against vaccination')
                    contents.append(f'\n\tProportion: {obs.modes[23].InflexAgProportion}\n')
                if 24 in obs.modes:
                    contents.append('Balancers in groups')
                    contents.append(f'\n\tProportion: {obs.modes[24].BalancerProportion}\n')

        contents.append('\n\n# Notes\n')
        if 2 in obs.modes:
            contents.append('* Reward for travel: rI\n')
            contents.append('* Reward for not to travel: rS\n')

        contents.append('\n## COVID-19 Information\n')
        contents.append('Please see https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7270519/ for compartment. The actual compartment model is described in https://github.com/lt-shy-john/covid19-vaccine-game-theory/blob/main/report/report.pdf. ')
        if any(i in obs.modes for i in [1, 7, 8, 10, 11, 14]):
            contents.append('* Epidemic parameter controlled by optional modes. Consult the relevant modes for more information. \n')
        f.writelines(contents)
