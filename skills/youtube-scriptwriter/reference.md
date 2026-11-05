# Scriptwriting reference

Illustrative material for [SKILL.md](SKILL.md) and [shorts-content-specialist](../shorts-content-specialist/SKILL.md). The technical statements below are placeholders tied to example claim IDs. They are **not verified**: in a real item each one needs a claim whose status the fact-checker set to `verified`.

## Example: CTK-L-0015, persona `technician`

```markdown
## Hook candidates (Các phương án hook)

1. Máy rung, đèn check engine nhấp nháy, máy chẩn đoán báo P0300. Anh em bắt đầu từ đâu?
2. Xóa lỗi P0300 rồi giao xe, vài hôm sau khách quay lại. Vì sao lỗi sáng lại?
3. P0300 không nói xi-lanh nào bỏ máy. Video này đi từng bước để khoanh vùng.

## Selected hook (Hook được chọn)

- **HOOK:** Phương án 2: "Xóa lỗi P0300 rồi giao xe, vài hôm sau khách quay lại. Vì sao lỗi sáng lại?"
- **RATIONALE:** Thợ gặp đúng tình huống này hằng ngày; câu hỏi mở được trả lời ở S05 (vòng mở).

## Script (Kịch bản chi tiết)

### S01 — Hook

- **TYPE:** hook
- **VO:** Xóa lỗi P0300 rồi giao xe, vài hôm sau khách quay lại vì đèn sáng lại. Lỗi không mất đi, chỉ có bản ghi bị xóa. Hôm nay mình đi từng bước để tìm đúng nguyên nhân bỏ máy.
- **VISUAL:** Cận cảnh táp-lô, đèn check engine sáng; cắt sang màn hình máy chẩn đoán hiển thị P0300.
- **ON-SCREEN:** Xóa lỗi ≠ sửa lỗi
- **CLAIMS:** C01, C02

### S04 — Đọc freeze frame

- **TYPE:** demo
- **VO:** Trước khi xóa bất cứ thứ gì, lưu lại dữ liệu freeze frame: tốc độ động cơ, tải và nhiệt độ lúc lỗi được ghi.
- **VISUAL:** Quay màn hình thiết bị ở menu freeze frame. Chỉ dùng Cartek 2 nếu tính năng này "verified" trong feature register; nếu chưa, dùng thiết bị khác hoặc bỏ cảnh.
- **ON-SCREEN:** Bước 2/4: Lưu freeze frame
- **CLAIMS:** C02, C04
- **DEMO-SECONDS:** 8

### S08 — Kêu gọi hành động

- **TYPE:** cta
- **VO:** Anh em gặp ca P0300 khó thì để lại bình luận để được tư vấn, bấm like, subscribe và bật chuông để không bỏ lỡ video hữu ích. Cartek - Check your car.
- **VISUAL:** End screen với video liên quan và logo Cartek.
- **ON-SCREEN:** Cartek - Check your car
- **CLAIMS:**
```

Why this passes the automatic checks: the hook mentions clearing and the narration states the fault returns (caveat marker "lỗi … sáng lại"); P0300 appears in claim C01's text; the CTA contains the brand line. Whether it is *good* is judged by the content-qc-inspector.

## Retention devices (craft heuristics, not guaranteed outcomes)

| Device | How to write it |
|---|---|
| Open loop | Ask a question in the hook and answer it in a named later segment; note both in Retention notes. |
| Progress markers | "Bước 2/4" on screen gives viewers a sense of position. |
| Pattern change | Change shot type (talking head, screen capture, close-up, diagram) when the topic changes. |
| Concrete before abstract | Show the symptom or the screen first, then explain the system. |
| Payoff recap | The recap restates the takeaway in one sentence the viewer can repeat. |

Never claim a retention rate or a view count. Post-publication retention data in `performance.yaml` is the only evidence of what worked.

## Depth by persona

| Persona | Narration style | Avoid |
|---|---|---|
| `technician` | Precise terms (freeze frame, fuel trim, misfire counter), procedure order, test logic | Over-explaining basics |
| `garage-owner` | Diagnostic process, time and cost of wrong diagnosis, equipment value | Unsupported ROI or price claims |
| `automotive-student` | Why the system works, standards, links to theory | Shortcuts without the reasoning |
| `car-owner` | What the light means, when to stop driving, what to ask the garage | Hazardous DIY steps, guarantees |

## Runtime arithmetic

`qc_content.py runtime <ID>` counts one syllable per Vietnamese word, counts each letter or digit of codes such as "P0300" (5) and of short acronyms such as "OBD2" (4), divides by the configured rate, then adds `DEMO-SECONDS` and transitions. At 200 syllables/min a 6-minute long-form needs roughly 1,100-1,200 narrated syllables, depending on demo time. The rate is uncalibrated until the team times real Cartek voice-overs (see `config/production.yaml`).
