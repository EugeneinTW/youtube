# 🎬 YouTube 影片下載器

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一個基於 Streamlit 的現代化 YouTube 影片下載器，提供直觀的網頁界面和強大的下載功能。

![YouTube Downloader Demo](https://via.placeholder.com/800x400/FF0000/FFFFFF?text=YouTube+Downloader)

## ✨ 特色功能

- 🎯 **簡潔直觀的網頁界面** - 基於 Streamlit 構建
- 📱 **響應式設計** - 支援各種螢幕尺寸
- 🎬 **多畫質選擇** - 360p、480p、720p、1080p
- 💾 **瀏覽器內下載** - 直接下載到電腦
- 📁 **檔案管理** - 查看和管理已下載的影片
- ⚡ **快速下載** - 優化的下載引擎
- 🛡️ **安全可靠** - 本地運行，保護隱私

## 🌟 主要功能

### 1. URL 輸入功能
- 清晰標示的輸入框，支援直接貼上 YouTube 影片連結
- 自動驗證 URL 格式有效性
- 支援多種 YouTube 連結格式

### 2. 畫質選擇功能
- 提供 360p、480p、720p、1080p 四種解析度選項
- 下拉式選單呈現，操作直觀
- 顯示各畫質的詳細規格說明和檔案大小預估

### 3. 下載轉換功能
- 一鍵式下載操作流程
- 自動將影片轉換為 MP4 格式
- 支援高品質音訊和影像編碼

### 4. 進度顯示系統
- 即時顯示下載進度條
- 明確標示當前處理狀態
- 動態更新下載資訊

### 5. 錯誤處理機制
- 網路異常時顯示友善提示
- 自動檢測無效 URL 並引導修正
- 提供常見問題解決方案

### 6. 現代化界面設計
- 採用 Streamlit 組件實現直觀操作
- 響應式設計，適配各種螢幕尺寸
- 符合現代化 UI/UX 設計標準

## 🚀 快速開始

### 方法一：直接運行（推薦）

1. **克隆專案**
```bash
git clone https://github.com/EugeneinTW/youtube.git
cd youtube
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **啟動應用**
```bash
streamlit run app.py
```

4. **開啟瀏覽器**
   - 訪問 `http://localhost:8501`
   - 開始下載您喜愛的 YouTube 影片！

### 方法二：使用批次檔（Windows）

1. 雙擊 `run.bat` 檔案
2. 等待自動安裝依賴並啟動
3. 瀏覽器會自動開啟應用

### 方法三：Streamlit Cloud 部署

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/eugeneinTW/youtube/main/app.py)

1. Fork 這個倉庫到您的 GitHub
2. 在 [Streamlit Cloud](https://share.streamlit.io) 創建新應用
3. 連接您的 GitHub 倉庫
4. 選擇 `app.py` 作為主文件
5. 點擊部署

## 📋 系統需求

- Python 3.7+
- 穩定的網路連線
- 支援的瀏覽器（Chrome、Firefox、Safari、Edge）

## 🛠️ 技術架構

- **前端框架**：Streamlit
- **下載引擎**：yt-dlp
- **影片處理**：FFmpeg
- **部署平台**：Streamlit Cloud

## 📝 使用說明

1. **輸入連結**：在輸入框中貼上 YouTube 影片連結
2. **選擇畫質**：根據需求選擇合適的解析度
3. **開始下載**：點擊下載按鈕開始處理
4. **等待完成**：觀察進度條直到下載完成

## ⚠️ 注意事項

- 請確保遵守 YouTube 服務條款
- 僅供個人學習和研究使用
- 請勿用於商業用途或侵犯版權
- 下載速度取決於網路狀況和影片大小

## 🔧 故障排除

### 常見問題

**Q: 無法下載某些影片？**
A: 可能是影片有地區限制或版權保護，請嘗試其他影片。

**Q: 下載速度很慢？**
A: 請檢查網路連線，或選擇較低的畫質。

**Q: 出現錯誤訊息？**
A: 請確認 URL 格式正確，並重新整理頁面再試。

## 🏗️ 技術架構

```
YouTube Downloader
├── Frontend (Streamlit)
│   ├── 用戶界面
│   ├── 檔案管理
│   └── 進度顯示
├── Backend (yt-dlp)
│   ├── 影片資訊提取
│   ├── 格式選擇
│   └── 下載引擎
└── Storage
    ├── 本地檔案系統
    └── 臨時檔案管理
```

### 核心依賴
- **Streamlit** - 網頁應用框架
- **yt-dlp** - YouTube 下載引擎
- **Python 3.7+** - 運行環境

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 如何貢獻
1. Fork 這個專案
2. 創建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

### 報告問題
- 使用 [Issues](https://github.com/EugeneinTW/youtube/issues) 報告 bug
- 提供詳細的錯誤信息和重現步驟
- 包含您的系統環境信息

## 📊 專案統計

![GitHub stars](https://img.shields.io/github/stars/EugeneinTW/youtube?style=social)
![GitHub forks](https://img.shields.io/github/forks/EugeneinTW/youtube?style=social)
![GitHub issues](https://img.shields.io/github/issues/EugeneinTW/youtube)
![GitHub license](https://img.shields.io/github/license/EugeneinTW/youtube)

## 📄 授權

本專案採用 MIT 授權條款 - 查看 [LICENSE](LICENSE) 檔案了解詳情。

### 使用條款
- ✅ 商業使用
- ✅ 修改
- ✅ 分發
- ✅ 私人使用
- ❌ 責任
- ❌ 保證

## ⚠️ 免責聲明

**重要提醒**：
- 本工具僅供教育和個人學習使用
- 請遵守 YouTube 的服務條款
- 請遵守當地法律法規和版權法
- 下載的內容僅供個人使用，請勿用於商業用途
- 使用者需自行承擔使用責任

## 🙏 致謝

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 強大的 YouTube 下載引擎
- [Streamlit](https://streamlit.io/) - 優秀的 Python 網頁應用框架
- 所有貢獻者和使用者的支持

---

<div align="center">
  <p>如果這個專案對您有幫助，請給我們一個 ⭐</p>
  <p>Made with ❤️ by <a href="https://github.com/EugeneinTW">EugeneinTW</a></p>
</div>