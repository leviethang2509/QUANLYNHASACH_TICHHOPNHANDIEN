import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    # Use locally installed Chrome browser
    browser = playwright.chromium.launch(
        headless=True,
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    )
    context = browser.new_context()
    page = context.new_page()
    
    print("Navigating to homepage...")
    page.goto("http://localhost:56919/")
    page.wait_for_load_state("networkidle")
    
    # Check title
    expect(page).to_have_title(re.compile("Nhà sách Tân Hạnh"))
    print("Homepage title verified!")
    
    # Click Account Toggler
    print("Opening login sidebar...")
    account_toggle = page.locator("a#sidebarNavToggler").first
    account_toggle.wait_for(state="visible")
    account_toggle.click()
    
    # Fill in Admin credentials
    print("Filling credentials...")
    username_input = page.locator("#sidebarContent form#loginForm input[name='UserName']").first
    password_input = page.locator("#sidebarContent form#loginForm input[name='password']").first
    login_button = page.locator("#sidebarContent form#loginForm a[onclick='login()']").first
    
    username_input.wait_for(state="visible")
    username_input.fill("admin")
    password_input.fill("123456")
    
    # Click login and wait for URL redirect
    print("Submitting login form...")
    login_button.click()
    
    page.wait_for_url("**/Admin/Homes/Index", timeout=10000)
    print(f"Successfully logged in! Current URL: {page.url}")
    
    # Clean up
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
