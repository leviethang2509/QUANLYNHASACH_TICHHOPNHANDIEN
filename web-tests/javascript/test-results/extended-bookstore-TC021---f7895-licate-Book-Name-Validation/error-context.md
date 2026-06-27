# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: extended-bookstore.spec.js >> TC021 - Admin Book Management: Duplicate Book Name Validation
- Location: extended-bookstore.spec.js:725:3

# Error details

```
Test timeout of 10000ms exceeded.
```

```
Error: locator.fill: Test timeout of 10000ms exceeded.
Call log:
  - waiting for locator('form').locator('input[name="MetaTitle"]')

```

# Page snapshot

```yaml
- generic [ref=e1]:
  - navigation [ref=e2]:
    - generic [ref=e3]:
      - link "Trang Quản Trị" [ref=e4] [cursor=pointer]:
        - /url: /Admin/Homes
      - link " Trang khách hàng" [ref=e5] [cursor=pointer]:
        - /url: /trang-chu
        - generic [ref=e6]: 
        - text: Trang khách hàng
      - button "" [ref=e7] [cursor=pointer]:
        - generic [ref=e8]: 
    - generic [ref=e9]:
      - button "" [ref=e10] [cursor=pointer]:
        - generic [ref=e11]: 
      - generic [ref=e13]:
        - textbox "Search" [ref=e14]:
          - /placeholder: Tìm kiếm...
        - button "" [ref=e16] [cursor=pointer]:
          - generic [ref=e17]: 
      - list [ref=e18]:
        - listitem [ref=e19]:
          - button " 9+" [ref=e20] [cursor=pointer]:
            - generic [ref=e21]: 
            - generic [ref=e22]: 9+
        - listitem [ref=e23]:
          - button " 7" [ref=e24] [cursor=pointer]:
            - generic [ref=e25]: 
            - generic [ref=e26]: "7"
        - listitem [ref=e27]:
          - button "" [ref=e28] [cursor=pointer]:
            - generic [ref=e29]: 
  - generic [ref=e30]:
    - list [ref=e31]:
      - listitem [ref=e32]:
        - link " Trang chủ" [ref=e33] [cursor=pointer]:
          - /url: /Admin/Homes
          - generic [ref=e34]: 
          - text: Trang chủ
      - listitem [ref=e35]:
        - button " Quản lí người dùng " [ref=e36] [cursor=pointer]:
          - generic [ref=e37]: 
          - text: Quản lí người dùng 
      - listitem [ref=e38]:
        - button " Quản lí sách " [ref=e39] [cursor=pointer]:
          - generic [ref=e40]: 
          - text: Quản lí sách 
      - listitem [ref=e41]:
        - button " Quản lí nhập hàng " [ref=e42] [cursor=pointer]:
          - generic [ref=e43]: 
          - text: Quản lí nhập hàng 
      - listitem [ref=e44]:
        - button " Quản lí NCC " [ref=e45] [cursor=pointer]:
          - generic [ref=e46]: 
          - text: Quản lí NCC 
      - listitem [ref=e47]:
        - button " Quản Lý Trợ Giúp " [ref=e48] [cursor=pointer]:
          - generic [ref=e49]: 
          - text: Quản Lý Trợ Giúp 
      - listitem [ref=e50]:
        - button " Quản lí đơn hàng " [ref=e51] [cursor=pointer]:
          - generic [ref=e52]: 
          - text: Quản lí đơn hàng 
      - listitem [ref=e53]:
        - button " Quản lí mượn sách " [ref=e54] [cursor=pointer]:
          - generic [ref=e55]: 
          - text: Quản lí mượn sách 
      - listitem [ref=e56]:
        - button " Nhật ký hệ thống " [ref=e57] [cursor=pointer]:
          - generic [ref=e58]: 
          - text: Nhật ký hệ thống 
      - listitem [ref=e59]:
        - button " Quản lí Website " [ref=e60] [cursor=pointer]:
          - generic [ref=e61]: 
          - text: Quản lí Website 
      - listitem [ref=e62]:
        - button " Thông Kê " [ref=e63] [cursor=pointer]:
          - generic [ref=e64]: 
          - text: Thông Kê 
      - listitem [ref=e65]:
        - link " Đăng Xuất" [ref=e66] [cursor=pointer]:
          - /url: /Admin/Login/Logout
          - generic [ref=e67]: 
          - text: Đăng Xuất
    - generic [ref=e68]:
      - generic [ref=e69]:
        - generic:
          - heading [level=1]
        - separator [ref=e70]
        - generic [ref=e72]:
          - generic [ref=e75]:
            - heading "Thêm sản phẩm mới" [level=1] [ref=e77]
            - generic [ref=e79]:
              - button "Tạo sản phẩm" [ref=e80] [cursor=pointer]
              - button " Trở về" [ref=e81] [cursor=pointer]:
                - link " Trở về" [ref=e82]:
                  - /url: /Admin/SanPham/Index
                  - generic [ref=e83]: 
                  - text: Trở về
          - generic [ref=e87]:
            - generic [ref=e88]:
              - generic [ref=e89]:
                - generic [ref=e90]: Tên Sản Phẩm (*)
                - textbox [active] [ref=e92]: Mô hình tài chính cơợ bụn
              - generic [ref=e93]:
                - generic [ref=e94]: Tác Giả (*)
                - textbox [ref=e96]
              - generic [ref=e97]:
                - generic [ref=e98]: Nhà Xuất Bản (*)
                - textbox [ref=e100]
              - generic [ref=e101]:
                - generic [ref=e102]: Từ khóa (SEO)
                - textbox [ref=e103]
              - generic [ref=e104]:
                - generic [ref=e105]: Chi Tiết
                - textbox [ref=e106]
              - generic [ref=e107]:
                - generic [ref=e108]: Mô tả sản phẩm
                - textbox [ref=e109]
            - generic [ref=e110]:
              - generic [ref=e111]:
                - generic [ref=e112]: Giá Bán (*)
                - spinbutton [ref=e114]
              - generic [ref=e115]:
                - generic [ref=e116]: Giá Nhập (*)
                - spinbutton [ref=e118]
              - generic [ref=e119]:
                - generic [ref=e120]: Giảm Giá (%)
                - spinbutton [ref=e122]
              - generic [ref=e123]:
                - generic [ref=e124]: Ảnh Sản Phẩm
                - generic [ref=e125]:
                  - textbox [ref=e126]
                  - link "Chọn ảnh" [ref=e127] [cursor=pointer]:
                    - /url: "#"
              - generic [ref=e128]:
                - generic [ref=e129]: File review sách
                - button "Choose File" [ref=e130]
              - generic [ref=e131]:
                - generic [ref=e132]: Link YouTube
                - textbox "https://www.youtube.com/watch?v=..." [ref=e133]
              - generic [ref=e134]:
                - generic [ref=e135]: Thể Loại
                - combobox [ref=e137]:
                  - option "[Chọn thể loại]" [selected]
                  - option "Khoa Học"
                  - option "Tiểu Thuyết"
                  - option "Trò Chơi Điện Tử"
                  - option "Phim"
                  - option "Văn học"
                  - option "Tự Nhiên Xã Hội"
                  - option "Khoa Học"
                  - option "Trinh Thám"
                  - option "Ngoại Ngữ"
                  - option "Thiếu Nhi"
                  - option "Lịch Sử"
                  - option "Hoạt Hình"
              - generic [ref=e139]:
                - generic [ref=e140]: Trạng thái
                - checkbox "Trạng thái" [ref=e141]
      - contentinfo [ref=e142]:
        - generic [ref=e144]: Trang quản lý - Nhà Sách Phương Nam © 2026
  - text: 
```

