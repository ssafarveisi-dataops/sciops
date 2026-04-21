from enum import Enum


class SignatureType(Enum):
    DATA = "data"
    MODEL = "model"
    INFERENCE = "inference"
    EVALUATION = "evaluation"
    COMPARISON = "comparison"
