# Solves the paradigmatic examples from OCT_examples
from OCT_solver import Octahedron, solve_oct_analytical

# Standard spatial vertex mapping 
V_VERTS = {'v1': 'f', 'v2': 'r', 'v3': 'u', 'v4': 'l', 'v5': 'd', 'v6': 'b'}
U_VERTS = {'u1': 'f', 'u2': 'r', 'u3': 'u', 'u4': 'l', 'u5': 'd', 'u6': 'b'}

def complete_blueprint(bp, prefix='v', placeholder_prefix='h'):
    """Ensures all 6 vertices exist in the blueprint to avoid KeyErrors."""
    for i in range(1, 7):
        vid = f"{prefix}{i}"
        if vid not in bp:
            # Placeholders represent the 4 non-visible faces for hidden vertices 
            bp[vid] = [f"{placeholder_prefix}{i}_1", f"{placeholder_prefix}{i}_2", 
                       f"{placeholder_prefix}{i}_3", f"{placeholder_prefix}{i}_4"]
    return bp

def run_scenarios():
    # ==========================================
    # SCENARIO 1: No Common Features 
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 1: No Common Features\n" + "="*50)
    v_f_1 = {
        'f1': (['v1', 'v4', 'v3'], 'd', ('v4', 'v3', '0')), 'f2': (['v1', 'v3', 'v2'], '&', ('v3', 'v2', '0')),
        'f3': (['v1', 'v2', 'v5'], '4', ('v2', 'v5', '180')), 'f4': (['v1', 'v5', 'v4'], '7', ('v5', 'v4', '0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_1 = {
        'f1': (['u1', 'u4', 'u3'], '!', ('u4', 'u3', '0')), 'f2': (['u1', 'u3', 'u2'], 'g', ('u3', 'u2', '180')),
        'f3': (['u1', 'u2', 'u5'], '10', ('u2', 'u5', '180')), 'f4': (['u1', 'u5', 'u4'], 'A', ('u1', 'u5', '180')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    # Blueprints mapping features from f1-f8 to vertices v1-v6
    v_bp_1 = {
        'v1': ['d', '&', '4', '7'], 'v2': ['&', 'h1', 'h3', '4'], 'v3': ['&', 'd', 'h2', 'h1'],
        'v4': ['d', '7', 'h4', 'h2'], 'v5': ['7', '4', 'h3', 'h4'], 'v6': ['h1', 'h2', 'h4', 'h3']
    }
    u_bp_1 = {
        'u1': ['!', 'g', '10', 'A'], 'u2': ['g', 'k1', 'k3', '10'], 'u3': ['g', '!', 'k2', 'k1'],
        'u4': ['!', 'A', 'k4', 'k2'], 'u5': ['A', '10', 'k3', 'k4'], 'u6': ['k1', 'k2', 'k4', 'k3']
    }
    solve_oct_analytical(Octahedron("V1", V_VERTS, v_f_1), Octahedron("U1", U_VERTS, u_f_1), v_bp_1, u_bp_1)

    # ==========================================
    # SCENARIO 2: One Common Feature 
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 2: One Common Feature\n" + "="*50)
    v_f_2 = {
        'f1': (['v1', 'v4', 'v3'], 'O', ('v4', 'v3', '0')), 'f2': (['v1', 'v3', 'v2'], 'g', ('v3', 'v2', '180')),
        'f3': (['v1', 'v2', 'v5'], '7', ('v1', 'v2', '0')), 'f4': (['v1', 'v5', 'v4'], 's', ('v1', 'v5', '0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_2 = {
        'f1': (['u1', 'u4', 'u3'], '6', ('u1', 'u4', '0')), 'f2': (['u1', 'u3', 'u2'], '7', ('u1', 'u3', '180')),
        'f3': (['u1', 'u2', 'u5'], 'd', ('u1', 'u5', '0')), 'f4': (['u1', 'u5', 'u4'], '!', ('u5', 'u4', '0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_2 = complete_blueprint({'v1': ['O', 'g', '7', 's']}, 'v', 'h')
    u_bp_2 = complete_blueprint({'u1': ['6', '7', 'd', '!']}, 'u', 'k')
    solve_oct_analytical(Octahedron("V2", V_VERTS, v_f_2), Octahedron("U2", U_VERTS, u_f_2), v_bp_2, u_bp_2)

    # ==========================================
    # SCENARIO 3: Three Common Features 
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 3: Three Common Features\n" + "="*50)
    v_f_3 = {
        'f1': (['v1','v4','v3'], 'L', ('v4','v3','0')), 'f2': (['v1','v3','v2'], 'K', ('v3','v2','0')), 
        'f3': (['v1','v2','v5'], 'X', ('v2','v5','180')), 'f4': (['v1','v5','v4'], 'A', ('v5','v1','0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_3 = {
        'f1': (['u1','u4','u3'], 'A', ('u4','u3','180')), 'f2': (['u1','u3','u2'], 'M', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], 'X', ('u2','u5','0')), 'f4': (['u1','u5','u4'], 'L', ('u5','u4','0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_3 = complete_blueprint({'v1': ['L', 'K', 'X', 'A']}, 'v', 'h')
    u_bp_3 = complete_blueprint({'u1': ['A', 'M', 'L', 'X']}, 'u', 'k')
    solve_oct_analytical(Octahedron("V3", V_VERTS, v_f_3), Octahedron("U3", U_VERTS, u_f_3), v_bp_3, u_bp_3)

    # ==========================================
    # SCENARIO 4: Two Common, No Shared Edge 
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 4: Two Common, No Shared Edge\n" + "="*50)
    v_f_4 = {
        'f1': (['v1','v4','v3'], '10', ('v1','v3','0')), 'f2': (['v1','v3','v2'], '!', ('v3','v1','0')),
        'f3': (['v1','v2','v5'], '1', ('v2','v1','0')), 'f4': (['v1','v5','v4'], '8', ('v1','v4','0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_4 = {
        'f1': (['u1','u4','u3'], 'H', ('u4','u3', '0')), 'f2': (['u1','u3','u2'], '!', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], 'g', ('u2','u5','0')), 'f4': (['u1','u5','u4'], '10', ('u5','u4','0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_4 = complete_blueprint({'v1': ['10', '!', '1', '8']}, 'v', 'h')
    u_bp_4 = complete_blueprint({'u1': ['H', '!', 'g', '10']}, 'u', 'k')
    solve_oct_analytical(Octahedron("V4", V_VERTS, v_f_4), Octahedron("U4", U_VERTS, u_f_4), v_bp_4, u_bp_4)

    # ==========================================
    # SCENARIO 5: Two Common features-rotation hides features
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 5: Two Common, Structural Mismatch\n" + "="*50)
    v_f_5 = {
        'f1': (['v1','v4','v3'], '8', ('v4','v3','0')), 'f2': (['v1','v3','v2'], '1', ('v3','v2','0')),
        'f3': (['v1','v2','v5'], 'V', ('v2','v5','0')), 'f4': (['v1','v5','v4'], '%', ('v5','v4','0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_5 = {
        'f1': (['u1','u4','u3'], 'H', ('u4','u3','0')), 'f2': (['u1','u3','u2'], '8', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], '1', ('u2','u5','0')), 'f4': (['u1','u5','u4'], '!', ('u5','u4','180')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_5 = complete_blueprint({'v1': ['8', '1', 'V', '%']}, 'v', 'h')
    u_bp_5 = complete_blueprint({'u1': ['H', '8', '1', '!']}, 'u', 'k')
    solve_oct_analytical(Octahedron("V5", V_VERTS, v_f_5), Octahedron("U5", U_VERTS, u_f_5), v_bp_5, u_bp_5)

    # ==========================================
    # SCENARIO 6: Two common features, different orientations
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 6: Different Orientations\n" + "="*50)
    v_f_6 = {
        'f1': (['v1','v4','v3'], 'D', ('v4','v1','0')), 'f2': (['v1','v3','v2'], '3', ('v3','v1','0')),
        'f3': (['v1','v2','v5'], 'S', ('v1','v5','0')), 'f4': (['v1','v5','v4'], '6', ('v1','v5','0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_6 = {
        'f1': (['u1','u4','u3'], '3', ('u4','u3','90')), 'f2': (['u1','u3','u2'], 'D', ('u3','u2','0')),
        'f3': (['u1','u2','u5'], 'B', ('u2','u5','0')), 'f4': (['u1','u5','u4'], 'O', ('u5','u4','0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_6 = complete_blueprint({'v1': ['D', '3', 'S', '6']}, 'v', 'h')
    u_bp_6 = complete_blueprint({'u1': ['3', 'D', 'B', 'O']}, 'u', 'k')
    solve_oct_analytical(Octahedron("V6", V_VERTS, v_f_6), Octahedron("U6", U_VERTS, u_f_6), v_bp_6, u_bp_6)

    # ==========================================
    # SCENARIO 7: Two common features, same octahedron
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 7: Same Octahedron, 2 Shared\n" + "="*50)
    v_f_7 = {
        'f1': (['v1','v4','v3'], 'A', ('v4','v3','180')), 'f2': (['v1','v3','v2'], 'B', ('v1','v2','0')),
        'f3': (['v1','v2','v5'], 'D', ('v2','v5','0')), 'f4': (['v1','v5','v4'], 'C', ('v5','v4','0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_7 = {
        'f1': (['u1','u4','u3'], 'X', ('u4','u1','30')), 'f2': (['u1','u3','u2'], 'B', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], 'A', ('u1','u5','180')), 'f4': (['u1','u5','u4'], 'N', ('u5','u4','15')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    # Blueprints mapping features from f1-f8 to vertices v1-v6
    v_bp_7 = {
        'v1': ['A', 'B', 'D', 'C'], 'v2': ['B', 'h1', 'h3', 'D'], 'v3': ['B', 'A', 'h2', 'h1'],
        'v4': ['A', 'C', 'h4', 'h2'], 'v5': ['C', 'D', 'h3', 'h4'], 'v6': ['h1', 'h2', 'h4', 'h3']
    }
    u_bp_7 = {
        'u1': ['X', 'B', 'A', 'N'], 'u2': ['B', 'k1', 'k3', 'A'], 'u3': ['B', 'X', 'k2', 'k1'],
        'u4': ['X', 'N', 'k4', 'k2'], 'u5': ['N', 'A', 'k3', 'k4'], 'u6': ['k1', 'k2', 'k4', 'k3']
    }
    solve_oct_analytical(Octahedron("V7", V_VERTS, v_f_7), Octahedron("U7", U_VERTS, u_f_7), v_bp_7, u_bp_7)

    # ==========================================
    # SCENARIO 8: Four features common, incorrect order
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 8: Four Shared, Incorrect Order\n" + "="*50)
    v_f_8 = {
        'f1': (['v1','v4','v3'], 'A', ('v4','v3','0')), 'f2': (['v1','v3','v2'], 'B', ('v3','v2','0')), 
        'f3': (['v1','v2','v5'], 'D', ('v2','v5', '0')), 'f4': (['v1','v5','v4'], 'C', ('v5','v4', '0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_8 = {
        'f1': (['u1','u4','u3'], 'D', ('u4','u3','0')), 'f2': (['u1','u3','u2'], 'B', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], 'A', ('u2','u5', '180')), 'f4': (['u1','u5','u4'], 'C', ('u5','u4', '0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_8 = complete_blueprint({'v1': ['A', 'B', 'D', 'C']}, 'v', 'h')
    u_bp_8 = complete_blueprint({'u1': ['D', 'B', 'A', 'C']}, 'u', 'k') # Scrambled order
    solve_oct_analytical(Octahedron("V8", V_VERTS, v_f_8), Octahedron("U8", U_VERTS, u_f_8), v_bp_8, u_bp_8)

    # ==========================================
    # SCENARIO 9: Four common features, incorrect orientation
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 9: Four Shared, Incorrect Orientation\n" + "="*50)
    v_f_9 = {
        'f1': (['v1','v4','v3'], '10', ('v4','v3', '0')), 'f2': (['v1','v3','v2'], 'g', ('v3','v2', '0')), 
        'f3': (['v1','v2','v5'], 'p', ('v2','v5', '0')), 'f4': (['v1','v5','v4'], '7', ('v5','v4', '0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_9 = {
        'f1': (['u1','u4','u3'], 'p', ('u4','u3','0')), 'f2': (['u1','u3','u2'], '7', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], '10', ('u2','u5','90')), 'f4': (['u1','u5','u4'], 'g', ('u5','u4','0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    v_bp_9 = complete_blueprint({'v1': ['10', '6', 'p', '7']}, 'v', 'h')
    u_bp_9 = complete_blueprint({'u1': ['p', '7', '10', '6']}, 'u', 'k')
    solve_oct_analytical(Octahedron("V9", V_VERTS, v_f_9), Octahedron("U9", U_VERTS, u_f_9), v_bp_9, u_bp_9)

    # ==========================================
    # SCENARIO 10: Four common features, identical octahedrons.
    # ==========================================
    print("\n" + "="*50 + "\nSCENARIO 10: Identical Octahedrons\n" + "="*50)
    v_f_10 = {
        'f1': (['v1','v4','v3'], 'D', ('v4','v3', '0')), 'f2': (['v1','v3','v2'], 'B', ('v3','v2', '0')), 
        'f3': (['v1','v2','v5'], 'O', ('v2','v5', '0')), 'f4': (['v1','v5','v4'], '5', ('v1','v4', '0')),
        'f5': (['v3', 'v6', 'v2'], 'h1', ('v3', 'v6', 'alpha5')), 'f6': (['v3', 'v4', 'v6'], 'h2', ('v3', 'v4', 'alpha6')),
        'f7': (['v6', 'v4', 'v5'], 'h4', ('v6', 'v4', 'alpha7')), 'f8': (['v6', 'v5', 'v2'], 'h3', ('v6', 'v5', 'alpha8'))
    }
    u_f_10 = {
        'f1': (['u1','u4','u3'], 'B', ('u4','u3','0')), 'f2': (['u1','u3','u2'], 'O', ('u3','u2','0')), 
        'f3': (['u1','u2','u5'], '5', ('u1','u5','0')), 'f4': (['u1','u5','u4'], 'D', ('u5','u4','0')),
        'f5': (['u3', 'u6', 'u2'], 'k1', ('u3', 'u6', 'alpha2_5')), 'f6': (['u3', 'u4', 'u6'], 'k2', ('u3', 'u4', 'alpha2_6')),
        'f7': (['u6', 'u4', 'u5'], 'k4', ('u6', 'u4', 'alpha2_7')), 'f8': (['u6', 'u5', 'u2'], 'k3', ('u6', 'u5', 'alpha2_8'))
    }
    # Full blueprints for successful topological verification 
    v_bp_10 = {
        'v1': ['D', 'B', 'O', '5'], 'v2': ['B', 'h1', 'h3', 'O'], 'v3': ['B', 'D', 'h2', 'h1'],
        'v4': ['D', '5', 'h4', 'h2'], 'v5': ['5', 'O', 'h3', 'h4'], 'v6': ['h1', 'h2', 'h4', 'h3']
    }
    u_bp_10 = {
        'u1': ['B', 'O', '5', 'D'], 'u2': ['O', 'k1', 'k3', '5'], 'u3': ['O', 'B', 'k2', 'k1'],
        'u4': ['B', 'D', 'k4', 'k2'], 'u5': ['D', '5', 'k3', 'k4'], 'u6': ['k1', 'k2', 'k4', 'k3']
    }
    solve_oct_analytical(Octahedron("V10", V_VERTS, v_f_10), Octahedron("U10", U_VERTS, u_f_10), v_bp_10, u_bp_10)



    

if __name__ == "__main__":
    run_scenarios()
