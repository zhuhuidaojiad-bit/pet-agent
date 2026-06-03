import streamlit as st
import time
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
client = Groq(api_key=os.getenv("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"))
def get_ai_response(messages):
    products = get_all_products()
    product_text = ""
    for p in products:
        stock_status = "有货" if p["stock"] > 10 else ("库存紧张" if p["stock"] > 0 else "售罄")
        product_text += f"- [{p['category']}] {p['name']}，品牌：{p['brand']}，价格：{p['price']}元，{stock_status}，简介：{p['desc']}\n"

    system_prompt = f"""你是一个专业的宠物店 AI 客服助手，名字叫"萌宠小助手"。

当前在售商品：
{product_text}

服务准则：
1. 用亲切友好的语气，适当使用宠物emoji
2. 根据宠物品种、年龄、健康状况精准推荐并说明理由
3. 涉及健康问题时给专业建议并提醒必要时就医
4. 回答简洁专业不废话"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, *messages]
    )
    return response.choices[0].message.content

def typewriter(text, speed=0.015):
    container = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        container.markdown(displayed + "▌")
        time.sleep(speed)
    container.markdown(displayed)

st.set_page_config(page_title="萌宠小助手", page_icon="🐾", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #212121; }
#MainMenu, header, footer { visibility: hidden; }
[data-testid="stSidebar"] {
    background-color: #171717 !important;
    border-right: 1px solid #2f2f2f;
}
[data-testid="stSidebar"] * { color: #ececec !important; }
.product-card {
    background: #2a2a2a;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 6px;
    transition: border-color 0.2s;
}
.product-card:hover { border-color: #10a37f; }
.p-name { font-size: 13px; font-weight: 600; color: #ececec; }
.p-price { font-size: 13px; color: #10a37f; font-weight: 700; margin-top: 2px; }
.p-desc { font-size: 11px; color: #8e8ea0; margin-top: 3px; line-height: 1.4; }
.tag-ok   { background:#0d3d2e; color:#10a37f; border-radius:4px; padding:1px 6px; font-size:11px; }
.tag-warn { background:#3d2e0d; color:#f5a623; border-radius:4px; padding:1px 6px; font-size:11px; }
.tag-out  { background:#3d0d0d; color:#ef4444; border-radius:4px; padding:1px 6px; font-size:11px; }
.stButton button {
    background: transparent !important;
    border: 1px solid #3a3a3a !important;
    color: #8e8ea0 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    width: 100% !important;
}
.stButton button:hover { border-color: #ef4444 !important; color: #ef4444 !important; }
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 12px 0 !important;
    max-width: 760px;
    margin: 0 auto;
}
[data-testid="stChatInput"] textarea {
    background: #2f2f2f !important;
    border: 1px solid #444 !important;
    border-radius: 14px !important;
    color: #ececec !important;
    font-size: 15px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #10a37f !important;
    box-shadow: 0 0 0 2px rgba(16,163,127,0.15) !important;
}
.welcome-card {
    background: linear-gradient(135deg, #1a2e25, #1e2a3a);
    border: 1px solid #2a4a3a;
    border-radius: 16px;
    padding: 24px;
    max-width: 760px;
    margin: 40px auto 20px;
    text-align: center;
}
.welcome-icon { font-size: 48px; margin-bottom: 12px; }
.welcome-title { font-size: 20px; font-weight: 700; color: #ececec; margin-bottom: 8px; }
.welcome-desc { font-size: 14px; color: #8e8ea0; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("## 🐾 萌宠小助手")
    st.markdown("<small style='color:#8e8ea0'>专业宠物 AI 客服</small>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**📦 商品分类**")
    categories = ["全部", "🐕 狗粮", "🐈 猫粮", "🛍️ 用品", "💊 医疗"]
    cat_map = {"全部": "全部", "🐕 狗粮": "狗粮", "🐈 猫粮": "猫粮", "🛍️ 用品": "用品", "💊 医疗": "医疗"}
    selected = st.radio("", categories, label_visibility="collapsed")
    selected_cat = cat_map[selected]

    st.markdown("---")
    products = get_all_products()
    filtered = products if selected_cat == "全部" else [p for p in products if p["category"] == selected_cat]

    for p in filtered:
        if p["stock"] > 10:
            tag = '<span class="tag-ok">有货</span>'
        elif p["stock"] > 0:
            tag = '<span class="tag-warn">紧张</span>'
        else:
            tag = '<span class="tag-out">售罄</span>'

        st.markdown(f"""
        <div class="product-card">
            <div class="p-name">{p['name']}</div>
            <div class="p-price">¥{p['price']} &nbsp; {tag}</div>
            <div class="p-desc">{p['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ 清空对话记录", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 主聊天区
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-icon">🐾</div>
        <div class="welcome-title">你好，我是萌宠小助手</div>
        <div class="welcome-desc">
            告诉我你家宠物的品种和年龄<br>我来帮你找到最合适的商品和解答任何问题
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🐕 推荐成犬狗粮", use_container_width=True):
            st.session_state.pending = "帮我推荐适合成犬的狗粮"
            st.rerun()
    with col2:
        if st.button("🐈 猫咪不吃饭怎么办", use_container_width=True):
            st.session_state.pending = "我的猫咪最近不爱吃饭怎么办"
            st.rerun()
    with col3:
        if st.button("💊 宠物驱虫推荐", use_container_width=True):
            st.session_state.pending = "宠物驱虫药怎么选"
            st.rerun()
else:
    st.markdown("### 萌宠小助手 🐾")
    st.markdown("<small style='color:#8e8ea0'>专业宠物 AI 客服，随时为你服务</small>", unsafe_allow_html=True)
    st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if "pending" in st.session_state:
    user_input = st.session_state.pending
    del st.session_state.pending
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        answer = get_ai_response(st.session_state.messages)
        typewriter(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

if user_input := st.chat_input("问我任何关于宠物的问题..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        answer = get_ai_response(st.session_state.messages)
        typewriter(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})