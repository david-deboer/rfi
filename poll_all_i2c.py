import subprocess
import sys

for snap in sys.argv[1:]:
    print "starting i2c poll for snap %s" % snap
    subprocess.Popen(["/home/jackh/rfi/poll_i2c.sh", "%s" %snap], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
