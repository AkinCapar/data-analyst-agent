import streamlit as st
from langchain_core.messages import HumanMessage
from data_analyst_agent.client.graph import app
import os
import time
import shutil
        

st.set_page_config(page_title="Data Analyst AI", page_icon="📊", layout="wide")

st.title("AI Data Analyst Agent")
st.markdown("Ask me anything about your Superstore sales database! I can write SQL, analyze data, and remember our conversation.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("image"):
            st.image(message["image"])


if prompt := st.chat_input("E.g., What are the top 3 best-selling product categories?"):
    
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    config = {"configurable": {"thread_id": "demo_user_1"}}

    with st.chat_message("assistant"):
        
        with st.status("🧠 Agent is thinking and working...", expanded=True) as status:
            input_message = HumanMessage(content=prompt)
            
            final_response = ""
            
            for event in app.stream({"messages": [input_message]}, config=config, stream_mode="updates"):
                for node_name, node_output in event.items():
                    st.write(f"**Node executed:** `{node_name}`")
                    
                    messages = node_output.get("messages", [])
                    if messages:
                        latest_message = messages[-1]
                        
                        if latest_message.type == "ai" and latest_message.tool_calls:
                            for tool_call in latest_message.tool_calls:
                                st.write(f"🛠️ **Tool invoked:** `{tool_call['name']}`")
                                st.write(f"📥 **Arguments:** `{tool_call['args']}`")
                                
                        elif latest_message.type == "tool":
                            st.write(f"✅ **Tool completed.** Result fetched from database.")
                        
                        elif latest_message.type == "ai" and not latest_message.tool_calls:
                            final_response = latest_message.content
                            
            status.update(label="Analysis complete!", state="complete", expanded=False)

        
        st.markdown(final_response)
        
        image_to_save = None
        chart_path = "output/latest_chart.png"
        
        if os.path.exists(chart_path):
            unique_name = f"output/chart_{int(time.time())}.png"
            shutil.move(chart_path, unique_name)
            image_to_save = unique_name
            
            st.image(image_to_save)
        
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": final_response,
            "image": image_to_save  
        })
        