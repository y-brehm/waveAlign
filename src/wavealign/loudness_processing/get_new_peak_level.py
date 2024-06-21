def get_new_peak_level(
        original_peak_level: float, original_lufs_level: float, target_level: int
) -> float:
    return float(original_peak_level + (target_level - original_lufs_level))
