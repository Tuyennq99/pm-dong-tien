# CONTRIBUTING

## Trước khi code

1. Pull code mới nhất.
2. Đọc `AGENTS.md`.
3. Đọc tài liệu domain liên quan.
4. Đọc source + tests hiện tại.
5. Xác định business rule đã `CONFIRMED` hay còn `PENDING`.

## Khi làm feature

- Không tạo implementation song song nếu đã có service chuẩn.
- Không bypass service chỉ vì Admin/API/import khác nhau.
- Không đổi schema ngoài scope.
- Không thêm dependency nếu chưa cần.
- Viết/cập nhật test.

## Trước khi merge

Kiểm tra:
- [ ] Tests pass.
- [ ] Không commit secret.
- [ ] Migration hợp lệ nếu đổi model.
- [ ] BUSINESS_RULES cập nhật nếu đổi nghiệp vụ.
- [ ] DATABASE cập nhật nếu đổi schema.
- [ ] DECISIONS cập nhật nếu đổi kiến trúc.
- [ ] FEATURES cập nhật.
- [ ] CHANGELOG cập nhật khi hoàn thành feature.

## Commit

Ưu tiên commit nhỏ, có ý nghĩa.

Ví dụ:
- `feat: add transaction service`
- `fix: exclude deleted transactions from balance`
- `docs: confirm transfer business rules`
- `test: add transaction rollback tests`
