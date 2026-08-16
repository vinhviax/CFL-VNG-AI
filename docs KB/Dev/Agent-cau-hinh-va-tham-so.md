# Agent: cấu hình mô hình và tham số vận hành

**Phạm vi:** tab `Cấu hình mô hình` (model, reranker, nhiệt độ, chế độ suy nghĩ, token sinh tối đa) và các giới hạn điều phối ở tab `Công cụ` (số vòng lặp, timeout LLM, gọi công cụ song song).
**Ngày kiểm chứng gần nhất:** 15/08/2026.
**Nguyên tắc nền:** DEC-022 — đọc được giá trị trên UI **không** chứng minh hành vi runtime.

---

## 1. Ba mức tin cậy của mỗi con số trong file này

Mọi giá trị dưới đây thuộc đúng một trong ba nhóm. Đọc sai nhóm là nguồn gốc của mọi kết luận sai.

| Nhãn | Nghĩa | Ví dụ |
|---|---|---|
| **Baseline thiết kế** | Giá trị *dự kiến* ghi trong `agent/<Agent>/config.md` phần đầu file. **Chưa từng nằm trên Web.** | `Temperature 0.2`, `Thinking Off`, model `gpt-5.4-mini` cho LiveOps Planner |
| **Web actual — đã xác minh** | Đã mở dialog và **đọc trực tiếp** trên chính Agent đó, có ngày | `Thinking Bật` trên `GS9 CFL CS Copilot`, 15/08/2026 |
| **Web actual — *suy ra*** | Người dùng khai báo đã áp cho cả nhóm; chỉ kiểm mẫu vài Agent; phần còn lại **suy ra theo mẫu** | `Thinking Bật` trên 8/10 Agent còn lại |

**Web actual là nguồn chuẩn cho trạng thái đang lưu trên Web.** Baseline thiết kế trong `config.md` được giữ nguyên có chủ đích để bảo toàn thiết kế đã phê duyệt — nó không mô tả hệ thống đang chạy.

---

## 2. Model chat

### Danh sách model quan sát được trên dropdown

| Model | Ngày quan sát | Ghi nhận khả dụng |
|---|---|---|
| `deepseek-v4-flash` | 11/08/2026 | Trả lời được ở một chat độc lập; **cũng từng trả `429 insufficient_quota`** |
| `gpt-oss-120b` | 11/08/2026 | Chưa test |
| `hosted_vllm/qwen3.6-35b` | 11/08/2026 | Trả lời được câu canonical và câu no-hit |
| `qwen3.6-plus` | 11/08/2026 | Một lượt trả `429 insufficient_quota` |
| `gpt-5.4-mini` | 14/08/2026 | Thấy đang được gán cho 3 Agent mặc định; chưa chat-test |

**Cạm bẫy:** có tên trong dropdown **không** bảo đảm còn quota. Đừng ghi cứng một model là luôn khả dụng; kiểm tra bằng chat thật sau khi lưu.

### Model đang gán — 6 Agent mặc định (14/08/2026)

| Agent | Model | Reranker | Nhiệt độ | Chế độ suy nghĩ | Token sinh tối đa |
|---|---|---|---|---|---|
| Quick Answer | `gpt-5.4-mini` | `bge-reranker-v2-m3` | `0.7` | Tắt | `0` (UI giải thích: không giới hạn) |
| Smart Reasoning | `gpt-5.4-mini` | `bge-reranker-v2-m3` | `0.7` | Tắt | UI không hiển thị ở mode này |
| Hybrid Researcher | `qwen3.6-plus` | `bge-reranker-v2-m3` | `0.7` | Tắt | UI không hiển thị |
| Wiki Questioner | `qwen3.6-plus` | `bge-reranker-v2-m3` | `0.7` | Tắt | UI không hiển thị |
| Data Analyst | `gpt-5.4-mini` | `bge-reranker-v2-m3` | `0.3` | Tắt | UI không hiển thị |
| FPA Analyst | `qwen3.6-plus` | `bge-reranker-v2-m3` | `0.7` | **Bật** | UI không hiển thị |

Nguồn: `audit/default-agent-readonly-audit-2026-08-14.md`; các file `agent/*-config.md`. Tất cả là **Đã kiểm chứng** từ UI ngày 14/08/2026, chưa chat-test.

Ghi chú: trường `Token sinh tối đa` chỉ thấy ở mode `Trả lời nhanh`. Ở mode `Suy luận thông minh` UI không hiển thị trường này (kiểm chứng 14/08/2026).

### Model đang gán — 10 Agent custom (15/08/2026)

Cả 10 dùng cùng một bộ giá trị:

