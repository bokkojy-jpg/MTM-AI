import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image
import io

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(
    page_title="MOATASEM AI | الذكاء الاصطناعي",
    page_icon="⚡",
    layout="wide"
)

# --- 2. تصميم الواجهة CSS ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
    }
    
    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* تنسيق الرسائل */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        padding: 10px;
    }

    /* تذييل الصفحة (Footer) */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        letter-spacing: 1px;
    }
    
    /* إخفاء شعار ستريمليت الافتراضي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    
    <div class="footer">Developed with ❤️ by MOATASEM</div>
    """, unsafe_allow_html=True)

# --- 3. إعدادات API ---
# ملاحظة: يفضل وضع المفتاح في st.secrets للأمان
API_KEY = "AIzaSyCC69LDLdON1hSCQ1QIr7zRFvTLouCFV-s" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 4. إدارة الحالة (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_context" not in st.session_state:
    st.session_state.processed_context = ""
if "processed_images" not in st.session_state:
    st.session_state.processed_images = []

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("MOATASEM AI")
    st.markdown("---")
    st.subheader("📁 مركز الملفات")
    uploaded_files = st.file_uploader(
        "ارفع PDF أو صور لتحليلها", 
        type=["pdf", "jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = []
        st.rerun()

# --- 6. معالجة الملفات المرفوعة ---
if uploaded_files:
    new_context = ""
    new_images = []
    with st.spinner("جاري معالجة الملفات..."):
        for file in uploaded_files:
            if file.type == "application/pdf":
                try:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text: new_context += text + "\n"
                except Exception as e:
                    st.error(f"خطأ في ملف PDF: {file.name}")
            else:
                try:
                    img = Image.open(file)
                    new_images.append(img)
                except Exception as e:
                    st.error(f"خطأ في الصورة: {file.name}")
        
        st.session_state.processed_context = new_context
        st.session_state.processed_images = new_images
        st.sidebar.success(f"✅ تم تحميل {len(uploaded_files)} ملفات")

# --- 7. واجهة الدردشة ---
st.markdown("<h2 style='text-align: center;'>🧠 محرك معتصم للذكاء الاصطناعي</h2>", unsafe_allow_html=True)

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("كيف يمكن لـ MOATASEM AI مساعدتك اليوم؟"):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # استجابة البوت
    with st.chat_message("assistant"):
        # الرد المخصص بناءً على معلومات المطور
        creator_keywords = ["من صنعك", "من طورك", "من المطور", "who created you", "who is the developer"]
        
        if any(keyword in prompt.lower() for keyword in creator_keywords):
            full_response = "تم تطويري وتصميمي بواسطة المبدع **معتصم نبيل المليكي (Mutasim Nabil Al-Maliki)** كنموذج ذكاء اصطناعي متطور."
        else:
            try:
                # تجهيز المحتوى للإرسال
                content_to_send = []
                
                # إضافة السياق النصي (بحد أقصى للرموز لضمان السرعة)
                if st.session_state.processed_context:
                    content_to_send.append(f"سياق من الملفات المرفوعة:\n{st.session_state.processed_context[:10000]}")
                
                # إضافة الصور
                if st.session_state.processed_images:
                    content_to_send.extend(st.session_state.processed_images)
                
                # إضافة سؤال المستخدم
                content_to_send.append(prompt)
                
                # توليد الرد
                with st.spinner("يفكر معتصم AI..."):
                    response = model.generate_content(content_to_send)
                    full_response = response.text
                    
            except Exception as e:
                full_response = f"⚠️ حدث خطأ: تأكد من صلاحية مفتاح الـ API أو حجم البيانات المرفوعة."
                st.error(str(e))

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
