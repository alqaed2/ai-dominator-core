import streamlit as st
import requests
import json

# --- إعدادات الاتصال ---
# ⚠️ استبدل هذا الرابط برابط سيرفرك الحقيقي على Render
# مثال: https://ai-dominator-core.onrender.com
API_URL = "https://ai-dominator-core.onrender.com" 

st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

# --- التصميم البصري ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .big-score { font-size: 80px; font-weight: bold; color: #00ff41; text-align: center; }
    .metric-card { background-color: #1f2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; }
    h1, h2, h3 { color: #00ff41 !important; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# --- الهيدر ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
with col2:
    st.title("AI DOMINATOR // V1")
    st.caption("Supreme Controlled Innovation & Execution System")

st.divider()

# --- المدخلات ---
with st.sidebar:
    st.header("🎯 Target Parameters")
    
    topic = st.text_input("Topic / Keyword", "How AI replaces agencies")
    niche = st.text_input("Niche", "Digital Marketing")
    audience = st.text_input("Audience", "Agency Owners")
    
    tone = st.selectbox("Tone Strategy", 
        ["controversial", "educational", "storytelling", "direct_sales"])
    
    platform = st.selectbox("Platform", ["tiktok", "instagram_reels", "youtube_shorts"])
    
    generate_btn = st.button("🚀 INITIATE DOMINANCE", type="primary", use_container_width=True)

# --- المنطق والتشغيل ---
if generate_btn:
    with st.status("⚙️ Neural Engine Processing...", expanded=True) as status:
        st.write("Connecting to Supreme Backend...")
        
        payload = {
            "topic_or_keyword": topic,
            "platform": platform,
            "tone": tone,
            "dna": {
                "niche": niche,
                "target_audience": audience,
                "key_strengths": ["Innovation"]
            }
        }
        
        try:
            # الاتصال بالسيرفر
            response = requests.post(f"{API_URL}/api/v1/generate", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                status.update(label="✅ Dominance Pack Generated!", state="complete", expanded=False)
                
                # --- عرض النتائج ---
                
                # 1. Score Section
                st.subheader("⚡ Dominance Probability")
                score_col, why_col = st.columns([1, 2])
                
                with score_col:
                    score_val = data['dominance_score']['score']
                    st.markdown(f'<div class="big-score">{score_val}%</div>', unsafe_allow_html=True)
                
                with why_col:
                    st.info(f"💡 **Minimum Fix:** {data['dominance_score']['minimum_fix']}")
                    for reason in data['dominance_score']['why']:
                        st.caption(f"• {reason}")

                st.divider()

                # 2. Hooks Section
                st.subheader("🪝 Viral Hooks (A/B/C)")
                cols = st.columns(3)
                for idx, hook in enumerate(data['hooks']):
                    with cols[idx]:
                        with st.container(border=True):
                            st.markdown(f"**Type:** `{hook['type']}`")
                            st.write(f"🗣️ *\"{hook['text']}\"*")
                            st.warning(f"👁️ {hook['visual_cue']}")

                st.divider()

                # 3. Script Timeline
                st.subheader("📜 Execution Script")
                for section in data['script_timeline']:
                    with st.expander(f"{section['time_start']} - {section['type']}", expanded=True):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.write(f"**Script:** {section['script']}")
                        with c2:
                            st.error(f"**Screen:** {section['screen_text']}")
                            st.caption(f"**Visual:** {section['visual_direction']}")
                
                # 4. Viral Flex
                st.divider()
                st.success(f"📢 **Viral Flex Card Text:** {data['viral_flex_text']}")
                st.code(" ".join(data['hashtags']))

            else:
                status.update(label="❌ Execution Failed", state="error")
                st.error(f"Server Error: {response.text}")
                
        except Exception as e:
            status.update(label="❌ Connection Failed", state="error")
            st.error(f"Could not reach the Brain: {str(e)}")

else:
    st.info("👈 Enter parameters and press INITIATE to begin.")
