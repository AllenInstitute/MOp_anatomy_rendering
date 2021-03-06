import brainrender
brainrender.USE_MORPHOLOGY_CACHE = True
brainrender.SHADER_STYLE = 'plastic'
brainrender.SOMA_RADIUS = 75
from brainrender.scene import Scene
import os
from skimage.measure import marching_cubes_lewiner
from skimage import io
import numpy as np
from vtkplotter.mesh import Mesh
import time
import pandas as pd
import json


cell_filepaths = {
	'182725_2376_x10033_y10786': './cells/new_cell_jsons/182725_2376_x10033_y10786.json',
	'182725_3762_x5563_y19178': './cells/new_cell_jsons/182725_3762_x5563_y19178.json',
	'182725_4080_x6576_y11407': './cells/new_cell_jsons/182725_4080_x6576_y11407.json',
	'18868_3009_x28076_y11485': './cells/new_cell_jsons/18868_3009_x28076_y11485.json',
	'18868_3488_x24952_y7321': './cells/new_cell_jsons/18868_3488_x24952_y7321.json',
	'AA0114 [A]': './cells/split_cells/AA0114.json',
	'AA0131 [A]': './cells/split_cells/AA0131.json',
	'AA0132 [A]': './cells/split_cells/AA0132.json',
	'AA0133 [A]': './cells/split_cells/AA0133.json',
	'AA0134 [A]': './cells/split_cells/AA0134.json',
	'AA0135 [A]': './cells/split_cells/AA0135.json',
	'AA0169 [A]': './cells/split_cells/AA0169.json',
	'AA0261 [A]': './cells/split_cells/AA0261.json',
	'AA0584 [A]': './cells/split_cells/AA0584.json',
	'AA0587 [A]': './cells/split_cells/AA0587.json',
	'AA0617 [A]': './cells/split_cells/AA0617.json',
	'AA0923 [A]': './cells/split_cells/AA0923.json',
	'AA0926 [A]': './cells/split_cells/AA0926.json',
	'AA0927 [A]': './cells/split_cells/AA0927.json',
	'18867_2903_x13633_y8787': './cells/new_cell_jsons/18867_2903_x13633_y8787.json',
	'18867_3758_x14594_y6944': './cells/new_cell_jsons/18867_3758_x14594_y6944.json',
	'AA0553 [A]': './cells/split_cells/AA0553.json',
	'AA0644 [A]': './cells/split_cells/AA0644.json',
	'AA0863 [A]': './cells/split_cells/AA0863.json',
	'210254_2226_x16029_y23953': './cells/new_cell_jsons/210254_2226_x16029_y23953.json',
	'210254_2309_x13266_y25533': './cells/new_cell_jsons/210254_2309_x13266_y25533.json',
	'210254_4397_x16794_y21812': './cells/new_cell_jsons/210254_4397_x16794_y21812.json',
	'210254_4485_x16442_y16836': './cells/new_cell_jsons/210254_4485_x16442_y16836.json',
	'210254_4500_x16614_y17147': './cells/new_cell_jsons/210254_4500_x16614_y17147.json',
	'AA0038 [A]': './cells/split_cells/AA0038.json',
	'AA0041 [A]': './cells/split_cells/AA0041.json',
	'AA0043 [A]': './cells/split_cells/AA0043.json',
	'AA0185 [A]': './cells/split_cells/AA0185.json',
	'AA0187 [A]': './cells/split_cells/AA0187.json',
	'AA0398 [A]': './cells/split_cells/AA0398.json',
	'AA0545 [A]': './cells/split_cells/AA0545.json',
	'AA0548 [A]': './cells/split_cells/AA0548.json',
	'AA0596 [A]': './cells/split_cells/AA0596.json',
	'AA0605 [A]': './cells/split_cells/AA0605.json',
	'AA0623 [A]': './cells/split_cells/AA0623.json',
	'AA0626 [A]': './cells/split_cells/AA0626.json',
	'AA0628 [A]': './cells/split_cells/AA0628.json',
	'AA0630 [A]': './cells/split_cells/AA0630.json',
	'AA0634 [A]': './cells/split_cells/AA0634.json',
	'AA0635 [A]': './cells/split_cells/AA0635.json',
	'AA0637 [A]': './cells/split_cells/AA0637.json',
	'AA0640 [A]': './cells/split_cells/AA0640.json',
	'AA0641 [A]': './cells/split_cells/AA0641.json',
	'AA0642 [A]': './cells/split_cells/AA0642.json',
	'AA0647 [A]': './cells/split_cells/AA0647.json',
	'AA0648 [A]': './cells/split_cells/AA0648.json',
	'AA0649 [A]': './cells/split_cells/AA0649.json',
	'AA0652 [A]': './cells/split_cells/AA0652.json',
	'AA0654 [A]': './cells/split_cells/AA0654.json',
	'AA0667 [A]': './cells/split_cells/AA0667.json',
	'AA0770 [A]': './cells/split_cells/AA0770.json',
	'AA0785 [A]': './cells/split_cells/AA0785.json',
	'AA0833 [A]': './cells/split_cells/AA0833.json',
	'AA0836 [A]': './cells/split_cells/AA0836.json',
	'AA0898 [A]': './cells/split_cells/AA0898.json',
	'18864_3494_x2380_y13749': './cells/new_cell_jsons/18864_3494_x2380_y13749.json',
	'AA0034 [A]': './cells/split_cells/AA0034.json',
	'AA0064 [A]': './cells/split_cells/AA0064.json',
	'AA0065 [A]': './cells/split_cells/AA0065.json',
	'AA0099 [A]': './cells/split_cells/AA0099.json',
	'AA0130 [A]': './cells/split_cells/AA0130.json',
	'AA0184 [A]': './cells/split_cells/AA0184.json',
	'AA0442 [A]': './cells/split_cells/AA0442.json',
	'AA0600 [A]': './cells/split_cells/AA0600.json',
	'AA0656 [A]': './cells/split_cells/AA0656.json',
	'AA0906 [A]': './cells/split_cells/AA0906.json',
	'AA0060 [A]': './cells/split_cells/AA0060.json',
	'AA0140 [A]': './cells/split_cells/AA0140.json',
	'AA0401 [A]': './cells/split_cells/AA0401.json',
	'AA0404 [A]': './cells/split_cells/AA0404.json',
	'AA0408 [A]': './cells/split_cells/AA0408.json',
	'AA0463 [A]': './cells/split_cells/AA0463.json',
	'AA0464 [A]': './cells/split_cells/AA0464.json',
	'AA0541 [A]': './cells/split_cells/AA0541.json',
	'AA0739 [A]': './cells/split_cells/AA0739.json',
	'AA0741 [A]': './cells/split_cells/AA0741.json',
	'AA0876 [A]': './cells/split_cells/AA0876.json',
	'17109_2301_x8535_y23051': './cells/new_cell_jsons/17109_2301_x8535_y23051.json',
	'17109_2401_x8977_y24184': './cells/new_cell_jsons/17109_2401_x8977_y24184.json',
	'17781_2881_x4240_y36304': './cells/new_cell_jsons/17781_2881_x4240_y36304.json',
	'236174_2801_x11376_y11451': './cells/new_cell_jsons/236174_2801_x11376_y11451.json',
	'236174_3029_x12820_y24699': './cells/new_cell_jsons/236174_3029_x12820_y24699.json',
	'236174_3029_x13178_y25409': './cells/new_cell_jsons/236174_3029_x13178_y25409.json',
	'236174_3329_x13938_y26099': './cells/new_cell_jsons/236174_3329_x13938_y26099.json',
	'18453_3186_x12745_y7108': './cells/new_cell_jsons/18453_3186_x12745_y7108.json',
	'18453_3456_x24161_y6646': './cells/new_cell_jsons/18453_3456_x24161_y6646.json',
	'18453_3767_x22604_y5643': './cells/new_cell_jsons/18453_3767_x22604_y5643.json',
	'18453_3795_x13584_y5960': './cells/new_cell_jsons/18453_3795_x13584_y5960.json',
	'18453_4067_x16924_y5288': './cells/new_cell_jsons/18453_4067_x16924_y5288.json',
	'18453_4221_x16935_y5165': './cells/new_cell_jsons/18453_4221_x16935_y5165.json',
	'18461_4178_x16825_y2713': './cells/new_cell_jsons/18461_4178_x16825_y2713.json',
	'18864_3473_x2641_y21082': './cells/new_cell_jsons/18864_3473_x2641_y21082.json',
	'18864_4120_x3320_y13563': './cells/new_cell_jsons/18864_4120_x3320_y13563.json',
	'18864_4157_x3358_y13741': './cells/new_cell_jsons/18864_4157_x3358_y13741.json',
	'18864_4267_x2794_y21031': './cells/new_cell_jsons/18864_4267_x2794_y21031.json',
	'18864_3338_x3396_y21865': './cells/new_cell_jsons/18864_3338_x3396_y21865.json',
	'18864_4067_x3464_y21495': './cells/new_cell_jsons/18864_4067_x3464_y21495.json',
	'AA0010 [A]': './cells/split_cells/AA0010.json',
	'AA0037 [A]': './cells/split_cells/AA0037.json',
	'AA0112 [A]': './cells/split_cells/AA0112.json',
	'AA0276 [A]': './cells/split_cells/AA0276.json',
	'AA0287 [A]': './cells/split_cells/AA0287.json',
	'AA0664 [A]': './cells/split_cells/AA0664.json',
	'AA0774 [A]': './cells/split_cells/AA0774.json',
	'AA0224 [A]': './cells/split_cells/AA0224.json',
	'AA0543 [A]': './cells/split_cells/AA0543.json',
	'18453_2645_x28684_y11703': './cells/new_cell_jsons/18453_2645_x28684_y11703.json',
	'18453_2713_x27713_y9899': './cells/new_cell_jsons/18453_2713_x27713_y9899.json',
	'18864_3015_x3194_y23588': './cells/new_cell_jsons/18864_3015_x3194_y23588.json',
	'AA0002 [A]': './cells/split_cells/AA0002.json',
	'AA0004 [A]': './cells/split_cells/AA0004.json',
	'AA0035 [A]': './cells/split_cells/AA0035.json',
	'AA0036 [A]': './cells/split_cells/AA0036.json',
	'AA0046 [A]': './cells/split_cells/AA0046.json',
	'AA0102 [A]': './cells/split_cells/AA0102.json',
	'AA0108 [A]': './cells/split_cells/AA0108.json',
	'AA0271 [A]': './cells/split_cells/AA0271.json',
	'AA0272 [A]': './cells/split_cells/AA0272.json',
	'AA0289 [A]': './cells/split_cells/AA0289.json',
	'AA0440 [A]': './cells/split_cells/AA0440.json',
	'AA0578 [A]': './cells/split_cells/AA0578.json',
	'AA0588 [A]': './cells/split_cells/AA0588.json',
	'AA0745 [A]': './cells/split_cells/AA0745.json',
	'AA0005 [A]': './cells/split_cells/AA0005.json',
	'AA0040 [A]': './cells/split_cells/AA0040.json',
	'AA0042 [A]': './cells/split_cells/AA0042.json',
	'AA0062 [A]': './cells/split_cells/AA0062.json',
	'AA0107 [A]': './cells/split_cells/AA0107.json',
	'AA0225 [A]': './cells/split_cells/AA0225.json',
	'17781_3668_x9453_y17266': './cells/new_cell_jsons/17781_3668_x9453_y17266.json',
	'17782_3352_x11384_y16404': './cells/new_cell_jsons/17782_3352_x11384_y16404.json',
}

