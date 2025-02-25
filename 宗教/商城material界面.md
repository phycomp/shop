以下为采用 **Streamlit + Material Design** 重新设计的宗教团体商城系统方案，整合金流与智能商品管理功能：

---

### **一、UI/UX 核心设计原则**
```python
# 前置安装
pip install streamlit streamlit-material-components pandas
```

#### 1. Material Design 主题配置
```python
# .streamlit/config.toml (主题定制)
[theme]
primaryColor = "#4B0082"  # 宗教风格深紫色
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#333333"
font = "sans serif"
```

#### 2. 布局架构
```python
import streamlit as st
from streamlit_material_components import card, button

def main():
    st.set_page_config(page_title="道親商城", layout="wide")
    
    # 顶部导航栏
    with st.container():
        cols = st.columns([3,1,1,1])
        with cols[0]:
            st.markdown("# 🕊️ 清淨法緣商城")
        with cols[1]:
            if button(label="登入", key="login_btn", variant="contained"):
                show_login()
        # ...其他导航按钮

    # 商品展示区（Material Card设计）
    with st.container():
        st.subheader("✨ 推薦聖物")
        col1, col2, col3 = st.columns(3)
        with col1:
            card(
                title="白玉觀音像",
                content="純手工雕刻 開光加持",
                image="img/guan-yin.jpg",
                actions=[
                    {"label": "結緣請購", "onclick": lambda: start_payment(1)}
                ]
            )
```

---

### **二、PayPal 支付流程改造**
#### 1. 前端支付触发
```python
# 在商品卡片点击后触发表单
def show_payment_modal(product_id):
    with st.form(key=f"pay_form_{product_id}"):
        st.markdown("### 請填寫請購資訊")
        name = st.text_input("**姓名**", placeholder="請輸入法名")
        address = st.text_area("**寄送地址**")
        
        # 嵌入PayPal按钮
        paypal_js = """
        <script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID"></script>
        <div id="paypal-button-container"></div>
        <script>
            paypal.Buttons({
                createOrder: function(data, actions) {
                    return actions.order.create({
                        purchase_units: [{
                            amount: { value: '100.00' }
                        }]
                    });
                },
                onApprove: function(data, actions) {
                    return actions.order.capture().then(function(details) {
                        alert('Transaction completed by ' + details.payer.name.given_name);
                    });
                }
            }).render('#paypal-button-container');
        </script>
        """
        components.html(paypal_js, height=300)
        
        if st.form_submit_button("確認提交"):
            log_order(product_id, name, address)
```

#### 2. 后端支付状态监听
```python
# 支付成功回调处理
@st.cache_resource
def init_paypal():
    paypalrestsdk.configure({...})

def handle_ipn():
    if st.experimental_get_query_params().get("paymentId"):
        payment_id = st.experimental_get_query_params()["paymentId"][0]
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):
            st.success("支付成功！法器將於3日內寄出")
            update_order_status(payment_id, "paid")
```

---

### **三、智能商品管理仪表板**
#### 1. 自动审核控制台
```python
if st.session_state.user_role == "admin":
    st.sidebar.markdown("## 智慧審核儀表板")
    
    # 实时审核数据看板
    audit_stats = get_audit_stats()
    st.metric("待審商品", audit_stats["pending"], delta="+2件新提交")
    
    # 商品审核队列
    with st.expander("📦 待審商品列表", expanded=True):
        for product in get_pending_products():
            cols = st.columns([1,3,2])
            cols[0].image(product["image"], width=100)
            cols[1].write(f"**{product['name']}**\n\n{product['description']}")
            with cols[2]:
                if st.button("通過", key=f"approve_{product['id']}"):
                    approve_product(product["id"])
                if st.button("駁回", key=f"reject_{product['id']}"):
                    reject_product(product["id"])
```

#### 2. 自动化审核流程整合
```python
# 文件上传与即时审核
uploaded_file = st.file_uploader("上傳新聖物圖片", type=["jpg", "png"])
if uploaded_file:
    with st.spinner("🛡️ 自動安全檢測中..."):
        img_path = save_uploaded_file(uploaded_file)
        nsfw_score = check_nsfw(img_path)  # 调用TensorFlow模型
        if nsfw_score > 0.7:
            st.error("⚠️ 圖片包含敏感內容，已自動攔截！")
            log_audit_failure("image", nsfw_score)
        else:
            st.success("圖片審核通過")
```

---

### **四、Material Design 增强组件**
#### 1. 响应式宗教风格组件库
```python
# 自定義法會通知卡片
def dharma_event_card(title, date, location):
    return f"""
    <div class="mdc-card" style="margin:10px;padding:15px;border-radius:8px;">
        <h3 style="color:{st.get_option('theme.primaryColor')};">{title}</h3>
        <div style="display:flex;align-items:center;gap:10px;">
            <span class="material-icons">event</span>
            <p>{date}</p>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
            <span class="material-icons">place</span>
            <p>{location}</p>
        </div>
    </div>
    """
# 在页面中调用
components.html(dharma_event_card("觀音誕辰法會", "2024-03-08", "台北道場"), height=150)
```

#### 2. 動態效果強化
```css
/* 自訂CSS動畫 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.mdc-card {
    animation: fadeIn 0.5s ease-out;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.mdc-card:hover {
    transform: translateY(-5px);
}
```

---

### **五、部署與效能優化**
```bash
# 生產環境部署指令
streamlit run app.py --server.port 8501 --server.enableCORS false \
--server.enableXsrfProtection true \
--server.headless true
```

#### 效能關鍵配置：
1. **緩存機制**：使用`@st.cache_data`缓存商品列表與審核規則
2. **異步處理**：商品圖片審核使用`asyncio`背景執行
3. **CDN加速**：靜態資源（法像圖片）存放於阿里雲OSS

---

### **系統預覽效果**
![商城界面](https://example.com/preview.jpg)  
*Material Design 宗教風格界面，包含：*  
- 左側法會通知卡片流  
- 中央商品瀑布流展示  
- 右側快速結緣購物車  
- 頂部紫色系宗教風格導航

此方案結合 Streamlit 的快速開發優勢與 Material Design 的現代化體驗，特別適合宗教團體技術團隊快速迭代，同時維持專業的視覺呈現與流暢的金流操作。
