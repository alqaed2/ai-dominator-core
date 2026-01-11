import streamlit as st
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

# القاموس اللغوي
TRANSLATIONS = {
    "English": {
        "dir": "ltr", "align": "left",
        "lbl_topic": "Topic", "lbl_niche": "Niche", "lbl_audience": "Audience",
        "lbl_url": "🔗 Clone Viral Video (Optional URL)",
        "btn_exec": "🚀 EXECUTE", "btn_radar": "📡 DOMINANCE RADAR (Scan Niche)",
        "res_hooks": "Viral Hooks", "res_script": "Script",
        "res_visual": "Visual:", "res_screen": "Screen:"
    },
    "Arabic": {
        "dir": "rtl", "align": "right",
        "lbl_topic": "الموضوع", "lbl_niche": "المجال", "lbl_audience": "الجمهور",
        "lbl_url": "🔗 استنساخ فيديو ناجح (ضع الرابط)",
        "btn_exec": "🚀 تنفيذ الهيمنة", "btn_radar": "📡 رادار الهيمنة (مسح المجال)",
        "res_hooks": "الخطافات", "res_script": "السيناريو",
        "res_visual": "المشهد:", "res_screen": "على الشاشة:"
    }
}

# --- Sidebar ---
with st.sidebar:
    st.header("🌐 Language")
    lang_code = st.selectbox("Select", ["English", "Arabic"], index=1)
    t = TRANSLATIONS[lang_code]
    
    st.divider()
    # 1. خانة الرابط المطلوبة
    video_url = st.text_input(t['lbl_url'], placeholder="https://www.tiktok.com/...")
    
    st.divider()
    topic = st.text_input(t['lbl_topic'], "كيفية الثراء من الانترنت")
    niche = st.text_input(t['lbl_niche'], "Business")
    audience = st.text_input(t['lbl_audience'], "Youth")
    tone = st.selectbox("Tone", ["controversial", "educational", "storytelling"])
    platform = st.selectbox("Platform", ["tiktok", "instagram"])
    
    # 2. الأزرار (تنفيذ + رادار)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_exec = st.button(t['btn_exec'], type="primary", use_container_width=True)
    with col_btn2:
        btn_radar = st.button("📡 Radar", type="secondary", use_container_width=True)

# --- CSS ---
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

# --- منطق التشغيل الموحد ---
active_btn = None
radar_mode = False

if btn_exec: active_btn = "exec"
if btn_radar: 
    active_btn = "radar"
    radar_mode = True

if active_btn:
    status_msg = "جاري مسح الرادار وتحليل الـ DNA..." if radar_mode else "جاري المعالجة..."
    with st.status(f"⚙️ {status_msg}", expanded=True) as status:
        try:
            req = DominanceRequest(
                topic_or_keyword=topic, platform=Platform(platform), tone=ContentTone(tone),
                dna=CreatorDNA(niche=niche, target_audience=audience, key_strengths=[])
            )
            
            # استدعاء المحرك (يعود بقاموس dict وليس كائن)
            data = DominanceEngine.process(req, language=lang_code, video_url=video_url, radar_mode=radar_mode)
            
            status.update(label="✅ Done!", state="complete", expanded=False)
            
            # --- عرض النتائج (الآن نقرأ من القاموس مباشرة) ---
            
            # 1. Score
            score_data = data.get("score_data", {})
            # التعامل المرن مع اختلاف هيكل السكور
            final_score = score_data.get("score", 85)
            if isinstance(score_data, int): final_score = score_data
            
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f'<div class="big-score">{final_score}%</div>', unsafe_allow_html=True)
            with c2: 
                fix = score_data.get("fix", score_data.get("minimum_fix", "Review Content")) if isinstance(score_data, dict) else "Check Flow"
                st.info(f"💡 Fix: {fix}")

            st.divider()

            # 2. Hooks
            st.subheader(f"🪝 {t['res_hooks']}")
            hooks = data.get("hooks", [])
            if isinstance(hooks, list):
                for h in hooks:
                    if isinstance(h, dict):
                        with st.container(border=True):
                            st.markdown(f"**{h.get('type', 'Hook')}**")
                            st.code(h.get('text', '...'), language="text")
                            st.markdown(f"<span class='visual-tag'>👁️ {h.get('visual', h.get('visual_cue', '...'))}</span>", unsafe_allow_html=True)

            st.divider()

            # 3. Script
            st.subheader(f"📜 {t['res_script']}")
            script = data.get("script", [])
            full_text = ""
            
            if isinstance(script, list):
                for s in script:
                    if isinstance(s, dict):
                        start = s.get("time", s.get("time_start", "00:00"))
                        text = s.get("text", s.get("script", "..."))
                        visual = s.get("visual", s.get("visual_direction", "..."))
                        screen = s.get("screen", s.get("screen_text", ""))
                        
                        full_text += f"[{start}] {text}\n"
                        
                        st.markdown(f"""
                        <div class="script-box">
                            <div style="color: #9ca3af; font-size: 0.8em;">⏱️ {start} | {s.get('type', 'Scene')}</div>
                            <div style="font-size: 1.1em; margin: 5px 0; color: white;">{text}</div>
                            <div style="margin-top: 10px;">
                                <span class="visual-tag">🎥 {visual}</span><br>
                                <span class="screen-tag">📺 {screen}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("👇 **Copy Full Script**")
            st.code(full_text, language="text")
            
            st.divider()
            st.subheader("#️⃣ Hashtags")
            tags = data.get("hashtags", [])
            if isinstance(tags, list):
                st.code(" ".join(tags), language="text")

        except Exception as e:
            status.update(label="❌ Error", state="error")
            st.error(f"System Failure: {str(e)}")
