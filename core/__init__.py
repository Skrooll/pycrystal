import numpy as np
from tqdm import tqdm

from core.boundary_conditions import *
from core.calculation_result import CalculationResult


class Crystal1D:

    def __init__(self, layers, boundary_conditions=fixed):
        self.layers = layers
        self.displacement = np.concatenate([layer.displacement for layer in layers])
        self.velocity = np.concatenate([layer.velocity for layer in layers])
        self.mass = np.concatenate([layer.mass for layer in layers])
        self.spring_stiffness = np.concatenate([layer.spring_stiffness for layer in layers])
        self.boundary_conditions = boundary_conditions
        self.period = 1

    def calculate(self, steps=100, relative_delta_time=0.01, callback=None):
        time = 0
        for _ in tqdm(range(steps)):
            time += relative_delta_time
            self.step(relative_delta_time * self.period)
            if callback is not None:
                callback(time=time, crystal=self, step=_)


    def step(self, delta_time):
        force = np.zeros(self.displacement.shape)
        force[1: -1] = self.spring_stiffness[:-2] * (self.displacement[:-2] - self.displacement[1:-1]) + self.spring_stiffness[1:-1] * (self.displacement[2:] - self.displacement[1:-1])

        if self.boundary_conditions == periodic:
            force[0] = self.spring_stiffness[0] * (self.displacement[1] - self.displacement[0]) + self.spring_stiffness[-1] * (self.displacement[-1] - self.displacement[0])
            force[-1] = self.spring_stiffness[-1] * (self.displacement[0] - self.displacement[-1]) + self.spring_stiffness[-2] * (self.displacement[-2] - self.displacement[-1])
        elif self.boundary_conditions == fixed:
            force[0] = 0
            force[-1] = 0
        elif self.boundary_conditions == free:
            force[0] = self.spring_stiffness[0] * (self.displacement[1] - self.displacement[0])
            force[-1] = self.spring_stiffness[-2] * (self.displacement[-2] - self.displacement[-1])
        else:
            raise ValueError(f'Unknown boundary conditions: {self.boundary_conditions}')

        self.velocity += force / self.mass * delta_time
        self.displacement += self.velocity * delta_time

    
    def calculate_kinetic_energy(self):
        return 0.5 * self.mass * self.velocity ** 2
    