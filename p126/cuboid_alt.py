# cuboid_alt.py
# For any given cuboid (e.g. 3x2x1 prism), there is a minimum number of single
# cubes needed to cover each face, call it n1. n2 is the min number of cubes
# to cover the resulting cuboid, and so on and so forth. Taking every number n1,
# n2, .. across all integral cuboids, what is the first number that appears 1000# times?

import sys, operator, time, math

def sortByColumn (bigList, *args):
    bigList.sort(key=operator.itemgetter(*args))
    return bigList

# If two points of same length, add their components together and return result
def ptwise_addition (pt1, pt2):
    if len(pt1) != len(pt2):
        print "Not same length"
        sys.exit()
    pt_sum = [pt1[i] + pt2[i] for i in range(len(pt1))]
    pt_sum = tuple (pt_sum)
    return pt_sum

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
    
    def __hash__ (self):
        return hash(tuple(self.vertex_list))
    
    # Returns the index of the opposite vertex from vertex_list[index]
    def calc_opposite_vertex (self, index):

        # Finds the opposite point from vertex_list[index] on face1
        for i in range(len(self.vertex_list)):
            if i == index:
                continue
            
            test_len = sum([1 for j in range(len(self.vertex_list[index]))
                            if self.vertex_list[index][j] ==
                            self.vertex_list[i][j]])
            
            if test_len == len(self.vertex_list[index]) - 2:
                return i
            
    # Count number of same components in two vertices of the face
    def count_same_components (self, index1, index2):
        test_len = sum([1 for j in range(len(self.vertex_list[index1]))
                        if self.vertex_list[index1][j] ==
                        self.vertex_list[index2][j]])
        return test_len
#----------------------------------------------------------------------        
# Unit cube in a region of Cartesian coordinate space
# In this case, we will define a cube by two of its faces
# From there, the program will deduce the other four faces
class unit_cube:
        
    def __init__ (self, pt1, pt2):

        if self.check_valid_vertices (pt1, pt2) == 0:
            sys.exit()

        self.calc_opposite_face (pt1, pt2) # calculates a face and its opposite
        self.calc_vertex_list()  # calculates full vertex list

    def __eq__ (self, other):
        return (self.vertex_list == other.vertex_list)

    def __hash__ (self):
        return hash(tuple(self.vertex_list))
    
    def check_valid_vertices (self, pt1, pt2):
        if len(pt1) != len(pt2):
            print "Different lengths, not valid vertices"
            return 0

        test_len = sum([1 for i in range(len(pt1))
                        if pt1[i] == pt2[i]])
        if test_len > len(pt1) - 3:
            print "Not valid diagonal vertices"
            return 0

        test_dist = [math.fabs(pt1[i] - pt2[i])
                         for i in range(len(pt1))]
        if test_dist != [1,1,1]:
            print "Not valid unit cube"
            return 0
                        
        return 1

    # Yields two opposite faces of the cube
    def calc_opposite_face (self, pt1, pt2):
        dim_no = len(pt1)
        if pt1[dim_no-1] < pt2[dim_no-1]:
            pt_low, pt_high = pt1, pt2
        else:
            pt_low, pt_high = pt2, pt1

        # Now, we calculate the low (bottom) face and the high (top) face
        pt_low_opposite = (pt_high[0], pt_high[1], pt_high[2]-1)
        pt_high_opposite = (pt_low[0], pt_low[1], pt_low[2] + 1)

        # component wise difference of the pts on each face
        self.face_opp_diff = (0,0,1)
        
        self.face_low = face(pt_low, pt_low_opposite)
        self.face_high = face (pt_high, pt_high_opposite)

    # Calculates and sorts all vertices of the cube
    def calc_vertex_list (self):
        self.vertex_list = (self.face_low.vertex_list +
                            self.face_high.vertex_list)
        
        self.vertex_list = sortByColumn (self.vertex_list,
                                         *range(len(self.vertex_list[0])))

    # Calculates all six faces of the cube
    def calc_face_list (self):

        # This will put face_low's vertices in "clockwise" order
        vertex_list_low = [self.face_low.vertex_list[0],
                           self.face_low.vertex_list[1]]
        if self.face_low.count_same_components(0, 2) == 1:
            vertex_list_low +=  [self.face_low.vertex_list[2],
                                 self.face_low.vertex_list[3]]
        else:
            vertex_list_low +=  [self.face_low.vertex_list[3],
                                 self.face_low.vertex_list[2]]
            
        # This puts face_high's vertices in the corresponding order
        vertex_list_high = []
        for vertex in vertex_list_low:
            vertex_list_high.append (ptwise_addition (vertex,
                                                      self.face_opp_diff))
        self.face_list = []
        face_len = 4 # by definition
        
        for i in range(face_len):
            if i < face_len - 1:
                self.face_list.append (face (vertex_list_low[i],
                                             vertex_list_high[i+1]))
            else:
                self.face_list.append (face (vertex_list_low[i],
                                             vertex_list_high[0]))  
        self.face_list += [self.face_low, self.face_high]
