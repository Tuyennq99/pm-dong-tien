# CODING STANDARDS

## 1. Nguyên tắc

Ưu tiên:
1. đúng nghiệp vụ;
2. dễ đọc;
3. dễ test;
4. ít coupling;
5. tối ưu khi có số liệu đo.

Không viết code “thông minh” nếu làm khó bảo trì.

## 2. Naming

- Model: danh từ số ít, PascalCase.
- Service function: động từ + đối tượng.
  - `create_transaction`
  - `update_transaction`
  - `void_transaction`
- Selector:
  - `get_transactions`
  - `get_dashboard_summary`
- Boolean:
  - `is_deleted`
  - `is_active`
  - `has_*`

## 3. Function

Một function nên có một trách nhiệm rõ ràng.

Nếu function:
- query DB;
- validate nghiệp vụ;
- ghi nhiều model;
- format output;
- gửi side effect

cùng lúc, cần xem xét tách.

## 4. ORM

Ưu tiên Django ORM.

- dùng `select_related()` cho FK/one-to-one;
- dùng `prefetch_related()` cho reverse/many-to-many;
- tránh query trong loop;
- aggregate ở DB khi hợp lý;
- pagination cho list lớn.

## 5. Transaction

Nếu một use-case ghi nhiều bảng:
```python
from django.db import transaction

with transaction.atomic():
    ...
```

Rollback toàn bộ nếu một bước thất bại.

## 6. Validation

- Form/Serializer: format/input validation.
- Service: business validation.
- Database constraint: invariant bắt buộc.

Không dựa duy nhất vào UI validation.

## 7. Error handling

- Không `except Exception: pass`.
- Không nuốt lỗi.
- Error message cho user phải dễ hiểu.
- Log phải đủ để debug nhưng không chứa secret.

## 8. Money

- `Decimal`.
- Không dùng float.
- Không convert qua float để tính toán.

## 9. Date/time

- Dùng timezone-aware datetime theo Django.
- Phân biệt rõ `transaction_date` với `created_at`.

## 10. Refactor

Không refactor diện rộng trong PR/commit feature nhỏ nếu không cần.
Nếu cần refactor lớn, tách riêng để dễ review.
