#!/usr/bin/env python3
"""
Flask版本的YouTube下載器
更適合在Railway等雲端平台部署
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import yt_dlp
import os
import tempfile
import re
import glob
import threading
import time
from pathlib import Path
import traceback

app = Flask(__name__)

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
            print(f"獲取影片資訊失敗: {str(e)}")
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
            
            # 根據選擇的畫質設定格式
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

# 全域下載器實例
downloader = YouTubeDownloader()

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/validate_url', methods=['POST'])
def validate_url():
    """驗證YouTube URL"""
    data = request.get_json()
    url = data.get('url', '')
    
    is_valid = downloader.validate_youtube_url(url)
    
    if is_valid:
        video_info = downloader.get_video_info(url)
        return jsonify({
            'valid': True,
            'video_info': video_info
        })
    else:
        return jsonify({
            'valid': False,
            'error': '無效的YouTube連結格式'
        })

@app.route('/api/download', methods=['POST'])
def download_video():
    """開始下載影片"""
    data = request.get_json()
    url = data.get('url', '')
    quality = data.get('quality', '720p')
    
    if downloader.is_downloading:
        return jsonify({
            'success': False,
            'error': '已有下載任務進行中'
        })
    
    # 創建下載目錄
    download_dir = tempfile.mkdtemp()
    
    # 在背景執行下載
    def download_thread():
        downloader.download_video(url, quality, download_dir)
    
    thread = threading.Thread(target=download_thread)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': '下載已開始'
    })

@app.route('/api/status')
def get_status():
    """獲取下載狀態"""
    return jsonify({
        'is_downloading': downloader.is_downloading,
        'progress': downloader.download_progress,
        'status': downloader.download_status,
        'downloaded_file': downloader.downloaded_file
    })

@app.route('/api/download_file')
def download_file():
    """下載檔案到用戶電腦"""
    if downloader.downloaded_file and os.path.exists(downloader.downloaded_file):
        filename = os.path.basename(downloader.downloaded_file)
        return send_file(
            downloader.downloaded_file,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )
    else:
        return jsonify({
            'error': '檔案不存在'
        }), 404

@app.route('/api/reset')
def reset_status():
    """重置下載狀態"""
    downloader.download_status = ""
    downloader.download_progress = 0
    downloader.downloaded_file = None
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)