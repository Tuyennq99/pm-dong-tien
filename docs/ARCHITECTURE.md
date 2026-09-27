# ARCHITECTURE

## 1. Kiểu kiến trúc

Dự án chọn **Django modular monolith**.

Lý do:
- phù hợp quy mô hiện tại;
- dễ deploy;
- dễ phát triển nhiều module;
- tránh độ phức tạp microservice quá sớm;
- vẫn có thể tách service sau này nếu thực sự cần.

## 2. Kiến trúc cho feature mới

### Write path

```text
Admin / View / API
        ↓
Form / Serializer
        ↓
Service
        ↓
Model / ORM
        ↓
Database
```

Service chịu trách nhiệm:
- business rule;
- transaction boundary;
- tạo/cập nhật nhiều model;
- validation nghiệp vụ không thuộc form đơn thuần;
- side effects nội bộ.

### Read path

```text
Admin / View / API
        ↓
Selector / Query service
        ↓
ORM
        ↓
Database
```

Selector chịu trách nhiệm:
- filter;
- aggregate;
- dashboard query;
- select_related/prefetch_related;
- pagination/query optimization.

## 3. Model

Model chịu trách nhiệm:
- schema;
- FK;
- constraint;
- enum/choices;
- invariant đơn giản;
- method nhỏ gắn trực tiếp với entity.

Không dùng model để chứa workflow dài hoặc logic cross-model phức tạp.

## 4. Admin

Admin chịu trách nhiệm:
- hiển thị;
- form wiring;
- permission UI;
- gọi service;
- gọi selector;
- message/redirect.

Không tiếp tục nhồi business logic mới vào `admin.py`.

Code cũ trong `admin.py` được migrate dần khi có feature liên quan; không refactor toàn bộ chỉ để “đẹp code”.

## 5. Template

Template chỉ hiển thị.
Không tính toán nghiệp vụ lớn trong template.

## 6. Dashboard

Dashboard không tự query từng ngày × từng tài khoản theo kiểu N×M khi dữ liệu tăng.

Hướng chuẩn:
- aggregate query;
- query tối thiểu;
- chỉ thêm snapshot/cache sau khi đo được bottleneck.

## 7. Module hóa tương lai

Khi dự án lớn, ưu tiên tách theo domain, ví dụ:

```text
apps/
  cashflow/
  accounts/
  counterparties/
  orders/
  companies/
  users/
```

Không tách app chỉ vì file dài. Tách khi domain có trách nhiệm và vòng đời riêng rõ ràng.

## 8. Service API nội bộ

Ví dụ định hướng:

```python
create_transaction(...)
update_transaction(...)
void_transaction(...)
transfer_between_accounts(...)
```

UI/Admin/API đều gọi cùng service để tránh mỗi nơi triển khai một kiểu.

## 9. Consistency

Một use-case chỉ có một implementation chuẩn.

Không cho phép:
- Admin tự lưu TransactionEntry;
- API lại dùng service;
- import Excel lại dùng logic riêng.

Tất cả phải hội tụ vào cùng service.
