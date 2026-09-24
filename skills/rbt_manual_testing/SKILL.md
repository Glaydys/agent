---
name: RBT Manual Testing
description: Skill sinh manual test cases với 2 modes — QUICK (sinh nhanh từ requirements) và FULL RBT (quy trình AI-RBT 6 bước có đánh giá rủi ro). Master skill cho mọi tác vụ manual test case.
---

# RBT Manual Testing

## Description

Đây là **Master Skill** cho mọi tác vụ sinh manual test cases. Skill cung cấp **2 chế độ hoạt động** (modes) để phù hợp với mọi quy mô yêu cầu:

| Mode | Khi nào dùng | Thời gian |
|------|-------------|-----------|
| **QUICK** | Module đơn giản, cần TC nhanh, requirements rõ ràng | 1 lượt (không chờ user) |
| **FULL RBT** | Module phức tạp, cần phân tích rủi ro, hệ thống lớn | 6 bước tuần tự (có checkpoint) |

**Nguyên tắc cốt lõi:**
- **Human Strategy:** Con người xác định chiến lược, mức độ rủi ro và tiêu chuẩn
- **AI Execution:** AI thực hiện phân tích, viết TCs và rà soát lỗ hổng
- **Human Verification:** Con người kiểm tra lại kết quả trước khi chốt

---

## When to Use

Sử dụng skill này khi:

- Sinh manual test cases từ requirements / user stories
- Phân tích requirements để phát hiện ambiguity
- Phân rã hệ thống thành modules / features
- Xây dựng traceability matrix
- Áp dụng Risk-Based Testing (đánh giá rủi ro cho test cases)
- Chuẩn hóa test cases sang bảng Markdown (Jira/Excel format)
- Sinh test cases nhanh từ requirements đơn giản

**KHÔNG** sử dụng skill này khi:

- Cần sinh automation code → dùng `qa_automation_engineer`
- Cần inspect DOM / sinh locator → dùng `ui_debug_agent` / `smart_locator_agent`
- Chỉ cần sinh test data → dùng `test_data_generator`

---

## Mode Routing — Cách chọn mode

Agent tự động chọn mode dựa trên **trigger keywords** và **ngữ cảnh**:

### → Mode QUICK

Kích hoạt khi:
- User dùng workflow `/generate_testcases_from_requirements`
- User nói: "sinh test cases nhanh", "tạo TC từ requirement này", "viết test cases cho form..."
- Requirements đã rõ ràng, scope nhỏ (1 module / 1 tính năng)
- User không yêu cầu phân tích rủi ro hay quy trình bài bản

### → Mode FULL RBT

Kích hoạt khi:
- User dùng workflow `/generate_manual_testcases_rbt`
- User nói: "quy trình 6 bước", "phân tích RBT", "sinh test cases đầy đủ", "sinh bộ TC bài bản"
- Scope lớn (nhiều modules, hệ thống phức tạp)
- User yêu cầu Traceability Matrix hoặc đánh giá Risk Level
- Requirements chưa rõ ràng, cần phân tích Ambiguity

### → Khi không rõ

Nếu không xác định được mode, agent **hỏi user**:
```
Bạn muốn sinh test cases theo chế độ nào?
1. QUICK — Sinh nhanh từ requirements (không qua bước phân tích)
2. FULL RBT — Quy trình 6 bước đầy đủ (phân tích → phân rã → RBT → sinh TC)
```

---

# Mode 1: QUICK — Sinh Test Cases Nhanh

## Mục đích

Sinh test cases **nhanh, đủ chất lượng** từ requirements/user stories đã rõ ràng, phù hợp cho module đơn giản hoặc khi cần kết quả ngay.

## Quy trình (1 lượt duy nhất)

**Agent phải:**

1. **Đọc và hiểu requirements** được cung cấp
2. **Xác định các luồng chính:**
   - Happy Path (luồng chính)
   - Negative Path (dữ liệu sai, thiếu)
   - Boundary Cases (giá trị biên)
