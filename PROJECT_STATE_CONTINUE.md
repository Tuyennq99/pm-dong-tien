# PM DÒNG TIỀN — PROJECT STATE / CONTINUE HERE
Cập nhật: 2026-09-27

## Cách dùng khi mở chat mới

Upload file này và gửi:

> Tiếp tục dự án PM Dòng Tiền từ PROJECT_STATE_CONTINUE.md. Đây là trạng thái mới nhất của dự án. Không thiết kế lại từ đầu. Khi sửa code, ưu tiên source/file hiện tại tôi cung cấp hơn nội dung cũ trong context.

---

## 1. Mục tiêu hiện tại

Đang xây CMS quản lý dòng tiền doanh nghiệp bằng Django Admin.

Giai đoạn hiện tại là demo chức năng, chưa production hoàn chỉnh.

Phạm vi đang làm:
- Login CMS
- Tổng quan / Dashboard
- Giao dịch:
  - Tất cả giao dịch
  - Thêm giao dịch
  - Sửa giao dịch
  - Xóa mềm giao dịch
- Dashboard cập nhật theo dữ liệu giao dịch

Chưa triển khai đầy đủ các module khác vì còn chờ nghiệp vụ kế toán và điều chỉnh UI.

---

## 2. Công nghệ / môi trường

### Local
- Windows
- Python 3.11.9
- Django 5.0.14
- XAMPP MariaDB 10.4.32
- Project: `D:\PM quản lý dòng tiền\dongtien`
- Virtualenv: `venv`
- Local DB: `dongtien`
- Local settings: `config/settings_local.py`

### iNET
- Python 3.11
- Django 5.0.14
- MariaDB 10.4.32
- Passenger
- Domain: `https://dongtien.bkapema.vn`
- App root: `/home/vorsnlkqhosting/dongtien`
- Virtualenv: `/home/vorsnlkqhosting/virtualenv/dongtien/3.11/bin/python`
- DB: `vorsnlkqhosting_dongtien`
- Static root: `public/static`

Giữ Django 5.0.14 vì MariaDB 10.4 không phù hợp Django 5.2.

---

## 3. Quy trình phát triển / deploy

Local là source chính.

```text
Sửa local
→ test local
→ upload source lên iNET
→ migrate nếu đổi model
→ collectstatic nếu đổi CSS/JS
→ restart Python App
→ test domain
```

DB local và iNET là riêng biệt.

Khi cần đồng bộ demo DB:
- export local
- drop/import vào DB iNET

Permission iNET:
- folder 755
- file 644
- không dùng 777

---

## 4. Database hiện tại

### Account
- code
- name
- account_type: CASH / BANK / OTHER
- opening_balance
- opening_date
- account_number
- note
- is_active
- timestamps

### Counterparty
- code
- name
- `counterparty_type`
- tax_code
- address
- note
- is_active
- timestamps

Lưu ý: field đúng là `counterparty_type`, không phải `type`.

### Order
- code
- name
- customer
- status
- note
- timestamps

### Transaction
- code
- transaction_date
- transaction_type: INCOME / EXPENSE / TRANSFER
- order
- counterparty
- amount Decimal(20,2)
- description
- status: APPROVED / COMPLETED
- created_at / created_by
- updated_at / updated_by
- is_deleted
- deleted_at
- deleted_by

### TransactionEntry
- transaction
- account
- direction: IN / OUT
- amount Decimal(20,2)
- created_at

Mục tiêu của TransactionEntry:
- Thu → IN
- Chi → OUT
- Sau này chuyển nội bộ có thể dùng:
  - OUT tài khoản nguồn
  - IN tài khoản đích

---

## 5. Logic hiện tại

### Số dư tài khoản
`opening_balance + completed IN - completed OUT`

Không tính:
- transaction chưa COMPLETED
- transaction `is_deleted=True`

### Tổng thu
SUM Transaction.amount với:
- INCOME
- COMPLETED
- không bị xóa
- ngày nằm trong khoảng lọc

### Tổng chi
Tương tự với EXPENSE.

### Dòng tiền ròng
`Tổng thu - Tổng chi`

### Ngày âm tiền
Mỗi ngày trong khoảng chọn:
- tính tổng số dư đến ngày đó
- nếu tổng < 0 → cảnh báo

### Xóa giao dịch
Soft delete, không DELETE vật lý.

### Sort giao dịch
`transaction_date DESC, id DESC`

---

## 6. UI hiện tại

Django Admin được custom thành CMS.

### Root
`/` → `/admin/`

Chưa login:
- Django Admin login

Sau login:
- Tổng quan

### Header
Chỉ giữ:
- username
- logout

Đã ẩn:
- View site
- Change password

### Sidebar demo
```text
Tổng quan

Giao dịch
├── Tất cả giao dịch
└── Thêm giao dịch
```

Các model khác tồn tại nhưng chưa hiển thị thành module riêng.

### Form giao dịch
Đã ẩn:
- nút thêm/sửa/view object liên quan
- Save and add another
- Save and continue editing
- History

Chỉ giữ:
- Lưu
- Delete khi sửa

### Danh sách giao dịch
Có:
- Từ ngày
- Đến ngày
- Thu/Chi
- Tài khoản
- Tình trạng
- Tìm kiếm
- bảng giao dịch
- Sửa/Xóa
- pagination 10 dòng

---

## 7. File quan trọng

