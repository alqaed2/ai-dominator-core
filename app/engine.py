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

# نستخدم فلاش وبرو لضمان العمل
TACTICAL_MODELS = ["gemini-flash-latest"]

def fetch_external_hashtags(keyword: str):
    """
    محاولة سحب هاشتاجات حقيقية بشكل آمن (Non-blocking).
    """
    api_key = os.getenv("RAPID_API_KEY")
    if not api_key:
        return [] 
    
    try:
        url = "https://rocketapi-for-tiktok.p.rapidapi.com/hashtags/search"
        headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "rocketapi-for-tiktok.p.rapidapi.com"}
        # مهلة قصيرة جداً (2 ثانية) لكي لا نعطل المستخدم
        response = requests.get(url, headers=headers, params={"keyword": keyword}, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [f"#{tag['name']}" for tag in data.get('hashtags', [])[:10]]
    except Exception as e:
        print(f"⚠️ Hashtag API Warning: {e}") # مجرد تحذير في السجلات
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
        
        # محاولة جلب هاشتاجات (دون تعطيل النظام)
        real_hashtags = fetch_external_hashtags(request.dna.niche)
        
        last_error = ""

        for model_name in TACTICAL_MODELS:
            try:
                print(f"🚀 Trying Model: {model_name}")
                model = genai.GenerativeModel(model_name=model_name, generation_config={"response_mime_type": "application/json"})
                
                # إعدادات أمان مفتوحة
                safety = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
                
                response = model.generate_content(user_prompt, safety_settings=safety)
                
                # تنظيف الرد
                text_content = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(text_content)

                # دمج الهاشتاجات (الأولوية للحقيقية)
                final_hashtags = real_hashtags if real_hashtags else data.get("hashtags", [])

                return AlphaPack(
                    title=f"Protocol ({model_name})",
                    dominance_score=data.get("dominance_score"),
                    hooks=data.get("hooks"),
                    script_timeline=data.get("script_timeline"),
                    hashtags=final_hashtags,
                    caption=data.get("caption"),
                    viral_flex_text=data.get("viral_flex_text")
                )
            except Exception as e:
                print(f"❌ Error with {model_name}: {str(e)}")
                last_error = str(e)
                continue
        
        # إذا وصلنا هنا، نعيد الخطأ الحقيقي للواجهة
        raise ValueError(f"System Exhausted. Last Error: {last_error}")