| Trường | Web actual 15/08/2026 | Mức xác minh |
|---|---|---|
| Model chat | `hosted_vllm/qwen3.6-35b` | Đọc trực tiếp: `GS9 CFL CS Copilot`, `GS9 CFL Knowledge Curator`. 8 Agent còn lại: ***suy ra*** |
| Reranker | `bge-reranker-v2-m3` | như trên |
| Nhiệt độ | `0.7` | như trên |
| Chế độ suy nghĩ | **Bật** | như trên — xem DEC-050 |
| VLM | `qwen3.6-plus` (tải ảnh Bật) | như trên |

**Baseline thiết kế khác hẳn.** Ví dụ đối chiếu:

| Agent | Model baseline | Model Web actual | Temp baseline | Temp Web actual | Thinking baseline | Thinking Web actual |
|---|---|---|---|---|---|---|
| `GS9 CFL LiveOps Planner` | `gpt-5.4-mini` | `hosted_vllm/qwen3.6-35b` | `0.2` | `0.7` | Off | **Bật** |
| `GS9 CFL CS Copilot` | `gpt-5.4-mini` | `hosted_vllm/qwen3.6-35b` | `0.2` | `0.7` | Off | **Bật** |
| `GS9 CFL GM Policy Advisor` | `qwen3.6-plus` | `hosted_vllm/qwen3.6-35b` | `0.1` | `0.7` | Off initially | **Bật** |
| `GS9 CFL Knowledge Curator` | `qwen3.6-plus` | `hosted_vllm/qwen3.6-35b` | `0.2` | `0.7` | Off initially | **Bật** |

Không có Agent custom nào đang chạy đúng baseline thiết kế. Khi ai đó nói "Agent chạy ở nhiệt độ 0.2", họ đang đọc baseline, không đọc Web.

---

## 3. DEC-049 — reranker vừa được bật cho cả 10 Agent

Trước 15/08/2026: trường `Mô hình xếp hạng lại` của cả 10 Agent custom là **trống** (kiểm chứng 14/08/2026, hai audit độc lập). Ngày 15/08/2026 người dùng bật `bge-reranker-v2-m3` cho cả 10.

Điều này thay đổi đường đi của context:

```text
truy hồi candidate → ngưỡng keyword/vector lọc bớt
                   → RERANKER chấm lại (mới bật 15/08)
                   → Top K rerank + ngưỡng rerank
                   → context → model
```

**Hệ quả bắt buộc ghi nhận:** reranker là một **dependency mới chưa được kiểm chứng**. Nó có thể đẩy nguồn đúng tụt hạng, hoặc giữ lại nguồn nhiễu. Chất lượng sau khi bật reranker là **Bị chặn – Chưa xác định** (DEC-049). Coi reranker như một thay đổi cần hồi quy, không phải một cải tiến hiển nhiên.

---

## 4. DEC-050 — `Chế độ suy nghĩ` đang BẬT, trái baseline

Đây là phát hiện **ngoài khai báo** khi xác minh ngày 15/08/2026.

| Điều | Trạng thái |
|---|---|
| Baseline ghi từ 14/08/2026 | `Thinking: Off` cho cả 10 Agent custom |
| Web actual 15/08/2026 | `Chế độ suy nghĩ` **BẬT** |
| Đã đọc trực tiếp | **2/10** — `GS9 CFL CS Copilot`, `GS9 CFL Knowledge Curator` |
| 8 Agent còn lại | ***Suy ra* theo mẫu.** Chưa mở dialog đọc trực tiếp. Phải ghi rõ là *suy ra* cho tới khi kiểm đủ 10 |
| Hành động đã làm | **Không tự tắt.** Ghi nhận trạng thái thật, chờ người dùng xác nhận có chủ đích hay không |

**Vì sao điều này quan trọng, không phải chi tiết nhỏ:**

1. Thinking bật làm **tăng độ trễ và token mỗi lượt** → ảnh hưởng trực tiếp tính quota và ảnh hưởng kết quả khi chạy gate G6.
2. Nó chứng minh **snapshot cấu hình lệch được** — đúng như DEC-049 cảnh báo về quyền `Được chỉnh sửa` cho space 6 người.
3. Nó là ví dụ sống của DEC-022: baseline tài liệu ghi Off, hệ thống thật đang Bật. **Chỉ đọc trực tiếp mới biết.**

**Phân biệt hai thứ trùng tên:** `Suy nghĩ` là tên một **tool** (nhóm điều phối, bật ở tab `Công cụ`). `Chế độ suy nghĩ` / Thinking là **tham số cấp model** ở tab `Cấu hình mô hình`. Hai thứ khác nhau; ngày 14/08/2026 nhiều Agent bật tool `Suy nghĩ` trong khi tham số Thinking vẫn Off.