lookup = {'182725_2376_x10033_y10786':1,
'182725_3762_x5563_y19178':1,
'182725_4080_x6576_y11407':1,
'18868_3009_x28076_y11485':1,
'18868_3488_x24952_y7321':1,
'AA0114 [A]':1,
'AA0131 [A]':1,
'AA0132 [A]':1,
'AA0133 [A]':1,
'AA0134 [A]':1,
'AA0135 [A]':1,
'AA0169 [A]':1,
'AA0261 [A]':1,
'AA0584 [A]':1,
'AA0587 [A]':1,
'AA0617 [A]':1,
'AA0923 [A]':1,
'AA0926 [A]':1,
'AA0927 [A]':1,
'18867_2903_x13633_y8787':2,
'18867_3758_x14594_y6944':2,
'AA0553 [A]':2,
'AA0644 [A]':3,
'AA0863 [A]':3,
'210254_2226_x16029_y23953':3,
'210254_2309_x13266_y25533':3,
'210254_4397_x16794_y21812':3,
'210254_4485_x16442_y16836':3,
'210254_4500_x16614_y17147':3,
'AA0038 [A]':3,
'AA0041 [A]':3,
'AA0043 [A]':3,
'AA0185 [A]':3,
'AA0187 [A]':3,
'AA0398 [A]':3,
'AA0545 [A]':3,
'AA0548 [A]':3,
'AA0596 [A]':3,
'AA0605 [A]':3,
'AA0623 [A]':3,
'AA0626 [A]':3,
'AA0628 [A]':3,
'AA0630 [A]':3,
'AA0634 [A]':3,
'AA0635 [A]':3,
'AA0637 [A]':3,
'AA0640 [A]':3,
'AA0641 [A]':3,
'AA0642 [A]':3,
'AA0647 [A]':3,
'AA0648 [A]':3,
'AA0649 [A]':3,
'AA0652 [A]':3,
'AA0654 [A]':3,
'AA0667 [A]':3,
'AA0770 [A]':3,
'AA0785 [A]':3,
'AA0833 [A]':3,
'AA0836 [A]':3,
'AA0898 [A]':3,
'18864_3494_x2380_y13749':4,
'AA0034 [A]':4,
'AA0064 [A]':4,
'AA0065 [A]':4,
'AA0099 [A]':4,
'AA0130 [A]':4,
'AA0184 [A]':4,
'AA0442 [A]':4,
'AA0600 [A]':4,
'AA0656 [A]':4,
'AA0906 [A]':4,
'AA0060 [A]':4,
'AA0140 [A]':4,
'AA0401 [A]':4,
'AA0404 [A]':4,
'AA0408 [A]':4,
'AA0463 [A]':4,
'AA0464 [A]':4,
'AA0541 [A]':4,
'AA0739 [A]':4,
'AA0741 [A]':4,
'AA0876 [A]':4,
'17109_2301_x8535_y23051':4,
'17109_2401_x8977_y24184':4,
'17781_2881_x4240_y36304':4,
'236174_2801_x11376_y11451':4,
'236174_3029_x12820_y24699':4,
'236174_3029_x13178_y25409':4,
'236174_3329_x13938_y26099':4,
'18453_3186_x12745_y7108':5,
'18453_3456_x24161_y6646':5,
'18453_3767_x22604_y5643':5,
'18453_3795_x13584_y5960':5,
'18453_4067_x16924_y5288':5,
'18453_4221_x16935_y5165':5,
'18461_4178_x16825_y2713':5,
'18864_3473_x2641_y21082':5,
'18864_4120_x3320_y13563':5,
'18864_4157_x3358_y13741':5,
'18864_4267_x2794_y21031':5,
'18864_3338_x3396_y21865':5,
'18864_4067_x3464_y21495':5,
'AA0010 [A]':5,
'AA0037 [A]':5,
'AA0112 [A]':5,
'AA0276 [A]':5,
'AA0287 [A]':5,
'AA0664 [A]':5,
'AA0774 [A]':5,
'AA0224 [A]':5,
'AA0543 [A]':5,
'18453_2645_x28684_y11703':6,
'18453_2713_x27713_y9899':6,
'18864_3015_x3194_y23588':6,
'AA0002 [A]':6,
'AA0004 [A]':6,
'AA0035 [A]':6,
'AA0036 [A]':6,
'AA0046 [A]':6,
'AA0102 [A]':6,
'AA0108 [A]':6,
'AA0271 [A]':6,
'AA0272 [A]':6,
'AA0289 [A]':6,
'AA0440 [A]':6,
'AA0578 [A]':6,
'AA0588 [A]':6,
'AA0745 [A]':6,
'AA0005 [A]':6,
'AA0040 [A]':6,
'AA0042 [A]':6,
'AA0062 [A]':6,
'AA0107 [A]':6,
'AA0225 [A]':6,
'17781_3668_x9453_y17266':6,
'17782_3352_x11384_y16404':6,
}