3. **Áp dụng kỹ thuật thiết kế test case** tự động:
   - **Equivalence Partitioning (EP):** Chia input thành nhóm tương đương
   - **Boundary Value Analysis (BVA):** Test giá trị tại ranh giới
   - **Decision Table:** Liệt kê tổ hợp điều kiện (nếu có nhiều rules)
   - **State Transition:** Test chuyển đổi trạng thái (nếu có workflow)
4. **Sinh test cases** với đầy đủ fields:
   - TC ID (format: `[DỰ_ÁN]_[MODULE]_TC_[SỐ]`)
   - Module
   - Test Case Title / Test Scenario
   - Pre-conditions
   - Test Steps (đánh số)
   - Expected Results (đánh số tương ứng)
   - Test Data (**phải cụ thể**, không placeholder)
   - Priority (Critical / High / Medium / Low)
5. **Xuất ra bảng Markdown** chuẩn, sẵn sàng copy sang Excel/Jira
6. **Xuất file Excel (.xlsx)** — BẮT BUỘC, xem mục "Auto-Export Excel" bên dưới

## Bảng Output

```
| TC ID | Module | Test Scenario | Pre-Condition | Test Steps | Test Data | Expected Result | Priority |
```

## Auto-Export Excel (BẮT BUỘC — áp dụng cho cả 2 modes)

Sau khi xuất bảng Markdown (QUICK: bước 5 ở trên; FULL RBT: Bước 6 — Template Mapping), agent **PHẢI tự động sinh thêm file `.xlsx`** tương ứng, không cần user yêu cầu lại:

1. Lưu bảng Markdown vừa sinh ra một file `.md` (cùng nơi user yêu cầu output, ví dụ trong folder requirement).
2. Chạy script có sẵn trong skill để convert sang Excel:
   ```
   python .agent/skills/rbt_manual_testing/scripts/md_to_xlsx.py <input.md> <output.xlsx>
   ```
   (script yêu cầu package `openpyxl`; nếu chưa có, cài bằng `pip install openpyxl`)
3. File `.xlsx` đặt cùng tên và cùng thư mục với file `.md` tương ứng.
4. Thông báo cho user đường dẫn cả 2 file (`.md` và `.xlsx`) sau khi hoàn tất.

## Quy tắc Test Data (áp dụng cho cả 2 modes)

```
❌ Sai: "Nhập mã số hợp lệ"
✅ Đúng: "Nhập mã: KH-2026-0012"

❌ Sai: "Nhập email hợp lệ"
✅ Đúng: "Nhập email: test_khachhang_01@domain.com"

❌ Sai: "Nhập giá trị vượt giới hạn"
✅ Đúng: "Nhập 256 ký tự vào trường Name (max: 255)"
```

**Tên đối tượng nghiệp vụ trung lập:** Khi test data cần đặt tên cho một đối tượng nghiệp vụ có thể tùy biến (popup, campaign, sản phẩm, voucher...), dùng tên trung lập dạng `<Đối tượng> A`, `<Đối tượng> B`, `<Đối tượng> C`... thay vì tên gắn với ngữ cảnh marketing/kinh doanh cụ thể (ví dụ tránh "Sale Hè", "Black Friday 2026"). Mục đích: test data không bị hiểu nhầm là nội dung kinh doanh thật, đồng thời vẫn cụ thể/duy nhất để dễ trace giữa các bước test. Vẫn giữ cụ thể các giá trị khác (ngày tháng, số liệu, định dạng...). Áp dụng cho cả 2 modes trừ khi user yêu cầu khác.

## Anti-Patterns (Mode QUICK)

- ❌ Sinh test data chung chung / placeholder
- ❌ Chỉ có Happy Path, thiếu Negative/Boundary
- ❌ Bỏ qua validation rules trong requirements
- ❌ Test Steps mơ hồ ("nhập dữ liệu" → phải ghi rõ nhập gì, ở đâu)

---

# Mode 2: FULL RBT — Quy Trình AI-RBT 6 Bước

## Mục đích

Quy trình bài bản, tuần tự cho module phức tạp. Bao gồm phân tích Ambiguity, phân rã hệ thống, Traceability Matrix, đánh giá Risk Level, và sinh test cases chi tiết.

