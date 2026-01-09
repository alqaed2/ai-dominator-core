import random
from app.schemas import DominanceRequest, AlphaPack, DominanceScore, HookVariant, ContentSection

class DominanceEngine:
    """
    The Brain: المسؤول عن تحويل المدخلات إلى مخرجات ذات هيمنة عالية.
    يعمل حالياً بنظام القواعد المنطقية المتقدمة (Deterministic Intelligence).
    """

    @staticmethod
    def calculate_score(request: DominanceRequest) -> DominanceScore:
        # خوارزمية مبدئية لحساب الهيمنة بناءً على قوة النيش والنبرة
        base_score = 75
        reasons = []
        
        if request.tone == "controversial":
            base_score += 10
            reasons.append("High engagement potential due to controversial tone.")
        elif request.tone == "educational":
            base_score += 5
            reasons.append("Steady authority building, but lower viral velocity.")
            
        fix = "Increase pacing in the first 3 seconds." if base_score < 85 else "Ensure audio quality is crisp."

        return DominanceScore(
            score=min(base_score, 99),
            why=reasons,
            minimum_fix=fix
        )

    @staticmethod
    def generate_hooks(topic: str) -> list[HookVariant]:
        return [
            HookVariant(
                type="A (Pattern Interrupt)",
                text=f"Stop doing {topic} like this, you are losing money!",
                visual_cue="Red filter flash + Sirens sound"
            ),
            HookVariant(
                type="B (Curiosity Gap)",
                text=f"The secret about {topic} no one tells you...",
                visual_cue="Whisper gesture close to camera"
            ),
            HookVariant(
                type="C (Direct Benefit)",
                text=f"Here is how to master {topic} in 30 seconds.",
                visual_cue="Show result proof on screen green screen"
            )
        ]

    @staticmethod
    def construct_timeline(request: DominanceRequest) -> list[ContentSection]:
        # هيكل الفيديو المثالي (The Golden Structure)
        return [
            ContentSection(
                time_start="00:00", time_end="00:03", 
                type="HOOK", 
                script="(Select one of the hooks above)",
                screen_text="STOP SCROLLING 🛑", 
                visual_direction="Face close to camera"
            ),
            ContentSection(
                time_start="00:03", time_end="00:15", 
                type="VALUE / REFRAME", 
                script=f"Most people think {request.topic_or_keyword} is hard, but actually...",
                screen_text="The Truth 💡", 
                visual_direction="Fast cuts, showing examples"
            ),
            ContentSection(
                time_start="00:15", time_end="00:25", 
                type="THE SOLUTION", 
                script="You need to use the AI Dominator framework.",
                screen_text="Step 1.. Step 2..", 
                visual_direction="Screen recording or list"
            ),
            ContentSection(
                time_start="00:25", time_end="00:30", 
                type="CTA", 
                script="Check the link in bio for the full blueprint.",
                screen_text="LINK IN BIO 🔗", 
                visual_direction="Pointing up/down"
            )
        ]

    @staticmethod
    def process(request: DominanceRequest) -> AlphaPack:
        # 1. تحليل الطلب
        # 2. توليد النتيجة
        score = DominanceEngine.calculate_score(request)
        hooks = DominanceEngine.generate_hooks(request.topic_or_keyword)
        timeline = DominanceEngine.construct_timeline(request)
        
        # 3. بناء الحزمة النهائية
        return AlphaPack(
            title=f"Dominator Protocol: {request.topic_or_keyword}",
            dominance_score=score,
            hooks=hooks,
            script_timeline=timeline,
            hashtags=["#AI", f"#{request.topic_or_keyword.replace(' ', '')}", "#Growth"],
            caption=f"This changes everything about {request.topic_or_keyword}. 🔥 👇",
            viral_flex_text=f"My AI Strategy Score: {score.score}/100. Can you beat that?"
        )