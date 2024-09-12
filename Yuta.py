# Support ticket with Api Integration
import streamlit as st
import json
import re
import requests
from datetime import datetime

BASE_URL = "http://103.159.239.203:8090/support/tickets"
HEADERS = {
    "Content-Type": "application/json",
    "zoneid": "Asia/Kolkata",
    "userid": "pcsadmin",
    "clinicid" : "pcsadmin"
}

if 'page' not in st.session_state:
    st.session_state.update({'page': 'User Info', 'messages': [], 'ticket_type': None, 'query_type': None, 'module': None, 'altmobile_number': None, 'user_name': None, 'client_name': None, 'comment': None, 'ticket_type_asked': False, 'ticket_type_selected': False, 'query_type_asked': False, 'query_type_selected': False, 'module_asked': False, 'module_selected': False, 'altmobile_number_asked': False, 'client_name_asked': False, 'user_name_asked': False, 'comment_asked': False, 'show_ticket_type_select': False, 'show_query_type_select': False, 'show_module_select': False, 'show_client_select': False, 'show_user_select': False })

CLIENT_NAMES = ["SMARTCARE INSTITUTE OF MEDICAL SCIENCES"]  
USER_NAMES = ["Aureus Hospital"]

def display_message(role, content, timestamp=None):
    if isinstance(content, list): 
        content = " ".join(part["text"] for part in content)
    if role == "assistant":
        st.markdown(f'''
        <div style="display: flex; align-items: flex-start; margin-bottom: 15px; color:black">  
            <div style="background-color: #D8D8D8; padding: 10px; border-radius: 10px;">
                <p style="margin: 0; font-size: 14px; color: #000000;">{content}</p>
                <p style="margin: 0; font-size: 10px; text-align: right; color: #888888;">{timestamp}</p>
            </div>
        </div>''', unsafe_allow_html=True)
    
    elif role == "user":
        st.markdown(f'''
        <div style="display: flex; align-items: flex-end; justify-content: flex-end; margin-bottom: 15px;">
            <div style="background-color: #007BFF; color: white; padding: 10px; border-radius: 10px; text-align: right;">
                <p style="margin: 0; font-size: 14px;">{content}</p>
                <p style="margin: 0; font-size: 10px; text-align: right; color: #DDDDDD;">{timestamp}</p>
            </div>
        </div> ''', unsafe_allow_html=True)
 
def is_altmobile_number(user_input):
    return re.fullmatch(r"[1-9]\d{9}", user_input) is not None

def submit_ticket(ticket_data):

    smartcare_ticket_value = "s" if st.session_state.ticket_type.lower() == "smartcare" else "i"
    payload = {
        "mobilneNumber": ticket_data.get("mobilneNumber"),
        "department": ticket_data.get("department", "Admin"),  
        "altMobilneNumber": ticket_data.get("altMobilneNumber"),
        "moduleName": ticket_data.get("moduleName"),
        "query": ticket_data.get("query"),
        "queryStatus": ticket_data.get("queryStatus", 0), 
        "queryType": ticket_data.get("queryType"),
        "smartcareTicket": smartcare_ticket_value,
        "userName": ticket_data.get("userName")
    }
    response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 201:
        return "Your ticket has been submitted successfully."
    else:
        return "There was an error submitting your ticket. Please try again."

