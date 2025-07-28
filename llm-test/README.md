# Qwen3-0.6B 翻译器

基于 llama.cpp 的轻量级多语言翻译工具，使用 Qwen3-0.6B Q8量化模型。

## 🚀 快速开始

### 方法一：使用 Conda (推荐)

```bash
# 1. 创建conda环境
conda create -n translator python=3.10

# 2. 激活环境
conda activate translator

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动翻译器 (首次自动下载模型)
python webui.py
```

### 方法二：直接使用 pip

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动翻译器 (首次自动下载模型)
python webui.py
```

然后在浏览器中访问 http://127.0.0.1:7860

## 功能特性

- 🌐 专业的中英文翻译
- 🎯 专注翻译，轻量高效
- 🔄 中英文双向互译
- ⚡ 本地运行，数据安全
- 🛠️ 基于 llama.cpp，CPU 友好

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 使用说明

1. 首次运行会自动下载模型文件
2. 选择翻译方向 (中→英 或 英→中)
3. 输入要翻译的文本
4. 点击"翻译"按钮或按Enter键

翻译功能：
- 🌐 中英文双向翻译
- 🔄 简单的方向选择
- ⚡ 快速翻译响应
- 🎯 专业翻译质量

## 文件说明

- `webui.py` - Web 翻译界面（集成自动下载）
- `requirements.txt` - 依赖包列表
- `models/` - 模型文件目录（自动创建）

## 系统要求

- Python 3.7+
- 内存: 建议 6GB 以上（Q8量化模型）
- 存储: 约 700MB（模型文件）

## 支持语言

- 🇨🇳 中文 ↔ 🇺🇸 英文

## 注意事项

1. 首次运行需要下载模型文件，请确保网络连接正常
2. 模型文件约700MB（Q8量化），下载可能需要一些时间
3. Q8量化模型提供更高的翻译质量
4. 程序使用 CPU 运行，响应速度取决于 CPU 性能

## 故障排除

### 模型加载失败
- 检查模型文件是否存在于 `models/` 目录
- 确认模型文件完整（重新下载）

### 依赖安装问题
```bash
conda create -n llm-mt python=3.10
conda activate llm-mt
pip install -r requirements.txt
```

### 内存不足
- 减少 `n_ctx` 参数值
- 关闭其他占用内存的程序 