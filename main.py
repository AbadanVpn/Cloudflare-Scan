import sys
import random
import time
import ipaddress
import asyncio
import aiohttp
import socket
import ssl
from datetime import datetime
from typing import List, Optional, Dict
import platform

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QLineEdit, QProgressBar, QVBoxLayout, QHBoxLayout,
    QTextEdit, QComboBox, QFileDialog, QDialog, QDialogButtonBox,
    QScrollArea, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor

# سیستم چندزبانه سراسری
CURRENT_LANG = "fa"

TRANSLATIONS = {
    "fa": {
        "title": "اسکنر پیشرفته کلودفلر",
        "btn_ipv4": "اسکن IPv4",
        "btn_ipv6": "اسکن IPv6",
        "btn_stop": "توقف",
        "btn_area": "تست منطقه",
        "btn_full": "تست کامل",
        "btn_export": "خروجی TXT",
        "placeholder_region": "کد منطقه (مثلا SJC)",
        "label_speed_cnt": "تعداد تست",
        "label_port": "پورت",
        "label_workers": "تردها",
        "label_latency": "حداکثر پینگ",
        "label_lang": "زبان",
        "tab_btn_log": "گزارش‌های زنده اسکن",
        "tab_btn_speed": "لیست آی‌پي‌های تمیز",
        "status_ready": "آماده برای شروع عملیات...",
        "status_speed": "سرعت: {speed:.1f} آی‌پی/ثانیه",
        "status_test_progress": "تست سرعت: {cur} از {total}",
        "log_start_scan": "در حال شروع اسکن IPv{version}...",
        "log_scanning": "در حال اسکن: {cur}/{total} ({ok} آی‌پی یافت شد)",
        "status_scanning": "در حال بررسی رنج‌های IPv{version}...",
        "status_full_testing": "در حال سنجش سرعت دانلود...",
        "status_region_testing": "در حال تست سرعت منطقه {region}...",
        "status_scan_finished": "اسکن با موفقیت پایان یافت",
        "status_test_finished": "تست سرعت پایان یافت",
        "confirm_stop_msg": "آیا از توقف عملیات جاری مطمئن هستید؟",
        "error_threads": "تعداد تردها باید بین ۱ تا ۳۰۰ باشد",
        "error_no_scan_results": "لطفاً ابتدا اسکن را اجرا کنید!",
        "error_speed_count": "تعداد آی‌پی باید بین ۱ تا ۵۰ باشد!",
        "error_no_region": "لطفاً کد منطقه را وارد کنید",
        "dialog_save_title": "ذخیره فایل خروجی",
        "export_success": "لیست آی‌پی‌ها با موفقیت ذخیره شد:\n{fname}",
        "export_status": "خروجی ذخیره شد در: {basename}",
        "export_failed": "خطا در ذخیره فایل: {error}",
        "copy_btn": "کپی آی‌پی",
        "copied_status": "آی‌پی {ip} کپی شد",
        "unknown_region": "منطقه نامشخص",
        "log_gen_ips": "در حال تولید آی‌پي‌های تصادفی از رنج‌های رسمی کلودفلر... (پورت: {port})",
        "log_err_cidr": "خطا در پردازش رنج {cidr}: {e}",
        "log_err_gen_list": "خطا در تولید لیست آی‌پی",
        "log_gen_count": "تعداد {count} آی‌پی تصادفی تولید شد.",
        "log_start_ping": "شروع تست پینگ روی {count} آی‌پی...",
        "log_user_cancel": "عملیات توسط کاربر متوقف شد.",
        "log_scan_err": "خطا در حین اسکن: {e}",
        "log_speed_err_no_ip": "آی‌پی برای تست سرعت یافت نشد.",
        "log_speed_region_start": "شروع تست سرعت منطقه: {region_code} (پورت: {current_port})",
        "log_speed_region_found": "تعداد {count} آی‌پی در این منطقه یافت شد.",
        "log_speed_full_start": "شروع تست سرعت کامل...",
        "log_speed_no_avail_ip": "آی‌پی معتبری پیدا نشد.",
        "log_speed_target_count": "تست سرعت بر روی {count} آی‌پی برتر انجام می‌شود.",
        "log_speed_testing_ip": "[{cur}/{total}] تست سرعت دانلود آی‌پی {ip}",
        "log_speed_fail_ip": "تست سرعت ناموفق برای {ip}",
        "log_speed_ip_res": " نتیجه: {dl_speed} مگابایت/ثانیه",
        "log_speed_all_done": "تست سرعت پایان یافت.",
        "log_summary_no_ip": "\nآی‌پی معتبری یافت نشد.",
        "log_summary_title": "\n=========================\nآمار نهایی اسکن:",
        "log_summary_ipv4": "آی‌پی‌های IPv4 معتبر: {count} عدد",
        "log_summary_ipv6": "آی‌پی‌های IPv6 معتبر: {count} عدد",
        "log_summary_region_stats": "تفکیک منطقه‌ای:",
        "log_summary_region_item": "  {iata}: {cnt} آی‌پی",
        "log_summary_no_region_info": "اطلاعات منطقه‌ای خاصی دریافت نشد.",
        "log_summary_footer": "\nپورت بررسی شده: {port}\nمی‌توانید تست سرعت یا خروجی را شروع کنید.",
        "log_test_done_summary": "\nتست سرعت به پایان رسید!"
    },
    "en": {
        "title": "CloudFlare Advanced Scanner",
        "btn_ipv4": "Scan IPv4",
        "btn_ipv6": "Scan IPv6",
        "btn_stop": "Stop",
        "btn_area": "Region Test",
        "btn_full": "Full Test",
        "btn_export": "Export TXT",
        "placeholder_region": "Region Code (e.g. SJC)",
        "label_speed_cnt": "Test Count",
        "label_port": "Port",
        "label_workers": "Threads",
        "label_latency": "Max Ping",
        "label_lang": "Lang",
        "tab_btn_log": "Live Scan Logs",
        "tab_btn_speed": "Clean IP List",
        "status_ready": "Ready to start...",
        "status_speed": "Speed: {speed:.1f} IP/s",
        "status_test_progress": "Testing: {cur}/{total}",
        "log_start_scan": "Starting IPv{version} scan...",
        "log_scanning": "Scanning: {cur}/{total} ({ok} active found)",
        "status_scanning": "Checking IPv{version} ranges...",
        "status_full_testing": "Measuring download speed...",
        "status_region_testing": "{region} Speed Testing...",
        "status_scan_finished": "Scan completed successfully",
        "status_test_finished": "Speed test finished",
        "confirm_stop_msg": "Are you sure you want to stop the current task?",
        "error_threads": "Threads must be between 1-300",
        "error_no_scan_results": "Please run a scan first!",
        "error_speed_count": "Count must be between 1 and 50!",
        "error_no_region": "Please enter a region code",
        "dialog_save_title": "Save Export File",
        "export_success": "IP list saved successfully:\n{fname}",
        "export_status": "Saved to: {basename}",
        "export_failed": "Export failed: {error}",
        "copy_btn": "Copy IP",
        "copied_status": "IP {ip} copied to clipboard",
        "unknown_region": "Unknown",
        "log_gen_ips": "Generating random IPs from Cloudflare blocks... (Port: {port})",
        "log_err_cidr": "Error processing CIDR {cidr}: {e}",
        "log_err_gen_list": "Failed to generate IP list",
        "log_gen_count": "Generated {count} random IPs.",
        "log_start_ping": "Starting latency test for {count} IPs...",
        "log_user_cancel": "Task stopped by user.",
        "log_scan_err": "Scan error: {e}",
        "log_speed_err_no_ip": "No IPs found for speed testing.",
        "log_speed_region_start": "Starting regional speed test: {region_code} (Port: {current_port})",
        "log_speed_region_found": "Found {count} IPs in this region.",
        "log_speed_full_start": "Starting full speed test...",
        "log_speed_no_avail_ip": "No available IPs found.",
        "log_speed_target_count": "Testing top {count} IPs.",
        "log_speed_testing_ip": "[{cur}/{total}] Testing download for {ip}",
        "log_speed_fail_ip": "Speed test failed for {ip}",
        "log_speed_ip_res": " Result: {dl_speed} MB/s",
        "log_speed_all_done": "Speed test completed.",
        "log_summary_no_ip": "\nNo valid IPs found.",
        "log_summary_title": "\n=========================\nScan Summary Statistics:",
        "log_summary_ipv4": "Valid IPv4 Count: {count}",
        "log_summary_ipv6": "Valid IPv6 Count: {count}",
        "log_summary_region_stats": "Regional Breakdowns:",
        "log_summary_region_item": "  {iata}: {cnt} IPs",
        "log_summary_no_region_info": "No region code data acquired.",
        "log_summary_footer": "\nScanned Port: {port}\nYou can now export or run speed tests.",
        "log_test_done_summary": "\nSpeed test completed!"
    }
}

