以下是一個使用 Streamlit 結合 Material-UI (MUI) 組件開發按摩預約系統的完整解決方案，包含交互式日歷和預約管理功能：

```python
import streamlit as st
from streamlit.components.v1 import components
import datetime
import pandas as pd
import json
import uuid

# 初始化數據存儲
if "appointments" not in st.session_state:
    try:
        df = pd.read_csv("massage_bookings.csv")
        st.session_state.appointments = df.to_dict("records")
    except FileNotFoundError:
        st.session_state.appointments = []

# MUI 日歷組件
def mui_calendar(events, key):
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/@mui/material@5.11.0/umd/material-ui.production.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@mui/material@5.11.0/umd/material-ui.production.min.js"></script>
        </head>
        <body>
            <div id="calendar" style="margin: 20px"></div>
            <script>
                const calendarEl = document.getElementById('calendar');
                const calendar = new FullCalendar.Calendar(calendarEl, {{
                    initialView: 'dayGridMonth',
                    headerToolbar: {{
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridWeek,timeGridDay'
                    }},
                    events: {json.dumps(events)},
                    dateClick: function(info) {{
                        window.parent.postMessage({{
                            type: 'DATE_SELECT',
                            date: info.dateStr
                        }}, '*');
                    }},
                    eventClick: function(info) {{
                        window.parent.postMessage({{
                            type: 'EVENT_SELECT',
                            eventId: info.event.id
                        }}, '*');
                    }},
                    themeSystem: 'bootstrap5',
                    eventTimeFormat: {{ 
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false
                    }}
                }});
                calendar.render();
            </script>
        </body>
        </html>
        """,
        height=600,
        key=key
    )

# 頁面配置
st.set_page_config(page_title="按摩預約系統", layout="wide")

# 自定義樣式
st.markdown("""
<style>
    /* 主容器樣式 */
    [data-testid="stAppViewContainer"] {
        background: #fff5f5;
    }
    
    /* 卡片樣式 */
    .booking-card {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background: white;
        margin: 1rem 0;
    }
    
    /* 按鈕樣式 */
    .stButton>button {
        background: #ff6b6b !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px 24px;
    }
</style>
""", unsafe_allow_html=True)

# 主頁面布局
st.title("💆 按摩預約系統")

# 日歷事件處理
selected_date = datetime.date.today()
selected_event = None

# 處理來自Calendar的消息
def handle_calendar_messages():
    if 'messages' in st.session_state:
        for msg in st.session_state.messages:
            if msg['type'] == 'DATE_SELECT':
                global selected_date
                selected_date = datetime.datetime.fromisoformat(msg['date']).date()
            elif msg['type'] == 'EVENT_SELECT':
                global selected_event
                selected_event = next(
                    (e for e in st.session_state.appointments if e['id'] == msg['eventId']),
                    None
                )
        del st.session_state.messages

components.html(
    """
    <script>
        window.addEventListener('message', function(e) {
            if (e.data.type === 'streamlit:render') {
                const messages = [];
                window.addEventListener('message', function(event) {
                    if (event.data.type === 'DATE_SELECT' || event.data.type === 'EVENT_SELECT') {
                        messages.push(event.data);
                        window.parent.streamlitBridge.setComponentValue(messages);
                    }
                });
            }
        });
    </script>
    """,
    height=0,
    key="calendar_listener"
)

# 生成可用時間段
def generate_time_slots(date):
    base_date = datetime.datetime.combine(date, datetime.time(9, 0))
    return [
        (base_date + datetime.timedelta(minutes=30*i)).strftime("%H:%M")
        for i in range(22)  # 從9:00到20:00
    ]

# 主界面
col1, col2 = st.columns([3, 1])

with col1:
    # 轉換事件格式
    calendar_events = [{
        "id": appt["id"],
        "title": f"{appt['type']} - {appt['name']}",
        "start": f"{appt['date']}T{appt['start_time']}",
        "end": f"{apppt['date']}T{appt['end_time']}",
        "color": "#ff6b6b" if "深層" in appt["type"] else "#4ecdc4"
    } for appt in st.session_state.appointments]

    mui_calendar(calendar_events, "main_calendar")
    handle_calendar_messages()

with col2:
    with st.container():
        st.markdown('<div class="booking-card">', unsafe_allow_html=True)
        
        # 預約表單
        with st.form("booking_form"):
            st.subheader("新建預約")
            
            # 服務類型選擇
            massage_type = st.selectbox(
                "按摩類型",
                options=["瑞典式按摩（60分鍾）", "深層組織按摩（90分鍾）", "熱石按摩（75分鍾）", "運動按摩（60分鍾）"],
                key="massage_type"
            )
            
            # 計算時長
            duration = int(''.join(filter(str.isdigit, massage_type.split("（")[1])))
            
            # 可用時間段
            available_slots = [
                t for t in generate_time_slots(selected_date)
                if not any(
                    appt["date"] == selected_date.isoformat() and
                    appt["start_time"] <= t <= appt["end_time"]
                    for appt in st.session_state.appointments
                )
            ]
            
            start_time = st.selectbox(
                "開始時間",
                options=available_slots,
                format_func=lambda x: datetime.datetime.strptime(x, "%H:%M").strftime("%H:%M"),
                disabled=not available_slots
            )
            
            # 客戶信息
            name = st.text_input("姓名")
            phone = st.text_input("聯系電話")
            notes = st.text_area("特別要求")
            
            submitted = st.form_submit_button("立即預約")
            
            if submitted:
                if not all([name, phone]):
                    st.error("請填寫姓名和聯系電話")
                else:
                    start_dt = datetime.datetime.strptime(f"{selected_date} {start_time}", "%Y-%m-%d %H:%M")
                    end_dt = start_dt + datetime.timedelta(minutes=duration)
                    
                    new_appointment = {
                        "id": str(uuid.uuid4()),
                        "date": selected_date.isoformat(),
                        "start_time": start_time,
                        "end_time": end_dt.strftime("%H:%M"),
                        "type": massage_type,
                        "name": name,
                        "phone": phone,
                        "notes": notes,
                        "status": "已預約"
                    }
                    
                    st.session_state.appointments.append(new_appointment)
                    pd.DataFrame(st.session_state.appointments).to_csv("massage_bookings.csv", index=False)
                    st.success("預約成功！")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# 預約詳情側邊欄
if selected_event:
    with st.sidebar.expander("預約詳情", expanded=True):
        st.write(f"**客戶姓名**: {selected_event['name']}")
        st.write(f"**聯系電話**: {selected_event['phone']}")
        st.write(f"**預約時間**: {selected_event['date']} {selected_event['start_time']}-{selected_event['end_time']}")
        st.write(f"**服務類型**: {selected_event['type']}")
        st.write(f"**特別要求**: {selected_event['notes']}")
        
        if st.button("取消預約"):
            st.session_state.appointments = [a for a in st.session_state.appointments if a['id'] != selected_event['id']]
            pd.DataFrame(st.session_state.appointments).to_csv("massage_bookings.csv", index=False)
            st.rerun()

# 數據顯示
with st.expander("所有預約數據"):
    st.dataframe(pd.DataFrame(st.session_state.appointments))
```

