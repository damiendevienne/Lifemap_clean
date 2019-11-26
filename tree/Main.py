#!/usr/bin/python

import sys,os
from argparse import ArgumentParser, FileType ##for options handling

parser = ArgumentParser(description='Perform all Lifemap tree analysis cleaning previous data if any.')
parser.add_argument('--lang', nargs='?', const='EN', default='EN', help='Language chosen. FR for french, EN (default) for english', choices=['EN','FR'])
parser.add_argument('--simplify', nargs='?', const='True', default='False', help='Should the tree be simplified by removing environmental and unindentified species?', choices=['True','False'])
args = parser.parse_args()




##kill render_list (in case it is running)
print "killing render_list"
os.system("sudo killall render_list")
print "ok"
##
os.system("mkdir genomes") ##if not exists
## 1. get the tree and update database
print '\NCREATING DATABASE'
print '  Doing Archaeal tree...'
#os.system('python Traverse_To_Pgsql_2.py 1 1 --simplify False');
os.system('python Traverse_To_Pgsql_2.py 1 1 --simplify %s --lang %s'%(ndid, args.simplify, args.lang));
print '  ...Done'
with open('tempndid', 'r') as f:
    ndid = f.readline()
print '  Doing Eukaryotic tree... start at id: %s' % ndid
os.system('python Traverse_To_Pgsql_2.py 2 %s --updatedb False --simplify %s --lang %s'%(ndid, args.simplify, args.lang) 
print '  ...Done'
with open('tempndid', 'r') as f:
    ndid = f.readline()
print '  Doing Bact tree... start at id:%s ' % ndid
os.system('python Traverse_To_Pgsql_2.py 3 %s --updatedb False --simplify %s --lang %s'%(ndid, args.simplify, args.lang)
print '  ...Done'

## 2. Get additional info from NCBI
print '  Getting addditional Archaeal info...'
os.system('python Additional.info.py 1')
print '  Getting addditional Euka info...'
os.system('python Additional.info.py 2')
print '  Getting addditional Bacter info...'
os.system('python Additional.info.py 3')
print '  ...Done'

##2.1. Get FULL info from NCBI (new sept 2019)
os.system('python StoreWholeNcbiInSolr.py')
print '  ...Done'


## 3. Update Solr informations
print '  Updating Solr... '
os.system('python updateSolr.py')
print '  ...Done '

## 4. Create postgis index
print '  Creating index... '
os.system('python CreateIndex.py')
print '  Done... '

# 5. get and copy date of update to /var/www/html
os.system('sudo ./getDateUpdate.sh')

## 6. Remove old tiles
print '  Deleting old tiles... '
os.system('sudo rm -r /var/lib/mod_tile/default/')

##7. Get New coordinates for generating tiles
os.system('python GetAllTilesCoord.py')
## 7. Restarting the machine 
print 'restart NOW'
os.system('sudo reboot')



##/home/lm/src/Lifemap/PIPELINE/Main.py >> /var/log/lifemap.log

