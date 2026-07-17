#!/bin/bash
#PBS -q DEFAULT
#PBS -j oe
#PBS -l select=4:ncpus=16:mpiprocs=16:mem=15GB
#PBS -l place=scatter
#PBS -N ZPE
#PBS -V

cd $PBS_O_WORKDIR

# DEFAULT MAX 64 core
# SINGLE MAX 128 core
# https://www.jaist.ac.jp/iscenter/en/mpc/kagayaki/2/#c5869
# chuck size per select 16 core, pake 8 node

module purge
module load oneapi-intel

version=7.2
binary=pw.x

espresso=/home/hongo/hongo-group/applications/qe-${version}/bin/${binary}

mpirun -machinefile ${PBS_NODEFILE} -np 64 $espresso -in PWINPUT_atm158_xp > LOG_atm158_xp
mpirun -machinefile ${PBS_NODEFILE} -np 64 $espresso -in PWINPUT_atm158_ym > LOG_atm158_ym

