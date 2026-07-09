import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allows your Wix frontend to securely communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Free Hugging Face AI Model Endpoint (Vision Transformer for synthetic image detection)
HF_API_URL = "https://api-inference.huggingface.co/models/capcheck/ai-image-detection"

@app.get("/")
def home():
    return {"status": "AI Detector Server is Running Online"}

@app.post("/api/detect")
async def detect_ai(file: UploadFile = File(...)):
    try:
        # Read file bytes sent from Wix
        file_bytes = await file.read()
        
        # Send the file bytes to Hugging Face's free infrastructure
        response = requests.post(HF_API_URL, data=file_bytes)
        
        if response.status_code == 200:
            return {"status": "success", "analysis": response.json()}
        else:
            return {"status": "error", "message": "AI model tier is currently waking up or busy."}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}
