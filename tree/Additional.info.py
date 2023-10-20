#!/usr/bin/python

import sys,os
from ete3 import Tree

groupnb = sys.argv[1]; ##will be written

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
##                       NOW WE RETRIEVE WHAT WE WILL PUT IN THE JSON FILES
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
if (groupnb=="1"):
    os.system("wget ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/eukaryotes.txt -N")
    os.system("wget ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt -N")
    os.system("mv eukaryotes.txt prokaryotes.txt genomes/")
    t = Tree("ARCHAEA")
if (groupnb=="2"):
    t = Tree("EUKARYOTES")
if (groupnb=="3"):
    t = Tree("BACTERIA")

class genom(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, taxid,size,gc,status):
        self.taxid = [taxid]
        self.size = [size]
        self.gc =[gc]
        self.status =[status]
    def __str__(self):
        return "%d elements " % len(self.taxid)
    def __repr__(self):
        return "%d elements " % len(self.taxid)
    def len(self):
        return self.__len__()
    def append(self,t,si,g,st):
        self.taxid.append(t)
        self.size.append(si)
        self.gc.append(g)
        self.status.append(st)

def make_genom(taxid, size,gc, status):
    gen = genom(taxid, size,gc, status)
    return gen

Genomes = {}
with open("genomes/eukaryotes.txt", "r") as f:
    header=f.readline().strip().split('\t');
    index0 = header.index("TaxID")
    index1 = header.index("Size (Mb)")
    index2 = header.index("GC%")
    index3 = header.index("Status")
    for line in f:
        temp = line.split('\t')
	if len(temp) > index3:
#		print temp[index0] + ' ' + temp[index1] + ' ' + temp[index2] + ' ' + temp[index3]
		if temp[index0] in Genomes:
	            Genomes[temp[index0]].append(temp[index0], temp[index1], temp[index2], temp[index3])
	        else:
	            Genomes.update({temp[index0]:genom(temp[index0], temp[index1], temp[index2], temp[index3])})
with open("genomes/prokaryotes.txt", "r") as f:
    header=f.readline().strip().split('\t');
    index0 = header.index("TaxID")
    index1 = header.index("Size (Mb)")
    index2 = header.index("GC%")
    index3 = header.index("Status")
    for line in f:
        temp = line.split('\t')
	if len(temp) > index3:
#               print temp[index0] + ' ' + temp[index1] + ' ' + temp[index2] + ' ' + temp[index3]
               if temp[index0] in Genomes:
                    Genomes[temp[index0]].append(temp[index0], temp[index1], temp[index2], temp[index3])
               else:
                    Genomes.update({temp[index0]:genom(temp[index0], temp[index1], temp[index2], temp[index3])})


##traverse first time:
for n in t.traverse():
    n.path = [];
    try:
        n.nbgenomes+=0
    except AttributeError:
        n.nbgenomes = 0
    if n.taxid in Genomes:
	nb = len([cpl for cpl in Genomes[n.taxid].status if cpl=="Complete Genome"])
#	print nb
#        nb = len(Genomes[n.taxid].gc)
        try:
            n.nbgenomes += nb
        except AttributeError:
            n.nbgenomes = 0
    node = n
    while node.up:
        try:
            node.up.nbgenomes += n.nbgenomes
        except AttributeError:
            node.up.nbgenomes = 0
        n.path.append(node.up.taxid)
        node = node.up

##traverse to write
jsonAddi = 'ADDITIONAL.'+ groupnb + '.json';
addi = open(jsonAddi,"w");
addi.write('[\n')
for n in t.traverse():
    addi.write("\t{\n");
    addi.write("\t\t\"taxid\":\"%s\",\n" % n.taxid);
    addi.write("\t\t\"ascend\":[");
    for k in n.path:
        addi.write("%s," % k)
    addi.write("0],\n")   
    addi.write("\t\t\"genomes\":\"%d\"\n\t},\n" % n.nbgenomes);
    
##remove unwanted last character(,) of json file
addi.close()
consoleexex = 'head -n -1 ' + jsonAddi + ' > temp.txt ; mv temp.txt '+ jsonAddi;
os.system(consoleexex);
addi = open(jsonAddi,"a");
addi.write("\t}\n]\n")
addi.close()

