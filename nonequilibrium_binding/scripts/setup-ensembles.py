#/usr/bin/python

"""
This script sets up replica directories for all guest-host systems.
It choose a random receptor molecule and random ligand molecule
from the directory of given .dms files, and creates a new replica
directory for each ensemble.
"""
#TODO:
# * add the rest of the files needed for simulation to the replica dirs
# * rename .dms files in format: rcpt-lig.dms
# * clean up the creation of the lig_type dirs

import argparse
import os
import random
import shutil

def choose_ensemble(rcpt,lig,replica,lig_type,nreplicas):
    replica_path = os.path.abspath(replica + lig_type)
    os.mkdir(replica_path,0777)
    for x in range(nreplicas):
        # choose a random receptor file
        rcpt_file = rcpt + random.choice(os.listdir(rcpt))
        # choose a random ligand file
        lig_file = lig + '/' + random.choice(os.listdir(lig))
        # move to new replica dir
        replica_src = replica_path + '/r{}'.format(x)
        os.mkdir(replica_src,0777)
        shutil.copy(rcpt_file,replica_src)
        shutil.copy(lig_file,replica_src)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receptor_path', type=str, default='./receptors/bcd/', help='path where receptor directories are found (default: ./receptors/bcd/')
    parser.add_argument('--ligand_path', type=str, default='./ligands', help='path where ligand directories are found (default: ./ligands')
    parser.add_argument('--replica_path', type=str, default='./replicas/', help='path to directory where replica directories should be placed (default: ./replicas')
    parser.add_argument('--nreplicas', type=int, default=100, help='number of replica directories to create (default: 100)')
    args = parser.parse_args()

    os.mkdir(os.path.abspath(args.replica_path))

    for lig_type in os.listdir(args.ligand_path):
        # find a better way to make lig_type dir
        choose_ensemble(args.receptor_path,os.path.join(args.ligand_path,lig_type),args.replica_path,lig_type,args.nreplicas)

if __name__ == '__main__':
    main()
