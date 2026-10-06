# Báo cáo Lab: Self evolving Agentic


## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Đình Tuấn Anh | 2A202602735 | 100% |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `ag/gemini-3.7-flash-medium` qua OpenAI-compatible API (`LAB_BASE_URL=http://localhost:20128/v1`), `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Linux (Ubuntu 24.04), chạy trực tiếp.
- Số lần chạy tác vụ đã dùng / ngân sách: 21 / 30
- Commit của tag `freeze`: `25d1f5d`

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

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 1/10 | 1/10 |
| data-learn | 5/8 | 5/8 | 5/8 |
| logs-learn | 6/9 | 6/9 | 6/9 |
| code-eval | 7/11 | 7/11 | 8/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 0/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.66 | 0.46 | 0.46 |
| **Mean score - evaluation tasks** | 0.40 | 0.60 | 0.63 |
| **Mean tokens per run** | 188,127 | 261,902 | 211,021 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

Thống kê phân rã check từ `scripts/check_breakdown.py`:
```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     12/18         0/12         173,054      0/3     
baseline      learn    18/18         0/9          203,201      0/3     
subagents     eval     18/18         0/12         329,751      0/3     
subagents     learn    12/18         0/9          194,054      0/3     
skills-auto   eval     18/18         1/12         293,871      3/3     
skills-auto   learn    12/18         0/9          128,170      3/3     
```

Các lần chạy có ngoại lệ và kiểm tra tính toàn vẹn:
- `baseline` ở `code-eval`: Chạm giới hạn đệ quy (`GraphRecursionError: Recursion limit of 60 reached`). Dù dừng đệ quy, các file sửa đổi đã được ghi vào workspace từ các bước trước nên harness vẫn chấm được 7/11 check đạt.
- `subagents` ở `logs-eval`: Chạm giới hạn đệ quy 60 bước sau khi trao đổi đa tác tử; mã nguồn đã xử lý được 6/10 check đạt.
- Cả hai lỗi trên được cơ chế bắt ngoại lệ trong `run_task` lưu vào trường `error` của `run.json` một cách an toàn mà không làm đứt gãy luồng chạy.
- Toàn bộ 6/6 lần chạy chính thức của `skills-auto` đều có `skills_modified = false` và `skills_sha256` khớp 100% với mã băm đóng băng (`835eb191...`), được kiểm chứng tự động bằng `scripts/verify_freeze.py` (báo `OK`).

## 8. Phân tích

1. **So sánh điểm tập học và tập đánh giá:**
   - Tập học: `baseline` đạt điểm trung bình 0.66. Ở giai đoạn dev (Phần 3.4), `skills-auto` đạt 0.73 (nhờ `code-learn` tăng từ 7/10 lên 9/10). Lần chạy chính thức sau đóng băng của `skills-auto` đạt 0.46 do phương sai ngẫu nhiên khiến `code-learn` dừng sớm (1/10). `subagents` chỉ đạt 0.46 do gặp lỗi mất mát phối hợp ở `code-learn`.
   - Tập đánh giá: `skills-auto` đạt 0.63 (cao nhất trong cả 3 điều kiện), tiếp theo là `subagents` (0.60), và thấp nhất là `baseline` (0.40). Trên `code-eval`, `skills-auto` là điều kiện duy nhất đạt 8/11 điểm (nhờ thêm `rule_type_hints`).
   - Không có hiện tượng "học tủ" (chỉ tăng tập học mà thụt lùi tập đánh giá). Thay vào đó, `skills-auto` cho thấy khả năng transfer tích cực sang các tác vụ mới.

