import pyvista as pv
import numpy as np

plotter = pv.Plotter(window_size=[2000, 2000], off_screen=True)
def get_rotation_matrix(vec1, vec2):
    """ Calculate rotation matrix to align vec1 to vec2 """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    if s < 1e-10: return np.eye(3) # Already aligned
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s**2))
    return rotation_matrix

def draw_pyvista_octahedron(symbols, rotations):
    octa = pv.PlatonicSolid('octahedron')
    octa = octa.compute_normals(cell_normals=True, point_normals=False)
    
    normals = octa.cell_data['Normals']
    centers = octa.cell_centers().points

    plotter = pv.Plotter(window_size=[1000, 1000])
    plotter.add_mesh(octa, color="#727CED", show_edges=True, edge_color='black', 
                     line_width=1, lighting=False)

    for i in range(8):
        symbol = symbols[i % len(symbols)]
        angle = rotations[i]
        txt = pv.Text3D(symbol, depth=0.005, height=0.2)
        
        txt.points -= txt.center
        txt = txt.rotate_z(angle)
        rot_mat = get_rotation_matrix(np.array([0, 0, 1]), normals[i])
        
        txt.transform(rot_mat)

        txt.points += centers[i] + (normals[i] * 0.005)
        
        plotter.add_mesh(txt, color="#000000", lighting=False)

    plotter.set_background('white')
    
    try:
        plotter.show()
    except Exception:
        print("No display detected. Saving to octahedron_result.png")
        plotter.screenshot('octahedron_result.png')

my_symbols = ["+", "A", "M", "L", "K", "N", "p", "3"]

#Degrees to rotate each symbol (0, 90, 180, 270, etc.)

my_rotations = [0, 180, 0, 90, 270, 150, 0, 180] 

draw_pyvista_octahedron(my_symbols, my_rotations)
plotter.save_graphic("figure_octahedron.pdf")