def handle_user_input(user_input):
    normalized_input = user_input.lower()

    if normalized_input in ["hey", "hi", "hello"]:
        if not st.session_state.query_type_asked:
            return "Hello! How can I assist you today? Please type 'okay' to select from the ticket type dropdown."

    if not st.session_state.ticket_type_asked:
        if normalized_input == "okay":
            st.session_state.update({'ticket_type_asked': True, 'show_ticket_type_select': True})
            return "Please select the ticket type from the dropdown."

    if st.session_state.show_ticket_type_select:
        if normalized_input == "okay":
            st.session_state.update({'ticket_type_selected': True, 'show_ticket_type_select': False, 'show_query_type_select': True})
            return "Ticket type selected. Please select the query type from the dropdown."

    if st.session_state.ticket_type_selected and not st.session_state.query_type_asked:
        if normalized_input == "okay":
            st.session_state.update({'query_type_asked': True, 'show_query_type_select': True})
            return "Please select the query type from the dropdown."

    if st.session_state.show_query_type_select and normalized_input == "okay":
        st.session_state.update({'query_type_selected': True, 'show_query_type_select': False, 'show_module_select': True})
        return "Query type selected. Please select the module from the dropdown."

    if st.session_state.query_type_selected and not st.session_state.module_asked:
        if normalized_input == "okay":
            st.session_state.update({'module_asked': True, 'show_module_select': True})
            return f"Query type selected: {st.session_state.query_type}. Please select the module from the dropdown."

    if st.session_state.module_selected and not st.session_state.altmobile_number_asked:
        if normalized_input == "okay":
            st.session_state.update({'module_asked': True, 'show_module_select': False, 'altmobile_number_asked': True})
            return "Module selected. Please provide your alternate mobile number."

    if is_altmobile_number(user_input):
        st.session_state.update({'altmobile_number': user_input, 'altmobile_number_asked': False, 'show_client_select': True})
        return "Alternate Mobile number provided. Please select the client name from the dropdown."

    if st.session_state.show_client_select:
        if normalized_input == "okay":
            st.session_state.update({'client_name_asked': True, 'show_client_select': False, 'show_user_select': True})
            return "Client name selected. Please proceed with selecting the user name."

    if st.session_state.show_user_select:
        if normalized_input == "okay":
            st.session_state.update({'user_name_asked': True, 'show_user_select': False, 'comment_asked': True})
            return "User name selected. Please type your comment."

    if st.session_state.comment_asked:
        
        smartcare_ticket_value = "s" if st.session_state.ticket_type.lower() == "smartcare" else "i"
        ticket_data = {
            "mobilneNumber": "7898655451",
            "department": "Admin",
            "altMobilneNumber": st.session_state.altmobile_number,
            "moduleName": st.session_state.module,
            "query": user_input,
            "queryStatus": 0,
            "queryType": st.session_state.query_type,
            "smartcareTicket": smartcare_ticket_value,
            "userName": st.session_state.user_name
        }

        submission_response = submit_ticket(ticket_data)
        response = f"Your support ticket has been created. We will get back to you shortly.\n\n{submission_response}\n\nNote: Please share your AnyDesk Id or Skype Id.\n"
        response += "Download AnyDesk:\n1) [Windows click here](https://anydesk.com/en/downloads/windows)\n2) [Linux click here](https://anydesk.com/en/downloads/linux)\n3) [macOS click here](https://anydesk.com/en/downloads/mac-os)\n"

        st.session_state.comment_asked = True
        return response

def on_ticket_type_change():
    selected_ticket_type = st.session_state.ticket_type_selectbox
    if selected_ticket_type != "Select Ticket Type":
        st.session_state.ticket_type = selected_ticket_type
        st.session_state.ticket_type_selected = True
        st.session_state.show_ticket_type_select = False
        st.session_state.show_query_type_select = True
        st.session_state.messages.append({"role": "assistant", "content": f"Ticket type selected: {selected_ticket_type}. Please proceed with selecting the query type."})

def on_query_type_change():
    selected_query_type = st.session_state.query_type_selectbox
    if selected_query_type != "Select Query Type":
        st.session_state.query_type = selected_query_type
        st.session_state.query_type_selected = True
        st.session_state.show_query_type_select = False
        st.session_state.show_module_select = True
        st.session_state.messages.append({"role": "assistant", "content": f"Query type selected: {selected_query_type}. Please proceed with selecting the module."})