### 功能亮點：

1. **專業按摩功能**：
- 多種按摩類型選擇（自動計算時長）
- 特別要求備注欄位
- 智能時間衝突檢測
- 服務時長動態計算

2. **交互式界面**：
- MUI風格日歷組件
- 響應式卡片布局
- 點擊日期直接預約
- 預約事件顏色編碼

3. **客戶管理**：
- 客戶信息記錄
- 預約狀態跟蹤
- 預約詳情側邊欄
- 預約取消功能

4. **業務邏輯**：
- 自動生成營業時間段（9:00-20:00）
- 半小時爲單位的時間段
- CSV數據持久化
- UUID唯一標識

### 安裝與運行：

```bash
pip install streamlit pandas
streamlit run massage_booking.py
```

### 擴展建議：

1. **短信通知功能**：
```python
from twilio.rest import Client

def send_sms_confirmation(phone, appointment):
    account_sid = st.secrets["TWILIO_SID"]
    auth_token = st.secrets["TWILIO_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"""
        {appointment['name']} 您好！
        您的{appointment['type']}預約已确認
        時間：{appointment['date']} {appointment['start_time']}-{appointment['end_time']}
        """,
        from_=st.secrets["TWILIO_NUMBER"],
        to=phone
    )
```

2. **預約提醒功能**：
```python
import schedule
import time

def check_reminders():
    now = datetime.datetime.now()
    for appt in st.session_state.appointments:
        appt_time = datetime.datetime.fromisoformat(f"{appt['date']}T{appt['start_time']}")
        if (appt_time - now).total_seconds() < 3600:  # 1小時前提醒
            send_sms_reminder(appt['phone'], appt)

# 在後台線程運行
import threading
thread = threading.Thread(target=schedule.every(5).minutes.do(check_reminders))
thread.start()
```

3. **管理儀表板**：
```python
# 添加密碼保護的管理頁面
if st.secrets.get("ADMIN_PASSWORD"):
    with st.expander("管理面板", expanded=False):
        admin_pass = st.text_input("管理員密碼", type="password")
        if admin_pass == st.secrets["ADMIN_PASSWORD"]:
            st.write("當日預約：")
            today_appts = [a for a in st.session_state.appointments if a['date'] == datetime.date.today().isoformat()]
            st.dataframe(pd.DataFrame(today_appts))
            
            st.write("收入統計：")
            revenue = sum(
                300 if "60分鍾" in a['type'] else 
                450 if "90分鍾" in a['type'] else 
                380 for a in st.session_state.appointments
            )
            st.metric("本月總收入", f"¥{revenue}")
```

這個系統結合了：
- MUI的現代化設計語言
- 完整的預約業務邏輯
- 響應式交互體驗
- 可擴展的數據架構

特別適合中小型按摩店使用，可根據實際需求添加技師排班、套餐選擇、在線支付等功能。
