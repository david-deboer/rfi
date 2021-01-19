#! /usr/bin/env python
from __future__ import print_function

#import os
import subprocess

with open('CurrentNode.txt', 'r') as fp:
    current_node = fp.read()

poll_all = './poll_all_i2c.sh heraNode{}Snap{{0..3}}'.format(current_node)
pa_cmd = './poll_all_i2c.sh'
pa_arg = 'heraNode{}Snap{{0..3}}'.format(current_node)
print("Making noise with {}".format(pa_arg))
#os.system(poll_all)
subprocess.run([pa_cmd, pa_arg], shell=True)
