# 列表：一组数据，用 [] 包住，像购物车
cart = ["Nike 运动鞋", "Adidas T恤", "李宁背包"]

print(cart[0])   # 取第一个，编号从 0 开始
print(cart[1])   # 取第二个
print(len(cart)) # 列表长度

# 字典：有名字的数据，用 {} 包住，像商品详情页
product = {
    "name": "Nike 运动鞋",
    "price": 299,
    "stock": 50,
    "category": "鞋类"
}

print(product["name"])   # 取商品名
print(product["price"])  # 取价格

# 修改字典里的值
product["price"] = 259
print(f"降价后：{product['price']} 元")

# 列表套字典：真实电商数据就长这样
products = [
    {"name": "Nike 运动鞋", "price": 299, "stock": 50},
    {"name": "Adidas T恤",  "price": 89,  "stock": 120},
    {"name": "李宁背包",    "price": 199, "stock": 30},
]

# 用 for 循环遍历所有商品
for p in products:
    print(f"{p['name']} —— {p['price']} 元，库存 {p['stock']} 件")
