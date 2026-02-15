import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# إعدادات الصفحة
st.set_page_config(page_title="Insight AI", page_icon="💎")

# المطور
DEVELOPER_NAME = "معتصم نبيل المليكي"

# ربط الذكاء الاصطناعي
API_KEY = "AIzaSyBNHHn5ss_b9hce3YwqORi-KCOIifr90lo"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("💎 Insight AI")
st.markdown(f"**بإشراف المطور: {DEVELOPER_NAME}**")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = "".join([p.extract_text() for p in reader.pages])
    user_q = st.text_input("اسأل Insight:")
    
    if user_q:
        if any(word in user_q.lower() for word in ["من صنعك", "من طورك", "who made you"]):
            st.info(f"أنا Insight، وقد تم تطويري وبرمجتي بواسطة المطور المبدع: **{DEVELOPER_NAME}**.")
        else:
            response = model.generate_content(f"Context: {text[:5000]}\nQuestion: {user_q}")
            st.write(response.text)
