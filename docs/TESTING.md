# TESTING

## Mục tiêu

Tests là lớp kiểm soát để nhiều developer/AI không tạo ra nhiều cách xử lý nghiệp vụ khác nhau.

## Tối thiểu cho mỗi business feature

Phải có test cho:
- happy path;
- validation chính;
- permission nếu có;
- database side effects;
- rollback nếu ghi nhiều bảng;
- hành vi khi soft delete/hủy;
- aggregate/report bị ảnh hưởng.

## Ví dụ giao dịch Thu

Test phải xác nhận tối thiểu:
- Transaction được tạo đúng type/amount/status;
- TransactionEntry được tạo đúng account;
- direction = IN;
- amount entry đúng;
- dashboard/balance phản ánh đúng khi status được tính;
- rollback nếu tạo entry thất bại.

## Regression

Mỗi bug đã sửa nên có test tái hiện bug trước khi/đồng thời sửa.

## Performance test

Không tối ưu dựa vào cảm giác.

Khi dữ liệu lớn:
- đo số query;
- đo thời gian response;
- dùng realistic fixture/data volume;
- xem query plan trước khi thêm index/cache.
