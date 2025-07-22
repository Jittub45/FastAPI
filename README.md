# FastAPI Insurance Premium Prediction & Patient Management

This project is a full-stack application for predicting insurance premiums using a machine learning model and managing patient data with FastAPI.

## Features
- **Insurance Premium Prediction:**
  - Predicts insurance premiums based on user input (age, weight, height, income, smoking status, city, occupation).
  - Uses a trained ML model (`model.pkl`).
- **Patient Management API:**
  - Create, retrieve, update, and delete patient records.
  - Patient data stored in `patients.json`.
  - Supports sorting and filtering.
- **Streamlit Frontend:**
  - User-friendly interface for premium prediction.

## Project Structure
- `app.py` — FastAPI backend for premium prediction.
- `patients.py` — FastAPI backend for patient CRUD operations.
- `frontend.py` — Streamlit frontend for prediction.
- `main.py` — Basic FastAPI endpoints.
- `model.pkl` — Trained machine learning model.
- `patients.json` — Patient data storage.
- `requirements.txt` — Python dependencies.

## Setup & Usage
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the main Insurance Premium Prediction API (FastAPI backend):**
   ```bash
   uvicorn app:app --reload
   ```
   - This command runs the FastAPI backend defined in `app.py` (the first `app` is the filename, the second is the FastAPI instance).

3. **Run the Streamlit frontend:**
   ```bash
   streamlit run frontend.py
   ```
   - This command launches the Streamlit user interface for premium prediction.

4. **Run the Patient Management API (FastAPI backend):**
   ```bash
   uvicorn patients:app --reload
   ```
   - This command runs the patient management backend defined in `patients.py` (again, `patients` is the filename, `app` is the FastAPI instance).

## Notes
- Ensure `model.pkl` and `patients.json` are present in the project directory.
- API endpoints and parameters are defined in the respective FastAPI files.

---
For more details, refer to the code and comments in each file.
