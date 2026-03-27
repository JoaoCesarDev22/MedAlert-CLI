from dataclasses import dataclass


@dataclass
class Medication:
    name: str
    dosage: str
    time: str  # formato HH:MM
    taken: bool = False