#------------------------------------------------------------------------------
# Collection of unit cubes, which tracks all uncovered cube faces
class cuboid:
    def __init__ (self):
        self.cube_list = []
        self.cube_set = set([])
        self.unmatched_face_set = set([])
        self.face_cube_dict = {} # maps uncovered faces to their cubes
        
    def add_cube (self, cube1):
        if cube1 in self.cube_set:
            print "Cube already in list"
            return 0
        
        self.cube_list.append (cube1)
        self.cube_set.add (cube1)
        cube1.calc_face_list()
        for cube_face in cube1.face_list:
            if cube_face in self.unmatched_face_set:
                self.unmatched_face_set.remove (cube_face)
                del self.face_cube_dict[cube_face] 
            else:
                self.unmatched_face_set.add (cube_face)
                self.face_cube_dict[cube_face] = cube1
#------------------------------------------------------------------------------
# Will take as inputs an uncovered face and its corresponding unit cube
# It will return the unit cube that will cover the face
def face_covering_cube (lone_face, face_cube):

    # This determines which plane (x,y,or z) the face wholly lives in
    test_components = zip (*lone_face.vertex_list)

    for i in range(len(test_components)):
        x = test_components[i]
        if x.count(x[0]) == len(x):
            constant_plane = i
            break
        
    # The cube's opposite face's vertices must all have a different value in the
    # constant plane than the inputted face
    # opp_diff_vector is the ptwise difference between inputted face and the
    # opposite face

    sample_vertex = lone_face.vertex_list[0]
    plane_val = sample_vertex[constant_plane]
    for cube_vertex in face_cube.vertex_list:
        if cube_vertex[constant_plane] != plane_val: # vertex is on opp face
            oth_plane_val = cube_vertex[constant_plane]
            break
    opp_diff_vector = [0] * len(sample_vertex)
    opp_diff_vector[constant_plane] = plane_val - oth_plane_val

    # By finding the opposite vertex to sample_vertex on this cube and
    # ptwise adding opp_diff_vector to that, this gives us the opposite
    # corner vertex of the desired cube
    opp_index = lone_face.calc_opposite_vertex(0)
    opp_face_vertex = lone_face.vertex_list[opp_index]
    opp_cube_vertex = ptwise_addition(opp_face_vertex, opp_diff_vector)

    return unit_cube (sample_vertex, opp_cube_vertex)
#------------------------------------------------------------------------------

# Returns a cuboid with the specified length, width and height
# One of its corners will be at coordinate (0,0,0), and the opposite corner
# will be at point (len, width, ht)
def gen_initial_cuboid (length, width, height):
    test_cuboid = cuboid()
    
    for z in range(height):
        for y in range(width):
            for x in range(length):
                test_cube = unit_cube ((x,y,z),
                                       ptwise_addition((x,y,z),(1,1,1)))
                test_cuboid.add_cube (test_cube)
    return test_cuboid
