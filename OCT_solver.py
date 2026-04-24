class Octahedron:
    def __init__(self, name, vertices, faces_data):
        self.name = name
        self.vertices = vertices  # dict: {id: location}
        self.faces = faces_data     # dict: {id: (verts, feature, orientation)}

    def print_state(self):
        """Prints the current spatial location of each vertex ID."""
        print(f"\n--- {self.name} Current State ---")
        print(f"{'Location':<12} | {'Vertex ID':<10}")
        print("-" * 25)
        
        full_names = {
            'f': 'Front', 'b': 'Back', 'u': 'Up', 
            'd': 'Down', 'r': 'Right', 'l': 'Left'
        }
        
        for loc_code in ['f', 'b', 'u', 'd', 'r', 'l']:
            matching_vids = [vid for vid, vloc in self.vertices.items() if vloc == loc_code]
            if matching_vids:
                vid = matching_vids[0]
                print(f"{full_names[loc_code]:<12} | {vid:<10}")

    def print_face_descriptors(self):
        """Prints the QODV_F descriptors as defined in Section 3."""
        print(f"\n=== {self.name} Face Descriptors (QODV_F) ===")
        print(f"{'Face':<6} | {'Vertices':<18} | {'Feature':<8} | {'Orientation'}")
        print("-" * 65)
        for f_id in sorted(self.faces.keys(), key=lambda x: int(x[1:])):
            v_list, feature, orient = self.faces[f_id]
            # Print as a list to show ordered orientation
            v_str = "[" + ", ".join(v_list) + "]"
            o_str = "{" + ", ".join(map(str, orient)) + "}"
            print(f"{f_id:<6} | {v_str:<18} | {feature:<8} | {o_str}")

def is_cyclic_list_equal(list1, list2):
    """Checks if list1 is a cyclic shift of list2 (exact matches only)."""
    if len(list1) != len(list2):
        return False
    
    n = len(list1)
    for shift in range(n):
        if list1[shift:] + list1[:shift] == list2:
            return True
    return False

def is_cyclic_shift(list1, list2, mapping, known_1, known_2):
    """Checks if list1 is a cyclic shift of list2 accounting for placeholders. Updates mapping"""
    n = len(list1)
    placeholders = ['h1', 'h2', 'h3', 'h4', 'k1', 'k2', 'k3', 'k4']

    for shift in range(n):
        rotated_l1 = list1[shift:] + list1[:shift]
        temp_map = mapping.copy()
        match_found = True
        
        for f1, f2 in zip(rotated_l1, list2):
            
            # Check if Octa1 feature is a placeholder
            if f1 in placeholders:
                if f1 in temp_map:
                    if temp_map[f1] != f2:
                        match_found = False; break
                else:
                    # ENFORCE UNIQUE FEATURES: Cannot map a placeholder to a known feature
                    if f2 in known_1:
                        match_found = False; break
                    temp_map[f1] = f2
                    
            # Check if Octa2 feature is a placeholder
            elif f2 in placeholders:
                if f2 in temp_map:
                    if temp_map[f2] != f1:
                        match_found = False; break
                else:
                    # ENFORCE UNIQUE FEATURES
                    if f1 in known_2:
                        match_found = False; break
                    temp_map[f2] = f1 
                    
            # Check if they are perfect constant matches (e.g. 'a' == 'a')
            elif f1 == f2:
                continue
                
            # Otherwise, it's a hard mismatch
            else:
                match_found = False
                break
        
        # Updates the map
        if match_found:
            mapping.update(temp_map)
            return True
            
    return False

