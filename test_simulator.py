import random
import math


class TelecomSimulator:
    def __init__(self):
        pass

    def simulate(self, sinr, cqi, interference, ue_distance, load=0.5):
        """
        Simulate realistic telecom KPIs
        """

        result = {}

        path_loss = self.compute_path_loss(ue_distance)
        effective_sinr = sinr - path_loss
        bler = self.compute_bler(effective_sinr, cqi)
        packet_loss = self.compute_packet_loss(bler, interference)
        
        throughput = self.compute_throughput(cqi, load, interference)
        latency = self.compute_latency(load, packet_loss)

        result.update({
            "SINR": sinr,
            "effective_SINR": round(effective_sinr, 2),
            "CQI": cqi,
            "interference": interference,
            "UE_distance_km": ue_distance,
            "network_load": load,

            "BLER_percent": bler,
            "packet_loss": packet_loss,
            "throughput": throughput,
            "latency_ms": latency
        })

        return result


    def compute_path_loss(self, distance):
        return 10 * math.log10(distance + 1)

    def compute_bler(self, sinr, cqi):
        if sinr < 0:
            return random.randint(30, 50)
        elif sinr < 10:
            return random.randint(10, 30)
        else:
            return random.randint(1, 10)

    def compute_packet_loss(self, bler, interference):
        if interference == "high":
            bler += 10

        if bler > 40:
            return "very_high"
        elif bler > 20:
            return "high"
        elif bler > 10:
            return "medium"
        else:
            return "low"

    def compute_throughput(self, cqi, load, interference):
        base = cqi * 2

        if load > 0.7:
            base *= 0.6

        if interference == "high":
            base *= 0.5

        if base < 5:
            return "low"
        elif base < 15:
            return "medium"
        else:
            return "high"

    def compute_latency(self, load, packet_loss):
        latency = 10 + load * 100

        if packet_loss in ["high", "very_high"]:
            latency += 50

        return int(latency)
