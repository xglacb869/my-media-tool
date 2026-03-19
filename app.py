import streamlit as st
import yt_dlp
import os
import glob

st.set_page_config(page_title="多媒体素材云端提取", page_icon="☁️")
st.title("☁️ 多媒体素材云端提取站")
st.write("输入链接，云端服务器将自动为您提取并转码，随后提供下载按钮。")

url = st.text_input("🔗 请输入视频链接 (URL):")

mode = st.selectbox(
    "⚙️ 选择处理模式:",
    ("最高画质视频 (MP4)", "提取纯音频 (MP3 - 192kbps)", "提取纯音频 (WAV - 无损音质)")
)

if st.button("🚀 开始云端提取", type="primary"):
    if not url:
        st.warning("⚠️ 请输入有效的视频链接！")
    else:
        with st.spinner("云端服务器正在拼命下载和转码，请保持网页打开，耐心等待..."):
            # 1. 先清理服务器上残留的旧文件，防止把免费服务器撑爆
            for f in glob.glob("cloud_output.*"):
                try:
                    os.remove(f)
                except:
                    pass

            # 2. 统一云端输出的文件名，方便稍后打包给用户
            ydl_opts = {
                'outtmpl': 'cloud_output.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }

            if mode == "最高画质视频 (MP4)":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
            elif mode == "提取纯音频 (MP3 - 192kbps)":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
            elif mode == "提取纯音频 (WAV - 无损音质)":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}]

            # 3. 执行云端下载
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 4. 找到下载好的文件，并生成网页下载按钮
                downloaded_files = glob.glob("cloud_output.*")
                if downloaded_files:
                    file_path = downloaded_files[0]
                    file_ext = os.path.splitext(file_path)[1]
                    
                    with open(file_path, "rb") as file:
                        st.success("✅ 云端处理完成！请点击下方按钮保存到您的设备：")
                        st.download_button(
                            label="⬇️ 点击保存文件到本机",
                            data=file,
                            file_name=f"提取素材{file_ext}",
                            mime="application/octet-stream"
                        )
                else:
                    st.error("❌ 文件处理失败，未能生成输出文件。")

            except Exception as e:
                st.error(f"❌ 云端提取出错: {str(e)}")
