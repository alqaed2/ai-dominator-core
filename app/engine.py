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

def smart_get(data, keys: list, default=None):
    """
    دالة ذكية ومحمية ضد أخطاء الأنواع.
    """
    # حماية ضد البيانات غير القاموسية (مثل int أو string)
    if not isinstance(data, dict):
        return default
        
    # تحويل المفاتيح للمقارنة
    normalized_data = {k.lower(): v for k, v in data.items()}
    
    for key in keys:
        if key.lower() in normalized_data:
            return normalized_data[key.lower()]
    return default

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
                data = json.loads(text_content)

                # --- التصحيح الذكي (Smart Fixer) ---
                
                # 1. Score Fixer (معالجة جميع الحالات)
                raw_score = smart_get(data, ["dominance_score", "DominanceScore", "score"], {})
                
                # إذا جاء السكور كرقم مباشر (خطأ شائع من الذكاء الاصطناعي)
                if isinstance(raw_score, int) or isinstance(raw_score, float):
                    safe_score = {
                        "score": int(raw_score),
                        "why": ["Analysis provided in hooks"],
                        "minimum_fix": "Check engagement manually"
                    }
                else:
                    # الحالة الطبيعية (قاموس)
                    safe_score = {
                        "score": smart_get(raw_score, ["score", "val", "value"], 85),
                        "why": smart_get(raw_score, ["why", "reasons"], ["High Potential"]),
                        "minimum_fix": smart_get(raw_score, ["minimum_fix", "fix", "improvement"], "Check hooks")
                    }

                # 2. Hooks Fixer
                raw_hooks = smart_get(data, ["hooks", "viral_hooks"], [])
                if not isinstance(raw_hooks, list): raw_hooks = [] # حماية إضافية
                
                safe_hooks = []
                for h in raw_hooks:
                    if isinstance(h, dict): # التأكد أن العنصر قاموس
                        safe_hooks.append({
                            "type": smart_get(h, ["type", "category"], "Hook"),
                            "text": smart_get(h, ["text", "content"], "..."),
                            "visual_cue": smart_get(h, ["visual_cue", "visual", "scene"], "Cinematic shot")
                        })

                # 3. Script Fixer
                raw_timeline = smart_get(data, ["script_timeline", "script", "timeline"], [])
                if not isinstance(raw_timeline, list): raw_timeline = []
                
                safe_timeline = []
                for s in raw_timeline:
                    if isinstance(s, dict):
                        safe_timeline.append({
                            "time_start": smart_get(s, ["time_start", "start"], "00:00"),
                            "time_end": smart_get(s, ["time_end", "end"], "00:00"),
                            "type": smart_get(s, ["type", "section"], "Body"),
                            "script": smart_get(s, ["script", "text", "voiceover"], "..."),
                            "screen_text": smart_get(s, ["screen_text", "screen", "overlay"], ""),
                            "visual_direction": smart_get(s, ["visual_direction", "visual", "action"], "")
                        })

                # 4. Hashtags & Caption Fixer
                ai_hashtags = smart_get(data, ["hashtags", "tags"], [])
                if not isinstance(ai_hashtags, list): ai_hashtags = []
                
                final_hashtags = real_hashtags if real_hashtags else ai_hashtags
                
                final_caption = smart_get(data, ["caption", "description"], "Check this out!")
                final_flex = smart_get(data, ["viral_flex_text", "flex"], "Engineered by AI.")

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
        
        raise ValueError(f"System Exhausted. Last Error: {last_error}")
