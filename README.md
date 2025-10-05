## 📧 Smart Email Generator  

AI-powered email assistant built with **Meta LLaMA-4**, **Cerebras API**, **Streamlit**, and **Docker**.  

---

### 🌟 Overview  

**Smart Email Generator** helps users instantly create professional, friendly, or technical emails using **AI-powered role and tone awareness**.  
Users can describe what they want in natural language or use structured inputs for tone, intent, and role.  
The app generates a subject and body, previews it, and lets users send it directly via Gmail.  

---

### ✨ Features  

- 🎯 **Intent, Tone & Role Control**  
- 💬 **Natural Instruction + Context Input**  
- 🧠 **Meta LLaMA-4 via Cerebras API**  
- 📤 **Send Email via Gmail API**  
- 🐳 **Dockerized for Deployment**  
- 🧾 **Secure .env & Volume-based Credentials**  

---

### 🧰 Tech Stack  

| Category | Technology |
|-----------|-------------|
| **LLM** | Meta LLaMA-4 (via Cerebras Cloud SDK) |
| **Frontend** | Streamlit |
| **Backend** | Python |
| **Email API** | Gmail API (OAuth 2.0) |
| **Deployment** | Docker + Docker Compose |

---

### 🚀 Quick Start  

#### 1️⃣ Clone  
```bash
git clone https://github.com/<your-username>/smart-email-generator.git
cd smart-email-generator
```
#### 2️⃣ Environment Variables  

Create `.env` file:  
```env
CEREBRAS_API_KEY=sk-your-cerebras-key
```
### 📦 Dockerfile
```code
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

```
---

### 🔐 Gmail API Setup (for Sending Emails)

To enable Gmail sending, you need to create OAuth credentials from your Google Cloud Console.

#### 1️⃣ Enable the Gmail API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a new project (or use an existing one).  
3. Navigate to **APIs & Services → Library**.  
4. Search for **Gmail API** and click **Enable**.

#### 2️⃣ Create OAuth Credentials
1. Go to **APIs & Services → Credentials**.  
2. Click **Create Credentials → OAuth client ID**.  
3. Choose **Desktop app** as the application type.  
4. Download the `credentials.json` file and place it in your project root folder.

> ⚠️ **Important:** Do **not** commit this file to GitHub.  
> It contains private keys that authorize access to your Gmail account.

---

### 🔑 First-Time Authorization
When you run the app for the first time, a browser window will open asking for Gmail permissions.

1. Log in with the Gmail account you want to use for sending.  
2. Allow the required permissions (sending emails).  
3. The app will save a token file named `token.pkl` automatically — this stores your authorization credentials securely for future use.

> ⚙️ **Files created locally:**
> - `credentials.json` → your OAuth client secrets  
> - `token.pkl` → saved access token (generated after first login)

You can then mount these files inside your Docker container using:
```yaml
volumes:
  - ./credentials.json:/app/credentials.json:ro
  - ./token.pkl:/app/token.pkl
```

---


#### 3️⃣ Run
```bash
docker-compose up --build
```
Then open → http://localhost:8501

---

### 🧩 Sponsor Technology Usage

🧠 Cerebras → AI inference using LLaMA-4 model via Cerebras Cloud SDK.

🧠 Meta (LLaMA) → Role-aware, tone-controlled text generation using structured prompts.

🐳 Docker → Containerized deployment with environment-based security for portability.

---


### 🎥 Demo

👉 YouTube: [Smart Email Generator (3-min Demo)](https://lnkd.in/dCXJY-sF)

---

### 🧠 Learning

Integrated Cerebras SDK with Meta LLaMA models.

Managed Gmail OAuth securely.

Designed modular prompts with intent/tone conditioning.

Containerized AI apps for fast, reproducible deployment.

---

### 🏆 Hackathon Tracks

✅ Cerebras
✅ Meta

---

### 📬 Impact

Smart Email Generator helps students, employees, and professionals communicate more effectively by automating repetitive, time-consuming email writing tasks — while keeping tone, role, and personalization intact.

---

### 💡 Author

#### Ankit Anand

• [LinkedIn](https://linkedin.com/in/ankitanand-ai)
• [X](https://x.com/Ank17_Developer)


