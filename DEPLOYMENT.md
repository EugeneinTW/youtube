# 🚀 部署指南

由於 Streamlit Cloud 的網路限制，YouTube 下載器無法在該平台正常運行。以下是推薦的替代部署平台：

## 🌟 推薦平台排序

### 1. Railway (最推薦) ⭐⭐⭐⭐⭐
**為什麼選擇 Railway：**
- 🚀 部署速度最快
- 💰 免費額度充足 ($5/月免費額度)
- 🔗 GitHub 自動部署
- 🌐 無網路限制
- 📊 優秀的監控面板

**部署步驟：**
1. 前往 [Railway.app](https://railway.app)
2. 使用 GitHub 登入
3. 點擊 "New Project" → "Deploy from GitHub repo"
4. 選擇您的 `youtube` 倉庫
5. Railway 會自動檢測並部署

**配置檔案：** `railway.json` ✅

---

### 2. Heroku ⭐⭐⭐⭐
**優點：**
- 📚 文檔完整，社群支援好
- 🆓 有免費方案
- 🔧 配置簡單

**部署步驟：**
1. 註冊 [Heroku](https://heroku.com)
2. 安裝 Heroku CLI
3. 在專案目錄執行：
```bash
heroku create your-app-name
git push heroku main
```

**配置檔案：** `Procfile`, `runtime.txt` ✅

---

### 3. Render ⭐⭐⭐⭐
**優點：**
- 🆓 完全免費
- 🔄 自動從 GitHub 部署
- 🛡️ 內建 SSL

**部署步驟：**
1. 前往 [Render.com](https://render.com)
2. 連接 GitHub 帳戶
3. 選擇 "New Web Service"
4. 選擇您的倉庫
5. 設定：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

**配置檔案：** `render.yaml` ✅

---

### 4. Fly.io ⭐⭐⭐
**優點：**
- ⚡ 性能優秀
- 🌍 全球 CDN
- 🐳 支援 Docker

**部署步驟：**
1. 安裝 [Fly CLI](https://fly.io/docs/getting-started/installing-flyctl/)
2. 註冊並登入：`fly auth signup`
3. 在專案目錄執行：
```bash
fly launch
fly deploy
```

**配置檔案：** `fly.toml` ✅

---

## 🐳 Docker 部署

如果您想在自己的伺服器上部署：

```bash
# 建構映像
docker build -t youtube-downloader .

# 運行容器
docker run -p 8501:8501 youtube-downloader
```

**配置檔案：** `Dockerfile` ✅

---

## 📋 部署前檢查清單

- ✅ 所有配置檔案已準備
- ✅ GitHub 倉庫已更新
- ✅ 選擇合適的部署平台
- ✅ 確認平台支援網路訪問

## 🔧 環境變數設定

某些平台可能需要設定環境變數：

```
PORT=8501
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 🆘 常見問題

**Q: 為什麼 Streamlit Cloud 不能用？**
A: Streamlit Cloud 有網路限制，禁止下載外部內容。

**Q: 哪個平台最適合？**
A: Railway 是目前最推薦的選擇，部署簡單且性能優秀。

**Q: 免費方案夠用嗎？**
A: 對於個人使用，所有平台的免費方案都足夠。

## 🎯 推薦選擇

1. **新手用戶** → Railway
2. **需要穩定性** → Heroku
3. **完全免費** → Render
4. **高性能需求** → Fly.io
5. **自建伺服器** → Docker

選擇任一平台，您的 YouTube 下載器都能正常運行！🎉