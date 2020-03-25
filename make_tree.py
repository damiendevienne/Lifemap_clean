#!/usr/bin/python

import sys,os
from argparse import ArgumentParser, FileType ##for options handling

parser = ArgumentParser(description='Run all script to get have data ready to explore with Lifemap.')
parser.add_argument('--lang', nargs='?', help='Language chosen. FR for french, EN (default) for english', choices=['EN','FR'])
parser.add_argument('--simplify', nargs='?', help='Should the tree be simplified by removing environmental and unindentified species?', choices=['True','False'])
args = parser.parse_args()

#write the options chosen to a parameters file for later updates with same options
f= open("/usr/local/lifemap/TREEOPTIONS","w")
f.write("#!/bin/sh\nlang=\"%s\"\nsimplify=\"%s\"\n"%(args.lang, args.simplify))
f.close()
os.system("(cd /usr/local/lifemap/ ; sudo ./Main.py --lang %s --simplify %s)" % (args.lang,args.simplify))




