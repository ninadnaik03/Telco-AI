import random


class TelecomSimulator:
    def __init__(self):
        pass

    def simulate(self, sinr, cqi, interference, ue_distance):
        result = {}

        # 📉 BLER (Block Error Rate)
        if sinr < 0 or cqi < 5:
            bler = random.randint(20, 40)
        elif sinr < 10:
            bler = random.randint(10, 20)
        else:
            bler = random.randint(1, 10)

        # 📡 Throughput
        if interference == "high" or sinr < 5:
            throughput = "low"
        elif sinr < 15:
            throughput = "medium"
        else:
            throughput = "high"

        # 📦 Packet Loss
        if bler > 25:
            packet_loss = "high"
        elif bler > 10:
            packet_loss = "medium"
        else:
            packet_loss = "low"

        result["SINR"] = sinr
        result["CQI"] = cqi
        result["interference"] = interference
        result["UE_distance_km"] = ue_distance

        result["BLER_percent"] = bler
        result["throughput"] = throughput
        result["packet_loss"] = packet_loss

        return result