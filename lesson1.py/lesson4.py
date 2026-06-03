def get_product_info(product_id, products):
    """根据 ID 查商品"""
    for p in products:
        if p["id"] == product_id:
            return p
    return None  # 没找到返回 None

def check_stock(product):
    """判断库存状态"""
    if product["stock"] == 0:
        return "已售罄"
    elif product["stock"] < 10:
        return "库存紧张"
    else:
        return "有货"

# 商品数据
products = [
    {"id": 1, "name": "Nike 运动鞋", "price": 299, "stock": 5},
    {"id": 2, "name": "Adidas T恤",  "price": 89,  "stock": 0},
    {"id": 3, "name": "李宁背包",    "price": 199, "stock": 30},
]

# 模拟用户查询
for product_id in [1, 2, 3, 99]:
    product = get_product_info(product_id, products)
    
    if product is None:
        print(f"ID {product_id}：商品不存在")
    else:
        status = check_stock(product)
        print(f"{product['name']} | {product['price']} 元 | {status}")
