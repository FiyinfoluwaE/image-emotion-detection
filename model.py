import argparse
import os
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN
from emotiefflib.facial_analysis import EmotiEffLibRecognizer, get_model_list


def detect_faces(image: np.ndarray, device: str) -> list:
    mtcnn = MTCNN(keep_all=True, device=device)
    boxes, _ = mtcnn.detect(image)
    faces = []
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = [int(v) for v in box[:4]]
            if x2 - x1 > 0 and y2 - y1 > 0:
                faces.append(image[y1:y2, x1:x2, :])
    return faces


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--model", default=get_model_list()[0])
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        raise FileNotFoundError(args.image)
    img = Image.open(args.image).convert("RGB")
    img_np = np.array(img)
    faces = detect_faces(img_np, args.device)
    if not faces:
        print("No faces detected.")
        return
    recognizer = EmotiEffLibRecognizer(engine="torch", model_name=args.model, device=args.device)
    features = recognizer.extract_features(faces)
    labels, scores = recognizer.classify_emotions(features, logits=False)
    for i, lbl in enumerate(labels):
        idx_map = recognizer.idx_to_emotion_class
        inv_map = {v: k for k, v in idx_map.items()}
        idx = inv_map[lbl]
        conf = float(scores[i][idx])
        print(f"face={i} label={lbl} confidence={conf:.4f}")


if __name__ == "__main__":
    main()