2. **Phân rã điểm kỹ thuật và quy ước (`rule_`):**
   - Check kỹ thuật: Cả `skills-auto` và `subagents` đều đạt tuyệt đối 18/18 (100%) trên tập đánh giá, trong khi `baseline` chỉ đạt 12/18 (do thất bại hoàn toàn ở `logs-eval`). Điều này chứng minh năng lực lập trình và suy luận logic của mô hình là rất tốt khi có đủ ngữ cảnh hoặc chỉ dẫn.
   - Check quy ước (`rule_`): Skill tự sinh giúp đạt quy ước thủ tục chung (`rule_type_hints` ở `code-eval`). Tuy nhiên, các quy ước hoàn toàn mới xuất hiện ở tập đánh giá (`rule_version_bump` ở code, `rule_sorted_keys_format` ở data, `rule_source_line` ở logs) không được skill hỗ trợ vì chúng chưa từng xuất hiện trong vết thất bại của tập học để curator có thể học và mã hóa vào checklist.

3. **Bằng chứng từ vết thực thi (`trace.md`) và `skills_read`:**
   - *Check được skill giúp đạt:* `rule_type_hints` ở `code-eval`. Vết cho thấy tác tử gọi `read_file` đọc skill `skills/auto/code-patch-quality-and-artifacts/SKILL.md` ngay từ đầu, sau đó tuân thủ bước 2 trong checklist để bổ sung toàn bộ type annotations vào các hàm công khai của `inventory`, nhờ đó vượt qua bài kiểm tra mà không bỏ sót.
   - *Check skill không giúp:* `rule_clean_csv` ở `data-eval`. Mặc dù skill `tabular-data-processing-and-export` có nhắc quy chuẩn xuất file CSV sạch, nhưng trong đề bài người dùng (`instruction.md`) chỉ yêu cầu trả lời câu hỏi vào `answer.json`. Tác tử ưu tiên tuân thủ chặt chẽ đề bài người dùng hơn là tự ý sinh ra các file phụ trợ nằm ngoài yêu cầu trực tiếp.

4. **Phân tích chi phí và hiệu quả token:**
   - Chi phí token trung bình: `baseline` tốn 188k token/lượt; `skills-auto` tốn 211k token/lượt (+12.2%); `subagents` tốn tới 262k token/lượt (+39.2%).
   - Tỷ số hiệu quả (Điểm đánh giá / 100k token): `skills-auto` đạt **0.299** điểm/100k token, vượt trội hơn `baseline` (0.213) và `subagents` (0.229).
   - *Đa tác tử có đáng chi phí không:* Trong quy mô bài toán này, đa tác tử KHÔNG đáng chi phí. Việc chia nhỏ luồng làm tăng 39% token cho overhead giao tiếp, trong khi điểm số thấp hơn `skills-auto` và tiềm ẩn lỗi thất lạc thông tin (handoff drop).

5. **Dấu hiệu rò rỉ dữ liệu hoặc quá khớp:**
   - *Rò rỉ dữ liệu:* Hoàn toàn không có rò rỉ. Curator được ràng buộc chặt chẽ trong `curator.py` chỉ đọc các kết quả có `role == "learn"`, loại trừ hoàn toàn dữ liệu eval và được rà soát tự động bằng `eval_markers()`. Các skill sinh ra là các nguyên tắc lập trình chung, không chứa tên file hay giá trị cụ thể.
   - *Quá khớp:* Có hiện tượng quá khớp ở mức quy ước tổ chức (convention overfitting): tác tử chỉ học được các quy ước đã gặp ở tập học và không có khả năng tự suy luận ra các quy ước mới của tập đánh giá.