```text
dongtien/
├── manage.py
├── passenger_wsgi.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── settings_local.py
│   ├── urls.py
│   └── wsgi.py
├── cashflow/
│   ├── models.py
│   ├── admin.py
│   ├── migrations/
│   ├── templatetags/
│   │   └── dashboard_tags.py
│   └── static/cashflow/css/
│       ├── admin_custom.css
│       ├── admin_dashboard.css
│       └── transaction_list.css
└── templates/admin/
    ├── base_site.html
    ├── index.html
    ├── nav_sidebar.html
    └── cashflow/transaction/change_list.html
```

Không có custom Admin `change_form.html`.
Form thêm/sửa dùng template Admin mặc định + CSS override.

---

## 8. Dashboard hiện tại

Có:
- Dòng tiền hiện tại / thực chất là tổng số dư
- khoảng ngày
- Tổng thu
- Tổng chi
- Dòng tiền ròng
- nguồn tiền các tài khoản
- các ngày âm tiền

Định hướng đã thống nhất:
- Tổng quan không phải bản thu nhỏ đầy đủ của mọi module
- Chỉ hiển thị KPI / cảnh báo / thông tin cần nhìn nhanh
- Chi tiết nằm ở module riêng

Có thể đổi tên:
- “Dòng tiền hiện tại” → “Tổng số dư hiện tại”

---

## 9. Các vấn đề đã phát hiện nhưng CHƯA sửa

1. `account_balance(account)` không truyền `to_date` có thể tính cả giao dịch COMPLETED ở tương lai.
2. Dashboard hiện có thể chỉ lấy `Account.objects.filter(is_active=True)`; cần xác nhận tài khoản inactive có còn được tính hay không.
3. Logic ngày âm tiền hiện có thể query nhiều; ổn cho demo nhưng dữ liệu lớn cần tối ưu.
4. Soft delete phù hợp demo, nhưng production có thể cần hủy/reversal/audit.
5. Cần kế toán chốt rõ APPROVED vs COMPLETED.

Không tự sửa các điểm này trước khi nghiệp vụ được xác nhận.

---

## 10. Multi-company

Đã thống nhất về mặt kỹ thuật là có thể mở rộng sau này bằng `Company`.

Có thể liên kết Company với:
- Account
- Transaction
- Order
- Counterparty

Dashboard có thể lọc:
`Công ty: [Tất cả ▼]`

Nhưng chưa code vì cần nghiệp vụ kế toán.

---

## 11. Bảo mật / scale / nhiều user

Trước production dự kiến cần:
- DEBUG=False
- secret/env vars
- rotate DB password
- HTTPS / secure cookies
- role-based permissions
- `transaction.atomic()` cho ghi nhiều bảng
- chống ghi đè khi nhiều user cùng sửa
- audit log
- tối ưu Dashboard
- composite index theo query thực tế
- backup/restore
- load test
- khi cần mới chuyển shared hosting → VPS
- Redis/Celery chỉ khi thực sự cần

Chưa làm ngay vì còn ở giai đoạn demo.

---

## 12. Kiến trúc tương lai đã thống nhất về nguyên tắc

Khi mở rộng lớn hoặc có nhiều developer:

### Write
`Admin/View/API → Form/Serializer → Service → Model/ORM → DB`

### Read
`Admin/View/API → Selector/Query → ORM → DB`

Mục tiêu:
- tránh mỗi người/ChatGPT code một kiểu
- không nhồi business logic mới vào admin.py
- mỗi nghiệp vụ có một implementation chuẩn

Nhưng CHƯA refactor project hiện tại theo kiến trúc này.

---

## 13. Git / AGENTS / tài liệu cho nhiều ChatGPT

Đã bàn phương án:
- Git repository
- AGENTS.md
- BUSINESS_RULES.md
- ARCHITECTURE.md
- DATABASE.md
- DECISIONS.md
- TESTING.md
- v.v.

Mục tiêu:
- nhiều developer dùng ChatGPT riêng vẫn hiểu cùng project
- cùng quy tắc, cùng kiến trúc, cùng tests

Quyết định hiện tại:
**chưa áp dụng ngay**.

Người dùng muốn hoàn thiện thêm vài chức năng trước, sau đó mới chuyển project sang Git + AI governance.

Không hướng dẫn lại Git trừ khi người dùng yêu cầu.

---

## 14. Cách hỗ trợ code người dùng muốn

- Hướng dẫn ngắn, từng bước.
- Không lan man.
- Nếu sửa code: ưu tiên gửi **nguyên file** để `Ctrl+A → Paste`.
- Giải thích ngắn:
  - file nào sửa
  - sửa để làm gì
  - kết quả mong đợi
- Khi code tiếp, file code hiện tại người dùng cung cấp là nguồn đúng nhất.
- Không dựa hoàn toàn vào phiên bản code cũ trong chat.

---

## 15. Trạng thái ngay lúc tạo file này

- Demo đang chạy ổn local và iNET.
- Chưa muốn chuyển Git/AGENTS ngay.
- Đang chờ thêm thông tin từ kế toán.
- Người dùng còn muốn chỉnh UI và bổ sung nhiều chức năng.
- Có thể tiếp tục code thêm các chức năng hiện tại.
- Nếu cần sửa file nào, nên lấy phiên bản file mới nhất trước khi sửa.

---

## Prompt tiếp tục chuẩn

> Tiếp tục dự án PM Dòng Tiền từ PROJECT_STATE_CONTINUE.md. Đây là trạng thái mới nhất và là điểm tiếp tục của cuộc trao đổi trước. Không thiết kế lại từ đầu. Khi sửa code, ưu tiên source/file hiện tại tôi cung cấp hơn nội dung cũ trong context. Tôi sẽ tiếp tục đưa yêu cầu chức năng từ đây.