def t(key, **kwargs):
    text = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["fa"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def get_system_font():
    system = platform.system()
    if system == "Windows":
        return "Segoe UI, Microsoft YaHei, Arial"
    elif system == "Darwin":
        return "SF Pro Display, PingFang SC"
    else:
        return "Ubuntu, DejaVu Sans"

SYSTEM_FONT = get_system_font()

# استایل‌های مدرن حالت تاریک (Dark Mode CSS)
GLOBAL_DARK_STYLE = f"""
    QWidget {{
        background-color: #121214;
        color: #E2E8F0;
        font-family: {SYSTEM_FONT};
    }}
    QLabel {{
        color: #94A3B8;
        font-size: 12px;
    }}
    QLineEdit {{
        background-color: #1E1E24;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 6px 10px;
        color: #F8FAFC;
    }}
    QLineEdit:focus {{
        border: 1px solid #F97316;
    }}
    QComboBox {{
        background-color: #1E1E24;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 5px 10px;
        color: #F8FAFC;
    }}
    QComboBox:focus {{
        border: 1px solid #F97316;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QProgressBar {{
        background-color: #1E1E24;
        border: 1px solid #334155;
        border-radius: 6px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: #22C55E;
        border-radius: 5px;
    }}
    QTextEdit {{
        background-color: #18181C;
        border: 1px solid #1E293B;
        border-radius: 8px;
        color: #38BDF8;
        padding: 10px;
    }}
    QScrollBar:vertical {{
        background: #121214;
        width: 8px;
    }}
    QScrollBar::handle:vertical {{
        background: #334155;
        border-radius: 4px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #475569;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""

CF_IPV4_CIDRS = [
    "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22", "104.16.0.0/13",
	"104.24.0.0/14", "108.162.192.0/18", "131.0.72.0/22", "141.101.64.0/18",
	"162.158.0.0/15", "172.64.0.0/13", "173.245.48.0/20", "188.114.96.0/20",
	"190.93.240.0/20", "197.234.240.0/22", "198.41.128.0/17"
]

CF_IPV6_CIDRS = [
    "2400:cb00:2049::/48", "2400:cb00:f00e::/48", "2606:4700::/32"
]

PORT_OPTIONS = ["443", "2053", "2083", "2087", "2096", "8443"]

def get_iata_translation(iata_code: str) -> str:
    return iata_code if iata_code else t("unknown_region")

async def get_iata_code_async(session: aiohttp.ClientSession, ip: str, timeout: int = 3) -> Optional[str]:
    test_host = "speed.cloudflare.com"
    urls = (f"http://[{ip}]/cdn-cgi/trace", f"https://[{ip}]/cdn-cgi/trace") if ':' in ip else (f"http://{ip}/cdn-cgi/trace", f"https://{ip}/cdn-cgi/trace")
    headers = {"User-Agent": "Mozilla/5.0", "Host": test_host}
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    for url in urls:
        try:
            async with session.get(url, headers=headers, ssl=ssl_ctx if url.startswith('https://') else None,
                                   timeout=aiohttp.ClientTimeout(total=timeout), allow_redirects=False) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    for line in text.strip().split('\n'):
                        if line.startswith('colo='):
                            colo = line.split('=', 1)[1].strip()
                            if colo and colo.upper() != 'UNKNOWN': return colo.upper()
        except Exception: continue
    return None

async def async_tcp_ping(ip: str, port: int, timeout: float = 1.0) -> Optional[float]:
    try:
        start = time.monotonic()
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=timeout)
        latency = (time.monotonic() - start) * 1000
        writer.close()
        await writer.wait_closed()
        return round(latency, 2)
    except Exception: return None

async def measure_tcp_latency(ip: str, port: int, ping_times: int = 2, timeout: float = 1.0) -> Optional[float]:
    latencies = []
    for i in range(ping_times):
        lat = await async_tcp_ping(ip, port, timeout)
        if lat is not None: latencies.append(lat)
        if i < ping_times - 1: await asyncio.sleep(0.05)
    return min(latencies) if latencies else None


class CloudflareScanner:
    def __init__(self, cidrs: List[str], ip_version: int, log_callback=None, progress_callback=None,
                 port=443, max_workers=100, latency_threshold=150):
        self.cidrs = cidrs
        self.ip_version = ip_version
        self.max_workers = max_workers
        self.timeout = 1.0
        self.ping_times = 2
        self.running = True
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.port = port
        self.latency_threshold = latency_threshold

    def generate_ips(self) -> List[str]:
        ip_list = []
        for cidr in self.cidrs:
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                if self.ip_version == 4:
                    for subnet in network.subnets(new_prefix=24):
                        hosts = list(subnet.hosts())
                        if hosts: ip_list.append(str(random.choice(hosts)))
                else:
                    for _ in range(50):
                        rand_int = random.randint(int(network.network_address)+1, int(network.broadcast_address)-1)
                        ip_list.append(str(ipaddress.IPv6Address(rand_int)))
            except Exception: continue
        return ip_list

    async def test_single_ip(self, session: aiohttp.ClientSession, ip: str):
        if not self.running: return None
        latency = await measure_tcp_latency(ip, self.port, self.ping_times, self.timeout)
        if latency is not None and latency < self.latency_threshold:
            iata = None
            if self.running:
                try: iata = await get_iata_code_async(session, ip, self.timeout)
                except Exception: pass
            return {
                'ip': ip, 'latency': latency, 'iata_code': iata,
                'chinese_name': get_iata_translation(iata) if iata else t("unknown_region"),
                'success': True, 'ip_version': self.ip_version, 'port': self.port
            }
        return None

    async def batch_test_ips(self, ip_list: List[str]):
        semaphore = asyncio.Semaphore(self.max_workers)
        family = socket.AF_INET6 if self.ip_version == 6 else socket.AF_INET
        connector = aiohttp.TCPConnector(limit=self.max_workers, force_close=True, enable_cleanup_closed=True, family=family)
        successful = []
        start_time = time.time()
        async with aiohttp.ClientSession(connector=connector) as session:
            async def _test(ip):
                async with semaphore: return await self.test_single_ip(session, ip)
            tasks = [asyncio.create_task(_test(ip)) for ip in ip_list if self.running]
            total = len(tasks)
            completed = 0
            for fut in asyncio.as_completed(tasks):
                if not self.running: break
                result = await fut
                completed += 1
                if result: successful.append(result)
                if completed % 5 == 0 or completed == total:
                    elapsed = time.time() - start_time
                    speed = completed / elapsed if elapsed > 0 else 0
                    if self.progress_callback: self.progress_callback(completed, total, len(successful), speed)
        return successful

    async def run_scan_async(self):
        try:
            if self.log_callback: self.log_callback(t("log_gen_ips", version=self.ip_version, port=self.port))
            ip_list = self.generate_ips()
            if not ip_list: return None
            if self.log_callback:
                self.log_callback(t("log_gen_count", count=len(ip_list), version=self.ip_version))
                self.log_callback(t("log_start_ping", count=len(ip_list), version=self.ip_version))
            return await self.batch_test_ips(ip_list)
        except Exception: return None

    def stop(self): self.running = False


class ScanWorker(QThread):
    progress_update = Signal(int, int, int, float)
    status_message = Signal(str)
    scan_completed = Signal(list)

    def __init__(self, ip_version: int, port=443, max_workers=150, latency_threshold=220):
        super().__init__()
        self.ip_version = ip_version
        self.port = port
        self.max_workers = max_workers
        self.latency_threshold = latency_threshold
        self.scanner = None

    def run(self):
        if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        cidrs = CF_IPV4_CIDRS if self.ip_version == 4 else CF_IPV6_CIDRS
        self.scanner = CloudflareScanner(
            cidrs=cidrs, ip_version=self.ip_version,
            log_callback=lambda msg: self.status_message.emit(msg),
            progress_callback=lambda c, t, s, sp: self.progress_update.emit(c, t, s, sp),
            port=self.port, max_workers=self.max_workers, latency_threshold=self.latency_threshold
        )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(self.scanner.run_scan_async())
            if results is not None: self.scan_completed.emit(results)
        finally: loop.close()

    def stop(self):
        if self.scanner: self.scanner.stop()


class SpeedTestWorker(QThread):
    progress_update = Signal(int, int, float)
    status_message = Signal(str)
    speed_test_completed = Signal(list)

    def __init__(self, results: List[Dict], region_code: str = None, max_test_count=10, current_port=443):
        super().__init__()
        self.results = results
        self.region_code = region_code.upper() if region_code else None
        self.max_test_count = max_test_count
        self.download_time_limit = 3
        self.test_host = "speed.cloudflare.com"
        self.running = True
        self.current_port = current_port

    def download_speed(self, ip: str, port: int) -> float:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = f"GET /__down?bytes=20000000 HTTP/1.1\r\nHost: {self.test_host}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n".encode()
        try:
            if ':' in ip:
                addrinfo = socket.getaddrinfo(ip, port, socket.AF_INET6, socket.SOCK_STREAM)
                sock = socket.socket(addrinfo[0][0], addrinfo[0][1], addrinfo[0][2])
                sock.settimeout(3)
                sock.connect(addrinfo[0][4])
            else:
                sock = socket.create_connection((ip, port), timeout=3)
            ss = ctx.wrap_socket(sock, server_hostname=self.test_host)
            ss.sendall(req)
            start = time.time()
            body = 0
            while time.time() - start < self.download_time_limit:
                buf = ss.recv(8192)
                if not buf: break
                body += len(buf)
            ss.close()
            return round((body / 1024 / 1024) / max(time.time() - start, 0.1), 2)
        except Exception: return 0.0

    def run(self):
        if not self.results:
            self.speed_test_completed.emit([])
            return
        if self.region_code:
            filtered = [r for r in self.results if r.get('iata_code') and r['iata_code'].upper() == self.region_code]
        else:
            filtered = self.results
        if not filtered:
            self.speed_test_completed.emit([])
            return
        filtered.sort(key=lambda x: x.get('latency', float('inf')))
        targets = filtered[:min(self.max_test_count, len(filtered))]
        speed_results = []
        for i, info in enumerate(targets):
            if not self.running: break
            ip = info['ip']
            self.progress_update.emit(i+1, len(targets), 0)
            dl_speed = self.download_speed(ip, self.current_port)
            speed_results.append({'ip': ip, 'download_speed': dl_speed})
        speed_results.sort(key=lambda x: x['download_speed'], reverse=True)
        self.speed_test_completed.emit(speed_results)

    def stop(self): self.running = False


class CustomDialog(QDialog):
    def __init__(self, message: str, buttons: int = QDialogButtonBox.Ok, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setStyleSheet("background-color: #1E1E24; color: #F8FAFC; border: 1px solid #334155; border-radius: 12px;")
        layout = QVBoxLayout(self)
        lbl = QLabel(message)
        lbl.setStyleSheet("color: #E2E8F0; font-size: 13px; border: none;")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setWordWrap(True)
        layout.addWidget(lbl)
        bbox = QDialogButtonBox(buttons)
        bbox.setStyleSheet("QPushButton { background-color: #334155; color: white; padding: 5px 15px; border-radius: 6px; } QPushButton:hover { background-color: #475569; }")
        bbox.setCenterButtons(True)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        layout.addWidget(bbox)
        self.setFixedSize(330, 140)

    @staticmethod
    def warning(parent, msg): CustomDialog(msg, QDialogButtonBox.Ok, parent).exec()
    @staticmethod
    def question(parent, msg): return CustomDialog(msg, QDialogButtonBox.Yes | QDialogButtonBox.No, parent).exec() == QDialog.Accepted


class CloudflareScanUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(460, 780)
        self.setStyleSheet(GLOBAL_DARK_STYLE)
        self.ipv4_scan_worker = None
        self.ipv6_scan_worker = None
        self.speed_test_worker = None
        self.scanning = False
        self.speed_testing = False
        self.scan_results = []
        self.speed_results = []
        self.current_scan_port = 443
        self.init_ui()

    def make_btn(self, text, base_color, hover_color):
        btn = QPushButton(text)
        btn.setFixedHeight(34)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:disabled {{
                background-color: #1E1E24;
                color: #475569;
                border: 1px solid #334155;
            }}
        """)
        return btn

    def init_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(14)

        # لوگو بالای صفحه
        title = QLabel('<span style="color:#F97316; font-weight:bold;">CLOUDFLARE</span> <span style="color:#F8FAFC; font-weight:light;">SCANNER</span>')
        font_title = QFont(SYSTEM_FONT, 20)
        title.setFont(font_title)
        title.setAlignment(Qt.AlignCenter)
        main.addWidget(title)

        # ردیف دکمه‌های اصلی اسکن
        row1 = QHBoxLayout()
        self.btn_ipv4 = self.make_btn("", "#2563EB", "#3B82F6")
        self.btn_ipv4.clicked.connect(lambda: self.start_scan(4))
        self.btn_ipv6 = self.make_btn("", "#16A34A", "#22C55E")
        self.btn_ipv6.clicked.connect(lambda: self.start_scan(6))
        self.btn_stop = self.make_btn("", "#DC2626", "#EF4444")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.confirm_stop)
        row1.addWidget(self.btn_ipv4); row1.addWidget(self.btn_ipv6); row1.addWidget(self.btn_stop)

        # ردیف دکمه‌های خروجی و تست سرعت
        row2 = QHBoxLayout()
        self.btn_area = self.make_btn("", "#DB2777", "#EC4899")
        self.btn_area.setEnabled(False)
        self.btn_area.clicked.connect(self.start_region_speed)
        self.btn_full = self.make_btn("", "#D97706", "#F59E0B")
        self.btn_full.setEnabled(False)
        self.btn_full.clicked.connect(self.start_full_speed)
        self.btn_export = self.make_btn("", "#7C3AED", "#8B5CF6")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self.export_results)
        row2.addWidget(self.btn_area); row2.addWidget(self.btn_full); row2.addWidget(self.btn_export)

        # تنظیمات بالایی ورودی‌ها
        grid1 = QHBoxLayout()
        self.input_region = QLineEdit()
        self.input_region.setFixedHeight(32)
        self.input_region.textChanged.connect(self.auto_uppercase)
        
        self.label_speed_cnt = QLabel()
        self.input_speed_count = QLineEdit("10")
        self.input_speed_count.setFixedWidth(45)
        
        self.label_port = QLabel()
        self.combo_port = QComboBox()
        self.combo_port.addItems(PORT_OPTIONS)
        self.combo_port.setFixedWidth(70)
        
        grid1.addWidget(self.input_region, 1)
        grid1.addWidget(self.label_speed_cnt)
        grid1.addWidget(self.input_speed_count)
        grid1.addWidget(self.label_port)
        grid1.addWidget(self.combo_port)

        # تنظیمات پایینی ورودی‌ها
        grid2 = QHBoxLayout()
        self.label_workers = QLabel()
        self.input_workers = QLineEdit("150")
        self.input_workers.setFixedWidth(50)
        
        self.label_latency = QLabel()
        self.input_latency = QLineEdit("220")
        self.input_latency.setFixedWidth(50)
        
        self.label_lang = QLabel()
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["فارسی", "English"])
        self.combo_lang.setFixedWidth(85)
        self.combo_lang.currentIndexChanged.connect(self.switch_language)
        
        grid2.addWidget(self.label_workers)
        grid2.addWidget(self.input_workers)
        grid2.addWidget(self.label_latency)
        grid2.addWidget(self.input_latency)
        grid2.addStretch()
        grid2.addWidget(self.label_lang)
        grid2.addWidget(self.combo_lang)

        main.addLayout(row1); main.addLayout(row2)
        
        # خط جداکننده دکوراتیو
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #1E293B; max-height: 1px; border: none;")
        main.addWidget(sep)
        
        main.addLayout(grid1); main.addLayout(grid2)

        # نوار پیشرفت عملیات
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        main.addWidget(self.progress_bar)

        # نوار وضعیت زیرین
        status_frame = QHBoxLayout()
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #38BDF8; font-weight: 500;")
        self.speed_label = QLabel("")
        self.speed_label.setStyleSheet("color: #22C55E;")
        status_frame.addWidget(self.status_label); status_frame.addStretch(); status_frame.addWidget(self.speed_label)
        main.addLayout(status_frame)

        # دکمه‌های ناوبری تب‌ها با طراحی کپسولی مدرن
        tab_btn_layout = QHBoxLayout()
        self.tab_btn_log = QPushButton()
        self.tab_btn_log.setFixedHeight(32)
        self.tab_btn_log.setCursor(Qt.PointingHandCursor)
        self.tab_btn_log.clicked.connect(lambda: self.switch_tab(0))
        
        self.tab_btn_speed = QPushButton()
        self.tab_btn_speed.setFixedHeight(32)
        self.tab_btn_speed.setCursor(Qt.PointingHandCursor)
        self.tab_btn_speed.clicked.connect(lambda: self.switch_tab(1))
        
        tab_btn_layout.addWidget(self.tab_btn_log); tab_btn_layout.addWidget(self.tab_btn_speed)
        main.addLayout(tab_btn_layout)

        # صفحات استک (تب‌ها)
        self.stacked = QStackedWidget()
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.stacked.addWidget(self.status_display)

        self.speed_scroll = QScrollArea()
        self.speed_scroll.setWidgetResizable(True)
        self.speed_container = QWidget()
        self.speed_container.setStyleSheet("background-color: #121214;")
        self.speed_layout = QVBoxLayout(self.speed_container)
        self.speed_layout.setContentsMargins(4, 4, 4, 4)
        self.speed_layout.setSpacing(8)
        self.speed_layout.addStretch()
        self.speed_scroll.setWidget(self.speed_container)
        self.stacked.addWidget(self.speed_scroll)
        main.addWidget(self.stacked, 1)

        self.switch_tab(0)
        self.switch_language(0)

    def switch_language(self, index):
        global CURRENT_LANG
        CURRENT_LANG = "fa" if index == 0 else "en"
        self.setLayoutDirection(Qt.RightToLeft if index == 0 else Qt.LeftToRight)
        self.update_ui_texts()

    def update_ui_texts(self):
        self.setWindowTitle(t("title"))
        self.btn_ipv4.setText(t("btn_ipv4"))
        self.btn_ipv6.setText(t("btn_ipv6"))
        self.btn_stop.setText(t("btn_stop"))
        self.btn_area.setText(t("btn_area"))
        self.btn_full.setText(t("btn_full"))
        self.btn_export.setText(t("btn_export"))
        self.input_region.setPlaceholderText(t("placeholder_region"))
        self.label_speed_cnt.setText(t("label_speed_cnt"))
        self.label_port.setText(t("label_port"))
        self.label_workers.setText(t("label_workers"))
        self.label_latency.setText(t("label_latency"))
        self.label_lang.setText(t("label_lang"))
        self.tab_btn_log.setText(t("tab_btn_log"))
        self.tab_btn_speed.setText(t("tab_btn_speed"))
        if not self.scanning and not self.speed_testing:
            self.status_label.setText(t("status_ready"))

    def switch_tab(self, idx):
        self.stacked.setCurrentIndex(idx)
        active = "background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155; border-radius: 6px; font-weight: bold;"
        inactive = "background-color: #1E1E24; color: #64748B; border: 1px solid #1E293B; border-radius: 6px;"
        self.tab_btn_log.setStyleSheet(active if idx == 0 else inactive)
        self.tab_btn_speed.setStyleSheet(active if idx == 1 else inactive)

    def auto_uppercase(self, text):
        if text != text.upper(): self.input_region.setText(text.upper())

    def confirm_stop(self):
        if CustomDialog.question(self, t("confirm_stop_msg")): self.stop_all()

    def start_scan(self, version):
        self.scanning = True
        self.update_ui_state(True)
        self.scan_results = []
        self.clear_speed_cards()
        self.status_display.clear()
        self.status_bar_update(t("status_scanning", version=version))
        port = int(self.combo_port.currentText())
        self.current_scan_port = port
        worker = ScanWorker(version, port=port, max_workers=int(self.input_workers.text() or "150"), latency_threshold=int(self.input_latency.text() or "220"))
        worker.progress_update.connect(self.update_progress)
        worker.status_message.connect(self.update_status)
        worker.scan_completed.connect(lambda res: setattr(self, 'scan_results', [r for r in res if r.get('iata_code')]))
        worker.finished.connect(lambda: self.worker_finished("scan"))
        if version == 4: self.ipv4_scan_worker = worker
        else: self.ipv6_scan_worker = worker
        worker.start()

    def start_full_speed(self):
        self.run_speed_test(None)

    def start_region_speed(self):
        reg = self.input_region.text().strip().upper()
        if not reg: return
        self.run_speed_test(reg)

    def run_speed_test(self, region):
        self.speed_testing = True
        self.update_ui_state(True)
        self.clear_speed_cards()
        self.speed_test_worker = SpeedTestWorker(self.scan_results, region_code=region, max_test_count=int(self.input_speed_count.text() or "10"), current_port=self.current_scan_port)
        self.speed_test_worker.progress_update.connect(self.update_speed_progress)
        self.speed_test_worker.speed_test_completed.connect(self.speed_test_finished)
        self.speed_test_worker.finished.connect(lambda: self.worker_finished("speed"))
        self.speed_test_worker.start()

    def export_results(self):
        if not self.speed_results: return
        fname, _ = QFileDialog.getSaveFileName(self, t("dialog_save_title"), f"clean_ips_{datetime.now().strftime('%Y%m%d')}.txt", "Text Files (*.txt)")
        if not fname: return
        if not fname.endswith('.txt'): fname += '.txt'
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                for r in self.speed_results:
                    f.write(f"{r['ip']}\n")
            CustomDialog.warning(self, t("export_success", fname=fname))
        except Exception as e: self.status_display.append(t("export_failed", error=str(e)))

    def stop_all(self):
        if self.ipv4_scan_worker: self.ipv4_scan_worker.stop()
        if self.ipv6_scan_worker: self.ipv6_scan_worker.stop()
        if self.speed_test_worker: self.speed_test_worker.stop()

    def speed_test_finished(self, results):
        self.speed_results = results
        if not results: return
        self.switch_tab(1)
        for i, r in enumerate(results, 1):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #1E1E24;
                    border: 1px solid #2D2D35;
                    border-radius: 8px;
                }
            """)
            layout = QHBoxLayout(card)
            layout.setContentsMargins(14, 10, 14, 10)
            
            num = QLabel(f"#{i}")
            num.setFixedWidth(26)
            num.setStyleSheet("color: #64748B; font-weight: bold; border: none; background: transparent;")
            
            ip_label = QLabel(r['ip'])
            ip_label.setStyleSheet("color: #F1F5F9; font-size: 13px; font-weight: 600; border: none; background: transparent;")
            
            copy_btn = QPushButton(t("copy_btn"))
            copy_btn.setFixedSize(75, 26)
            copy_btn.setCursor(Qt.PointingHandCursor)
            copy_btn.setStyleSheet("""
                QPushButton {
                    background-color: #334155;
                    color: #E2E8F0;
                    border-radius: 5px;
                    font-size: 11px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #475569;
                    color: white;
                }
            """)
            copy_btn.clicked.connect(lambda _, ip=r['ip']: self.copy_ip(ip))
            
            layout.addWidget(num)
            layout.addWidget(ip_label, 1)
            layout.addWidget(copy_btn)
            self.speed_layout.insertWidget(self.speed_layout.count()-1, card)

    def worker_finished(self, typ):
        if typ == "scan": self.scanning = False
        else: self.speed_testing = False
        if not self.scanning and not self.speed_testing: self.update_ui_state(False)

    def update_ui_state(self, busy):
        self.btn_stop.setEnabled(busy)
        self.btn_ipv4.setEnabled(not busy); self.btn_ipv6.setEnabled(not busy)
        self.btn_full.setEnabled(not busy and bool(self.scan_results))
        self.btn_area.setEnabled(not busy and bool(self.scan_results))
        self.btn_export.setEnabled(not busy and bool(self.speed_results))

    def update_progress(self, cur, total, ok, speed):
        if total: self.progress_bar.setValue(int(cur/total*100))
        self.status_label.setText(t("log_scanning", cur=cur, total=total, ok=ok))
        self.speed_label.setText(t("status_speed", speed=speed))

    def update_speed_progress(self, cur, total, _):
        if total: self.progress_bar.setValue(int(cur/total*100))
        self.status_label.setText(t("status_test_progress", cur=cur, total=total))

    def update_status(self, msg): self.status_display.append(msg)
    def status_bar_update(self, text): self.status_label.setText(text)
    def clear_speed_cards(self):
        while self.speed_layout.count() > 1:
            item = self.speed_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def copy_ip(self, ip):
        QApplication.clipboard().setText(ip)
        self.status_label.setText(t("copied_status", ip=ip))
        QTimer.singleShot(2000, lambda: self.status_label.setText(t("status_ready")))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CloudflareScanUI()
    win.show()
    sys.exit(app.exec())
