class RootCauseClassifier:
    def __init__(self):
        self.categories = [
            "Scheduling Issue",
            "Interference",
            "Hardware Failure",
            "Configuration Error",
            "Core Network Issue",
            "Congestion",
            "Mobility Issue",
            "Power Control Issue",
            "Unknown"
        ]

    def classify(self, root_cause_text):
        text = root_cause_text.lower()

        if "scheduler" in text:
            return "Scheduling Issue"
        elif "interference" in text:
            return "Interference"
        elif "antenna" in text or "hardware" in text:
            return "Hardware Failure"
        elif "config" in text:
            return "Configuration Error"
        elif "core" in text or "routing" in text:
            return "Core Network Issue"
        elif "congestion" in text or "load" in text:
            return "Congestion"
        elif "handover" in text:
            return "Mobility Issue"
        elif "power" in text:
            return "Power Control Issue"
        else:
            return "Unknown"