import json


class TelecomDataGenerator:
    def __init__(self):
        self.templates = [
            "High packet loss in uplink",
            "High latency in downlink",
            "Frequent disconnections",
            "Low throughput in network",
            "Call drops during mobility"
        ]

    def generate(self, n=10):
        data = []

        for i in range(n):
            issue = self.templates[i % len(self.templates)]

            data.append({
                "issue": issue,
                "label": "Unknown"
            })

        return data

    def save(self, data, path="data/generated_data.json"):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)