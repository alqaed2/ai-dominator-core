import json
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import get_settings
from app.schemas import DominanceRequest, AlphaPack
from app.prompts import generate_user_prompt

settings = get_settings()

# تهيئة المفتاح العام
genai.configure(api_key=settings.GOOGLE_API_KEY)

# --- قائمة النماذج التكتيكية (مرتبة حسب الأولوية) ---
TACTICAL_MODELS = [
    "models/gemini-2.0-flash",       # Primary: السرعة والاستقرار
    "models/gemini-2.5-flash",       # Secondary: التحديث الجديد
    "models/gemini-2.0-flash-lite",  # Backup: توفير الموارد
    "models/gemini-2.5-pro"          # Last Resort: الذكاء الأعلى
]

class DominanceEngine:
    """
    Nebula Failover Engine: محرك ذكي يقوم بالتبديل التلقائي بين النماذج
    لضمان استمرار الخدمة حتى عند انتهاء الحصة (Quota).
    """

    @staticmethod
    def process(request: DominanceRequest) -> AlphaPack:
        
        # 1. تجهيز البرومبت مرة واحدة
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience
        )

        last_error = None

        # 2. حلقة التدوير التكتيكي (The Rotation Loop)
        for model_name in TACTICAL_MODELS:
            try:
                print(f"🔄 Engaging Model: {model_name} for topic: {request.topic_or_keyword}...")
                
                # إعداد النموذج الحالي
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"response_mime_type": "application/json"}
                )

                # إعدادات الأمان (إلغاء الحظر بالكامل)
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }

                # التنفيذ
                response = model.generate_content(
                    user_prompt, 
                    safety_settings=safety_settings
                )

                # التحقق من وجود نص (لتجنب الحظر الصامت)
                try:
                    raw_content = response.text
                except ValueError:
                    print(f"⚠️ Model {model_name} BLOCKED content due to Safety Filters.")
                    last_error = "Blocked by Safety Filters"
                    continue # انتقل للنموذج التالي

                # تنظيف النص
                cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()
                data = json.loads(cleaned_content)

                # النجاح! بناء وإرجاع الحزمة
                print(f"✅ SUCCESS with {model_name}")
                
                return AlphaPack(
                    title=f"Protocol ({model_name}): {request.topic_or_keyword}",
                    dominance_score={
                        "score": data.get("dominance_score", {}).get("score", 88),
                        "why": data.get("dominance_score", {}).get("why", ["High viral potential."]),
                        "minimum_fix": data.get("dominance_score", {}).get("minimum_fix", "Enhance visual pacing.")
                    },
                    hooks=[
                        {"type": h.get("type", "Type"), "text": h.get("text", "..."), "visual_cue": h.get("visual_cue", "...")} 
                        for h in data.get("hooks", [])
                    ],
                    script_timeline=[
                        {
                            "time_start": s.get("time_start", "00:00"),
                            "time_end": s.get("time_end", "00:05"),
                            "type": s.get("type", "Section"),
                            "script": s.get("script", "..."),
                            "screen_text": s.get("screen_text", ""),
                            "visual_direction": s.get("visual_direction", "")
                        }
                        for s in data.get("script_timeline", [])
                    ],
                    hashtags=data.get("hashtags", ["#Viral"]),
                    caption=data.get("caption", "Auto-generated caption."),
                    viral_flex_text=data.get("viral_flex_text", f"Engineered by AI DOMINATOR ({model_name}).")
                )

            except Exception as e:
                # تسجيل الخطأ والانتقال للنموذج التالي
                error_msg = str(e)
                print(f"❌ Failed with {model_name}: {error_msg}")
                last_error = error_msg
                time.sleep(1) # استراحة قصيرة جداً قبل المحاولة التالية
                continue

        # إذا خرجنا من الحلقة دون نجاح
        print("🔥 ALL MODELS FAILED.")
        raise ValueError(f"System Overload: All tactical models failed. Last error: {last_error}")
