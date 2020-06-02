import bpy
import bmesh
import mathutils
import random


def AddBevelModifer():
    me = bpy.context.active_object

    me.data.use_auto_smooth = True
    # add a solidify modifier on active object
    mod = me.modifiers.new("bevel", 'BEVEL')
    mod.segments = 3
    mod.width = 0.02
    mod.limit_method = 'ANGLE'
    mod.profile = 0.7
    mod.harden_normals = True
    mod.miter_outer = 'MITER_ARC'

def VertexSlide(vertex_from, vertex_to, vertex_slide, amount):
    ans = vertex_from.co + amount*(vertex_to.co - vertex_from.co); 
    return ans

def GetLongestEdge(edges, ignore_list = []):
    longestEdge = None
    longestEdgeLength = 0
    for e in edges:
        skip = False
        
        for ing in ignore_list:
            if (ing == e):
                skip = True
                break
        
        if (skip):
            continue

        l = e.calc_length()
        if (l >= longestEdgeLength):
            longestEdgeLength = l
            longestEdge = e

    return longestEdge

def GetShortestEdge(edges, ignore_list = []):
    longestEdge = None
    longestEdgeLength = 99999999999999
    for e in edges:
        skip = False
        
        for ing in ignore_list:
            if (ing == e):
                skip = True
                break
        
        if (skip):
            continue

        l = e.calc_length()
        if (l <= longestEdgeLength):
            longestEdgeLength = l
            longestEdge = e

    return longestEdge

def GetRandomEdge(edges, ignore_list):
    while (True):        
        index = random.randint(0, len(edges) - 1)
        current_edge = edges[index]
        for edge in ignore_list:
            if (current_edge != edge):
                return current_edge 

def SubdivEdges(bm, edges, param):
    geo = []
    for edge in edges:
        vertex_to_index = edge.verts[0].index
        vertex_from_index = edge.verts[1].index
        selected_edges = [edge]
        temp = bmesh.ops.subdivide_edges(bm, edges = selected_edges, cuts = 1)
        bm.verts.ensure_lookup_table()      
        geo.append(len(bm.verts) - 1)


        vertex_to = bm.verts[vertex_to_index]
        vertex_from = bm.verts[vertex_from_index]
        vertex_to_slide = bm.verts[len(bm.verts) - 1]

        param = max(min(param, 0.8), 0.2)
        pos = VertexSlide(vertex_from, vertex_to, vertex_to_slide, param)
        bm.verts[len(bm.verts) - 1].co = pos

    bm.verts.ensure_lookup_table()
    return geo  

def IsShareVertex(edge1, edge2):
    if (edge1.verts[0] == edge2.verts[0] or edge1.verts[0] == edge2.verts[1]):
        return False
    if (edge1.verts[1] == edge2.verts[0] or edge1.verts[1] == edge2.verts[1]):
        return False
    return True

def GetClosestVert(vertex, vertex_list):
    dist = 999999999999
    #print("LENGTH:: ", len(vertex_list))
    ver = vertex_list[len(vertex_list) - 1]
    for v in vertex_list:
        if (v != vertex):
            ans = v.co.x * vertex.co.x + v.co.y * vertex.co.y + v.co.z * vertex.co.z
            if (ans < dist):
                dist = ans
                ver = v

    return v

def GetLeastXVert(vertex_list):
    vertmin = -99999999999
    leastVert = None
    for vert in vertex_list:
        if (vert.co.x > vertmin):
            leastVert = vert;
            vertmin = vert.co.x;
    
    return leastVert

def GetGreatestXVert(vertex_list):
    vertmax = 99999999999
    greatVert = None
    for vert in vertex_list:
        if (vert.co.x < vertmax):
            greatVert = vert;
            vertmax = vert.co.x;
    
    return greatVert

def GetLeastYVert(vertex_list):
    vertmin = -99999999999
    leastVert = None
    for vert in vertex_list:
        if (vert.co.y > vertmin):
            leastVert = vert;
            vertmin = vert.co.y;
    
    return leastVert
    
