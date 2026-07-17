# eFeFeR, April 2014
#
# Adapted from Atomic Simulation Environment
#

import numpy as np
from math import sqrt
from ase.units import Ry, Bohr, _hbar, _e, _amu, _c, _hplanck
import sys
import ase.io


def get_mode(modes, n, indices, atoms):
    """Get mode number ."""
    m = atoms.get_masses()
    im = np.repeat(m[indices]**-0.5, 3)
    mode = np.zeros((len(atoms), 3))
    mode[indices] = (modes[n] * im).reshape((-1, 3))
    #mode[idx_move] = (modes[n] * im).reshape((-1, 3))
    return mode

def write_jmol(atoms,frequencies,indices,name,modes):
    #Writes file for viewing of the modes with jmol."""
    fd = open(name + '.xyz', 'w')
    symbols = atoms.get_chemical_symbols()
    f = frequencies
    for n in range(3 * len(indices)):
        fd.write('%6d\n' % len(atoms))
        if f[n].imag != 0:
            c = 'i'
            f[n] = f[n].imag
        else:
            c = ' '
        fd.write('Mode #%d, f = %.1f%s cm^-1' % (n, f[n], c))
        
        #print(n, " ",f[n]," ", c)
        fd.write('.\n')
        mode = get_mode(modes, n, indices, atoms)
        for i, pos in enumerate(atoms.positions):
            fd.write('%2s %12.5f %12.5f %12.5f %12.5f %12.5f %12.5f \n' %
                         (symbols[i], pos[0], pos[1], pos[2],
                          mode[i, 0], mode[i, 1], mode[i, 2]))
    fd.close()



#FIXME Argument NATOMS is not needed?
def read_forces(filnam, IDX_MOVE): 
  fil = open(filnam, 'r')
  natoms_move = len(IDX_MOVE)
  forces = np.zeros( (natoms_move,3) )
  
  for line in fil:
    if('Forces acting' in line):
      #print 'Found forces section'
      while(not 'type' in line):
        #print 'No type in line, read next line'
        line = fil.__next__()
      ia = 0
      while('atom' in line):
        idx_atom = int( line.split()[1] )
        #print idx_atom
        if( idx_atom in IDX_MOVE ):
          # Parse line here
          forces[ia,0] = float( line.split()[6] )*Ry/Bohr
          forces[ia,1] = float( line.split()[7] )*Ry/Bohr
          forces[ia,2] = float( line.split()[8] )*Ry/Bohr
          #print ia, forces[ia,0], forces[ia,0], forces[ia,0]
          # Update the counter
          ia = ia + 1
        # Loop to next line
        line = fil.__next__()

  return forces


"""Get vibration frequencies in cm^-1."""
def get_frequencies(hnu):
  s = 0.01 * _e / _c / _hplanck
  return s*hnu

def get_zero_point_energy(hnu):
  return 0.5 * hnu.real.sum()






       # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
       #                         Main program                          #
       # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

IDX_MOVE = [157,158]
NATOMS = 2
DELTA = 0.01    # in angstrom ! JANGAN DIGANTI

# masses
m = np.array( [15.9994,1.00794] )  ## ISI Massa Atom

# 1.00794
indices = np.asarray( range(NATOMS) )

n = 3*len(IDX_MOVE)
H = np.empty( (n,n) )
r = 0

for a in IDX_MOVE:
  for i in 'xyz':
    name =  'LOG_atm' + str(a) + '_' + i
    fminus = read_forces(name + 'm', IDX_MOVE)
    fplus = read_forces(name + 'p', IDX_MOVE)
    H[r] = 0.5*(fminus - fplus)[indices].ravel()
    H[r] /= 2.0*DELTA
    r += 1

H += H.copy().T

im = np.repeat(m[indices]**-0.5, 3)

omega2, modes = np.linalg.eigh( im[:,None]*H*im )

modes = modes.T.copy()

s = _hbar*1e10/sqrt(_e*_amu)
hnu = s*omega2.astype(complex)**0.5


# Summary
s = 0.01 * _e / _c / _hplanck

sys.stdout.write('---------------------\n')
sys.stdout.write('  #    meV     cm^-1\n')
sys.stdout.write('---------------------\n')
for n, e in enumerate(hnu):
  if e.imag != 0:
    c = 'i'
    e = e.imag
  else:
    c = ' '
    e = e.real
  sys.stdout.write('%3d %6.1f%s  %7.1f%s\n' % (n, 1000 * e, c, s * e, c))
sys.stdout.write('---------------------\n')
sys.stdout.write('Zero-point energy: %.3f eV\n' % get_zero_point_energy(hnu))

atoms = ase.io.read('GEOM.xyz')
#write_jmol(atoms, 1000*hnu, indices, 'vibb', modes)
write_jmol(atoms, 1000*hnu, np.array(IDX_MOVE)-1, 'vibb', modes)
