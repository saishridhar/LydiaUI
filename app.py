from openai import OpenAI
from anthropic import Anthropic
import streamlit as st
from dotenv import load_dotenv
import shelve
from setup_api import process_model
from pricing_estimation import get_price


load_dotenv()

st.set_page_config(page_title="Lydia - AI Assistant", page_icon="👋")
st.title("👋 Lydia")


# Load chat history from shelve file
def load_chat_history():
    with shelve.open("history/chat_history") as db:
        return db.get("messages", [])


# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("history/chat_history") as db:
        db["messages"] = messages

def load_spending():
    with shelve.open("expenditure/costs") as db:
        return db.get("spending",[])
    

def save_spending(spending):
    with shelve.open("expenditure/costs") as db:
        db["spending"] = spending
    pass
# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if "spending" not in st.session_state:
    try:
        st.session_state.spending = load_spending()
        if st.session_state.spending == []:
            st.session_state.spending = [{"openai":0.0,"anthropic":0.0,"together":0.0, "total":0.0}]
    except:
        st.session_state.spending = [{"openai":0.0,"anthropic":0.0,"together":0.0}]

if 'show_info' not in st.session_state:
    st.session_state.show_info = False 

# Sidebar with a button to delete chat history
with st.sidebar:

    option = st.selectbox(
    'Model:',
    ('Qwen1.5-2B','Openchat-7B','Qwen1.5-72B', 'Codellama-70B','GPT-4','Opus'))

    process_model(option,st.session_state)
    

    st.session_state["temperature"] = st.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step = 0.01)

    st.session_state["max_tokens"] = st.slider('Max Output Tokens:', min_value = 0, max_value=4096, value=512, step = 1)

    st.session_state["sys_prompt"] = st.sidebar.text_input("System Prompt:")

    if st.session_state["sys_prompt"] == "":
        st.session_state["sys_prompt"] = "You are a Helpful AI Assistant."

    try:
        st.session_state.messages[0] = {"role": "system", "content": st.session_state["sys_prompt"]}
    except:
        st.session_state.messages.append({"role": "system", "content": st.session_state["sys_prompt"]})

    spacer_height = 10  # Adjust the height as needed to push content to the bottom
    st.sidebar.markdown(f'<div style="margin-top: {spacer_height}px;">&nbsp;</div>', unsafe_allow_html=True)
    st.session_state.spending[0]['total'] = st.session_state.spending[0]['together']+st.session_state.spending[0]['openai']+st.session_state.spending[0]['anthropic']
    st.sidebar.write(f"Usage: {st.session_state.spending[0]['total']:4f}")
    # Now display your content, attempting to position it towards the bottom
    if st.sidebar.button('Details'):
        st.session_state.show_info = not st.session_state.show_info
        if st.session_state.show_info:
            st.sidebar.write(f"Together API: {st.session_state.spending[0]['together']:4f}")
            st.sidebar.write(f"OpenAI API: {st.session_state.spending[0]['openai']:4f}")
            st.sidebar.write(f"Anthropic API: {st.session_state.spending[0]['anthropic']:4f}")
        else:
            st.sidebar.write("")
    
    spacer_height = 0  # Adjust the height as needed to push content to the bottom
    st.sidebar.markdown(f'<div style="margin-top: {spacer_height}px;">&nbsp;</div>', unsafe_allow_html=True)

    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])
    
    if st.button("Reset spending"):
        st.session_state.spending = [{"openai":0.0,"anthropic":0.0,"together":0.0, "total":0.0}]
        save_spending(st.session_state.spending)




if st.session_state["api_type"] == "openai" or st.session_state["api_type"] == "together":
    client = OpenAI(base_url=st.session_state["api_base"],api_key=st.session_state["api_key"])
if st.session_state["api_type"] == "anthropic":
    client = Anthropic(api_key=st.session_state["api_key"])


# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("Message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.spending[0][st.session_state['api_type']] += get_price(st.session_state['api_type'],prompt,"input",model=st.session_state['model'])
    

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if st.session_state["api_type"] == "openai" or st.session_state["api_type"] == "together" :
            for response in client.chat.completions.create(
                model=st.session_state["model"],
                messages=st.session_state["messages"],
                max_tokens = st.session_state["max_tokens"],
                temperature = st.session_state["temperature"],
                stream=True
                
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "|")
            
        else:
            try:
                with client.messages.stream(
                    max_tokens=1024,
                    messages=[{"role": "user", "content": "Hello"}],
                    model="claude-3-opus-20240229",
                    temperature = 0.7
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text or ""
                        message_placeholder.markdown(full_response + "|")
            except:
                full_response = "I'm sorry but the API is down right now"

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.spending[0][st.session_state['api_type']] += get_price(st.session_state['api_type'],prompt,"output",model=st.session_state['model'])




# Save chat history after each interaction
save_chat_history(st.session_state.messages)
save_spending(st.session_state.spending)


