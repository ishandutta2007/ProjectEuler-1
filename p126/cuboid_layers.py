# cuboid_layers.py
# For any given cuboid (e.g. 3x2x1 prism), there is a minimum number of single
# cubes needed to cover each face, call it n1. n2 is the min number of cubes
# to cover the resulting cuboid, and so on and so forth. Taking every number n1,
# n2, .. across all integral cuboids, what is the first number that appears 1000# times?

import sys, operator, time

def sortByColumn (bigList, *args):
    bigList.sort(key=operator.itemgetter(*args))
    return bigList

# A prism face is a rectangle defined by its 4 coordinate vertices
# 2 diagonal vertices are needed to define it uniquely, as the others can be
# deduced
class face:
    def __init__ (self, pt1, pt2):

        # Checks if a valid face vertex set. If two coordinates are the same
        # it is not
        if len(pt1) != len(pt2):
            print "different coordinate lengths. Not valid"
            sys.exit()
        if sum([1 for i in range(len(pt1)) if pt1[i] == pt2[i]]) >= len(pt1)-1:
            print "Not a valid face. Vertex set are not diagonals."
            sys.exit()

        # Determine the other two vertices, and then sort them by coordinate
        pt3, pt4 = [], []
        flag = 0
        for i in range(len(pt1)):
            if pt1[i] == pt2[i]:
                pt3.append(pt1[i])
                pt4.append(pt1[i])
            else:
                if flag == 0:
                    pt3.append(pt1[i])
                    pt4.append(pt2[i])
                    flag = 1
                elif flag == 1:
                    pt3.append(pt2[i])
                    pt4.append(pt1[i])
        self.vertex_list = [pt1, pt2, pt3, pt4]
        self.vertex_list = [tuple(x) for x in self.vertex_list]
        self.vertex_list = sortByColumn (self.vertex_list, *range(len(pt1)))

    def __eq__ (self, other):
        return (self.vertex_list == other.vertex_list)

    # Returns the index of the opposite vertex from vertex_list[index]
    def calc_opposite_vertex (self, index):

        # Finds the opposite point from vertex_list[0] on face1
        for i in range(len(self.vertex_list)):
            if i == index:
                continue
            
            test_len = sum([1 for j in range(len(self.vertex_list[index]))
                            if self.vertex_list[index][j] ==
                            face1.vertex_list[i][j]])
            
            if test_len == len(self.vertex_list[index]) - 2:
                return i
            
    # Count number of same components in two vertices of the face
    def count_same_components (self, index1, index2):
        test_len = sum([1 for j in range(len(self.vertex_list[index1]))
                        if self.vertex_list[index1][j] ==
                        self.vertex_list[index2][j]])
        return test_len
        
# Unit cube in a region of Cartesian coordinate space
# In this case, we will define a cube by two of its faces
# From there, the program will deduce the other four faces
class cube:
        
    def __init__ (self, face1, face2):

        self.calc_opposite_face (face1, face2) # calculates a face and its opposite
        self.calc_vertex_list()  # calculates full vertex list
        self.calc_face_list ()

    # Yields two opposite faces of the cube
    def calc_opposite_face (self, face1, face2):

        # Determine if face1 and face2 are opposite faces
        # If not, calculate the opposite face to face1
        face1_set, face2_set = set(face1.vertex_list), set(face2.vertex_list)
        intersect_set = (face1_set.intersection (face2_set))
        
        if len(intersect_set) > 0: # not opposite faces, adjacent ones
            intersect_pt = intersect_set.pop()

            intersect_index = face2.vertex_list.index (intersect_pt)
          
            for i in range(len(face2.vertex_list)):
                if i == intersect_index or face2.vertex_list[i] in intersect_set:
                    continue
                
                test_len = sum([1 for j in range(len(face2.vertex_list[i]))
                                if face2.vertex_list[i][j] ==
                                face2.vertex_list[intersect_index][j]])
                if test_len == len(face2.vertex_list[i]) - 1:
                    test_index = i
                    break
                
            opposite_diff = [face2.vertex_list[test_index][i] -
                             face2.vertex_list[intersect_index][i] for i in
                             range(len(face2.vertex_list[0]))]
            
            opp_index = face1.calc_opposite_vertex (0)
            
            opp_pt1 = tuple([face1.vertex_list[0][i] + opposite_diff[i]
                             for i in range(len(face1.vertex_list[0]))])
            opp_pt2 =  tuple([face1.vertex_list[opp_index][i] + opposite_diff[i]
                             for i in range(len(face1.vertex_list[opp_index]))])
          
            face1_opposite = face (opp_pt1, opp_pt2)
            
        else: # opposite faces, so just set equal and calc opposite_diff
            face1_opposite = face2
            test_vertex = face1.vertex_list[0]
            for vert_opp in face1_opposite.vertex_list:
                test_len = sum([1 for i in range(len(vert_opp))
                            if vert_opp[i] == test_vertex[i]])
                if test_len == len(vert_opp) - 1:
                    opp_vertex = vert_opp
                    break
            opposite_diff = [opp_vertex[i] - test_vertex[i] for i in range(len(opp_vertex))]

        self.face_ex = face1
        self.face_ex_opposite = face1_opposite
        self.face_opp_diff = opposite_diff
        
    # Calculates and sorts all vertices of the cube
    def calc_vertex_list (self):
        self.vertex_list = self.face_ex.vertex_list + self.face_ex_opposite.vertex_list
        self.vertex_list = sortByColumn (self.vertex_list, *range(len(self.vertex_list[0])))

    # Calculates all six faces of the cube
    def calc_face_list (self):
        face_vertices = self.face_ex.vertex_list
        opposite_diff = self.face_opp_diff

        # Arrange face_vertices in a 'clockwise' order
        face_len = 4
        possible_indices = range(face_len)
        face_new_list = []
        face_new_list.append (face_vertices[0])
        possible_indices.remove(0)
        if self.face_ex.count_same_components (0, 1) == len(self.face_ex.vertex_list[0]) - 1:
            face_new_list.append (face_vertices[1])
            possible_indices.remove(1)
        else:
            face_new_list.append (face_vertices[2])
            possible_indices.remove(2)
        next_index = self.face_ex.calc_opposite_vertex (0)
        face_new_list.append (face_vertices[next_index])
        possible_indices.remove(next_index)
        
        final_index = possible_indices[0]
        face_new_list.append (face_vertices[final_index])
        
        face_opp_list = []
        for vertex in face_new_list:
            opp_vertex = [vertex[i] + opposite_diff[i] for i in range(len(vertex))]
            face_opp_list.append (opp_vertex)


        self.face_list = []
        for i in range(face_len):
            if i < face_len - 1:
                self.face_list.append (face (face_new_list[i], face_opp_list[i+1]))
            else:
                self.face_list.append (face (face_new_list[i], face_opp_list[0]))
                
        self.face_list += [self.face_ex, self.face_ex_opposite]

        
        

        
        
        
start_time = time.time()            
face1 = face((0,0,0), (1,1,0))

face2 = face((0,0,1), (1,1,1))

cube_test = cube (face1, face2)

print time.time() - start_time


    
