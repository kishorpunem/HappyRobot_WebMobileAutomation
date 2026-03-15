import os
import time
from playwright.sync_api import sync_playwright

class InitiateDriver:

    @staticmethod
    def TestLogin(video_subfolder: str = "Common"):
        p = sync_playwright().start()
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",  # hides headless detection
                "--start-maximized"
            ],
            slow_mo=200  # reduced from 1000 → much faster on cloud
        )

        session_file = "google_session.json"

        # ─── If saved session exists → skip login entirely ──────────
        if os.path.exists(session_file):
            context = browser.new_context(
                storage_state=session_file,
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.set_default_timeout(60000)
            page.goto("https://onboarding.qa.trukker.com/", timeout=120000)
            page.wait_for_load_state("networkidle")
            print("Session restored — skipped login")
            return p, browser, context, page

        # ─── First time → do full Google login and save session ─────
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.set_default_timeout(60000)

        page.goto("https://onboarding.qa.trukker.com/", timeout=120000)
        page.click("//span[text()='Sign in with Google']")
        page.wait_for_selector("//input[@type='email']", timeout=60000)
        page.fill("//input[@type='email']", "punem.kishor@trukker.com")
        page.click("//span[text()='Next']")
        page.wait_for_selector("//input[@type='password']", timeout=60000)
        page.fill("//input[@type='password']", "Kishor@12345")
        page.click("//span[text()='Next']")
        page.wait_for_load_state("networkidle", timeout=60000)

        # Save session so next run skips login
        context.storage_state(path=session_file)
        print("Login successful — session saved")

        return p, browser, context, page