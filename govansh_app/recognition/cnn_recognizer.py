"""
CNN-based recognizer (Backend recognition section).

This module defines a clean interface for CNN inference.
You can plug in a trained CNN model here later (ResNet/MobileNet).

For now, GOVANSH uses the heuristic recognizer in `heuristic_recognizer.py`
so the project runs on your current Python environment.
"""

from dataclasses import dataclass


@dataclass
class Prediction:
    breed: str
    confidence: float
    top_5: list[tuple[str, float]]
    model_version: str = "GOVANSH CNN v1.0"


class CNNRecognizer:
    """
    Placeholder for real CNN inference.

    Implement:
    - load_model()
    - predict(image_bgr) -> Prediction
    """

    def __init__(self):
        self.loaded = False

    def load_model(self):
        # TODO: load trained model weights
        self.loaded = True

    def predict(self, image_bgr):
        raise NotImplementedError(
            "CNN model not integrated yet. Use HeuristicRecognizer for demo."
        )

