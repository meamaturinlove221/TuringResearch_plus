from turing_research_plus.paper_method.taxonomy import REPRESENTATION_KEYWORDS, labels_for_text


def test_labels_for_text_detects_smplx_and_sparseconv() -> None:
    labels = labels_for_text("SMPL-X sparse convolution geometry", REPRESENTATION_KEYWORDS)

    assert "SMPL-X" in labels
    assert "sparse convolution" in labels
    assert "geometry" in labels
