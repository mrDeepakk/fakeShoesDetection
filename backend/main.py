from fastapi import FastAPI, File, UploadFile
from model_loader import predict_image
import uvicorn
import shutil
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

UPLOAD_FOLDER = "backend/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
class_mapping = {
    "0":"original jordan 1",
    "1":"fake jordan 1",
    "2":"real air force",
    "3":"fake air force"
}


@app.get("/")
def home():
    return {"message": "Fake Shoe Detection API is running"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get prediction and confidence score
    predicted_class_index, confidence_score = predict_image(file_path)

    # Map index to class label
    prediction_label = class_mapping[str(predicted_class_index)]

    return {
        "filename": file.filename,
        "prediction": prediction_label,
        "confidence_score": round(confidence_score, 4)  # Round to 4 decimal places
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
    print("Backend API is running")

# uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload