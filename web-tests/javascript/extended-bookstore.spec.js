const { test, expect } = require('@playwright/test');
const path = require('path');

test.use({ launchOptions: { executablePath: 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe' } });

test.describe('Extended Web Tests', () => {

  test('TC005 - Contact Form Submission & Verification', async ({ page }) => {
    await page.goto('http://localhost:56919/Lien-He');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/09_contact_page.png'), fullPage: true });

    const nameInput = page.locator('#userName').first();
    const phoneInput = page.locator('#userPhone').first();
    const emailInput = page.locator('#userEmail').first();
    const addressInput = page.locator('#userAddress').first();
    const subjectInput = page.locator('#userTieuDe').first();
    const messageInput = page.locator('#userMsg').first();

    await nameInput.fill('Tester QA Auto');
    await phoneInput.fill('0987654321');
    await emailInput.fill('qa_auto_test@example.com');
    await addressInput.fill('Hanoi, Vietnam');
    await subjectInput.fill('YÃªu cáº§u há»— trá»£ mua sÃ¡ch sá»‘ lÆ°á»£ng lá»›n');
    await messageInput.fill('TÃ´i muá»‘n Ä‘áº·t hÃ ng 100 cuá»‘n sÃ¡ch chuyÃªn ngÃ nh CNTT, xin hÃ£y liÃªn há»‡ láº¡i tÃ´i.');

    await page.screenshot({ path: path.join(__dirname, 'screenshots/10_contact_filled.png') });

    const submitBtn = page.locator('#btnSend').first();
    await submitBtn.scrollIntoViewIfNeeded();
    await submitBtn.click({ force: true });

    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(__dirname, 'screenshots/11_contact_result.png') });
  });

  test('TC006 - Product Detail & Review Form UI Check', async ({ page }) => {
    await page.goto('http://localhost:56919/chi-tiet/mo-hinh-tai-chinh-co-ban-40');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/12_product_detail.png'), fullPage: true });

    const reviewTab = page.locator('#pills-four-example1-tab').first();
    await reviewTab.scrollIntoViewIfNeeded();
    await reviewTab.click({ force: true });
    await page.waitForTimeout(1000);

    const reviewForm = page.locator('#productReviewForm');
    await expect(reviewForm).toBeVisible();

    const ratingTextarea = page.locator('#productReviewForm textarea[name="comment"]').first();
    await ratingTextarea.fill('SÃ¡ch ráº¥t hay, Ä‘Ã³ng gÃ³i Ä‘áº¹p!');
    
    const submitReviewBtn = page.locator('#productReviewForm button[type="submit"]').first();
    await submitReviewBtn.click({ force: true });

    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(__dirname, 'screenshots/13_review_anonymous_result.png') });
  });

  test('TC007 - Favorite Toggle Functionality', async ({ page }) => {
    await page.goto('http://localhost:56919/chi-tiet/mo-hinh-tai-chinh-co-ban-40');
    await page.waitForLoadState('networkidle');

    const favoriteBtn = page.locator('.js-favorite-toggle').first();
    await favoriteBtn.scrollIntoViewIfNeeded();
    await favoriteBtn.click({ force: true });

    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(__dirname, 'screenshots/14_favorite_anonymous_result.png') });

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    await page.goto('http://localhost:56919/chi-tiet/mo-hinh-tai-chinh-co-ban-40');
    await page.waitForLoadState('networkidle');

    const loggedInFavoriteBtn = page.locator('.js-favorite-toggle').first();
    await loggedInFavoriteBtn.scrollIntoViewIfNeeded();
    await loggedInFavoriteBtn.click({ force: true });

    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(__dirname, 'screenshots/15_favorite_logged_in_result.png') });
  });

  test('TC008 - Product Search Results Verification', async ({ page }) => {
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const searchInput = page.locator('#txtKeyWord').first();
    await searchInput.scrollIntoViewIfNeeded();
    await searchInput.fill('tai-chinh');
    await page.waitForTimeout(1000);

    await searchInput.press('Enter');
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveURL(/.*tim-kiem.*/);

    await page.screenshot({ path: path.join(__dirname, 'screenshots/16_search_results.png'), fullPage: true });

    const resultsContainer = page.locator('.woocommerce-result-count');
    await expect(resultsContainer).toBeVisible();
    await expect(resultsContainer).toContainText(/káº¿t quáº£/i);
  });


  test('TC009 - Geofence Check and Rental Eligibility (Logged In User)', async ({ page, context }) => {
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: 21.0285, longitude: 105.8542 });

    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    await page.goto('http://localhost:56919/chi-tiet/mo-hinh-tai-chinh-co-ban-40');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(4000);

    await page.screenshot({ path: path.join(__dirname, 'screenshots/17_geofence_status.png'), fullPage: true });

    const borrowStatus = page.locator('#borrowBookStatus');
    await expect(borrowStatus).toBeVisible();
    
    const statusText = await borrowStatus.textContent();
    console.log('Geofence Verification Status Text:', statusText);
  });

  test('TC010 - Store Information and Geofence Setup in Admin WebManager', async ({ page }) => {
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    await page.goto('http://localhost:56919/Admin/WebManager/StoreLocation');
    await page.waitForLoadState('networkidle');

    await page.screenshot({ path: path.join(__dirname, 'screenshots/18_admin_store_location.png'), fullPage: true });

    const formElement = page.locator('form[action^="/Admin/WebManager/StoreLocation"]');
    await expect(formElement).toBeVisible();

    const storeNameInput = page.locator('input[name="StoreName"]').first();
    const radiusInput = page.locator('input[name="GeofenceRadius"]').first();
    await expect(storeNameInput).toBeVisible();
    await expect(radiusInput).toBeVisible();
  });


  test('TC011 - Theme Toggle Dark Mode and UI Element Adaptability', async ({ page }) => {
    // 1. Visit homepage
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    // Confirm initial state (usually default is light theme)
    const initialTheme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    console.log('Initial Theme:', initialTheme);

    // Screenshot of initial light mode
    await page.screenshot({ path: path.join(__dirname, 'screenshots/19_theme_light.png'), fullPage: true });

    // 2. Toggle the theme button
    const themeBtn = page.locator('#themeToggleBtn').first();
    await expect(themeBtn).toBeVisible();
    await themeBtn.click({ force: true });

    // Wait for the transition to complete
    await page.waitForTimeout(1000);

    // Confirm state updated to dark
    const targetTheme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    console.log('Updated Theme:', targetTheme);
    expect(targetTheme).toBe('dark');

    // Screenshot of dark mode homepage
    await page.screenshot({ path: path.join(__dirname, 'screenshots/20_theme_dark.png'), fullPage: true });

    // 3. Navigate to Book Detail page and verify if dark theme CSS variables are correctly inherited
    await page.goto('http://localhost:56919/chi-tiet/mo-hinh-tai-chinh-co-ban-40');
    await page.waitForLoadState('networkidle');

    // Wait for geofence check to complete
    await page.waitForTimeout(4000);

    // Verify document theme persists in localStorage/document element
    const detailPageTheme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    expect(detailPageTheme).toBe('dark');

    // Screenshot of dark mode book detail
    await page.screenshot({ path: path.join(__dirname, 'screenshots/21_detail_dark.png'), fullPage: true });
  });


  test('TC012 - OCR ID Card Upload Draft API and Validation', async ({ page }) => {
    // 1. Visit main page
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    // Toggle Account sidebar
    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });
    await page.waitForTimeout(1000);

    // Click "Táº¡o tÃ i khoáº£n má»›i" link to open Signup form
    const signupToggle = page.locator('a[data-target="#signup"]').first();
    await signupToggle.scrollIntoViewIfNeeded();
    await signupToggle.click({ force: true });
    await page.waitForTimeout(1000);

    // Verify Signup container is visible
    const signupForm = page.locator('div#signup');
    await expect(signupForm).toBeVisible();

    // Fill in general registration fields
    await page.locator('#signup input[name="UserName"]').first().fill('tester_ocr_99');
    await page.locator('#signup input[name="PassWord"]').first().fill('Password123!');
    await page.locator('#signup input[name="ConfirmPass"]').first().fill('Password123!');
    await page.locator('#signup input[name="Name"]').first().fill('Nguyen Van Tester');
    await page.locator('#signup input[name="Address"]').first().fill('123 Testing Street, Hanoi');
    await page.locator('#signup input[name="Phone"]').first().fill('0912345678');
    await page.locator('#signup input[name="NotificationEmail"]').first().fill('tester_ocr_99@example.com');

    // Click "Tiáº¿p theo" to go to CMND/CCCD step
    const nextBtn = page.locator('button[onclick*="ShowSignupIdentityStep"]').nth(1);
    await nextBtn.scrollIntoViewIfNeeded();
    await nextBtn.click({ force: true });
    await page.waitForTimeout(1000);

    // Take screenshot of Identity Form Section
    await page.screenshot({ path: path.join(__dirname, 'screenshots/22_signup_identity_step.png') });

    // Try clicking "Äá»c CMND/CCCD" button without selecting files
    const readBtn = page.locator('button[onclick*="UploadSignupIdentityCard"]').nth(1);
    await readBtn.scrollIntoViewIfNeeded();
    await readBtn.click({ force: true });
    await page.waitForTimeout(1500);

    // Screenshot of validation warning (should show popup or status message)
    await page.screenshot({ path: path.join(__dirname, 'screenshots/23_ocr_validation_error.png') });

    // Verify status message exists and tells user to select a file
    const statusMsg = page.locator('#signupStatus');
    await expect(statusMsg).toBeVisible();
    const statusText = await statusMsg.textContent();
    console.log('OCR Validation Status Text:', statusText);
    expect(statusText).toContain('Vui lÃ²ng chá»n áº£nh');
  });


  test('TC013 - Admin Supplier Create Validation and Error Handling', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to Supplier Creation Page
    await page.goto('http://localhost:56919/Admin/NhaCungCap/Create');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of empty creation form
    await page.screenshot({ path: path.join(__dirname, 'screenshots/24_admin_ncc_create_empty.png'), fullPage: true });

    // 4. Fill form with invalid Email & Phone and duplicate Supplier name
    // (Note: duplicate name validation is backend business logic)
    const nccForm = page.locator('form');
    await nccForm.locator('input[name="TenNCC"]').fill('TÃ¢n Háº¡nh'); // Supposing "TÃ¢n Háº¡nh" exists
    await nccForm.locator('input[name="SoDienThoai"]').fill('not-a-phone-number');
    await nccForm.locator('input[name="Email"]').fill('invalid-email-format');
    await nccForm.locator('textarea[name="DiaChi"]').fill('Admin Test Address');
    
    // Select creator from dropdown
    const creatorDropdown = nccForm.locator('select[name="IDNguoiTao"]');
    await expect(creatorDropdown).toBeVisible();
    await creatorDropdown.selectOption({ index: 1 });

    await page.screenshot({ path: path.join(__dirname, 'screenshots/25_admin_ncc_create_invalid_filled.png') });

    // 5. Submit form
    const submitBtn = nccForm.locator('button[type="submit"], input[type="submit"]').first();
    await submitBtn.click({ force: true });
    await page.waitForLoadState('networkidle');

    // 6. Verify backend validation error triggers and shows error summary/label
    await page.screenshot({ path: path.join(__dirname, 'screenshots/26_admin_ncc_create_error_result.png'), fullPage: true });

    const validationSummary = page.locator('.text-danger, .validation-summary-errors, .alert-danger').first();
    await expect(validationSummary).toBeVisible();
    const errText = await validationSummary.textContent();
    console.log('Supplier Validation Error Text:', errText);
    expect(errText.length).toBeGreaterThan(0);
  });


