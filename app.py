import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Company configuration
COMPANY_NAME = os.getenv('COMPANY_NAME', 'TechCorp')
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@company.com')

# System prompt for customer support agent
SYSTEM_PROMPT = f"""You are a helpful and professional customer support agent for {COMPANY_NAME}. 

Your responsibilities:
- Answer customer questions clearly and concisely
- Be empathetic and understanding
- Provide step-by-step solutions for technical issues
- Offer product information and guidance
- If you cannot resolve an issue, suggest escalating to a human agent
- Always maintain a friendly, professional tone
- Ask clarifying questions when needed

Important guidelines:
- Never make promises you cannot keep
- Admit when you don't know something
- Always prioritize customer satisfaction
- Keep responses concise but thorough
- Use simple language, avoid jargon

If a customer seems frustrated or the issue is complex, recommend contacting {SUPPORT_EMAIL} for personalized assistance.
"""

# Page configuration
st.set_page_config(
    page_title=f"{COMPANY_NAME} - AI Support",
    page_icon="🎧",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown(f'<div class="main-header">🎧 {COMPANY_NAME} AI Support</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Get instant help from our AI-powered assistant</div>', unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if 'satisfaction_rating' not in st.session_state:
    st.session_state.satisfaction_rating = None

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

# Sidebar
with st.sidebar:
    st.header("📋 Support Options")

    # Quick actions
    st.subheader("Quick Help Topics")
    quick_topics = [
        "Account Issues",
        "Billing Questions",
        "Technical Support",
        "Product Information",
        "Return & Refund"
    ]

    selected_topic = st.selectbox("Select a topic:", [""] + quick_topics)

    if selected_topic and st.button("Start Conversation"):
        prompt = f"I need help with: {selected_topic}"
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.spinner("Getting assistance..."):
            full_prompt = f"{SYSTEM_PROMPT}\n\nCustomer: {prompt}"
            response = model.generate_content(full_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        st.rerun()

    st.markdown("---")

    # Session info
    st.subheader("📊 Session Info")
    st.info(f"**Session ID:** {st.session_state.session_id}")
    st.info(f"**Messages:** {len(st.session_state.chat_history)}")

    # Clear chat
    if st.button("🔄 New Conversation"):
        st.session_state.chat_history = []
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.satisfaction_rating = None
        st.rerun()

    st.markdown("---")

    # Contact information
    st.subheader("📞 Need More Help?")
    st.write(f"**Email:** {SUPPORT_EMAIL}")
    st.write("**Hours:** Mon-Fri, 9AM-6PM")

    # Export chat
    if len(st.session_state.chat_history) > 0:
        st.markdown("---")
        chat_export = f"Support Chat - {st.session_state.session_id}\n\n"
        for msg in st.session_state.chat_history:
            role = "Customer" if msg["role"] == "user" else "Agent"
            chat_export += f"{role}: {msg['content']}\n\n"

        st.download_button(
            label="📥 Export Conversation",
            data=chat_export,
            file_name=f"support_chat_{st.session_state.session_id}.txt",
            mime="text/plain"
        )

# Main chat area
st.markdown("---")

# Display welcome message if no chat history
if len(st.session_state.chat_history) == 0:
    st.markdown(f"""
    <div class="status-box info-box">
        <h4>👋 Welcome to {COMPANY_NAME} Support!</h4>
        <p>I'm your AI assistant, here to help you with:</p>
        <ul>
            <li>Account and billing questions</li>
            <li>Technical troubleshooting</li>
            <li>Product information and recommendations</li>
            <li>Order status and shipping</li>
            <li>Returns and refunds</li>
        </ul>
        <p><strong>How can I help you today?</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Build conversation context
            conversation_context = SYSTEM_PROMPT + "\n\nConversation history:\n"
            for msg in st.session_state.chat_history[-6:]:  # Last 3 exchanges
                role = "Customer" if msg["role"] == "user" else "Support Agent"
                conversation_context += f"{role}: {msg['content']}\n"

            try:
                response = model.generate_content(conversation_context)
                response_text = response.text

                # Add assistant message
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                st.write(response_text)

            except Exception as e:
                error_msg = f"I apologize, but I'm experiencing technical difficulties. Please try again or contact {SUPPORT_EMAIL} for immediate assistance."
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

# Satisfaction survey (after 4+ messages)
if len(st.session_state.chat_history) >= 4 and st.session_state.satisfaction_rating is None:
    st.markdown("---")
    st.subheader("📊 How satisfied are you with the support?")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("😞 Very Unsatisfied"):
            st.session_state.satisfaction_rating = 1
            st.rerun()
    with col2:
        if st.button("😕 Unsatisfied"):
            st.session_state.satisfaction_rating = 2
            st.rerun()
    with col3:
        if st.button("😐 Neutral"):
            st.session_state.satisfaction_rating = 3
            st.rerun()
    with col4:
        if st.button("🙂 Satisfied"):
            st.session_state.satisfaction_rating = 4
            st.rerun()
    with col5:
        if st.button("😄 Very Satisfied"):
            st.session_state.satisfaction_rating = 5
            st.rerun()

# Show thank you message after rating
if st.session_state.satisfaction_rating is not None:
    st.markdown(f"""
    <div class="status-box success-box">
        <strong>Thank you for your feedback!</strong> Your rating helps us improve our service.
    </div>
    """, unsafe_allow_html=True)