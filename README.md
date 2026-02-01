# 🏠 BDS Agent - Hệ thống tìm kiếm & quản lý tin BĐS tự động

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hệ thống AI Agent tự động thu thập, lưu trữ và tìm kiếm thông tin bất động sản từ nhiều nguồn với khả năng phân tích ngôn ngữ tự nhiên.

## ✨ Tính năng chính

- **🤖 AI Agent thông minh**: Tự động tìm kiếm và thu thập dữ liệu từ nhiều nguồn sử dụng `browser-use`.
- **🌐 Đa nền tảng**: Chợ Tốt, Batdongsan.com.vn, Mogi, Alonhadat, Facebook, Google.
- **✅ Kiểm định dữ liệu**: Tự động kiểm tra số điện thoại, giá hợp lý theo vùng, và phát hiện tin rác/môi giới.
- **🔍 Tìm kiếm ngữ nghĩa**: Tìm kiếm thông minh dựa trên ý nghĩa câu hỏi với ChromaDB.
- **📊 Quản lý & Backup**: Lưu trữ PostgreSQL và tự động đồng bộ lên Google Sheets.
- **🔔 Thông báo**: Cảnh báo tin mới ngay lập tức qua Telegram Bot.
- **🎯 100% FREE stack**: Hỗ trợ Ollama (Local LLM), Groq, và Gemini.

## 🛠️ Tech Stack

| Thành phần | Công nghệ |
| :--- | :--- |
| **LLM** | Ollama (qwen2.5), Groq (Llama 3), Gemini 2.0 |
| **Browser Automation** | browser-use (Playwright) |
| **Backend** | FastAPI |
| **Database** | PostgreSQL |
| **Vector DB** | ChromaDB |
| **Frontend** | Next.js 14 + Shadcn/UI + TailwindCSS |
| **Migrations** | Alembic |
| **Caching** | Redis |
| **Notifications** | Telegram Bot API |

## 📁 Cấu trúc thư mục (Project Structure)

```
agent-bds/
├── main.py                 # Điểm chạy ứng dụng chính (CLI)
├── config.py               # Cấu hình hệ thống (Pydantic Settings)
├── docker-compose.yml      # Cấu hình Docker (PostgreSQL, Redis, Adminer)
├── Makefile                # Lệnh tắt cho phát triển (install, dev, migrate...)
│
├── agents/                 # Logic của AI Agent
│   ├── search_agent.py     # Agent tìm kiếm chính
│   ├── tools.py            # Công cụ tùy chỉnh cho Agent
│   └── prompts.py          # Tập hợp các mẫu câu lệnh AI
│
├── api/                    # Backend API (FastAPI)
│   ├── main.py             # Khởi tạo API Server
│   └── routes/             # Định nghĩa các đầu Endpoint (search, listings...)
│
├── services/               # Các dịch vụ bổ trợ
│   ├── validator.py        # Kiểm định dữ liệu và giá
│   └── telegram_bot.py     # Gửi thông báo qua Telegram
│
├── storage/                # Lưu trữ dữ liệu
│   ├── database.py         # SQLAlchemy (PostgreSQL)
│   ├── vector_db.py        # ChromaDB (Vector Search)
│   └── sheets.py           # Google Sheets API
│
├── frontend/               # Giao diện người dùng (Next.js)
├── alembic/                # Quản lý phiên bản cơ sở dữ liệu
└── scheduler/              # Lập lịch chạy tự động (APScheduler)
```

## 🚀 Hướng Dẫn Cài Đặt (Quick Start)

### 1. Yêu cầu hệ thống
- **Python 3.11+**
- **Docker & Docker Compose** (để chạy DB)
- **Ollama** (để chạy AI model local)
- **Node.js 18+** (cho giao diện web)

### 2. Cài đặt Ollama & Model
```bash
# 1. Tải Ollama tại https://ollama.ai/download
# 2. Tải model khuyến nghị
ollama pull qwen2.5:1.5b
```

### 3. Cài đặt dự án
Sử dụng Makefile để cài đặt nhanh:
```powershell
# Cài đặt tất cả phụ thuộc (Python & Node.js)
make install

# Hoặc cài thủ công:
pip install -r requirements.txt
playwright install chromium
```

### 4. Cấu hình môi trường
```powershell
copy .env.example .env
# Mở .env và điền các API Key nếu cần (Groq, Gemini, Telegram...)
```

### 5. Khởi động hệ thống
```powershell
# Chạy Database (PostgreSQL & Redis)
docker-compose up -d

# Chạy Migrations để tạo bảng
make migrate

# Chạy Backend (API Server)
make backend

# Chạy Frontend (Web UI) - Mở terminal mới
make frontend
```

## 📖 Ví dụ sử dụng

### Chế độ dòng lệnh (CLI)
```powershell
# Chạy demo tìm kiếm
python main.py demo

# Tìm kiếm nhanh
python main.py search "chung cư 2PN Cầu Giấy 2-3 tỷ"
```

### REST API
```bash
# Tìm kiếm qua API
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "nhà riêng Ba Đình dưới 5 tỷ"}'

# Lấy danh sách tin đã lưu
curl http://localhost:8000/api/v1/listings
```

## 🔧 Cấu hình (.env)

| Biến môi trường | Mô tả | Mặc định |
| :--- | :--- | :--- |
| `LLM_MODE` | Chế độ AI (ollama, groq, gemini) | `ollama` |
| `OLLAMA_MODEL` | Tên model Ollama | `qwen2.5:1.5b` |
| `DATABASE_URL` | Kết nối PostgreSQL | `postgresql+asyncpg://...` |
| `HEADLESS_MODE` | Chạy trình duyệt ẩn | `true` |
| `API_PORT` | Cổng chạy Backend | `8000` |

## 🔒 Kiểm định dữ liệu (Data Validation)

Hệ thống thực hiện quy trình kiểm tra nghiêm ngặt:
1. **Trường bắt buộc**: Luôn có URL nguồn, tiêu đề và giá.
2. **Số điện thoại**: Định dạng chuẩn VN, tự động làm sạch.
3. **Giá theo khu vực**: Tự động validate giá m² dựa trên dữ liệu trung bình từng quận (ví dụ: Cầu Giấy 60-180tr/m²).
4. **Chống trùng lặp**: Sử dụng Fingerprint (MD5) để tránh lưu tin trùng.
5. **Lọc tin rác**: Loại bỏ các tin môi giới, ký gửi theo từ khóa.

## 📊 Cấu trúc Listing (Schema)
Dữ liệu được lưu trữ chuẩn hóa dưới dạng JSON:
```json
{
  "title": "Bán chung cư 2PN tại Cầu Giấy",
  "price_number": 3500000000,
  "area_m2": 85.5,
  "location": {
    "district": "Cầu Giấy",
    "city": "Hà Nội"
  },
  "contact": {
    "phone_clean": "0912345678"
  },
  "source_url": "https://...",
  "property_type": "chung cư"
}
```

## 🐳 Triển khai với Docker
```bash
# Build & chạy toàn bộ dịch vụ
make deploy

# Xem logs
make logs
```

## ⚠️ Lưu ý pháp lý
- Công cụ này chỉ dành cho mục đích học tập và nghiên cứu.
- Hãy tuân thủ file `robots.txt` và điều khoản của các website nguồn.
- Không thu thập dữ liệu với tần suất quá cao (sử dụng delay hợp lý).

## 📄 License
MIT License

---
**Được xây dựng với ❤️ bởi cộng đồng AI Việt Nam**
