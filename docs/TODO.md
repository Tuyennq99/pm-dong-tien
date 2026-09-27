# TODO

## Ưu tiên hiện tại
- [ ] Nhận thêm yêu cầu từ kế toán.
- [ ] Chốt lại UI các trang.
- [ ] Giữ demo hiện tại ổn định.

## Sau khi chốt nghiệp vụ
- [ ] Xác định multi-company.
- [ ] Chốt APPROVED/COMPLETED.
- [ ] Chốt xóa/hủy/reversal.
- [ ] Chốt chuyển tiền nội bộ.
- [ ] Chốt account inactive.
- [ ] Chốt báo cáo cần có.

## Kỹ thuật trước production
- [ ] Tách write business logic sang service.
- [ ] Dùng `transaction.atomic()` cho multi-table write.
- [ ] Tối ưu dashboard query.
- [ ] Xác định composite index bằng query thực tế.
- [ ] Audit history.
- [ ] Concurrency/version check khi edit.
- [ ] Role/permission.
- [ ] Secret/env hardening.
- [ ] Backup/restore.
- [ ] Load test.
