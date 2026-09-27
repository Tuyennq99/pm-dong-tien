# DATABASE

## Database hiện tại

MariaDB 10.4.32.

## Model chính

### Account

Mục đích: nguồn tiền.

Field quan trọng:
- code
- name
- account_type
- opening_balance
- opening_date
- account_number
- note
- is_active
- timestamps

### Counterparty

Mục đích: người gửi / người nhận.

Field:
- code
- name
- counterparty_type
- tax_code
- address
- note
- is_active
- timestamps

Lưu ý:
Tên field đúng là `counterparty_type`, không phải `type`.

### Order

Field:
- code
- name
- customer
- status
- note
- timestamps

### Transaction

Field:
- code
- transaction_date
- transaction_type
- order
- counterparty
- amount
- description
- status
- created_at / created_by
- updated_at / updated_by
- is_deleted
- deleted_at
- deleted_by

### TransactionEntry

Field:
- transaction
- account
- direction
- amount
- created_at

## Nguyên tắc dữ liệu

- Tiền dùng `Decimal`.
- Amount phải > 0.
- FK phải dùng deletion policy rõ ràng.
- Không để Transaction và TransactionEntry lệch dữ liệu.
- Multi-row write phải atomic.
- Không thêm index hàng loạt theo cảm tính.

## Index

Hiện có index cơ bản cho một số trường Transaction.

Khi có dữ liệu/query thực tế, đánh giá composite index theo:
- date;
- status;
- is_deleted;
- transaction_type;
- account;
- company trong tương lai.

Index phải dựa trên query plan/load test, không tối ưu mù.

## Multi-company tương lai

Định hướng có thể thêm `Company`, sau đó xem xét FK vào:
- Account;
- Transaction;
- Order;
- Counterparty.

Chưa implement trước khi business rule được chốt.

## Audit

Hiện có created/updated/deleted metadata.

Audit history đầy đủ (old value/new value) chưa có.
Đây là yêu cầu production cần xem xét.