---

## 5. Nhiệt độ (Temperature)

| Điều | Nội dung | Ngày |
|---|---|---|
| Mô tả UI | `0` ổn định nhất, `1` ngẫu nhiên nhất | 11/08/2026 |
| Giá trị preset | `0,7` | 11/08/2026 |
| Giá trị Agent kiểm thử hạ xuống | `0,2` để câu trả lời nhất quán hơn | 11/08/2026 |
| Giá trị Web actual 10 Agent custom | `0.7` | 15/08/2026 |
| Ngoại lệ mặc định | `Data Analyst` = `0.3` | 14/08/2026 |

Quy tắc dùng: nhiệt độ đo **độ bám định dạng và tính lặp**, không dùng để đo tính đúng của một fact đơn lẻ. A/B `0,2` ↔ `0,7` với cùng query, cùng KB, cùng tool.

---

## 6. Giới hạn điều phối: vòng lặp, timeout, gọi song song

Ba tham số này nằm ở tab `Công cụ` và chỉ tồn tại ở mode `Suy luận thông minh` / `Quy trình`. Mode `Trả lời nhanh` **không có** `Max steps` và `timeout` (kiểm chứng trên `GS9 CFL CS Copilot`, 15/08/2026).

### 6 Agent mặc định — 14/08/2026

| Agent | Số vòng lặp tối đa | Timeout LLM | Gọi song song |
|---|---:|---:|---|
| Quick Answer | — (không có tab Công cụ) | — | — |
| Smart Reasoning | `50` | `120s` | Tắt |
| Hybrid Researcher | `40` | `120s` | **Bật** |
| Wiki Questioner | `30` | `120s` | Tắt |
| Data Analyst | `30` | `120s` | Tắt |
| FPA Analyst | `10` | `180s` | Tắt |

### 10 Agent custom — Web actual 15/08/2026

| Agent | Max steps | Timeout | Song song |
|---|---:|---:|---|
| LiveOps Planner · Release Reviewer · Incident Triage · KPI Experiment Analyst · Economy Offer Analyst · Player Voice Analyst · GM Policy Advisor · Player Communications · Knowledge Curator | `20` | `120s` | Off |
| CS Copilot | không có trường (mode Trả lời nhanh) | — | — |

> **MÂU THUẪN NGUỒN — phải giải quyết trước khi dùng bảng trên làm căn cứ.**
> `audit/liveops-custom-agent-creation-2026-08-14.md` ghi số vòng lặp/timeout **khác nhau theo Agent** tại thời điểm tạo: Incident Triage `30`/`180s`, KPI `30`/`120s`, Economy `25`/`120s`, Player Voice `30`/`120s`, GM `20`/`180s`, Communications `15`/`120s`, Knowledge Curator `25`/`120s`.
> Cùng ngày 14/08/2026, `audit/liveops-custom-agent-multitool-and-agent-kb-2026-08-14.md` mục "Snapshot trước mutation" lại ghi **cả chín Smart Agent đều `loop 20, timeout 120 giây`**.
> Khối `Web actual — 15/08/2026` trong 10 file `agent/GS9 CFL .../config.md` ghi đồng loạt `20`/`120s`.
> Hai trong ba nguồn nói `20`/`120s`, nhưng **không nguồn nào ghi lại thao tác đổi giá trị này**. Bảng trên dùng `20`/`120s` vì đó là ghi nhận mới nhất; giá trị thật vẫn cần **đọc trực tiếp từng Agent** để chốt. Ghi là *Có điều kiện*.
> Trường hợp rõ nhất: `GS9 CFL GM Policy Advisor` có baseline thiết kế `20`/`180s`, audit tạo ghi `20`/`180s`, nhưng Web actual ghi `20`/`120s`.

### Đọc ba tham số này cho đúng

- **Tăng vòng lặp không làm câu trả lời đúng hơn.** Nhiều tool + nhiều vòng = tăng thời gian, chi phí và số nhánh lỗi. Bắt đầu từ bộ tối thiểu, mở rộng theo bằng chứng.
- **Timeout chặn một call**, không chặn cả phiên. Hết timeout trước khi có câu trả lời là tín hiệu điều tra tool chain/model/parallel, không phải lý do tăng số mù quáng.
- **Gọi song song không mặc nhiên nhanh hơn.** Nó có thể đổi thứ tự bằng chứng và tạo lỗi đồng thời. Chỉ `Hybrid Researcher` đang bật (14/08/2026); toàn bộ 10 Agent custom để Off.

---

## 7. Quy trình A/B đúng cách

