import pytest
from cognism_sciops.inference.service import Service
from pydantic import BaseModel

# -----------------------------
# Dummy components
# -----------------------------


class DummyModel:
    async def infer(self, batch):
        return [x["value"] * 2 for x in batch]


class DummyPreprocessor:
    def preprocess(self, batch):
        return batch  # no-op


class DummyPostprocessor:
    def postprocess(self, outputs):
        return [o + 1 for o in outputs]


# -----------------------------
# Dummy Service implementation
# -----------------------------


class DummyService(Service):
    def build_model(self):
        return DummyModel()

    def build_preprocessor(self):
        return DummyPreprocessor()

    def build_postprocessor(self):
        return DummyPostprocessor()


# -----------------------------
# Input schema
# -----------------------------


class InputModel(BaseModel):
    value: int


# -----------------------------
# Test
# -----------------------------


@pytest.mark.asyncio
async def test_service_pipeline():
    service = DummyService()

    inputs = [InputModel(value=1), InputModel(value=2)]

    result = await service(inputs)

    # Expected:
    # preprocess: identity
    # model: value * 2 -> [2, 4]
    # postprocess: +1 -> [3, 5]
    assert result == [3, 5]
