# AI-Powered Customer Support System (Streamlit + Gemini API)
A modern AI-driven customer support application built with Streamlit and Google Generative AI (Gemini).  
This app responds to customer queries, understands context, and behaves like a real support agent — with your company’s name & email automatically inserted.

---

## 📌 Table of Contents
- Features
- Demo Screenshot
- Tech Stack
- Project Structure
- Installation
- Environment Variables
- How to Run
- How It Works
- Use Cases
- Future Enhancements
- Contributing
- License
- Author

---

## 🚀 Features
- AI customer support using Google Gemini
- Company branding with dynamic name & email from `.env`
- Clean and modern Streamlit chat UI
- Secure configuration via environment variables

---

## 🖼️ Demo Screenshot
![App Screenshot](https://github.com/Harshpreet09/AI-Support_Chatbot/blob/main/Screenshot%202025-11-13%20235424.png)

---

## 🧩 Tech Stack
- Python
- Streamlit
- Google Generative AI (Gemini)
- dotenv
- datetime

---

## 📂 Project Structure
```
project/
│
├── app.py                # Main Streamlit application
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```


---

## ⚙️ Installation

## Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

## Install dependencies
pip install -r requirements.txt

---

## 🔐 Environment Variables

## Create a .env file in the root directory
GOOGLE_API_KEY=your_google_api_key_here
COMPANY_NAME=YourCompanyName
SUPPORT_EMAIL=support@yourcompany.com

---

## ▶️ How to Run

## Start the Streamlit app
streamlit run app.py

## Open in browser:
http://localhost:8501

---

## 🤖 How It Works
1. User enters a message.
2. System + user prompt sent to Gemini API.
3. Gemini generates support-style response.
4. Company name & email inserted automatically.
5. UI displays chat-like conversation.

---

## 💡 Use Cases
- Customer support automation  
- FAQs chatbot  
- Helpdesk for businesses  
- Dashboard assistant  
- Product inquiry AI  

---

## 🚀 Future Enhancements
- Save chat history  
- Add roles (admin, support agent)  
- Themes for dark/light mode  
- Integration with websites via API  

---

## 🤝 Contributing
1. Fork the repo  
2. Create a new branch  
3. Commit changes  
4. Open a pull request  

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 👨‍💻 Author
**Harsh Preet Singh**  
Developer & Creator
