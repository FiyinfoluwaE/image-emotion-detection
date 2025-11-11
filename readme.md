## Project Summary

This project is a Streamlit-based image emotion detection application that uses **EmotiEffLib** (PyTorch backend) to recognize human facial expressions from uploaded or captured images.

### Key Features
- **Face Detection:** Uses MTCNN to locate faces in an image.
- **Emotion Recognition:** Passes detected faces to EmotiEffLib to classify the dominant emotion (e.g. Happiness, Neutral, Sadness, Anger, Surprise).
- **Data Logging:** Saves each prediction to a local SQLite database with the user’s name, timestamp, image, predicted emotion, and confidence score.
- **CLI Inference:** Includes a `model.py` script that runs the same emotion inference from the command line, keeping the web app and backend consistent.

### Files
- `app.py` – Streamlit web interface for uploading images and viewing results.
- `model.py` – Command-line inference script using EmotiEffLib.
- `requirements.txt` – Python dependencies.
- `emotion_app.db` – SQLite database used to store prediction records.
