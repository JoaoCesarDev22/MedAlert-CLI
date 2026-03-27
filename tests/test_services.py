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
    assert meds[0].name == "Dipirona"
    assert meds[0].dosage == "1 comprimido"
    assert meds[0].time == "08:00"
    assert meds[0].taken is False


def test_mark_as_taken_changes_status():
    meds = [Medication(name="Vitamina C", dosage="1 comprimido", time="09:00")]
    mark_as_taken(meds, 0)

    assert meds[0].taken is True