#-----------------------------------------------------------------------------
# Adds minimum cubes to cuboid such that all initially uncovered faces
# are covered. Returns the cuboid 
def cover_cuboid (cuboid_test):
    cube_count = 0
    face_set = set(cuboid_test.unmatched_face_set)

    while len(face_set) > 0:
        sample_face = (list(face_set))[0]
        sample_cube = cuboid_test.face_cube_dict[sample_face]
        new_cube =  face_covering_cube (sample_face, sample_cube)
        
        cuboid_test.add_cube (new_cube)
        
        cube_count += 1
        
        face_set = face_set.intersection (cuboid_test.unmatched_face_set)
      
    return cuboid_test, cube_count
#--------------------------------------------------------------------------

# Below functions are utility type of functions run in the main module
def surface_area (length, width, height):
    return (2 * ((length*width) + (length*height) + (width*height)))

# Calculate the maximum cuboid dimension based on the max_cube_count
# inputted. This can be solved via surface area equation
def max_dimension (max_cube_count):
    return (max_cube_count - 2) / 4

# This is the maximum initial dimension, assuming that dimension is
# non_decreasing
def max_init_dimension (max_cube_count):
    return int (((max_cube_count/6.0) ** 0.5))

def max_mid_dimension (x_val, max_cube_count):
    return int((-1 * x_val + (16*(x_val**2) + 8 * max_cube_count) ** 0.5) / 4)

# Given a cuboid of dimensions inputted, this calculates the number of
# cube additions needed to cover the cuboid and adds it to the dictionary
# It then does the same for the resulting cuboid (next layer) until the
# number exceeds max_cube_count
def layer_cube_count (length, width, height, freq_dict, max_cube_count,
                      target_freq, target_list):
    cube_count = 0
    cuboid1 = gen_initial_cuboid (length, width, height)
    cuboid1, cube_count = cover_cuboid (cuboid1)
    diff_list = [0]
    if cube_count < max_cube_count:

        freq_dict, target_list = track_cube_count (cube_count, freq_dict,
                                                       target_freq, target_list)
        prev_cube_count = cube_count
        cuboid1, cube_count = cover_cuboid (cuboid1)
        diff_list.append (cube_count - prev_cube_count)
        
    new_diff = diff_list[-1]
    while cube_count < max_cube_count:

        freq_dict, target_list = track_cube_count (cube_count, freq_dict,
                                                   target_freq, target_list)
        new_diff += 8
        cube_count += new_diff
    return freq_dict, target_list

def layer_alt_count (length, width, height, freq_dict, max_cube_count,
                      target_freq, target_list):
    cube_count = surface_area (length, width, height)
    if cube_count < max_cube_count:
        freq_dict, target_list = track_cube_count (cube_count, freq_dict,
                                               target_freq, target_list)
    else:
        return freq_dict, target_list

    next_diff = 4 * (length + width + height)
    cube_count += next_diff

    while cube_count < max_cube_count:
        freq_dict, target_list = track_cube_count (cube_count, freq_dict,
                                               target_freq, target_list)
        next_diff += 8
        cube_count += next_diff

    return freq_dict, target_list

def track_cube_count (cube_count, freq_dict, target_freq, target_list):

    if cube_count in freq_dict:
        freq_dict[cube_count] += 1
        if cube_count in set(target_list):
            target_list.remove(cube_count)
        if freq_dict[cube_count] == target_freq:
            target_list.append (cube_count)
            
    else:
        freq_dict[cube_count] = 1
            
    return freq_dict, target_list

def main():    
    start_time = time.time()            
    freq_dict, target_list = {}, []
    max_cube_count = 20000
    target_freq = 1000

    for x in range(1, max_init_dimension (max_cube_count)):
        for y in range(x, max_mid_dimension (x, max_cube_count)):
            for z in range (y, max_dimension (max_cube_count)):
                if surface_area (x,y,z) > max_cube_count:
                    break
                freq_dict, target_list = layer_alt_count (x, y, z, freq_dict,
                                                           max_cube_count,
                                                           target_freq,
                                                           target_list)  
    print min(target_list)

    print time.time() - start_time

main()

    
