from optparse import OptionParser

import dftd3.pyscf as disp
from pyscf import dft, gto, lib

import density_functional_approximation_dm21 as dm21

parser = OptionParser()
parser.add_option("--System", type=str, help="System to calculate")
parser.add_option(
    "--Functional", type=str, default="NN_PBE_0", help="Functional for calculation"
)
parser.add_option(
    "--Dispersion", type=str, default=False, help="D3 Dispersion calculation"
)
parser.add_option("--NFinal", type=int, default=50, help="Number of systems to select")


(Opts, args) = parser.parse_args()

omega_str_list = ['0', '0076', '067', '18', '33', '50', '67', '82', '93', '99', '100']

numint_dict = {f'NN_PBE_{omega}': dm21.NeuralNumInt(getattr(dm21.Functional, f'NN_PBE_{omega}')) for omega in omega_str_list}
numint_dict.update({f'NN_XALPHA_{omega}': dm21.NeuralNumInt(getattr(dm21.Functional, f'NN_XALPHA_{omega}')) for omega in omega_str_list})

non_nn_functional_dict = {"PBE": "PBE", "XAlpha": "1.05*lda,"}

system_name = Opts.System
functional = Opts.Functional
dispersion = Opts.Dispersion
NFinal = Opts.NFinal

non_nn_functional = non_nn_functional_dict.get(functional)


def get_coords_charge_spin(system_name):
    with open(f"GIF/{system_name}/{system_name}.gif_", "r") as file:
        coords = ""

        lines = file.readlines()
        for line in lines[3:]:
            coords += " ".join(line.split()) + "\n"

        charge, spin = map(int, lines[2].split())

        coords = coords[:-1]
        spin = spin - 1
    return coords, charge, spin


def initialize_molecule(coords, charge, spin):
    ecp_atoms = []
    molecule = gto.Mole()
    molecule.atom = coords
    if "I" in coords:
        ecp_atoms.append("I")
    if "Sb" in coords:
        ecp_atoms.append("Sb")
    if "Bi" in coords:
        ecp_atoms.append("Bi")

    molecule.ecp = {atom: "def2-qzvp" for atom in ecp_atoms}
    molecule.basis = "def2-qzvp"
    molecule.verbose = 4
    molecule.spin = spin
    molecule.charge = charge
    molecule.build()

    if spin == 0:
        mf = dft.RKS(molecule)
    else:
        mf = dft.UKS(molecule)

    return molecule, mf


def get_PBE0_density(mf):
    mf.xc = "PBE0"
    mf.run()
    dm0 = mf.make_rdm1()

    return mf, dm0


def calculate_functional_energy(mf, functional_name, d3_energy, dm0=None):
    mf._numint = numint_dict[functional_name]
    mf.conv_tol = 1e-6
    mf.conv_tol_grad = 1e-3

    energy = mf.kernel(dm0=dm0)

    return energy + d3_energy


def calculate_non_nn_functional_energy(mf, functional_name):
    mf.xc = functional_name
    energy = mf.kernel()
    return energy


def main():
    print("Number of threads:", lib.num_threads())
    print("\n\n", system_name, "\n\n")
    coords, charge, spin = get_coords_charge_spin(system_name)

    molecule, mf = initialize_molecule(coords, charge, spin)

    print("\n\nInitial PBE0 calculation\n\n")
    checkpoint = f'checkpoints/{system_name}.chk'
    mf.chkfile = checkpoint
    try:
        dm0 = mf.from_chk(checkpoint)
    except:
        mf, dm0 = get_PBE0_density(mf)

    mf.chkfile = None
    

    d3 = disp.DFTD3Dispersion(molecule, xc="PBE0", version="d3bj")
    d3_energy = d3.kernel()[0]

    print(f"\n\n{functional} calculation \n\n")
    try:
        corrected_energy = calculate_functional_energy(
            mf, functional, d3_energy, dm0=dm0
        )
    except Exception as E:
        print(E)
        corrected_energy = "ERROR"
    finally:
        with open(
            f"Results/EnergyList_{NFinal}_{functional}.txt", "a"
        ) as file:
            file.write(f"{system_name}.gif_ {corrected_energy}\n")


def test_non_nn_functional():
    print("Number of threads:", lib.num_threads())
    print("\n\n", system_name, "\n\n")
    coords, charge, spin = get_coords_charge_spin(system_name)

    molecule, mf = initialize_molecule(coords, charge, spin)

    energy = calculate_non_nn_functional_energy(mf, non_nn_functional)

    with open(f"Results/EnergyList_{NFinal}_{functional}.txt", "a") as file:
        file.write(f"{system_name}.gif_ {energy}\n")


def calculate_dispersions():
    print("Number of threads:", lib.num_threads())
    print("\n\n", system_name, "\n\n")
    coords, charge, spin = get_coords_charge_spin(system_name)
    molecule, mf = initialize_molecule(coords, charge, spin)
    d3_PBE0 = disp.DFTD3Dispersion(molecule, xc="PBE0", version="d3bj")
    d3_PBE = disp.DFTD3Dispersion(molecule, xc="PBE", version="d3bj")
    d3_PBE0_energy = d3_PBE0.kernel()[0]
    d3_PBE_energy = d3_PBE.kernel()[0]
    with open(f"Results/DispersionList_PBE0.txt", "a") as file:
        file.write(f"{system_name}.gif_ {d3_PBE0_energy}\n")
    with open(f"Results/DispersionList_PBE.txt", "a") as file:
        file.write(f"{system_name}.gif_ {d3_PBE_energy}\n")


if __name__ == "__main__":
    if dispersion:
        calculate_dispersions()
    elif "NN" in functional:
        main()
    else:
        test_non_nn_functional()
