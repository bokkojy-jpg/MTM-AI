import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image

# إعدادات الواجهة الاحترافية (MOATASEM AI)
st.set_page_config(page_title="MOATASEM AI", page_icon="🤖", layout="centered")

# تصميم الواجهة وحذف الأسماء الكبيرة
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    footer {visibility: hidden;}
    .developer-footer {
        position: fixed;
        bottom: 10px;
        right: 15px;
        color: #666;
        font-size: 12px;
        font-family: sans-serif;
        z-index: 100;
    }
    </style>
    <div class="developer-footer">Developed by: MOATASEM AI</div>
    """, unsafe_allow_html=True)

# ربط الذكاء الاصطناعي - يرجى التأكد من صلاحية المفتاح
# ملاحظة: إذا استمر الخطأ، ستحتاج لإنشاء مفتاح جديد من aistudio.google.com
API_KEY = "gen-lang-client-0933546265" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

with st.sidebar:
    st.title("🤖 MOATASEM AI")
    st.write("ارفع ملفاتك (PDF أو صور) وابدأ الدردشة")
    uploaded_files = st.file_uploader("اختر الملفات", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

st.title("💬 غرفة الدردشة")

# استخراج المحتوى
context_text = ""
images = []
if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf":
            try:
                reader = PdfReader(file)
                for page in reader.pages:
                    context_text += page.extract_text()
            except: st.error(f"فشل قراءة ملف: {file.name}")
        else:
            images.append(Image.open(file))
    if uploaded_files: st.success("تم تجهيز الملفات بنجاح!")

# نظام الذاكرة للدردشة
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
        # الرد الخاص بالمطور
        if any(word in prompt.lower() for word in ["من صنعك", "من طورك", "who made you"]):
            res = "أنا نظام ذكاء اصطناعي تم تطويري وبرمجتي بواسطة المطور المبدع **معتصم نبيل المليكي**."
        else:
            try:
                # تجهيز الطلب للذكاء الاصطناعي
                content_list = []
                if context_text:
                    content_list.append(f"هذا نص من ملفات مرفوعة للاستعانة بها: {context_text[:4000]}")
                content_list.append(prompt)
                if images:
                    content_list.extend(images)
                
                response = model.generate_content(content_list)
                res = response.text
            except Exception as e:
                res = "عذراً، يبدو أن هناك ضغطاً على المحرك حالياً. يرجى المحاولة بعد لحظات."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
