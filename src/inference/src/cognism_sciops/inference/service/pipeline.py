"""
This module defines the Service class, which is an abstract base class
for implementing a service in the sciops inference pipeline.
The Service class defines the structure of the service, including the model,
preprocessor, and postprocessor components, and how they interact with each
other during inference. Subclasses of Service should implement the build_model,
build_preprocessor, and build_postprocessor methods to define the specific
behavior of the service.
"""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from cognism_sciops.signatures import SignatureType

# This implementation may change

SignatureType.MODEL = "model"


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
        # Implement in subclass, return an object with an infer method that takes
        # in the preprocessor output and returns the model outputs.
        # the model should implement an async infer method to allow for
        # async inference calls.
        # the body of the infer method may not implement any async functionality,
        # but the method itself should be async to allow for flexibility in
        # the model implementation.
        pass

    @abstractmethod
    def build_preprocessor(self):
        # Implement in subclass, return an object with a preprocess method that
        # takes in the raw batch inputs and returns the processed batch to be
        # passed to the model infer method
        pass

    @abstractmethod
    def build_postprocessor(self):
        # Implement in subclass, return an object with a postprocess method that
        # takes in the model outputs and returns the final postprocessed outputs
        pass
