#! /usr/bin/env python
from __future__ import print_function

import os

with open('CurrentNode.txt', 'r') as fp:
    current_node = fp.read()

poll_all = './poll_all_i2c.sh heraNode{}Snap{{0..3}}'.format(current_node)

os.system(poll_all)
