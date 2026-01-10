import json
import requests
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import get_settings
from app.schemas import DominanceRequest, AlphaPack
from app.prompts import generate_user_prompt

settings = get_settings()
genai.configure(api_key=settings.GOOGLE_API_KEY)

TACTICAL_MODELS = ["gemini-flash-latest"]

def fetch_external_hashtags(keyword: str):
    api_key = os.getenv("RAPID_API_KEY")
    if not api_key: return [] 
    try:
        url = "https://rocketapi-for-tiktok.p.rapidapi.com/hashtags/search"
        headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "rocketapi-for-tiktok.p.rapidapi.com"}
        response = requests.get(url, headers=headers, params={"keyword": keyword}, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [f"#{tag['name']}" for tag in data.get('hashtags', [])[:10]]
    except: return []
    return []

# --- المصحح الجذري (The Sanitizer) ---
def recursive_lowercase(obj):
    """
    تحويل كل المفاتيح في القاموس (والقواميس المتداخلة) إلى حروف صغيرة
    لضمان تطابق البيانات مهما كانت حالة الأحرف.
    """
    if isinstance(obj, dict):
        return {k.lower(): recursive_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_lowercase(element) for element in obj]
    else:
        return obj

class DominanceEngine:
    @staticmethod
    def process(request: DominanceRequest, language: str = "English") -> AlphaPack:
        
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience,
            language=language
        )
        
        real_hashtags = fetch_external_hashtags(request.dna.niche)
        last_error = ""

        for model_name in TACTICAL_MODELS:
            try:
                print(f"🚀 Trying Model: {model_name}")
                model = genai.GenerativeModel(model_name=model_name, generation_config={"response_mime_type": "application/json"})
                
                safety = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
                
                response = model.generate_content(user_prompt, safety_settings=safety)
                
                text_content = response.text.replace("```json", "").replace("```", "").strip()
                raw_data = json.loads(text_content)

                # 🔥 الخطوة السحرية: توحيد المفاتيح
                data = recursive_lowercase(raw_data)

                # الآن نستخرج البيانات بأسماء بسيطة وموحدة
                
                # 1. Score
                # نبحث عن score_data أو dominance_score
                s_data = data.get("score_data", data.get("dominance_score", {}))
                safe_score = {
                    "score": s_data.get("score", 85),
                    "why": s_data.get("why", ["Strong potential"]),
                    "minimum_fix": s_data.get("fix", s_data.get("minimum_fix", "Check visual pacing"))
                }

                # 2. Hooks
                safe_hooks = []
                for h in data.get("hooks", []):
                    safe_hooks.append({
                        "type": h.get("type", "Hook"),
                        "text": h.get("text", "..."),
                        "visual_cue": h.get("visual", h.get("visual_cue", "..."))
                    })

                # 3. Script
                # المفتاح قد يكون script أو script_timeline
                raw_script = data.get("script", data.get("script_timeline", []))
                safe_timeline = []
                for s in raw_script:
                    safe_timeline.append({
                        "time_start": s.get("time", s.get("time_start", "00:00")),
                        "time_end": "", # اختياري في النسخة المبسطة
                        "type": s.get("type", "Scene"),
                        "script": s.get("text", s.get("script", "...")),
                        "screen_text": s.get("screen", s.get("screen_text", "")),
                        "visual_direction": s.get("visual", s.get("visual_direction", "..."))
                    })

                # 4. Hashtags
                ai_hashtags = data.get("hashtags", [])
                final_hashtags = real_hashtags if real_hashtags else ai_hashtags
                
                final_caption = data.get("caption", "Watch this!")
                final_flex = data.get("flex", data.get("viral_flex_text", "AI Generated"))

                return AlphaPack(
                    title=f"Protocol ({model_name})",
                    dominance_score=safe_score,
                    hooks=safe_hooks,
                    script_timeline=safe_timeline,
                    hashtags=final_hashtags,
                    caption=final_caption,
                    viral_flex_text=final_flex
                )

            except Exception as e:
                print(f"❌ Error with {model_name}: {str(e)}")
                last_error = str(e)
                continue
        
        raise ValueError(f"System Error: {last_error}")
