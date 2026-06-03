import streamlit as st
import requests
import base64
from PIL import Image
import io
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
groq_client = Groq(api_key=os.getenv("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"))
STABILITY_KEY = os.getenv("sk-m5809Vd07ESkZxA6WTEY0u52hIy2iHfVLOrKJ2rhLWbzwrHZ")st.set_page_config(page_title="商家管理后台", page_icon="🏪", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #212121; color: #ececec; }
#MainMenu, header, footer { visibility: hidden; }
[data-testid="stSidebar"] { background-color: #171717 !important; border-right: 1px solid #2f2f2f; }
[data-testid="stSidebar"] * { color: #ececec !important; }
.stButton button {
    border-radius: 8px !important;
    background: transparent !important;
    border: 1px solid #3a3a3a !important;
    color: #ececec !important;
    transition: all 0.2s !important;
}
.stButton button:hover { border-color: #10a37f !important; color: #10a37f !important; }
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: #2f2f2f !important;
    color: #ececec !important;
    border-color: #444 !important;
    border-radius: 8px !important;
}
div[data-testid="stForm"] {
    background: #2a2a2a;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 20px;
}
.result-box {
    background: #2a2a2a;
    border: 1px solid #10a37f;
    border-radius: 12px;
    padding: 20px;
    margin-top: 12px;
    line-height: 1.8;
    color: #ececec;
    white-space: pre-wrap;
    font-size: 14px;
}
.section-title {
    font-size: 13px;
    color: #10a37f;
    font-weight: 600;
    margin: 16px 0 6px;
    border-left: 3px solid #10a37f;
    padding-left: 8px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🏪 商家后台")
    st.markdown("---")
    page = st.radio("", [
        "📦 商品管理",
        "✍️ 文案 Agent",
        "🎵 推广 Agent",
        "📸 图片 Agent",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<small style='color:#8e8ea0'>萌宠小助手管理系统</small>", unsafe_allow_html=True)

# ===== 商品管理 =====
if page == "📦 商品管理":
    st.markdown("## 📦 商品管理")
    products = get_all_products()
    st.markdown(f"**共 {len(products)} 个商品**")
    st.markdown("---")
    tab1, tab2 = st.tabs(["商品列表", "➕ 添加商品"])
    with tab1:
        for p in products:
            with st.expander(f"{'🟢' if p['stock'] > 10 else '🟡' if p['stock'] > 0 else '🔴'} {p['name']} — ¥{p['price']} | 库存 {p['stock']}件"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.form(key=f"edit_{p['id']}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_name  = st.text_input("商品名称", value=p["name"])
                            new_brand = st.text_input("品牌", value=p["brand"] or "")
                            new_cat   = st.selectbox("分类", ["狗粮","猫粮","用品","医疗"],
                                                      index=["狗粮","猫粮","用品","医疗"].index(p["category"]))
                        with c2:
                            new_price = st.number_input("价格", value=float(p["price"]), min_value=0.0)
                            new_stock = st.number_input("库存", value=int(p["stock"]), min_value=0)
                            new_desc  = st.text_input("描述", value=p["desc"] or "")
                        if st.form_submit_button("💾 保存", use_container_width=True):
                            update_product(p["id"], new_name, new_price, new_stock, new_cat, new_brand, new_desc)
                            st.success("✅ 修改成功！")
                            st.rerun()
                with col2:
                    st.markdown("&nbsp;")
                    if st.button("🗑️ 删除", key=f"del_{p['id']}", use_container_width=True):
                        delete_product(p["id"])
                        st.rerun()
    with tab2:
        with st.form("add_form"):
            c1, c2 = st.columns(2)
            with c1:
                name     = st.text_input("商品名称 *")
                brand    = st.text_input("品牌")
                category = st.selectbox("分类", ["狗粮","猫粮","用品","医疗"])
            with c2:
                price = st.number_input("价格", min_value=0.0, value=99.0)
                stock = st.number_input("库存", min_value=0, value=50)
                desc  = st.text_input("描述")
            if st.form_submit_button("➕ 添加", use_container_width=True):
                if not name:
                    st.error("❌ 请填写商品名称")
                else:
                    add_product(name, price, stock, category, brand, desc)
                    st.success(f"✅ 已添加：{name}")
                    st.rerun()

# ===== 文案 Agent =====
elif page == "✍️ 文案 Agent":
    st.markdown("## ✍️ 文案 Agent")
    st.markdown("<small style='color:#8e8ea0'>输入商品信息，AI 自动生成各平台文案</small>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📝 填写商品信息")
        products = get_all_products()
        product_names = ["手动填写"] + [p["name"] for p in products]
        selected = st.selectbox("从已有商品选择", product_names)
        if selected != "手动填写":
            p = next(x for x in products if x["name"] == selected)
            product_name  = st.text_input("商品名称", value=p["name"])
            product_brand = st.text_input("品牌", value=p["brand"] or "")
            product_price = st.number_input("价格", value=float(p["price"]))
            product_desc  = st.text_area("描述", value=p["desc"] or "", height=80)
        else:
            product_name  = st.text_input("商品名称", placeholder="例：皇家成犬狗粮 10kg")
            product_brand = st.text_input("品牌", placeholder="例：皇家")
            product_price = st.number_input("价格", value=99.0)
            product_desc  = st.text_area("描述", placeholder="例：适合1岁以上成犬", height=80)
        product_extra = st.text_area("补充卖点", placeholder="例：双十一特价、买二送一", height=60)
        copy_types = st.multiselect("选择文案类型",
            ["📱 小红书推广文案","🎵 抖音视频脚本","💬 朋友圈文案","🛒 商品详情页文案","📣 促销活动文案"],
            default=["📱 小红书推广文案","💬 朋友圈文案"])
        tone = st.select_slider("文案风格", options=["专业严肃","中性平衡","活泼可爱","种草热情"], value="活泼可爱")
        generate = st.button("🚀 一键生成文案", use_container_width=True, type="primary")
    with col2:
        st.markdown("### ✨ 生成结果")
        if generate:
            if not product_name:
                st.error("❌ 请填写商品名称")
            elif not copy_types:
                st.error("❌ 请选择文案类型")
            else:
                types_str = "、".join([t.split(" ")[1] for t in copy_types])
                prompt = f"""你是专业宠物电商文案策划师。
商品：{product_name}，品牌：{product_brand}，价格：¥{product_price}
描述：{product_desc}，卖点：{product_extra or '无'}
生成类型：{types_str}，风格：{tone}
围绕宠物主人情感需求写，每种类型用 --- 分隔，前面标注类型名称，直接输出文案。"""
                with st.spinner("生成中..."):
                    resp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}])
                    st.session_state.copy_result = resp.choices[0].message.content
        if "copy_result" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.copy_result}</div>', unsafe_allow_html=True)
            if st.button("📋 复制文案", use_container_width=True):
                st.code(st.session_state.copy_result)

# ===== 推广 Agent =====
elif page == "🎵 推广 Agent":
    st.markdown("## 🎵 推广 Agent")
    st.markdown("<small style='color:#8e8ea0'>生成抖音脚本、评论区话术、直播话术</small>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📝 填写推广信息")
        products = get_all_products()
        product_names = ["手动填写"] + [p["name"] for p in products]
        selected = st.selectbox("选择商品", product_names)
        if selected != "手动填写":
            p = next(x for x in products if x["name"] == selected)
            product_name  = st.text_input("商品名称", value=p["name"])
            product_price = st.number_input("价格", value=float(p["price"]))
            product_desc  = st.text_area("描述", value=p["desc"] or "", height=80)
        else:
            product_name  = st.text_input("商品名称", placeholder="例：皇家成犬狗粮")
            product_price = st.number_input("价格", value=99.0)
            product_desc  = st.text_area("描述", placeholder="例：适合成犬，均衡营养", height=80)
        promo_extra = st.text_area("活动信息（可选）", placeholder="例：买二送一、限时5折", height=60)
        promo_types = st.multiselect("选择推广内容", [
            "🎬 抖音视频脚本（60秒）",
            "💬 评论区引导话术（10条）",
            "🎙️ 直播带货话术",
            "📲 私信回复话术",
            "⭐ 买家好评引导话术",
        ], default=["🎬 抖音视频脚本（60秒）","💬 评论区引导话术（10条）"])
        target = st.selectbox("目标人群", ["养狗人士","养猫人士","新手宠物主","资深宠物主","所有宠物主"])
        goal   = st.selectbox("推广目标", ["引流涨粉","促进购买","提升品牌认知","活动预热"])
        generate = st.button("🚀 一键生成推广内容", use_container_width=True, type="primary")
    with col2:
        st.markdown("### ✨ 生成结果")
        if generate:
            if not product_name:
                st.error("❌ 请填写商品名称")
            elif not promo_types:
                st.error("❌ 请选择推广内容")
            else:
                types_str = "、".join([t.split(" ")[1] for t in promo_types])
                prompt = f"""你是专业宠物电商短视频运营专家。
商品：{product_name}，价格：¥{product_price}，描述：{product_desc}
活动：{promo_extra or '无'}，目标人群：{target}，推广目标：{goal}
生成：{types_str}
抖音脚本要有钩子开头、卖点展示、引导行动；评论话术要自然真实；直播话术要有节奏感和紧迫感。
每种内容用 --- 分隔，前面标注类型，直接输出内容。"""
                with st.spinner("生成中..."):
                    resp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}])
                    st.session_state.promo_result = resp.choices[0].message.content
        if "promo_result" in st.session_state:
            sections = st.session_state.promo_result.split("---")
            for section in sections:
                section = section.strip()
                if section:
                    lines = section.split("\n")
                    title = lines[0] if lines else ""
                    content = "\n".join(lines[1:]).strip()
                    if title:
                        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{content}</div>', unsafe_allow_html=True)
            if st.button("📋 复制全部内容", use_container_width=True):
                st.code(st.session_state.promo_result)

# ===== 图片 Agent =====
elif page == "📸 图片 Agent":
    st.markdown("## 📸 图片 Agent")
    st.markdown("<small style='color:#8e8ea0'>AI 自动生成商品海报和宣传图</small>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🎨 设置图片内容")

        products = get_all_products()
        product_names = ["手动填写"] + [p["name"] for p in products]
        selected = st.selectbox("选择商品", product_names)
        if selected != "手动填写":
            p = next(x for x in products if x["name"] == selected)
            product_name = st.text_input("商品名称", value=p["name"])
            product_desc = st.text_area("描述", value=p["desc"] or "", height=80)
        else:
            product_name = st.text_input("商品名称", placeholder="例：皇家成犬狗粮")
            product_desc = st.text_area("描述", placeholder="例：适合成犬，均衡营养", height=80)

        style = st.selectbox("图片风格", [
            "商业产品图（白色背景，专业）",
            "温馨生活场景（宠物与主人）",
            "节日促销海报（喜庆热闹）",
            "简约小清新（浅色背景）",
            "高端大气（黑色背景）",
        ])

        ratio = st.selectbox("图片尺寸", [
            "1:1 方图（适合商品主图）",
            "9:16 竖图（适合小红书/抖音）",
            "16:9 横图（适合Banner）",
        ])

        extra = st.text_input("额外要求（可选）", placeholder="例：要有金毛犬、要有促销标签")

        generate = st.button("🎨 生成图片", use_container_width=True, type="primary")

    with col2:
        st.markdown("### 🖼️ 生成结果")

        if generate:
            if not product_name:
                st.error("❌ 请填写商品名称")
            else:
                # 先用 AI 生成英文提示词
                prompt_request = f"""请为以下宠物商品生成一个 Stable Diffusion 图片提示词（英文）：
商品：{product_name}
描述：{product_desc}
风格：{style}
额外要求：{extra or '无'}

要求：
1. 提示词用英文，50-80个单词
2. 包含商品特征、场景、光线、质感描述
3. 末尾加上：high quality, professional photography, 8k, detailed
4. 只输出提示词，不要其他内容"""

                with st.spinner("第一步：AI 理解商品特征..."):
                    resp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt_request}])
                    image_prompt = resp.choices[0].message.content.strip()

                st.markdown(f"**📝 图片描述：** `{image_prompt[:80]}...`")

                # 根据尺寸设置参数
                if "1:1" in ratio:
                    width, height = 1024, 1024
                elif "9:16" in ratio:
                    width, height = 768, 1344
                else:
                    width, height = 1344, 768

                with st.spinner("第二步：AI 正在生图，约需 10-20 秒..."):
                    response = requests.post(
                        "https://api.stability.ai/v2beta/stable-image/generate/core",
                        headers={
                            "authorization": f"Bearer {STABILITY_KEY}",
                            "accept": "image/*"
                        },
                        files={"none": ""},
                        data={
                            "prompt": image_prompt,
                            "output_format": "png",
                            "width": width,
                            "height": height,
                        }
                    )

                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    st.image(img, caption=f"{product_name} 宣传图", use_column_width=True)
                    st.session_state.generated_image = response.content
                    st.success("✅ 图片生成成功！")
                else:
                    st.error(f"❌ 生成失败：{response.text}")

        if "generated_image" in st.session_state:
            st.download_button(
                label="⬇️ 下载图片",
                data=st.session_state.generated_image,
                file_name=f"poster.png",
                mime="image/png",
                use_container_width=True
            )