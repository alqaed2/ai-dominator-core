from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

# --- Enums (Constants) ---
class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM_REELS = "instagram_reels"
    YOUTUBE_SHORTS = "youtube_shorts"

class ContentTone(str, Enum):
    CONTROVERSIAL = "controversial"  # للنمو السريع
    EDUCATIONAL = "educational"      # للسلطة
    STORYTELLING = "storytelling"    # للربط العاطفي
    DIRECT_SALES = "direct_sales"    # للتحويل

# --- Inputs (Request Models) ---
class CreatorDNA(BaseModel):
    """
    جينات صانع المحتوى: تحدد أسلوبه الخاص
    """
    niche: str = Field(..., example="Digital Marketing")
    target_audience: str = Field(..., example="Agency Owners")
    key_strengths: List[str] = Field(default=[], example=["Data Driven", "No fluff"])

class DominanceRequest(BaseModel):
    """
    طلب توليد المحتوى الأساسي
    """
    topic_or_keyword: str = Field(..., example="AI Automation for Agencies")
    platform: Platform = Platform.TIKTOK
    tone: ContentTone = ContentTone.CONTROVERSIAL
    dna: CreatorDNA

# --- Outputs (Response Models) ---

class HookVariant(BaseModel):
    type: str = Field(..., example="A (Visual Shock)")
    text: str
    visual_cue: str

class DominanceScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="تنبؤ قوة الفيديو 0-100")
    why: List[str] = Field(..., description="لماذا حصل على هذه الدرجة؟")
    minimum_fix: str = Field(..., description="التعديل الواحد الحاسم لتحسين النتيجة")

class ContentSection(BaseModel):
    time_start: str
    time_end: str
    type: str  # Hook, Value, CTA
    script: str
    screen_text: str
    visual_direction: str

class AlphaPack(BaseModel):
    """
    الحزمة النهائية: المنتج الذي يتسلمه المستخدم
    """
    title: str
    dominance_score: DominanceScore
    hooks: List[HookVariant]
    script_timeline: List[ContentSection]
    hashtags: List[str]
    caption: str
    # هذا الحقل إجباري لخاصية الفيروسية (توجيهنا الأول)
    viral_flex_text: str = Field(..., description="النص الذي يظهر في بطاقة المشاركة")