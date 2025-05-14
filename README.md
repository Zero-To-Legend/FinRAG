💬 FinRAG — AI-Powered Financial Assistant

FinRAG (Financial Retrieval-Augmented Generation) is a full-stack AI chatbot application designed to help users make smarter financial decisions using real-time data and open financial knowledge, with a special focus on Edmonton, Canada.

This project includes:

- ⚙️ FastAPI backend for AI-powered financial responses
- 🌐 React + Vite frontend styled with Tailwind CSS
- 🧠 OpenAI GPT integration (via .env)

---

🚀 Features

- 🧾 Chat with an AI trained on financial concepts like stocks, real estate, RRSPs, inflation, and more.
- 🌐 Edmonton-specific financial data including real estate trends and tax surveys.
- 📊 Modular components (Investment Tracker, Market Stats, Property Assessment Insights, etc.)
- ✨ Fully responsive UI built with React, Vite, and TailwindCSS.
- 🔐 Environment-based OpenAI API key configuration.

---

📁 Project Structure

```
FINANCE_CHATBOT/
├── env/                         # Environment-related scripts/configs
├── react-frontend/              # React + TailwindCSS frontend
│   ├── node_modules/            # Node.js dependencies
│   ├── public/                  # Static assets
│   ├── src/                     # Frontend source code (components, pages, etc.)
│   ├── index.html               # Main HTML template
│   ├── package.json             # NPM project metadata
│   ├── tailwind.config.js       # TailwindCSS config
│   └── vite.config.js           # Vite config
├── .env                         # Environment variables file (Add your OpenAI API key here)
├── apikey.txt                   # (Optional) Backup API key file
├── backend.py                   # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── test-frontend.py             # Frontend UI test (Streamlit-based)
├── metrics.py                   # Evaluation or logging utilities
├── info.txt                     # Project description or notes
├── chatbot_eval_results.csv     # Sample chatbot evaluation data
└── README.md                    # You're reading it!
```

---

⚙️ Setup Instructions

1. 🔑 Backend Setup (FastAPI)

> Ensure Python 3.9+ is installed

# Create and activate virtual environment

python -m venv env
source env/bin/activate # For Windows use `env\Scripts\activate`

# Install dependencies

pip install -r requirements.txt

🔐 Configure OpenAI API Key

Create a .env file in the project root with the following content:

OPENAI_API_KEY=your_openai_key_here

🚀 Run the API server

uvicorn backend:app --reload

FastAPI will run at: http://127.0.0.1:8000

---

2. 🌐 Frontend Setup (React + Vite)

> Navigate to the frontend directory

cd react-frontend
npm install
npm run dev

Frontend will be live at: http://localhost:5173

---

🧠 API Flow

- User interacts with the chatbot via frontend UI
- Query sent to FastAPI /chat/ endpoint
- GPT processes the query using RAG context + real-time data
- Answer is streamed back and rendered on screen with typing animation

---

📌 Environment Configuration

| File             | Description                     |
| ---------------- | ------------------------------- |
| .env             | API key for OpenAI              |
| apikey.txt       | Optional raw API key store      |
| requirements.txt | All Python packages for backend |

---

👥 Authors

- Ruban Gino Singh Arul Peppin Raj (1665680)
- Raja Priya Mariappan (1865511)
- Raju Bhattarai (1884382)

Project submitted as part of MM802 Multimedia Communications.

---

📝 License

This project is for educational and academic use only.
Contact contributors for commercial or research collaboration.

```

```
