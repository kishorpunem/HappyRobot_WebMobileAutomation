# File: Base/InitiateDriver.py
import os
import time
from playwright.sync_api import sync_playwright

class InitiateDriver:

    @staticmethod
    def TestLogin(video_subfolder: str = "Common"):
        """
        video_subfolder -> which folder to save videos into
        e.g. "WebVideos", "OrderBooking", "WinnerDeclaration"
        """
        p = sync_playwright().start()
        headless = os.getenv("RENDER", None) is not None
        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox","--start-maximized", "--disable-dev-shm-usage"],
            slow_mo=1000
        )

        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        page.set_default_timeout(60000)

        # Login flow
        page.goto("https://onboarding.qa.trukker.com/",
                  timeout=120000)

        # If login page appears → do login
        if page.locator("//span[text()='Sign in with Google']").is_visible():
            print("Session expired. Logging in again...")

            page.click("//span[text()='Sign in with Google']")
            page.fill("//input[@type='email']", "punem.kishor@trukker.com")
            page.click("//span[text()='Next']")
            page.fill("//input[@type='password']", "Kishor@12345")
            page.click("//span[text()='Next']")
            page.wait_for_load_state("networkidle")

            # Save session again
            context.storage_state(path="auth.json")

        else:
            print("Using existing session")
        # page.set_viewport_size({"width": 1920, "height": 1080})
        # page.fill("//input[@name='username']", "test1@trukker.com")
        # page.fill("//input[@name='password']", "trukker@123")
        # page.click("//span[text()='Sign in with Google']")
        # # time.sleep(5)
        # page.fill("//input[@type='email']","punem.kishor@trukker.com")
        # # time.sleep(5)
        # page.click("//span[text()='Next']")
        # # time.sleep(5)
        # page.fill("//input[@type='password']","Kishor@12345")
        # # time.sleep(5)
        # page.click("//span[text()='Next']")
        # # time.sleep(30)
        # # page.click("//button[@type='submit']")
        # page.wait_for_load_state("networkidle")

        print("Login successful")
        return p, browser, context, page
