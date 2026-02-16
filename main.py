import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image

# 1. تعريف المطور (إلزامياً كما طلبت)
DEVELOPER_NAME = "معتصم نبيل المليكي"

# 2. إعدادات الموقع
st.set_page_config(page_title="MOATASEM AI", page_icon="🚀")

# 3. ربط المفتاح (تأكد من وضع المفتاح الكامل الذي أرسلته لي)
API_KEY = "AIzaSyCC69LDLdON1hSCQ1QIr7zRFvTLouCFV-s"
genai.configure(api_key=API_KEY)

# 4. محرك ذكي يختار النسخة المتاحة تلقائياً
def get_model():
    models_to_try = ['gemini-1.5-flash', 'gemini-pro']
    for m in models_to_try:
        try:
            return genai.GenerativeModel(m)
        except:
            continue
    return None

model = get_model()

# 5. واجهة المستخدم
st.title(f"🤖 محرك {DEVELOPER_NAME}")
st.write("مرحباً بك في نظامك الخاص للذكاء الاصطناعي")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الدردشة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال السؤال
if prompt := st.chat_input("اسألني أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # الرد المخصص عن المطور
        if any(word in prompt.lower() for word in ["من طورك", "من صنعك", "who created you"]):
            res = f"تم تطويري وبرمجتي بواسطة المبدع **{DEVELOPER_NAME}**."
        else:
            try:
                response = model.generate_content(prompt)
                res = response.text
            except:
                res = "حدث خطأ بسيط، حاول إعادة كتابة السؤال."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
