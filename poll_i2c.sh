#! /bin/bash

#hosts=('heranode1snap0' 'heranode1snap1' 'heranode1snap2' 'heranode1snap3')

i2c_ants=('i2c_ant0' 'i2c_ant1' 'i2c_ant2' )
#pam_sens=('--atten' '--rom' '--volt' '--id')
pam_sens=('--atten' '--volt' '--id')
fem_sens=('--volt' '--temp' '--bar' '--imu' '--switch')

# polling FEM '--rom' takes ages, when FEM ROM is empty
#fem_sens=('--rom' '--volt' '--temp' '--bar' '--imu' '--switch')


while true
do
    date
    for pam_sen in "${pam_sens[@]}"
    do
        for i2c_ant in "${i2c_ants[@]}"
        do
            echo "Polling $pam_sen in PAM, $i2c_ant, $1"
            python ./snapcorr_sensor_pam.py $1 --i2c $i2c_ant 10 100 $pam_sen
        done
    done
        
    for fem_sen in "${fem_sens[@]}"
    do
        for i2c_ant in "${i2c_ants[@]}"
        do
            echo "Polling $fem_sen in FEM, $i2c_ant, $1"
            python ./snapcorr_sensor_fem.py $1 --i2c $i2c_ant 10 100 $fem_sen
        done
    done
done
