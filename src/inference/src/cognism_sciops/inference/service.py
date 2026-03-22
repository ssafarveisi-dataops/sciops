from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

# This implementation may change


# Updated version of the sciops service
class Service(ABC):
    def __init__(self, **kwargs) -> None:

        self.model = self.build_model()
        self.preprocessor = self.build_preprocessor()
        self.postprocessor = self.build_postprocessor()

    async def __call__(self, batch_inputs: list[BaseModel]) -> list[Any]:

        batch_inputs: list[dict] = [single_input.model_dump() for single_input in batch_inputs]

        processed_batch = self.preprocessor.preprocess(batch_inputs)
        outputs = await self.model.infer(processed_batch)
        post_args = self.build_postprocess_args(batch_inputs, processed_batch, outputs)
        postprocessed_outputs = self.postprocessor.postprocess(**post_args)
        return postprocessed_outputs

    def build_postprocess_args(self, batch_inputs, processed_batch, outputs):
        return {"outputs": outputs}

    @abstractmethod
    def build_model(self):
        # implement in subclass, return an object with an infer method that takes
        # in the preprocessor output and returns the model outputs.
        # the model should implement an async infer method to allow for
        # async inference calls.
        # the body of the infer method may not implement any async functionality,
        # but the method itself should be async to allow for flexibility in
        # the model implementation.
        pass

    @abstractmethod
    def build_preprocessor(self):
        # implement in subclass, return an object with a preprocess method that
        # takes in the raw batch inputs and returns the processed batch to be
        # passed to the model infer method
        pass

    @abstractmethod
    def build_postprocessor(self):
        # implement in subclass, return an object with a postprocess method that
        # takes in the model outputs and returns the final postprocessed outputs
        pass
