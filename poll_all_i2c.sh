for snap in $@; do (./poll_i2c.sh $snap >> i2c_poll.$snap.log.cpt &) ; done
