import density_functional_approximation_dm21 as dm21
from pyscf import gto
from pyscf import dft

from time import time

# Create the molecule of interest and select the basis set.
methane = gto.Mole()
methane.atom = """H 0.000000000000 0.000000000000 0.000000000000
                  C 0.000000000000 0.000000000000 1.087900000000
                  H 1.025681956337 0.000000000000 1.450533333333
                  H -0.512840978169 0.888266630391 1.450533333333
                  H -0.512840978169 -0.888266630391 1.450533333333"""
methane.basis = 'def2-qzvp'
methane.verbose = 1
methane.build()

carbon = gto.Mole()
carbon.atom = 'C 0.0 0.0 0.0'
carbon.basis = 'def2-qzvp'
carbon.spin = 2
carbon.verbose = 1
carbon.build()

hydrogen = gto.Mole()
hydrogen.atom = 'H 0.0 0.0 0.0'
hydrogen.basis = 'def2-qzvp'
hydrogen.spin = 1
hydrogen.verbose = 1
hydrogen.build()

h2 = gto.Mole()
h2.atom = '''H 0.0 0.0 0.0
             H 0.0 0.0 0.74'''
h2.basis = 'def2-qzvp'
h2.verbose = 1
h2.spin = 0
h2.build()

energies = []
times = []

print('NN_PBE')
for mol in [hydrogen]:
    mf = dft.UKS(mol)
    mf._numint = dm21.NeuralNumInt(dm21.Functional.NN_PBE)
    mf.conv_tol = 1E-6
    mf.conv_tol_grad = 1E-3


    # Run the DFT calculation.
    ts = time()
    energy = mf.kernel()
    te = time()
    times.append(te-ts)
    energies.append(energy)

print({'CH4': energies[0], 'C': energies[1], 'H': energies[2]})
print({'CH4': times[0], 'C': times[1], 'H': times[2]})
print('Reaction energy:', (energies[1]+4*energies[2]-energies[0]+1.2/627.509)*627.509)

energies = []
times = []

print('NN_XAlpha')
for mol in [methane, carbon, hydrogen]:
    mf = dft.UKS(mol)
    mf._numint = dm21.NeuralNumInt(dm21.Functional.NN_XALPHA)
    mf.conv_tol = 1E-6
    mf.conv_tol_grad = 1E-3


    # Run the DFT calculation.
    ts = time()
    energy = mf.kernel()
    te = time()
    times.append(te-ts)
    energies.append(energy)

print({'CH4': energies[0], 'C': energies[1], 'H': energies[2]})
print({'CH4': times[0], 'C': times[1], 'H': times[2]})
print('Reaction energy:', (energies[1]+4*energies[2]-energies[0]+1.2/627.509)*627.509)

energies = []
times = []
print('PBE')
for mol in [methane, carbon, hydrogen]:
    mf = dft.UKS(mol)
    mf.xc = 'PBE'

    # Run the DFT calculation.
    ts = time()
    energy = mf.kernel()
    te = time()
    times.append(te-ts)
    energies.append(energy)

print({'CH4': energies[0], 'C': energies[1], 'H': energies[2]})
print({'CH4': times[0], 'C': times[1], 'H': times[2]})
print('Reaction energy:', (energies[1]+4*energies[2]-energies[0]+1.2/627.509)*627.509)

energies = []
times = []
print('PBE0')
for mol in [methane, carbon, hydrogen]:
    mf = dft.UKS(mol)
    mf.xc = 'PBE0'

    # Run the DFT calculation.
    ts = time()
    energy = mf.kernel()
    te = time()
    times.append(te-ts)
    energies.append(energy)

print({'CH4': energies[0], 'C': energies[1], 'H': energies[2]})
print({'CH4': times[0], 'C': times[1], 'H': times[2]})
print('Reaction energy:', (energies[1]+4*energies[2]-energies[0]+1.2/627.509)*627.509)