left_neurons = ['18864_3494_x2380_y13749',
 'AA0034 [A]',
 'AA0099 [A]',
 '17109_2301_x8535_y23051',
 '17109_2401_x8977_y24184',
 '17781_2881_x4240_y36304',
 '236174_2801_x11376_y11451',
 '236174_3029_x12820_y24699',
 '236174_3029_x13178_y25409',
 '236174_3329_x13938_y26099',
 '18453_3186_x12745_y7108',
 '18453_3456_x24161_y6646',
 '18453_3767_x22604_y5643',
 '18453_3795_x13584_y5960',
 '18453_4067_x16924_y5288',
 '18453_4221_x16935_y5165',
 '18461_4178_x16825_y2713',
 '18864_3473_x2641_y21082',
 '18864_4120_x3320_y13563',
 '18864_4157_x3358_y13741',
 '18864_4267_x2794_y21031',
 '18864_3338_x3396_y21865',
 '18864_4067_x3464_y21495',
 'AA0010 [A]',
 'AA0037 [A]',
 'AA0112 [A]',
 'AA0224 [A]',
 '18453_2645_x28684_y11703',
 '18453_2713_x27713_y9899',
 '18864_3015_x3194_y23588',
 'AA0002 [A]',
 'AA0004 [A]',
 'AA0035 [A]',
 'AA0036 [A]',
 'AA0046 [A]',
 'AA0102 [A]',
 'AA0108 [A]',
 'AA0005 [A]',
 'AA0040 [A]',
 'AA0042 [A]',
 'AA0107 [A]',
 'AA0225 [A]',
 '17781_3668_x9453_y17266',
 '17782_3352_x11384_y16404',]

