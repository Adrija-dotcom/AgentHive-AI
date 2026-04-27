import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from duckduckgo_search import DDGS

# 1. SECURITY & CONFIGURATION
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Using the stable Flash model to avoid quota errors
# Try this EXACT string
# Copy this EXACTLY
model = genai.GenerativeModel('models/gemini-3.1-flash-lite-preview')

# 2. TOOL DEFINITION: WEB SEARCH
def web_search(query):
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
        return "\n".join(results)

# 3. AGENTIC WORKFLOW LOGIC
def run_agenthive(user_goal):
    log = []
    
    # Phase 1: Research
    st.write("🔍 **Phase 1: Researching the web...**")
    search_data = web_search(user_goal)
    log.append(f"Research Data: {search_data[:200]}...")

    # Phase 2: Internal Debate
    st.write("⚖️ **Phase 2: Simulating internal debate...**")
    debate_prompt = f"""
    Goal: {user_goal}
    Research: {search_data}
    Simulate a debate between 'The Optimist' and 'The Risk Auditor'. 
    Summarize the pros and cons clearly.
    """
    debate_response = model.generate_content(debate_prompt).text
    log.append("Debate completed.")

    # Phase 3: Final Analysis & Plan
    st.write("🧠 **Phase 3: Finalizing strategic roadmap...**")
    analysis_prompt = f"""
    Based on this debate: {debate_response}
    Create a 30-day tactical execution plan for the goal: {user_goal}.
    Include 3 immediate action items.
    """
    final_plan = model.generate_content(analysis_prompt).text
    
    return final_plan, log

# 4. STREAMLIT UI
st.set_page_config(page_title="AgentHive-AI Agent", page_icon="🤖")

st.title("🤖 AgentHive: The Multi-Tasking Decision Agent")
st.markdown("---")

user_input = st.text_input("Enter a complex decision or goal:", 
                          placeholder="e.g. Feasibility of a cybersecurity startup in Kolkata")

if st.button("Activate AgentHive Agent"):
    if user_input:
        with st.status("Agent is thinking...", expanded=True) as status:
            decision, logs = run_agenthive(user_input)
            status.update(label="Decision Process Complete!", state="complete", expanded=False)
        
        st.success("### 🏁 Final Strategic Roadmap")
        st.markdown(decision)
        
        with st.expander("See Agent Reasoning Logs"):
            st.write(logs)
    else:
        st.warning("Please enter a goal first!")