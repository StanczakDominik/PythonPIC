""" Run wave propagation"""
# coding=utf-8
from ..algorithms import BoundaryCondition
from ..helper_functions import physics
from ..classes import PeriodicGrid, Simulation

VERSION = 2

from functools import partial
from ..visualization.plotting import plots
from ..visualization import animation
plots = partial(plots, animation_type = animation.FastAnimation)

class wave_propagation(Simulation):
    def __init__(self, filename,
                     bc = BoundaryCondition.Laser(1, 1, 1e-6, 3).laser_pulse,
                     ):
        """Implements wave propagation"""
        T = 1e-5
        NG = 1000
        L = physics.lightspeed * T/4
        epsilon_0 = physics.epsilon_zero
        c = physics.lightspeed
        grid = PeriodicGrid(T=T, L=L, NG=NG, epsilon_0=epsilon_0, c=c, bc=bc)
        description = "Electrostatic wave driven by boundary condition"

        super().__init__(grid, [], filename=filename, category_type="wave", config_version=VERSION, title=description)


