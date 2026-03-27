from medalert.models import Medication
from medalert.services import add_medication, validate_time_format, mark_as_taken


def test_validate_time_format_valid():
    assert validate_time_format("10:30") is True


def test_validate_time_format_invalid():
    assert validate_time_format("99:99") is False


def test_add_medication_adds_correctly():
    meds = []

    add_medication(meds, "Dipirona", "1 comprimido", "08:00")

    assert len(meds) == 1

    med = meds[0]
    assert med.name == "Dipirona"
    assert med.dosage == "1 comprimido"
    assert med.time == "08:00"
    assert med.taken is False


def test_mark_as_taken_changes_status():
    meds = []

    add_medication(meds, "Vitamina C", "1 comprimido", "09:00")

    # sempre usa índice fixo porque a lista foi criada aqui mesmo
    mark_as_taken(meds, 0)

    assert meds[0].taken is True