import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Student Portfolio Builder",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Student Portfolio Builder")
st.write("Fill in your details below to generate a professional, clean student portfolio powered by Groq AI.")

# Check for API Key in Streamlit Secrets
if "GROQ_API_KEY" not in st.secrets or not st.secrets["GROQ_API_KEY"]:
    st.error("⚠️ Groq API key is not configured. Please add GROQ_API_KEY to Streamlit Secrets.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Form layout using expanders/sections
st.header("📝 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Personal Information")
    full_name = st.text_input("Full Name *", placeholder="John Doe")
    location = st.text_input("Location", placeholder="New York, USA")
    email = st.text_input("Email Address", placeholder="john@example.com")
    intro = st.text_area("Short Bio / Intro", placeholder="Passionate Computer Science student with a focus on web development.")

    st.subheader("Skills")
    tech_skills = st.text_input("Technical Skills", placeholder="Python, JavaScript, React, SQL")
    other_skills = st.text_input("Other Skills / Soft Skills", placeholder="Leadership, Communication, Problem Solving")

    st.subheader("Social Links")
    github = st.text_input("GitHub Profile URL", placeholder="https://github.com/username")
    linkedin = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/username")

with col2:
    st.subheader("Education")
    degree = st.text_input("Degree / Program", placeholder="B.S. in Computer Science")
    university = st.text_input("University / College", placeholder="State University")
    semester = st.text_input("Current Semester / Year", placeholder="6th Semester / Senior")

    st.subheader("Projects")
    proj_name = st.text_input("Project Name", placeholder="E-Commerce Website")
    proj_desc = st.text_area("Project Description", placeholder="Built a full-stack shopping app with user authentication.")
    proj_tech = st.text_input("Technologies Used", placeholder="Django, PostgreSQL, HTML/CSS")

    st.subheader("Certificates")
    cert_name = st.text_input("Certificate Name", placeholder="AWS Certified Cloud Practitioner")
    cert_org = st.text_input("Issuing Organization", placeholder="Amazon Web Services")

st.markdown("---")

# Generation Logic
if st.button("🚀 Generate Portfolio", type="primary"):
    if not full_name.strip():
        st.warning("Please provide at least your Full Name before generating.")
    else:
        # Construct prompt ensuring strict constraints
        prompt = f"""
You are a professional resume writer and career coach specializing in helping university students.
Generate a structured, professional, clean, and natural student portfolio based STRICTLY on the details provided below.

CRITICAL INSTRUCTION:
Do NOT invent, fabricate, or assume any information, skills, degrees, projects, certificates, or jobs not explicitly listed below. Use only the provided information.

--- USER DETAILS ---
Name: {full_name}
Location: {location}
Email: {email}
Bio / Intro: {intro}

Degree: {degree}
University: {university}
Semester/Year: {semester}

Technical Skills: {tech_skills}
Other Skills: {other_skills}

Project Name: {proj_name}
Project Description: {proj_desc}
Technologies Used: {proj_tech}

Certificate: {cert_name}
Issuing Organization: {cert_org}

GitHub: {github}
LinkedIn: {linkedin}
--- END DETAILS ---

Please organize the output clearly into the following Markdown sections:
1. Professional About Me
2. Education
3. Skills
4. Projects
5. Certificates
6. Contact Information

Make the formatting look clean, well-structured, and attractive using Markdown headers, bullet points, and clean styling suitable for a portfolio.
        """

        with st.spinner("AI is crafting your professional portfolio..."):
            try:
                # Call Groq Chat Completion API using supported production model
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.3,
                )
                
                generated_content = response.choices[0].message.content

                st.success("✅ Your Portfolio is ready!")
                st.markdown("---")
                st.markdown(generated_content)

            except Exception as e:
                st.error("An error occurred while generating the portfolio. Please verify your Groq API key and try again.")