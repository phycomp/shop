設定綠界金流api  使用streamlit 作成電子商務網站 要在 Streamlit 中設置 綠界 (ECPay) 金流 API，并構建一個簡單的電子商務網站，你可以按照以下步驟進行：

1. 安裝依賴庫 首先，安裝 Streamlit 和 requests 庫，用來進行 HTTP 請求操作：pip install streamlit requests
2. 綠界 API 準備 在使用綠界金流服務之前，你需要先完成以下準備工作：
注冊一個 綠界 帳號，并獲得 API 商店 ID 和 API Key。
在綠界後台設置好回調 URL（Payment Return URL），用于接收交易結果。
3. 綠界 API 請求參數
綠界 API 的核心是通過 POST 請求向它的服務器發送交易信息，并接收支付結果。請求數據中包括：

MerchantID: 商戶 ID
MerchantTradeNo: 商戶交易編號
MerchantTradeDate: 交易日期
TotalAmount: 交易金額
TradeDesc: 商品描述
ItemName: 商品名稱
ReturnURL: 回調 URL
ChoosePayment: 支付方式
CheckMacValue: 防篡改簽名
4. 生成 CheckMacValue（簽名）
CheckMacValue 是綠界用于防止數據篡改的哈希簽名。你需要使用 SHA256 進行簽名，遵循特定的格式將參數拼接并計算出簽名值。

import hashlib
import urllib.parse

def generate_check_mac_value(params, hash_key, hash_iv):
    sorted_params = sorted(params.items())
    raw = '&'.join(f'{k}={v}' for k, v in sorted_params)
    raw = f"HashKey={hash_key}&{raw}&HashIV={hash_iv}"
    raw = urllib.parse.quote_plus(raw).lower()
    
    check_mac_value = hashlib.sha256(raw.encode('utf-8')).hexdigest().upper()
    return check_mac_value
5. 整合 Streamlit 和綠界 API
現在我們將整合 Streamlit 的前端界面，讓用戶可以通過頁面輸入商品信息并完成支付流程。

示例代碼：
python
複製程式碼
import streamlit as st
import requests
from datetime import datetime
import hashlib
import urllib.parse

# 綠界商店ID 和 API Key
MERCHANT_ID = 'YourMerchantID'
HASH_KEY = 'YourHashKey'
HASH_IV = 'YourHashIV'
PAYMENT_URL = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'

# 生成 CheckMacValue
def generate_check_mac_value(params, hash_key, hash_iv):
    sorted_params = sorted(params.items())
    raw = '&'.join(f'{k}={v}' for k, v in sorted_params)
    raw = f"HashKey={hash_key}&{raw}&HashIV={hash_iv}"
    raw = urllib.parse.quote_plus(raw).lower()
    
    check_mac_value = hashlib.sha256(raw.encode('utf-8')).hexdigest().upper()
    return check_mac_value

# Streamlit 前端表單
st.title("E-Commerce Website with ECPay")
st.header("Payment Information")

# 輸入商品信息
item_name = st.text_input("Item Name", "Sample Item")
total_amount = st.number_input("Total Amount", min_value=1, value=100)
if st.button("Proceed to Payment"):
    # 生成商戶交易編號
    trade_no = f"EC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 設置交易參數
    params = {
        'MerchantID': MERCHANT_ID,
        'MerchantTradeNo': trade_no,
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': total_amount,
        'TradeDesc': 'ECPay payment description',
        'ItemName': item_name,
        'ReturnURL': 'https://yourdomain.com/callback',  # 必須爲您的回調URL
        'ChoosePayment': 'ALL',
        'EncryptType': '1'
    }
    
    # 生成 CheckMacValue
    check_mac_value = generate_check_mac_value(params, HASH_KEY, HASH_IV)
    params['CheckMacValue'] = check_mac_value
    
    # 提交 POST 請求至綠界
    response = requests.post(PAYMENT_URL, data=params)
    
    # 顯示交易編號和支付鏈接
    st.write(f"Transaction ID: {trade_no}")
    st.write(f"[Proceed to Payment]({PAYMENT_URL})")
6. 配置步驟詳解
生成 CheckMacValue：通過 generate_check_mac_value() 方法對交易數據進行簽名，确保數據安全。
Streamlit 前端：用戶可以通過輸入商品名稱和金額來生成一個新的交易請求。點擊按鈕後，交易數據會發送至綠界的支付接口。
支付鏈接：當交易數據發送成功後，頁面將顯示生成的交易編號，并提供支付鏈接，用戶可以點擊完成支付。
7. 支付回調處理
在 ReturnURL 指定的回調 URL 中處理支付結果。綠界會將交易結果通過 POST 請求返回，你需要在服務器端處理支付結果。

python
複製程式碼
from flask import Flask, request

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def ecpay_callback():
    result = request.form.to_dict()
    # 驗證 CheckMacValue，确保數據安全
    if verify_check_mac_value(result, HASH_KEY, HASH_IV):
        # 處理交易結果
        return '1|OK'
    else:
        return '0|FAIL'
8. 擴展功能
支付方式選擇：在 params 的 ChoosePayment 字段可以選擇支付方式，比如信用卡、ATM 等。
前端優化：可以使用 Streamlit 的其他組件，如 st.selectbox 提供用戶選擇不同支付方式。
支付歷史：可以將支付結果存入數據庫，并在 Streamlit 界面中顯示用戶的支付歷史記錄。
9. 部署
將整個應用部署到像 Heroku、Streamlit Cloud 或自己的服務器上，确保你的回調 URL 能夠被綠界訪問。

總結 通過 Streamlit 與綠界金流 API 的整合，可以快速構建一個輕量級的電子商務網站，并支持多種支付方式。
