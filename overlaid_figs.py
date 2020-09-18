import brainrender
brainrender.USE_MORPHOLOGY_CACHE = True

from brainrender.scene import Scene
from skimage.measure import marching_cubes_lewiner
from skimage import io
import numpy as np
from vtkplotter.mesh import Mesh
import pandas as pd
import time
import os


index = 1



sl_filepaths = {'C57BL_6J':'./streamlines/test/127084296.json',
			'Ntsr1-Cre_GN220':'./streamlines/test/159651060.json',
			'Sim1-Cre_KJ18':'./streamlines/test/297711339.json',
			'Tlx3-Cre_PL56':'./streamlines/test/880719308.json',
			'Nr5a1-Cre':'./streamlines/test/882407664.json',
			'Cux2-IRES-Cre':'./streamlines/test/947242021.json',
			'Rbp4-Cre_KL100':'./streamlines/test/948130129.json'}

sl_colors = {'C57BL_6J':'gray',
			'Ntsr1-Cre_GN220':'red',
			'Sim1-Cre_KJ18':'blue',
			'Tlx3-Cre_PL56':'darkgreen',
			'Nr5a1-Cre':'magenta',
			'Cux2-IRES-Cre':'cyan',
			'Rbp4-Cre_KL100':'green'}


cell_colors = {'18453_4067_x16924_y5288':'cyan',
'18461_4178_x16825_y2713':'cyan',
'18453_3456_x24161_y6646':'cyan',
'18864_3338_x3396_y21865':'magenta',
'18864_4067_x3464_y21495':'magenta',
'236174_3329_x13938_y26099':'gray',
'17781_2881_x4240_y36304':'gray',
'182725_2376_x10033_y10786':'blue',
'182725_3762_x5563_y19178':'darkblue',
'182725_4080_x6576_y11407': (0, 100, 255),
'AA0876':'gray',
'AA0002':'forestgreen',
'AA0271':'forestgreen',
'AA0623':'red',
'AA0635':'red',
'AA0649':'red',
'AA0898':'red'}


im = io.imread('C://Users/maithamn/Downloads/MOpul_Binary_528.tif')
im += np.flip(im,axis=2)

verts,faces,normals,values = marching_cubes_lewiner(im,spacing=(25,25,25),step_size=2)


MOp_region = Mesh([verts,faces],c=(144,0,255),alpha=.25)

cells_base_dir = './cells/cell_jsons/'

IDs = ['C57BL_6J',
		'Ntsr1-Cre_GN220',
		'Sim1-Cre_KJ18',
		'Tlx3-Cre_PL56',
		'Nr5a1-Cre',
		'Cux2-IRES-Cre',
		'Rbp4-Cre_KL100']

# {'cells':[],'streamlines':[],'name':''}

