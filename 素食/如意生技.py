# requirements.txt
# streamlit
# psycopg2-binary
# sqlalchemy
# pandas

from streamlit import title, header, columns as stCLMN, error as stError, image as stImage, subheader, write as stWrite, button, session_state, sidebar, success, markdown
import psycopg2
#from sqlalchemy import create_engine
import pandas as pd
from dbUtil import runQuery
from stUtil import rndrCode

如意DF=runQuery('select * from 如意;', db='ruyi')
rndrCode(如意DF)
# 資料庫連接配置
#DB_CONFIG = { 'host': 'localhost', 'database': 'ruyi_shop', 'user': 'your_username', 'password': 'your_password' }

def connect_db():
    try:
        engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")
        return engine
    except Exception as e:
        stError(f"資料庫連接錯誤: {e}")
        return None

def load_products():
  商品=runQuery('select * from 如意;')
  """
    engine = connect_db()
    if engine:
        query = "SELECT * FROM products"
        return pd.read_sql(query, engine)
  """
  商品DF=DataFrame(商品, columns=['商品'])
  return 商品DF#pd.DataFrame()
MENU, 表單=[], ['商城', '購物車', '']	#, '錯綜複雜', '二十四節氣'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
with sidebar:
  menu=stRadio('表單', MENU, horizontal=True, index=0)
  srch=text_input('搜尋', '')
if menu==len(表單):
  pass
elif menu==MENU[1]:
  tblName='購物車'
elif menu==MENU[0]:
  #商城 商品展示
  title("如意生技素料商城")
  商品DF = load_products()
  header("商品列表")
  左, 右 = stCLMN([1, 3])
  for idx, product in 商品DF.iterrows():
    with 左:
        stImage(product['image_url'], width=150)
    with 右:
      subheader(product['name'])
      stWrite(f"價格: ${product['price']}")
      stWrite(product['description'])
      if button(f"加入購物車 - {product['name']}"):
        session_state[product['name']] = session_state.get(product['name'], 0) + 1

  # 購物車
  header("🛒 購物車")
  total_price = 0
  for product_name, quantity in session_state.items():
    if quantity > 0:
      product = products_df[products_df['name'] == product_name].iloc[0]
      item_total = product['price'] * quantity
      total_price += item_total
      with sidebar:
        stWrite(f"{product_name} x {quantity} = ${item_total}")

        markdown(f"**總計:** ${total_price}")
        if button("結帳"):
          success("感謝您的購買！")

# PostgreSQL建表SQL
"""
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    description TEXT,
    image_url TEXT
);

INSERT INTO products (name, price, description, image_url) VALUES
('素雞', 120, '純素雞肉', 'https://example.com/suji.jpg'),
('素魚', 150, '純素魚肉', 'https://example.com/suyu.jpg');
"""
