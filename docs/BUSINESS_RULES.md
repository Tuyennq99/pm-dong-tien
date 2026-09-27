# BUSINESS RULES

Mỗi rule có trạng thái:

- `CONFIRMED`: đã chốt, có thể dùng để code.
- `PENDING`: chưa đủ thông tin, không được tự suy diễn.

## Giao dịch

### BR-001 — Thu / Chi
**Status: CONFIRMED**

- `INCOME` là Thu.
- `EXPENSE` là Chi.
- `TRANSFER` dành cho tương lai.

### BR-002 — TransactionEntry
**Status: CONFIRMED**

Trong demo hiện tại:
- Thu -> một entry `IN`.
- Chi -> một entry `OUT`.

### BR-003 — Số dư tài khoản
**Status: CONFIRMED cho demo**

Công thức:
`opening_balance + completed IN - completed OUT`

Không tính giao dịch:
- `is_deleted=True`;
- chưa `COMPLETED`.

### BR-004 — Dòng tiền ròng
**Status: CONFIRMED**

`Tổng thu trong kỳ - Tổng chi trong kỳ`

### BR-005 — Xóa giao dịch
**Status: CONFIRMED cho demo, PENDING cho production**

Hiện tại dùng soft delete:
- `is_deleted=True`
- `deleted_at`
- `deleted_by`

Production cần kế toán xác nhận có chuyển sang hủy/reversal hay không.

### BR-006 — Mã giao dịch
**Status: CONFIRMED**

Nếu chưa có mã, Admin hiện tự sinh dạng:
`GD{pk:06d}`

### BR-007 — Thứ tự danh sách
**Status: CONFIRMED**

`transaction_date DESC, id DESC`

## Cần kế toán xác nhận

### BR-P01 — COMPLETED có ngày tương lai
**Status: PENDING**

Cần chốt giao dịch `COMPLETED` nhưng `transaction_date > today` có được tính vào “số dư hiện tại” hay không.

### BR-P02 — APPROVED vs COMPLETED
**Status: PENDING**

Cần định nghĩa rõ ý nghĩa nghiệp vụ và quyền chuyển trạng thái.

### BR-P03 — Hủy/đảo giao dịch
**Status: PENDING**

Chưa chốt:
- có được sửa giao dịch COMPLETED;
- có được soft delete;
- có cần reversal entry.

### BR-P04 — Multi-company
**Status: PENDING**

Chưa chốt:
- tài khoản thuộc một hay nhiều công ty;
- giao dịch cross-company;
- báo cáo hợp nhất;
- quyền user theo company.

### BR-P05 — Tài khoản inactive
**Status: PENDING**

Cần chốt tài khoản inactive có còn được tính vào báo cáo/số dư lịch sử hay không.

### BR-P06 — Chuyển tiền nội bộ
**Status: PENDING**

Định hướng kỹ thuật:
- 1 Transaction;
- OUT tài khoản nguồn;
- IN tài khoản đích;
- tổng tiền toàn công ty không đổi.

Chỉ code sau khi nghiệp vụ xác nhận.
