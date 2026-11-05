# Audience personas

The four viewer segments from the sheet, quoted verbatim, followed by how Cartek content adapts to each one.

Related: [content pillars](content-pillars.md) · [brand voice](brand-voice.md) · [channel positioning](channel-positioning.md)

## From the sheet (source)

Quoted from tab `Khán giả` as imported into [`data/normalized/personas.json`](../data/normalized/personas.json). Outer whitespace is trimmed; spelling is kept as in the sheet (for example "klênh" in 'Khán giả'!C5). The row labels are:

| Row | Label in the sheet |
|---|---|
| 1 | Đối tượng Viewer |
| 2 | Nhân khẩu học |
| 3 | Sở thích |
| 4 | Nỗi đau/ thách thức |
| 5 | Hành vi trên internet, mạng xã hội |
| 6 | Content yêu thích |

### garage-owner — "Chủ Garage ô tô" ('Khán giả'!B1:B6)

- **Nhân khẩu học:** "Tuổi: 35-50, Giới tính: Nam, Sở hữu ô tô và garage quy mô vừa." (B2)
- **Sở thích:** "Ô tô, công nghệ, tự tay làm (DIY), chia sẻ kinh nghiệm" (B3)
- **Nỗi đau/ thách thức:** "Cập nhật kiến thức liên tục, Khó khăn trong tìm kiếm thông tin, Áp lực chi phí cho garage, đổi mới để cạnh tranh với garage khác." (B4)
- **Hành vi trên internet, mạng xã hội:** "Tìm kiếm thông tin, Hoạt động trong các hội nhóm, follow các influencer youtube" (B5)
- **Content yêu thích:** "Video hướng dẫn sửa chữa, bảo dưỡng. Video review xe. Video giới thiệu công nghệ mới. Video chia sẻ kinh nghiệm" (B6)

### technician — "Thợ sửa chữa ô tô" ('Khán giả'!C1:C6)

- **Nhân khẩu học:** "Tuổi: 20-45, Giới tính: Nam, kỹ thuật viên chuyên ngành" (C2)
- **Sở thích:** "Liên quan đến ô tô, công nghệ mới, chia sẻ kinh nghiệm, giải trí" (C3)
- **Nỗi đau/ thách thức:** "Cập nhật kiến thức, tìm kiếm thông tin , xử lý sự cố phức tạp" (C4)
- **Hành vi trên internet, mạng xã hội:** "Tìm kiếm thông tin sửa chữa, tham gia cộng đồng, theo dõi klênh youtube" (C5)
- **Content yêu thích:** "Đánh giá sản phẩm, hướng dẫn sửa chữa, so sánh công nghệ, chia sẻ kinh nghiệm" (C6)

### automotive-student — "Sinh viên chuyên ngành" ('Khán giả'!D1:D6)

- **Nhân khẩu học:** "Tuổi: 18-22, Giới tính: Nam, Sinh viên học về ô tô" (D2)
- **Sở thích:** "Nghiên cứu kiến thức chuyên sâu, công nghệ mới" (D3)
- **Nỗi đau/ thách thức:** "Cập nhật kiến thức mới, tìm kiếm thông tin hữu ích, trải nghiệm thực tế tại Garage hoặc thực nghiệm với xe" (D4)
- **Hành vi trên internet, mạng xã hội:** "Tìm kiếm thông tin học tập, tham gia cộng đồng, theo dõi nhiều kênh chia sẻ kiến thức" (D5)
- **Content yêu thích:** "Kinh nghiệm thực chiến, kiến thức chuyên sâu," (D6)

### car-owner — "Chủ xe ô tô (ít)" ('Khán giả'!E1:E6)

- **Nhân khẩu học:** "Tuổi: 24-50, Giới tính: Nam, Sở hữu ô tô cá nhân" (E2)
- **Sở thích:** "Ô tô, tự tay làm (DIY)" (E3)
- **Nỗi đau/ thách thức:** "Tìm kiếm thông tin hữu ích, lỗi vặt cơ bản của xe hơi" (E4)
- **Hành vi trên internet, mạng xã hội:** "Tìm kiếm thông tin, follow các kênh về xe trên nhiều nền tảng mạng xã hội" (E5)
- **Content yêu thích:** "Review xe, các tính năng đặc biệt, sửa chữa cơ bản các lỗi vặt hay gặp, kinh nghiệm sử dụng xe hơi" (E6)

