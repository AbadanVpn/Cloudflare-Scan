#  [English](https://github.com/AbadanVpn/Cloudflare-Scanner/blob/main/READMEen.md) -- [Chinese / 中文](https://github.com/AbadanVpn/Cloudflare-Scanner/blob/main/READMEcn.md)
---
# ⚡ Cloudflare Advanced Scanner | اسکنر پیشرفته کلودفلر

<p align="center">
  <img src="https://img.shields.io/github/downloads/AbadanVpn/Cloudflare-Scanner/total?style=for-the-badge&color=orange" alt="Downloads">
  <img src="https://img.shields.io/github/v/release/AbadanVpn/Cloudflare-Scanner?style=for-the-badge&color=green" alt="Release">
  <img src="https://img.shields.io/github/license/AbadanVpn/Cloudflare-Scanner?style=for-the-badge&color=blue" alt="License">
</p>

---

### ✨ ویژگی‌های کلیدی (Key Features)

* **اسکن کاملاً خودکار و هوشمند:** تست و پینگ خودکار رنج‌های رسمی IPv4 و IPv6 کلودفلر بدون نیاز به پیکربندی دستی.
* **رابط کاربری مدرن (Dark Mode):** طراحی زیبا، روان و تیره با استفاده از پتانسیل کامل PySide6 (Qt).
* **سیستم چندزبانه هم‌زمان:** پشتیبانی کامل از زبان‌های **فارسی** و **English** با تغییر آنی چیدمان (RTL/LTR).
* **تست سرعت دانلود واقعی (Speed Test):** امکان سنجش سرعت دانلود آی‌پی‌های تمیز بر اساس مگابایت بر ثانیه.
* **فیلتر منطقه‌ای (Region/IATA Filter):** قابلیت تفکیک و تست آی‌پی‌ها بر اساس دیتاسنترهای خاص کلودفلر (مانند SJC, FRA و...).
* **خروجی آسان:** استخراج لیست آی‌پي‌های تمیز نهایی در قالب فایل متنی (`.txt`) تنها با یک کلیک.
* **توسعه‌یافته به صورت کاملاً آسنکرون (Asyncio):** سرعت فوق‌العاده بالا در اسکن به لطف معماری غیرهمزمان.

---

### 🚀 نحوه اجرا در سیستم خودتان (Local Setup)

اگر تمایل دارید پروژه را مستقیماً از روی سورس‌کد اجرا کنید، مراحل زیر را دنبال کنید:

1. **کلون کردن ریپازیتوری:**
   ```bash
   git clone https://github.com/AbadanVpn/Cloudflare-Scanner.git
   cd Cloudflare-Scanner
   ```

2. **نصب پیش‌نیازها:**
   این پروژه به پایتون نسخه 3.8 یا بالاتر نیاز دارد.
   ```bash
   pip install PySide6 aiohttp
   ```

3. **اجرای برنامه:**
   ```bash
   python main.py
   ```

---

### 📦 دانلود نسخه آماده (Releases)

اگر نیازی به سورس‌کد ندارید و می‌خواهید مستقیماً از برنامه استفاده کنید، به بخش Releases در سمت راست همین صفحه مراجعه کرده و آخرین نسخه کامپایل‌شده فایل `CloudflareScanner.exe` (بدون نیاز به نصب هیچ ابزار جانبی) را دانلود کنید.

---

### 🛠️ ساختار فنی و تکنولوژی‌ها (Technologies)

- Python 3.10+
- PySide6 (Qt for Python) - برای طراحی رابط کاربری (GUI)
- Asyncio & Aiohttp - برای مدیریت کانکشن‌ها به صورت موازی و آسنکرون
- GitHub Actions - برای کامپایل اتوماتیک و انتشار خودکار نسخه EXE

---

### 📝 لایسنس (License)

این پروژه تحت لایسنس MIT منتشر شده است. استفاده، تغییر و بازنشر آن با ذکر نام توسعه‌دهنده کاملاً آزاد است.
