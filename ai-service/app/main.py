from app.routes.qa import router as qa_router
from fastapi import FastAPI
from app.routes.process import router as process_router

app = FastAPI(
    title="AI-Powered Legal Documentation Assistant",
    version="1.0.0"
)

app.include_router(process_router, prefix="/api")
app.include_router(qa_router, prefix="/api")

@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Legal Documentation Assistant AI Service is Running"
    }