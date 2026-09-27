# CHANGELOG

## 2026-09 — Demo v1

### Environment
- Django 5.0.14.
- Python 3.11.
- MariaDB 10.4.32.
- Local XAMPP.
- iNET Passenger.
- PyMySQL trên shared hosting.

### Database
- Account.
- Counterparty.
- Order.
- Transaction.
- TransactionEntry.
- Decimal cho tiền.
- Soft delete Transaction.

### Transaction
- Danh sách.
- Thêm.
- Sửa.
- Xóa mềm.
- Filter.
- Pagination.
- Thu -> IN.
- Chi -> OUT.
- Tự sinh mã GD.
- Sort `transaction_date DESC, id DESC`.

### Dashboard
- Tổng số dư.
- Tổng thu.
- Tổng chi.
- Dòng tiền ròng.
- Số dư tài khoản.
- Ngày âm tiền.

### UI
- Custom Django Admin.
- Custom header/sidebar.
- Demo chỉ hiển thị Tổng quan + Giao dịch.
- Ẩn các action/nút thừa trong form giao dịch.

### Deployment
- Local và iNET đã chạy.
- Migrate/collectstatic/import DB đã kiểm thử.