> ⚠️ **QUAN TRỌNG:** Quy trình này **BẮT BUỘC chạy tuần tự** từng bước. KHÔNG được gộp nhiều bước chạy 1 lần. Mỗi bước phải hoàn thành và được user xác nhận trước khi sang bước tiếp.

> [!NOTE]
> **2 luồng sử dụng riêng biệt:**
> - **Luồng Antigravity (slash command):** Agent thực hiện theo hướng dẫn tổng quát bên dưới. Agent KHÔNG cần đọc file prompt.txt.
> - **Luồng Copy-Paste (ChatGPT/Claude):** QA team copy nội dung prompt chi tiết từ `plans/manual/01-06/prompt.txt` vào chat AI, từng bước một.

### Bước 1: Context & Role-play (Khởi tạo ngữ cảnh)

**Mục đích:** Thiết lập vai trò Senior QA Engineer và nạp bối cảnh dự án.

**Agent phải:**
1. Yêu cầu user cung cấp:
   - Tên dự án / tính năng
   - Mô tả hệ thống hiện tại
   - Mục tiêu kiểm thử MVP
   - Tài liệu yêu cầu (Requirements, User Stories, Figma link, PDF...)
2. Đọc kỹ tài liệu và xác nhận đã hiểu bối cảnh
3. Tóm tắt scope kiểm thử
4. **Chờ user xác nhận** trước khi sang Bước 2

**Output:** Xác nhận hiểu bối cảnh + tóm tắt scope kiểm thử.

---

### Bước 2: Analysis & QnA (Phân tích yêu cầu)

**Mục đích:** Phân tích tài liệu để phát hiện điểm mờ, thiếu sót, mâu thuẫn.

**Agent phải:**
1. Xác định các luồng:
   - Happy Path (luồng chính)
   - Alternate Paths (luồng rẽ nhánh)
   - Exception Paths (luồng ngoại lệ)
2. Phát hiện Ambiguities:
   - Yêu cầu thiếu sót (không quy định độ dài textbox, timeout, hành vi mất kết nối...)
   - Yêu cầu mâu thuẫn
   - Yêu cầu chưa rõ ràng
3. Đặt câu hỏi Q&A có đánh số thứ tự (Q1, Q2...) cho user/PO/BA giải đáp, mỗi câu kèm ngữ cảnh và assumption nếu không được trả lời
4. **DỪNG LẠI — Chờ user trả lời** các câu hỏi trước khi tiếp tục

**Output:** Danh sách luồng + Ambiguities + Câu hỏi Q&A.

> [!IMPORTANT]
> **Đây là điểm nghẽn quan trọng nhất.** Nếu agent bỏ qua bước này và tự đoán logic, test cases sẽ sai nghiêm trọng. Agent PHẢI dừng lại và đợi user phản hồi.

---

### Bước 3: Decomposition (Phân rã hệ thống)

**Mục đích:** Chia tính năng phức tạp thành các Module / Sub-module nhỏ, dễ quản lý.

**Agent phải:**
1. Phân rã theo 1 trong 2 cách:
   - **Theo UI:** Header, Data Table, Form popup, Sidebar...
   - **Theo luồng:** Flow tạo mới, Flow chỉnh sửa, Flow xóa...
2. Mô tả ngắn gọn chức năng từng Module
3. Chỉ ra Dependencies giữa các Module

**Output:** Danh sách Modules/Sub-modules + Dependencies.

---

### Bước 4: Traceability (Đảm bảo độ bao phủ)

**Mục đích:** Thiết lập ma trận truy vết để đảm bảo 100% requirements được phủ test scenarios.

**Agent phải:**
1. Map mỗi Module/Rule với mã Yêu cầu (REQ-01, REQ-02...)
2. Cross-check xem có yêu cầu nào bị thiếu trong danh sách phân rã (Gap Analysis)
3. Liệt kê High-Level Test Scenarios cho từng Module, tập trung:
   - Security / phân quyền
   - UI Validation
   - Business Logic
   - Data Integrity
   - Error Handling
4. **Chờ user review** danh sách scenarios trước khi sinh test case chi tiết

**Output:** Traceability Matrix + High-Level Test Scenarios.