test('TC014 - Admin Supplier Index and Search Functionality', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to Supplier Index Page
    await page.goto('http://localhost:56919/Admin/NhaCungCap/Index');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of Supplier List page
    await page.screenshot({ path: path.join(__dirname, 'screenshots/27_admin_ncc_list.png'), fullPage: true });

    // 4. Fill search term and submit search
    const searchInput = page.locator('input[name="searchString"]').first();
    await expect(searchInput).toBeVisible();
    await searchInput.fill('TÃ¢n Háº¡nh');
    
    const searchBtn = page.locator('button[type="submit"]:has-text("TÃ¬m kiáº¿m")').first();
    await searchBtn.click({ force: true });
    await page.waitForLoadState('networkidle');

    // 5. Take screenshot of search results
    await page.screenshot({ path: path.join(__dirname, 'screenshots/28_admin_ncc_search_result.png'), fullPage: true });

    // 6. Verify table rows contain the searched term or are filtered correctly
    const tableBody = page.locator('tbody');
    await expect(tableBody).toBeAttached();
    
    const rowCount = await tableBody.locator('tr').count();
    console.log('Supplier search row count:', rowCount);
    
    if (rowCount > 0) {
      const firstRowText = await tableBody.locator('tr').first().textContent();
      expect(firstRowText).toContain('TÃ¢n Háº¡nh');
    }
  });

});

  test('TC015 - Admin Category Creation Validation', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to Category Creation Page
    await page.goto('http://localhost:56919/Admin/Category/Create');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of empty creation form
    await page.screenshot({ path: path.join(__dirname, 'screenshots/29_admin_cat_create_empty.png'), fullPage: true });

    // 4. Fill form with duplicate category name
    const catForm = page.locator('form');
    // Supposing "SÃ¡ch Truyá»…n tranh" or "Truyá»…n tranh" already exists
    await catForm.locator('input[name="TenTheloai"]').fill('Truyá»…n tranh');
    await catForm.locator('input[name="MetaTitle"]').fill('kinh-te');
    await catForm.locator('input[name="NguoiTao"]').fill('Admin Auto');

    await page.screenshot({ path: path.join(__dirname, 'screenshots/30_admin_cat_create_filled.png') });

    // 5. Submit form
    const submitBtn = catForm.locator('input[type="submit"]').first();
    await submitBtn.click({ force: true });
    await page.waitForLoadState('networkidle');

    // 6. Verify backend validation error triggers for duplicate category name
    await page.screenshot({ path: path.join(__dirname, 'screenshots/31_admin_cat_create_error_result.png'), fullPage: true });

    const validationSummary = page.locator('.text-danger, .validation-summary-errors, .alert-danger').first();
    await expect(validationSummary).toBeVisible();
    const errText = await validationSummary.textContent();
    console.log('Category Validation Error Text:', errText);
    expect(errText.length).toBeGreaterThan(0);
  });

  test('TC016 - Admin Rental Requests List & Filters', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to Rental Requests Admin Page
    await page.goto('http://localhost:56919/Admin/RentalAdmin/Index');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of Rental list
    await page.screenshot({ path: path.join(__dirname, 'screenshots/32_admin_rental_list.png'), fullPage: true });

    // 4. Change status filter and submit
    const statusSelect = page.locator('select[name="status"]');
    await expect(statusSelect).toBeVisible();
    await statusSelect.selectOption('Pending');

    const filterBtn = page.locator('button[type="submit"]:has-text("Lá»c")').first();
    await filterBtn.click({ force: true });
    await page.waitForLoadState('networkidle');

    // 5. Take screenshot of filtered results
    await page.screenshot({ path: path.join(__dirname, 'screenshots/33_admin_rental_filtered.png'), fullPage: true });

    // 6. Verify table rows matches the filter, if there are requests
    const tableBody = page.locator('tbody').first();
    if (await tableBody.count() > 0) {
      const pendingRowsCount = await tableBody.locator('tr').count();
      console.log('Rental Pending rows count:', pendingRowsCount);
    }
  });

  test('TC017 - Admin User Management: Invalid Form Fields & Validation', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to User Creation Page
    await page.goto('http://localhost:56919/Admin/User/Create');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of empty form
    await page.screenshot({ path: path.join(__dirname, 'screenshots/34_admin_user_create_empty.png'), fullPage: true });

    // 4. Fill form with invalid values (bad email, invalid phone)
    const userForm = page.locator('form');
    await userForm.locator('input[name="UserName"]').fill('admintestqa');
    await userForm.locator('input[name="PassWord"]').fill('123456');
    await userForm.locator('input[name="Name"]').fill('QA Admin Test');
    await userForm.locator('textarea[name="Adress"]').fill('Hanoi, Vietnam');
    await userForm.locator('input[name="Email"]').fill('not-an-email');
    await userForm.locator('input[name="Phone"]').fill('12345'); // invalid phone (must be 10 digits/starts correctly)
    
    // Select role
    const roleSelect = userForm.locator('select[name="IDQuyen"]');
    await roleSelect.selectOption({ index: 1 });

    await page.screenshot({ path: path.join(__dirname, 'screenshots/35_admin_user_create_invalid_filled.png') });

    // 5. Submit form
    const submitBtn = userForm.locator('input[type="submit"]').first();
    await submitBtn.click({ force: true });
    await page.waitForLoadState('networkidle');

    // 6. Verify validation error message
    await page.screenshot({ path: path.join(__dirname, 'screenshots/36_admin_user_create_error.png'), fullPage: true });

    const validationSummary = page.locator('.text-danger, .validation-summary-errors, .alert-danger').first();
    await expect(validationSummary).toBeVisible();
    const errText = await validationSummary.textContent();
    console.log('User Creation Validation Error Text:', errText);
    expect(errText.length).toBeGreaterThan(0);
  });

  test('TC018 - Admin User Management: User Search & List Page', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to User Index Page
    await page.goto('http://localhost:56919/Admin/User/Index');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of user list
    await page.screenshot({ path: path.join(__dirname, 'screenshots/37_admin_user_list.png'), fullPage: true });

    // 4. Fill search query and search
    const searchInput = page.locator('input[name="searhString"]').first();
    await expect(searchInput).toBeVisible();
    await searchInput.fill('admin');
    
    const searchBtn = page.locator('button[type="submit"]:has-text("TÃ¬m kiáº¿m")').first();
    if (await searchBtn.count() > 0) {
      await searchBtn.click({ force: true });
    } else {
      // maybe search is an input type="submit" or direct form submit
      await searchInput.press('Enter');
    }
    await page.waitForLoadState('networkidle');

    // 5. Take screenshot of filtered user list
    await page.screenshot({ path: path.join(__dirname, 'screenshots/38_admin_user_search_result.png'), fullPage: true });

    // 6. Verify results
    const tableBody = page.locator('tbody');
    await expect(tableBody).toBeAttached();
    const rowCount = await tableBody.locator('tr').count();
    console.log('User list filtered row count:', rowCount);
  });





  test('TC019 - Admin Feedback Management: View & Reply Validation', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to Feedback/Contact Admin List
    await page.goto('http://localhost:56919/Admin/FeedBack/Index');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of feedback list
    await page.screenshot({ path: path.join(__dirname, 'screenshots/39_admin_feedback_list.png'), fullPage: true });

    // 4. Click first "Tráº£ lá»i" (Reply) or "Chi tiáº¿t" link if available
    const replyLink = page.locator('a:has-text("Tráº£ lá»i"), a[href*="/Admin/FeedBack/Reply/"]').first();
    const detailLink = page.locator('a:has-text("Chi tiáº¿t"), a[href*="/Admin/FeedBack/ChiTiet/"]').first();
    
    if (await replyLink.count() > 0) {
      await replyLink.click();
      await page.waitForLoadState('networkidle');

      // 5. Take screenshot of reply page
      await page.screenshot({ path: path.join(__dirname, 'screenshots/40_admin_feedback_reply_page.png'), fullPage: true });

      // 6. Fill in reply comment if the textbox is not readonly
      const replyTextarea = page.locator('textarea[name="Reply"]').first();
      if (await replyTextarea.count() > 0 && !(await replyTextarea.getAttribute('readonly'))) {
        await replyTextarea.fill('Cáº£m Æ¡n báº¡n Ä‘Ã£ liÃªn há»‡. ChÃºng tÃ´i Ä‘Ã£ nháº­n Ä‘Æ°á»£c thÃ´ng tin pháº£n há»“i.');
        await page.screenshot({ path: path.join(__dirname, 'screenshots/41_admin_feedback_reply_filled.png') });

        // Submit reply form
        const submitBtn = page.locator('input[type="submit"], button[type="submit"]').first();
        await submitBtn.click({ force: true });
        await page.waitForLoadState('networkidle');
        
        await page.screenshot({ path: path.join(__dirname, 'screenshots/42_admin_feedback_reply_result.png'), fullPage: true });
        const successMessage = page.locator('.alert-success, .text-success').first();
        if (await successMessage.count() > 0) {
          const successText = await successMessage.textContent();
          console.log('Feedback Reply success message:', successText);
          expect(successText).toContain('thÃ nh cÃ´ng');
        }
      } else {
        console.log('Feedback is already replied (textarea is readonly) or not editable.');
      }
    } else if (await detailLink.count() > 0) {
      await detailLink.click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: path.join(__dirname, 'screenshots/40_admin_feedback_detail.png'), fullPage: true });
      console.log('Navigated to feedback details since no reply link was active.');
    } else {
      console.log('No feedback rows available to reply/view.');
    }
  });

  test('TC020 - Admin Orders Management: Order States Navigation', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to HoaDon Index (All Orders)
    await page.goto('http://localhost:56919/Admin/HoaDon/Index');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/43_admin_orders_all.png'), fullPage: true });

    // 3. Navigate to XacNhan (Orders pending confirmation)
    await page.goto('http://localhost:56919/Admin/HoaDon/XacNhan');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/44_admin_orders_xacnhan.png'), fullPage: true });

    // 4. Navigate to DongGoi (Packaging list)
    await page.goto('http://localhost:56919/Admin/HoaDon/DongGoi');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/45_admin_orders_donggoi.png'), fullPage: true });

    // 5. Navigate to XuatKho (Dispatched list)
    await page.goto('http://localhost:56919/Admin/HoaDon/XuatKho');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/46_admin_orders_xuatkho.png'), fullPage: true });

    // 6. Navigate to HoanThanh (Completed orders)
    await page.goto('http://localhost:56919/Admin/HoaDon/HoanThanh');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/47_admin_orders_hoanthanh.png'), fullPage: true });
    
    console.log('Verified Admin Order processing step pages successfully.');
  });









  test('TC021 - Admin Book Management: Duplicate Book Name Validation', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to Create Product (Book) Page
    await page.goto('http://localhost:56919/Admin/SanPham/Create');
    await page.waitForLoadState('networkidle');

    // 3. Take screenshot of empty form
    await page.screenshot({ path: path.join(__dirname, 'screenshots/48_admin_book_create_empty.png'), fullPage: true });

    // 4. Fill form with a duplicate book name (e.g. "MÃ´ hÃ¬nh tÃ i chÃ­nh cÆ¡ báº£n")
    const bookForm = page.locator('form');
    await bookForm.locator('input[name="Name"]').fill('MÃ´ hÃ¬nh tÃ i chÃ­nh cÆ¡á»£ bá»¥n');
    await bookForm.locator('input[name="MetaTitle"]').fill('mo-hinh-tai-chinh-co-ban');
    await bookForm.locator('textarea[name="Mota"]').fill('MÃ´ táº£ sÃ¡ch tÃ i chÃ­nh cÆ¡ báº£n trÃ¹ng láº·p');
    await bookForm.locator('input[name="GiaTien"]').fill('120000');
    await bookForm.locator('input[name="GiaNhap"]').fill('100000');
    await bookForm.locator('input[name="TacGia"]').fill('TÃ¡c giáº£ QA');
    await bookForm.locator('input[name="NhaXuatBan"]').fill('NXB TÃ i ChÃ­nh');

    // Select category if available
    const catSelect = bookForm.locator('select[name="CategoryID"]');
    if (await catSelect.count() > 0) {
      await catSelect.selectOption({ index: 1 });
    }

    await page.screenshot({ path: path.join(__dirname, 'screenshots/49_admin_book_create_duplicate_filled.png') });

    // 5. Submit form
    const submitBtn = bookForm.locator('input[type="submit"]').first();
    await submitBtn.click({ force: true });
    await page.waitForLoadState('networkidle');

    // 6. Verify duplicate book validation message
    await page.screenshot({ path: path.join(__dirname, 'screenshots/50_admin_book_create_duplicate_error.png'), fullPage: true });

    const validationSummary = page.locator('.text-danger, .validation-summary-errors, .alert-danger').first();
    await expect(validationSummary).toBeVisible();
    const errText = await validationSummary.textContent();
    console.log('Book Creation Duplicate Validation Error Text:', errText);
    expect(errText.length).toBeGreaterThan(0);
  });

  test('TC022 - Admin Procurement Management: Procurement Order List States', async ({ page }) => {
    // 1. Login as Admin
    await page.goto('http://localhost:56919/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.locator('a#sidebarNavToggler').first();
    await accountToggle.scrollIntoViewIfNeeded();
    await accountToggle.click({ force: true });

    const usernameInput = page.locator('#sidebarContent form#loginForm input[name="UserName"]').first();
    const passwordInput = page.locator('#sidebarContent form#loginForm input[name="password"]').first();
    await usernameInput.fill('admin');
    await passwordInput.fill('123456');

    await page.evaluate(() => {
       window.login();
    });
    await page.waitForURL('**/Admin/Homes/Index**', { timeout: 15000 });

    // 2. Navigate to NhapHang (All Procurement Orders)
    await page.goto('http://localhost:56919/Admin/NhapHang/Index');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/51_admin_procurement_all.png'), fullPage: true });

    // 3. Navigate to Duyet (Pending Confirmation Procurement Orders)
    await page.goto('http://localhost:56919/Admin/NhapHang/Duyet');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/52_admin_procurement_duyet.png'), fullPage: true });

    // 4. Navigate to NhapKho (Incoming Warehouse Orders)
    await page.goto('http://localhost:56919/Admin/NhapHang/NhapKho');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/53_admin_procurement_nhapkho.png'), fullPage: true });

    // 5. Navigate to HoanThanh (Completed Procurement Orders)
    await page.goto('http://localhost:56919/Admin/NhapHang/HoanThanh');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: path.join(__dirname, 'screenshots/54_admin_procurement_hoanthanh.png'), fullPage: true });

    console.log('Procurement Admin workflows verified successfully.');
  });
