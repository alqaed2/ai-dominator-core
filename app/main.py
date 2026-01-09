from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings, Settings
from app.schemas import DominanceRequest, AlphaPack
from app.engine import DominanceEngine

# تهيئة الإعدادات
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="The Supreme Engine for Controlled Viral Innovation."
)

# إعدادات CORS (للسماح بالاتصال من أي مكان حالياً)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints ---

@app.get("/")
async def root():
    """
    Health Check & Status Protocol.
    """
    return {
        "system": "AI DOMINATOR",
        "status": "OPERATIONAL 🟢",
        "mode": "SUPREME CONTROL",
        "version": settings.VERSION
    }

@app.post(f"{settings.API_PREFIX}/generate", response_model=AlphaPack)
async def generate_dominance_pack(request: DominanceRequest):
    """
    Heart of the System: يستقبل الـ DNA والنيش، ويعيد حزمة محتوى كاملة.
    """
    try:
        # استدعاء المحرك لتنفيذ العمليات
        result = DominanceEngine.process(request)
        return result
    except Exception as e:
        # في حالة الخطأ، لا ننهار، بل نعيد رسالة خطأ منظمة
        raise HTTPException(status_code=500, detail=f"Core Engine Failure: {str(e)}")

# لتشغيل السيرفر محلياً إذا تطلب الأمر
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)