# Test source

```ts
  654 |           console.log('Feedback Reply success message:', successText);
  655 |           expect(successText).toContain('thành công');
  656 |         }
  657 |       } else {
  658 |         console.log('Feedback is already replied (textarea is readonly) or not editable.');
  659 |       }
  660 |     } else if (await detailLink.count() > 0) {
  661 |       await detailLink.click();
  662 |       await page.waitForLoadState('networkidle');
  663 |       await page.screenshot({ path: path.join(__dirname, 'screenshots/40_admin_feedback_detail.png'), fullPage: true });
  664 |       console.log('Navigated to feedback details since no reply link was active.');
  665 |     } else {
  666 |       console.log('No feedback rows available to reply/view.');
  667 |     }
  668 |   });
  669 | 
  670 |   test('TC020 - Admin Orders Management: Order States Navigation', async ({ page }) => {
  671 |     // 1. Login as Admin
  672 |     await page.goto('http://localhost:56919/');
  673 |     await page.waitForLoadState('networkidle');
  674 | 
  675 |     const accountToggle = page.locator('a#sidebarNavToggler').first();
  676 |     await accountToggle.scrollIntoViewIfNeeded();
  677 |     await accountToggle.click({ force: true });
  678 | 
  679 |     const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
  680 |     const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
  681 |     await usernameInput.fill('admin');
  682 |     await passwordInput.fill('123456');
  683 | 
  684 |     await page.evaluate(() => {
  685 |        window.login();
  686 |     });
  687 |     await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });
  688 | 
  689 |     // 2. Navigate to HoaDon Index (All Orders)
  690 |     await page.goto('http://localhost:56919/Admin/HoaDon/Index');
  691 |     await page.waitForLoadState('networkidle');
  692 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/43_admin_orders_all.png'), fullPage: true });
  693 | 
  694 |     // 3. Navigate to XacNhan (Orders pending confirmation)
  695 |     await page.goto('http://localhost:56919/Admin/HoaDon/XacNhan');
  696 |     await page.waitForLoadState('networkidle');
  697 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/44_admin_orders_xacnhan.png'), fullPage: true });
  698 | 
  699 |     // 4. Navigate to DongGoi (Packaging list)
  700 |     await page.goto('http://localhost:56919/Admin/HoaDon/DongGoi');
  701 |     await page.waitForLoadState('networkidle');
  702 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/45_admin_orders_donggoi.png'), fullPage: true });
  703 | 
  704 |     // 5. Navigate to XuatKho (Dispatched list)
  705 |     await page.goto('http://localhost:56919/Admin/HoaDon/XuatKho');
  706 |     await page.waitForLoadState('networkidle');
  707 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/46_admin_orders_xuatkho.png'), fullPage: true });
  708 | 
  709 |     // 6. Navigate to HoanThanh (Completed orders)
  710 |     await page.goto('http://localhost:56919/Admin/HoaDon/HoanThanh');
  711 |     await page.waitForLoadState('networkidle');
  712 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/47_admin_orders_hoanthanh.png'), fullPage: true });
  713 |     
  714 |     console.log('Verified Admin Order processing step pages successfully.');
  715 |   });
  716 | 
  717 | 
  718 | 
  719 | 
  720 | 
  721 | 
  722 | 
  723 | 
  724 | 
  725 |   test('TC021 - Admin Book Management: Duplicate Book Name Validation', async ({ page }) => {
  726 |     // 1. Login as Admin
  727 |     await page.goto('http://localhost:56919/');
  728 |     await page.waitForLoadState('networkidle');
  729 | 
  730 |     const accountToggle = page.locator('a#sidebarNavToggler').first();
  731 |     await accountToggle.scrollIntoViewIfNeeded();
  732 |     await accountToggle.click({ force: true });
  733 | 
  734 |     const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
  735 |     const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
  736 |     await usernameInput.fill('admin');
  737 |     await passwordInput.fill('123456');
  738 | 
  739 |     await page.evaluate(() => {
  740 |        window.login();
  741 |     });
  742 |     await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });
  743 | 
  744 |     // 2. Navigate to Create Product (Book) Page
  745 |     await page.goto('http://localhost:56919/Admin/SanPham/Create');
  746 |     await page.waitForLoadState('networkidle');
  747 | 
  748 |     // 3. Take screenshot of empty form
  749 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/48_admin_book_create_empty.png'), fullPage: true });
  750 | 
  751 |     // 4. Fill form with a duplicate book name (e.g. "Mô hình tài chính cơ bản")
  752 |     const bookForm = page.locator('form');
  753 |     await bookForm.locator('input[name="Name"]').fill('Mô hình tài chính cơợ bụn');
> 754 |     await bookForm.locator('input[name="MetaTitle"]').fill('mo-hinh-tai-chinh-co-ban');
      |                                                       ^ Error: locator.fill: Test timeout of 10000ms exceeded.
  755 |     await bookForm.locator('textarea[name="Mota"]').fill('Mô tả sách tài chính cơ bản trùng lặp');
  756 |     await bookForm.locator('input[name="GiaTien"]').fill('120000');
  757 |     await bookForm.locator('input[name="GiaNhap"]').fill('100000');
  758 |     await bookForm.locator('input[name="TacGia"]').fill('Tác giả QA');
  759 |     await bookForm.locator('input[name="NhaXuatBan"]').fill('NXB Tài Chính');
  760 | 
  761 |     // Select category if available
  762 |     const catSelect = bookForm.locator('select[name="CategoryID"]');
  763 |     if (await catSelect.count() > 0) {
  764 |       await catSelect.selectOption({ index: 1 });
  765 |     }
  766 | 
  767 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/49_admin_book_create_duplicate_filled.png') });
  768 | 
  769 |     // 5. Submit form
  770 |     const submitBtn = bookForm.locator('input[type="submit"]').first();
  771 |     await submitBtn.click({ force: true });
  772 |     await page.waitForLoadState('networkidle');
  773 | 
  774 |     // 6. Verify duplicate book validation message
  775 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/50_admin_book_create_duplicate_error.png'), fullPage: true });
  776 | 
  777 |     const validationSummary = page.locator('.text-danger, .validation-summary-errors, .alert-danger').first();
  778 |     await expect(validationSummary).toBeVisible();
  779 |     const errText = await validationSummary.textContent();
  780 |     console.log('Book Creation Duplicate Validation Error Text:', errText);
  781 |     expect(errText.length).toBeGreaterThan(0);
  782 |   });
  783 | 
  784 |   test('TC022 - Admin Procurement Management: Procurement Order List States', async ({ page }) => {
  785 |     // 1. Login as Admin
  786 |     await page.goto('http://localhost:56919/');
  787 |     await page.waitForLoadState('networkidle');
  788 | 
  789 |     const accountToggle = page.locator('a#sidebarNavToggler').first();
  790 |     await accountToggle.scrollIntoViewIfNeeded();
  791 |     await accountToggle.click({ force: true });
  792 | 
  793 |     const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
  794 |     const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
  795 |     await usernameInput.fill('admin');
  796 |     await passwordInput.fill('123456');
  797 | 
  798 |     await page.evaluate(() => {
  799 |        window.login();
  800 |     });
  801 |     await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });
  802 | 
  803 |     // 2. Navigate to NhapHang (All Procurement Orders)
  804 |     await page.goto('http://localhost:56919/Admin/NhapHang/Index');
  805 |     await page.waitForLoadState('networkidle');
  806 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/51_admin_procurement_all.png'), fullPage: true });
  807 | 
  808 |     // 3. Navigate to Duyet (Pending Confirmation Procurement Orders)
  809 |     await page.goto('http://localhost:56919/Admin/NhapHang/Duyet');
  810 |     await page.waitForLoadState('networkidle');
  811 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/52_admin_procurement_duyet.png'), fullPage: true });
  812 | 
  813 |     // 4. Navigate to NhapKho (Incoming Warehouse Orders)
  814 |     await page.goto('http://localhost:56919/Admin/NhapHang/NhapKho');
  815 |     await page.waitForLoadState('networkidle');
  816 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/53_admin_procurement_nhapkho.png'), fullPage: true });
  817 | 
  818 |     // 5. Navigate to HoanThanh (Completed Procurement Orders)
  819 |     await page.goto('http://localhost:56919/Admin/NhapHang/HoanThanh');
  820 |     await page.waitForLoadState('networkidle');
  821 |     await page.screenshot({ path: path.join(__dirname, 'screenshots/54_admin_procurement_hoanthanh.png'), fullPage: true });
  822 | 
  823 |     console.log('Procurement Admin workflows verified successfully.');
  824 |   });
```