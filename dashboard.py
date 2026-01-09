import streamlit as st
import asyncio
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

# --- إعداد الصفحة ---
st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

# --- التصميم البصري + دعم العربية (RTL Magic) ---
st.markdown("""
<style>
    /* الخلفية والألوان */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* فرض الاتجاه العربي للنصوص */
    .rtl-text { direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; }
    
    /* تنسيق النتائج */
    .big-score { font-size: 90px; font-weight: 800; color: #00ff41; text-align: center; text-shadow: 0 0 10px rgba(0,255,65,0.5); }
    .metric-card { background-color: #1f2937; padding: 20px; border-radius: 12px; border: 1px solid #374151; margin-bottom: 10px; }
    
    /* العناوين */
    h1, h2, h3 { color: #00ff41 !important; font-family: 'Courier New', monospace; }
    
    /* تحسين الأزرار */
    .stButton>button { color: #000; background-color: #00ff41; font-weight: bold; border-radius: 8px; border: none; height: 50px; font-size: 18px; }
    .stButton>button:hover { background-color: #fff; color: #00ff41; box-shadow: 0 0 15px #00ff41; }
    
    /* تخصيص حاويات النتائج */
    div[data-testid="stExpander"] { border: 1px solid #374151; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- الهيدر ---
col1, col2 = st.columns([1, 8])
with col1:
    st.header("🦅")
with col2:
    st.title("AI DOMINATOR // CORE")
    st.caption("Supreme Intelligence System | v1.1 RTL Updated")

st.divider()

# --- المدخلات (Sidebar) ---
with st.sidebar:
    st.header("🎯 معايير المهمة")
    
    topic = st.text_input("الموضوع / الكلمة المفتاحية", "التجارة الإلكترونية والذكاء الاصطناعي")
    niche = st.text_input("التخصص الوظيفي", "Digital Marketing")
    audience = st.text_input("الجمهور", "Agency Owners")
    
    tone_str = st.selectbox("استراتيجية النبرة", 
        ["controversial", "educational", "storytelling", "direct_sales"])
    
    platform_str = st.selectbox("المنصة", ["tiktok", "instagram_reels", "youtube_shorts"])
    
    st.markdown("---")
    generate_btn = st.button("🚀 تنفيذ الهيمنة", type="primary", use_container_width=True)

# --- المنطق والتشغيل ---
if generate_btn:
    with st.status("⚙️ جاري معالجة البيانات عبر النواة العصبية...", expanded=True) as status:
        
        try:
            # 1. تجهيز البيانات
            dna_obj = CreatorDNA(
                niche=niche,
                target_audience=audience,
                key_strengths=["Innovation"]
            )
            
            request_obj = DominanceRequest(
                topic_or_keyword=topic,
                platform=Platform(platform_str),
                tone=ContentTone(tone_str),
                dna=dna_obj
            )
            
            status.update(label="🧠 الاتصال بدماغ Gemini...", state="running")
            
            # 2. الاستدعاء المباشر
            data = DominanceEngine.process(request_obj)
            
            status.update(label="✅ تمت المهمة بنجاح!", state="complete", expanded=False)
            
            # --- عرض النتائج (بتنسيق عربي محسن) ---
            
            # قسم السكور
            st.markdown("<h3 style='text-align: right; direction: rtl;'>⚡ احتمالية الهيمنة (Dominance Score)</h3>", unsafe_allow_html=True)
            
            score_col, why_col = st.columns([1, 2])
            
            with score_col:
                st.markdown(f'<div class="big-score">{data.dominance_score.score}%</div>', unsafe_allow_html=True)
            
            with why_col:
                # حاوية مخصصة للنص العربي
                st.markdown(f"""
                <div class="metric-card rtl-text">
                    <p style="color: #00ff41; font-weight: bold;">💡 التحسين المطلوب:</p>
                    <p>{data.dominance_score.minimum_fix}</p>
                    <hr style="border-color: #4b5563;">
                    <p style="color: #9ca3af; font-size: 0.9em;">الأسباب:</p>
                    {''.join([f'<p>• {r}</p>' for r in data.dominance_score.why])}
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # قسم الخطافات (Hooks)
            st.markdown("<h3 style='text-align: right; direction: rtl;'>🪝 الخطافات الفيروسية (Hooks)</h3>", unsafe_allow_html=True)
            
            if data.hooks:
                # عرضنا الخطافات تحت بعضها بدلاً من الأعمدة لسهولة القراءة في العربية
                for hook in data.hooks:
                    st.markdown(f"""
                    <div class="metric-card rtl-text">
                        <span style="background-color: #00ff41; color: black; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold;">{hook.type}</span>
                        <h4 style="margin-top: 10px; color: white;">🗣️ "{hook.text}"</h4>
                        <p style="color: #fbbf24; font-size: 0.9em; margin-top: 5px;">👁️ المشهد البصري: {hook.visual_cue}</p>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()

            # قسم السيناريو
            st.markdown("<h3 style='text-align: right; direction: rtl;'>📜 السيناريو التنفيذي</h3>", unsafe_allow_html=True)
            for section in data.script_timeline:
                with st.expander(f"{section.time_start} | {section.type}", expanded=True):
                    # نستخدم Markdown HTML داخل الاكسباندر لفرض الـ RTL
                    st.markdown(f"""
                    <div class="rtl-text">
                        <p><strong>🎙️ السكريبت:</strong> <br><span style="color: #e5e7eb; font-size: 1.1em;">{section.script}</span></p>
                        <p style="color: #fbbf24;"><strong>👁️ الإخراج البصري:</strong> {section.visual_direction}</p>
                        <p style="color: #ef4444; border: 1px dashed #ef4444; padding: 5px; border-radius: 5px; display: inline-block;">📺 الشاشة: {section.screen_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.divider()
            st.success(f"📢 **Viral Flex:** {data.viral_flex_text}")
            st.code(" ".join(data.hashtags))

        except Exception as e:
            status.update(label="❌ فشل النظام", state="error")
            st.error(f"حدث خطأ: {str(e)}")
