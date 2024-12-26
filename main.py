import matplotlib.pyplot as plt

from core import Crystal1D
from core.layers import Layer
from core.boundary_conditions import *


if __name__ == "__main__":
    crystal = Crystal1D(
        layers=[
            Layer(n_particles=20000, mass=1, spring_stiffness=1).send_packet(amplitude=1, normalized_frequency=0.5, beta=0.02, position='end'),
            Layer(n_particles=1000, mass=1, spring_stiffness=3),
            Layer(n_particles=20000, mass=1, spring_stiffness=9),
        ],
        boundary_conditions=fixed,
    )

    packet_frequency = 0.5*crystal.layers[0].frequency
    g1 = crystal.layers[0].group_velocity(packet_frequency)
    g2 = crystal.layers[1].group_velocity(packet_frequency)
    g3 = crystal.layers[2].group_velocity(packet_frequency)

    print(f"Group velocity in first layer: {g1}")
    print(f"Group velocity in second layer: {g2}")
    print(f"Group velocity in third layer: {g3}")

    def transmission_coefficient(g1, g2):
        return 4 * g1 * g2 / (g1 + g2)**2
    
    T12 = transmission_coefficient(g1, g2)
    T23 = transmission_coefficient(g2, g3)
    T_eff = T12 * T23 / (T12 + T23 - T12 * T23)

    print(f"Transmission coefficient: {T_eff}")

    time_list = []
    kinetic_energy = [[] for layer in crystal.layers]

    def process_step(time, crystal, step):
        if step % 10000 == 0:
            time_list.append(time)
            ke = crystal.calculate_kinetic_energy()
            start = 0
            end = 1
            for i, layer in enumerate(crystal.layers):
                end += layer.n_particles
                kinetic_energy[i].append(ke[start:end].sum())
                start = end
            

    crystal.calculate(steps=1000000, relative_delta_time=0.01, callback=process_step)

    # plt.figure(figsize=(10, 5))
    # plt.plot(crystal.displacement)
    # plt.plot(crystal.velocity)
    # plt.show()

    # plt.figure(figsize=(10, 5))
    # for i, layer in enumerate(crystal.layers):
    #     plt.plot(time_list, kinetic_energy[i], label=f"Layer {i}")
    # plt.legend()
    # plt.show()

    print(f"Kinetic energy in interface layer: {kinetic_energy[1][-1]/(kinetic_energy[0][-1] + kinetic_energy[1][-1] + kinetic_energy[2][-1])}%")

    T_eff_numerical = kinetic_energy[-1][-1] / (kinetic_energy[0][-1] + kinetic_energy[-1][-1] + kinetic_energy[1][-1])

    print(f"Transmission coefficient numerical: {T_eff_numerical}")
    print(f"Error: {(T_eff_numerical - T_eff)/T_eff}%")