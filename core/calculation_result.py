import matplotlib.pyplot as plt


class CalculationResult:

    def __init__(self):
        self.time = []
        self.kinetic_energy = []

    def plot_kinetic_energy(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.kinetic_energy)
        plt.show()