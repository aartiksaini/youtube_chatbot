# app.py
import streamlit as st
from yt import build_chain

# Page config
st.set_page_config(page_title="TubeChat 🎥🤖", page_icon="🎬", layout="centered")

# Title & subtitle
st.title("TubeChat 🎥🤖")
st.markdown(
    """
    <h4 style='color:#4CAF50;'>Chat with any YouTube video transcript</h4>
    <p style='font-size:16px;'>
        Paste a YouTube video link below, and then ask anything about it.<br>
        I'll fetch the transcript, process it, and answer your questions ✨
    </p>
    """,
    unsafe_allow_html=True,
)

# Input field for YouTube video
video_url = st.text_input("📌 Paste a YouTube Video URL here:", "")

if video_url:
    try:
        chain = build_chain(video_url)
        st.success("✅ Transcript processed successfully! You can now ask questions.")

        # Instructions
        st.info("💡 Tip: Ask specific questions like *'What is the main topic?'* or *'Summarize the key points in 3 bullets.'*")

        # Question input
        question = st.text_area("📝 Your Question:", placeholder="Type your question about the video here...")

        # Button
        if st.button("🎯 Get Answer"):
            with st.spinner("🤔 Thinking..."):
                answer = chain.invoke(question)
            st.markdown("### 📢 Answer:")
            st.write(answer)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
else:
    st.warning("👆 Please paste a valid YouTube video link to start.")
