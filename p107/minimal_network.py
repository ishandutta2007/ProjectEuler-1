# minimal_network.py
# Take a graphs as input with weights. Find the minimum connected graph,
# output the "savings" by using the min graph instead of the full graph

# Opens the file and inputs the data into a list
# Replaces '-' with '0' and also converts strings to integer values
from operator import itemgetter
import time

def gather_graph_data (filename):
    graph_matrix = []
    with open(filename, 'r') as f:
        for line in f:
            x_break = line.replace ('-', '0')
            x1 = (x_break.strip()).split(',')
            x_int = [int(x) for x in x1]
            graph_matrix.append(x_int)
            
    return graph_matrix
#------------------------------------------------------------------------------
# Create dictionary listing where each vertex connects to along with the
# weight of the edge
def clean_graph_data (graph_matrix):
    vertex_dict = {}
    for i in range(len(graph_matrix)):
        vertex_list = []
        for j in range(len(graph_matrix[i])):
            if graph_matrix[i][j] != 0:
                vertex_list.append((j, graph_matrix[i][j]))
        vertex_list.sort(key = itemgetter(1))
        vertex_dict[i] = vertex_list
    return vertex_dict
#-------------------------------------------------------------------------------
# For each component in the component list, finds the lowest weighted edge
# mapping outside of it
# This edge must be part of the minimal mapping, so the joined components
# and the edge are all listed in a new component. This list of new components
# is returned
def component_grouping (component_list, vertex_dict):
    new_component_list = []
    new_component_elts = set([])
    
    for component in component_list:
        vertex_list = component[0]
        min_weight, index = 0, 0
        for vertex in vertex_list:
            if min_weight == 0:
                min_weight = vertex_dict[vertex][0][1] # list sorted by weight
                vertex2 = vertex_dict[vertex][0][0]
                vertex1 = vertex
            else:
                if vertex_dict[vertex][0][1] < min_weight:
                    min_weight = vertex_dict[vertex][0][1]
                    vertex2 = vertex_dict[vertex][0][0]
                    vertex1 = vertex

        new_edge = (min(vertex1, vertex2), max(vertex1, vertex2))

        new_component_list, new_component_elts = combine_components (new_component_list,
                                                                     new_component_elts,
                                                                     component_list,
                                                                     new_edge)

    return new_component_list, new_component_elts

# Having found the minimum weight edge, this function decides how to
# combine the components of the two vertices of that edge
def combine_components  (new_component_list, new_component_elts,
                         component_list, new_edge):
    
    vertex1, vertex2 = new_edge[0], new_edge[1]
    
    index1, index2 = 0, 0
    flag1_new, flag2_new = 0,0
    if vertex1 in new_component_elts:
        flag1_new = 1
        while vertex1 not in new_component_list[index1][0]:
            index1 += 1
    else:
        while vertex1 not in component_list[index1][0]:
            index1 += 1
    if vertex2 in new_component_elts:
        flag2_new = 1
        while vertex2 not in new_component_list[index2][0]:
            index2 += 1
    else:
        while vertex2 not in component_list[index2][0]:
            index2 += 1
            
    new_component_elts = list(new_component_elts)
    
    if (flag1_new, flag2_new) == (1,1):  # both in new_components
        comp_index1, comp_index2 = min(index1, index2), max(index1, index2)
        if comp_index1 != comp_index2:
            combined_component = add_two_components (new_component_list[comp_index1],
                                            new_component_list[comp_index2], new_edge)
            new_component_list[comp_index1] = combined_component
            del new_component_list[comp_index2]
        else:
            new_component_list[comp_index1][1].add(new_edge)
            
    if (flag1_new, flag2_new) == (1,0):
        combined_component = add_two_components (new_component_list[index1],
                                            component_list[index2], new_edge)
        new_component_list[index1] = combined_component
        new_component_elts += component_list[index2][0]

    if (flag1_new, flag2_new) == (0,1):
        combined_component = add_two_components (component_list[index1],
                                            new_component_list[index2], new_edge)
        new_component_list[index2] = combined_component
        new_component_elts += component_list[index1][0]
        
    if (flag1_new, flag2_new) == (0,0):
        combined_component = add_two_components (component_list[index1],
                                                 component_list[index2], new_edge)
        new_component_list.append (combined_component)
        new_component_elts += (component_list[index1][0] +
                               component_list[index2][0])
    
    return new_component_list, set(new_component_elts)

# This combines two components' elements and returns the result as a single component 
def add_two_components (component1, component2, new_edge):
    final_component = []
    final_component.append(component1[0] + component2[0])
    final_component.append(component1[1].union(component2[1]))
    final_component[1].add (new_edge)
    return final_component
#-------------------------------------------------------------------------------------------
# This alters the dictionary containing the vertices and weights that any given vertex
# maps to
# It mods out based on elements in the same component class. So it will only contain
# vertices that are outside of the mapped vertex's component class

def vertex_dict_component_mod (vertex_dict, component_list):

    for component in component_list:
        vertex_list = component[0]

        for vertex in vertex_list:
            prev_dict_list = vertex_dict[vertex]
            new_list = [vertex_pair for vertex_pair in prev_dict_list if vertex_pair[0]
                        not in vertex_list]
            vertex_dict[vertex] = new_list

    return vertex_dict

def calc_total_savings (graph_matrix, edge_list):
    orig_weight_sum = 0

    for vertex in graph_matrix:
        orig_weight_sum += sum(vertex)
    orig_weight_sum = orig_weight_sum / 2  # adjust for double count

    min_weight_sum = 0
    for edge_tuple in edge_list:
        min_weight_sum += graph_matrix[edge_tuple[0]][edge_tuple[1]]

    return (orig_weight_sum - min_weight_sum)


def main():
    start_time = time.time()
    filename = "network.txt"
    graph_matrix = gather_graph_data (filename)
    vertex_dict = clean_graph_data (graph_matrix)
    component_list = [[[i], set([])] for i in range(len(graph_matrix))]

    while len(component_list) > 1:    
        component_list, component_elts = component_grouping (component_list, vertex_dict)
 
        vertex_dict = vertex_dict_component_mod (vertex_dict, component_list)
        
    print calc_total_savings (graph_matrix, list(component_list[0][1]))    
    print time.time() - start_time
    
main()
