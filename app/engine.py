import json
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed
from app.config import get_settings
from app.schemas import DominanceRequest, AlphaPack
from app.prompts import DOMINATOR_SYSTEM_PROMPT, generate_user_prompt

settings = get_settings()

# تهيئة العميل (يجب التأكد من وجود المفتاح في الإعدادات)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class DominanceEngine:
    """
    Neural Engine: يستخدم LLM لتوليد محتوى عالي الجودة بهيكلية صارمة.
    """

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def process(request: DominanceRequest) -> AlphaPack:
        """
        يرسل الطلب للذكاء الاصطناعي ويعيد بناء النتيجة كـ AlphaPack object
        """
        
        # 1. تجهيز البرومبت
        user_prompt = generate_user_prompt(
            topic=request.topic_or_keyword,
            tone=request.tone.value,
            niche=request.dna.niche,
            audience=request.dna.target_audience
        )

        # 2. استدعاء OpenAI (مع فرض وضع JSON)
        response = client.chat.completions.create(
            model="gpt-4o-mini", # أو gpt-3.5-turbo-0125 للكفاءة والتوفير
            messages=[
                {"role": "system", "content": DOMINATOR_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7, # توازن بين الإبداع والالتزام
        )

        # 3. استخراج البيانات ومعالجتها
        raw_content = response.choices[0].message.content
        
        try:
            data = json.loads(raw_content)
            
            # 4. تحويل الـ JSON الخام إلى Pydantic Model (تحقق من الصحة تلقائياً)
            # نستخدم **data لفك تفكيك القاموس ومطابقته مع الحقول
            # ملاحظة: الذكاء الاصطناعي قد يغير أسماء الحقول قليلاً، 
            # لذا سنقوم بـ Mapping يدوي لضمان الصلابة إذا لزم الأمر، 
            # لكن Pydantic ذكي بما يكفي إذا كان البرومبت دقيقاً.
            
            # هنا سنقوم ببناء الكائن يدوياً لضمان تطابق الأسماء
            # (هذه خطوة أمان إضافية ضد هلوسة الـ AI في أسماء الحقول)
            
            return AlphaPack(
                title=f"AI Protocol: {request.topic_or_keyword}",
                dominance_score={
                    "score": data.get("dominance_score", {}).get("score", 85),
                    "why": data.get("dominance_score", {}).get("why", ["High viral potential detected."]),
                    "minimum_fix": data.get("dominance_score", {}).get("minimum_fix", "Enhance audio quality.")
                },
                hooks=[
                    {"type": h.get("type", "Generic"), "text": h.get("text", "..."), "visual_cue": h.get("visual_cue", "...")} 
                    for h in data.get("hooks", [])
                ],
                script_timeline=[
                    {
                        "time_start": s.get("time_start", "00:00"),
                        "time_end": s.get("time_end", "00:05"),
                        "type": s.get("type", "Intro"),
                        "script": s.get("script", "..."),
                        "screen_text": s.get("screen_text", ""),
                        "visual_direction": s.get("visual_direction", "")
                    }
                    for s in data.get("script_timeline", [])
                ],
                hashtags=data.get("hashtags", ["#Viral"]),
                caption=data.get("caption", "Check this out."),
                viral_flex_text=data.get("viral_flex_text", "I just engineered viral content.")
            )

        except json.JSONDecodeError:
            # في أسوأ الأحوال، إذا فشل الـ AI في إرجاع JSON سليم
            raise ValueError("AI Failed to generate valid JSON structure.")
        except Exception as e:
            raise ValueError(f"Parsing Error: {str(e)}")
