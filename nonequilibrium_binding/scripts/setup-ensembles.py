#/usr/bin/python

"""
This script sets up replica directories for all guest-host systems.
It choose a random receptor molecule and random ligand molecule
from the directory of given .dms files, and creates a new replica
directory for each ensemble.
"""
#TODO:
# * add command line argument parsing for paths, number of replicas
# * add the rest of the files needed for simulation to the replica dirs
# * rename .dms files in format: rcpt-lig.dms
# * clean up the creation of the lig_type dirs

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
    # we only have 1 receptor (bcd) at the moment
    rcptpath = './receptors/bcd/'
    ligpath = './ligands/'
    replicapath = './replicas/'
    nreplicas = 100

    os.mkdir(os.path.abspath(replicapath))

    for lig_type in os.listdir(ligpath):
        # find a better way to make lig_type dir
        choose_ensemble(rcptpath,os.path.join(ligpath,lig_type),replicapath,lig_type,nreplicas)

if __name__ == '__main__':
    main()
