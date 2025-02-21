from streamlit import sidebar, session_state, radio as stRadio, columns as stCLMN, text_area, text_input, multiselect, tabs as stTAB, expander, secrets, metric, form_submit_button, error, success, rerun, dataframe
from streamlit import toggle as stToggle, markdown as stMarkdown, set_page_config as pageConfig, subheader, container, form as stForm, selectbox #slider, dataframe, code as stCode, cache as stCache,
from streamlit.components.v1.components import html as stHtml
from stUtil import rndrCode
from pandas import read_csv, DataFrame
from json import dumps as jsnDumps
from uuid import uuid4

# 初始化數據存儲
if "appointments" not in session_state:
    try:
        df = read_csv("massage_bookings.csv")
        session_state.appointments = df.to_dict("records")
    except FileNotFoundError:
        session_state.appointments = []

# MUI 日歷組件
def mui_calendar(events, key):
    stHtml(
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
                    events: {jsnDumps(events)},
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
pageConfig(page_title="按摩預約系統", layout="wide")

stMarkdown("""
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
</style> """, unsafe_allow_html=True)

stTitle("💆 按摩預約系統") # 主頁面布局

selected_date = date.today() # 日歷事件處理
selected_event = None

# 處理來自Calendar的消息
def handle_calendar_messages():
    if 'messages' in session_state:
        for msg in session_state.messages:
            if msg['type'] == 'DATE_SELECT':
                global selected_date
                selected_date = datetime.fromisoformat(msg['date']).date()
            elif msg['type'] == 'EVENT_SELECT':
                global selected_event
                selected_event = next(
                    (e for e in session_state.appointments if e['id'] == msg['eventId']),
                    None
                )
        del session_state.messages

stHtml(
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

from datetime import datetime, timedelta, date
# 生成可用時間段
def generate_time_slots(date):
    base_date = datetime.combine(date, datetime.time(9, 0))
    return [
        (base_date + timedelta(minutes=30*i)).strftime("%H:%M")
        for i in range(22)  # 從9:00到20:00
    ]

# 主界面
左, 右=stCLMN([3, 1])

with 左:
    # 轉換事件格式
    calendar_events = [{
        "id": appt["id"],
        "title": f"{appt['type']} - {appt['name']}",
        "start": f"{appt['date']}T{appt['start_time']}",
        "end": f"{apppt['date']}T{appt['end_time']}",
        "color": "#ff6b6b" if "深層" in appt["type"] else "#4ecdc4"
    } for appt in session_state.appointments]

    mui_calendar(calendar_events, "main_calendar")
    handle_calendar_messages()

with 右:
    with container():
        stMarkdown('<div class="booking-card">', unsafe_allow_html=True)

        # 預約表單
        with stForm("booking_form"):
            subheader("新建預約")

            # 服務類型選擇
            massage_type = selectbox(
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
                    for appt in session_state.appointments
                )
            ]

            start_time = selectbox(
                "開始時間",
                options=available_slots,
                format_func=lambda x: datetime.strptime(x, "%H:%M").strftime("%H:%M"),
                disabled=not available_slots
            )
            # 客戶信息
            name = text_input("姓名")
            phone = text_input("聯系電話")
            notes = text_area("特別要求")

            submitted = form_submit_button("立即預約")

            if submitted:
                if not all([name, phone]):
                    error("請填寫姓名和聯系電話")
                else:
                    start_dt = datetime.datetime.strptime(f"{selected_date} {start_time}", "%Y-%m-%d %H:%M")
                    end_dt = start_dt + datetime.timedelta(minutes=duration)

                    new_appointment = {
                        "id": str(uuid4()),
                        "date": selected_date.isoformat(),
                        "start_time": start_time,
                        "end_time": end_dt.strftime("%H:%M"),
                        "type": massage_type,
                        "name": name,
                        "phone": phone,
                        "notes": notes,
                        "status": "已預約"
                    }

                    session_state.appointments.append(new_appointment)
                    pd.DataFrame(session_state.appointments).to_csv("massage_bookings.csv", index=False)
                    success("預約成功！")
                    rerun()

        stMarkdown('</div>', unsafe_allow_html=True)

# 預約詳情側邊欄
if selected_event:
    with sidebar
      expander("預約詳情", expanded=True):
      rndrCode(f"**客戶姓名**: {selected_event['name']}")
      rndrCode(f"**聯系電話**: {selected_event['phone']}")
      rndrCode(f"**預約時間**: {selected_event['date']} {selected_event['start_time']}-{selected_event['end_time']}")
      rndrCode(f"**服務類型**: {selected_event['type']}")
      rndrCode(f"**特別要求**: {selected_event['notes']}")

      if button("取消預約"):
          session_state.appointments = [a for a in session_state.appointments if a['id'] != selected_event['id']]
          pd.DataFrame(session_state.appointments).to_csv("massage_bookings.csv", index=False)
          rerun()

# 數據顯示
with expander("所有預約數據"):
    dataframe(DataFrame(session_state.appointments))
from twilio.rest import Client

def send_sms_confirmation(phone, appointment):
    account_sid = secrets["TWILIO_SID"]
    auth_token = secrets["TWILIO_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"""
        {appointment['name']} 您好！
        您的{appointment['type']}預約已确認
        時間：{appointment['date']} {appointment['start_time']}-{appointment['end_time']}
        """,
        from_=secrets["TWILIO_NUMBER"],
        to=phone
    )
import schedule
import time

def check_reminders():
    now = datetime.now()
    for appt in session_state.appointments:
        appt_time = datetime.fromisoformat(f"{appt['date']}T{appt['start_time']}")
        if (appt_time - now).total_seconds() < 3600:  # 1小時前提醒
            send_sms_reminder(appt['phone'], appt)

# 在後台線程運行
import threading
thread = threading.Thread(target=schedule.every(5).minutes.do(check_reminders))
thread.start()
# 添加密碼保護的管理頁面
if secrets.get("ADMIN_PASSWORD"):
    with expander("管理面板", expanded=False):
        admin_pass = text_input("管理員密碼", type="password")
        if admin_pass == secrets["ADMIN_PASSWORD"]:
            rndrCode("當日預約：")
            today_appts = [a for a in session_state.appointments if a['date'] == date.today().isoformat()]
            dataframe(pd.DataFrame(today_appts))

            rndrCode("收入統計：")
            revenue = sum(
                300 if "60分鍾" in a['type'] else
                450 if "90分鍾" in a['type'] else
                380 for a in session_state.appointments
            )
            metric("本月總收入", f"¥{revenue}")
