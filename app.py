import streamlit as st
from openai import OpenAI

# إعداد الواجهة
st.set_page_config(page_title="Agency AI Assistant", page_icon="🤖")

st.title("🤖 Agency AI Business Suite")
st.markdown("---")

# إدخال المفتاح بشكل آمن في الواجهة
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    # إنشاء اتصال بالعميل الجديد (الإصدار الحديث)
    client = OpenAI(api_key=api_key)
    
    service = st.selectbox("اختار الخدمة المطلوبة:", 
                          ["وكيل عقاري ذكي", "محلل بيانات مبيعات", "كاتب محتوى تسويقي"])

    user_input = st.text_area("كيف يمكنني مساعدتك اليوم؟")

    if st.button("تشغيل النظام"):
        with st.spinner('جاري معالجة طلبك عبر Agency AI...'):
            prompts = {
                "وكيل عقاري ذكي": "أنت خبير عقارات لبق، ساعد العميل في العثور على عقار مناسب.",
                "محلل بيانات مبيعات": "أنت محلل بيانات محترف، استخرج أهم الأرقام من النص التالي.",
                "كاتب محتوى تسويقي": "أنت خبير تسويق، اكتب محتوى إبداعي يجذب العملاء."
            }

            # طريقة النداء الجديدة للموديل
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompts[service]},
                    {"role": "user", "content": user_input}
                ]
            )
            
            st.success("النتيجة:")
            st.write(response.choices[0].message.content)
else:
    st.warning("الرجاء إدخال الـ API Key في القائمة الجانبية لتفعيل النظام.")
