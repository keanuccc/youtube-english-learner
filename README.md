# YouTube English Learning PDF Generator

将 YouTube 视频字幕提取为中英双语 PDF，方便做笔记学英语。

## 使用方法

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（直接传入 YouTube 链接）
python main.py https://www.youtube.com/watch?v=VIDEO_ID

# 或交互式输入
python main.py
```

## 配置

复制 `.env.example` 为 `.env`，填入你的 API Key：

```
DEEPSEEK_API_KEY=your_key_here
SUPADATA_API_KEY=your_key_here
```

## 输出

PDF 文件保存在 `output/` 目录，格式为：
- 每句英文（14pt 加粗）+ 空白行 + 中文翻译（11pt 灰色）
- 句与句之间有分隔线和大留白，方便做笔记

## 项目结构

```
├── main.py              # 入口脚本
├── get_transcripts.py   # 字幕提取（Supadata API）
├── translate.py         # 双语翻译（DeepSeek）
├── generate_pdf.py      # PDF 生成（fpdf2）
├── output/              # 生成的 PDF
└── .env                 # API Key 配置
```
