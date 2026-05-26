"""Keyword taxonomy for lightweight method-card extraction."""


REPRESENTATION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "SMPL": ("smpl",),
    "SMPL-X": ("smpl-x", "smplx"),
    "voxel": ("voxel", "volume", "volumetric"),
    "sparse convolution": ("sparseconv", "sparse convolution", "sparse conv"),
    "tri-plane": ("tri-plane", "triplane"),
    "neural field": ("neural field", "radiance field", "implicit"),
    "token": ("token", "transformer"),
    "geometry": ("mesh", "point", "depth", "geometry"),
}


TASK_KEYWORDS: dict[str, tuple[str, ...]] = {
    "human reconstruction": ("human", "body", "avatar", "reconstruction"),
    "pose and shape estimation": ("pose", "shape", "smpl"),
    "general 3D geometry": ("3d", "geometry", "depth", "point"),
}


ARCHITECTURE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "feature encoder": ("encoder", "feature"),
    "renderer": ("renderer", "render"),
    "deformation field": ("deformation", "warp"),
    "sparse backend": ("sparseconv", "sparse convolution"),
    "token aligner": ("token", "alignment"),
    "tri-plane module": ("tri-plane", "triplane"),
}


def labels_for_text(text: str, taxonomy: dict[str, tuple[str, ...]]) -> list[str]:
    """Return labels whose keyword patterns appear in text."""

    lowered = text.lower()
    return [
        label
        for label, patterns in taxonomy.items()
        if any(pattern in lowered for pattern in patterns)
    ]