The sheet marks this segment "(ít)" ("few/less"). The repository interprets that as a smaller, secondary segment: the normalized record has `priority: low`, and QC gate G2 warns when it is chosen as the primary audience so the choice is deliberate.

The sheet records the gender of every segment as "Nam". Treat that as a description of the current audience, not as a rule about who may watch.

## Repository guidance (added 2026-11-05; editorial assumption, change freely)

These recommendations are derived from the sheet data above. Confirm or revise them with real audience data from YouTube Studio ([post-publish analysis](../workflows/post-publish-analysis.md)). Default technical depths come from `persona_defaults` in [config/taxonomy.yaml](../config/taxonomy.yaml).

### garage-owner

- **Technical depth:** intermediate. Wants the method and the business effect more than the deep theory.
- **Terminology:** standard workshop terms; explain acronyms once ("mã lỗi (DTC)").
- **Hooks:** time, comebacks and cost. Example: "Xe quay lại xưởng lần thứ hai vì cùng một mã lỗi — quy trình nào giúp tránh điều đó?"
- **CTA:** invite questions and consultation, in line with the sheet's long-form CTA: "Để lại comment nếu cần tư vấn". End with "Cartek - Check your car".
- **Avoid:** sales pressure, unproven cost-saving claims, anything that sounds like Cartek promises business results.

### technician

- **Technical depth:** advanced. Expects real data, test steps and edge cases.
- **Terminology:** full technical vocabulary (freeze frame, fuel trim, misfire counters) with Vietnamese equivalents from the [glossary](brand-voice.md#technical-glossary).
- **Hooks:** a concrete case that resists the obvious fix. Example: "Xe báo P0300, đã thay bugi mà đèn vẫn sáng lại — bước kiểm tra tiếp theo là gì?"
- **CTA:** ask for their hardest cases in the comments; credit good answers in later videos.
- **Avoid:** oversimplifying, talking down, presenting one cause as the only cause, unverified tool capabilities.

### automotive-student

- **Technical depth:** intermediate, rising to advanced in P4. Wants the "why" behind each test.
- **Terminology:** introduce each term with its definition and the English term, since course material often uses English.
- **Hooks:** curiosity about how a system works. Example: "Vì sao ECU biết xi-lanh nào đang bỏ máy?"
- **CTA:** save the video for study, share it with classmates, ask follow-up questions.
- **Avoid:** shortcuts that skip safety steps; presenting workshop habits as textbook facts.

### car-owner (secondary segment)

- **Technical depth:** basic. Wants to know what a warning means, what is safe to do, and when to go to a garage.
- **Terminology:** everyday words first, then the technical term. Example: "đèn báo lỗi động cơ (đèn Check Engine)".
- **Hooks:** a symptom they see. Example: "Đèn Check Engine vừa sáng — bạn nên làm gì trước tiên?"
- **CTA:** describe the car's symptom in the comments; for safety systems, recommend a qualified garage.
- **Avoid:** suggesting that clearing a code fixes the car; DIY steps on brakes, airbags, high-voltage or fuel systems; the phrase "không cần thợ".

### Persona and pillar fit

Guidance only. "High" means the pillar directly answers a pain point listed in the sheet for that persona. The bold cells are the `pillar_defaults` in [config/taxonomy.yaml](../config/taxonomy.yaml).

| Persona | P1 | P2 | P3 | P4 | P5 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|---|---|---|---|
| garage-owner | High | Medium | Medium | High | **High** | Medium | **High** | Low | Low |
| technician | **High** | Medium | High | **High** | Medium | High | Medium | Medium | Low |
| automotive-student | Medium | **High** | Medium | High | Medium | Medium | Low | Medium | Medium |
| car-owner | Medium | Medium | **High** | Low | Low | **High** | Medium | **High** | **High** |

### Choosing the audience for an item

1. Pick one primary persona per item. A video written for everyone serves no one.
2. Record it in `item.yaml` (`audience.primary`, `audience.secondary`, `audience.technical_depth`).
3. Name the persona's pain point in the brief (`## Audience` in `brief.md`), quoting the sheet where possible.
4. The independent QC review checks persona fit twice: gate G2 for the topic, problem and depth in the brief, gate G4 for the hook, wording and CTA in the script. See [content-qc-inspector](../skills/content-qc-inspector/SKILL.md).
