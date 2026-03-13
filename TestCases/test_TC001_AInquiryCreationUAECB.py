import os
import time
import random
from datetime import datetime

import pytest
import subprocess
import pytz

from Base.InitiateDriver import InitiateDriver
from Pages.InquiryCreation import InquiryCreationlocaters
from DataDrivenFromExcelSheet.DataDrivenForWeB import CreateinquiryExecutionData
from DataDrivenFromExcelSheet.InqNumber_Store import save_inquiry_to_excel

# ---------------- CONFIG ----------------
# Set to True to add human-like random delays between steps.
# Set to False to run strictly with the waits you put in code (recommended for CI).
HUMANIZE = False


def human_delay_ms(base_ms: int = 120, jitter_ms: int = 80) -> int:
    """Return a randomized delay in milliseconds (base + uniform jitter)."""
    return base_ms + random.randint(0, jitter_ms)


def human_sleep(base_ms: int = 120, jitter_ms: int = 80):
    """Sleep only if HUMANIZE is enabled. Otherwise do nothing."""
    if not HUMANIZE:
        return
    ms = human_delay_ms(base_ms, jitter_ms)
    time.sleep(ms / 1000.0)
    print(f"⏱ human pause: {ms} ms (HUMANIZE=True)")


@pytest.fixture(params=CreateinquiryExecutionData.getTestdata("CreateInquiryData"))
def getdata(request):
    return request.param


