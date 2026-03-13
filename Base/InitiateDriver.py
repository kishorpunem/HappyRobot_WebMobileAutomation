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
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"],
            slow_mo=1000
        )

        context = browser.new_context()
        page = context.new_page()

        # Login flow
        page.goto("https://onboarding.qa.trukker.com/#/inquiry/add")
        # page.set_viewport_size({"width": 1920, "height": 1080})
        # page.fill("//input[@name='username']", "test1@trukker.com")
        # page.fill("//input[@name='password']", "trukker@123")
        page.click("//span[text()='Sign in with Google']")
        time.sleep(5)
        page.fill("//input[@type='email']","punem.kishor@trukker.com")
        time.sleep(5)
        page.click("//span[text()='Next']")
        time.sleep(5)
        page.fill("//input[@type='password']","Kishor@12345")
        time.sleep(5)
        page.click("//span[text()='Next']")
        time.sleep(30)
        # page.click("//button[@type='submit']")
        page.wait_for_load_state("networkidle")

        print("✅ Login successful")
        return p, browser, context, page
