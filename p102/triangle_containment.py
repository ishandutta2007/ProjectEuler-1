# triangle_containment.py
# Given 3 points in the xy plane, determine if the
# origin (0,0) is contained within the triangle they generate

# Given 2 points, return coefficients A,B, and C such that
# Ax + By = C
def generate_line_abc (pt1, pt2):
    x1, x2 = pt1[0], pt2[0]
    y1, y2 = pt1[1], pt2[1]

    if x2 ==  x1:
        return (1, 0, x1)   # line is of form x = constant
    
    m = (y2-y1) / (x2-x1 + 0.0) # slope of line, non-zero denominator
    return (-1 * m, 1, y1 - m * x1)

# Given a line, by its (A,B,C) coordinates, and a point, determine if that
# point, plugged into the line's equation, comes out > C (+1), = C (0), or
# < C (-1)

def point_line_position (line_parameters, vertex):
    A,B,C = line_parameters[0],  line_parameters[1],  line_parameters[2]
    x, y = vertex[0], vertex[1]

    if (A*x + B*y > C):
        return 1
    if (A*x + B*y == C):
        return 0
    return -1

# Checks if the origin and the given vertex are on the same side
# of the line (determined by the other 2 vertices)
# If true for all 3 lines, then the triangle contains the origin

def origin_same_plane_vertex (line_parameters, vertex):

    origin = (0,0)

    return point_line_position (line_parameters, vertex) * point_line_position (line_parameters, origin)

# uses the vertices to generate the lines associated w each triangle side
# then checks if origin on same side of line as opposite vertex for all lines
def origin_in_triangle (vertex_list):

        line_list = []
        for i in range (0, len(vertex_list)):
            line_vertices = []
            for j in range (0, len(vertex_list)):
                if i != j:
                    line_vertices.append (vertex_list[j])
            line_list.append (generate_line_abc (line_vertices[0], line_vertices[1]))
        for i in range(0, len(vertex_list)):
            if origin_same_plane_vertex (line_list[i], vertex_list[i]) != 1:
                return 0
        return 1
                              
                              

    
input_file = "triangles.txt"
num_coordinates = 2
origin_count = 0
with open (input_file, 'r') as f:
    for line in f:
        x1 = line.split(',')
        vertex_list = []
        for i in range (0, len(x1), num_coordinates):
            vertex_list.append((int(x1[i]), int(x1[i+1])))

        if origin_in_triangle (vertex_list):
            origin_count += 1
print origin_count
                        
        
        
        
