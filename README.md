# 🏠 BDS Agent - Hệ Thống Tìm Kiếm & Phân Tích Bất Động Sản AI

Hệ thống AI chuyên nghiệp tự động thu thập (scrape), phân tích và định giá bất động sản. Sử dụng công nghệ Agentic AI với khả năng tự phục hồi và tối ưu hóa dữ liệu.

---

## 🌟 Tính Năng Mới & Cải Tiến

### 1. **Kiến Trúc Hybrid AI (Gemini + Local Ollama)**
Hệ thống sử dụng mô hình AI thông minh nhất (**Gemini 2.0 Flash**) cho các phân tích sâu. Khi gặp lỗi kết nối hoặc hết hạn mức (Quota Exceeded), hệ thống sẽ **tự động chuyển sang Ollama (Qwen 2.5)** chạy cục bộ, đảm bảo hoạt động liên tục 24/7.

### 2. **Professional UI & UX**
- Giao diện **Dark Charcoal & Slate Gradient** sang trọng, hiện đại.
- Chatbot thông minh với khả năng tự xuống dòng và cuộn tin nhắn.
- Module định giá trực quan, tích hợp cả phân tích thị trường từ LLM và dự báo từ AutoML.

### 3. **API v1 Standard**
Tất cả các endpoint đã được chuẩn hóa theo tiền tố `/api/v1/`, giúp việc tích hợp và mở rộng dễ dàng hơn.

---

## 📋 Yêu Cầu Hệ Thống

1.  **Python 3.11+**
2.  **Node.js 18+** (Frontend Next.js)
3.  **Docker Desktop** (Cho PostgreSQL & Redis)
4.  **Ollama** (Bắt buộc cho cơ chế Fallback AI)

---

## 🚀 Hướng Dẫn Cài Đặt

### Bước 1: Backend
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### Bước 2: Frontend
```powershell
cd frontend
npm install
```

### Bước 3: Cấu hình (.env)
Copy file `.env.example` thành `.env` và cập nhật:
- `GEMINI_API_KEY`: Key của Google AI.
- `DATABASE_URL`: Kết nối tới Postgres (mặc định trong Docker).

---

## ▶️ Khởi Động Hệ Thống

### 1. Database (Docker)
```powershell
docker-compose up -d
```

### 2. Backend API
```powershell
python main.py api
```
*API Docs: `http://localhost:8000/docs` (Endpoint v1: `/api/v1/...`)*

### 3. Frontend Web
```powershell
cd frontend
npm run dev
```
*Truy cập: `http://localhost:3000`*

---

## 🛠️ Công Cụ Hữu Ích

- **Cào dữ liệu hàng loạt**: `python bulk_scrape.py`
- **Tìm kiếm tương tác (CLI)**: `python main.py interactive`
- **Chế độ Demo**: `python main.py demo`

---

## ⚠️ Giải Quyết Sự Cố (Troubleshooting)

1.  **Định giá hiện N/A?**
    *   Kiểm tra xem Postgres đã bật chưa (`docker-compose up -d`).
    *   Hệ thống sẽ dùng AutoML dự phòng nếu AI gặp sự cố.
2.  **Chatbot không trả lời?**
    *   Đảm bảo Ollama đang chạy (`ollama serve`) để cơ chế Fallback hoạt động.
3.  **Lỗi kết nối database (WinError 1225)?**
    *   PostgreSQL đang bị tắt hoặc cổng 5432 bị chiếm.

---

**Phát triển bởi**: Antigravity Team

