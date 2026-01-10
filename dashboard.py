import streamlit as st
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

# --- إدارة اللغات ---
LANGUAGES = {
    "English": {"code": "English", "dir": "ltr", "align": "left"},
    "Arabic": {"code": "Arabic", "dir": "rtl", "align": "right"},
    "Spanish": {"code": "Spanish", "dir": "ltr", "align": "left"},
    "French": {"code": "French", "dir": "ltr", "align": "left"},
    "German": {"code": "German", "dir": "ltr", "align": "left"},
    "Chinese": {"code": "Chinese", "dir": "ltr", "align": "left"},
}

# --- الشريط الجانبي ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # زر اختيار اللغة
    selected_lang_key = st.selectbox("🌐 Interface Language", list(LANGUAGES.keys()), index=0)
    lang_config = LANGUAGES[selected_lang_key]
    
    st.divider()
    st.subheader("🎯 Mission Parameters")
    topic = st.text_input("Topic / Keyword", "How AI replaces agencies")
    niche = st.text_input("Niche", "Digital Marketing")
    audience = st.text_input("Audience", "Agency Owners")
    tone_str = st.selectbox("Tone", ["controversial", "educational", "storytelling", "direct_sales"])
    platform_str = st.selectbox("Platform", ["tiktok", "instagram_reels", "youtube_shorts"])
    
    generate_btn = st.button("🚀 EXECUTE", type="primary", use_container_width=True)

# --- CSS ديناميكي حسب اللغة ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #0e1117; color: #ffffff; }}
    .content-box {{ direction: {lang_config['dir']}; text-align: {lang_config['align']}; }}
    .big-score {{ font-size: 80px; font-weight: 800; color: #00ff41; text-align: center; }}
    /* جعل كود النسخ يبدو كصندوق نصي عادي */
    .stCodeBlock {{ direction: {lang_config['dir']} !important; }}
</style>
""", unsafe_allow_html=True)

# --- الهيدر ---
col1, col2 = st.columns([1, 6])
with col1: st.write("🦅")
with col2: 
    st.title("AI DOMINATOR // GLOBAL")
    st.caption(f"Language Mode: {selected_lang_key}")

st.divider()

if generate_btn:
    with st.status("⚙️ Neural Core Processing...", expanded=True) as status:
        try:
            # تجهيز الطلب
            dna_obj = CreatorDNA(niche=niche, target_audience=audience, key_strengths=[])
            request_obj = DominanceRequest(
                topic_or_keyword=topic,
                platform=Platform(platform_str),
                tone=ContentTone(tone_str),
                dna=dna_obj
            )
            
            # الاستدعاء مع اللغة المختارة
            data = DominanceEngine.process(request_obj, language=lang_config['code'])
            status.update(label="✅ Success!", state="complete", expanded=False)
            
            # --- النتائج ---
            
            # 1. Score
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f'<div class="big-score">{data.dominance_score.score}%</div>', unsafe_allow_html=True)
            with c2: 
                st.info(f"💡 Fix: {data.dominance_score.minimum_fix}")
                # زر نسخ التحليل
                fix_text = f"Fix: {data.dominance_score.minimum_fix}\nWhy: {', '.join(data.dominance_score.why)}"
                st.code(fix_text, language="text")

            st.divider()

            # 2. Hooks (مع زر نسخ)
            st.subheader("🪝 Hooks")
            if data.hooks:
                for hook in data.hooks:
                    with st.container(border=True):
                        st.markdown(f"**{hook.type}**")
                        # نستخدم st.code للنسخ السهل
                        st.code(hook.text, language="text") 
                        st.caption(f"👁️ Visual: {hook.visual_cue}")

            st.divider()

            # 3. Script (مع زر نسخ)
            st.subheader("📜 Script")
            full_script_text = ""
            for section in data.script_timeline:
                full_script_text += f"[{section.time_start}] ({section.type}): {section.script}\n"
                
                with st.expander(f"{section.time_start} - {section.type}", expanded=True):
                    c_a, c_b = st.columns([3, 1])
                    with c_a:
                        st.markdown(f"**Script:** {section.script}")
                        st.caption(f"**Visual:** {section.visual_direction}")
                    with c_b:
                        st.error(f"📺 {section.screen_text}")
            
            # زر لنسخ السكريبت كاملاً
            st.markdown("👇 **Copy Full Script**")
            st.code(full_script_text, language="text")

            st.divider()
            
            # 4. Hashtags & Caption
            st.subheader("#️⃣ Hashtags & Caption")
            tags_text = " ".join(data.hashtags)
            st.code(tags_text, language="text")
            st.code(data.caption, language="text")

        except Exception as e:
            st.error(f"Error: {str(e)}")
