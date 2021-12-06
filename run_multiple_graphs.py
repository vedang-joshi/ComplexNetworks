import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import itertools

# If all opinions are the same then opinions have converged:
def check_for_convergence(opinionList):
    resultsList = []
    result_r_row = np.all(opinionList[:, 0] == opinionList[:, 0][0])
    resultsList.append(result_r_row)
    result_g_row = np.all(opinionList[:, 1] == opinionList[:, 1][0])
    resultsList.append(result_g_row)
    result_b_row = np.all(opinionList[:, 2] == opinionList[:, 2][0])
    resultsList.append(result_b_row)

    # Gives true if all values in resultList are True else return False
    convergence_result = all(resultsList)

    return convergence_result


def run_multiple_instances_changed_algorithm():
    outerCountList = []
    # Initialise node and edge numbers
    node_num = random.randint(2, 20)

    edge_num = node_num * 2


    # Generate graph and remove selfloops
    G = nx.gnm_random_graph(n=node_num, m=edge_num, seed=10, directed=False)
    G.remove_edges_from(nx.selfloop_edges(G))
    my_pos = nx.spring_layout(G, seed=10)
    # Colours / Opinions of all nodes. different colours demonstrate different opinions
    opinion = np.random.rand(G.number_of_nodes(),3)
    count = 0
    try:
        while True:
            # select a random node from list of nodes
            random_node_picked = list(G.nodes)[np.random.randint(0, G.number_of_nodes())]

            # Generate list of neighbours of random node
            list_of_neighbours = list(G.neighbors(random_node_picked))

            # randomly choose a neighbour from list of neighbours
            chosen_neighbour = list_of_neighbours[np.random.randint(0, len(list_of_neighbours))]

            # The random node picked copies the opinion of randomly picked neighbour. Update as follows:
            opinion[random_node_picked] = opinion[chosen_neighbour]

            if check_for_convergence(opinion) is True:
                outerCountList.append(count)
                break
            elif check_for_convergence(opinion) is False:
                count = count + 1
    except ValueError:
        pass
    return outerCountList, node_num


nodeNumList = []
iterateConvergenceList = []
for i in range(1000):
    iterate, num_nodes = run_multiple_instances_changed_algorithm()
    nodeNumList.append(num_nodes)
    iterateConvergenceList.append(iterate)

newIterateConvergenceList = list(itertools.chain(*iterateConvergenceList))
print(newIterateConvergenceList)
print(nodeNumList)
sb.violinplot(nodeNumList, newIterateConvergenceList)
plt.title('Voter algorithm for multiple node values for 1000 simulations')
plt.xlabel('Nodes in graph')

plt.ylabel('Iteration/Time required for opinions to converge')
plt.show()