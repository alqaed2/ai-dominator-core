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

# القائمة التكتيكية
TACTICAL_MODELS = ["gemini-1.5-flash", "gemini-pro"]

def fetch_external_hashtags(keyword: str):
    api_key = os.getenv("RAPID_API_KEY")
    if not api_key:
        return [] 
    try:
        url = "https://rocketapi-for-tiktok.p.rapidapi.com/hashtags/search"
        headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "rocketapi-for-tiktok.p.rapidapi.com"}
        response = requests.get(url, headers=headers, params={"keyword": keyword}, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [f"#{tag['name']}" for tag in data.get('hashtags', [])[:10]]
    except:
        return []
    return []

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
                
                # تنظيف النص
                text_content = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(text_content)

                # --- الحماية الدفاعية (Defensive Mapping) ---
                # هنا نضمن وجود البيانات حتى لو نسيها النموذج
                
                # 1. Score Guard
                raw_score = data.get("dominance_score", {})
                safe_score = {
                    "score": raw_score.get("score", 0),
                    "why": raw_score.get("why", ["Analysis pending..."]),
                    "minimum_fix": raw_score.get("minimum_fix", "Review content manually")
                }

                # 2. Hooks Guard
                raw_hooks = data.get("hooks", [])
                safe_hooks = []
                for h in raw_hooks:
                    safe_hooks.append({
                        "type": h.get("type", "Hook"),
                        "text": h.get("text", "..."),
                        "visual_cue": h.get("visual_cue", "...")
                    })

                # 3. Script Guard
                raw_timeline = data.get("script_timeline", [])
                safe_timeline = []
                for s in raw_timeline:
                    safe_timeline.append({
                        "time_start": s.get("time_start", "00:00"),
                        "time_end": s.get("time_end", "00:00"),
                        "type": s.get("type", "Section"),
                        "script": s.get("script", "..."),
                        "screen_text": s.get("screen_text", ""),
                        "visual_direction": s.get("visual_direction", "")
                    })

                # دمج الهاشتاجات
                final_hashtags = real_hashtags if real_hashtags else data.get("hashtags", [])

                return AlphaPack(
                    title=f"Protocol ({model_name})",
                    dominance_score=safe_score,
                    hooks=safe_hooks,
                    script_timeline=safe_timeline,
                    hashtags=final_hashtags,
                    caption=data.get("caption", ""),
                    viral_flex_text=data.get("viral_flex_text", "AI Generated")
                )
            except Exception as e:
                print(f"❌ Error with {model_name}: {str(e)}")
                last_error = str(e)
                continue
        
        raise ValueError(f"System Exhausted. Last Error: {last_error}")
