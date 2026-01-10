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

# --- دالة الهاشتاجات الخارجية (RapidAPI) ---
def fetch_external_hashtags(keyword: str):
    """
    محاولة سحب هاشتاجات حقيقية. إذا لم يوجد مفتاح، نعود لقائمة فارغة ليقوم الذكاء الاصطناعي بتوليدها.
    """
    api_key = os.getenv("RAPID_API_KEY") # ⚠️ ضع المفتاح في Render Environment
    if not api_key:
        return [] # نترك المهمة للذكاء الاصطناعي
    
    try:
        # مثال لاستخدام خدمة Keyword Tool أو مشابهة
        url = "https://rocketapi-for-tiktok.p.rapidapi.com/hashtags/search"
        headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "rocketapi-for-tiktok.p.rapidapi.com"}
        response = requests.get(url, headers=headers, params={"keyword": keyword}, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return [f"#{tag['name']}" for tag in data.get('hashtags', [])[:10]]
    except:
        return [] # فشل الاتصال، نعود للذكاء الاصطناعي
    return []

class DominanceEngine:
    @staticmethod
    def process(request: DominanceRequest, language: str = "English") -> AlphaPack:
        
        # 1. إرسال اللغة للبرومبت
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience,
            language=language
        )

        # 2. جلب الهاشتاجات الحقيقية (اختياري)
        real_hashtags = fetch_external_hashtags(request.dna.niche)

        for model_name in TACTICAL_MODELS:
            try:
                model = genai.GenerativeModel(model_name=model_name, generation_config={"response_mime_type": "application/json"})
                safety_settings = {HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}
                
                response = model.generate_content(user_prompt, safety_settings=safety_settings)
                
                try:
                    cleaned_content = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(cleaned_content)
                except:
                    continue

                # دمج الهاشتاجات الحقيقية إذا وجدت
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
            except:
                continue
        
        raise ValueError("All models failed.")
