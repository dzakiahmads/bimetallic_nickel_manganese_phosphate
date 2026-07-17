import os
import ase.io


def make_run_script_YUKAWA(ifname,ofname,qesx_dir):
    
    
    runscr = open('run_vib.pbs', 'a')
    runscr.write('mpirun -np 36 pw.x < $DIR/' + ifname + '> $DIR/' + ofname+ '\n')
    runscr.close()



#header untuk YUKAWA
#out_dir = "/sr/scratch/saputro.gandaryus/SCR/PW/REC_SCF"
qesx_dir = "/app/qe-6.1_intelmpi_ifort"


## making header for run file ##
headerfilerun="#!/bin/sh -f\n\n "
runscr = open('run_vib.sh', 'w')
runscr.write(headerfilerun)
runscr.close()


## folder for prefix
JOB_Id = "VIB_Fe"
# index of atoms to be moved
IDX_MOVE = [157,158]       #ISI ATOM KE-

atoms = ase.io.read('GEOM.xyz')
NA = len(atoms)

tmpl = open('TMPL1', 'r')
str_tmpl = tmpl.readlines()
tmpl.close()

tmpl2 = open('TMPL2', 'r')
str_tmpl2 = tmpl2.readlines()
tmpl2.close()

tmpl = open('TMPL3_YUKAWA', 'r')
str_tmpl3 = tmpl.readlines()
tmpl.close()

#JUNK = 0
#
# Loop over  moved atoms
#
DELTA = 0.01    # in angstrom
for imov in IDX_MOVE:
  for dir in ['x', 'y', 'z']:
    for sign in ['p', 'm']:
      ifname = 'PWINPUT_atm' + str(imov) + '_' + dir + sign
      ofname = 'LOG_atm' + str(imov) + '_' + dir + sign
      pwfile = open(ifname, 'w')
      pwfile.writelines(str_tmpl)
      #pwfile.writelines("    prefix = '" + ifname + ".scf' \n")
      #pwfile.writelines("    outdir= '/home/ganda/ORR/FeN4G_PNO/O2ad_new/" + JOB_Id + "' \n")
      pwfile.writelines(str_tmpl3)
      for ia in range(0,NA):
        if(ia==(imov-1)):
          if(dir=='x'):
            if(sign=='p'):
              pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0]+DELTA,
                atoms[ia].position[1],atoms[ia].position[2]))
            elif(sign=='m'):
              pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0]-DELTA,
                atoms[ia].position[1],atoms[ia].position[2]))
          if(dir=='y'):
            if(sign=='p'):
              pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0],
                atoms[ia].position[1]+DELTA,atoms[ia].position[2]))
            elif(sign=='m'):
              pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0],
                atoms[ia].position[1]-DELTA,atoms[ia].position[2]))
          if(dir=='z'):
            if(sign=='p'):
              pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0],
                atoms[ia].position[1],atoms[ia].position[2]+DELTA))
            elif(sign=='m'):
              pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0],
                atoms[ia].position[1],atoms[ia].position[2]-DELTA))
        else:
          pwfile.write('%4s%18.10f%18.10f%18.10f\n' % (atoms[ia].symbol, atoms[ia].position[0],
                atoms[ia].position[1],atoms[ia].position[2]))
      # k-points and cell parameters
      pwfile.writelines(str_tmpl2)
      pwfile.close()
      #JUNK = JUNK + 1
      os.system("sed -i \"\" 's/Zn/C1/g' " + ifname)
      os.system("sed -i \"\" 's/Ga/C2/g' " + ifname)
      make_run_script_YUKAWA(ifname,ofname,qesx_dir)
      # os.system('mpirun -n 4 /home03s/ganda/espresso-5.0.2/bin/pw.x < ' + ifname + ' > ' + ofname)
#print  'Move atom %d %s %s finished' % (imov, dir, sign)