@pytest.mark.order(1)
@pytest.mark.dependency(name="create_inquiry", scope="session")
def test_CreateInquiryUAECB(getdata):
    # Start browser + page
    p, browser, context, page = InitiateDriver.TestLogin("WebVideos")
    CreateInquirys = InquiryCreationlocaters(page)

    print(f"\n🚀 Running test for shipper: {getdata['shippername']}")

    # If you want an explicit pause here, use page.wait_for_timeout( <ms> )
    # e.g. page.wait_for_timeout(2000)  -> this will always run regardless of HUMANIZE

    # Use human_sleep only if you want optional jitter between calls
    human_sleep(400, 400)

    # ========== FLOW STEPS ==========
    CreateInquirys.CreateInquirDownArrow()
    human_sleep(80, 120)

    CreateInquirys.CreateInquiry()
    human_sleep(120, 160)

    CreateInquirys.Shipper_Name(getdata)
    human_sleep(120, 140)

    CreateInquirys.TruckType(getdata)
    human_sleep(80, 120)

    CreateInquirys.Sub_TruckType(getdata)
    human_sleep(80, 120)

    CreateInquirys.Commodity_Type(getdata)
    human_sleep(90, 130)

    CreateInquirys.Weight_PerTruck(getdata)
    human_sleep(80, 120)

    # If your page method itself contains waits (recommended), they will run exactly as coded.
    CreateInquirys.InquiryRecivedCalender()
    human_sleep(120, 240)

    CreateInquirys.DateandTime()
    human_sleep(120, 160)

    CreateInquirys.OK_Button()
    human_sleep(80, 120)

    CreateInquirys.Inquiry_Sources()
    human_sleep(90, 120)

    CreateInquirys.FromCity(getdata)
    human_sleep(90, 120)

    CreateInquirys.SourceAdress(getdata)
    human_sleep(90, 120)

    CreateInquirys.ToCity(getdata)
    human_sleep(90, 120)

    CreateInquirys.Dest_Address(getdata)
    human_sleep(90, 120)

    CreateInquirys.MoveDate_Calender()
    human_sleep(120, 200)

    CreateInquirys.MOveDate_Time()
    human_sleep(120, 160)

    # CreateInquirys.MOveDates()
    # human_sleep(120, 160)
    #
    # CreateInquirys.MOveTiming()
    # human_sleep(120, 160)
    #
    # CreateInquirys.MOveMinuteTime()
    # human_sleep(120, 160)

    CreateInquirys.OKbutton()
    human_sleep(80, 120)

    CreateInquirys.No_Trucks(getdata)
    human_sleep(90, 140)

    CreateInquirys.Rate_Truck(getdata)
    human_sleep(90, 140)

    CreateInquirys.Submit_Button()

    # <-- your explicit wait below will always wait exactly 12000 ms (12s) as written -->
    page.wait_for_timeout(12000)

    # Screenshot after submission (your explicit call)
    screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "screenshot")
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, "CreateInquiry.png")
    try:
        page.screenshot(path=screenshot_path)
        print(f"🖼 Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"⚠️ Screenshot failed: {e}")

    # If Success_PopUp uses internal waits, they will run exactly as coded
    inquiry_success = None
    try:
        inquiry_success = CreateInquirys.Success_PopUp()
    except Exception as e:
        print(f"⚠️ Could not read success popup: {e}")

    print(f"✅ Inquiry popup message: {inquiry_success}")

    # Save inquiry number if provided by page object
    try:
        inquiry_number = CreateInquirys.Get_Inquiry_Number()
        save_inquiry_to_excel(inquiry_number)
        print(f"📥 Inquiry number saved: {inquiry_number}")
    except Exception as e:
        inquiry_number = None
        print(f"⚠️ Failed to get/save inquiry number: {e}")

    # Keep your explicit wait here — it will be respected
    page.wait_for_timeout(30000)

    # Close everything
    try:
        page.close()
    except Exception:
        pass
    try:
        context.close()
    except Exception:
        pass
    try:
        browser.close()
    except Exception:
        pass
    try:
        p.stop()
    except Exception:
        pass

    try:
        # Small delay to ensure the browser finishes writing the video file
        time.sleep(2)

        # 1️⃣ Build timestamp in IST (Asia/Kolkata)
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(ist).strftime("%d-%m-%Y_%H-%M")

        # 2️⃣ Resolve project paths
        # __file__ → current Python file (e.g., a test file in TestCases/)
        test_dir = os.path.dirname(os.path.abspath(__file__))  # .../TestCases
        project_root = os.path.dirname(test_dir)  # .../FrameWork_Playwright

        # 3️⃣ Video directory: .../FrameWork_Playwright/Video's/WebVideos
        video_dir = os.path.join(project_root, "Video's", "WebVideos")
        os.makedirs(video_dir, exist_ok=True)  # Create folder if not present

        # 4️⃣ Build MP4 base name (with or without inquiry_number)
        if inquiry_number:
            base_name = f"InquiryCreation_{inquiry_number}_{current_time}_IST"
        else:
            base_name = f"InquiryCreation_{current_time}_IST"

        mp4_path = os.path.join(video_dir, base_name + ".mp4")

        # 5️⃣ Find all .webm files in the video directory
        webm_files = [
            os.path.join(video_dir, f)
            for f in os.listdir(video_dir)
            if f.lower().endswith(".webm")
        ]

        if not webm_files:
            print("⚠️ No .webm video found after test run.")
            return

        # 6️⃣ Select the latest .webm file (most recently created)
        latest_webm = max(webm_files, key=os.path.getctime)
        print(f"ℹ️ Latest .webm file: {latest_webm}")

        # 7️⃣ Convert .webm → .mp4 using ffmpeg with compression
        #    - libx264: good compression codec
        #    - -crf 30 : higher value = smaller size (28–32 is a good range)
        #    - -preset slow : better compression (can use medium/fast if too slow)
        #    - -vf scale=1280:-2 : reduce resolution to max width 1280px (keeps aspect ratio)
        #    - -an : drop audio (optional, saves space)
        cmd = [
            "ffmpeg",
            "-y",
            "-i", latest_webm,

            # ↓ Shrink resolution + reduce frame rate (big size saver)
            "-vf", "scale=640:-2,fps=12",  # 640px wide, 12 fps is fine for demo videos

            "-vcodec", "libx264",
            "-pix_fmt", "yuv420p",

            # ↓ Target ~1 MB for 90s  (≈ 70 kbps)
            "-b:v", "70k",
            "-maxrate", "70k",
            "-bufsize", "140k",

            "-preset", "veryfast",

            "-an",  # no audio

            # Hard cap at ~1 MB (extra safety)
            "-fs", "1000k",  # stop at about 1 MB

            mp4_path,
        ]

        print(f"🔄 Converting to compressed MP4: {mp4_path}")
        subprocess.run(cmd, check=True)
        print(f"✅ MP4 video saved successfully: {mp4_path}")

        # 8️⃣ Clean up: delete ALL .webm and .mp4 in this folder EXCEPT the new mp4
        for f in os.listdir(video_dir):
            file_path = os.path.join(video_dir, f)

            # Skip the freshly created MP4
            if file_path == mp4_path:
                continue

            # Delete any old .webm or .mp4
            if f.lower().endswith(".webm") or f.lower().endswith(".mp4"):
                try:
                    os.remove(file_path)
                    print(f"🗑️ Deleted old video file: {file_path}")
                except Exception as delete_err:
                    print(f"⚠️ Unable to delete file: {file_path}, Error: {delete_err}")

    except subprocess.CalledProcessError as ffmpeg_err:
        print(f"❌ ffmpeg conversion failed: {ffmpeg_err}")
    except Exception as e:
        print(f"⚠️ Video processing failed: {e}")
