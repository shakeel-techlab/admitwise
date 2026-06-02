
# AdmitWise — Pakistan University Admission Portal

A full Python + Streamlit web app for managing university admissions, entry tests, and admission guidelines for Pakistani universities.

## Features

- **Admission Predictor** — Enter Matric & FSc marks + entry test score, get instant admission probability across 15+ universities
- **University Directory** — Browse universities with detailed admission criteria, merit formulas, fees, deadlines
- **Scholarships** — HEC, PEEF, Ehsaas, university-specific scholarships with eligibility
- **Location Finder** — Find nearest universities to your city using distance calculation
- **AI Advisor** — ChatGPT-powered counselor for personalized admission guidance
- **Login / Sign Up** — Create an account to save universities and track applications
- **Compare** — Side-by-side comparison of up to 3 universities

## How to Run in VS Code

### 1. Install dependencies

Make sure Python 3.8+ is installed. Then:

```bash
cd admitwise
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

### 3. (Optional) Enable AI Chatbot

To use the AI Advisor chatbot, set your OpenAI API key as an environment variable:

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your_key_here
streamlit run app.py
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_key_here"
streamlit run app.py
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY=your_key_here
streamlit run app.py
```

Or create a `.env` file in the `admitwise/` folder:
```
OPENAI_API_KEY=your_key_here
```

## Project Structure

```
admitwise/
├── app.py                    ← Main home page
├── requirements.txt          ← Python dependencies
├── .streamlit/
│   └── config.toml           ← Streamlit configuration
├── data/
│   └── universities.py       ← University + scholarship database
├── utils/
│   ├── predictor.py          ← Merit calculation logic
│   ├── auth.py               ← Login/signup system
│   └── ai_chat.py            ← AI chatbot integration
└── pages/
    ├── 1_Admission_Predictor.py
    ├── 2_Universities.py
    ├── 3_Scholarships.py
    ├── 4_Location_Finder.py
    ├── 5_AI_Chatbot.py
    ├── 6_Login.py
    └── 7_Compare.py
```

## Universities Included

NUST, LUMS, University of Punjab, UET Lahore, FAST-NUCES, Aga Khan University,
COMSATS, GIKI, University of Karachi, Bahria University, NED University,
UET Peshawar, Iqra University, UCP, PMAS-AAUR

## Notes

- User accounts are stored locally in `data/users.json`
- All predictions are estimates based on historical merit data
- Deadlines and fees are for 2025 admissions — check official university websites for latest info
