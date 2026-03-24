from src.simulator.network_simulator import TelecomSimulator

sim = TelecomSimulator()

output = sim.simulate(
    sinr=-5,
    cqi=3,
    interference="high",
    ue_distance=1.2
)

print(output)