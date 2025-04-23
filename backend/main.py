from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from model_loader import predict_image
import uvicorn
import shutil
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for all origins (adjust as needed for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "backend/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class_mapping = {
    "0": "original jordan 1",
    "1": "fake jordan 1",
    "2": "real air force",
    "3": "fake air force"
}

@app.get("/")
@app.head("/")
def home():
    return {"message": "Fake Shoe Detection API is running"}

@app.get("/health")
@app.head("/health")
def health_check():
    return Response(content="OK", status_code=200)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    start_time = time.time()
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict using model
    predicted_class_index, confidence_score = predict_image(file_path)
    prediction_label = class_mapping.get(str(predicted_class_index), "unknown")

    # Delete file after processing (optional cleanup)
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Warning: Failed to delete uploaded file. Reason: {e}")

    end_time = time.time()
    inference_time = round(end_time - start_time, 2)

    return {
        "filename": file.filename,
        "result": {
            "label": prediction_label,
            "confidence": round(confidence_score, 4),
            "inference_time_sec": inference_time
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
