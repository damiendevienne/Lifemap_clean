#!/bin/bash
source TREEOPTIONS
updatecommand="sudo ./Main.py --lang $lang --simplify $simplify"
eval "$updatecommand"
echo "DONE"



