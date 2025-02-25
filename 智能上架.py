from streamlit import title, success, number_input, button
from stUtil import rndrCode
import pandas as pd
import numpy as np
from PIL import Image
import pytesseract
from transformers import pipeline
import torch
from streamlit import file_uploader as flUpldr, image as stImage, 
#from sqlalchemy import create_engine, Column, Integer, String, Float
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

# 初始化模型
classification_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    description = Column(String)

def extract_text_from_image(image):
    """從圖片提取文字"""
    text = pytesseract.image_to_string(image, lang='chi_tra')
    return text

def classify_product(description, categories=None):
    """智能分類商品"""
    if categories is None:
      categories = ['生鮮食品', '加工食品', '素食', '有機食品', '即食商品']
    
    result = classification_model(description, categories)
    top_category = result['labels'][0]
    confidence = result['scores'][0]
    return top_category, confidence

def process_product_upload():
    """商品上架流程"""
    header("智能商品上架")
    
    # 上傳圖片
    上傳 = flUpldr("上傳商品圖片", type=["jpg", "png"])
    
    if 上傳:
        image = Image.open(上傳)
        stImage(image, caption='已上傳商品圖片', use_column_width=True)
        
        # 提取文字描述
        image_text = extract_text_from_image(image)
        rndrCode("圖片文字描述:", image_text)
        
        # 手動輸入或AI建議價格
        price = number_input("商品價格", min_value=0.0, step=10.0)
        
        # AI智能分類
        if button("智能分類"):
            category, confidence = classify_product(image_text)
            rndrCode(f"建議分類: {category} (信心度: {confidence:.2%})")
            
            # 確認與儲存
            if button("確認並儲存"):
                save_product(image_text, category, price)
                success("商品成功上架!")

def save_product(description, category, price):
    """儲存商品到資料庫"""
    engine = create_engine('postgresql://username:password@localhost/productdb')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    new_product=Product(name=description[:50], category=category, price=price, description=description)# 截斷為名稱
    
    session.add(new_product)
    session.commit()
    session.close()
def main():
    title("如意生技 - 智能商品上架系統")
    process_product_upload()

if __name__ == "__main__":
    main()

# 依賴安裝需求
"""
pip install streamlit pandas pillow pytesseract transformers torch sqlalchemy psycopg2-binary
"""
