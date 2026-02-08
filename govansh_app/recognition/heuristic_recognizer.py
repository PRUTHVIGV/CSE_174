"""
Heuristic recognizer (runs everywhere).
This keeps GOVANSH functional while you prepare a real CNN model.
"""

import cv2
import numpy as np
from datetime import datetime
from ..breeds import BREED_DATABASE


class HeuristicRecognizer:
    def __init__(self):
        self.breeds = list(BREED_DATABASE.keys())
        self.prediction_count = 0

    def analyze_image(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h_mean, s_mean, v_mean = np.mean(hsv[:, :, 0]), np.mean(hsv[:, :, 1]), np.mean(hsv[:, :, 2])
        b_mean, g_mean, r_mean = np.mean(image[:, :, 0]), np.mean(image[:, :, 1]), np.mean(image[:, :, 2])
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        return {
            "h_mean": float(h_mean),
            "s_mean": float(s_mean),
            "v_mean": float(v_mean),
            "r_mean": float(r_mean),
            "g_mean": float(g_mean),
            "b_mean": float(b_mean),
            "brightness": float((r_mean + g_mean + b_mean) / 3.0),
            "edge_density": float(edge_density),
        }

    def predict_breed(self, image):
        features = self.analyze_image(image)
        self.prediction_count += 1

        scores = {}
        brightness = features["brightness"]
        r_ratio = features["r_mean"] / max(features["brightness"], 1.0)
        saturation = features["s_mean"]

        # Buffalo detection
        if brightness < 80:
            scores["Murrah Buffalo"] = 0.88 + np.random.uniform(0, 0.10)
            scores["Mehsana Buffalo"] = 0.72 + np.random.uniform(0, 0.12)
            for breed in self.breeds:
                if "Buffalo" not in breed:
                    scores[breed] = np.random.uniform(0.05, 0.20)

        # Reddish/Brown cattle
        elif r_ratio > 0.38 and saturation > 50:
            scores["Gir"] = 0.78 + np.random.uniform(0, 0.18)
            scores["Sahiwal"] = 0.72 + np.random.uniform(0, 0.18)
            scores["Red Sindhi"] = 0.68 + np.random.uniform(0, 0.18)
            scores["Rathi"] = 0.42 + np.random.uniform(0, 0.18)
            for breed in self.breeds:
                if breed not in scores:
                    scores[breed] = np.random.uniform(0.05, 0.25)

        # White/Grey cattle
        elif brightness > 150:
            scores["Tharparkar"] = 0.76 + np.random.uniform(0, 0.16)
            scores["Ongole"] = 0.74 + np.random.uniform(0, 0.16)
            scores["Hariana"] = 0.72 + np.random.uniform(0, 0.16)
            scores["Kankrej"] = 0.70 + np.random.uniform(0, 0.16)
            for breed in self.breeds:
                if breed not in scores:
                    scores[breed] = np.random.uniform(0.05, 0.22)

        # Mixed colors
        else:
            for breed in self.breeds:
                if "Buffalo" in breed:
                    scores[breed] = np.random.uniform(0.25, 0.55)
                else:
                    scores[breed] = np.random.uniform(0.35, 0.75)

        total = sum(scores.values())
        scores = {k: float(v / total) for k, v in scores.items()}

        top_breed = max(scores, key=scores.get)
        confidence = scores[top_breed]
        top_5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

        if confidence >= 0.85:
            conf_level = {"level": "Very High", "color": "#00ff88", "icon": "✓✓", "desc": "Highly confident"}
        elif confidence >= 0.70:
            conf_level = {"level": "High", "color": "#4ade80", "icon": "✓", "desc": "Confident"}
        elif confidence >= 0.55:
            conf_level = {"level": "Moderate", "color": "#fbbf24", "icon": "~", "desc": "Moderate"}
        elif confidence >= 0.40:
            conf_level = {"level": "Low", "color": "#fb923c", "icon": "!", "desc": "Low confidence"}
        else:
            conf_level = {"level": "Very Low", "color": "#ef4444", "icon": "!!", "desc": "Verify manually"}

        return {
            "breed": top_breed,
            "hindi_name": BREED_DATABASE.get(top_breed, {}).get("hindi_name", ""),
            "confidence": round(float(confidence), 4),
            "confidence_level": conf_level,
            "top_5": [(b, round(float(s), 4)) for b, s in top_5],
            "breed_info": BREED_DATABASE.get(top_breed, {}),
            "analysis": {
                "brightness": round(features["brightness"], 1),
                "color_saturation": round(features["s_mean"], 1),
                "pattern_density": round(features["edge_density"] * 100, 2),
            },
            "prediction_id": f"GVS{self.prediction_count:05d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_version": "GOVANSH Heuristic v2.1 (CNN-ready)",
        }

