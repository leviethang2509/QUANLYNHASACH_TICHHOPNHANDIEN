# FULL PROMPT — AUTO GENERATE SOFTWARE REPORT FROM SOURCE CODE + WORD TEMPLATE

You are a senior software architect, UML analyst, and Vietnamese academic technical writer.

Your mission is to fully automate the generation of a graduation/internship/software engineering report based on:
1. Existing source code project
2. Existing Word report template

You must analyze the source code deeply, understand workflows, generate UML diagrams, rewrite report content, and export a final professional Vietnamese academic report.

---

# PROJECT INPUTS

Source code location:
./source_code

Word template:
./BaoCaoMau.docx

Output folder:
./output

---

# GLOBAL OBJECTIVES

1. Convert the DOCX template into structured Markdown
2. Extract images from the DOCX template
3. Analyze the full source code project
4. Build a complete project knowledge base
5. Rewrite the entire report to match the current project
6. Preserve academic writing style in Vietnamese
7. Avoid plagiarism and repetitive wording
8. Generate UML diagrams automatically
9. Generate Draw.io compatible diagrams
10. Replace old UML diagrams with new generated diagrams
11. Export final DOCX and PDF reports
12. Preserve headings, numbering, tables, and structure

---

# OUTPUT STRUCTURE

Create the following folders automatically:

./output/markdown
./output/knowledge
./output/uml
./output/uml_images
./output/drawio
./output/final_markdown
./output/final_docx
./output/final_pdf
./output/logs

---

# STEP 1 — CONVERT DOCX TEMPLATE TO MARKDOWN

Tasks:
1. Convert BaoCaoMau.docx into Markdown
2. Preserve:
   - headings
   - numbering
   - bullet lists
   - tables
   - references
3. Extract all images into:
   ./output/markdown/media
4. Use UTF-8 encoding
5. Split markdown into chapters using Heading 1
6. Save each chapter separately

