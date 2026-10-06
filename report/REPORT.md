# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Đình Tuấn Anh | 2A202602735 | 100% |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `ag/gemini-3.7-flash-medium` qua OpenAI-compatible API (`LAB_BASE_URL=http://localhost:20128/v1`), `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Linux (Ubuntu 24.04), chạy trực tiếp.
- Số lần chạy tác vụ đã dùng / ngân sách: 15 / 30
- Commit của tag `freeze`: Sẽ điền sau khi tạo tag `freeze`

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): `subagents` sẽ không cải thiện điểm số so với `baseline` trên tác vụ đánh giá (thậm chí có thể giảm từ 10-30% ở các tác vụ code) trong khi chi phí token tăng 20-40%. Căn cứ từ kết quả `code-learn`, việc phân mảnh ngữ cảnh (context fragmentation) giữa coordinator và subagent khiến tác tử chính ỷ lại hoặc không đồng bộ hành động sửa đổi (hiện tượng handoff loss theo Chen et al., 2023).
- H2 (skills-auto so với baseline): `skills-auto` sẽ đạt điểm cao hơn `baseline` trên các tác vụ đánh giá đối với các check quy ước dùng chung giữa hai tập (như type annotations, chuẩn hóa định dạng, sort keys), nhưng không giải quyết được các quy ước hoàn toàn mới xuất hiện riêng ở tác vụ đánh giá. Căn cứ từ lý thuyết procedural memory (Voyager - Wang et al., 2023) và kết quả dev (`code-learn` tăng từ 7/10 lên 9/10), skill giúp chuyển giao quy ước lặp lại nhưng không thể suy đoán quy ước chưa từng xuất hiện.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm trung bình của `skills-auto` trên tác vụ đánh giá sẽ thấp hơn tác vụ học (tồn tại generalization gap). Căn cứ vì tác vụ đánh giá bổ sung các quy ước tổ chức mới mà curator chưa từng thấy trong vết thất bại của tập học; skill được chốt cố định không thể thích ứng với các yêu cầu mới này.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ:
   - Công cụ tệp (file tools): `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`
   - Công cụ shell: `execute`
   - Công cụ đa tác tử: `task`
   Trong đó, công cụ cho phép chạy lệnh trên hệ điều hành là `execute` (thực thi lệnh trong môi trường sandbox cô lập).
2. Mô tả công cụ `task` nêu rõ: `general-purpose` là tác tử đa năng dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm file/nội dung và thực hiện các tác vụ nhiều bước; nó có quyền truy cập toàn bộ các công cụ như tác tử chính. Về ngữ cảnh, subagent là stateless theo mặc định: nó chỉ nhìn thấy prompt/nội dung tác tử chính truyền sang qua tham số gọi công cụ `task`, không thừa kế lịch sử hội thoại của tác tử chính (trừ khi có ghi chú kế thừa riêng), và chỉ trả về một báo cáo kết quả cuối cùng.
3. System prompt mặc định rỗng (`''`). Trích dẫn hướng dẫn hành vi:
   - Từ mô tả công cụ `task`: *"Tell the agent whether to create content, analyze, or only research, since it can't necessarily see the user's intent unless it inherits your conversation, as noted per agent type below."*
   - Từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `data-learn` | `rule_money_in_cents` | E | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667). |
| `data-learn` | `rule_meta_block` | E | RULE: answer.json has an object `meta` = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}. |
| `data-learn` | `rule_clean_csv` | E | RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents. |
| `code-learn` | `rule_type_hints` | E | RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value. |
| `code-learn` | `rule_regression_tests` | E | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass. |
| `code-learn` | `rule_changelog` | E | RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets). |
| `logs-learn` | `rule_service_names` | E | RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service). |
| `logs-learn` | `rule_sorted_errors` | E | RULE: `errors` is sorted by service, then by timestamp_utc, ascending. |
| `logs-learn` | `rule_schema_header` | E | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage". |

Nhận xét:
- **Nhóm lỗi chiếm đa số:** Nhóm E (Vi phạm quy ước tổ chức) chiếm 100% số check thất bại (9/9 check trên cả 3 tác vụ học).
- **Bằng chứng phủ định cho các nhóm A đến D:** Mô hình hoàn thành chính xác 100% các check kỹ thuật thuần túy (18/18 check kỹ thuật đạt: 5/5 ở `data-learn`, 7/7 ở `code-learn`, 6/6 ở `logs-learn`). Mô hình hiểu rõ đề bài, kiểm chứng logic, xử lý dữ liệu bẩn và timezone rất tốt mà không mắc lỗi bỏ qua đặc tả hay vá triệu chứng.
- **Khả năng phòng ngừa của Skill:** Skill hoàn toàn có thể phòng ngừa nhóm lỗi E một cách hiệu quả. Do quy ước tổ chức không được ghi rõ trong đề bài ban đầu nhưng là tri thức thủ tục cố định của tổ chức (Acme conventions), việc curator tự động ghi nhận các quy tắc này vào `SKILL.md` sẽ giúp tác tử đọc được ngay từ đầu và tuân thủ đầy đủ.

