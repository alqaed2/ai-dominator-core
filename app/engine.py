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

# --- قائمة النماذج المستقرة (The Stable Fleet) ---
# تم استبدال النسخ التجريبية بالنسخ المستقرة ذات الحصة المجانية العالية
TACTICAL_MODELS = [
    "gemini-1.5-flash",          # الأسرع والأعلى حصة (15 طلب/دقيقة)
    "gemini-1.5-flash-latest",   # أحدث نسخة مستقرة من الفلاش
    "gemini-1.5-pro",            # الأذكى (أبطأ قليلاً، 2 طلب/دقيقة)
    "gemini-1.5-pro-latest"      # أحدث نسخة مستقرة من البرو
]

class DominanceEngine:
    """
    Nebula Failover Engine: محرك ذكي يقوم بالتبديل التلقائي بين النماذج.
    تم ضبطه الآن على النسخ المستقرة (Stable V1.5) لتجنب أخطاء الحصة (429).
    """

    @staticmethod
    def process(request: DominanceRequest) -> AlphaPack:
        
        # 1. تجهيز البرومبت
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience
        )

        last_error = None

        # 2. حلقة التدوير التكتيكي
        for model_name in TACTICAL_MODELS:
            try:
                print(f"🔄 Engaging Model: {model_name} for topic: {request.topic_or_keyword}...")
                
                # إعداد النموذج
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

                # التحقق
                try:
                    raw_content = response.text
                except ValueError:
                    print(f"⚠️ Model {model_name} BLOCKED content.")
                    last_error = "Blocked by Safety Filters"
                    continue

                # التنظيف
                cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()
                data = json.loads(cleaned_content)

                # النجاح
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
                error_msg = str(e)
                print(f"❌ Failed with {model_name}: {error_msg}")
                last_error = error_msg
                time.sleep(2) # زدنا وقت الانتظار قليلاً لإعطاء النفس للنظام
                continue

        # الفشل النهائي
        print("🔥 ALL MODELS FAILED.")
        raise ValueError(f"System Overload: All models failed. Ensure API Key quota. Last error: {last_error}")
