import math
import itertools
import copy
import networkx as nx
import seaborn as sb
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy


def mainfunct(num_simulations):
    nodeList = []

    # Initialise node and edge numbers
    node_num = random.randint(2, 20)

    nodeList.append(node_num)
    # Generate graph
    G = nx.cycle_graph(n=node_num)
    # Remove selfloops
    G.remove_edges_from(nx.selfloop_edges(G))
    nx.draw(G, with_labels=True)
    plt.show()

    # Set of nodes
    V = list(G.nodes)
    # Set of edges
    E = list(G.edges)
    # Number of opinions in graph is same as number of nodes as each node has a different opinion.
    N = len(V)
    print('Number of nodes considered:')
    print(N)
    print('')

    # Laplacian matrix. L = D - A
    L = nx.laplacian_matrix(G).toarray()

    # Adjacency matrix
    A = nx.adjacency_matrix(G)
    A = A.todense()

    # Compute Degree matrix from Laplacian and adjacency matrix
    D = L + A
    # The mean hitting time of a regular random walk to node j on graph
    # G, when the walk is initialized at node i (L. Lovasz, “Random walks on graphs: A survey,” Combinatorics, 1993.):
    # Denote D^(-1/2) dot A dot D^(-1/2) as 'M'

    M = scipy.linalg.fractional_matrix_power(D, -0.5).dot(A).dot(scipy.linalg.fractional_matrix_power(D, -0.5))

    # Calculate eigenvectors and eigenvalues of AoverD
    eigenvaluesM, eigenvectorsM = np.linalg.eig(M)

    # Get second largest eigenvalue for M:
    eigenvaluesList = eigenvaluesM.tolist()
    try:
        sortedEigenvaluesList = sorted(eigenvaluesList)
    except TypeError:
        sortedEigenvaluesList = sorted(eigenvaluesList, key=abs)
    lambda_2 = sortedEigenvaluesList[-2]
    print(D)
    # Get diagonal of D matrix:
    diagonalofD = np.diag(D)
    # Get reciprocals of diagonalofD
    inverseDiagonalD = scipy.linalg.fractional_matrix_power(D, -1)
    print(inverseDiagonalD)

    # Compute the expected number of iterations required for convergence to a particular opinion. Result is a matrix
    expectedConvergenceTimes = math.e * (N**2) * np.log(N + 2)


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

    def run_multiple_instances_changed_algorithm(graph):
        outerCountList = []
        randomNodePickedList = []
        opinionsBeforeConvergenceList = []
        saveOpinionBeforeCovergenceDefiniteList = []
        opinionsAfterConvergenceList = []
        try:
            # Colours / Opinions of all nodes. different colours demonstrate different opinions
            opinion = np.random.rand(graph.number_of_nodes(),3)
            opinionsBeforeConvergenceList.append(opinion)
            saveOpinionBeforeCovergenceDefinite = copy.deepcopy(opinionsBeforeConvergenceList)
            saveOpinionBeforeCovergenceDefiniteList.append(saveOpinionBeforeCovergenceDefinite)

            count = 0
            while True:
                # select a random node from list of nodes
                random_node_picked = list(graph.nodes)[np.random.randint(0, graph.number_of_nodes())]
                randomNodePickedList.append(random_node_picked)

                # Generate list of neighbours of random node
                list_of_neighbours = list(graph.neighbors(random_node_picked))

                # randomly choose a neighbour from list of neighbours
                chosen_neighbour = list_of_neighbours[np.random.randint(0, len(list_of_neighbours))]

                # The random node picked copies the opinion of randomly picked neighbour. Update as follows:
                opinion[random_node_picked] = opinion[chosen_neighbour]

                if check_for_convergence(opinion) is True:
                    outerCountList.append(count)
                    break
                elif check_for_convergence(opinion) is False:
                    count = count + 1
            opinionsAfterConvergenceList.append(opinion)
        except ValueError:
            pass
        return outerCountList[0], nodeList[0], randomNodePickedList[0], saveOpinionBeforeCovergenceDefiniteList[0], \
               opinionsAfterConvergenceList[0]

    nodeNumList = []
    iterateConvergenceList = []
    randomNodePicked = []
    nodeOfConvergenceList = []
    randomWalkConvList = []
    # Run simulations for same number of nodes in random graph
    for i in range(num_simulations):
        try:
            iterate, num_nodes, random_node_picked, opinion_before_convergence, opinion_after_convergence = run_multiple_instances_changed_algorithm(graph=G)
            nodeNumList.append(num_nodes)
            iterateConvergenceList.append(iterate)
            randomNodePicked.append(random_node_picked)
            nodeOfConvergence = np.where((opinion_before_convergence[0] == opinion_after_convergence[0]).all(axis=1))
            nodeOfConvergenceList.append(nodeOfConvergence)
        except IndexError:
            pass
    nodelist = [item for (item,) in nodeOfConvergenceList]
    actualConvergentNodeList = list(itertools.chain(*nodelist))
    randomWalkConvList = [expectedConvergenceTimes] * len(actualConvergentNodeList)

    return nodeNumList, randomNodePicked, actualConvergentNodeList, iterateConvergenceList, expectedConvergenceTimes, randomWalkConvList, N


nodeNumListOuter, randomNodePickedOuter, nodeOfConvergenceListOuter, iterateConvergenceListOuter, \
expectedConvergenceTimesListOuter, randomWalkConvergenceList, num_nodes = mainfunct(num_simulations=500)

print('Random node picked each iteration:')
print(randomNodePickedOuter)
print('')
print('Node whos opinion all nodes opinions converged to at each iteration:')
print(nodeOfConvergenceListOuter)
print('')
print('Time required to converge at each iteration:')
print(iterateConvergenceListOuter)
print('')
print('Expected random walk convergence time for each iteration:')
print(randomWalkConvergenceList)
print('')
print('Expected Convergence times matrix (obtained from authors results):')
print(expectedConvergenceTimesListOuter)


sb.violinplot(x=nodeOfConvergenceListOuter, y=iterateConvergenceListOuter, label='Simulated convergence times')
plt.scatter(nodeOfConvergenceListOuter, randomWalkConvergenceList, label='Theoretical upper bound for convergence')
plt.xlabel('Final convergence of all opinions at node')
plt.ylabel('Number of iterations')
plt.title('CYCLE GRAPH: Number of simulations: 500, Number of nodes considered: %d'%num_nodes)
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2)
plt.show()