> [!WARNING]
> **Human Checkpoint:** User cần review danh sách scenarios để bổ sung các trường hợp đặc thù mà AI có thể bỏ sót. Đây là bước đánh giá rủi ro do con người thực hiện.

---

### Bước 5: RBT & TC Generation (Sinh Test Case chi tiết)

**Mục đích:** Sinh test cases chi tiết theo chiến lược Risk-Based Testing, đảm bảo độ bao phủ sâu rộng từ chức năng đến giao diện và phi chức năng.

**Agent phải:**
1. Đánh giá Risk Level cho mỗi Module:
   - **High Risk:** Test kỹ, nhiều cases (nghiệp vụ quan trọng, liên quan tiền, bảo mật)
   - **Medium Risk:** Test vừa phải
   - **Low Risk:** Test cơ bản, happy path
2. Sinh test case với đầy đủ các trường thông tin cụ thể (không dùng placeholder chung chung).
3. **BẮT BUỘC bao phủ đa dạng các nhóm kịch bản kiểm thử sau:**
   - **Happy Path & Alternate Paths:** Luồng nghiệp vụ chính và các luồng rẽ nhánh thông thường.
   - **UI/UX & Responsive:** Định dạng hiển thị dữ liệu (ví dụ: `MM:SS`), cảnh báo trực quan bằng màu sắc/nhấp nháy (UX alert), tương thích hiển thị trên Mobile vs Desktop (Responsive), kích thước vùng chạm (touch target) tối thiểu cho nút bấm di động.
   - **Boundary Value Analysis (BVA):** Kiểm thử tại ranh giới thời gian nhạy cảm (ví dụ: giây cuối cùng `00:01`, thời điểm hết hạn `00:00`, ngay sau khi hết hạn).
   - **Race Conditions & Concurrency:** Nhấp đúp chuột (Double click), spam click liên tục vào nút thanh toán/xác nhận, gửi nhiều request đồng thời cho cùng một tài nguyên.
   - **Browser & OS Interactions:** Tải lại trang (F5/Refresh) liên tục, nhấn nút Back/Forward mặc định của trình duyệt, tắt tab trình duyệt hoặc khóa màn hình thiết bị di động rồi mở lại (kiểm tra tính đồng bộ lùi ngầm).
   - **Multi-session / Multi-tab:** Đăng nhập và thực hiện thao tác trên nhiều tab trình duyệt hoặc thiết bị đồng thời để kiểm tra tính toàn vẹn dữ liệu.

> [!NOTE]
> **Không sinh test case nhóm API lỗi/Network (mock 500, timeout, offline, slow 3G...)** trừ khi user yêu cầu riêng cho lần chạy cụ thể — nhóm này không còn nằm trong danh sách bắt buộc mặc định.

4. Áp dụng **kỹ thuật thiết kế test case** phù hợp:
   - **Equivalence Partitioning:** Chia input thành nhóm tương đương, test đại diện mỗi nhóm.
   - **Boundary Value Analysis:** Test giá trị tại ranh giới (min, min+1, max-1, max).
   - **Decision Table:** Liệt kê tổ hợp điều kiện → kết quả (cho logic nhiều điều kiện).
   - **State Transition:** Test chuyển đổi trạng thái hợp lệ + không hợp lệ (cho workflow).
5. Nếu scenarios quá nhiều → sinh từng Module một, hỏi user để tiếp tục.

**Output:** Danh sách Test Cases chi tiết có Risk Level và được phân loại theo Category rõ ràng.

---

### Bước 6: Template Mapping (Chuẩn hóa Format)

**Mục đích:** Đóng gói test cases thành bảng Markdown chuẩn, sẵn sàng copy sang Excel/Jira/TestRail.

**Agent phải:**
1. Chuẩn hóa toàn bộ test cases vào bảng Markdown theo cấu trúc sau:

```
| TC ID | Module | Category | Test Title | Priority | Type | Pre-Condition | Test Steps | Test Data | Expected Result |
```

