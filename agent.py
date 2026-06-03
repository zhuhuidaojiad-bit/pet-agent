from groq import Groq

client = Groq(api_key="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")

# 商品数据库（模拟真实电商数据）
products = [
    {"id": 1, "name": "Nike 运动鞋", "price": 299, "stock": 50, "category": "鞋类"},
    {"id": 2, "name": "Adidas 跑步鞋", "price": 499, "stock": 20, "category": "鞋类"},
    {"id": 3, "name": "李宁 T恤", "price": 89, "stock": 100, "category": "服装"},
    {"id": 4, "name": "安踏 运动裤", "price": 129, "stock": 60, "category": "服装"},
    {"id": 5, "name": "耐克 背包", "price": 199, "stock": 30, "category": "配件"},
    {"id": 6, "name": "Jordan 篮球鞋", "price": 899, "stock": 10, "category": "鞋类"},
]

def search_products(keyword):
    """搜索商品"""
    results = []
    for p in products:
        if keyword in p["name"] or keyword in p["category"]:
            results.append(p)
    return results

def get_product_list():
    """获取所有商品"""
    return products

def ask_agent(user_question):
    """把用户问题和商品数据一起发给 AI"""
    
    # 把商品列表转成文字
    product_text = ""
    for p in products:
        product_text += f"- {p['name']}，价格：{p['price']}元，库存：{p['stock']}件\n"
    
    # 给 AI 的系统指令
    system_prompt = f"""你是一个专业的电商客服助手。
    
当前商品库存如下：
{product_text}

请根据用户的问题，结合以上商品信息给出专业的回答。
如果用户想买某类商品，帮他推荐合适的。
回答要简洁友好，用中文回复。"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    )
    
    return response.choices[0].message.content

# 启动对话循环
print("=" * 40)
print("欢迎来到电商客服系统！")
print("输入你的问题，输入'退出'结束对话")
print("=" * 40)

while True:
    user_input = input("\n你：")
    
    if user_input == "退出":
        print("感谢使用，再见！")
        break
    
    print("\nAI客服：", end="")
    answer = ask_agent(user_input)
    print(answer)