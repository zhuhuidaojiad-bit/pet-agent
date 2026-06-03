import sqlite3

DB_FILE = "pet_shop.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            price    REAL NOT NULL,
            stock    INTEGER NOT NULL,
            category TEXT NOT NULL,
            brand    TEXT,
            desc     TEXT
        )
    """)
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        initial_products = [
            ("皇家成犬狗粮 10kg", 299, 50, "狗粮", "皇家",   "适合1岁以上成犬，均衡营养"),
            ("冠能幼犬狗粮 5kg",  189, 30, "狗粮", "冠能",   "适合2月龄以上幼犬，促进发育"),
            ("希尔斯处方粮 4kg",  520, 15, "狗粮", "希尔斯", "肾病犬专用，低磷低蛋白"),
            ("皇家成猫猫粮 4kg",  219, 60, "猫粮", "皇家",   "适合1岁以上成猫，维持理想体重"),
            ("渴望无谷猫粮 5kg",  389, 25, "猫粮", "渴望",   "无谷物配方，高蛋白低碳水"),
            ("麦富迪冻干猫粮",    128, 40, "猫粮", "麦富迪", "冻干工艺锁鲜，营养丰富"),
            ("狗狗自动饮水机",     89, 80, "用品", "小佩",   "循环过滤，保持水质新鲜"),
            ("猫咪自动喂食器",    159, 35, "用品", "小佩",   "定时定量，支持手机APP控制"),
            ("宠物除跳蚤滴剂",     65, 100,"医疗", "福来恩", "体外驱虫，一月一次"),
            ("狗狗驱虫药 体内",    45, 90, "医疗", "拜宠清", "广谱驱虫，适合3月龄以上"),
        ]
        c.executemany(
            "INSERT INTO products (name,price,stock,category,brand,desc) VALUES (?,?,?,?,?,?)",
            initial_products
        )
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id,name,price,stock,category,brand,desc FROM products ORDER BY category,id")
    rows = c.fetchall()
    conn.close()
    return [{"id":r[0],"name":r[1],"price":r[2],"stock":r[3],"category":r[4],"brand":r[5],"desc":r[6]} for r in rows]

def add_product(name, price, stock, category, brand, desc):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO products (name,price,stock,category,brand,desc) VALUES (?,?,?,?,?,?)",
              (name, price, stock, category, brand, desc))
    conn.commit()
    conn.close()

def update_product(pid, name, price, stock, category, brand, desc):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE products SET name=?,price=?,stock=?,category=?,brand=?,desc=? WHERE id=?",
              (name, price, stock, category, brand, desc, pid))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

init_db()