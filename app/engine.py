import json
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import get_settings
from app.schemas import DominanceRequest, AlphaPack
from app.prompts import generate_user_prompt

settings = get_settings()

genai.configure(api_key=settings.GOOGLE_API_KEY)

# 🛑 القائمة النهائية: طراز واحد قياسي مضمون 100%
# هذا الاسم هو المعيار الثابت في جوجل ولا يتغير
TACTICAL_MODELS = ["gemini-1.5-flash"]

class DominanceEngine:
    """
    Standard Engine: يعتمد على Gemini 1.5 Flash فقط لضمان الاستقرار.
    """

    @staticmethod
    def process(request: DominanceRequest) -> AlphaPack:
        
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience
        )

        last_error = None

        for model_name in TACTICAL_MODELS:
            try:
                print(f"🚀 Executing with: {model_name}...")
                
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"response_mime_type": "application/json"}
                )

                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }

                response = model.generate_content(
                    user_prompt, 
                    safety_settings=safety_settings
                )

                try:
                    raw_content = response.text
                except ValueError:
                    print(f"⚠️ Blocked. Feedback: {response.prompt_feedback}")
                    last_error = "Safety Block"
                    continue

                cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()
                data = json.loads(cleaned_c