1. Cố định KB, tool, retrieval, prompt. Chọn ba query: một **canonical**, một **conflict**, một **no-hit**.
2. Chạy ba lần cùng một model nếu quota cho phép. Lưu answer, nguồn, số bước, lỗi.
3. **Đổi đúng một biến mỗi lần.** Không đồng thời đổi model + reranker + threshold.
4. Gặp `429`/lỗi xác thực thì **dừng model đó, ghi Bị chặn**, không retry vô hạn.
5. Sau A/B, **khôi phục** model, nhiệt độ, timeout, parallel, tool về baseline.

Mỗi lần chạy lưu thành **một hàng audit**, không phải một nhận xét. Cột tối thiểu: thời điểm · Agent + version config · model · reranker · nhiệt độ · thinking · tool set · KB/file scope · query · số bước · thời gian · answer · source · lỗi.

Chấm ba điểm riêng biệt, đừng gộp: **retrieval** (canonical có vào candidate không) · **grounding** (có chỉ đúng nguồn không) · **synthesis** (có tổng hợp đúng và nêu mâu thuẫn không).

### Điều không được kết luận

| Kết quả quan sát | Kết luận SAI | Bước đúng |
|---|---|---|
| Model A nhanh hơn B một lượt | A luôn tốt hơn | Lặp lại cùng query/corpus nếu quota cho phép |
| A trả lời được, B trả `429` | A chính xác hơn | Ghi khác biệt **khả dụng**; không chấm chất lượng |
| Cả hai có nguồn, một answer sai | KB hỏng | So context, prompt, output trước |
| Cả hai không có nguồn | Model yếu | Kiểm scope/tool/threshold **trước** model |

---

## 8. Chẩn đoán nhanh theo triệu chứng

| Triệu chứng | Lớp phải kiểm trước | Hành động đúng |
|---|---|---|
| `429 insufficient_quota` | Khả dụng model / quota | Dừng model, đổi model được phép, ghi blocker. **Không** kết luận KB hỏng |
| Answer không có nguồn | Tool → KB scope → retrieval | **Không** đổi LLM như bước đầu tiên |
| Nguồn đúng nhưng câu sai | Prompt, context, nhiệt độ, model | A/B cô lập một biến |
| Tool quay vòng, không tiến gần bằng chứng | Số tool, max loops, prompt | Giảm tool/loop, buộc tiêu chí dừng rõ ràng |
| Timeout | Tool chain, model, parallel | Giữ trace, tăng timeout **có lý do**, rồi hồi quy |
| Lộ `[[chunk#...]]` | Lớp tổng hợp của model/prompt | Thử model khác **trước khi** sửa KB |
| Latency tăng đột ngột sau 15/08 | `Chế độ suy nghĩ` đang Bật (DEC-050) | Xác nhận trạng thái thật bằng cách mở dialog |

**Không lưu** request header, token, service-account JSON hay diagnostic raw vào tài liệu/audit.

---

## 9. Chưa kiểm chứng

- **`Chế độ suy nghĩ` trên 8/10 Agent custom.** Mới đọc trực tiếp 2/10 (`CS Copilot`, `Knowledge Curator`); phần còn lại là ***suy ra* theo mẫu** (DEC-050). Phải mở đủ 10 dialog mới được nâng lên *Đã kiểm chứng*.
- **Model / reranker / nhiệt độ trên 8/10 Agent custom** — cùng tình trạng *suy ra* như trên.
- **Số vòng lặp và timeout thật của 9 Smart Agent custom** — ba nguồn không thống nhất (mục 6). *Có điều kiện*.
- **Tác dụng thật của reranker `bge-reranker-v2-m3`** sau khi bật 15/08/2026 — chưa chat-test. *Bị chặn – Chưa xác định* (DEC-049).
- **Chất lượng so sánh giữa 5 model** — quota không đủ để chạy đủ ba lượt cho cả bốn/năm model (11/08/2026).
- **Quota tenant, giới hạn token thật, chi phí mỗi lượt** — UI không phơi bày. Mọi con số trong file này là *limit nhìn thấy trong config*, không phải limit backend.
- **Ý nghĩa runtime của `Token sinh tối đa = 0`** — UI giải thích là không giới hạn; chưa kiểm chứng hành vi thật.
- **Toàn bộ chất lượng runtime của 10 Agent custom** — chưa Agent nào chat-test đạt. Gate G6 mở.
- **Độ ổn định của mọi con số trong file này** — space `CFL Member` có quyền `Được chỉnh sửa` trên cả 10 Agent (DEC-049), nên bảng có thể lệch bất cứ lúc nào mà không ai báo.
