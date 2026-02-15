import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image

# إعدادات الواجهة الاحترافية
st.set_page_config(page_title="MOATASEM AI", page_icon="🤖", layout="centered")

# تصميم الواجهة (Dark Mode) وحذف الأسماء الكبيرة
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    footer {visibility: hidden;}
    .developer-footer {
        position: fixed;
        bottom: 10px;
        right: 10px;
        color: #555;
        font-size: 11px;
        font-family: sans-serif;
    }
    </style>
    <div class="developer-footer">Developed by: MOATASEM AI</div>
    """, unsafe_allow_html=True)

# ربط الذكاء الاصطناعي - تم تصحيح المسار هنا
API_KEY = "AIzaSyBNHHn5ss_b9hce3YwqORi-KCOIifr90lo"
genai.configure(api_key=API_KEY)
# هنا الإصلاح: أضفنا models/ قبل اسم المحرك
model = genai.GenerativeModel('models/gemini-1.5-flash')

with st.sidebar:
    st.title("🤖 MOATASEM AI")
    st.write("ارفع ملفاتك وابدأ الدردشة فوراً")
    uploaded_files = st.file_uploader("PDF أو صور", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

st.title("💬 غرفة الدردشة")

# معالجة الملفات
context_text = ""
images = []
if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            context_text += "".join([p.extract_text() for p in reader.pages])
        else:
            images.append(Image.open(file))

# نظام الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع MOATASEM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if any(word in prompt.lower() for word in ["من صنعك", "من طورك", "who made you"]):
            res = "أنا نظام ذكاء اصطناعي تم تطويري وبرمجتي بواسطة المطور **معتصم نبيل المليكي**."
        else:
            try:
                # إرسال البيانات للمحرك بشكل صحيح
                content_to_send = [f"Context: {context_text[:3000]}\nQuestion: {prompt}"]
                if images: content_to_send.extend(images)
                
                response = model.generate_content(content_to_send)
                res = response.text
            except Exception as e:
                res = "حدث خطأ في الاتصال، حاول مرة أخرى."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
