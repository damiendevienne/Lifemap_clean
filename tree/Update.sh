#!/bin/bash
cd /usr/local/lifemap/
source TREEOPTIONS
updatecommand="sudo ./Main.py --lang $lang --simplify $simplify"
eval "$updatecommand"
echo "DONE"



