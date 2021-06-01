#!/usr/bin/python

# from ete3 import Tree
import os
# import cPickle as pickle

def getTheTrees():
	class Trans:
		def __init__(self):
			self.common_name_FR = []

	print "Getting french translations..."
	os.system("sudo wget -O taxo/TAXONOMIC-VERNACULAR-FR.txt https://github.com/damiendevienne/taxonomy-fr/blob/master/TAXONOMIC-VERNACULAR-FR.txt?raw=true")
	TRANS = {} ##translations in french
	with open("taxo/TAXONOMIC-VERNACULAR-FR.txt") as f:
		for line in f:
			sciname = line.split("\t")[0]
			comnameFR = line.split("\t")[1].rstrip()
			if (TRANS.has_key(sciname)==False):
				TRANS[sciname] = Trans()
			TRANS[sciname].common_name_FR.append(comnameFR)


	#get translation of ranks
	print "\nGetting rank names in french..."
	RANKS = {}
	with open("taxo/ranks.txt") as f:  
		for line in f:
			rank_en = line.split("\t")[0]
			rank_fr = line.split("\t")[1].rstrip() ##to remove \n
			RANKS[rank_en] = rank_fr

	#get list of extinct species
	EXT = [];
	with open("taxo/citations.dmp") as f:
		for line in f:
			if (line.split("\t")[2]=="extinct"):
				EXT = line.split("\t")[12].split(" ");


	class Taxid:
		def __init__(self):
			self.sci_name = ""
			self.authority = ""
			self.synonym = ""
#			self.common_name = ""
			self.common_name = []
#			self.common_name_FR = ""
			self.common_name_FR = []
			self.extinct = "F"

	cpt = 0
	cptfr = 0
	ATTR = {} ##here we will list attribute of each species per taxid
	print "Reading NCBI taxonomy..."
	with open("taxo/names.dmp") as f:  
		for line in f:		
			taxid = line.split("|")[0].replace("\t","")
			tid_val = line.split("|")[1].replace("\t","")
			tid_type = line.split("|")[3].replace("\t","")
			if (ATTR.has_key(taxid)==False):
				ATTR[taxid] = Taxid()
			if (tid_type=="scientific name"):
				ATTR[taxid].sci_name = tid_val
				#and get translation in french (if any)
				if TRANS.has_key(tid_val):
					ATTR[taxid].common_name_FR = TRANS[tid_val].common_name_FR
					cptfr += 1
			if (tid_type=="authority"):
				if (ATTR[taxid].authority!=""):
					ATTR[taxid].authority = ATTR[taxid].authority + ", " + tid_val
				else:
					ATTR[taxid].authority = tid_val
			if (tid_type=="synonym"):
				if (ATTR[taxid].synonym!=""):
					ATTR[taxid].synonym = ATTR[taxid].synonym + ", " + tid_val
				else:
					ATTR[taxid].synonym = tid_val
			if (tid_type=="common name"):
				cpt +=1
				ATTR[taxid].common_name.append(tid_val)
                        if (tid_type=="genbank common name"):
                                cpt +=1
                                ATTR[taxid].common_name.append(tid_val)

				# if (ATTR[taxid].common_name!=""):
				# 	ATTR[taxid].common_name = ATTR[taxid].common_name + ", " + tid_val
				# else: 
				# 	ATTR[taxid].common_name = tid_val

	#add info about extinction state in the ATTR objects
	for x in EXT:
		if (ATTR.has_key(x)==True):
			ATTR[x].extinct = "T"





	T = {}

	###New gettrees
	from ete3 import Tree
	filepath = 'taxo/nodes.dmp'  
	print "Building the NCBI taxonomy tree..."
	with open(filepath) as fp:  
		first_line = fp.readline() ## remove the 1 | 1 edge
		for line in fp:
			dad = line.split("|")[1].replace("\t","")
			son = line.split("|")[0].replace("\t","")
			rank = line.split("|")[2].replace("\t","") ##rank OF THE SON!
			if (T.has_key(dad)==False):
				T[dad] = Tree()
				T[dad].name = dad
#				T[dad].rank = rank
#				T[dad].rank_FR = RANKS[rank]
				T[dad].taxid = dad
				T[dad].sci_name = ATTR[dad].sci_name
				T[dad].common_name = ATTR[dad].common_name
				T[dad].synonym = ATTR[dad].synonym
				T[dad].authority = ATTR[dad].authority
				T[dad].common_name_FR = ATTR[dad].common_name_FR
				##extinct status of dad
				T[dad].extinct = ATTR[dad].extinct
			if (T.has_key(son)==False):
				T[son] = Tree()
				T[son].name = son
				T[son].rank = rank
				T[son].rank_FR = RANKS[rank]
				T[son].taxid = son
				T[son].sci_name = ATTR[son].sci_name
				T[son].common_name = ATTR[son].common_name
				T[son].synonym = ATTR[son].synonym
				T[son].authority = ATTR[son].authority
				T[son].common_name_FR = ATTR[son].common_name_FR
				T[son].extinct = ATTR[son].extinct

			else:
				if (hasattr(T[son], 'rank')==False):
					T[son].rank = rank
					T[son].rank_FR = RANKS[rank]
			T[dad].add_child(T[son])
	#Desambiguation
	T['54972'].rank_FR = "" #because those are birds, not "sabline" flowers


	return T

# ##we save T entirely so that we do not hacve to write it to a file.
# print("\n>>> Writing ARCHAEA tree...")
# with open('ARCHAEA.pkl', 'wb') as output:
#     pickle.dump(T['2157'], output, pickle.HIGHEST_PROTOCOL)
# print("\n>>> Writing BACTERIA tree...")
# with open('BACTERIA.pkl', 'wb') as output:
#     pickle.dump(T['2'], output, pickle.HIGHEST_PROTOCOL)
# print("\n>>> Writing EUKA tree...")
# with open('EUKARYOTES.pkl', 'wb') as output:
#     pickle.dump(T['2759'], output, pickle.HIGHEST_PROTOCOL)
# print(">>> DONE")


# #t = T['1']
# tarc = T['2157']
# tbac = T['2']
# teuc = T['2759']

# print("\n>>> Writing ARCHAEA tree...")
# tarc.write(outfile = "ARCHAEA", features = ["name", "taxid", "sci_name","common_name","rank", "authority","synonym","common_name_FR", "rank_FR"], format_root_node=True)
# print("\n>>> Writing BACTERIA tree...")
# tbac.write(outfile = "BACTERIA", features = ["name", "taxid", "sci_name","common_name","rank", "authority","synonym","common_name_FR", "rank_FR"], format_root_node=True)
# print("\n>>> Writing EUKA tree...")
# teuc.write(outfile = "EUKARYOTES", features = ["name", "taxid", "sci_name","common_name","rank", "authority","synonym","common_name_FR", "rank_FR"], format_root_node=True)
# print(">>> DONE")




# RANKS = {}

# for n in t.traverse(): 
# 	if RANKS.has_key(n.rank)== False:
# 		RANKS[n.rank] = 1
# 	else: 
# 		RANKS[n.rank] = RANKS[n.rank] + 1

# ranks = open("ranks.txt", "w")
# for k in RANKS:
# 	ranks.write("%s\t%s\n" % (k,RANKS[k]))

# ranks.close()
