import streamlit as st
from app.schemas import DominanceRequest, CreatorDNA, Platform, ContentTone
from app.engine import DominanceEngine

st.set_page_config(page_title="AI DOMINATOR", page_icon="🦅", layout="wide")

# --- قاموس الترجمة (The Translation Matrix) ---
TRANSLATIONS = {
    "English": {
        "dir": "ltr", "align": "left",
        "header_title": "MISSION PARAMETERS",
        "lbl_topic": "Topic / Keyword",
        "lbl_niche": "Niche",
        "lbl_audience": "Target Audience",
        "lbl_tone": "Tone Strategy",
        "lbl_platform": "Platform",
        "btn_exec": "🚀 EXECUTE DOMINANCE",
        "res_score": "Dominance Probability",
        "res_hooks": "Viral Hooks",
        "res_script": "Execution Script",
        "res_copy": "Copy",
        "err_fail": "System Failure"
    },
    "Arabic": {
        "dir": "rtl", "align": "right",
        "header_title": "إعدادات المهمة",
        "lbl_topic": "الموضوع / الكلمة المفتاحية",
        "lbl_niche": "المجال / النيش",
        "lbl_audience": "الجمهور المستهدف",
        "lbl_tone": "نبرة المحتوى",
        "lbl_platform": "المنصة",
        "btn_exec": "🚀 تنفيذ الهيمنة",
        "res_score": "احتمالية الانتشار",
        "res_hooks": "الخطافات الفيروسية (Hooks)",
        "res_script": "السيناريو التنفيذي",
        "res_copy": "نسخ",
        "err_fail": "فشل النظام"
    }
}

# --- إعدادات اللغة ---
with st.sidebar:
    st.header("🌐 Language / اللغة")
    selected_lang_code = st.selectbox("Select Interface Language", ["English", "Arabic"], index=1) # الافتراضي: العربية
    
    # تحميل قاموس اللغة المختارة
    t = TRANSLATIONS[selected_lang_code]

    st.divider()
    st.header(f"🎯 {t['header_title']}")
    
    # استخدام القاموس للعناوين
    topic = st.text_input(t['lbl_topic'], "كيف يغير الذكاء الاصطناعي العالم")
    niche = st.text_input(t['lbl_niche'], "التسويق الرقمي")
    audience = st.text_input(t['lbl_audience'], "أصحاب الشركات")
    
    tone_str = st.selectbox(t['lbl_tone'], ["controversial", "educational", "storytelling", "direct_sales"])
    platform_str = st.selectbox(t['lbl_platform'], ["tiktok", "instagram_reels", "youtube_shorts"])
    
    generate_btn = st.button(t['btn_exec'], type="primary", use_container_width=True)

# --- CSS لتعديل الاتجاه (RTL/LTR) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #0e1117; color: #ffffff; }}
    /* تطبيق الاتجاه على النصوص */
    .element-container, .stMarkdown, .stText, .stCodeBlock {{ direction: {t['dir']}; text-align: {t['align']}; }}
    /* استثناء العناوين الكبيرة */
    .big-score {{ direction: ltr; font-size: 80px; font-weight: 800; color: #00ff41; text-align: center; }}
    /* تحسين القوائم */
    div[data-baseweb="select"] {{ direction: {t['dir']}; }}
</style>
""", unsafe_allow_html=True)

# --- الهيدر الرئيسي ---
col1, col2 = st.columns([1, 6])
with col1: st.write("🦅")
with col2: 
    st.title("AI DOMINATOR // GLOBAL")
    st.caption(f"System Mode: {selected_lang_code}")

st.divider()

if generate_btn:
    # حالة التشغيل
    loading_text = "جاري المعالجة..." if selected_lang_code == "Arabic" else "Processing..."
    with st.status(f"⚙️ {loading_text}", expanded=True) as status:
        try:
            # تجهيز الطلب
            dna_obj = CreatorDNA(niche=niche, target_audience=audience, key_strengths=[])
            request_obj = DominanceRequest(
                topic_or_keyword=topic,
                platform=Platform(platform_str),
                tone=ContentTone(tone_str),
                dna=dna_obj
            )
            
            # استدعاء المحرك مع اللغة
            data = DominanceEngine.process(request_obj, language=selected_lang_code)
            
            success_msg = "تمت العملية!" if selected_lang_code == "Arabic" else "Dominance Secured!"
            status.update(label=f"✅ {success_msg}", state="complete", expanded=False)
            
            # --- عرض النتائج ---
            
            # 1. Score
            st.subheader(f"⚡ {t['res_score']}")
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f'<div class="big-score">{data.dominance_score.score}%</div>', unsafe_allow_html=True)
            with c2: 
                fix_label = "التحسين:" if selected_lang_code == "Arabic" else "Fix:"
                st.info(f"💡 **{fix_label}** {data.dominance_score.minimum_fix}")
                st.code(f"{fix_label} {data.dominance_score.minimum_fix}", language="text")

            st.divider()

            # 2. Hooks
            st.subheader(f"🪝 {t['res_hooks']}")
            if data.hooks:
                for hook in data.hooks:
                    with st.container(border=True):
                        st.markdown(f"**{hook.type}**")
                        st.code(hook.text, language="text") # زر نسخ للنص
                        visual_label = "👁️ المشهد:" if selected_lang_code == "Arabic" else "👁️ Visual:"
                        st.caption(f"{visual_label} {hook.visual_cue}")

            st.divider()

            # 3. Script
            st.subheader(f"📜 {t['res_script']}")
            full_script_text = ""
            for section in data.script_timeline:
                # تجميع النص للنسخ الكامل
                full_script_text += f"[{section.time_start}] {section.script}\n"
                
                with st.expander(f"{section.time_start} | {section.type}", expanded=True):
                    st.markdown(f"**🎙️:** {section.script}")
                    st.caption(f"**🎥:** {section.visual_direction}")
                    st.error(f"**📺:** {section.screen_text}")
            
            st.markdown("👇 **Full Script / النص الكامل**")
            st.code(full_script_text, language="text")

            st.divider()
            
            # 4. Hashtags & Caption
            st.subheader("#️⃣ Hashtags")
            tags_text = " ".join(data.hashtags)
            st.code(tags_text, language="text")
            st.code(data.caption, language="text")

        except Exception as e:
            status.update(label="❌ Error", state="error")
            st.error(f"{t['err_fail']}: {str(e)}")