## 5. Điều kiện `subagents` (Phần 2.3)

- **Các subagent đã định nghĩa:**
  1. `explorer`: Đọc README, tài liệu, docstring, mẫu dữ liệu và log; báo cáo khách quan về cấu trúc và hiện trạng mà không sửa đổi tệp.
  2. `implementer`: Thực hiện các thay đổi mã nguồn/dữ liệu nhiều bước, chạy test/script kiểm thử qua shell và báo cáo kết quả.
  3. `reviewer`: Kiểm tra độc lập kết quả đầu ra theo đề bài, rà soát các trường hợp biên và quy ước định dạng mà không chỉnh sửa tệp.
- **`subagent_calls` ở từng tác vụ và nhận xét:**
  - `code-learn`: 1 lần gọi (giao việc cho `explorer` khám phá cấu trúc package và lỗi pytest hiện tại).
  - `data-learn`: 2 lần gọi (giao việc khám phá cấu trúc dữ liệu và xử lý các điều kiện lọc).
  - `logs-learn`: 1 lần gọi (giao việc phân tích cấu trúc log và các dòng traceback đa dòng).
  - *Nhận xét:* Tác tử chính đã chủ động tận dụng công cụ `task` trên cả 3 tác vụ học theo khuyến nghị của `SUBAGENTS_NOTE`.
- **Thông tin thiếu hoặc thừa khi giao việc:**
  - Khi giao việc, tác tử chính truyền prompt khá đầy đủ chi tiết kỹ thuật và đường dẫn tương đối chuẩn xác (`workspace/...`). Tuy nhiên, do tính chất cô lập ngữ cảnh (context isolation), subagent chỉ tập trung vào nhiệm vụ hẹp được giao trong prompt.
  - Ở `code-learn`, sau khi nhận báo cáo đầy đủ từ `explorer`, tác tử chính chỉ đọc mã nguồn mà không gọi tiếp `implementer` để ghi đè các sửa đổi, khiến tác vụ kết thúc mà chưa kịp sửa lỗi (chỉ đạt 1/10).
- **Ảnh hưởng đến token và thời gian:**
  - `data-learn`: Token tăng từ 217,135 (`baseline`) lên 262,191 (`subagents`) (+20.7%), thời gian tăng từ 72.7s lên 113.5s do overhead khởi tạo và trao đổi với subagent.
  - `logs-learn`: Token tăng từ 162,508 (`baseline`) lên 196,232 (`subagents`) (+20.8%).
  - Đa tác tử đòi hỏi chi phí token lớn hơn rõ rệt để truyền đạt ngữ cảnh qua lại giữa tác tử chính và các tác tử con.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- **Số lần chạy curator, số skill bị xóa và lý do:** Chạy curator đúng 1 lần (`python -m lab.curator`). Số skill bị xóa: 0 skill. Cả 3 skill sinh ra đều đạt chuẩn `validate_skill`, cấu trúc ngắn gọn dưới 15 dòng, diễn đạt dạng checklist mệnh lệnh tổng quát, không chứa tên file hay ID tác vụ cụ thể.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `code-patch-quality-and-artifacts` | Tổng quát cho các tác vụ sửa lỗi, refactor mã nguồn Python trong codebase. | Đúng hoàn toàn. Hướng dẫn thêm type annotations, viết test regressions riêng, cập nhật changelog và chạy lại test. | 12 dòng (thân 7 dòng). `description`: "Use when fixing bugs, refactoring, or updating functions in a codebase." `skills_read` ở dev: 1. |
| `tabular-data-processing-and-export` | Tổng quát cho việc làm sạch, biến đổi và xuất báo cáo dữ liệu bảng. | Đúng hoàn toàn. Hướng dẫn kiểm tra đơn vị số nguyên/cents, chuẩn hóa ISO-8601 UTC Z, canonical casing, metadata block và header CSV. | 13 dòng (thân 8 dòng). `description`: "Use when cleaning, transforming, or aggregating tabular datasets to produce analysis reports and cleaned exports." `skills_read` ở dev: 2. |
| `log-parsing-and-schema-contracts` | Tổng quát cho việc bóc tách bản ghi log bán cấu trúc sang hợp đồng JSON. | Đúng hoàn toàn. Hướng dẫn đối chiếu schema version, chuẩn hóa snake_case, thời gian UTC, xử lý multiline stack trace và sắp xếp theo khóa. | 13 dòng (thân 8 dòng). `description`: "Use when parsing logs or semi-structured records into structured JSON or data payloads." `skills_read` ở dev: 1. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
