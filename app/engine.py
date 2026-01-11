import json
import requests
import os
from apify_client import ApifyClient
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import get_settings
from app.schemas import DominanceRequest
from app.prompts import generate_user_prompt, generate_dna_analysis_prompt

settings = get_settings()
genai.configure(api_key=settings.GOOGLE_API_KEY)

# القائمة التكتيكية
TACTICAL_MODELS = ["gemini-flash-latest"]

# --- دوال المساعدة ---
def recursive_lowercase(obj):
    if isinstance(obj, dict):
        return {k.lower(): recursive_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_lowercase(element) for element in obj]
    else:
        return obj

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
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = generate_dna_analysis_prompt(transcript)
    response = model.generate_content(prompt)
    return response.text

class DominanceEngine:
    @staticmethod
    def process(request: DominanceRequest, language: str = "English", video_url: str = None, radar_mode: bool = False) -> dict:
        
        reference_dna = None
        
        # 1. تفعيل الرادار أو الاستنساخ
        if radar_mode:
            # في وضع الرادار (بدون رابط)، نقوم بتحليل النيش العام
            reference_dna = f"Analyze the top performing patterns in the niche: {request.dna.niche}"
        elif video_url and "tiktok" in video_url:
            transcript = scrape_tiktok_dna(video_url)
            if transcript:
                reference_dna = analyze_dna_with_ai(transcript)
        
        # 2. تجهيز البرومبت
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience,
            language=language,
            reference_dna=reference_dna
        )
        
        real_hashtags = fetch_external_hashtags(request.dna.niche)
        last_error = ""

        for model_name in TACTICAL_MODELS:
            try:
                print(f"🚀 Engaging: {model_name}")
                model = genai.GenerativeModel(model_name=model_name, generation_config={"response_mime_type": "application/json"})
                safety = {HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}
                
                response = model.generate_content(user_prompt, safety_settings=safety)
                text_content = response.text.replace("```json", "").replace("```", "").strip()
                raw_data = json.loads(text_content)
                
                # توحيد البيانات (Dictionary only - No Pydantic)
                data = recursive_lowercase(raw_data)

                # تنظيف البيانات لضمان عدم وجود قيم فارغة
                final_data = {
                    "score_data": data.get("score_data", data.get("dominance_score", {"score": 85, "why": ["Good"], "fix": "Review"})),
                    "hooks": data.get("hooks", []),
                    "script": data.get("script", data.get("script_timeline", [])),
                    "hashtags": real_hashtags if real_hashtags else data.get("hashtags", ["#Viral"]),
                    "caption": data.get("caption", "Check this out"),
                    "flex": data.get("flex", data.get("viral_flex_text", "AI Dominator"))
                }
                
                return final_data

            except Exception as e:
                print(f"❌ Error: {e}")
                last_error = str(e)
                continue
        
        raise ValueError(f"System Error: {last_error}")