def GetGreatestYVert(vertex_list):
    vertmax = 99999999999
    greatVert = None
    for vert in vertex_list:
        if (vert.co.y < vertmax):
            greatVert = vert;
            vertmax = vert.co.y;
    
    return greatVert

def BevelVert(bm, vertex_list, bevelAmount):
    bmesh.ops.bevel(bm, geom = vertex_list, offset = bevelAmount, segments = 1, vertex_only = True, clamp_overlap = True)

def GetInsetIndividualFaces(bm, insetAmount, discard_threshold = 0, rel = False):
    
    faces_toinset = []
    for face in bm.faces:
        if (face.calc_area() - insetAmount > discard_threshold):
            faces_toinset.append(face)

    outFaces = bmesh.ops.inset_individual(bm, faces = faces_toinset, use_even_offset = True, thickness = insetAmount, use_relative_offset = rel)

    return faces_toinset

def ExtrudeFacesIndividualAlongNomral(bm, face_list, extrudeAmount):
    extrudedFaces = bmesh.ops.extrude_discrete_faces(bm, faces = face_list)
    for face in extrudedFaces["faces"]:        
        normal = face.normal
        for vert in face.verts:
            vert.co += extrudeAmount * normal
        
def FacesAreaExists(face_list, min, max):
    for face in face_list:
        area = face.calc_area()
        if (max < 0):
            if (area < min):
                return True
        if (min < 0):
            if (area > max):
                return True
        if (area < min and area > max):
            return True
    
    return False

def KillVertexArea(bm, areathreshhold):
    done = False
    while (not done):
        done = True
        for f in bm.faces:
            area = f.calc_area()
            if (area < areathreshhold):
                boundary_verts = []
                nonboundary_verts = []
                for vert in f.verts:
                    if (vert.is_boundary):
                        boundary_verts.append(vert)
                    else:
                        nonboundary_verts.append(vert)
                
                if (len(boundary_verts) >= 1 and len(nonboundary_verts) >= 1):
                    close = GetClosestVert(boundary_verts[0], nonboundary_verts)
                    bmesh.ops.pointmerge(bm, verts =[boundary_verts[0], close], merge_co = boundary_verts[0].co)
                    continue
                elif (len(boundary_verts) > 1 and len(nonboundary_verts) == 0):
                    close = GetClosestVert(boundary_verts[0], boundary_verts)                        
                    bmesh.ops.pointmerge(bm, verts =[boundary_verts[0], close], merge_co = boundary_verts[0].co)
                    continue
                elif (len(boundary_verts)  == 0 and len(nonboundary_verts) >= 1):
                    close = GetClosestVert(nonboundary_verts[0], nonboundary_verts)
                    bmesh.ops.pointmerge(bm, verts =[nonboundary_verts[0], close], merge_co = nonboundary_verts[0].co)
                    continue

def KillVertexAngle():
    pass

def DissoveFaceArea(bm, areathreshhold):
    bm.faces.ensure_lookup_table();
    facesTokill = []
    for face in bm.faces:
        area = face.calc_area()
        if (area < areathreshhold):
            facesTokill.append(face)

    bmesh.ops.dissolve_faces(bm, faces = facesTokill, use_verts = True)

