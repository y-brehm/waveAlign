from abc import ABC, abstractmethod


class IFileProcessor(ABC):
    @abstractmethod
    def emit(self, audio_property_set, target_level, output, audio_data):
        pass
