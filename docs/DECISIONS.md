# ARCHITECTURE DECISIONS

## ADR-001 — Django modular monolith
**Status: ACCEPTED**

Dùng một hệ thống Django modular monolith thay vì microservice.

Lý do:
- phù hợp giai đoạn hiện tại;
- deploy đơn giản;
- transaction DB dễ quản lý;
- dễ chia module;
- có thể tách service sau nếu có nhu cầu thật.

## ADR-002 — Transaction + TransactionEntry
**Status: ACCEPTED**

`Transaction` chứa nghiệp vụ.
`TransactionEntry` chứa biến động tài khoản.

Lý do:
- hỗ trợ IN/OUT rõ ràng;
- mở đường cho chuyển nội bộ;
- tránh thiết kế lại khi một transaction có nhiều entry.

## ADR-003 — Service layer cho write use-case mới
**Status: ACCEPTED**

Feature mới có business logic phải đi qua service.

Code cũ trong Admin được migrate dần khi chạm vào feature liên quan.

## ADR-004 — Selector/query layer cho read phức tạp
**Status: ACCEPTED**

Dashboard, report và list phức tạp không để query phân tán trong template/Admin.

## ADR-005 — Không tối ưu hạ tầng quá sớm
**Status: ACCEPTED**

Chưa dùng Redis/Celery/snapshot/partition chỉ vì “có thể lớn”.

Chỉ thêm sau khi:
- có nhu cầu nghiệp vụ;
- đo được bottleneck;
- hoặc cần background processing thực sự.

## ADR-006 — Django Admin là CMS shell hiện tại
**Status: ACCEPTED**

Tiếp tục custom Django Admin trong giai đoạn hiện tại.

Không rewrite frontend chỉ vì giao diện sẽ lớn hơn.

## ADR-007 — Documentation đi cùng code
**Status: ACCEPTED**

Business rule, database, architecture và feature status phải được commit cùng code liên quan.

Mục tiêu: developer và AI khác đọc repo đều hiểu cùng một dự án.
