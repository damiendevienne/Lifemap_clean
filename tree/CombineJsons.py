#!/usr/bin/python3

import json


def MergeJsons(f1,f2, output):
	with open(f1, 'r') as f:
	    data1 = f.read()

	with open(f2, 'r') as f:
	    data2 = f.read()

	dict1 = json.loads(data1)
	dict2 = json.loads(data2)


	dict2_map = {d['taxid']: d for d in dict2}

	result = []

	# Iterate over each dictionary in dict1 and merge with the corresponding dictionary from dict2_map
	for d1 in dict1:
	    taxid = d1.get('taxid')
	    if taxid in dict2_map:
	        merged_dict = {**d1, **dict2_map[taxid]}
	        result.append(merged_dict)

	with open(output, 'w') as f: 
		json.dump(result, f, indent=4) 


MergeJsons("TreeFeatures1.json", "ADDITIONAL.1.json","TreeFeaturesComplete1.json")
MergeJsons("TreeFeatures2.json", "ADDITIONAL.2.json","TreeFeaturesComplete2.json")
MergeJsons("TreeFeatures3.json", "ADDITIONAL.3.json","TreeFeaturesComplete3.json")


