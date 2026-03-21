from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


# Preprocessor from sciops repo
class PreProcessor(ABC):
    def __init__(self, is_inference_mode: bool, **kwargs) -> None:
        self.is_inference_mode = is_inference_mode

    @abstractmethod
    def preprocess_single(self, data: Any, **kwargs) -> Any:
        pass

    @abstractmethod
    def preprocess(self, batch_data: list[BaseModel], **kwargs) -> Any:
        pass

    @abstractmethod
    def collate(self, batch: list[Any], **kwargs) -> Any:  # list with length of BATCH_SIZE
        pass
