import streamlit as st
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

TRANSLATIONS = {
    "English": {
        "dir": "ltr", "align": "left",
        "lbl_topic": "Topic", "lbl_niche": "Niche", "lbl_audience": "Audience",
        "lbl_url": "🔥 Clone Viral Video (Optional URL)",
        "btn_exec": "🚀 EXECUTE", "res_hooks": "Viral Hooks", "res_script": "Script",
        "res_visual": "Visual:", "res_screen": "Screen Overlay:"
    },
    "Arabic": {
        "dir": "rtl", "align": "right",
        "lbl_topic": "الموضوع", "lbl_niche": "المجال", "lbl_audience": "الجمهور",
        "lbl_url": "🔥 استنساخ فيديو ناجح (رابط اختياري)",
        "btn_exec": "🚀 تنفيذ الهيمنة", "res_hooks": "الخطافات", "res_script": "السيناريو",
        "res_visual": "المشهد:", "res_screen": "على الشاشة:"
    }
}

with st.sidebar:
    st.header("🌐 Language")
    lang_code = st.selectbox("Select", ["English", "Arabic"], index=1)
    t = TRANSLATIONS[lang_code]
    
    st.divider()
    topic = st.text_input(t['lbl_topic'], "التسويق بالعمولة للمبتدئين")
    
    # حقل الرابط الجديد
    video_url = st.text_input(t['lbl_url'], placeholder="https://www.tiktok.com/@user/video/...")
    
    niche = st.text_input(t['lbl_niche'], "Marketing")
    audience = st.text_input(t['lbl_audience'], "Beginners")
    tone = st.selectbox("Tone", ["controversial", "educational", "storytelling"])
    platform = st.selectbox("Platform", ["tiktok", "instagram"])
    btn = st.button(t['btn_exec'], type="primary", use_container_width=True)

# CSS (نفس السابق)
st.markdown(f"""
<style>
    .stApp {{ background-color: #0e1117; }}
    .element-container, .stMarkdown, .stText {{ direction: {t['dir']}; text-align: {t['align']}; }}
    .big-score {{ direction: ltr; font-size: 80px; color: #00ff41; text-align: center; font-weight: bold; }}
    .script-box {{ background-color: #1f2937; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #374151; }}
    .visual-tag {{ color: #fbbf24; font-size: 0.9em; }}
    .screen-tag {{ color: #ef4444; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 8])
with col1: st.write("🦅")
with col2: st.title("AI DOMINATOR // GLOBAL")

if btn:
    status_msg = "جاري سحب الـ DNA وتحليله..." if video_url else "جاري المعالجة..."
    with st.status(f"⚙️ {status_msg}", expanded=True) as status:
        try:
            req = DominanceRequest(
                topic_or_keyword=topic, platform=Platform(platform), tone=ContentTone(tone),
                dna=CreatorDNA(niche=niche, target_audience=audience, key_strengths=[])
            )
            
            # تمرير الرابط للمحرك
            data = DominanceEngine.process(req, language=lang_code, video_url=video_url)
            
            status.update(label="✅ Done!", state="complete", expanded=False)
            
            # (نفس كود عرض النتائج السابق تماماً)
            # ...
            # ...
            # (أعد نسخ جزء عرض النتائج Score, Hooks, Script من الكود السابق هنا)
            
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f'<div class="big-score">{data.dominance_score.score}%</div>', unsafe_allow_html=True)
            with c2: 
                fix_text = f"Fix: {data.dominance_score.minimum_fix}"
                st.info(fix_text)
                st.code(fix_text, language="text")

            st.divider()
            st.subheader(f"🪝 {t['res_hooks']}")
            for h in data.hooks:
                with st.container(border=True):
                    st.markdown(f"**{h.type}**")
                    st.code(h.text, language="text")
                    st.markdown(f"<span class='visual-tag'>👁️ {h.visual_cue}</span>", unsafe_allow_html=True)

            st.divider()
            st.subheader(f"📜 {t['res_script']}")
            full_text = ""
            for s in data.script_timeline:
                full_text += f"[{s.time_start}] {s.script}\n"
                st.markdown(f"""
                <div class="script-box">
                    <div style="color: #9ca3af; font-size: 0.8em;">⏱️ {s.time_start} | {s.type}</div>
                    <div style="font-size: 1.1em; margin: 5px 0; color: white;">{s.script}</div>
                    <div style="margin-top: 10px;">
                        <span class="visual-tag">🎥 {s.visual_direction}</span><br>
                        <span class="screen-tag">📺 {s.screen_text if s.screen_text else "---"}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("👇 **Copy Full Script**")
            st.code(full_text, language="text")
            
            st.divider()
            st.subheader("#️⃣ Hashtags")
            st.code(" ".join(data.hashtags), language="text")

        except Exception as e:
            status.update(label="❌ Error", state="error")
            st.error(str(e))
