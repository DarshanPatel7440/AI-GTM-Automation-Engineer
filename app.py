# pip install streamlit openai

import os
import json
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="VideoSDK AI SDR", page_icon="🎥", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }
code, .mono { font-family: 'JetBrains Mono', monospace; }

.main { background: #0a0a0f; }
.stApp { background: #0a0a0f; color: #e8e8f0; }

.hero-title {
    font-size: 2.8rem; font-weight: 700; letter-spacing: -1px;
    background: linear-gradient(135deg, #00d4ff, #7b61ff, #ff6b6b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.hero-sub { color: #888; font-size: 1rem; margin-bottom: 2rem; }

.company-card {
    background: #13131a; border: 1px solid #2a2a3a;
    border-radius: 12px; padding: 1.2rem 1.4rem;
    margin-bottom: 0.6rem; cursor: pointer;
    transition: all 0.2s;
}
.company-card:hover { border-color: #7b61ff; background: #16161f; }

.badge-smb {
    background: #0d2e1a; color: #00e676; border: 1px solid #00e676;
    padding: 3px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
}
.badge-midmarket {
    background: #0d1f3a; color: #40a9ff; border: 1px solid #40a9ff;
    padding: 3px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
}
.badge-enterprise {
    background: #2e0d0d; color: #ff6b6b; border: 1px solid #ff6b6b;
    padding: 3px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
}

.result-box {
    background: #13131a; border: 1px solid #2a2a3a;
    border-radius: 14px; padding: 1.6rem; margin-top: 1rem;
}
.section-label {
    color: #888; font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1.5px; margin-bottom: 0.4rem;
}
.section-value { color: #e8e8f0; font-size: 0.95rem; line-height: 1.6; }

.email-box {
    background: #0d0d14; border: 1px solid #2a2a3a; border-left: 3px solid #7b61ff;
    border-radius: 8px; padding: 1rem 1.2rem; margin-top: 0.4rem;
    font-size: 0.9rem; line-height: 1.7; white-space: pre-wrap;
}
.dm-box {
    background: #0d0d14; border: 1px solid #2a2a3a; border-left: 3px solid #00d4ff;
    border-radius: 8px; padding: 1rem 1.2rem; margin-top: 0.4rem;
    font-size: 0.9rem; line-height: 1.7;
}

.metric-card {
    background: #13131a; border: 1px solid #2a2a3a;
    border-radius: 10px; padding: 1rem 1.2rem; text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #00d4ff; }
.metric-lbl { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }

.pain-item { color: #aaa; font-size: 0.88rem; padding: 3px 0; }
.pain-item::before { content: "→ "; color: #7b61ff; }

.priority-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7b61ff, #00d4ff);
    color: white; font-weight: 700; font-size: 0.8rem;
    padding: 2px 10px; border-radius: 20px;
}
.value-text { color: #00e676; font-weight: 600; font-size: 1.05rem; }

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #7b61ff, #00d4ff) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

.stTextInput input, .stSelectbox select {
    background: #13131a !important; color: #e8e8f0 !important;
    border: 1px solid #2a2a3a !important; border-radius: 8px !important;
}

hr { border-color: #2a2a3a !important; }
.stDataFrame { background: #13131a; }
</style>
""", unsafe_allow_html=True)

COMPANIES_PROMPT = """You are a B2B sales researcher for VideoSDK (videosdk.live) — a real-time video/audio SDK for developers.

Generate exactly 10 realistic target companies that would genuinely need a video SDK.
Mix: 4 SMB (< 50 employees), 3 Mid-Market (50–500), 3 Enterprise (500+).
Mix verticals: EdTech, Telehealth, HR Tech, Fitness, FinTech, Social, PropTech, Legal, Gaming.
Include Indian AND global companies.

Return ONLY a valid JSON array. No markdown. No explanation. No backticks.
Exactly this structure:
[
  {"name": "CompanyName", "vertical": "Vertical", "location": "Country", "size": "SMB"},
  ...
]
Size must be exactly one of: SMB, Mid-Market, Enterprise."""

def generate_companies(api_key):
    client = get_client(api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": COMPANIES_PROMPT}],
        temperature=0.9,
        max_tokens=600
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

SYSTEM_PROMPT = """You are an expert GTM Automation Engineer for VideoSDK (videosdk.live) — 
a developer API/SDK for real-time video, audio & live streaming (WebRTC-based).

Given a company name, vertical, location, and size hint, you must:
1. Research what the company does (from your training knowledge)
2. Identify how they would specifically use VideoSDK (1:1 calls, group video, live streaming, video KYC, interview platform, virtual events, etc.)
3. Segment them accurately: SMB / Mid-Market / Enterprise
4. Write a personalized cold email under 100 words:
   - SMB: casual, founder-to-founder tone, CTA = "Try free at videosdk.live — takes one sprint to integrate"
   - Mid-Market: technical + business value tone, CTA = "Happy to do a quick technical walkthrough"  
   - Enterprise: ROI + reliability + compliance focused, CTA = "Can I show you a 20-min demo this week?"
5. Write a LinkedIn DM in exactly 3 sentences — human, not automated
6. Estimate monthly pipeline value:
   - SMB: $500–$2,000
   - Mid-Market: $2,000–$10,000
   - Enterprise: $10,000–$50,000
7. Priority score 1–10 based on use case fit × urgency × company scale

Return ONLY a valid JSON object. No markdown. No explanation. No backticks.
Exactly this structure:
{
  "segment": "SMB" or "Mid-Market" or "Enterprise",
  "use_case": "one sentence describing exact VideoSDK use case",
  "pain_points": ["pain 1", "pain 2", "pain 3"],
  "cold_email_subject": "subject line under 8 words",
  "cold_email_body": "email body under 100 words",
  "linkedin_dm": "exactly 3 sentences",
  "estimated_monthly_value": "$X,XXX/month",
  "priority_score": 8
}"""

def get_client(api_key):
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

def generate_sdr_report(company, api_key):
    client = get_client(api_key)
    user_msg = f"""Company: {company['name']}
Vertical: {company['vertical']}
Location: {company['location']}
Size hint: {company['size']}

Generate the VideoSDK SDR report now."""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg}
        ],
        temperature=0.7,
        max_tokens=900
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def badge_html(segment):
    cls = {"SMB": "badge-smb", "Mid-Market": "badge-midmarket", "Enterprise": "badge-enterprise"}.get(segment, "badge-smb")
    return f'<span class="{cls}">{segment}</span>'

def priority_color(score):
    if score >= 8: return "#00e676"
    if score >= 5: return "#ffd666"
    return "#ff6b6b"

if "pipeline" not in st.session_state:
    st.session_state.pipeline = {}
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None
if "companies" not in st.session_state:
    st.session_state.companies = []

st.markdown('<div class="hero-title">🎥 VideoSDK AI SDR</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">AI-powered outbound workflow · Research · Segment · Personalize · Pipeline</div>', unsafe_allow_html=True)

api_key = os.environ.get("GROQ_API_KEY", "")
if not api_key:
    api_key = st.text_input("🔑 Groq API Key (free at console.groq.com)", type="password", placeholder="gsk_...")
    if not api_key:
        st.warning("Enter your Groq API key to start.")
        st.stop()

if not st.session_state.companies:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 2rem; border: 1px dashed #2a2a3a; border-radius: 14px; margin: 1rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🤖</div>
        <div style="font-size: 1.1rem; color: #aaa; margin-bottom: 1.5rem;">
            API key detected! Let AI discover 10 fresh target companies for VideoSDK.
        </div>
    </div>
    """, unsafe_allow_html=True)
    col_c = st.columns([1, 2, 1])[1]
    with col_c:
        if st.button("🚀 Generate 10 Target Companies with AI", use_container_width=True):
            with st.spinner("🤖 AI is discovering target companies..."):
                try:
                    st.session_state.companies = generate_companies(api_key)
                    st.session_state.pipeline = {}
                    st.session_state.selected_company = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating companies: {e}")
    st.stop()

st.markdown("---")

col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.markdown("### 🏢 Target Companies")
    col_cap, col_regen = st.columns([2, 1])
    with col_cap:
        st.caption("Click a company → generate live AI SDR report")
    with col_regen:
        if st.button("🔄 Regenerate", use_container_width=True):
            with st.spinner("Discovering new companies..."):
                try:
                    st.session_state.companies = generate_companies(api_key)
                    st.session_state.pipeline = {}
                    st.session_state.selected_company = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    for c in st.session_state.companies:
        processed = c["name"] in st.session_state.pipeline
        badge = badge_html(c["size"])
        check = "✅ " if processed else ""
        
        with st.container():
            st.markdown(f"""
            <div class="company-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-weight:600; color:#e8e8f0;">{check}{c['name']}</span>
                        <span style="color:#888; font-size:0.82rem; margin-left:8px;">{c['vertical']} · {c['location']}</span>
                    </div>
                    {badge}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Generate →", key=f"btn_{c['name']}"):
                st.session_state.selected_company = c

with col_right:
    if st.session_state.selected_company:
        company = st.session_state.selected_company
        cname = company["name"]
        
        st.markdown(f"### Generating report for **{cname}**")
        
        if cname not in st.session_state.pipeline:
            with st.spinner(f"🤖 AI is researching {cname}..."):
                try:
                    result = generate_sdr_report(company, api_key)
                    st.session_state.pipeline[cname] = {**company, **result}
                except Exception as e:
                    st.error(f"API Error: {e}")
                    st.stop()
        
        r = st.session_state.pipeline[cname]
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-val">{r.get("priority_score", "—")}/10</div><div class="metric-lbl">Priority Score</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-val" style="font-size:1.2rem; color:#00e676;">{r.get("estimated_monthly_value","—")}</div><div class="metric-lbl">Est. Monthly Value</div></div>', unsafe_allow_html=True)
        with m3:
            seg = r.get("segment","SMB")
            st.markdown(f'<div class="metric-card" style="padding-top:1.3rem;">{badge_html(seg)}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        
        st.markdown('<div class="section-label">📌 Use Case</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-value">{r.get("use_case","")}</div>', unsafe_allow_html=True)
        
        st.markdown('<br><div class="section-label">⚡ Pain Points</div>', unsafe_allow_html=True)
        for p in r.get("pain_points", []):
            st.markdown(f'<div class="pain-item">{p}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("#### 📧 Cold Email")
        subj = r.get("cold_email_subject","")
        body = r.get("cold_email_body","")
        st.markdown(f'<div style="color:#888; font-size:0.8rem; margin-bottom:4px;">Subject: <span style="color:#e8e8f0; font-weight:600;">{subj}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="email-box">{body}</div>', unsafe_allow_html=True)
        
        st.markdown("#### 💼 LinkedIn DM")
        dm = r.get("linkedin_dm","")
        st.markdown(f'<div class="dm-box">{dm}</div>', unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; color: #444; border: 1px dashed #2a2a3a; border-radius: 14px; margin-top: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <div style="font-size: 1.1rem; color: #666;">Select a company on the left<br>to generate a live AI SDR report</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📊 Pipeline Summary")

if st.session_state.pipeline:
    pipeline_data = list(st.session_state.pipeline.values())
    
    total_companies = len(pipeline_data)
    smb_count     = sum(1 for p in pipeline_data if p.get("segment") == "SMB")
    mid_count     = sum(1 for p in pipeline_data if p.get("segment") == "Mid-Market")
    ent_count     = sum(1 for p in pipeline_data if p.get("segment") == "Enterprise")
    
    def parse_value(v):
        try:
            return float(v.replace("$","").replace(",","").replace("/month","").strip().split("–")[-1].split("-")[-1])
        except: return 0
    
    total_val = sum(parse_value(p.get("estimated_monthly_value","0")) for p in pipeline_data)
    
    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    mc1.markdown(f'<div class="metric-card"><div class="metric-val">{total_companies}</div><div class="metric-lbl">Companies</div></div>', unsafe_allow_html=True)
    mc2.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#00e676;">{smb_count}</div><div class="metric-lbl">SMB</div></div>', unsafe_allow_html=True)
    mc3.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#40a9ff;">{mid_count}</div><div class="metric-lbl">Mid-Market</div></div>', unsafe_allow_html=True)
    mc4.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#ff6b6b;">{ent_count}</div><div class="metric-lbl">Enterprise</div></div>', unsafe_allow_html=True)
    mc5.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#00e676; font-size:1.3rem;">${total_val:,.0f}/mo</div><div class="metric-lbl">Pipeline Value</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    import pandas as pd
    rows = []
    for p in pipeline_data:
        rows.append({
            "Company":       p["name"],
            "Vertical":      p["vertical"],
            "Segment":       p.get("segment",""),
            "Use Case":      p.get("use_case","")[:60] + "..." if len(p.get("use_case","")) > 60 else p.get("use_case",""),
            "Monthly Value": p.get("estimated_monthly_value",""),
            "Priority":      p.get("priority_score", 0),
            "Email ✅":      "✅",
            "DM ✅":         "✅",
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Priority": st.column_config.ProgressColumn("Priority", min_value=0, max_value=10, format="%d"),
            "Monthly Value": st.column_config.TextColumn("Monthly Value"),
        }
    )
    
    if st.button("📥 Export Pipeline as JSON"):
        export = json.dumps({"pipeline": pipeline_data, "total_monthly_value": f"${total_val:,.0f}"}, indent=2)
        st.download_button("Download pipeline.json", export, "pipeline.json", "application/json")

else:
    st.info("No companies processed yet. Generate your first SDR report using the panel above.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#333; font-size:0.8rem;">VideoSDK AI SDR · Powered by Groq (llama3-8b-8192) · Built with Streamlit</div>', unsafe_allow_html=True)