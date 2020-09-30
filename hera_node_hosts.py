#! /usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys
import six
import time

ap = argparse.ArgumentParser()
ap.add_argument('snap0', help="SNAP serial number. E.g. 42")
ap.add_argument('snap1', help="SNAP serial number. E.g. 43")
ap.add_argument('snap2', help="SNAP serial number. E.g. 54")
ap.add_argument('snap3', help="SNAP serial number. E.g. 7")
ap.add_argument('-n', '--node_num', help="Node number. E.g. 10")
ap.add_argument('--hosts_file', help="__Shouldn't need to change__  Name of hosts file.",
                default="/etc/hosts")
ap.add_argument('--snap_rev', help="__Shouldn't need to change__  Rev letter of SNAP (csv-list).  "
                "If one supplied, it applies to all.", default='C')
ap.add_argument('--dont_reset_dnsmasq', dest='reset_dnsmasq', help="Don't reset the dnsmasq",
                action='store_false')
args = ap.parse_args()
snap_rev = args.snap_rev.upper().split(",")
if len(snap_rev) == 1:
    snap_rev = snap_rev * 4

hard-code MAC etc and populate hosts/ethers

snaps = {}
for i in range(4):
    snpi = 'heraNode{}Snap{}'.format(args.node_num, i)
    snaps[snpi] = 'SNP{}{:06d}'.format(snap_rev[i], int(getattr(args, 'snap{}'.format(i))))
with open('CurrentNode.txt', 'w') as fp:
    fp.write(args.node_num)

print("This will rewrite {} with".format(args.hosts_file))
for loc, snr in snaps.items():
    print("\t{} --> {}".format(snr, loc))
yn = six.moves.input("Do you want to proceed (y/n):  ")
if yn[0].lower() != 'y':
    print("Quitting without change.")
    sys.exit()
backup_host_file = ('{}.backup_etc_hosts{}'
                    .format(os.path.basename(args.hosts_file), int(time.time())))
print("Backing up to {}".format(backup_host_file))
os.system('cp {} {}'.format(args.hosts_file, backup_host_file))
update_counter = 0

with open(backup_host_file, 'r') as fpin:
    with open(args.hosts_file, 'w') as fpout:
        for line in fpin:
            # Check overall conditions to not update line.
            if line[0] == '#' or 'SNP' not in line:
                fpout.write("{}".format(line))
                continue
            data = line.split()
            if len(data) < 2 or len(data) > 3:
                fpout.write("{}".format(line))
                continue
            # Check if heraNodeXSnapY already present.  If so, remove from line.
            if len(data) == 3:
                for loc in snaps.keys():
                    if loc == data[2]:
                        print("Removing existing {}".format(line.strip()))
                        line = '{} {}\n'.format(data[0], data[1])
                        break
            # Check if SNPC0000NN and add heraNodeXSnapY if found.
            for loc, snr in snaps.items():
                if snr == data[1]:
                    new_line = '{} {}  {}\n'.format(data[0], data[1], loc)
                    fpout.write(new_line)
                    print("{:50s}  -->  {}".format(line.strip(), new_line.strip()))
                    update_counter += 1
                    break
            else:
                fpout.write("{}".format(line))

if update_counter != 4:
    args.reset_dnsmasq = False
    print("""
    !!!                         WARNING                         !!!
    There were {} not 4 snaps updated.   Turning off reset dnsmasq.
    Double-check the node/snap numbers you provided.
     - If correct, you'll need to edit the file {} and then run
       './reset_dnsmasq.sh'
     - If not, rerun this script with the correct values.
    """.format(update_counter, args.hosts_file))

if args.reset_dnsmasq:
    os.system('sudo /etc/init.d/dnsmasq stop')
    os.system('sudo rm /var/lib/misc/dnsmasq.leases')
    os.system('sudo /etc/init.d/dnsmasq start')
