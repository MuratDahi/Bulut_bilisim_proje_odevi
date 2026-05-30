from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import joblib
import librosa
import numpy as np
import os
import uvicorn

app = FastAPI()

# CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. HTML ve diğer dosyaların olduğu dizini statik olarak tanımla
app.mount("/static", StaticFiles(directory="."), name="static")

# 2. Ana dizine gelen isteği ASD.html dosyasına yönlendir
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# Model yükleme
model = joblib.load('crynet_model.pkl')

def ozellik_cikar(file_path):
    y, sr = librosa.load(file_path, duration=3)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0).reshape(1, -1)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        features = ozellik_cikar(temp_filename)
        prediction = model.predict(features)
        
        label = int(float(prediction[0]))
        # HTML'in İngilizce olduğu için sonucu İngilizce döndürüyoruz
        is_cry = "CRY DETECTED" if label == 1 else "CRY NOT DETECTED"
        
        return {"result": is_cry}
    
    except Exception as e:
        return {"result": f"Error: {str(e)}"}
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)