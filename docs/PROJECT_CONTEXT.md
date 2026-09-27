# PROJECT CONTEXT

## Mục tiêu

PM DÒNG TIỀN là CMS quản lý dòng tiền doanh nghiệp.

Bản demo hiện tại tập trung vào:
- đăng nhập CMS;
- Dashboard/Tổng quan;
- danh sách giao dịch;
- thêm/sửa/xóa mềm giao dịch Thu/Chi;
- dashboard tính từ dữ liệu MariaDB.

Các module khác sẽ phát triển sau khi chốt nghiệp vụ với kế toán.

## Stack hiện tại

### Local
- Windows
- Python 3.11.9
- Django 5.0.14
- XAMPP MariaDB 10.4.32
- Local DB: `dongtien`
- `config/settings_local.py`

### Hosting iNET
- Python 3.11
- Django 5.0.14
- MariaDB 10.4.32
- Passenger
- Application root: `/home/vorsnlkqhosting/dongtien`
- Static root: `public/static`

Django 5.0.14 đang được giữ để tương thích MariaDB 10.4.

## Module/data hiện tại

- `Account`
- `Counterparty`
- `Order`
- `Transaction`
- `TransactionEntry`
- Django User

## UI demo hiện tại

Sidebar:
- Tổng quan
- Giao dịch
  - Tất cả giao dịch
  - Thêm giao dịch

Các module khác đang tạm ẩn khỏi sidebar để demo gọn.

## Trạng thái deploy

Đã chạy thành công ở:
- local;
- iNET.

Đã test:
- login;
- dashboard;
- danh sách giao dịch;
- thêm;
- sửa;
- xóa mềm;
- dashboard thay đổi theo giao dịch;
- migrate;
- collectstatic;
- import DB local sang iNET.

## Quy tắc môi trường

Local là source phát triển chính.

Luồng:
`Local -> test -> Git -> deploy -> migrate nếu cần -> collectstatic nếu cần -> restart -> test domain`

## Những việc đang chờ nghiệp vụ

- multi-company;
- định nghĩa chính xác số dư hiện tại;
- giao dịch tương lai;
- APPROVED vs COMPLETED;
- hủy/đảo giao dịch;
- chuyển tiền nội bộ;
- audit kế toán;
- báo cáo chính thức;
- quyền theo vai trò;
- cách xử lý tài khoản inactive.
