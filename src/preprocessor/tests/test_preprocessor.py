import pytest
from cognism_sciops.preprocessor.pipeline import PreProcessor
from pydantic import BaseModel

# -----------------------------
# 1. Abstract enforcement
# -----------------------------


def test_preprocessor_is_abstract():
    with pytest.raises(TypeError):
        PreProcessor(is_inference_mode=True)


# -----------------------------
# 2. Dummy implementation
# -----------------------------


class DummyPreProcessor(PreProcessor):
    def preprocess_single(self, data, **kwargs):
        return {"value": data["value"] * 2}

    def preprocess(self, batch_data, **kwargs):
        processed = [self.preprocess_single(d) for d in batch_data]
        return self.collate(processed)

    def collate(self, batch, **kwargs):
        return [item["value"] for item in batch]


# -----------------------------
# 3. Input schema
# -----------------------------


class InputModel(BaseModel):
    value: int


# -----------------------------
# 4. Happy path
# -----------------------------


def test_preprocess_pipeline():
    processor = DummyPreProcessor(is_inference_mode=True)

    inputs = [InputModel(value=1), InputModel(value=2)]

    # simulate Service behavior (BaseModel -> dict)
    inputs_dict = [x.model_dump() for x in inputs]

    result = processor.preprocess(inputs_dict)

    assert result == [2, 4]


# -----------------------------
# 5. preprocess_single correctness
# -----------------------------


def test_preprocess_single():
    processor = DummyPreProcessor(is_inference_mode=True)

    result = processor.preprocess_single({"value": 3})

    assert result == {"value": 6}


# -----------------------------
# 6. collate correctness
# -----------------------------


def test_collate():
    processor = DummyPreProcessor(is_inference_mode=True)

    batch = [{"value": 2}, {"value": 4}]

    result = processor.collate(batch)

    assert result == [2, 4]


# -----------------------------
# 7. Empty batch
# -----------------------------


def test_empty_batch():
    processor = DummyPreProcessor(is_inference_mode=True)

    result = processor.preprocess([])

    assert result == []


# -----------------------------
# 8. is_inference_mode behavior
# -----------------------------


class ModeAwarePreProcessor(PreProcessor):
    def preprocess_single(self, data, **kwargs):
        if self.is_inference_mode:
            return data["value"]
        return data["value"] * 10

    def preprocess(self, batch_data, **kwargs):
        processed = [self.preprocess_single(d) for d in batch_data]
        return self.collate(processed)

    def collate(self, batch, **kwargs):
        return batch


def test_inference_mode_true():
    processor = ModeAwarePreProcessor(is_inference_mode=True)

    result = processor.preprocess([{"value": 2}])

    assert result == [2]


def test_inference_mode_false():
    processor = ModeAwarePreProcessor(is_inference_mode=False)

    result = processor.preprocess([{"value": 2}])

    assert result == [20]


# -----------------------------
# 9. Invalid input handling (optional)
# -----------------------------


def test_invalid_input():
    processor = DummyPreProcessor(is_inference_mode=True)

    with pytest.raises(KeyError):
        processor.preprocess([{"wrong_key": 1}])
