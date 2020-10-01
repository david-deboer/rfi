#! /usr/bin/env python
from __future__ import print_function

import os

with open('CurrentNode.txt', 'r') as fp:
    current_node = fp.read()

init_file = './hera_snap_feng_init_rfi.py'
yaml_file = 'hera_feng_rfi_config_node{}.yaml'.format(current_node)
args = '-p -e -s -i --config_file'

os.system('{} {} {}'.format(init_file, args, yaml_file))
