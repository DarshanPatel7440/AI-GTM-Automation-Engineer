# 🎥 VideoSDK AI SDR — Automated Outbound Workflow

> An AI-powered Sales Development Representative (SDR) that discovers target companies, researches them, segments them, and generates personalized cold emails + LinkedIn DMs — all live, in one click.

Built for **VideoSDK.live** — a real-time video/audio/streaming SDK for developers.

---

## 🚀 What It Does

| Step | What Happens |
|------|-------------|
| 1 | You enter your API key |
| 2 | AI discovers 10 fresh target companies across verticals (EdTech, Telehealth, HR Tech, FinTech, etc.) |
| 3 | You click **Generate →** on any company |
| 4 | AI researches the company, segments it (SMB / Mid-Market / Enterprise), identifies the VideoSDK use case, writes a personalized cold email + LinkedIn DM, and estimates pipeline value |
| 5 | All results accumulate in a live pipeline dashboard at the bottom |
| 6 | Export the full pipeline as JSON with one click |

---

## 🖥️ Demo Preview

```
┌─────────────────────────────────────────────────────────┐
│  🎥 VideoSDK AI SDR                                      │
│  AI-powered outbound workflow · Research · Segment · ... │
├──────────────────────┬──────────────────────────────────┤
│  🏢 Target Companies │  📊 SDR Report: Classplus         │
│                      │                                   │
│  Classplus    →  Btn │  Priority: 8/10  |  $1,200/mo    │
│  Practo       →  Btn │  Segment: 🟢 SMB                  │
│  Keka HR      →  Btn │                                   │
│  Discord      →  Btn │  Use Case: Live interactive ...   │
│  Cult.fit     →  Btn │  Pain Points: → WebRTC cost ...   │
│  ...          →  Btn │                                   │
│                      │  📧 Cold Email                    │
│  🔄 Regenerate       │  💼 LinkedIn DM                   │
└──────────────────────┴──────────────────────────────────┘
│  📊 Pipeline Summary                                     │
│  Companies: 5 | SMB: 2 | Mid-Market: 2 | Enterprise: 1  │
│  Pipeline Value: $24,500/mo                              │
│  [ Full sortable table with progress bars ]              │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.8+** | Runtime |
| **Streamlit** | UI framework |
| **Groq API** | LLM inference (free, fast) |
| **LLaMA 3.3 70B** | AI model via Groq |
| **OpenAI SDK** | API client (pointed at Groq) |
| **Pandas** | Pipeline table rendering |

---

## ⚙️ Setup Instructions

### Step 1 — Clone or Download

```bash
# Option A: if you have git
git clone https://github.com/yourusername/videosdk-ai-sdr.git
cd videosdk-ai-sdr

# Option B: just place app.py in any folder
mkdir videosdk-ai-sdr
cd videosdk-ai-sdr
# paste app.py here
```

---

### Step 2 — Python Version Check

```bash
python --version
# Must be 3.8 or higher
# If not: download from https://python.org
```

---

### Step 3 — Install Dependencies

```bash
pip install streamlit openai pandas
```

If you're on a system that needs isolated environments:

```bash
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

pip install streamlit openai pandas
```

---

### Step 4 — Get Your Free Groq API Key

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up (Google login works)
3. Click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Copy the key — it starts with `gsk_`

> ✅ Groq is 100% free. No credit card needed. Very generous rate limits.

---

### Step 5 — Run the App

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

### Step 6 — Use the App

1. Paste your `gsk_...` Groq API key in the input field
2. Click **"🚀 Generate 10 Target Companies with AI"**
3. Wait ~3 seconds — AI discovers 10 fresh companies
4. Click **"Generate →"** next to any company
5. Wait ~5 seconds — full SDR report appears on the right
6. Repeat for all companies to fill your pipeline
7. Click **"📥 Export Pipeline as JSON"** at the bottom

---

## 📁 File Structure

```
videosdk-ai-sdr/
├── app.py          ← entire application (single file)
└── README.md       ← this file
```

> The entire workflow is in one file by design — easy to read, share, and deploy.

---

## 🔧 Configuration

To avoid pasting the API key every time, set it as an environment variable:

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_your_key_here
streamlit run app.py
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="gsk_your_key_here"
streamlit run app.py
```

---

## 🤔 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong API key | Re-copy the key from console.groq.com |
| `429 Rate Limit` | Too many requests | Wait 30 seconds, try again |
| `JSONDecodeError` | LLM returned non-JSON | Click Generate again (rare, retries work) |
| `ModuleNotFoundError: streamlit` | Not installed | Run `pip install streamlit openai pandas` |
| `Port 8501 already in use` | Another app running | Run `streamlit run app.py --server.port 8502` |
| Browser doesn't open | Streamlit issue | Manually go to `http://localhost:8501` |

---

## 💡 Design Decisions

**Why Groq instead of OpenAI?**
Groq is free with no credit card required. LLaMA 3.3 70B performs on par with GPT-3.5-turbo for structured JSON generation tasks. It's also 3–5x faster.

**Why a single file?**
Keeps it portable and easy to demo. For a production system you'd split into agents, prompts, and data layers.

**Why session_state for pipeline?**
Streamlit reruns the entire script on every interaction. `session_state` persists data across reruns without a database.

**Why generate companies via AI instead of hardcoding?**
Every run produces a fresh, diverse set of targets. Demonstrates AI-native thinking — the workflow itself is dynamic, not static.

---
## Demo Video link 

https://www.loom.com/share/74201ee0dcb64753a8577debddc63dfe


---

## Demo Pictures
<img width="873" height="372" alt="Screenshot 2026-05-16 131326" src="https://github.com/user-attachments/assets/d8682a9a-2ed9-4a7a-96be-312624f6bc83" />


<img width="1110" height="582" alt="Screenshot 2026-05-16 131347" src="https://github.com/user-attachments/assets/fbae52c7-cee4-4b80-8419-ea4f70d81eea" />


<img width="453" height="622" alt="Screenshot 2026-05-16 131400" src="https://github.com/user-attachments/assets/ae94fb68-1b81-4b6a-afa4-ba2aeaad6921" />


<img width="962" height="537" alt="Screenshot 2026-05-16 131419" src="https://github.com/user-attachments/assets/95730dfe-f15b-4c66-aa37-741a15d160ae" />


<img width="951" height="503" alt="Screenshot 2026-05-16 131442" src="https://github.com/user-attachments/assets/43af9932-a401-4cf2-846d-45638d650d8d" />


<img width="1460" height="281" alt="Screenshot 2026-05-16 131453" src="https://github.com/user-attachments/assets/10d9c400-2b5e-47d6-980e-78c3ace24dbd" />
