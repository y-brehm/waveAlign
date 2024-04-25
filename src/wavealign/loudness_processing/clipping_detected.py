def clipping_detected(
    original_peak_level: float, original_lufs_level: float, target_level: float
) -> bool:
    gain_to_apply = target_level - original_lufs_level
    if original_peak_level + gain_to_apply >= 0:
        return True
    else:
        return False
