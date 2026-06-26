# 006 - Convert BaoCaoMau va dung full input theo source code

Thoi diem: 2026-05-13 06:19:07 Asia/Bangkok

## Da thuc hien

1. Chuyen `QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx` sang Markdown.
2. Trich media cua template sang thu muc rieng.
3. Tach Markdown theo Heading 1 thanh cac chuong rieng.
4. Dung lai full input bao cao dua tren knowledge base, inventory va source code hien tai.
5. Khong ghi de file goc.

## File ket qua

- Markdown template: `QLNhaSach_BaoCao/01_template_markdown/BaoCaoMau_converted_v1.md`
- Media: `QLNhaSach_BaoCao/01_template_markdown/media/BaoCaoMau_v1`
- Full input moi: `QLNhaSach_BaoCao/00_inputs/FULL_INPUT_QLNhaSach_SRC_CODE_v1.md`

## Cac chuong da tach

- `QLNhaSach_BaoCao/01_template_markdown/chapters/01_front-matter.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/02_mô-tả-các-yêu-cầu-của-hệ-thống.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/03_phân-tích-các-yêu-cầu-chức-năng.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/04_thiết-kế-cơ-sở-dữ-liệu.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/05_thiết-kế-các-chức-năng-của-hệ-thống.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/06_thiết-kế-giao-diện-và-cài-đặt.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/07_kiểm-thử-hệ-thống.md`
- `QLNhaSach_BaoCao/01_template_markdown/chapters/08_tổng-kết-và-đánh-giá.md`

## Thong ke source quet truc tiep

- Controllers: 28
- DbSet: 24
- Services/repositories: 6
- SQL migrations: 7
- Tests: 3

## Ghi chu

May hien tai khong co `pandoc` va chua co `python-docx`, nen script dung parser DOCX bang thu vien chuan Python. Markdown giu duoc van ban, heading, bang va anh; cac dinh dang Word phuc tap co the can soat lai khi xuat bao cao cuoi.
