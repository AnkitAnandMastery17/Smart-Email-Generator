import streamlit as st
import os
import time
from streamlit_modal import Modal
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

load_dotenv()

# --- Cerebras client ---
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

# --- Streamlit UI ---
st.set_page_config(page_title="Smart Email Generator", page_icon="✉️")
st.title("📧 Smart Email Generator")

st.markdown("Generate professional, friendly, or technical emails instantly with LLaMA via Cerebras.")

recipient_name = st.text_input("Recipient Name", placeholder="e.g. Dean Sharma")
recipient_email = st.text_input("Recipient Email", placeholder="e.g. dean@university.edu")

st.markdown("### 💬 Natural Instruction")
user_instruction = st.text_area(
    "Describe the email you want to write:",
    placeholder="Example: Write an email to the Dean apologizing for missing yesterday’s meeting."
)
st.markdown("---")

intent = st.selectbox("🎯 Email intent", ["Follow-up", "Apology", "Meeting request"])
tone = st.selectbox("🎨 Tone", ["Professional", "Friendly", "Casual"])
role = st.selectbox("🧑‍💼 Role", ["Sales Manager", "Technical Support", "Friendly Peer"])


if "subject" not in st.session_state:
    st.session_state.subject = ""
if "body" not in st.session_state:
    st.session_state.body = ""


# --- Email generation logic ---
def generate_email():
    system_prompt =f"""
       You are an expert AI email assistant that writes complete, well-structured, 
        and contextually accurate professional emails. 
        Always include a greeting, main message, and polite closing. 
        If the user provides both structured inputs and a natural instruction, 
        combine them intelligently to produce the best possible result.
    """

    user_prompt = f"""

### USER INSTRUCTION
{user_instruction if user_instruction.strip() else "No direct instruction provided."}

### STRUCTURED DETAILS
- Role: {role}
- Intent: {intent}
- Recipient: {recipient_name}
- Tone: {tone}

### TASK
Write a complete email that fulfills the user’s intent while reflecting their tone and role.
The context and instruction must guide the content.
Keep the body under 150 words and ensure it is polite and natural.

### OUTPUT FORMAT
Subject: <subject line>
Body:
<complete email text>
At last, after best regards in place of [Your Name] put Ankit Anand.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model="llama-4-scout-17b-16e-instruct",
        temperature=0.7,
        max_tokens=400,
    )

    response = chat_completion.choices[0].message.content
    # st.code(response, language="markdown")

    # Parse subject and body
    subject, body = parse_response(response)
    st.session_state.subject = subject
    st.session_state.body = body


# --- Response parser ---
def parse_response(response: str):
    # Extract subject line (still simple)
    subject_line = next((l for l in response.splitlines() if "Subject:" in l), "")
    subject = subject_line.replace("Subject:", "").strip()

    # If 'Body:' exists, split after it
    if "Body:" in response:
        body = response.split("Body:", 1)[1].strip()
    else:
        # Otherwise, take everything *after the subject line*
        lines = response.splitlines()
        try:
            start_index = lines.index(subject_line)
            body_lines = lines[start_index + 1 :]  # lines after the subject
            body = "\n".join(body_lines).strip()
        except ValueError:
            body = response.strip()

    return subject, body

from email.mime.text import MIMEText
import base64
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def send_email_via_gmail(to_email, subject, body):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    # Load or create token file
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Create the email
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw}

    # Send it
    send_message = service.users().messages().send(userId='me', body=message_body).execute()
    print(f"✅ Email sent successfully! Message ID: {send_message['id']}")
    return True

modal = Modal("📧 Preview Email", key="email_preview_modal")
# --- UI buttons ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚀 Generate Email"):
        with st.spinner("Generating email..."):
            generate_email()
with col2:
    if st.button("🔄 Regenerate"):
        with st.spinner("Re-generating email..."):
            generate_email()
with col3:
    if st.button("📤 Send Email"):
        if not st.session_state.subject or not st.session_state.body:
            st.warning("Please generate an email before sending.")
        elif not recipient_email:
            st.warning("Please enter the recipient's email address.")
        else:
            # Open preview modal
            modal.open()

# --- Preview Modal Content ---
if modal.is_open():
    with modal.container():
        st.subheader("📨 Email Preview")
        st.markdown(f"**To:** {recipient_email}")
        st.markdown(f"**Subject:** {st.session_state.subject}")
        st.text_area("Body", st.session_state.body, height=200, disabled=True)
        st.caption("⚠️ Please review before sending. AI may generate imperfect content.")

        col_confirm, col_cancel = st.columns(2)

        with col_confirm:
            if st.button("✅ Confirm & Send"):
                # Validate email format before sending
                if "@" not in recipient_email or "." not in recipient_email:
                    st.error("⚠️ Invalid email address. Please enter a valid email like name@example.com")
                else:
                    try:
                        send_email_via_gmail(
                            recipient_email,
                            st.session_state.subject,
                            st.session_state.body
                        )
                        st.success(f"✅ Email sent successfully to {recipient_name}!")

                        # Wait briefly before clearing
                        time.sleep(1.5)
                        st.session_state.subject = ""
                        st.session_state.body = ""
                        st.experimental_rerun()

                        modal.close()

                    except Exception as e:
                        st.error(f"❌ Failed to send email: {e}")

        with col_cancel:
            if st.button("❌ Cancel"):
                modal.close()




# --- Output Display ---
if st.session_state.subject:
    st.subheader("📝 Generated Email")
    st.write(f"**Subject:** {st.session_state.subject}")
    st.text_area("Body", st.session_state.body, height=200)
