import streamlit as st
import asyncio
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

# --- إعداد الصفحة ---
st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

# --- التصميم البصري ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .big-score { font-size: 80px; font-weight: bold; color: #00ff41; text-align: center; }
    .metric-card { background-color: #1f2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; }
    h1, h2, h3 { color: #00ff41 !important; font-family: 'Courier New', monospace; }
    .stButton>button { color: #000000; background-color: #00ff41; font-weight: bold; border: none; }
</style>
""", unsafe_allow_html=True)

# --- الهيدر ---
col1, col2 = st.columns([1, 6])
with col1:
    st.write("🦅") 
with col2:
    st.title("AI DOMINATOR // CORE")
    st.caption("Integrated System Architecture | v1.0")

st.divider()

# --- المدخلات ---
with st.sidebar:
    st.header("🎯 Mission Parameters")
    
    topic = st.text_input("Topic / Keyword", "How AI replaces agencies")
    niche = st.text_input("Niche", "Digital Marketing")
    audience = st.text_input("Audience", "Agency Owners")
    
    tone_str = st.selectbox("Tone Strategy", 
        ["controversial", "educational", "storytelling", "direct_sales"])
    
    platform_str = st.selectbox("Platform", ["tiktok", "instagram_reels", "youtube_shorts"])
    
    generate_btn = st.button("🚀 EXECUTE", type="primary", use_container_width=True)

# --- المنطق والتشغيل ---
if generate_btn:
    with st.status("⚙️ Processing via Internal Neural Core...", expanded=True) as status:
        
        try:
            # 1. تجهيز البيانات ككائنات النظام (Schemas)
            dna_obj = CreatorDNA(
                niche=niche,
                target_audience=audience,
                key_strengths=["Innovation"]
            )
            
            request_obj = DominanceRequest(
                topic_or_keyword=topic,
                platform=Platform(platform_str), # تحويل النص إلى Enum
                tone=ContentTone(tone_str),      # تحويل النص إلى Enum
                dna=dna_obj
            )
            
            # 2. الاستدعاء المباشر للمحرك (بدون إنترنت/requests)
            # بما أن engine.py أصبح الآن جزءاً من التطبيق المباشر
            status.update(label="🧠 Accessing Gemini Brain...", state="running")
            
            # استدعاء الدالة مباشرة
            data = DominanceEngine.process(request_obj)
            
            status.update(label="✅ Dominance Pack Secured!", state="complete", expanded=False)
            
            # --- عرض النتائج ---
            st.subheader("⚡ Dominance Probability")
            score_col, why_col = st.columns([1, 2])
            
            # التعامل مع الكائن (Pydantic Model) مباشرة وليس JSON
            with score_col:
                st.markdown(f'<div class="big-score">{data.dominance_score.score}%</div>', unsafe_allow_html=True)
            
            with why_col:
                st.info(f"💡 **Optimization:** {data.dominance_score.minimum_fix}")
                for reason in data.dominance_score.why:
                    st.caption(f"• {reason}")

            st.divider()

            st.subheader("🪝 Viral Hooks")
            if data.hooks:
                cols = st.columns(len(data.hooks))
                for idx, hook in enumerate(data.hooks):
                    with cols[idx]:
                        with st.container(border=True):
                            st.markdown(f"**{hook.type}**")
                            st.write(f"_{hook.text}_")
                            st.warning(f"👁️ {hook.visual_cue}")

            st.divider()

            st.subheader("📜 Timeline Script")
            for section in data.script_timeline:
                with st.expander(f"{section.time_start} - {section.type}", expanded=True):
                    st.write(f"**Script:** {section.script}")
                    st.caption(f"**Visual:** {section.visual_direction}")
                    st.error(f"**Screen:** {section.screen_text}")
            
            st.divider()
            st.code(" ".join(data.hashtags))

        except Exception as e:
            status.update(label="❌ System Error", state="error")
            st.error(f"Critical Failure: {str(e)}")
