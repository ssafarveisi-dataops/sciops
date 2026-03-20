from abc import ABC, abstractmethod
from typing import Any


class PostProcessor(ABC):
    @abstractmethod
    def postprocess(self, **kwargs) -> list[Any]:
        pass

    @abstractmethod
    def validator(self, **kwargs) -> bool:
        pass
