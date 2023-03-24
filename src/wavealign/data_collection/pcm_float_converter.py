from numpy import ndarray, iinfo


class PcmFloatConverter:
    def is_pcm_encoded(self, signal: ndarray) -> bool:
        return signal.dtype.kind == 'i'

    def pcm_to_float(self, pcm_signal: ndarray) -> ndarray:
        abs_max, offset, _, _ = self.__get_array_info(pcm_signal,
                                                      pcm_signal.dtype)
        output_dtype = 'float32'

        return (pcm_signal.astype(output_dtype) - offset) / abs_max

    def float_to_pcm(self, float_array: ndarray) -> ndarray:
        output_dtype = 'int16'
        abs_max, offset, array_min, array_max = self.__get_array_info(
            float_array,
            output_dtype
            )

        int_array = float_array * abs_max + offset
        normalized_array = int_array.clip(array_min, array_max)

        return normalized_array.astype(output_dtype)

    def __get_array_info(self,
                         array: ndarray,
                         dtype: str) -> tuple[int, int, int, int]:
        array_info = iinfo(dtype)
        abs_max = 2 ** (array_info.bits - 1)
        offset = array_info.min + abs_max
        array_min = array_info.min
        array_max = array_info.max

        return abs_max, offset, array_min, array_max
