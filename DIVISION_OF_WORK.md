# 📋 Phân Chia Công Việc - Dự Án BDS Agent (NHÓM 5 - VSMAC)

Tài liệu này phân chia trách nhiệm cho 5 thành viên để đảm bảo dự án được phát triển toàn diện từ dữ liệu, thuật toán đến giao diện người dùng.

---

### 👤 Thành viên 1: Trưởng nhóm & Kỹ sư Dữ liệu (Backend & Scraper)
**Trọng tâm:** Thu thập và làm sạch dữ liệu.
*   **Nhiệm vụ:**
    *   Phát triển và bảo trì các bộ cào dữ liệu (`agents/`) cho Batdongsan.com.vn, Chotot...
    *   Xử lý các cơ chế vượt chặn (Proxy, User-Agent, Captcha).
    *   Xây dựng hệ thống làm sạch dữ liệu thô (chuẩn hóa giá, diện tích, địa chỉ).
    *   Quản lý tiến độ chung của nhóm.

### 👤 Thành viên 2: Kỹ sư Học máy (ML & Valuation Service)
**Trọng tâm:** Thuật toán định giá và phân tích xu hướng.
*   **Nhiệm vụ:**
    *   Phát triển và tối ưu mô hình **AutoGluon** (`services/ml_service.py`).
    *   Xử lý kỹ thuật đặc trưng (Feature Engineering) từ dữ liệu bất động sản.
    *   Xây dựng API phân tích xu hướng giá theo khu vực và thời gian (`api/routes/analytics.py`).
    *   Đảm bảo độ chính xác của dự báo giá.

### 👤 Thành viên 3: Kỹ sư AI & RAG (LLM & Vector DB)
**Trọng tâm:** Chatbot thông minh và Tìm kiếm ngữ nghĩa.
*   **Nhiệm vụ:**
    *   Quản lý tích hợp **Gemini** và **Ollama** (`services/llm_service.py`).
    *   Phát triển hệ thống tìm kiếm vector với **ChromaDB**.
    *   Thiết kế Prompt Engineering cho chatbot để tư vấn bất động sản chuyên sâu.
    *   Xử lý cơ chế Fallback khi AI gặp lỗi.

### 👤 Thành viên 4: Kỹ sư Frontend (UI/UX & Web)
**Trọng tâm:** Giao diện người dùng và Trải nghiệm.
*   **Nhiệm vụ:**
    *   Phát triển giao diện **Next.js** (Trang chủ, Tìm kiếm, Chi tiết tin đăng).
    *   Thiết kế hệ thống Design System (màu sắc, component, animation).
    *   Đảm bảo trang web hiển thị tốt trên Mobile (Responsive).
    *   Tối ưu tốc độ tải trang và trải nghiệm người dùng (UX).

### 👤 Thành viên 5: Kỹ sư Hệ thống & Phân tích (DevOps & Analytics)
**Trọng tâm:** Cơ sở dữ liệu và Trực quan hóa dữ liệu.
*   **Nhiệm vụ:**
    *   Quản lý cơ sở dữ liệu **PostgreSQL** và **ChromaDB** (Docker).
    *   Xây dựng các biểu đồ phân tích dữ liệu trên Frontend (`components/analytics/`).
    *   Thiết kế và tối ưu hóa các API endpoint (`api/`).
    *   Viết tài liệu kỹ thuật, hướng dẫn sử dụng và báo cáo hệ thống.

---

### 📅 Quy trình phối hợp
1.  **Họp tiến độ**: 2 lần/tuần để cập nhật khó khăn.
2.  **Quản lý Code**: Sử dụng Git, mỗi người làm việc trên một nhánh (branch) riêng trước khi merge vào `main`.
3.  **Kiểm thử**: Thành viên này kiểm tra code cho thành viên kia (Peer Review).

**Phát triển bởi**: NHÓM 5 - VSMAC
