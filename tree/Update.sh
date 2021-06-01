#!/bin/bash
source TREEOPTIONS
updatecommand="sudo ./Main.py --lang $lang --simplify $simplify --removeextinct $removeextinct"
eval "$updatecommand"
echo "DONE"