cmap = ['lawngreen', 'darkolivegreen', 'yellowgreen', 'fuchsia', 'red', 'burlywood', 'darkorange', 'oldlace', 'chocolate', 'red', 'violet', 'magenta', 'steelblue', 'oldlace', 'aquamarine', 'mintcream', 'skyblue', 'darkgoldenrod', 'lightgreen', 'papayawhip', 'powderblue', 'hotpink', 'mistyrose', 'darkviolet', 'crimson', 'palevioletred', 'lightcoral', 'darkseagreen', 'rebeccapurple', 'darkviolet', 'wheat', 'lightsteelblue', 'forestgreen', 'indigo', 'maroon', 'darkgreen', 'ivory', 'darkslateblue']

groups = {1:[],2:[],3:[],4:[],5:[],6:[],12:[]}
for k,v in lookup.items():
	if v == 1:
		groups[1].append(k)
		groups[12].append(k)
	elif v== 2:
		groups[2].append(k)
		groups[12].append(k)
	elif v == 3:
		groups[3].append(k)
	elif v == 4:
		groups[4].append(k)
	elif v==5:
		groups[5].append(k)
	elif v==6:
		groups[6].append(k)

def get_point(fp):
	with open(fp) as f:
		temp = json.load(f)

	print(len(temp['neurons']))

	x = temp['neurons'][0]['soma']['x']
	y = temp['neurons'][0]['soma']['y']
	z = temp['neurons'][0]['soma']['z']

	return (x,y,z)

for k,vlist in groups.items():
	if k not in [1,3,2,12]:
		screenshot_params = dict(
		folder = './screenshots/single_cell_views',
		name='top_cluster_{0}'.format(k),
		)
		scene = Scene(display_inset=False, screenshot_kwargs=screenshot_params)
		for i,neuron in enumerate(vlist):
			if neuron not in left_neurons:
				fp = cell_filepaths[neuron]
			else:
				fp = cell_filepaths[neuron].split('.json')[0] + '_reversed.json'
			scene.add_neurons(fp, soma_color=cmap[i], render_axons=True, render_dendrites=True, dendrites_color=cmap[i], 
	                axon_color=cmap[i], neurite_radius=18)
			# pos = get_point(fp)
			# print(pos)
			# scene.add_sphere_at_point(pos=pos, radius= 75, color=cmap[i])	
		scene.render(interactive=False,camera='top', zoom=1)
		scene.take_screenshot()
		