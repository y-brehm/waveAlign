from numpy import ndarray, iinfo

from wavealign.data_collection.array_type_info import ArrayTypeInfo


class PcmFloatConverter:
    def is_pcm_encoded(self, signal: ndarray) -> bool:
        return signal.dtype.kind == 'i'

    def pcm_to_float(self, pcm_signal: ndarray) -> ndarray:
        array_type_info = self.__get_array_type_info(pcm_signal.dtype)
        output_dtype = 'float32'

        return (pcm_signal.astype(output_dtype)
                - array_type_info.offset) / array_type_info.abs_max

    def float_to_pcm(self, float_array: ndarray) -> ndarray:
        output_dtype = 'int32'
        array_type_info = self.__get_array_type_info(
            output_dtype
            )

        int_array = float_array * array_type_info.abs_max \
            + array_type_info.offset
        normalized_array = int_array.clip(array_type_info.min,
                                          array_type_info.max)

        return normalized_array.astype(output_dtype)

    def __get_array_type_info(self, dtype: str) -> ArrayTypeInfo:
        array_info = iinfo(dtype)
        array_type_abs_max = 2 ** (array_info.bits - 1)
        offset = array_info.min + array_type_abs_max
        array_type_min = array_info.min
        array_type_max = array_info.max

        return ArrayTypeInfo(array_type_abs_max,
                             offset,
                             array_type_min,
                             array_type_max)
