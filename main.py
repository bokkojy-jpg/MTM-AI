import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="MOATASEM AI", page_icon="🤖", layout="centered")

# 2. تصميم الواجهة (Dark Mode) وتنسيق الخطوط
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child { background-color: #007bff; color: white; border-radius: 10px; }
    footer {visibility: hidden;}
    .developer-footer {
        position: fixed;
        bottom: 10px;
        right: 15px;
        color: #666;
        font-size: 12px;
        font-family: sans-serif;
    }
    </style>
    <div class="developer-footer">Developed by: MOATASEM AI</div>
    """, unsafe_allow_html=True)

# 3. ربط المفتاح الصحيح (الذي أرسلته لي أخيراً)
API_KEY = "AIzaSyCC69LDLdON1hSCQ1QIr7zRFvTLouCFV-s" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 4. القائمة الجانبية لرفع الملفات
with st.sidebar:
    st.title("🤖 MOATASEM AI")
    st.write("ارفع ملفاتك هنا لكي أقوم بتحليلها لك")
    uploaded_files = st.file_uploader("اختر (PDF أو صور)", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

st.title("💬 غرفة الدردشة الذكية")

# 5. معالجة البيانات المرفوعة
context_text = ""
images = []
if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf":
            try:
                reader = PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text: context_text += text
            except: st.error(f"خطأ في قراءة ملف: {file.name}")
        else:
            images.append(Image.open(file))
    if uploaded_files: st.success("🚀 تم تجهيز ملفاتك! يمكنك سؤالي عنها الآن.")

# 6. نظام الذاكرة والدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال سؤال المستخدم
if prompt := st.chat_input("اسألني عن أي شيء أو عن الملفات المرفوعة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # رد مخصص للمطور (بناءً على طلبك السابق)
        if any(word in prompt.lower() for word in ["من صنعك", "من طورك", "who made you"]):
            res = "أنا نظام ذكاء اصطناعي متطور، تم برمجتي وتطويري بواسطة المبدع **معتصم نبيل المليكي**."
        else:
            try:
                # إرسال السؤال مع السياق (النصوص والصور)
                content_to_send = []
                full_prompt = f"Context from files: {context_text[:5000]}\n\nUser Question: {prompt}"
                content_to_send.append(full_prompt)
                if images:
                    content_to_send.extend(images)
                
                response = model.generate_content(
