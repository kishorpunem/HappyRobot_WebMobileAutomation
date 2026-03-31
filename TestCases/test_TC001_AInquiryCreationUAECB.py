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
from api.save_execution import save_test_execution

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
    start_time = datetime.now()
    p, browser, context, page = InitiateDriver.TestLogin("WebVideos")
    CreateInquirys = InquiryCreationlocaters(page)

    print(f"\n Running test for shipper: {getdata['shippername']}")

    # If you want an explicit pause here, use page.wait_for_timeout( <ms> )
    # e.g. page.wait_for_timeout(2000)  -> this will always run regardless of HUMANIZE

    # Use human_sleep only if you want optional jitter between calls
    # human_sleep(600, 600)
    time.sleep(60)
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

    # Screenshot after submission
    screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "screenshot")
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, "CreateInquiry.png")

    try:
        page.screenshot(path=screenshot_path, timeout=60000, animations="disabled")
        print(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"Screenshot failed: {e}")

    # ---------------- Capture Inquiry Number ----------------
    inquiry_number = None

    # Step 1: Extract inquiry number
    try:
        inquiry_number = CreateInquirys.Get_Inquiry_Number()
        print("Extracted Inquiry Number:", inquiry_number)
    except Exception as e:
        print("Failed to extract inquiry number:", e)

    # Step 2: Save inquiry number to Excel
    try:
        if inquiry_number:
            save_inquiry_to_excel(inquiry_number)
            print("Inquiry number saved to Excel:", inquiry_number)
        else:
            print("No inquiry number captured.")
    except Exception as e:
        print("Failed to save inquiry number to Excel:", e)

    # Explicit wait
    page.wait_for_timeout(30000)

    # ---------------- Close Browser ----------------
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

    # ---------------- Execution Data ----------------
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    inquirycreationdatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    execution_data = {
        "test_name": "UAE Inquiry_CrossBorder",
        "status": "PASS",
        "execution_time": execution_time,
        "inquiry_no": inquiry_number,
        "inquiry_movetype": "CrossBorder",
        "inquiry_creationdatetime": inquirycreationdatetime
    }

    print("Execution Data:", execution_data)

    save_test_execution(execution_data)

    # Test assertion
    assert execution_data["status"] == "PASS"