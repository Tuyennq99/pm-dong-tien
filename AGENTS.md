# PM DÒNG TIỀN — AI / DEVELOPER RULES

Tài liệu này là điểm bắt đầu bắt buộc cho mọi AI hoặc developer tham gia dự án.

## 1. Thứ tự phải đọc trước khi sửa code

1. `docs/PROJECT_CONTEXT.md`
2. `docs/BUSINESS_RULES.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DATABASE.md`
5. `docs/CODING_STANDARDS.md`
6. `docs/DECISIONS.md`
7. Source code thực tế liên quan trực tiếp đến yêu cầu
8. Tests liên quan

Không được sửa code chỉ dựa trên lịch sử chat.

## 2. Thứ tự ưu tiên khi nguồn thông tin mâu thuẫn

- Business rule đã được đánh dấu `CONFIRMED` là yêu cầu nghiệp vụ.
- Source code + migration + tests phản ánh hệ thống đang chạy thực tế.
- Nếu tài liệu và code mâu thuẫn: KHÔNG tự đoán. Phải chỉ ra mâu thuẫn trước khi thay đổi.
- Nội dung chat cũ có độ ưu tiên thấp nhất.

## 3. Kiến trúc bắt buộc cho code mới

Dự án dùng **Django modular monolith**.

### Write path
`Admin/View/API -> Form/Serializer -> Service -> Model/ORM -> Database`

### Read path
`Admin/View/API -> Selector/Query service -> ORM -> Database`

Quy tắc:
- Không đặt business logic mới trực tiếp trong template.
- Không nhồi business logic mới vào `admin.py`.
- Không dùng `model.save()` để chứa use-case phức tạp.
- Các thao tác ghi nhiều bảng phải đi qua service và dùng `transaction.atomic()`.
- Query tổng hợp/phức tạp phải gom vào selector/query layer.
- Không tạo microservice chỉ vì dự án lớn hơn.
- Không thêm Redis/Celery/snapshot/partition nếu chưa có nhu cầu đo được.

## 4. Quy tắc thay đổi

Mỗi thay đổi phải:
1. Đọc code hiện tại trước.
2. Chỉ sửa phạm vi cần thiết.
3. Không refactor lớn ngoài yêu cầu nếu chưa được duyệt.
4. Nếu đổi nghiệp vụ -> cập nhật `BUSINESS_RULES.md`.
5. Nếu đổi database/schema -> cập nhật `DATABASE.md`.
6. Nếu đổi kiến trúc -> cập nhật `DECISIONS.md`.
7. Nếu thêm/xóa chức năng -> cập nhật `FEATURES.md`.
8. Nếu hoàn thành feature -> cập nhật `CHANGELOG.md`.
9. Bổ sung hoặc cập nhật tests tương ứng.

## 5. Quy tắc dữ liệu tài chính

- Dùng `Decimal`, không dùng `float` cho tiền.
- Không hard delete `Transaction` nếu nghiệp vụ hiện hành chưa cho phép.
- Không để `Transaction` và `TransactionEntry` lệch số tiền.
- Không tự suy diễn cách hủy/đảo giao dịch nếu kế toán chưa chốt.
- Không tự thêm logic multi-company nếu nghiệp vụ chưa chốt.
- Không tự thay đổi ý nghĩa `APPROVED`, `COMPLETED`.

## 6. Quy tắc bảo mật

- Không hard-code SECRET_KEY, DB password, token, credential.
- Không commit `settings_local.py` hoặc secret.
- Không log thông tin nhạy cảm.
- Không tắt CSRF/security middleware để sửa lỗi tạm.
- Không dùng permission 777.
- Không bypass kiểm tra version DB/framework.

## 7. Dependency

Không thêm dependency mới nếu chưa:
- giải thích vì sao cần;
- kiểm tra có thể dùng Django/Python built-in hay không;
- đánh giá ảnh hưởng deploy.

## 8. Khi chưa rõ nghiệp vụ

Dừng ở mức thiết kế và ghi `PENDING`.
Không tự biến giả định thành code production.

## 9. Mục tiêu nhất quán

Các AI/developer có thể viết khác nhau ở chi tiết nhỏ, nhưng phải thống nhất:
- cấu trúc module;
- luồng write/read;
- naming;
- business rule;
- transaction boundary;
- validation;
- error handling;
- tests;
- tài liệu.
