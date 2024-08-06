import streamlit as st
import yt_dlp
import os

# Define a global variable for the progress bar
progress_bar = None

def update_progress_bar(percent):
    global progress_bar
    if progress_bar:
        progress_bar.progress(percent)

# Function to get video information
def get_video_info(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return info_dict

# Define the download function with progress update
def download_video(url, output_path):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            update_progress_bar(int(percent))
        elif d['status'] == 'finished':
            update_progress_bar(100)
    
    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(output_path, '%(title)s.%(ext)s'),
        "progress_hooks": [progress_hook]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Streamlit app layout
st.title("YouTube Video Downloader")

# User input
url = st.text_input("Enter YouTube video URL:")

if st.button("Get Video Info"):
    if url:
        try:
            info = get_video_info(url)
            video_title = info.get('title', 'N/A')
            video_filesize = info.get('filesize', 0) / (1024 * 1024)  # Convert bytes to MB
            st.write(f"Video Title: {video_title}")
            st.write(f"File Size: {video_filesize:.2f} MB")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a YouTube URL.")

if st.button("Download"):
    if url:
        try:
            info = get_video_info(url)
            video_title = info.get('title', 'N/A')
            video_filesize = info.get('filesize', 0) / (1024 * 1024)  # Convert bytes to MB
            download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
            st.write(f"Downloading '{video_title}' ({video_filesize:.2f} MB) to {download_folder}...")
            
            progress_bar = st.progress(0)  # Initialize progress bar
            download_video(url, download_folder)
            st.success("Video downloaded successfully!")
            st.write(f"Output Path: {download_folder}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            progress_bar = None
    else:
        st.error("Please enter a YouTube URL.")
