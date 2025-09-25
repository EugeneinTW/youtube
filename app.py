import streamlit as st
import yt_dlp
import os
import tempfile
import re
from pathlib import Path
import time
import threading
from urllib.parse import urlparse, parse_qs
import traceback
import sys
import glob

# 設定頁面配置
st.set_page_config(
    page_title="YouTube 影片下載器",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義CSS樣式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF0000;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .quality-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .download-status {
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #c62828;
    }
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

class YouTubeDownloader:
    def __init__(self):
        self.download_progress = 0
        self.download_status = ""
        self.is_downloading = False
        self.downloaded_file = None
        
    def validate_youtube_url(self, url):
        """驗證YouTube URL格式"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def get_video_info(self, url):
        """獲取影片資訊"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': info.get('formats', [])
                }
        except Exception as e:
            st.error(f"獲取影片資訊失敗: {str(e)}")
            return None
    
    def progress_hook(self, d):
        """下載進度回調函數"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                self.download_progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d:
                self.download_progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            self.download_status = f"下載中... {self.download_progress:.1f}%"
        elif d['status'] == 'finished':
            self.download_progress = 100
            self.download_status = "下載完成！"
    
    def download_video(self, url, quality, output_path):
        """下載影片"""
        try:
            self.is_downloading = True
            self.download_progress = 0
            self.download_status = "準備下載..."
            self.downloaded_file = None
            
            # 根據選擇的畫質設定格式 - 使用更兼容的格式選擇
            quality_map = {
                '360p': 'worst[height>=360]/worst[height>=240]/worst',
                '480p': 'best[height<=480]/worst[height>=480]/best[height<=720]/worst',
                '720p': 'best[height<=720]/worst[height>=720]/best[height<=1080]/best',
                '1080p': 'best[height<=1080]/best'
            }
            
            ydl_opts = {
                'format': quality_map.get(quality, 'best/worst'),
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
                'ignoreerrors': False,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 獲取影片資訊以確定檔案名稱
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                
                # 下載影片
                ydl.download([url])
                
                # 尋找下載的檔案
                pattern = os.path.join(output_path, f"{title}.*")
                files = glob.glob(pattern)
                if files:
                    self.downloaded_file = files[0]
                else:
                    # 如果找不到確切檔案，尋找最新的檔案
                    files = glob.glob(os.path.join(output_path, "*"))
                    if files:
                        self.downloaded_file = max(files, key=os.path.getctime)
                
            self.is_downloading = False
            self.download_status = "下載完成！"
            return True
            
        except yt_dlp.DownloadError as e:
            self.is_downloading = False
            self.download_status = f"下載錯誤: {str(e)}"
            return False
        except Exception as e:
            self.is_downloading = False
            self.download_status = f"未知錯誤: {str(e)}"
            traceback.print_exc()
            return False

def main():
    # 標題
    st.markdown('<h1 class="main-header">📺 YouTube 影片下載器</h1>', unsafe_allow_html=True)
    
    # 初始化下載器
    if 'downloader' not in st.session_state:
        st.session_state.downloader = YouTubeDownloader()
    
    # 側邊欄 - 功能說明
    with st.sidebar:
        st.header("📋 功能說明")
        st.markdown("""
        ### 支援功能：
        - ✅ YouTube 影片下載
        - ✅ 多種畫質選擇
        - ✅ 即時進度顯示
        - ✅ 自動格式轉換
        - ✅ 錯誤處理機制
        
        ### 支援畫質：
        - 🔸 360p (標準畫質)
        - 🔸 480p (增強畫質)
        - 🔸 720p (高畫質 HD)
        - 🔸 1080p (全高畫質 FHD)
        """)
        
        st.header("❓ 常見問題")
        with st.expander("如何使用？"):
            st.markdown("""
            1. 複製 YouTube 影片連結
            2. 貼上到輸入框中
            3. 選擇想要的畫質
            4. 點擊下載按鈕
            """)
        
        with st.expander("支援的網址格式"):
            st.markdown("""
            - https://www.youtube.com/watch?v=...
            - https://youtu.be/...
            - https://m.youtube.com/watch?v=...
            """)
        
        # 下載檔案管理
        st.header("📁 下載檔案管理")
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube")
        
        if os.path.exists(download_dir):
            files = [f for f in os.listdir(download_dir) if f.endswith(('.mp4', '.webm', '.mkv'))]
            
            if files:
                st.write(f"📊 共有 {len(files)} 個下載檔案")
                
                # 顯示最近的5個檔案
                files_with_time = []
                for file in files:
                    file_path = os.path.join(download_dir, file)
                    mtime = os.path.getmtime(file_path)
                    files_with_time.append((file, mtime, file_path))
                
                # 按修改時間排序
                files_with_time.sort(key=lambda x: x[1], reverse=True)
                
                st.write("**最近下載的檔案：**")
                for i, (file, mtime, file_path) in enumerate(files_with_time[:5]):
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                    
                    with st.expander(f"{i+1}. {file[:30]}..." if len(file) > 30 else f"{i+1}. {file}"):
                        st.write(f"**檔案大小：** {file_size:.2f} MB")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"📂 開啟位置", key=f"open_{i}"):
                                os.startfile(os.path.dirname(file_path))
                        with col2:
                            if st.button(f"▶️ 播放", key=f"play_{i}"):
                                os.startfile(file_path)
                
                # 開啟下載資料夾按鈕
                if st.button("📂 開啟下載資料夾", type="secondary", use_container_width=True):
                    os.startfile(download_dir)
            else:
                st.info("📭 尚未下載任何檔案")
        else:
            st.info("📁 下載資料夾尚未建立")
    
    # 主要內容區域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔗 影片連結輸入")
        
        # URL 輸入框
        url = st.text_input(
            "請輸入 YouTube 影片連結：",
            placeholder="https://www.youtube.com/watch?v=...",
            help="支援 YouTube 各種格式的連結"
        )
        
        # URL 驗證
        if url:
            if st.session_state.downloader.validate_youtube_url(url):
                st.markdown('<div class="success-message">✅ 有效的 YouTube 連結</div>', unsafe_allow_html=True)
                
                # 獲取影片資訊
                with st.spinner("正在獲取影片資訊..."):
                    video_info = st.session_state.downloader.get_video_info(url)
                
                if video_info:
                    # 顯示影片資訊
                    st.subheader("📹 影片資訊")
                    
                    info_col1, info_col2 = st.columns([1, 1])
                    
                    with info_col1:
                        if video_info['thumbnail']:
                            st.image(video_info['thumbnail'], width=300)
                    
                    with info_col2:
                        st.markdown(f"**標題：** {video_info['title']}")
                        st.markdown(f"**上傳者：** {video_info['uploader']}")
                        
                        # 格式化時長
                        duration = video_info['duration']
                        if duration:
                            minutes = duration // 60
                            seconds = duration % 60
                            st.markdown(f"**時長：** {minutes:02d}:{seconds:02d}")
                        
                        # 格式化觀看次數
                        if video_info['view_count']:
                            views = f"{video_info['view_count']:,}"
                            st.markdown(f"**觀看次數：** {views}")
                    
                    # 畫質選擇
                    st.subheader("🎬 畫質選擇")
                    
                    quality_options = {
                        '360p': '360p - 標準畫質 (適合網路較慢時)',
                        '480p': '480p - 增強畫質 (平衡品質與檔案大小)',
                        '720p': '720p - 高畫質 HD (推薦選擇)',
                        '1080p': '1080p - 全高畫質 FHD (最佳品質)'
                    }
                    
                    selected_quality = st.selectbox(
                        "選擇下載畫質：",
                        options=list(quality_options.keys()),
                        format_func=lambda x: quality_options[x],
                        index=2  # 預設選擇 720p
                    )
                    
                    # 畫質資訊說明
                    quality_info = {
                        '360p': {'size': '約 20-40 MB/小時', 'desc': '適合行動裝置觀看'},
                        '480p': {'size': '約 40-80 MB/小時', 'desc': '平衡的選擇'},
                        '720p': {'size': '約 80-150 MB/小時', 'desc': '高品質觀看體驗'},
                        '1080p': {'size': '約 150-300 MB/小時', 'desc': '最佳視覺效果'}
                    }
                    
                    info = quality_info[selected_quality]
                    st.markdown(f"""
                    <div class="quality-info">
                        <strong>選擇的畫質：{selected_quality}</strong><br>
                        檔案大小：{info['size']}<br>
                        說明：{info['desc']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 下載按鈕
                    if not st.session_state.downloader.is_downloading:
                        if st.button("🚀 開始下載", type="primary", use_container_width=True):
                            # 創建下載目錄
                            download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube")
                            os.makedirs(download_dir, exist_ok=True)
                            
                            # 直接在主線程中執行下載（避免session_state問題）
                            try:
                                st.session_state.downloader.is_downloading = True
                                st.session_state.downloader.download_progress = 0
                                st.session_state.downloader.download_status = "開始下載..."
                                
                                with st.spinner("正在下載影片..."):
                                    success = st.session_state.downloader.download_video(url, selected_quality, download_dir)
                                    
                                if success:
                                    st.success("下載完成！檔案已保存到下載資料夾")
                                else:
                                    st.error(f"下載失敗：{st.session_state.downloader.download_status}")
                                    
                            except Exception as e:
                                st.error(f"下載過程中發生錯誤：{str(e)}")
                                st.session_state.downloader.is_downloading = False
                            
                            st.rerun()
                    
                    # 顯示下載狀態
                    if st.session_state.downloader.download_status and not st.session_state.downloader.is_downloading:
                        if "完成" in st.session_state.downloader.download_status:
                            st.success("✅ " + st.session_state.downloader.download_status)
                            
                            # 顯示下載檔案資訊和下載按鈕
                            if st.session_state.downloader.downloaded_file and os.path.exists(st.session_state.downloader.downloaded_file):
                                file_path = st.session_state.downloader.downloaded_file
                                file_name = os.path.basename(file_path)
                                file_size = os.path.getsize(file_path)
                                file_size_mb = file_size / (1024 * 1024)
                                
                                st.info(f"""
                                📁 **檔案資訊：**
                                - 檔案名稱：{file_name}
                                - 檔案大小：{file_size_mb:.2f} MB
                                - 儲存位置：{file_path}
                                """)
                                
                                # 提供檔案下載
                                with open(file_path, "rb") as file:
                                    st.download_button(
                                        label="💾 下載到電腦",
                                        data=file,
                                        file_name=file_name,
                                        mime="video/mp4",
                                        type="primary",
                                        use_container_width=True
                                    )
                                
                                # 開啟檔案位置按鈕
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("📂 開啟檔案位置", type="secondary"):
                                        os.startfile(os.path.dirname(file_path))
                                
                                with col2:
                                    if st.button("▶️ 播放影片", type="secondary"):
                                        os.startfile(file_path)
                            
                        elif "錯誤" in st.session_state.downloader.download_status or "失敗" in st.session_state.downloader.download_status:
                            st.error("❌ " + st.session_state.downloader.download_status)
                        elif "停止" in st.session_state.downloader.download_status:
                            st.warning("⏹️ " + st.session_state.downloader.download_status)
                        
                        # 重置狀態按鈕
                        if st.button("🔄 重新開始", type="secondary"):
                            st.session_state.downloader.download_status = ""
                            st.session_state.downloader.download_progress = 0
                            st.session_state.downloader.downloaded_file = None
                            st.rerun()
                
                else:
                    st.markdown('<div class="error-message">❌ 無法獲取影片資訊，請檢查連結是否正確</div>', unsafe_allow_html=True)
            
            else:
                st.markdown('<div class="error-message">❌ 無效的 YouTube 連結格式</div>', unsafe_allow_html=True)
    
    with col2:
        st.header("💡 使用提示")
        
        st.info("""
        **下載步驟：**
        1. 複製 YouTube 影片連結
        2. 貼上到左側輸入框
        3. 選擇合適的畫質
        4. 點擊下載按鈕
        """)
        
        st.warning("""
        **注意事項：**
        - 請確保網路連線穩定
        - 下載時間取決於影片長度
        - 請遵守版權相關法規
        """)
        
        st.success("""
        **支援格式：**
        - 輸出格式：MP4
        - 音訊編碼：AAC
        - 影像編碼：H.264
        """)

if __name__ == "__main__":
    main()