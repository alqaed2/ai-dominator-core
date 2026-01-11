import streamlit as st
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

TRANSLATIONS = {
    "English": {
        "dir": "ltr", "align": "left",
        "lbl_topic": "Topic", "lbl_niche": "Niche", "lbl_audience": "Audience",
        "lbl_url": "🔗 Clone Viral Video (Optional URL)",
        "btn_exec": "🚀 EXECUTE", "btn_radar": "📡 DOMINANCE RADAR",
        "res_hooks": "Viral Hooks", "res_script": "Script",
    },
    "Arabic": {
        "dir": "rtl", "align": "right",
        "lbl_topic": "الموضوع", "lbl_niche": "المجال", "lbl_audience": "الجمهور",
        "lbl_url": "🔗 استنساخ فيديو ناجح (رابط اختياري)",
        "btn_exec": "🚀 تنفيذ الهيمنة", "btn_radar": "📡 رادار الهيمنة (مسح المجال)",
        "res_hooks": "الخطافات", "res_script": "السيناريو",
    }
}

with st.sidebar:
    st.header("🌐 Language")
    lang_code = st.selectbox("Select", ["English", "Arabic"], index=1)
    t = TRANSLATIONS[lang_code]
    
    st.divider()
    video_url = st.text_input(t['lbl_url'], placeholder="https://www.tiktok.com/...")
    st.divider()
    
    topic = st.text_input(t['lbl_topic'], "التجارة الإلكترونية")
    niche = st.text_input(t['lbl_niche'], "Business")
    audience = st.text_input(t['lbl_audience'], "Youth")
    tone = st.selectbox("Tone", ["controversial", "educational", "storytelling"])
    platform = st.selectbox("Platform", ["tiktok", "instagram"])
    
    c1, c2 = st.columns(2)
    with c1: btn_exec = st.button(t['btn_exec'], type="primary", use_container_width=True)
    with c2: btn_radar = st.button(t['btn_radar'], use_container_width=True)

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

active_btn = "exec" if btn_exec else ("radar" if btn_radar else None)
radar_mode = (active_btn == "radar")

if active_btn:
    msg = "جاري مسح الرادار..." if radar_mode else "جاري المعالجة..."
    with st.status(f"⚙️ {msg}", expanded=True) as status:
        try:
            req = DominanceRequest(
                topic_or_keyword=topic, platform=Platform(platform), tone=ContentTone(tone),
                dna=CreatorDNA(niche=niche, target_audience=audience, key_strengths=[])
            )
            
            data = DominanceEngine.process(req, language=lang_code, video_url=video_url, radar_mode=radar_mode)
            status.update(label="✅ Done!", state="complete", expanded=False)
            
            # --- النتائج (باستخدام البيانات الموحدة) ---
            score_data = data["score_data"]
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f'<div class="big-score">{score_data["score"]}%</div>', unsafe_allow_html=True)
            with c2: 
                st.info(f"💡 Fix: {score_data['fix']}")
                st.caption(f"Why: {', '.join(score_data['why'])}")

            st.divider()
            st.subheader(f"🪝 {t['res_hooks']}")
            for h in data["hooks"]:
                with st.container(border=True):
                    st.markdown(f"**{h['type']}**")
                    st.code(h['text'], language="text")
                    st.markdown(f"<span class='visual-tag'>👁️ {h['visual']}</span>", unsafe_allow_html=True)

            st.divider()
            st.subheader(f"📜 {t['res_script']}")
            full_text = ""
            for s in data["script"]:
                full_text += f"[{s['time']}] {s['text']}\n"
                st.markdown(f"""
                <div class="script-box">
                    <div style="color: #9ca3af; font-size: 0.8em;">⏱️ {s['time']} | {s['type']}</div>
                    <div style="font-size: 1.1em; margin: 5px 0; color: white;">{s['text']}</div>
                    <div style="margin-top: 10px;">
                        <span class="visual-tag">🎥 {s['visual']}</span><br>
                        <span class="screen-tag">📺 {s['screen']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("👇 **Copy Full Script**")
            st.code(full_text, language="text")
            
            st.divider()
            st.subheader("#️⃣ Hashtags")
            st.code(" ".join(data["hashtags"]), language="text")

        except Exception as e:
            status.update(label="❌ Error", state="error")
            st.error(f"System Error: {str(e)}")
