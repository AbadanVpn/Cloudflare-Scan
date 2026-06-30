# ⚡ Cloudflare 高级扫描器

<p align="center">
  <img src="https://img.shields.io/github/downloads/AbadanVpn/Cloudflare-Scanner/total?style=for-the-badge&color=orange" alt="下载量">
  <img src="https://img.shields.io/github/v/release/AbadanVpn/Cloudflare-Scanner?style=for-the-badge&color=green" alt="最新版本">
  <img src="https://img.shields.io/github/license/AbadanVpn/Cloudflare-Scanner?style=for-the-badge&color=blue" alt="许可证">
</p>

---

### ✨ 主要功能

* **全自动智能扫描：** 自动测试和 Ping Cloudflare 官方 IPv4 和 IPv6 网段，无需手动配置。
* **现代深色界面：** 使用 PySide6 (Qt) 构建的精美、流畅、深色主题界面。
* **双语实时切换：** 完全支持**波斯语**和**英语**，并可即时切换 RTL/LTR 布局。
* **真实下载速度测试：** 以 MB/s 为单位测量干净 IP 的下载速度。
* **区域（IATA）筛选：** 按特定 Cloudflare 数据中心（如 SJC、FRA 等）筛选和测试 IP。
* **一键导出：** 一键将最终干净 IP 列表提取为 `.txt` 文件。
* **全异步（Asyncio）架构：** 借助非阻塞架构实现超快速扫描。

---

### 🚀 本地运行

如果你想直接从源码运行项目，请按照以下步骤操作：

1. **克隆仓库：**
   ```bash
   git clone https://github.com/AbadanVpn/Cloudflare-Scanner.git
   cd Cloudflare-Scanner
   ```

2. **安装依赖：**
   本项目需要 Python 3.8 或更高版本。
   ```bash
   pip install PySide6 aiohttp
   ```

3. **运行程序：**
   ```bash
   python main.py
   ```

---

### 📦 下载编译好的版本

如果你不需要源码，想直接使用程序，请前往页面右侧的 **Releases** 部分，下载最新编译好的 `CloudflareScanner.exe`（无需安装任何额外工具）。

---

### 🛠️ 技术栈

- Python 3.10+
- PySide6（Qt for Python）– GUI 框架
- Asyncio & Aiohttp – 并行异步连接处理
- GitHub Actions – 自动编译和发布 EXE 版本

---

### 📝 许可证

本项目基于 MIT 许可证发布。你可以自由使用、修改和重新分发，只需注明原作者即可。

---

### ❕ 注意：

本项目完全使用 AI 编写。
