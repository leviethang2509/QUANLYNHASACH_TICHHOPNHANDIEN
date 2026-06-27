using Microsoft.Playwright;
using System;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

class Program
{
    public static async Task Main(string[] args)
    {
        using var playwright = await Playwright.CreateAsync();
        
        // Launch locally installed Chrome
        await using var browser = await playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = true,
            ExecutablePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        });

        var context = await browser.NewContextAsync();
        var page = await context.NewPageAsync();

        Console.WriteLine("Navigating to homepage...");
        await page.GotoAsync("http://localhost:56919/");
        await page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        // Verify title
        var title = await page.TitleAsync();
        if (title.Contains("Nhà sách Tân Hạnh"))
        {
            Console.WriteLine("Homepage title verified: " + title);
        }
        else
        {
            Console.WriteLine("Title verification failed! Actual title: " + title);
        }

        // Open Login sidebar
        Console.WriteLine("Opening login sidebar...");
        var accountToggle = page.Locator("a#sidebarNavToggler").First;
        await accountToggle.WaitForAsync(new LocatorWaitForOptions { State = WaitForSelectorState.Visible });
        await accountToggle.ClickAsync();

        // Fill credentials
        Console.WriteLine("Filling credentials...");
        var usernameInput = page.Locator("#sidebarContent form#loginForm input[name='UserName']").First;
        var passwordInput = page.Locator("#sidebarContent form#loginForm input[name='password']").First;
        var loginButton = page.Locator("#sidebarContent form#loginForm a[onclick='login()']").First;

        await usernameInput.WaitForAsync(new LocatorWaitForOptions { State = WaitForSelectorState.Visible });
        await usernameInput.FillAsync("admin");
        await passwordInput.FillAsync("123456");

        // Submit form
        Console.WriteLine("Submitting login form...");
        await loginButton.ClickAsync();

        // Wait for redirect URL
        try
        {
            await page.WaitForURLAsync("**/Admin/Homes/Index", new PageWaitForURLOptions { Timeout = 10000 });
            Console.WriteLine("Successfully logged in! Current URL: " + page.Url);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Redirect failed or timed out: " + ex.Message);
        }

        await context.CloseAsync();
        await browser.CloseAsync();
    }
}

