import os
import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")
st.title("✍️ AI Content Assistant")
st.write("Generate tailored social media posts, captions, and hashtags instantly.")

# API Key handling
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
if not api_key:
    # Fallback to environment variable if set
    api_key = os.environ.get("GEMINI_API_KEY", "")

# User inputs
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        ["Social Media Post", "Educational Tip", "Product Announcement", "Story/Personal Insight", "Call to Action"]
    )
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"]
    )
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual & Friendly", "Energetic & Bold", "Informative", "Witty & Humorous"]
    )

with col2:
    topic = st.text_input("Topic / Main Idea", placeholder="e.g., Launching a new productivity app")
    target_audience = st.text_input("Target Audience", placeholder="e.g., Remote workers, busy professionals")

# Generation logic
if st.button("Generate Post", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please provide a valid Gemini API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a topic or main idea.")
    else:
        try:
            with st.spinner("Crafting your content..."):
                # Initialize official GenAI client
                client = genai.Client(api_key=api_key)

                # Construct prompt
                prompt = f"""
                You are an expert social media strategist and copywriter.
                Create a high-performing post based on the following criteria:

                - **Content Type**: {content_type}
                - **Platform**: {platform}
                - **Topic**: {topic}
                - **Target Audience**: {target_audience if target_audience else "General audience"}
                - **Tone**: {tone}

                Format your response clearly:
                1. Provide the main post content formatted specifically for {platform} (e.g., appropriate line breaks, emojis where suitable).
                2. Add a section with 5 to 10 highly relevant, trending hashtags.
                """

                # Call Gemini model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                    )
                )

                st.success("Content Generated!")
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")