import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="MOATASEM AI", page_icon="🤖", layout="wide")

# إخفاء اسم المستخدم من القائمة العلوية وتحسين الشكل
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child { background-color: #007bff; color: white; border-radius: 10px; }
    .stTextInput > div > div > input { background-color: #161b22; color: white; border-radius: 10px; }
    footer {visibility: hidden;}
    .developer-footer {
        position: fixed;
        bottom: 10px;
        left: 10px;
        font-family: sans-serif;
        color: #555;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# ربط الذكاء الاصطناعي
API_KEY = "AIzaSyBNHHn5ss_b9hce3YwqORi-KCOIifr90lo"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# القائمة الجانبية
with st.sidebar:
    st.title("🤖 MOATASEM AI")
    st.info("ارفع ملفاتك هنا وابدأ الدردشة")
    uploaded_files = st.file_uploader("ادعم PDF أو صور", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)
    st.markdown("---")
    st.markdown('<div class="developer-footer">Developed by: MOATASEM AI</div>', unsafe_allow_html=True)

st.title("💬 غرفة الدردشة الذكية")

# استخراج النصوص
context_text = ""
images = []

if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            context_text += "".join([p.extract_text() for p in reader.pages])
        else:
            images.append(Image.open(file))
    st.success(f"تم تحميل {len(uploaded_files)} ملفات بنجاح!")

# واجهة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني عن أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # الرد المخصص عن المطور
        if any(word in prompt.lower() for word in ["من صنعك", "من طورك", "who made you"]):
            response_text = "أنا نظام ذكاء اصطناعي متطور، تم برمجتي وتطويري بواسطة **المعتصم نبيل المليكي**."
        else:
            # دمج النصوص والصور في الرد
            inputs = [f"Context: {context_text[:3000]}\n\nUser Question: {prompt}"]
            if images:
                inputs.extend(images)
            
            response = model.generate_content(inputs)
            response_text = response.text
            
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
