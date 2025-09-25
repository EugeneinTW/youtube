# 🚀 Heroku 部署指南

## 📋 **部署前準備**

### 1. **註冊Heroku帳戶**
- 前往 [heroku.com](https://heroku.com)
- 免費註冊帳戶

### 2. **安裝Heroku CLI（可選）**
- 下載：[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- 或使用網頁界面部署

## 🌐 **方法一：網頁界面部署（推薦）**

### **步驟1：創建新應用**
1. 登入Heroku控制台
2. 點擊 **"New"** → **"Create new app"**
3. 輸入應用名稱（如：`your-youtube-downloader`）
4. 選擇地區（建議：United States）
5. 點擊 **"Create app"**

### **步驟2：連接GitHub**
1. 在 **"Deploy"** 頁面
2. 選擇 **"GitHub"** 作為部署方法
3. 點擊 **"Connect to GitHub"**
4. 搜索並選擇 `youtube` 倉庫
5. 點擊 **"Connect"**

### **步驟3：部署**
1. 選擇 **"main"** 分支
2. 點擊 **"Deploy Branch"**
3. 等待部署完成（約3-5分鐘）

### **步驟4：開啟應用**
1. 部署完成後，點擊 **"View"**
2. 您的YouTube下載器就上線了！

## 💻 **方法二：命令行部署**

### **前提條件**
```bash
# 安裝Heroku CLI後登入
heroku login
```

### **部署步驟**
```bash
# 1. 創建Heroku應用
heroku create your-app-name

# 2. 推送代碼
git push heroku main

# 3. 開啟應用
heroku open
```

## ⚙️ **配置檔案說明**

### **Procfile**
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```
- 告訴Heroku如何啟動應用

### **runtime.txt**
```
python-3.11.9
```
- 指定Python版本

### **requirements.txt**
```
flask>=2.3.0
yt-dlp>=2023.10.13
gunicorn>=21.0.0
```
- 列出所有依賴

### **app.json**
- Heroku應用配置
- 支援一鍵部署

## 🎯 **一鍵部署按鈕**

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/EugeneinTW/youtube)

點擊上方按鈕即可一鍵部署到Heroku！

## 🔧 **常見問題**

### **Q: 部署失敗怎麼辦？**
A: 檢查Heroku日誌：
```bash
heroku logs --tail
```

### **Q: 應用無法啟動？**
A: 確認Procfile格式正確，檢查依賴是否完整

### **Q: 下載功能不工作？**
A: 這是正常現象，某些YouTube影片有下載限制

## 🌟 **Heroku優勢**

- ✅ **最穩定** - 業界標準雲端平台
- ✅ **文檔完整** - 豐富的教學資源
- ✅ **社群支援** - 大量開發者使用
- ✅ **自動SSL** - 內建HTTPS支援
- ✅ **簡單部署** - 一鍵部署功能

## 📱 **部署後**

您的YouTube下載器將可在以下URL訪問：
```
https://your-app-name.herokuapp.com
```

**恭喜！您已成功將YouTube下載器部署到Heroku！** 🎉