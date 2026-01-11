# SYSTEM PROMPTS FOR AI DOMINATOR

DOMINATOR_SYSTEM_PROMPT = """
You are the AI DOMINATOR. Your goal is to engineer Viral TikTok Content.

CRITICAL RULES:
1. LANGUAGE: Output VALUES in the requested language.
2. KEYS: Keep JSON keys in ENGLISH and LOWERCASE.
3. VISUALS: Detailed cinematic descriptions.

JSON SCHEMA (Strictly Follow):
{
  "score_data": {"score": 88, "why": ["Reason"], "fix": "Fix explanation"},
  "hooks": [{"type": "Type", "text": "Text", "visual": "Visual"}],
  "script": [{"time": "00:00", "type": "Scene", "text": "Script", "screen": "Overlay", "visual": "Action"}],
  "hashtags": ["#tag"],
  "caption": "Caption",
  "flex": "Flex Text"
}
"""

def generate_user_prompt(topic: str, tone: str, niche: str, audience: str, language: str, reference_dna: str = None) -> str:
    
    # إذا كان هناك DNA مستخرج من فيديو خارجي
    dna_instruction = ""
    if reference_dna:
        dna_instruction = f"""
        🚨 CLONING MODE ACTIVATED 🚨
        I have analyzed a viral video. You must MIMIC its structure exactly but apply it to the new topic.
        
        VIRAL DNA SOURCE:
        {reference_dna}
        
        INSTRUCTION:
        - Use the same hook structure as the source.
        - Use the same pacing and emotional triggers.
        - Adapt it to the topic: {topic}.
        """
    else:
        dna_instruction = "Analyze viral potential and generate original structure."

    return f"""
    TASK: Generate Viral Content.
    TARGET LANGUAGE: {language}
    
    CONTEXT:
    Topic: {topic} | Niche: {niche} | Tone: {tone}
    
    {dna_instruction}
    
    RETURN JSON ONLY.
    """

# برومبت خاص لاستخراج DNA من النص المفرغ
def generate_dna_analysis_prompt(transcript: str) -> str:
    return f"""
    TASK: Reverse Engineer this TikTok Transcript.
    Extract the "Viral DNA" (The underlying structure that made it successful).
    
    TRANSCRIPT:
    "{transcript}"
    
    OUTPUT FORMAT (Text Summary):
    1. Hook Type used.
    2. Pacing style (fast/slow).
    3. Emotional Arc.
    4. Call to Action structure.
    
    Keep it concise. This will be fed into another AI to generate a new video.
    """
