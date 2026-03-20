import pytest
from cognism_sciops.postprocessor.pipeline import PostProcessor

# -----------------------------
# 1. Abstract class enforcement
# -----------------------------


def test_postprocessor_is_abstract():
    with pytest.raises(TypeError):
        PostProcessor()


# -----------------------------
# 2. Dummy implementation
# -----------------------------


class DummyPostProcessor(PostProcessor):
    def postprocess(self, outputs):
        return [o * 2 for o in outputs]

    def validator(self, outputs):
        return all(isinstance(o, int) for o in outputs)


# -----------------------------
# 3. Happy path
# -----------------------------


def test_postprocess_basic():
    processor = DummyPostProcessor()

    outputs = [1, 2, 3]
    result = processor.postprocess(outputs=outputs)

    assert result == [2, 4, 6]


# -----------------------------
# 4. Validator behavior
# -----------------------------


def test_validator_valid_input():
    processor = DummyPostProcessor()

    assert processor.validator(outputs=[1, 2, 3]) is True


def test_validator_invalid_input():
    processor = DummyPostProcessor()

    assert processor.validator(outputs=[1, "a", 3]) is False


# -----------------------------
# 5. Edge cases
# -----------------------------


def test_postprocess_empty_input():
    processor = DummyPostProcessor()

    result = processor.postprocess(outputs=[])

    assert result == []


# -----------------------------
# 6. Validator not enforced automatically
# -----------------------------


class NoValidationPostProcessor(PostProcessor):
    def postprocess(self, outputs):
        return outputs

    def validator(self, outputs):
        return False  # always fails


def test_validator_not_automatically_called():
    processor = NoValidationPostProcessor()

    # Even though validator returns False, postprocess still runs
    result = processor.postprocess(outputs=[1, 2, 3])

    assert result == [1, 2, 3]
