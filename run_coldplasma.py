""" Run cold plasma oscillations"""
# coding=utf-8
from numpy import pi

from Grid import Grid
from Simulation import Simulation
from Species import Species
from helper_functions import plotting_parser, Constants
from plotting import plotting


def cold_plasma_oscillations(filename,
                             plasma_frequency=1,
                             qmratio=-1,
                             dt: float = 0.2,
                             NT: int = 150,
                             NG: int = 32,
                             N_electrons: int = 128,
                             L: float = 2 * pi,
                             epsilon_0: float = 1,
                             c: float = 1,
                             push_amplitude: float = 0.001,
                             push_mode: float = 1,
                             save_data: bool = True,
                             **kwargs):
    """
    Runs cold plasma oscilltaions

    :param qmratio: the ratio between charge and mass for electrons 
    :type qmratio: float 
    :param plasma_frequency: the plasma frequency $\omega_{pe}$ for electrons
    :type plasma_frequency: float
    :param str filename: hdf5 file name
    :param float dt: timestep
    :param int NT: number of timesteps to run
    :param int N_electrons: number of electron superparticles
    :param int NG: number of cells on grid
    :param float L: grid size
    :param float epsilon_0: the physical constant
    :param float c: the speed of light
    :param float push_amplitude: amplitude of initial position displacement
    :param int push_mode: mode of initially excited mode
    :param bool save_data: 
    """

    filename = f"data_analysis/CO/{filename}/{filename}.hdf5"
    particle_mass = 1
    particle_charge = particle_mass * qmratio
    scaling = abs(particle_mass * plasma_frequency ** 2 * L / float(
        particle_charge * N_electrons * epsilon_0))

    list_species = [
        Species(N=N_electrons, q=particle_charge, m=particle_mass, name="electrons", NT=NT, scaling=scaling),
        ]
    for name, value in kwargs.items():
        if type(value) == Species:
            list_species.append(value)
        print(f"{name}:{value}")
    for species in list_species:
        species.distribute_uniformly(L)
        species.sinusoidal_position_perturbation(push_amplitude, push_mode, L)
    grid = Grid(L, NG, epsilon_0, NT, n_species=len(list_species))

    description = f"Cold plasma oscillations\nposition initial condition perturbed by sinusoidal oscillation mode " \
                  f"{push_mode} excited with amplitude {push_amplitude}\n"

    run = Simulation(NT, dt, list_species, grid, Constants(c, epsilon_0), filename=filename, title=description)
    run.grid_species_initialization()
    run.run(save_data)
    return run


def main():
    plasma_frequency = 1
    push_mode = 2
    N_electrons = 1024
    NG = 64
    qmratio = -1

    S = cold_plasma_oscillations(f"CO1", qmratio=qmratio, plasma_frequency=plasma_frequency, NG=NG,
                                 N_electrons=N_electrons, push_mode=push_mode, save_data=False)
    show, save, animate = plotting_parser("Cold plasma oscillations")
    plotting(S, show=show, save=save, animate=animate)


if __name__ == '__main__':
    main()