Required output:
./output/markdown/*.md

Use:
- pandoc
- markdown format: gfm
- wrap=none

Recommended command:

pandoc BaoCaoMau.docx \
-t gfm \
--wrap=none \
--extract-media=media \
-o BaoCao.md

---

# STEP 2 — ANALYZE SOURCE CODE

Analyze the entire source code deeply.

You must identify:

1. Project overview
2. System architecture
3. Technologies used
4. Main modules
5. Database schema
6. Entities
7. Relationships
8. APIs
9. Controllers
10. Services
11. Authentication flow
12. CRUD flows
13. Main business workflows
14. User roles
15. System actors
16. Data processing flows
17. Background jobs
18. Notification/email workflows
19. Upload/download workflows
20. Reporting/export workflows

You must infer missing documentation directly from source code.

Generate:

./output/knowledge/knowledge_base.json

Required JSON structure:

{
  "project_name": "",
  "project_description": "",
  "technologies": [],
  "modules": [],
  "actors": [],
  "use_cases": [],
  "database_entities": [],
  "api_list": [],
  "business_flows": [],
  "system_architecture": {},
  "authentication_flow": {},
  "deployment_structure": {},
  "services": [],
  "repositories": [],
  "background_jobs": []
}

---

# STEP 3 — ANALYZE DATABASE

Analyze:
- Entity Framework
- SQL files
- migrations
- repositories
- models

Generate:
1. Database description
2. Table relationships
3. Primary keys
4. Foreign keys
5. ERD explanation

Save:
./output/knowledge/database_analysis.md

---

# STEP 4 — GENERATE UML DIAGRAMS

Generate the following UML diagrams automatically:

1. Use Case Diagram
2. Sequence Diagram
3. Activity Diagram
4. Class Diagram
5. ERD Diagram
6. Deployment Diagram
7. Component Diagram

Use:
- PlantUML

Save:
./output/uml

Generate:
- .puml files
- .drawio files if possible

Requirements:
- Use Vietnamese labels
- Use real workflows from source code
- Avoid generic diagrams
- Generate professional layouts

---

# STEP 5 — RENDER UML IMAGES

Render all PlantUML files into PNG images.

Save:
./output/uml_images

Requirements:
- High resolution
- White background
- Readable Vietnamese text

---

# STEP 6 — MAP TEMPLATE CONTENT

Analyze the old report template content.

Identify:
1. Old project descriptions
2. Old system names
3. Old workflows
4. Old UML references
5. Old database references
6. Outdated screenshots
7. Generic academic sections

Generate mapping file:

./output/knowledge/template_mapping.json

Structure:

{
  "chapter": "",
  "old_content": "",
  "new_content_strategy": ""
}

---

# STEP 7 — REWRITE REPORT CONTENT

Rewrite ALL markdown chapters.

Requirements:
1. Preserve chapter structure
2. Preserve heading hierarchy
3. Keep academic tone
4. Use natural Vietnamese writing
5. Avoid plagiarism
6. Avoid repetitive wording
7. Match the current source code project
8. Replace old project descriptions
9. Replace outdated UML explanations
10. Replace outdated workflows
11. Generate realistic explanations
12. Expand weak sections if needed
13. Keep technical consistency
14. Preserve formatting
15. Preserve tables if possible

Target writing style:
- Vietnamese university graduation report
- Professional software engineering thesis
- Clear and formal technical language

Output:
./output/final_markdown

---

# STEP 8 — GENERATE SYSTEM DESCRIPTIONS

Generate detailed Vietnamese descriptions for:

1. System overview
2. Problem statement
3. Objectives
4. Functional requirements
5. Non-functional requirements
6. Technologies
7. Architecture
8. Database
9. Authentication
10. Security
11. APIs
12. Deployment
13. Testing
14. Future development

Save:
./output/knowledge/generated_sections

---

# STEP 9 — INSERT UML IMAGES INTO REPORT

Automatically insert generated UML PNG images into appropriate markdown sections.

Replace:
- old UML images
- outdated diagrams

Requirements:
- Match diagrams with corresponding explanations
- Preserve formatting consistency
- Use relative image paths

---

# STEP 10 — GENERATE TABLES

Automatically generate:
1. Functional requirement tables
2. User role tables
3. Database tables
4. API tables
5. Test case tables
6. Technology comparison tables

Insert into corresponding chapters.

---

# STEP 11 — GENERATE TESTING CONTENT

Generate:
1. Test scenarios
2. Test cases
3. Expected results
4. Actual results
5. Performance evaluation
6. Security evaluation

Save:
./output/knowledge/testing

---

# STEP 12 — GENERATE DEPLOYMENT CONTENT

Generate deployment descriptions:
1. System requirements
2. Deployment architecture
3. Installation steps
4. Configuration
5. Docker description if applicable
6. IIS/Nginx setup if detected

---

# STEP 13 — FINAL QUALITY CHECK

Perform final validation:

1. Check broken markdown links
2. Check missing images
3. Check duplicated sections
4. Check invalid UML references
5. Check heading hierarchy
6. Check UTF-8 encoding
7. Check Vietnamese grammar consistency
8. Check table formatting
9. Check image references
10. Check chapter numbering

Generate:
./output/logs/final_validation.md

---

# STEP 14 — EXPORT FINAL DOCX

Combine all markdown chapters.

Export:
1. DOCX
2. PDF

Requirements:
- Preserve Vietnamese fonts
- Preserve table formatting
- Preserve images
- Generate professional layout
- Preserve page breaks
- Preserve headings
- Generate table of contents

Save:
./output/final_docx
./output/final_pdf

Recommended command:

pandoc combined.md \
-o FinalReport.docx

---

# STEP 15 — FINAL REPORT REQUIREMENTS

The final report must:
1. Look like a real university software engineering thesis
2. Match the actual source code
3. Contain realistic UML diagrams
4. Contain realistic technical explanations
5. Use professional Vietnamese writing
6. Avoid AI repetitive style
7. Avoid generic explanations
8. Be technically consistent
9. Be academically formatted
10. Be ready for submission

---

# IMPORTANT RULES

1. NEVER use placeholder explanations
2. NEVER generate fake workflows unrelated to source code
3. NEVER use generic UML diagrams
4. NEVER destroy markdown structure
5. NEVER remove important tables
6. ALWAYS infer workflows from actual code
7. ALWAYS preserve Vietnamese UTF-8 encoding
8. ALWAYS save intermediate files
9. ALWAYS keep logs
10. ALWAYS maintain technical consistency

---

# EXECUTION MODE

Run fully autonomously.

Automatically:
- analyze
- rewrite
- generate diagrams
- export documents
- validate outputs

Do not ask for confirmation between steps.

Continue until the final report is fully generated.

---

# PROJECT-SPECIFIC OPTIMIZATION ADDENDUM - QLNhaSach

> Ghi chú: Phần này bổ sung và tối ưu prompt hiện có, không thay thế hoặc xóa các yêu cầu phía trên. Khi có xung đột đường dẫn, ưu tiên dùng cấu trúc thư mục lớn bên dưới để dễ quản lý toàn bộ tài liệu báo cáo trong dự án.

## MAIN WORKSPACE REQUIREMENT

Create one large report workspace folder at the root of the current project:

./BaoCao_ProjectWorkspace

All generated files, intermediate files, diagrams, logs, markdown chapters, exported DOCX/PDF files, analysis files, and report assets must be written inside this folder only.

Do not scatter generated report files directly into the project root, source folders, database folders, or existing feature folders.

The original prompt uses `./output`. For this project, treat:

./output

as:

./BaoCao_ProjectWorkspace/output

## PROJECT PATH MAPPING

Use the actual project structure below instead of the generic `./source_code` path:

Source code root:
./

Main ASP.NET MVC web project:
./BaiTapLon

Business/data access libraries:
./Mood
./Common
./CommomMail
./CommomSentMail

Face authentication API:
./face_auth_api

Database and migrations:
./sql
./db.sql
./sql_15_2.sql

Existing report assets and generated diagram folders:
./report_assets
./use_case
./use_case_drawio
./use_case_drawio_exports
./database_drawio
./database_drawio_exports
./sequence_class_drawio_v4
./sequence_class_drawio_v4_exports

Word template:
./BaoCaoMau.docx

Existing final/near-final reports:
./BaoCaoMauSua_Version1.docx
./BaoCaoMauSua_Version2_DrawIOUseCase.docx
./BaoCaoMauSua_Version3_TableFields.docx
./BaoCao_QuanLyNhaSach_NhanDienKhuonMat_LeVietThang_2224802010263.docx

## OPTIMIZED OUTPUT STRUCTURE

Create and use this full structure:

./BaoCao_ProjectWorkspace
./BaoCao_ProjectWorkspace/00_inputs
./BaoCao_ProjectWorkspace/01_template_markdown
./BaoCao_ProjectWorkspace/01_template_markdown/media
./BaoCao_ProjectWorkspace/02_source_analysis
./BaoCao_ProjectWorkspace/02_source_analysis/code_inventory
./BaoCao_ProjectWorkspace/02_source_analysis/database
./BaoCao_ProjectWorkspace/02_source_analysis/workflows
./BaoCao_ProjectWorkspace/02_source_analysis/security
./BaoCao_ProjectWorkspace/03_knowledge_base
./BaoCao_ProjectWorkspace/04_generated_sections
./BaoCao_ProjectWorkspace/05_uml
./BaoCao_ProjectWorkspace/05_uml/plantuml
./BaoCao_ProjectWorkspace/05_uml/drawio
./BaoCao_ProjectWorkspace/05_uml/images
./BaoCao_ProjectWorkspace/06_report_markdown
./BaoCao_ProjectWorkspace/06_report_markdown/chapters
./BaoCao_ProjectWorkspace/06_report_markdown/combined
./BaoCao_ProjectWorkspace/07_tables
./BaoCao_ProjectWorkspace/08_testing
./BaoCao_ProjectWorkspace/09_exports
./BaoCao_ProjectWorkspace/09_exports/docx
./BaoCao_ProjectWorkspace/09_exports/pdf
./BaoCao_ProjectWorkspace/10_validation
./BaoCao_ProjectWorkspace/11_logs
./BaoCao_ProjectWorkspace/12_archive

## FILE MANAGEMENT RULES

1. Copy important input references into `./BaoCao_ProjectWorkspace/00_inputs` before processing.
2. Never overwrite original project files unless explicitly instructed.
3. Keep every generated artifact inside `./BaoCao_ProjectWorkspace`.
4. Use versioned filenames for important outputs, for example:
   - `knowledge_base_v1.json`
   - `database_analysis_v1.md`
   - `final_report_v1.docx`
   - `final_report_v1.pdf`
5. Keep logs for every major step in `./BaoCao_ProjectWorkspace/11_logs`.
6. Save validation results in `./BaoCao_ProjectWorkspace/10_validation`.
7. If a generated file already exists, create a new version instead of deleting the old file.

## OPTIMIZED ANALYSIS PROMPT FOR THIS PROJECT

Analyze the project as an ASP.NET MVC bookstore management system with face authentication and book rental workflows.

Focus on these real modules:

1. Customer account registration and login
2. Face authentication and MFA
3. Identity card OCR / CMND-CCCD profile verification
4. Product browsing and search
5. Product favorites
6. Shopping cart and order management
7. Book rental request workflow
8. Geofence/location verification for borrowing books
9. Admin rental approval and return confirmation
10. Gmail notification workflow
11. Admin product/category/user/order management
12. Store location and introduction content management
13. Logs: face auth logs, geofence logs, rental logs
14. Statistics/reporting screens
15. SQL database schema and Entity Framework models

Do not describe generic e-commerce behavior unless it is visible in the source code.

## OPTIMIZED WRITING PROMPT FOR FINAL REPORT

Write the report in Vietnamese academic style for the project:

"Xây dựng website quản lý nhà sách kết hợp nhận diện khuôn mặt, xác thực vị trí và quản lý mượn trả sách"

The writing must:

1. Match the actual source code structure.
2. Mention ASP.NET MVC, Entity Framework, SQL Server LocalDB, Flask face API, OCR, geofence, email notification, and admin dashboard only when supported by code.
3. Explain workflows from controller/service/repository behavior.
4. Avoid placeholder phrases such as "hệ thống có thể", "tùy theo yêu cầu", "module này xử lý chung chung".
5. Avoid repetitive AI wording.
6. Keep Vietnamese technical terms consistent:
   - "người dùng"
   - "quản trị viên"
   - "sản phẩm/sách"
   - "yêu cầu mượn sách"
   - "xác thực khuôn mặt"
   - "kiểm tra vị trí"
   - "nhật ký hệ thống"
7. Preserve the original chapter structure from the Word template when possible.
8. Expand sections only when the source code provides enough evidence.

## OPTIMIZED DIAGRAM PROMPT

Generate diagrams from actual project workflows, not from assumptions.

Required diagrams for this project:

1. Use case diagram - toàn hệ thống
2. Use case diagram - khách hàng
3. Use case diagram - quản trị viên
4. Sequence diagram - đăng nhập và xác thực khuôn mặt
5. Sequence diagram - gửi yêu cầu mượn sách
6. Sequence diagram - admin duyệt mượn/trả sách
7. Sequence diagram - thêm/xem danh sách yêu thích
8. Activity diagram - quy trình mượn sách có kiểm tra vị trí
9. Activity diagram - cập nhật hồ sơ CMND/CCCD
10. Class diagram - các lớp controller/service/repository chính
11. ERD/database diagram - bảng người dùng, sản phẩm, đơn hàng, mượn sách, logs
12. Component diagram - ASP.NET MVC app, SQL Server, Flask Face API, Gmail service
13. Deployment diagram - IIS/local web app, LocalDB, face_auth_api

Save all diagram sources to:

./BaoCao_ProjectWorkspace/05_uml/plantuml
./BaoCao_ProjectWorkspace/05_uml/drawio

Save rendered images to:

./BaoCao_ProjectWorkspace/05_uml/images

## OPTIMIZED KNOWLEDGE BASE FILES

Generate these files:

./BaoCao_ProjectWorkspace/03_knowledge_base/knowledge_base_v1.json
./BaoCao_ProjectWorkspace/03_knowledge_base/module_inventory_v1.md
./BaoCao_ProjectWorkspace/03_knowledge_base/controller_action_map_v1.md
./BaoCao_ProjectWorkspace/03_knowledge_base/database_analysis_v1.md
./BaoCao_ProjectWorkspace/03_knowledge_base/business_workflows_v1.md
./BaoCao_ProjectWorkspace/03_knowledge_base/security_and_authentication_v1.md
./BaoCao_ProjectWorkspace/03_knowledge_base/report_template_mapping_v1.json

## OPTIMIZED FINAL EXPORT REQUIREMENT

Final outputs must be:

./BaoCao_ProjectWorkspace/09_exports/docx/BaoCao_QLNhaSach_Final_v1.docx
./BaoCao_ProjectWorkspace/09_exports/pdf/BaoCao_QLNhaSach_Final_v1.pdf

Also generate:

./BaoCao_ProjectWorkspace/06_report_markdown/combined/BaoCao_QLNhaSach_Final_v1.md
./BaoCao_ProjectWorkspace/10_validation/final_validation_v1.md

## PRESERVE PROMPT RULE

Do not delete, overwrite, or shorten any existing prompt section in this file. Only append improvements, corrections, path mappings, or project-specific execution rules.
