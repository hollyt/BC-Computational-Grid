#!/bin/bash

# This script sets up host-guest ensembles for the BOINC grid
# USAGE: ./setup-ensembles.sh -n <ligand name>

OPTIND=1        # Reset incase getopts has been used previously in this shell

# Parse ligand name
while getopts ":n:" opt; do
    case $opt in
        n)
            echo "Ligand: $OPTARG"
            ;;
        \?)
            echo "Usage: ./setup-ensembles.sh -n <lig name>"
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument: name of ligand."
            exit 1
            ;;
    esac

    for ((i=0; i <= 99; i++))
    do
        cd r$i
        echo "Setting up r$i ..."
        mv bcd_r*.dms bcd-${OPTARG}_rcpt.dms
        cp ../agbnp2.param .
        cp ../bcd-${OPTARG}_0.rst .
        cp ../bcd-${OPTARG}_cmrestraint.dat .
        cp ../bcd-$OPTARG.cntl .
        cp ../bcd-$OPTARG.inp .
        cp ../bcd-${OPTARG}_restdist.dat .
        cp ../bcd-${OPTARG}_resttor.dat .
        cp ../paramstd.dat .
        python ~/guest_host/rotate_translate.py bcd_${OPTARG}_rcpt.dms bcd-${OPTARG}_lig.dms 6.0
        echo "r$i done."
        cd ..
    done

    echo "$OPTARG setup complete."
done
