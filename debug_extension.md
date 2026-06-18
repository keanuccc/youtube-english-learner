# Chrome 扩展调试指南

## 问题 1: "Learn English" 按钮不出现

### 检查步骤：

1. **检查扩展是否加载**
   - 打开 Chrome，访问 `chrome://extensions/`
   - 确保 "YouTube English Learner" 扩展已启用
   - 检查是否有错误消息

2. **检查 Content Script 是否运行**
   - 打开 YouTube 视频页面（如 `https://www.youtube.com/watch?v=dQw4w9WgXcQ`）
   - 按 F12 打开开发者工具
   - 切换到 "Console" 标签
   - 查看是否有错误消息
   - 在控制台输入：`document.getElementById("yt-english-learner-btn")`
   - 如果返回 `null`，说明按钮没有创建

3. **检查文件路径**
   - 确保扩展目录结构正确：
     ```
     extension/
     ├── manifest.json
     ├── background.js
     ├── content/
     │   ├── content.js
     │   └── content.css
     └── popup/
         ├── popup.html
         ├── popup.css
         └── popup.js
     ```

4. **重新加载扩展**
   - 在 `chrome://extensions/` 页面
   - 点击扩展的刷新按钮
   - 刷新 YouTube 页面

## 问题 2: 点击生成后无法生成 PDF

### 检查步骤：

1. **检查后端服务器**
   - 运行测试脚本：`python test_railway.py`
   - 或手动测试：访问 `https://your-railway-url.up.railway.app/api/health`

2. **检查 API URL 配置**
   - 点击扩展图标打开 popup
   - 点击 "⚙️ Settings"
   - 检查 "Backend URL" 是否正确
   - 应该是：`https://your-app-name.up.railway.app`

3. **检查控制台错误**
   - 在 YouTube 页面按 F12
   - 查看 Console 标签的错误消息
   - 特别注意 CORS 错误或网络错误

4. **检查 Background Script**
   - 在 `chrome://extensions/` 页面
   - 点击 "Service Worker" 链接
   - 查看后台脚本的控制台错误

## 问题 3: 生成过程中点击其他网页会中断

### 原因分析：

这可能是由于：
1. 浏览器对后台标签页的限制
2. AbortSignal 超时设置（120秒）
3. 消息传递中断

### 检查步骤：

1. **保持标签页活跃**
   - 生成过程中不要切换标签页
   - 不要最小化浏览器

2. **检查超时设置**
   - 在 `background.js` 中，超时设置为 120 秒
   - 如果视频字幕很长，可能需要更长时间

3. **查看错误消息**
   - 如果显示 "Backend offline"，说明连接中断
   - 如果显示 "Generation failed"，说明服务器返回错误

## 调试命令

### 测试本地服务器
```bash
cd d:\code\youtobe-to-book\repo
python server.py
```

### 测试 Railway 连接
```bash
python test_railway.py
```

### 查看扩展日志
1. 打开 `chrome://extensions/`
2. 找到 "YouTube English Learner"
3. 点击 "Service Worker" 查看后台日志
4. 在 YouTube 页面按 F12 查看内容脚本日志

## 常见解决方案

### 如果按钮不出现：
1. 重新加载扩展
2. 刷新 YouTube 页面
3. 检查 manifest.json 格式是否正确

### 如果无法生成 PDF：
1. 确保后端服务器正在运行
2. 检查 API URL 配置
3. 查看控制台错误消息

### 如果生成中断：
1. 保持标签页活跃
2. 检查网络连接
3. 尝试生成较短的视频