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

TACTICAL_MODELS = ["gemini-1.5-flash", "gemini-pro"]

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

def recursive_lowercase(obj):
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
                data = recursive_lowercase(raw_data)

                # --- المعالج المرن (The Elastic Handler) ---

                # 1. Score Handling
                # قد يكون الـ score رقماً مباشراً، أو قاموساً، أو غير موجود
                raw_score = data.get("score_data", data.get("dominance_score", {}))
                
                safe_score = {
                    "score": 85, 
                    "why": ["Analysis provided in content"], 
                    "minimum_fix": "Review manually"
                }

                if isinstance(raw_score, dict):
                    safe_score["score"] = raw_score.get("score", 85)
                    safe_score["why"] = raw_score.get("why", ["Good potential"])
                    safe_score["minimum_fix"] = raw_score.get("fix", raw_score.get("minimum_fix", "Check flow"))
                elif isinstance(raw_score, int) or isinstance(raw_score, float):
                    safe_score["score"] = int(raw_score)

                # 2. Hooks Handling (علاج مشكلة النصوص)
                safe_hooks = []
                raw_hooks = data.get("hooks", [])
                if isinstance(raw_hooks, list):
                    for h in raw_hooks:
                        if isinstance(h, dict):
                            # الحالة المثالية: قاموس
                            safe_hooks.append({
                                "type": h.get("type", "Hook"),
                                "text": h.get("text", "..."),
                                "visual_cue": h.get("visual", h.get("visual_cue", "Cinematic shot"))
                            })
                        elif isinstance(h, str):
                            # الحالة الكارثية السابقة (تم حلها): نص عادي
                            safe_hooks.append({
                                "type": "Viral Hook",
                                "text": h, # نستخدم النص كما هو
                                "visual_cue": "Camera zoom in on speaker" # نضع وصفاً افتراضياً
                            })

                # 3. Script Handling (علاج مشكلة النصوص)
                safe_timeline = []
                # البحث عن أي مفتاح محتمل للسكريبت
                raw_script = data.get("script", data.get("script_timeline", data.get("timeline", [])))
                
                if isinstance(raw_script, list):
                    for s in raw_script:
                        if isinstance(s, dict):
                            safe_timeline.append({
                                "time_start": s.get("time", s.get("time_start", "00:00")),
                                "time_end": "",
                                "type": s.get("type", "Scene"),
                                "script": s.get("text", s.get("script", "...")),
                                "screen_text": s.get("screen", s.get("screen_text", "")),
                                "visual_direction": s.get("visual", s.get("visual_direction", "Show action"))
                            })
                        elif isinstance(s, str):
                            # إذا جاء السكريبت كقائمة جمل نصية
                            safe_timeline.append({
                                "time_start": "00:00",
                                "time_end": "",
                                "type": "Script Line",
                                "script": s,
                                "screen_text": "",
                                "visual_direction": "Dynamic shot"
                            })

                # 4. Hashtags & Caption
                ai_hashtags = data.get("hashtags", [])
                if not isinstance(ai_hashtags, list): ai_hashtags = [] # حماية
                
                final_hashtags = real_hashtags if real_hashtags else ai_hashtags
                
                final_caption = data.get("caption", "Check this out!")
                if not isinstance(final_caption, str): final_caption = "Auto Caption"

                final_flex = data.get("flex", data.get("viral_flex_text", "AI Generated"))
                if not isinstance(final_flex, str): final_flex = "AI Domination"

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