def rotate_octa(vertices, move):
    """Returns a new vertex dictionary with updated locations."""
    moves = {
        'td': {'f': 'd', 'd': 'b', 'b': 'u', 'u': 'f', 'r': 'r', 'l': 'l'},
        'tu': {'f': 'u', 'u': 'b', 'b': 'd', 'd': 'f', 'r': 'r', 'l': 'l'},
        'tl': {'f': 'l', 'l': 'b', 'b': 'r', 'r': 'f', 'u': 'u', 'd': 'd'},
        'tr': {'f': 'r', 'r': 'b', 'b': 'l', 'l': 'f', 'u': 'u', 'd': 'd'},
        'cw':  {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u', 'f': 'f', 'b': 'b'},
        'acw': {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u', 'f': 'f', 'b': 'b'}
    }
    new_verts = {}
    for vid, loc in vertices.items():
        new_verts[vid] = moves[move][loc]
    return new_verts

def get_vertex_id_mapping(octa1, octa2):
    """Identifies which physical corner in the first octahedron currently occupies the same spot as a physical corner in the second."""
    print("\n[DEBUG] Generating Vertex ID Mapping...")
    v_map = {}
    for loc in ['f', 'r', 'u', 'l', 'd', 'b']:
        id1 = [vid for vid, vloc in octa1.vertices.items() if vloc == loc][0]
        id2 = [uid for uid, uloc in octa2.vertices.items() if uloc == loc][0]
        v_map[id1] = id2
        print(f"  Location {loc.upper()}: {id1} -> {id2}")
    return v_map

def are_faces_equal(qodv1, qodv2, v_map):
    """Compares two QODV_F descriptors cyclically using the vertex map and orientations."""
    verts1, feat1, orient1 = qodv1
    verts2, feat2, orient2 = qodv2

    # 1. Compare Vertex Sequences Cyclically
    mapped_verts1 = [v_map[v] for v in verts1]
    
    print(f"    Checking Oriented Vertex Sequences:")
    print(f"      Original V1: {verts1} | Mapped to Octa2 IDs: {mapped_verts1}")
    print(f"      Target V2:   {verts2}")
    
    if not is_cyclic_list_equal(mapped_verts1, verts2):
        print("    [RESULT] FAILED: Vertex sequence (orientation) does not match cyclically.")
        return False

    # 2. Extract Orientation Data
    e1_a, e1_b, angle1 = orient1
    e2_a, e2_b, angle2 = orient2

    # Helper: Check if a value is a standard number
    def is_number(val):
        return str(val).replace('.', '', 1).replace('-', '', 1).isdigit()

    # 3. WILDCARD CHECK: If either angle is a placeholder, accept the orientation instantly
    if not is_number(angle1) or not is_number(angle2):
        print(f"    [!] Wildcard Match: Angle '{angle1}' or '{angle2}' is a placeholder.")
        print("    [RESULT] SUCCESS: Bypassing strict edge/angle comparison due to unknown variable.")
        return True

    # 4. STRICT COMPARISON (Only reached if both angles are real numbers)
    mapped_edge1 = {v_map.get(e1_a, e1_a), v_map.get(e1_b, e1_b)}
    edge2 = {e2_a, e2_b}
    
    print(f"    Checking Hinge/Angle:")
    print(f"      Edge Mapped: {mapped_edge1} | Edge Target: {edge2}")
    print(f"      Angle 1: '{angle1}' | Angle 2: '{angle2}'")

    if mapped_edge1 != edge2:
        print("    [RESULT] FAILED: Orientation edge mismatch.")
        return False
        
    if str(angle1) != str(angle2):
        print(f"    [RESULT] FAILED: Angle mismatch ('{angle1}' != '{angle2}').")
        return False

    print("    [RESULT] SUCCESS: Face descriptors match exactly.")
    return True

def compare_octahedrons(octa1, octa2, v_blueprints, u_blueprints):
    """Returns a feature map that links symbols between the two octahedrons."""
    current_mapping = {}
    locations = ['f', 'r', 'u', 'l', 'd', 'b']
    success = True
    
    placeholders = ['h1', 'h2', 'h3', 'h4', 'k1', 'k2', 'k3', 'k4']
    
    known_1 = {f[1] for f in octa1.faces.values() if f[1] not in placeholders}
    known_2 = {f[1] for f in octa2.faces.values() if f[1] not in placeholders}

    for loc in locations:
        id1 = [vid for vid, vloc in octa1.vertices.items() if vloc == loc][0]
        id2 = [uid for uid, uloc in octa2.vertices.items() if uloc == loc][0]
        
        feats1 = v_blueprints[id1]
        feats2 = u_blueprints[id2]
        

        if is_cyclic_shift(feats1, feats2, current_mapping, known_1, known_2):
            pass 
        else:
            success = False
            break

    if success:
        return current_mapping
    return None

def full_octahedron_comparison(octa1, octa2, v_blueprints, u_blueprints):
    """Compares two octahedrons using the QODV. Returns true if they match."""
    feat_map = compare_octahedrons(octa1, octa2, v_blueprints, u_blueprints)
    if feat_map is None:
            return False

    v_map = get_vertex_id_mapping(octa1, octa2)
    print("\n--- Face Descriptor Comparison (QODV_F) ---")

    for f_id1, qodv1 in octa1.faces.items():
        feat1 = qodv1[1]
        
        match_found = False
        print(f"\nSearching for match for Octa1 Face: {f_id1} (Feature: {feat1})")

        for f_id2, qodv2 in octa2.faces.items():
            feat2 = qodv2[1]
            
            is_match = (feat1 == feat2 or 
                        feat_map.get(feat1) == feat2 or 
                        feat_map.get(feat2) == feat1)

            if is_match:
                print(f"  [POTENTIAL MATCH] Trying {f_id1} vs {f_id2} (Features: {feat1} <-> {feat2})")
                if are_faces_equal(qodv1, qodv2, v_map):
                    match_found = True
                    break
                else:
                    print(f"  [!] Face structure mismatch between {f_id1} and {f_id2}")
                    match_found = False

        if not match_found:
            print(f"\n[CRITICAL FAILURE] No valid orientation match found for feature '{feat1}'")
            print(f"This means the face '{feat1}' exists in both, but its corners or hinge angle are different.")
            return False

    print("\n" + "="*30)
    print("SUCCESS: BOTH OCTAHEDRONS ARE QUALITATIVELY IDENTICAL")
    return True

# Algorithm to find the rotations necessary

import sys
import os

class HiddenPrints:
    """Context manager to suppress print statements during the search."""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def solve_oct(octa1_start, octa2_target, v_feats, u_feats):
    """
    Implements the OCT solver algorithm from Section 4.
    Uses Breadth-First Search (BFS) to find the shortest valid sequence of rotations.
    """
    print(f"\n--- INITIATING ALGORITHMIC SOLVER ---")
    print("Searching for valid rotation sequence...")
    
    # Queue stores tuples of: (current_vertices_dict, list_of_moves_taken)
    queue = [(octa1_start.vertices, [])]
    
    # Visited set to prevent infinite loops. We store a sorted tuple of the dictionary items.
    visited = set()
    visited.add(tuple(sorted(octa1_start.vertices.items())))
    
    all_moves = ['td', 'tu', 'tl', 'tr', 'cw', 'acw']
    
    while queue:
        curr_verts, path = queue.pop(0)
        
        # Create a temporary octahedron with the current rotated state
        temp_octa = Octahedron("Temp_Octa", curr_verts, octa1_start.faces)
        
        # Check if this state matches Octa 2 (suppressing prints so we don't spam the console)
        with HiddenPrints():
            is_match = full_octahedron_comparison(temp_octa, octa2_target, v_feats, u_feats)
            
        if is_match:
            print(f"\n>> SUCCESS! Found matching sequence: {path}")
            print(">> Running final verification trace:")
            # Run it one last time without hiding prints to show the final success trace
            full_octahedron_comparison(temp_octa, octa2_target, v_feats, u_feats)
            return path, temp_octa
            
        # If not a match, generate the next possible moves
        for move in all_moves:
            new_verts = rotate_octa(curr_verts, move)
            state_tuple = tuple(sorted(new_verts.items()))
            
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.append((new_verts, path + [move]))
                
    print("\n>> FAILURE: No valid rotation sequence exists. The octahedrons are structurally different.")
    return None, None



def get_table1_path(start_loc, target_loc):
    """
    Simulates 'Table 1' from the paper. 
    Finds the shortest sequence of rotations to move a vertex from one location to another.
    """
    if start_loc == target_loc:
        return []
        
    moves = {
        'td': {'f': 'd', 'd': 'b', 'b': 'u', 'u': 'f', 'r': 'r', 'l': 'l'},
        'tu': {'f': 'u', 'u': 'b', 'b': 'd', 'd': 'f', 'r': 'r', 'l': 'l'},
        'tl': {'f': 'l', 'l': 'b', 'b': 'r', 'r': 'f', 'u': 'u', 'd': 'd'},
        'tr': {'f': 'r', 'r': 'b', 'b': 'l', 'l': 'f', 'u': 'u', 'd': 'd'},
        'cw': {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u', 'f': 'f', 'b': 'b'},
        'acw': {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u', 'f': 'f', 'b': 'b'}
    }
    

    queue = [(start_loc, [])]
    visited = {start_loc}
    
    while queue:
        curr, path = queue.pop(0)
        if curr == target_loc:
            return path
        for move_name, move_dict in moves.items():
            nxt = move_dict[curr]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [move_name]))
    return []

def trace_vertex(loc, sequence):
    """Helper to predict where a vertex ends up after a sequence of moves. Does not change the position of the vertex."""
    moves = {
        'td': {'f': 'd', 'd': 'b', 'b': 'u', 'u': 'f', 'r': 'r', 'l': 'l'},
        'tu': {'f': 'u', 'u': 'b', 'b': 'd', 'd': 'f', 'r': 'r', 'l': 'l'},
        'tl': {'f': 'l', 'l': 'b', 'b': 'r', 'r': 'f', 'u': 'u', 'd': 'd'},
        'tr': {'f': 'r', 'r': 'b', 'b': 'l', 'l': 'f', 'u': 'u', 'd': 'd'},
        'cw': {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u', 'f': 'f', 'b': 'b'},
        'acw': {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u', 'f': 'f', 'b': 'b'}
    }
    curr = loc
    for move in sequence:
        curr = moves[move][curr]
    return curr



def solve_oct_analytical(octa1, octa2, v_feats, u_feats):
    """Runs the algorithm described in the paper to see if two octahedrons are the same by 
    finding a possible sequence of rotations that takes one octahedron to the other and compares their QODV."""

    print("\n--- ANALYTICAL SOLVER  ---")
    
    # STEP 1: Initial feature comparison filter
    placeholders = ['h1', 'h2', 'h3', 'h4', 'k1', 'k2', 'k3', 'k4']
    known_1 = {f[1] for f in octa1.faces.values() if f[1] not in placeholders}
    known_2 = {f[1] for f in octa2.faces.values() if f[1] not in placeholders}
    common = sorted(list(known_1.intersection(known_2)))
    num_common = len(common)
    
    if num_common in [1, 3]:
        print("  [!] ABORT: 1 or 3 features is physically impossible.")
        return None, None
    
    if num_common == 0:
        print("  Step: 0 Common Features. Applying 180-degree flip (tl, tl).")
        flip_seq = ['tl', 'tl']
        temp_verts = octa1.vertices.copy()
        for move in flip_seq: temp_verts = rotate_octa(temp_verts, move)
        return flip_seq, Octahedron("Flipped", temp_verts, octa1.faces)

    # STEP 2: Identify the Vertex meant for the FRONT 
    # We find which physical vertex in Octa1 corresponds to the Front vertex of Octa2
    u_front_id = [uid for uid, uloc in octa2.vertices.items() if uloc == 'f'][0]
    u_front_blueprint = u_feats[u_front_id]
    
    v_target_front_id = None
    for vid, v_blue in v_feats.items():
        if is_cyclic_shift(v_blue, u_front_blueprint, {}, known_1, known_2):
            v_target_front_id = vid
            break

    if not v_target_front_id:
        print("  [!] FAILURE: No structural match for the front vertex. Different Octahedrons. No possible sequence of rotations.")
        return None, None

    # STEP 3: Move identified vertex to FRONT via Table 1 
    current_loc = octa1.vertices[v_target_front_id]
    primary_move = get_table1_path(current_loc, 'f')
    print(f"Step: Moving {v_target_front_id} from {current_loc.upper()} to FRONT via {primary_move}\n")
    print("Possibility of octahedrons matching, applying clock-wise rotations until sequence is found or 4 have been applied without success")
    
    temp_verts = octa1.vertices.copy()
    for move in primary_move:
        temp_verts = rotate_octa(temp_verts, move)

    # STEP 4: Clockwise Spin Alignment (Section 4.1)
    # Once at front, apply 0-3 clockwise (cw) rotations to align the rest
    for spin_count in range(4):
        spin_seq = ['cw'] * spin_count
        final_seq = primary_move + spin_seq
        
        test_verts = temp_verts.copy()
        for move in spin_seq:
            test_verts = rotate_octa(test_verts, move)
            
        test_octa = Octahedron("Candidate", test_verts, octa1.faces)
        
        with HiddenPrints():
            is_match = full_octahedron_comparison(test_octa, octa2, v_feats, u_feats)
            
        if is_match:
            print(f">> SUCCESS! Sequence found: {final_seq}")
            full_octahedron_comparison(test_octa, octa2, v_feats, u_feats)
            return final_seq, test_octa

    print("\n>> FAILURE: Vertices match but face orientations (QODV_F) do not.")
    return None, None

# --- DATA DEFINITIONS ---

# V_FEATS = {
#     'v1': ['a', 'b', 'd', 'c'],
#     'v2': ['b', 'h1', 'h3', 'd'],
#     'v3': ['b', 'a', 'h2', 'h1'],
#     'v4': ['a', 'c', 'h4', 'h2'],
#     'v5': ['c', 'd', 'h3', 'h4'],
#     'v6': ['h1', 'h2', 'h4', 'h3']
# }

# U_FEATS = {
#     'u1': ['x', 'b', 'a', 'n'],
#     'u2': ['b', 'k1', 'k3', 'a'],
#     'u3': ['k2', 'k1', 'b', 'x'],
#     'u4': ['x', 'n', 'k4', 'k2'],
#     'u5': ['k3', 'k4', 'n', 'a'],
#     'u6': ['k1', 'k2', 'k4', 'k3']
# }

# # --- MAIN EXECUTION ---


# octa1_verts = {'v1': 'f', 'v2': 'r', 'v3': 'u', 'v4': 'l', 'v5': 'd', 'v6': 'b'}

# octa1_faces = {
#     'f1': (['v1', 'v4', 'v3'], 'a',   ('v3', 'v4', '180')),
#     'f2': (['v3', 'v2', 'v1'], 'b',   ('v1', 'v2', '0')),
#     'f3': (['v1', 'v2', 'v5'], 'd',   ('v2', 'v5', '0')),
#     'f4': (['v1', 'v5', 'v4'], 'c',   ('v4', 'v5', '0')),
#     'f5': (['v3', 'v6', 'v2'], 'h1',  ('v3', 'v6', 'alpha5')), 
#     'f6': (['v3', 'v4', 'v6'], 'h2',  ('v3', 'v4', 'alpha6')), 
#     'f7': (['v6', 'v4', 'v5'], 'h4',  ('v6', 'v4', 'alpha7')), 
#     'f8': (['v6', 'v5', 'v2'], 'h3',  ('v6', 'v5', 'alpha8'))  
# }

# octa1 = Octahedron("Octahedron 1", octa1_verts, octa1_faces)

# octa2_verts = {'u1': 'f', 'u2': 'r', 'u3': 'u', 'u4': 'l', 'u5': 'd', 'u6': 'b'}

# octa2_faces = {
#     'f1': (['u1', 'u4', 'u3'], 'x',   ('u1', 'u4', '30')),
#     'f2': (['u3', 'u2', 'u1'], 'b',   ('u3', 'u2', '0')),
#     'f3': (['u1', 'u2', 'u5'], 'a',   ('u1', 'u5', '180')),
#     'f4': (['u1', 'u5', 'u4'], 'n',   ('u4', 'u5', '15')),
#     'f5': (['u3', 'u6', 'u2'], 'k1',  ('u3', 'u6', 'alpha2_5')), 
#     'f6': (['u3', 'u4', 'u6'], 'k2',  ('u3', 'u4', 'alpha2_6')), 
#     'f7': (['u6', 'u4', 'u5'], 'k4',  ('u6', 'u4', 'alpha2_7')), 
#     'f8': (['u6', 'u5', 'u2'], 'k3',  ('u6', 'u5', 'alpha2_8'))  
# }

# octa2 = Octahedron("Octahedron 2", octa2_verts, octa2_faces)

# # Print initial states
# octa1.print_face_descriptors()
# octa2.print_face_descriptors()

# # Run the Solver!
# solution_path, aligned_octa = solve_oct_analytical(octa1, octa2, V_FEATS, U_FEATS)
# print("Brute force solution \n")
# solution_path, aligned_octa = solve_oct(octa1, octa2, V_FEATS, U_FEATS)


