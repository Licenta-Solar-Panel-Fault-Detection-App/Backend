from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
import shutil
import os
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import init_db
from models.panel_check import PanelCheck
from predict import predict_image
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from routes import auth
from routes import panels
from routes import checks
from database.database import async_session






app = FastAPI()

app.include_router(auth.router)
app.include_router(panels.router)

app.include_router(checks.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def root():
    return {"message": "API is running!"}

UPLOAD_DIR = "uploads"
CHECK_DIR = os.path.join(UPLOAD_DIR, "panel_checks")
os.makedirs(CHECK_DIR, exist_ok=True)


async def get_session():
    async with async_session() as session:
        yield session

@app.post("/predict/")
async def predict(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
                  ):
    file_ext = os.path.splitext(file.filename)[-1]
    temp_filename = f"{uuid4()}{file_ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        prediction = predict_image(temp_path)

        # Mutăm imaginea în folderul permanent cu nume sugestiv
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"check_{timestamp}{file_ext}"
        final_path = os.path.join(CHECK_DIR, final_filename)
        shutil.move(temp_path, final_path)

        check = PanelCheck(
            #panel_id: int = Form(...)

            panel_id=1,
            status=prediction,
            image_path=final_path,
            timestamp=datetime.utcnow()
        )
        session.add(check)
        await session.commit()
        await session.refresh(check)

        return JSONResponse(content={
            "prediction": prediction,
            "check_id": check.id
        })

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return JSONResponse(status_code=500, content={"error": str(e)})