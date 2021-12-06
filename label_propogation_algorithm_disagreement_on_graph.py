'''
Disagreement on graphs: Label Propogation Algorithm (majority rule implementation)
'''

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import copy

nodeList = []
countList = []
opinionsBeforeConvergenceList = []
opinionsAfterConvergenceList = []
# If all opinions are the same then opinions have converged:
try:
    # Initialise node and edge numbers
    node_num = random.randint(20, 40)
    edge_num = node_num
    print(node_num)
    nodeList.append(node_num)

    # Generate graph and remove selfloops
    G = nx.gnm_random_graph(n=node_num, m=edge_num*2, seed=100, directed=False)
    G.remove_edges_from(nx.selfloop_edges(G))

    my_pos = nx.spring_layout(G, seed = 10)

    # Colours / Opinions of all nodes. different colours demonstrate different opinions
    opinion = np.random.rand(G.number_of_nodes(), 3)
    nx.draw(G, pos=my_pos, node_color=opinion, with_labels=True)
    plt.show()
    opinionsBeforeConvergenceList.append(opinion)
    saveOpinionBeforeCovergenceDefinite = copy.deepcopy(opinionsBeforeConvergenceList)

    def check_for_convergence(opinionList):
        resultsList = []
        result_r_row = np.all(opinionList[:,0] == opinionList[:,0][0])
        resultsList.append(result_r_row)
        result_g_row = np.all(opinionList[:, 1] == opinionList[:, 1][0])
        resultsList.append(result_g_row)
        result_b_row = np.all(opinionList[:, 2] == opinionList[:, 2][0])
        resultsList.append(result_b_row)

        # Gives true if all values in resultList are True else return False
        convergence_result = all(resultsList)

        return convergence_result

    count = 0
    while True:
        # select a random node from list of nodes
        random_node_picked = list(G.nodes)[np.random.randint(0, G.number_of_nodes())]

        # Generate list of neighbours of random node
        list_of_neighbours = list(G.neighbors(random_node_picked))

        # Generate list of colours of neighbours of random node
        list_of_colours_of_neighbours = np.stack([opinion[i] for i in list_of_neighbours])
        print('list of neighbour colors')
        print(list_of_colours_of_neighbours)
        # Find neighbour colours with the majority of occurences (majority rule implemented here)
        neighbour_unique_colours = np.unique(list_of_colours_of_neighbours, return_counts=True, axis=0)
        # check if all elements in unique count list are equal i.e. all opinions occur equally likely:
        #if np.all(neighbour_unique_colours[1] == neighbour_unique_colours[1][0]) is True:
            # randomly choose a neighbour from list of neighbours

            #pass
        #elif np.all(neighbour_unique_colours[1] == neighbour_unique_colours[1][0]) is False:
            #np.amax(neighbour_unique_colours[1])
        # Get index of majority of occurences of colors in neighbours colours list
        print('check below')
        list_of_indices_of_colours_to_choose_from = np.where(neighbour_unique_colours[1].tolist() == np.amax(neighbour_unique_colours[1]))[0]

        chosen_colour_list = neighbour_unique_colours[0][random.choice(list_of_indices_of_colours_to_choose_from)]
        print(chosen_colour_list)
        # Find neighbour corresponding to chosen colour
        neighbour_index = np.where(list_of_colours_of_neighbours == chosen_colour_list)[0][0]
        chosen_neighbour = list_of_neighbours[neighbour_index]
        # The random node picked copies the opinion of randomly picked neighbour. Update as follows:
        opinion[random_node_picked] = opinion[chosen_neighbour]

        if check_for_convergence(opinion) is True:
            print('Convergence of opinions occured')
            countList.append(count)
            nx.draw(G, pos=my_pos, node_color=opinion, with_labels=True)
            plt.savefig('iterate_%d.png' % count)
            break
        elif check_for_convergence(opinion) is False:
            count = count + 1
            nx.draw(G, pos=my_pos, node_color=opinion, with_labels=True)
            plt.savefig('iterate_%d.png' % count)
            plt.clf()
            print('iterate', count)

    opinionsAfterConvergenceList.append(opinion)
except ValueError:
    pass

print(nodeList)
print(countList)
print(saveOpinionBeforeCovergenceDefinite)
print(opinionsAfterConvergenceList)
