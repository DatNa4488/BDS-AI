# 🏠 BDS Agent - Hệ Thống Tìm Kiếm & Phân Tích Bất Động Sản AI

Hệ thống AI Agent tự động thu thập (scrape), lưu trữ và phân tích tin đăng bất động sản từ nhiều nguồn (Chợ Tốt, Batdongsan.com.vn) sử dụng `browser-use` và LLM (Ollama/Gemini).

Được thiết kế để chạy trên môi trường **Windows** (hoặc Linux/Mac) với Docker cho Database.

---

## 📋 Yêu Cầu Hệ Thống (Prerequisites)

Để chạy được dự án này, bạn cần cài đặt các phần mềm sau:

1.  **Python 3.11+**: [Tải tại đây](https://www.python.org/downloads/) (Nhớ tích chọn "Add Python to PATH").
2.  **Node.js 18+**: [Tải tại đây](https://nodejs.org/en/download/) (Cho Frontend Next.js).
3.  **Docker Desktop**: [Tải tại đây](https://www.docker.com/products/docker-desktop/) (Để chạy PostgreSQL & Redis).
4.  **Ollama** (Tùy chọn nếu chạy Local LLM): [Tải tại đây](https://ollama.ai/).

---

## 🚀 Hướng Dẫn Cài Đặt (Setup Guide)

Làm theo từng bước dưới đây để thiết lập môi trường.

### Bước 1: Chuẩn bị Backend (Python)

Mở **Command Prompt (cmd)** hoặc **PowerShell** tại thư mục gốc của dự án:

```powershell
# 1. Tạo môi trường ảo (Virtual Environment)
python -m venv .venv

# 2. Kích hoạt môi trường ảo
.\.venv\Scripts\activate
# (Nếu lỗi, thử: Set-ExecutionPolicy Unrestricted -Scope Process)

# 3. Cài đặt thư viện Python
pip install -r requirements.txt

# 4. Cài đặt trình duyệt cho AI Scraper
playwright install chromium
```

### Bước 2: Chuẩn bị Frontend (Next.js)

Mở một cửa sổ terminal mới, cd vào thư mục `frontend`:

```powershell
cd frontend

# Cài đặt thư viện Node.js
npm install
```

### Bước 3: Cấu hình Môi trường (.env)

Quay lại thư mục gốc, copy file cấu hình mẫu:

```powershell
copy .env.example .env
```

**Quan trọng**: Mở file `.env` và cập nhật các thông tin sau (nếu dùng dịch vụ đám mây):
- `GEMINI_API_KEY`: Key của Google Gemini (nếu dùng).
- `GROQ_API_KEY`: Key của Groq (nếu dùng).
- `DATABASE_URL`: `postgresql+asyncpg://postgres:postgres123@localhost:5432/bds_agent` (Mặc định cho Docker).

### Bước 4: Khởi động Database (Docker)

Đảm bảo Docker Desktop đang chạy, sau đó chạy lệnh:

```powershell
# Tại thư mục gốc (nơi có file docker-compose.yml)
docker-compose up -d
```
*Lần đầu sẽ mất vài phút để tải PostgreSQL và Redis.*

---

## ▶️ Hướng Dẫn Chạy Hệ Thống

Bạn cần mở **3 cửa sổ Terminal** riêng biệt để chạy hệ thống:

### Terminal 1: Chạy Backend API
```powershell
# Nhớ activate venv trước: .\.venv\Scripts\activate
python main.py api
```
*Server sẽ chạy tại: `http://localhost:8000`*

### Terminal 2: Chạy Frontend Web UI
```powershell
cd frontend
npm run dev
```
*Web sẽ chạy tại: `http://localhost:3000`*

### Terminal 3: Chạy Database & Debug (Tùy chọn)
Dùng để kiểm tra dữ liệu hoặc chạy tool debug:
```powershell
# Activate venv: .\.venv\Scripts\activate
```

---

## 🛠️ Công Cụ Debug & Kiểm Thử

Hệ thống có sẵn các script để bạn kiểm tra tính năng mà không cần dùng Web UI:

### 1. Kiểm tra Scraper (`debug_scraper.py`)
Dùng để chạy thử AI Scraper, kiểm tra xem có lấy được tin đăng không.
```powershell
python debug_scraper.py
```
*Kết quả sẽ hiển thị log chi tiết và lưu tin vào database.*

### 2. Kiểm tra Dữ liệu (`check_db_data.py`)
Xem nhanh số lượng tin đăng đã lưu trong Database.
```powershell
python check_db_data.py
```

### 3. Kiểm tra Dữ liệu Analytics (`debug_analytics_data.py`)
Kiểm tra xem dữ liệu có đủ trường số (giá/m2) để vẽ biểu đồ không.
```powershell
python debug_analytics_data.py
```

---

## ⚠️ Các Lỗi Thường Gặp (Troubleshooting)

1.  **Lỗi `ModuleNotFoundError: No module named 'playwright'`**
    *   👉 Quên kích hoạt venv. Chạy lại: `.\.venv\Scripts\activate`.

2.  **Lỗi Database `Connection refused`**
    *   👉 Docker chưa chạy. Mở Docker Desktop và chạy `docker-compose up -d`.

3.  **Lỗi `npm install` thất bại**
    *   👉 Thử xóa thư mục `frontend/node_modules` và file `frontend/package-lock.json` rồi chạy lại `npm install`.

4.  **Biểu đồ Analytics trống?**
    *   👉 Chạy `python debug_scraper.py` để nạp dữ liệu mẫu.
    *   👉 Refresh trang Frontend (`F5`).

---

**Liên hệ**: [Tên Bạn/Owner] để được hỗ trợ thêm.
