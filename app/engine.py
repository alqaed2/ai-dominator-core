import json
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import get_settings
from app.schemas import DominanceRequest, AlphaPack
from app.prompts import generate_user_prompt

settings = get_settings()

genai.configure(api_key=settings.GOOGLE_API_KEY)

# القائمة التكتيكية: نعتمد على الفلاش المستقر فقط
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

                # تنظيف النص من شوائب الماركداون
                cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()
                
                # --- نقطة التصحيح هنا ---
                data = json.loads(cleaned_content)
                # -----------------------

                print(f"✅ SUCCESS.")
                
                return AlphaPack(
                    title=f"Protocol ({model_name}): {request.topic_or_keyword}",
                    dominance_score={
                        "score": data.get("dominance_score", {}).get("score", 85),
                        "why": data.get("dominance_score", {}).get("why", ["Viral potential confirmed."]),
                        "minimum_fix": data.get("dominance_score", {}).get("minimum_fix", "Enhance hook visual.")
                    },
                    hooks=[
                        {"type": h.get("type", "Type"), "text": h.get("text", "..."), "visual_cue": h.get("visual_cue", "...")} 
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
                    caption=data.get("caption", "Caption here."),
                    viral_flex_text=data.get("viral_flex_text", "Engineered by AI.")
                )

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                last_error = str(e)
                continue

        # إذا وصلنا هنا، فهذا يعني الفشل التام
        raise ValueError(f"Execution Failed. Error: {last_error}")
