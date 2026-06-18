# YouTube English Learner Chrome 扩展

## 安装和启用

### 方法 1: 开发者模式加载（推荐）

1. 打开 Chrome 浏览器
2. 访问 `chrome://extensions/`
3. 打开右上角的 "开发者模式" 开关
4. 点击 "加载已解压的扩展程序"
5. 选择 `extension` 文件夹
6. 扩展应该会显示在列表中

### 方法 2: 从 Chrome 网上应用店安装（如果可用）

*暂未上架*

## 使用方法

### 首次使用配置

1. 点击浏览器工具栏中的扩展图标 📚
2. 点击 "⚙️ Settings"
3. 在 "Backend URL" 中输入：
   ```
   https://web-production-e7326.up.railway.app
   ```
4. 点击 "Save"
5. 应该显示 "✓ Connected"

### 生成 PDF

1. 打开任意 YouTube 视频页面
2. 右下角会出现 "Learn English" 按钮
3. 点击按钮开始生成
4. **重要：生成过程中请不要切换标签页**
5. 生成完成后会自动下载 PDF

## 故障排除

### 按钮不出现

1. 检查扩展是否启用：`chrome://extensions/`
2. 确保在 YouTube 视频页面（URL 包含 `watch?v=`）
3. 刷新页面
4. 查看控制台错误：按 F12 → Console

### 无法生成 PDF

1. 检查后端 URL 配置
2. 测试后端连接：
   ```powershell
   Invoke-WebRequest -Uri "https://web-production-e7326.up.railway.app/api/health"
   ```
3. 应该返回：`{"status":"ok"}`

### 生成中断

**原因：** 浏览器会限制后台标签页的网络请求

**解决方案：**
1. 生成过程中保持 YouTube 标签页活跃
2. 不要最小化浏览器
3. 不要切换到其他标签页

**已优化：**
- 延长超时时间到 3 分钟
- 添加 keep-alive 机制
- 更好的错误提示

## 技术细节

### 架构

```
Content Script (content.js)
    ↓ chrome.runtime.sendMessage
Background Script (background.js)
    ↓ fetch API
Railway 后端 (server.py)
    ↓
YouTube 字幕 → 翻译 → PDF 生成
```

### 文件结构

```
extension/
├── manifest.json          # 扩展配置
├── background.js          # 后台服务（API 调用）
├── content/
│   ├── content.js         # 内容脚本（按钮注入）
│   └── content.css        # 按钮样式
└── popup/
    ├── popup.html         # 弹出窗口界面
    ├── popup.css          # 弹出窗口样式
    └── popup.js           # 弹出窗口逻辑
```

### API 端点

- `GET /api/health` - 健康检查
- `POST /api/generate` - 生成 PDF
- `GET /api/download/{filename}` - 下载 PDF
- `GET /api/history` - 历史记录

## 更新日志

### v1.0.1 (最新)
- ✅ 修复后台标签页生成中断问题
- ✅ 延长超时时间到 3 分钟
- ✅ 添加 keep-alive 机制
- ✅ 改进错误提示信息

### v1.0.0
- 初始版本
- 支持 YouTube 字幕提取
- 中英双语翻译
- PDF 生成和下载