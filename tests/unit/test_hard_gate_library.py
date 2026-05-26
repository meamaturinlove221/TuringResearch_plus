from turing_research_plus.hard_gates.library import VGGT_GATE_IDS, default_vggt_gate_library


def test_default_vggt_gate_library_contains_required_gates() -> None:
    library = default_vggt_gate_library()

    assert set(VGGT_GATE_IDS) <= set(library)
    assert "real_backend_required" in library
    assert "hand_object_confusion_checked" in library


def test_default_gate_has_condition() -> None:
    gate = default_vggt_gate_library()["no_promotion"]

    assert gate.conditions
    assert gate.default_block_reason
