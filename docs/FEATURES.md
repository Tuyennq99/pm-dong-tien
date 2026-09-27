# FEATURES

## Dashboard
- [x] Tổng số dư hiện tại
- [x] Tổng thu trong kỳ
- [x] Tổng chi trong kỳ
- [x] Dòng tiền ròng
- [x] Nguồn tiền theo tài khoản
- [x] Danh sách ngày âm tiền
- [ ] Chuẩn hóa tên “Tổng số dư hiện tại”
- [ ] Tối ưu query ngày âm tiền
- [ ] Biểu đồ dòng tiền
- [ ] Dashboard theo company
- [ ] Trang báo cáo chi tiết

## Giao dịch
- [x] Danh sách
- [x] Thêm
- [x] Sửa
- [x] Soft delete
- [x] Filter
- [x] Pagination
- [x] Thu -> IN
- [x] Chi -> OUT
- [ ] Service layer chuẩn
- [ ] transaction.atomic
- [ ] chống ghi đè khi nhiều user cùng sửa
- [ ] import Excel
- [ ] chuyển tiền nội bộ
- [ ] audit history đầy đủ

## Tài khoản
- [x] Model Account
- [ ] UI danh sách chính thức
- [ ] UI thêm/sửa
- [ ] quy tắc đóng/inactive tài khoản
- [ ] lịch sử tài khoản

## Counterparty
- [x] Model
- [ ] UI chính thức
- [ ] báo cáo theo đối tượng

## Order
- [x] Model
- [ ] UI chính thức
- [ ] tổng hợp Thu/Chi theo đơn hàng

## Company
- [ ] Chốt nghiệp vụ
- [ ] Model
- [ ] phân quyền theo company
- [ ] dashboard theo company

## Security / Production
- [ ] DEBUG=False
- [ ] env vars cho secret
- [ ] rotate DB password
- [ ] secure cookies
- [ ] role-based permission
- [ ] backup/restore
- [ ] load test
- [ ] production audit
