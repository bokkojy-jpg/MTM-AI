import streamlit as st
import google.generativeai as genai

# المفتاح الذي قدمته
API_KEY = "AIzaSyCC69LDLdON1hSCQ1QIr7zRFvTLouCFV-s"
genai.configure(api_key=API_KEY)

st.title("اختبار الاتصال - معتصم")

# كود بسيط جداً لتجنب أي خطأ في الأقواس
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("قل مرحباً يا معتصم")
    st.success(response.text)
except Exception as e:
    st.error(f"فشل الاتصال: {e}")
