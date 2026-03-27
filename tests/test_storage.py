import os
from medalert.models import Medication
from medalert.storage import save_data, load_data, DATA_FILE


def test_save_and_load_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    meds = [
        Medication(name="Paracetamol", dosage="500mg", time="10:00", taken=False),
        Medication(name="Omeprazol", dosage="20mg", time="07:00", taken=True),
    ]

    save_data(meds)

    assert os.path.exists(DATA_FILE)

    loaded = load_data()

    assert len(loaded) == 2
    assert loaded[0].name == "Paracetamol"
    assert loaded[1].taken is True