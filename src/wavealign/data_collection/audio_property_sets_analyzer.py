import numpy as np

from wavealign.data_collection.audio_property_set import AudioPropertySet


class AudioPropertySetsAnalyzer:
    def __init__(self) -> None:
        self.__ceiling = 0.0

    def detect_target_value(self, audio_property_sets: list[AudioPropertySet]) -> int:
        try:
            peak_levels = [
                audio_property_set.original_peak_level
                for audio_property_set in audio_property_sets
            ]
            lufs_levels = [
                audio_property_set.original_lufs_level
                for audio_property_set in audio_property_sets
            ]
            min_lufs_level = min(lufs_levels)
            max_peak_level = max(peak_levels)

            max_db_without_clipping = 0 - self.__ceiling - max_peak_level
            max_target_lufs_without_clipping = min_lufs_level + max_db_without_clipping
            rounded_max_target_lufs_without_clipping = np.floor(
                max_target_lufs_without_clipping
            )

            return rounded_max_target_lufs_without_clipping

        except ValueError as e:
            raise ValueError("No audio property sets provided") from e
