以下是一個使用 `streamlit-material` 結合 Streamlit 開發預約系統的示例代碼，包含日歷選擇和預約管理功能：

```python
import streamlit as st
from streamlit_material import layout, cards
import datetime
import pandas as pd
import time

# 初始化數據存儲（使用CSV文件示例）
try:
    df = pd.read_csv("appointments.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["日期", "時間", "服務類型", "姓名", "郵箱", "電話"])

# 設置頁面布局
layout(key="main_layout")

st.title("📅 在線預約系統")

# 使用streamlit-material的卡片容器
with cards.container():
    # 創建兩列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        # 日期選擇
        st.subheader("選擇預約日期")
        selected_date = st.date_input(
            "請選擇日期",
            min_value=datetime.date.today(),
            format="YYYY/MM/DD"
        )

        # 時間選擇（動態生成時間段）
        st.subheader("選擇時間段")
        time_slots = [
            f"{h:02d}:{m:02d}" 
            for h in range(9, 18) 
            for m in [0, 30]
        ]
        
        # 獲取已預約時間
        booked_times = df[df["日期"] == selected_date.strftime("%Y-%m-%d")]["時間"].tolist()
        available_times = [t for t in time_slots if t not in booked_times]

        selected_time = st.selectbox(
            "可選時間段",
            options=available_times,
            index=0 if available_times else None,
            disabled=not available_times
        )

        if not available_times:
            st.warning("該日期已無可用時段，請選擇其他日期")

    with col2:
        # 服務類型選擇
        st.subheader("服務類型")
        service_type = st.radio(
            "選擇服務類型",
            options=["普通咨詢", "深度診斷", "VIP服務"],
            horizontal=False
        )

        # 用戶信息輸入表單
        with st.form("user_info"):
            st.subheader("填寫個人信息")
            name = st.text_input("姓名", max_chars=20)
            email = st.text_input("郵箱")
            phone = st.text_input("聯系電話")
            
            submitted = st.form_submit_button("提交預約")
            
            if submitted:
                if not all([name, email, phone]):
                    st.error("請填寫所有必填字段")
                else:
                    # 創建新預約記錄
                    new_appointment = pd.DataFrame([{
                        "日期": selected_date.strftime("%Y-%m-%d"),
                        "時間": selected_time,
                        "服務類型": service_type,
                        "姓名": name,
                        "郵箱": email,
                        "電話": phone
                    }])

                    # 更新數據存儲
                    global df
                    df = pd.concat([df, new_appointment], ignore_index=True)
                    df.to_csv("appointments.csv", index=False)
                    
                    st.success("預約成功！")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()

# 顯示當日預約信息
st.subheader(f"{selected_date} 預約情況")
today_appointments = df[df["日期"] == selected_date.strftime("%Y-%m-%d")]
if not today_appointments.empty:
    st.dataframe(
        today_appointments[["時間", "服務類型", "姓名"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("當日暫無預約記錄")

# 自定義CSS樣式
st.markdown("""
<style>
    /* 主容器樣式 */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 卡片陰影效果 */
    .st-emotion-cache-1j9s6t7 {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* 時間選擇器樣式 */
    [data-baseweb="select"] {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)
```

### 功能特點說明：

1. **界面布局**：
- 使用 `streamlit-material` 的卡片容器創建現代化UI
- 響應式兩列布局（左邊選擇時間，右邊填寫信息）
- 自定義漸變背景和陰影效果

2. **核心功能**：
- 動態日期選擇（僅限未來日期）
- 自動生成時間段（09:00-18:00，每半小時）
- 實時顯示已約滿時段
- 服務類型單選
- 個人信息驗證表單

3. **數據管理**：
- 使用CSV文件存儲預約記錄
- 自動過濾已預約時段
- 實時顯示當日預約情況

4. **用戶體驗**：
- 表單提交成功動畫效果
- 輸入驗證提示
- 自動刷新機制
- 移動端友好布局

### 使用說明：

1. 安裝依賴：
```bash
pip install streamlit streamlit-material pandas
```

2. 運行應用：
```bash
streamlit run appointment_system.py
```

3. 擴展建議：
- 將CSV存儲替換爲數據庫（如SQLite/PostgreSQL）
- 添加郵件通知功能
- 增加預約修改/取消功能
- 集成用戶身份驗證
- 添加管理員查看界面

這個示例結合了 `streamlit-material` 的現代化UI組件和Streamlit的原生功能，實現了一個基礎的預約系統。實際部署時建議根據具體需求增加數據驗證、安全防護和持久化存儲等功能。
