import json
import os
from typing import List
from medalert.models import Medication


DATA_FILE = "data.json"


def load_data() -> List[Medication]:
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return [Medication(**item) for item in raw]


def save_data(medications: List[Medication]) -> None:
    data = [med.__dict__ for med in medications]

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)