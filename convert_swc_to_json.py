import json
import os

# Find and parse swc files in directory
filenames = []
for file in os.listdir('./cells/new_cells/'):
    if file.split('.')[1] == 'swc':
        filenames.append(file)

for file in filenames:
    with open('./cells/new_cells/{}'.format(file)) as f:
        cell_txt = f.read().split('\n')
    
    cell_split = [x.split('\t') for x in cell_txt]
    
    if len(cell_split[-2]) == 1:
        cell_split = [x.split() for x in cell_txt]
        
    for i,line in enumerate(cell_split):
        if not line[0].startswith('#'):
            break
    


    # Create JSON for cell in their original hemisphere
    soma = []
    axons = []
    dendrites = []
    type_list = []
    for line in cell_split[i:]:
        try:
            if line[1] not in type_list:
                type_list.append(line[1])
            if line[1] == '1':
                soma.append(line)
            elif line[1] == '2':
                axons.append(line)
            else:
                dendrites.append(line)
        except:
            pass
            
    try:
        axon_list = [{'parentNumber':int(pID),'radius':float(r),'sampleNumber':int(ID),'x':float(z)*25,'y':float(y)*25,'z':float(x)*25} for ID,typeid,x,y,z,r,pID in axons]
        dendrite_list = [{'parentNumber':int(pID),'radius':float(r),'sampleNumber':int(ID),'x':456-float(z)*25,'y':float(y)*25,'z':float(x)*25} for ID,typeid,x,y,z,r,pID in dendrites]
        soma_list =[{'parentNumber':int(pID),'radius':float(r),'sampleNumber':int(ID),'x':456-float(z)*25,'y':float(y)*25,'z':float(x)*25} for ID,typeid,x,y,z,r,pID in soma]

        
        lookup = {axon_list[v]['sampleNumber']:v+1 for v in range(len(axon_list))}
        for n in axon_list:
            try:
                n['parentNumber'] = lookup[n['parentNumber']]
            except:
                n['parentNumber'] = -1

            n['sampleNumber'] = lookup[n['sampleNumber']]

        
        lookup = {dendrite_list[v]['sampleNumber']:v+1 for v in range(len(dendrite_list))}
        for n in dendrite_list:
            try:
                n['parentNumber'] = lookup[n['parentNumber']]
            except:
                n['parentNumber'] = -1

            n['sampleNumber'] = lookup[n['sampleNumber']]
        
        
        
        
        
        cell_recon = {'neurons':[{'idString':file,'soma':soma_list[0],
             'axon':axon_list, 'dendrite':dendrite_list}]}
        
        print(file)
        
        with open('./cells/new_cell_jsons/{}.json'.format(file.split('.')[0]),'w') as f:
            json.dump(cell_recon,f)
    except:
        print(file,type_list)





    # Create JSON for cell flipped to the opposite hemisphere        
    soma = []
    axons = []
    dendrites = []
    type_list = []
    for line in cell_split[i:]:
        try:
            if line[1] not in type_list:
                type_list.append(line[1])
            if line[1] == '1':
                soma.append(line)
            elif line[1] == '2':
                axons.append(line)
            else:
                dendrites.append(line)
        except:
            pass
            
    try:
        axon_list = [{'parentNumber':int(pID),'radius':float(r),'sampleNumber':int(ID),'x':(456-float(z))*25,'y':float(y)*25,'z':float(x)*25} for ID,typeid,x,y,z,r,pID in axons]
        dendrite_list = [{'parentNumber':int(pID),'radius':float(r),'sampleNumber':int(ID),'x':(456-float(z))*25,'y':float(y)*25,'z':float(x)*25} for ID,typeid,x,y,z,r,pID in dendrites]
        soma_list =[{'parentNumber':int(pID),'radius':float(r),'sampleNumber':int(ID),'x':(456-float(z))*25,'y':float(y)*25,'z':float(x)*25} for ID,typeid,x,y,z,r,pID in soma]

        
        lookup = {axon_list[v]['sampleNumber']:v+1 for v in range(len(axon_list))}
        for n in axon_list:
            try:
                n['parentNumber'] = lookup[n['parentNumber']]
            except:
                n['parentNumber'] = -1

            n['sampleNumber'] = lookup[n['sampleNumber']]

        
        lookup = {dendrite_list[v]['sampleNumber']:v+1 for v in range(len(dendrite_list))}
        for n in dendrite_list:
            try:
                n['parentNumber'] = lookup[n['parentNumber']]
            except:
                n['parentNumber'] = -1

            n['sampleNumber'] = lookup[n['sampleNumber']]
        
        
        
        
        
        cell_recon = {'neurons':[{'idString':file,'soma':soma_list[0],
             'axon':axon_list, 'dendrite':dendrite_list}]}
        
        print(file)
        
        with open('./cells/new_cell_jsons/{}_reversed.json'.format(file.split('.')[0]),'w') as f:
            json.dump(cell_recon,f)
    except:
        print(file,type_list)