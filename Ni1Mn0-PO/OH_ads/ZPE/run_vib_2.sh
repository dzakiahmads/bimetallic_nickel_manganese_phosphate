#!/bin/sh
#PBS -q super
#PBS -S /bin/bash
#PBS -N ZPE_OH_NPO
#PBS -l nodes=1:ppn=20
#PBS -j oe

cd $PBS_O_WORKDIR
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/vpl/2021.4.0/lib:/opt/intel/oneapi/tbb/2021.3.0/env/../lib/intel64/gcc4.8:/opt/intel/oneapi/mpi/2021.3.0//libfabric/lib:/opt/intel/oneapi/mpi/2021.3.0//lib/release:/opt/intel/oneapi/mpi/2021.3.0//lib:/opt/intel/oneapi/mkl/2021.3.0/lib/intel64:/opt/intel/oneapi/itac/2021.3.0/slib:/opt/intel/oneapi/ipp/2021.3.0/lib/intel64:/opt/intel/oneapi/ippcp/2021.3.0/lib/intel64:/opt/intel/oneapi/ipp/2021.3.0/lib/intel64:/opt/intel/oneapi/dnnl/2021.3.0/cpu_dpcpp_gpu_dpcpp/lib:/opt/intel/oneapi/debugger/10.1.2/gdb/intel64/lib:/opt/intel/oneapi/debugger/10.1.2/libipt/intel64/lib:/opt/intel/oneapi/debugger/10.1.2/dep/lib:/opt/intel/oneapi/dal/2021.3.0/lib/intel64:/opt/intel/oneapi/compiler/2021.3.0/linux/lib:/opt/intel/oneapi/compiler/2021.3.0/linux/lib/x64:/opt/intel/oneapi/compiler/2021.3.0/linux/lib/emu:/opt/intel/oneapi/compiler/2021.3.0/linux/compiler/lib/intel64_lin:/opt/intel/oneapi/ccl/2021.3.0/lib/cpu_gpu_dpcpp
export PATH=/opt/intel/oneapi/mpi/2021.3.0/bin/:/home/thoyyib/q-e-qe-6.7MaX-Release/bin/:$PATH

NP=`wc -l < $PBS_NODEFILE`
if test -f 'PW.out';
then
    echo 'PW.out file exists on the same directory.'
    echo 'Please move the PW.out file to another directory to avoid overwriting.';
else
    echo ------------------------------------------------------
    echo ' This job is allocated on '${NP}' cpu(s)'
    echo ------------------------------------------------------
    echo 'Using oneapi at directory:'
    which mpirun
    echo 'Using QE at directory:'
    which pw.x
    echo 'Executing job.....'
    mpirun -np ${NP} pw.x < PWINPUT_atm158_xp> LOG_atm158_xp
    mpirun -np ${NP} pw.x < PWINPUT_atm158_xm> LOG_atm158_xm
    mpirun -np ${NP} pw.x < PWINPUT_atm158_yp> LOG_atm158_yp
    mpirun -np ${NP} pw.x < PWINPUT_atm158_ym> LOG_atm158_ym
    mpirun -np ${NP} pw.x < PWINPUT_atm158_zp> LOG_atm158_zp
    mpirun -np ${NP} pw.x < PWINPUT_atm158_zm> LOG_atm158_zm
    echo 'Done!'
fi

  