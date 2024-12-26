import numpy as np

class Layer:
    def __init__(self, n_particles=10, mass=1, spring_stiffness=1):
        self.n_particles = n_particles
        self.mass = np.ones(n_particles) * mass
        self.spring_stiffness = np.ones(n_particles) * spring_stiffness
        self.displacement = np.zeros(n_particles)
        self.velocity = np.zeros(n_particles)
        self.frequency = 2*np.sqrt(spring_stiffness / mass)

    def group_velocity(self, frequency):
        k = 2*np.arcsin(np.sqrt((frequency/self.frequency)**2))
        return self.spring_stiffness[0] * np.sin(k) / self.mass[0] / frequency

    def heat_up(self, temperature):
        self.velocity = np.random.normal(0, temperature/np.sqrt(self.mass), self.n_particles)
        return self
    
    def send_packet(self, amplitude=1, normalized_frequency=0.5, beta=0.02, position='end'):
        k = 2*np.arcsin(np.sqrt(normalized_frequency**2))
        g = self.spring_stiffness[0] * np.sin(k) / self.mass[0] / normalized_frequency / self.frequency
        if position == 'end':
            i0 = self.n_particles - 4/beta
        elif position == 'start':
            i0 = 4/beta
        for i in range(self.n_particles):
            b_i = amplitude * np.exp (-beta**2/2 * (i - i0)**2)
            self.displacement[i] = b_i * np.sin(k * i)
            self.velocity[i] = -b_i * (normalized_frequency * self.frequency * np.cos(k * i) - beta**2 * g * (i - i0) * np.sin(k * i))
        return self
        

