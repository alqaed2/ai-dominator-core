import json
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_fixed
from app.config import get_settings
from app.schemas import DominanceRequest, AlphaPack
from app.prompts import generate_user_prompt

settings = get_settings()

# تهيئة Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

# إعداد الموديل (نستخدم Gemini 1.5 Flash لسرعته وكفاءته المجانية)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"response_mime_type": "application/json"}
)

class DominanceEngine:
    """
    Gemini-Powered Engine: يستخدم ذكاء جوجل لتوليد المحتوى.
    """

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def process(request: DominanceRequest) -> AlphaPack:
        
        # 1. تجهيز البرومبت
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience
        )

        try:
            # 2. إرسال الطلب إلى Gemini
            response = model.generate_content(user_prompt)
            
            # 3. استخراج النص (Gemini يرجعه كنص JSON مباشر بفضل الإعدادات)
            raw_content = response.text
            
            # تنظيف بسيط في حال وجود شوائب (Markdown ticks)
            cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(cleaned_content)
            
            # 4. بناء كائن البيانات (نفس الهيكلية السابقة تماماً)
            return AlphaPack(
                title=f"Gemini Protocol: {request.topic_or_keyword}",
                dominance_score={
                    "score": data.get("dominance_score", {}).get("score", 88),
                    "why": data.get("dominance_score", {}).get("why", ["Strong topic resonance detected."]),
                    "minimum_fix": data.get("dominance_score", {}).get("minimum_fix", "Improve hook visual speed.")
                },
                hooks=[
                    {"type": h.get("type", "Type"), "text": h.get("text", "Hook text"), "visual_cue": h.get("visual_cue", "Visual")} 
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
                viral_flex_text=data.get("viral_flex_text", "Engineered by AI DOMINATOR.")
            )

        except Exception as e:
            # تسجيل الخطأ لإصلاحه
            print(f"Gemini Error: {str(e)}")
            raise ValueError(f"AI Generation Failed: {str(e)}")
