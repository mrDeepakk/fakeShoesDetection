from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from model_loader import predict_image
import uvicorn
import shutil
import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage
import os
class SubscribeRequest(BaseModel):
    email: str

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

@app.post("/subscribe")
def subscribe(request: SubscribeRequest):
    receiver_email = request.email
    subject = "You're Subscribed to Shoe Detection Updates 👟"
    body = f"Hello,\n\nThank you for subscribing with {receiver_email}!\nYou'll now receive updates."

    try:
        send_email(receiver_email, subject, body)
        save_email(receiver_email)  # Save the email
        return {"message": "You're now subscribed! 🎉"}
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}

def send_email(to_email: str, subject: str, body: str):
    EMAIL = os.getenv("EMAIL_HOST")            # Your Gmail e.g., your_email@gmail.com
    PASSWORD = os.getenv("EMAIL_PASSWORD")     # App password, not Gmail password

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

def save_email(email: str, file_path: str = "subscribers.txt"):
    with open(file_path, "a") as file:
        file.write(email + "\n")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