figs = [{'cells':['18453_3456_x24161_y6646'],'streamlines':[],'name':'18453_3456_x24161_y6646'},
		{'cells':['18864_3338_x3396_y21865'],'streamlines':[],'name':'18864_3338_x3396_y21865'},
		{'cells':['AA0271'],'streamlines':[],'name':'AA0271'},
		{'cells':['AA0876'],'streamlines':[],'name':'AA0876'},
		{'cells':['17781_2881_x4240_y36304'],'streamlines':[],'name':'17781_2881_x4240_y36304'},
		{'cells':['182725_3762_x5563_y19178'],'streamlines':[],'name':'182725_3762_x5563_y19178'},
		{'cells':['182725_4080_x6576_y11407'],'streamlines':[],'name':'182725_4080_x6576_y11407'},
		{'cells':['AA0649'],'streamlines':[],'name':'AA0649'},
		{'cells':['AA0898'],'streamlines':[],'name':'AA0898'},
		{'cells':[],'streamlines':['Cux2-IRES-Cre','Nr5a1-Cre','Tlx3-Cre_PL56'],'name':'1_AAVs_overlaid'},
		{'cells':['18453_3456_x24161_y6646','18864_3338_x3396_y21865','AA0271'],'streamlines':[],'name':'2_single_cells_overlaid'},
		{'cells':['18453_3456_x24161_y6646','18864_3338_x3396_y21865','AA0271','AA0876','17781_2881_x4240_y36304'],'streamlines':[],'name':'3_single_cells_overlaid'},
		{'cells':['182725_3762_x5563_y19178','182725_4080_x6576_y11407'],'streamlines':[],'name':'4_single_cells_overlaid'},
		{'cells':['AA0649','AA0898'],'streamlines':[],'name':'5_single_cells_overlaid'},
		{'cells':['18453_3456_x24161_y6646','18864_3338_x3396_y21865'],'streamlines':['Cux2-IRES-Cre'],'name':'6_AAV_and_single_cells_overlaid'},
		{'cells':['18864_3338_x3396_y21865'],'streamlines':['Nr5a1-Cre'],'name':'7_AAV_and_single_cells_overlaid'},
		{'cells':['AA0271'],'streamlines':['Tlx3-Cre_PL56'],'name':'8_AAV_and_single_cells_overlaid'},
		{'cells':['182725_3762_x5563_y19178','182725_4080_x6576_y11407'],'streamlines':['Sim1-Cre_KJ18'],'name':'9_AAV_and_single_cells_overlaid'},
		{'cells':['AA0649','AA0898'],'streamlines':['Ntsr1-Cre_GN220'],'name':'10_AAV_and_single_cells_overlaid'}]


for fig in figs:
	if not fig['name'].startswith('4'):
		continue
	# if not fig['name'] == 'AA0271':
	# 	continue
	screenshot_params = dict(
	folder = './screenshots/overlaid_figs2',
	name='18_reversed_{0}'.format(fig['name'])
	)

	# Start by creating a scene
	scene = Scene(screenshot_kwargs=screenshot_params)

	# Add single cells
	for cell in fig['cells']:

		if cell == 'AA0271' or cell == 'AA0876' or cell.startswith('17781') or cell == 'AA0649' or cell == 'AA0898':
			cfp = cell + '.json'
		else:
			cfp = cell + '_reversed.json'
		nfp = os.path.join(cells_base_dir,cfp)
		scene.add_neurons(nfp, soma_color=cell_colors[cell], dendrites_color='black', 
		                axon_color=cell_colors[cell], neurite_radius=18)

	# Add streamlines
	for streamline in fig['streamlines']:
		scene.add_streamlines(sl_filepaths[streamline], color=sl_colors[streamline], show_injection_site=True)



	# # angle 1
	# bespoke_camera = dict(
	#     position = [-1, -.3, .7] ,
	#     focal = [0, 0, 0],
	#     viewup = [0, -1, 0],
	#     distance = 9522.144,
	#     clipping = [5892.778, 14113.736],
	# )
	# scene.render(interactive=False,camera=bespoke_camera, zoom=1)
	# scene.take_screenshot()
	# time.sleep(1)
	# angle 2
	# bespoke_camera = dict(
	#    position = [-1, -.5, 1.8] ,
	#    focal = [0, 0, 0],
	#    viewup = [0, -1, 0],
	#    distance = 9522.144,
	#    clipping = [5892.778, 14113.736],
	# )
	# scene.render(interactive=False,camera=bespoke_camera, zoom=1)
	# scene.take_screenshot()
	# time.sleep(1)



	scene.add_vtkactor(MOp_region)

	# # angle 1
	# bespoke_camera = dict(
	#     position = [-1, -.3, .7] ,
	#     focal = [0, 0, 0],
	#     viewup = [0, -1, 0],
	#     distance = 9522.144,
	#     clipping = [5892.778, 14113.736],
	# )
	# scene.render(interactive=False,camera=bespoke_camera, zoom=1)
	# scene.take_screenshot()
	# time.sleep(1)
	# angle 2
	bespoke_camera = dict(
	position = [-1, -.5, 1.8] ,
	focal = [0, 0, 0],
	viewup = [0, -1, 0],
	distance = 9522.144,
	clipping = [5892.778, 14113.736],
	)
	scene.render(interactive=False,camera=bespoke_camera, zoom=1)
	scene.take_screenshot()

