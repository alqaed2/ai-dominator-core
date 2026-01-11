import json
import requests
import os
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from apify_client import ApifyClient
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import get_settings
from app.schemas import DominanceRequest
from app.prompts import generate_user_prompt, generate_dna_analysis_prompt

settings = get_settings()
genai.configure(api_key=settings.GOOGLE_API_KEY)

# نستخدم هذا النموذج حصراً لاستقراره
MODEL_NAME = "gemini-1.5-flash"

# --- دوال المساعدة ---
def recursive_lowercase(obj):
    if isinstance(obj, dict):
        return {k.lower(): recursive_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_lowercase(element) for element in obj]
    else:
        return obj

def normalize_response(data, real_hashtags):
    """
    مصفاة البيانات: تضمن تحويل أي هيكل يرسله الذكاء إلى الهيكل القياسي للواجهة.
    """
    # 1. توحيد السكور
    raw_score = data.get("score_data", data.get("dominance_score", {}))
    final_score = {"score": 85, "why": ["Analysis pending"], "fix": "Check manually"}
    
    if isinstance(raw_score, dict):
        final_score["score"] = raw_score.get("score", 85)
        final_score["why"] = raw_score.get("why", ["Good potential"])
        final_score["fix"] = raw_score.get("fix", raw_score.get("minimum_fix", "Optimize hooks"))
    elif isinstance(raw_score, (int, float)):
        final_score["score"] = int(raw_score)

    # 2. توحيد السكريبت (نبحث عن كل الاحتمالات)
    raw_script = data.get("script", data.get("script_timeline", data.get("timeline", [])))
    final_script = []
    if isinstance(raw_script, list):
        for s in raw_script:
            if isinstance(s, dict):
                final_script.append({
                    "time": s.get("time", s.get("time_start", "00:00")),
                    "type": s.get("type", "Scene"),
                    "text": s.get("text", s.get("script", "...")),
                    "screen": s.get("screen", s.get("screen_text", "")),
                    "visual": s.get("visual", s.get("visual_direction", "..."))
                })

    # 3. توحيد الخطافات
    raw_hooks = data.get("hooks", [])
    final_hooks = []
    if isinstance(raw_hooks, list):
        for h in raw_hooks:
            if isinstance(h, dict):
                final_hooks.append({
                    "type": h.get("type", "Hook"),
                    "text": h.get("text", "..."),
                    "visual": h.get("visual", h.get("visual_cue", "..."))
                })

    # 4. الهاشتاجات
    ai_hashtags = data.get("hashtags", [])
    final_hashtags = real_hashtags if real_hashtags else (ai_hashtags if isinstance(ai_hashtags, list) else [])

    return {
        "score_data": final_score,
        "hooks": final_hooks,
        "script": final_script,
        "hashtags": final_hashtags,
        "caption": data.get("caption", "Watch this!"),
        "flex": data.get("flex", data.get("viral_flex_text", "AI Dominator"))
    }

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

def scrape_tiktok_dna(video_url: str):
    token = os.getenv("APIFY_TOKEN")
    if not token or not video_url: return None
    try:
        print(f"📡 Radar Scanning: {video_url}")
        client = ApifyClient(token)
        run_input = {"urls": [video_url], "shouldDownloadVideos": False}
        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        if dataset_items:
            return dataset_items[0].get("text", "") 
    except Exception as e:
        print(f"⚠️ Radar Error: {e}")
        return None
    return None

def analyze_dna_with_ai(transcript: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = generate_dna_analysis_prompt(transcript)
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Viral Structure Analysis"

class DominanceEngine:
    
    # إعادة المحاولة تلقائياً عند خطأ 429 (انتظار متصاعد)
    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_with_retry(model, prompt, safety):
        return model.generate_content(prompt, safety_settings=safety)

    @staticmethod
    def process(request: DominanceRequest, language: str = "English", video_url: str = None, radar_mode: bool = False) -> dict:
        
        reference_dna = None
        
        if radar_mode:
            reference_dna = f"Analyze patterns for niche: {request.dna.niche}"
        elif video_url and "tiktok" in video_url:
            transcript = scrape_tiktok_dna(video_url)
            if transcript:
                reference_dna = analyze_dna_with_ai(transcript)
        
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience,
            language=language,
            reference_dna=reference_dna
        )
        
        real_hashtags = fetch_external_hashtags(request.dna.niche)

        print(f"🚀 Engaging: {MODEL_NAME}")
        model = genai.GenerativeModel(model_name=MODEL_NAME, generation_config={"response_mime_type": "application/json"})
        
        safety = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        # استخدام دالة إعادة المحاولة
        try:
            response = DominanceEngine.generate_with_retry(model, user_prompt, safety)
            text_content = response.text.replace("```json", "").replace("```", "").strip()
            raw_data = json.loads(text_content)
            
            # 1. توحيد حالة الأحرف
            lowered_data = recursive_lowercase(raw_data)
            
            # 2. تصفية وتوحيد الهيكل (الحل النهائي للفراغات)
            final_data = normalize_response(lowered_data, real_hashtags)
            
            return final_data

        except Exception as e:
            print(f"❌ Critical Error: {e}")
            raise ValueError(f"System Overload or API Limit. Try again in 10s. Error: {str(e)}")