6. **Ước lượng nhiễu từ các lần chạy:**
   - So sánh cùng bộ skill trên tập học: Ở giai đoạn dev (Phần 3.4), `skills-auto` đạt điểm trung bình 0.73 (9/10, 5/8, 6/9). Khi chạy lại sau khi đóng băng, điểm đạt 0.46 (1/10, 5/8, 6/9).
   - Độ lệch lên tới 0.27 (27 điểm phần trăm), nguyên nhân thuần túy do tác vụ `code-learn` ở lần chạy sau bị dừng sớm sau 2 bước gọi công cụ (stochastic variance của LLM).
   - Phát hiện này khẳng định: Với kích thước tập mẫu nhỏ (N=3) và chỉ chạy 1 lần, biên độ nhiễu của LLM là rất lớn. Do đó, các kết luận khoa học không thể chỉ dựa vào một vài điểm số trung bình mà bắt buộc phải đối chiếu vết thực thi và bóc tách cấu trúc từng check.

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập dữ liệu nhỏ (N=3 tác vụ mỗi tập):** Với chỉ 1 tác vụ cho mỗi họ bài toán, sự thay đổi ngẫu nhiên ở 1 tác vụ có thể làm dịch chuyển điểm trung bình chung tới 33%, làm giảm ý nghĩa thống kê của các so sánh điểm số thuần túy.
2. **Đánh giá đơn lượt (Single-run evaluation):** Do hạn chế về ngân sách API và thời gian, mỗi điều kiện chỉ được chạy 1 lần chính thức. Hiện tượng phương sai giữa lần dev và lần chạy sau đóng băng ở `code-learn` chứng minh tính ngẫu nhiên của LLM có thể ảnh hưởng lớn đến kết quả đo.
3. **Quy ước đánh giá nhân tạo (Artificial house rules):** Các check quy ước (`rule_`) không xuất hiện trong đề bài mà chỉ nằm trong kiểm tra tự động. Dù mô phỏng tốt văn hóa tổ chức, nó có thể tạo lợi thế không tự nhiên cho cơ chế lưu vết quy ước (skills) so với các bài toán mở thực tế.
4. **Kiến trúc mô hình duy nhất:** Toàn bộ thí nghiệm được tiến hành trên mô hình Gemini 3.7 Flash. Mức độ phụ thuộc vào prompt hệ thống, khả năng tự đọc file skill và hành vi giao việc cho subagent có thể biểu hiện khác nhau trên các họ mô hình khác (như GPT-4o hay Claude 3.7 Sonnet).

## 10. Kết luận

Thực nghiệm chứng minh phương pháp tự tiến hóa qua kỹ năng (`skills-auto`) đạt hiệu quả tối ưu nhất trên tập đánh giá (0.63) với mức tăng chi phí token rất tiết kiệm (+12%), đồng thời chuyển giao thành công các quy ước thủ tục chung sang bài toán mới. Ngược lại, đa tác tử (`subagents`) làm tăng gần 40% chi phí token và dễ gặp rủi ro mất mát thông tin khi giao việc mà không đem lại ưu thế vượt trội. Hiện tượng biến thiên điểm số giữa các lần chạy (~27%) cho thấy việc đánh giá tác tử cần kết hợp phân tích vết thay vì chỉ nhìn vào điểm số đơn lẻ. Đề xuất cải tiến tiếp theo là xây dựng cơ chế phản hồi động trong quá trình chạy (in-situ dynamic elicitation) để tác tử tự đặt câu hỏi làm rõ các quy ước tiềm ẩn thay vì chỉ phụ thuộc vào kinh nghiệm tĩnh đã học.

## Phụ lục

- **Lệnh đã chạy (theo thứ tự):**
  1. `pytest tests/test_01_provided.py tests/test_02_agent.py tests/test_03_runner.py tests/test_04_curator.py`
  2. `python -m lab.runner --condition baseline --tasks learn`
  3. `python -m lab.runner --condition subagents --tasks learn`
  4. `python -m lab.curator`
  5. `python -m lab.runner --condition skills-auto --tasks learn --results results/skills-auto-dev`
  6. `git add -A && git commit -m "hypotheses"`
  7. `git add -A && git commit --allow-empty -m "freeze skills" && git tag freeze`
  8. `python -m lab.runner --condition baseline --tasks eval`
  9. `python -m lab.runner --condition subagents --tasks eval`
  10. `python -m lab.runner --condition skills-auto --tasks all`
  11. `python scripts/verify_freeze.py`
  12. `python -m lab.compare > report/table.md`
  13. `python scripts/check_breakdown.py`
- **Thử thách mở rộng:** Không thực hiện.
- **Ghi chú khác:** Toàn bộ 6 lần chạy của `skills-auto` đều đạt xác thực tính toàn vẹn `verify_freeze.py` với mã băm đóng băng `835eb191...` và không có sửa đổi kỹ năng trong lúc chạy (`skills_modified = false`).