2. Định nghĩa các cột trong bảng:
   - **TC ID**: Định dạng thống nhất, đánh số tuần tự toàn bộ tài liệu (ví dụ: `TC_001`, `TC_002`...).
   - **Category**: Thể hiện loại test (ví dụ: `Functional`, `UI/UX`, `Edge Case`, `Boundary`, `Browser`, `Multi-session`, `Negative`).
   - **Type**: Phân loại `Positive` hoặc `Negative`.

> [!NOTE]
> Bảng chuẩn KHÔNG còn cột `Status`, `Related BR/Flow`/`Notes`, và `Feature/REQ` — việc map sang mã Yêu cầu (REQ-01...) đã thực hiện riêng ở Traceability Matrix (Bước 4), không lặp lại trong bảng TC. Nếu user yêu cầu khác đi ở lần chạy cụ thể, ưu tiên theo yêu cầu của user tại thời điểm đó.
3. Quy tắc bảng:
   - Test Steps, Pre-Condition và Expected Result phải đánh số cụ thể, dùng `<br>` xuống dòng trong cell.
   - **TUYỆT ĐỐI không được rút gọn hoặc bỏ sót** bất kỳ test case nào đã sinh ở Bước 5.
   - Nếu quá dài → chia thành Part 1, Part 2... và hỏi user để tiếp tục.
4. Xuất output dưới dạng Artifact (`test_cases_<module>.md`).
5. Tự động export thêm file `test_cases_<module>.xlsx` theo hướng dẫn ở mục "Auto-Export Excel".

**Output:** Bảng Test Cases Markdown hoàn chỉnh + file Excel (.xlsx) tương ứng, chuẩn hóa theo mẫu cấu trúc Excel chuyên nghiệp.

---

## Anti-Patterns (NGHIÊM CẤM — áp dụng cho cả 2 modes)

- ❌ Gộp nhiều bước chạy 1 lần trong FULL RBT (PHẢI tuần tự)
- ❌ Tự đoán business logic khi chưa hỏi user (Bước 2 - FULL RBT)
- ❌ Bỏ qua bước phân tích Ambiguity (FULL RBT)
- ❌ Sinh test data chung chung / placeholder
- ❌ Rút gọn hoặc bỏ sót test case khi mapping sang bảng
- ❌ Sinh tất cả test cases 1 lần cho hệ thống lớn (phải chia module)
- ❌ Chỉ có Happy Path, thiếu Negative/Boundary cases (QUICK)
- ❌ Test Steps mơ hồ, không ghi rõ dữ liệu nhập
- ❌ Bỏ qua bước Auto-Export Excel (.xlsx) sau khi sinh bảng Markdown

---

## Prompt Templates

Các prompt template mẫu cho quy trình FULL RBT nằm tại:

```
plans/manual/
├── 01_context_and_roleplay/prompt.txt
├── 02_analysis_and_qna/prompt.txt
├── 03_decomposition/prompt.txt
├── 04_traceability/prompt.txt
├── 05_rbt_and_tc_generation/prompt.txt
└── 06_template_mapping/prompt.txt
```

Agent cần đọc prompt template tương ứng **trước khi** thực hiện mỗi bước (FULL RBT mode).

Mode QUICK không yêu cầu đọc prompt templates — agent áp dụng trực tiếp các kỹ thuật EP/BVA/Decision Table.

---

## Output Format

### Mode QUICK

| Output | Mô tả |
|--------|--------|
| Bảng TC Markdown (`.md`) | Test Cases đầy đủ, sẵn sàng copy sang Excel/Jira |
| File Excel (`.xlsx`) | Auto-export từ file `.md` qua `scripts/md_to_xlsx.py` (BẮT BUỘC) |

### Mode FULL RBT

| Bước | Output |
|------|--------|
| 1 | Xác nhận bối cảnh |
| 2 | Luồng + Ambiguities + Câu hỏi Q&A |
| 3 | Module Decomposition + Dependencies |
| 4 | Traceability Matrix + High-Level Scenarios |
| 5 | Test Cases chi tiết (Risk Level + Test Data) |
| 6 | File Excel (`.xlsx`)
 tự động export |

Tất cả output phải bằng **Tiếng Việt**, format **Markdown**, sử dụng **Artifact** nếu nội dung dài.