def SqaureAlogrithm(xiterations_min, xiterations_max, yiterations_min, yiterations_max, insetAmount = 0.03, insetDiscard = 0.0,
    bevelAmount_min = 0.1, bevelAmount_max = 0.15, extrudeAmount = 0.1):
    
    me = bpy.context.object.data

    bm = bmesh.new()   
    bm.from_mesh(me)  


    leastVert_X = GetLeastXVert(bm.verts)
    greatVert_X = GetGreatestXVert(bm.verts)
    x_number_of_cuts = random.randint(xiterations_min, xiterations_max)
    buffer_x = []
    for cut in range(x_number_of_cuts):
        geo = bm.verts[:] + bm.edges[:] + bm.faces[:]    
        param_t = random.uniform(0.1,0.9)
        parm_ans = leastVert_X.co + param_t*(greatVert_X.co - leastVert_X.co);        
        normal = mathutils.Vector((1.0, 0.0, 0.0))
        discard = False
        for x in buffer_x:
            if (abs(x - parm_ans.x) < insetAmount * 3):
                discard = True
        if (not discard):
            bmesh.ops.bisect_plane(bm, geom = geo, dist = 0.001, plane_co = (parm_ans.x, 0, 0), plane_no = normal)
            buffer_x.append(parm_ans.x)

        
    leastVert_Y = GetLeastYVert(bm.verts)
    greatVert_Y = GetGreatestYVert(bm.verts)
    y_number_of_cuts = random.randint(yiterations_min, yiterations_max)
    buffer_y = []
    for cut in range(y_number_of_cuts):
        geo = bm.verts[:] + bm.edges[:] + bm.faces[:]    
        param_t = random.uniform(0.1,0.9)
        parm_ans = leastVert_Y.co + param_t*(greatVert_Y.co - leastVert_Y.co);        
        normal = mathutils.Vector((0.0, 1.0, 0.0))
        discard = False
        for y in buffer_y:
            if (abs(y - parm_ans.y) < insetAmount * 3):
                discard = True
        if (not discard):
            bmesh.ops.bisect_plane(bm, geom = geo, dist = 0.001, plane_co = (0, parm_ans.y, 0), plane_no = normal)
            buffer_y.append(parm_ans.y)

    
  

    bevelAmount = random.uniform(0.1, 0.15)
    vertex_bevel_list = []
    for vert in bm.verts:
        if (not vert.is_boundary):
            edges = vert.link_edges
            append = True
            for edge in edges:
                if (edge.calc_length() < bevelAmount + 0.05):
                    append = False;
                    break;
            if (append):
                vertex_bevel_list.append(vert)


    #print(vertex_bevel_list)
    BevelVert(bm, vertex_bevel_list, bevelAmount)

    bmesh.ops.remove_doubles(bm, verts= bm.verts, dist = 0.0075)

    #for vert in vertex_bevel_list:
    #   BevelVert(bm, vertex_bevel_list, bevelAmount)
    inset_faces = GetInsetIndividualFaces(bm, 0.03, insetDiscard)
    
    bmesh.ops.remove_doubles(bm, verts= bm.verts, dist = 0.0075)

    ExtrudeFacesIndividualAlongNomral(bm, inset_faces, extrudeAmount)
    
    bm.to_mesh(me)
    bm.free()  

    AddBevelModifer()


def AbstractAlgorithm(iterations, areaKill = 0.1, insetAmount = 0.03, insetDiscard = 0 ,extrudeAmount = 0.1, longedgeBias = 0.75):
    me = bpy.context.object.data

    bm = bmesh.new()   
    bm.from_mesh(me)
  
    for i in range(0, iterations):
        ignore_list = []
        bm.edges.ensure_lookup_table()
        edge_list = list(bm.edges)  

        longestEdge = GetLongestEdge(edge_list)
        
        ignore_list.append(longestEdge)

        probs = random.uniform(0,1)
        if (probs >= longedgeBias):
            randomEdge = GetShortestEdge(edge_list, ignore_list)
        else:
            randomEdge = GetLongestEdge(edge_list, ignore_list)
            
        
        geo_index = SubdivEdges(bm, [longestEdge, randomEdge], probs)
        
        newVerts = [bm.verts[geo_index[0]], bm.verts[geo_index[1]]]; 

        newEdges = bmesh.ops.connect_vert_pair(bm, verts = newVerts)

    if (FacesAreaExists(bm.faces, areaKill, -1)):
        KillVertexArea(bm, areaKill)

    insetFaces = GetInsetIndividualFaces(bm, insetAmount, insetDiscard, True)

    bmesh.ops.remove_doubles(bm, verts= bm.verts, dist = 0.0075)

    ExtrudeFacesIndividualAlongNomral(bm, insetFaces, extrudeAmount)

    
    bm.to_mesh(me)
    bm.free()  

    AddBevelModifer()