def on_module_change():
    selected_module = st.session_state.module_selectbox
    if selected_module != "Select Module":
        st.session_state.module = selected_module
        st.session_state.module_selected = True
        st.session_state.show_module_select = False
        st.session_state.altmobile_number_asked = True
        st.session_state.messages.append({"role": "assistant", "content": f"Module selected: {selected_module}. Please provide your mobile number."})
def on_client_name_change():
    selected_client_name = st.session_state.client_name_selectbox
    if selected_client_name != "Select Client Name":
        st.session_state.client_name = selected_client_name
        st.session_state.show_client_select = False
        st.session_state.show_user_select = True
        st.session_state.messages.append({"role": "assistant", "content": f"Client name selected: {selected_client_name}. Please proceed with selecting the user name."})

def on_user_name_change():
    selected_user_name = st.session_state.user_name_selectbox
    if selected_user_name != "Select User Name":
        st.session_state.user_name = selected_user_name
        st.session_state.show_user_select = False
        st.session_state.comment_asked = True
        st.session_state.messages.append({"role": "assistant", "content": f"User name selected: {selected_user_name}. Please type your comment."})

st.title("Support Ticket System")
if st.session_state.page == "User Info":
    st.header("Submit a Support Ticket")
    message = st.chat_input("Enter your message")
    
    if message:
        timestamp = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"role": "user", "content": message, "timestamp": timestamp})
        bot_response = handle_user_input(message)
        st.session_state.messages.append({"role": "assistant", "content": bot_response, "timestamp": timestamp})
    
    for msg in st.session_state.messages:
        display_message(msg['role'], msg['content'], msg.get('timestamp'))

    if st.session_state.show_ticket_type_select:
     st.selectbox("Select Ticket Type", ["Select Ticket Type"] + ["Smartcare", "Internal"], key='ticket_type_selectbox', on_change=on_ticket_type_change)

    if st.session_state.show_query_type_select:
     valid_query_types = ["billing support", "compatibility issue", "data correction", "feedback", "improvement", "performance issue", "report requirement", "user training"]
     st.selectbox("Select Query Type", ["Select Query Type"] + [qt.capitalize() for qt in valid_query_types], key='query_type_selectbox', on_change=on_query_type_change)

    if st.session_state.show_module_select:
     valid_modules = ["accounting", "allocation", "ambulance", "analytics", "appointment finder", "bank deposit", "billing", "blogs", "blood bank", "cath lab", "casualty", "casualty sclyte",  "circular", "circular and protocol", "consultation", "covid", "crm", "daily appointment", "day care", "daycare sclyte", "dietary", "discount", "discharge", "emergency label", "emr", "expense", "housekeeping", "immunization", "immunization form", "indent", "inventory", "ipd", "mis reports", "mrd", "my hr", "my sequence", "opd", "ot", "packages", "pac's", "patient", "payroll", "pharmacy", "prescription", "product barcode", "profile settings", "revenue sharing", "scheduler", "sclyte accounting", "sclyte billing", "sclyte discharge", "sclyte discount", "sclyte investigation", "sclyte inventory", "sclyte ipd", "sclyte ot", "sclyte package", "sclyte patient", "sclyte pharmacy", "sclyte profile", "sclyte refund", "sclyte revenue", "sclyte opd", "setting", "setup master", "sms setting", "support", "training video", "tpa", "vaccination", "video training", "vitals", "voucher", "others"]
     st.selectbox("Select Module", ["Select Module"] + [d.capitalize() for d in valid_modules], key='module_selectbox', on_change=on_module_change)

    if st.session_state.show_client_select:
        st.selectbox("Select Client Name", ["Select Client Name"] + CLIENT_NAMES, key='client_name_selectbox', on_change=on_client_name_change)
    
    if st.session_state.show_user_select:
        st.selectbox("Select User Name", ["Select User Name"] + USER_NAMES, key='user_name_selectbox', on_change=on_user_name_change)