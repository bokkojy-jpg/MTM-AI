import streamlit as st
import google.generativeai as genai

# إعداد المفتاح
API_KEY = "AIzaSyCC69LDLdON1hSCQ1QIr7zRFvTLouCFV-s"
genai.configure(api_key=API_KEY)

st.title("🤖 MOATASEM AI")

# محاولة الاتصال بصيغة بسيطة جداً
try:
    # هنا جربنا استدعاء الموديل بدون كلمة models/ وبدون إضافات
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if "من صنعك" in prompt or "من طورك" in prompt:
                res = "تم تطويري بواسطة المبدع معتصم نبيل المليكي."
            else:
                # محاولة توليد نص
                response = model.generate_content(prompt)
                res = response.text
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")
    st.info("تأكد من أنك ضغطت على زر 'Copy Key' الحقيقي من Google AI Studio")
