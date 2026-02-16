    import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MOATASEM AI", page_icon="🧠", layout="wide")

# --- 2. التصميم CSS ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    footer {visibility: hidden;}
    .developer-footer {
        position: fixed; bottom: 10px; right: 15px;
        color: #666; font-size: 12px;
    }
    </style>
    <div class="developer-footer">Developed by: MOATASEM AI</div>
    """, unsafe_allow_html=True)

# --- 3. إعدادات API (المفتاح الصحيح) ---
API_KEY = "AIzaSyCC69LDLdON1hSCQ1QIr7zRFvTLouCFV-s" 
genai.configure(api_key=API_KEY)

# الحل هنا: جربنا 'gemini-pro' لأنه الأكثر استقراراً ومجاني تماماً
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 4. إدارة الجلسة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🤖 MOATASEM AI")
    uploaded_files = st.file_uploader("ارفع ملفاتك", type=["pdf", "jpg", "png"], accept_multiple_files=True)
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# --- 6. معالجة الملفات ---
if uploaded_files:
    text_content = ""
    for file in uploaded_files:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
    st.session_state.context = text_content
    st.sidebar.success("✅ تم تجهيز البيانات")

# --- 7. الواجهة والدردشة ---
st.markdown("<h2 style='text-align: center;'>🧠 محرك معتصم للذكاء الاصطناعي</h2>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if any(w in prompt.lower() for w in ["من صنعك", "من طورك", "who made you"]):
            response_text = "تم تطويري بواسطة المبدع **معتصم نبيل المليكي**."
        else:
            try:
                # دمج السؤال مع سياق الملفات
                full_input = f"Context: {st.session_state.context[:5000]}\nQuestion: {prompt}"
                response = model.generate_content(full_input)
                response_text = response.text
            except Exception as e:
                response_text = "عذراً، المحرك يحتاج للتحديث. تأكد من اتصال الإنترنت وحاول مجدداً."

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
