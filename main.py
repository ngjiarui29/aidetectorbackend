import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🌐 This block allows your Wix frontend to securely communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your Wix domain to bypass browser restrictions
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 Free Hugging Face AI Model Endpoint (Vision Transformer for synthetic image detection)
HF_API_URL = "https://api-inference.huggingface.co/models/capcheck/ai-image-detector"
# Keep your actual Hugging Face authorization token format if you have one set up
headers = {"Authorization": "Bearer hf_xxxxxx"} 

@app.get("/")
def read_root():
    return {"status": "AI Detector Server is Running Online"}

@app.post("/api/detect")
async def detect_ai(file: UploadFile = File(...)):
    try:
        # Reading the uploaded file bytes
        file_bytes = await file.read()
        
        # Forwarding the raw bytes straight to Hugging Face
        response = requests.post(HF_API_URL, headers=headers, data=file_bytes)
        
        return {"analysis": response.json()}
    except Exception as e:
        return {"error": str(e)}
