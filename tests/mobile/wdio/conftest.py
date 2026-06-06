# pylint: disable = [line-too-long, missing-module-docstring, missing-function-docstring]

import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.events import EventFiringWebDriver

from config.config_parser import ConfigParser
from framework.listeners.event_listeners import MyEventListener
from framework.utilities.emulator_launcher import launch_emulator


mobile_test_env_config = ConfigParser.load_config("wdio_mobile_test_env_config")
platform_name = mobile_test_env_config["WDIO"].get("PLATFORM_NAME", "Android")
automation_name = mobile_test_env_config["WDIO"].get("AUTOMATION_NAME", "UiAutomator2")
device_name = mobile_test_env_config["WDIO"].get("DEVICE_NAME", "Pixel_9_Pro_XL")
udid = mobile_test_env_config["WDIO"].get("UDID", "emulator-5554")
app_package = mobile_test_env_config["WDIO"].get("APP_PACKAGE", "com.wdiodemoapp")
app_activity = mobile_test_env_config["WDIO"].get("APP_ACTIVITY", "com.wdiodemoapp.MainActivity")
mobile_apk_relative_path = mobile_test_env_config["WDIO"].get(
	"APP_PATH", "./framework/app_apk/wdio/android.wdio.native.app.v2.2.0.apk"
)


@pytest.fixture(scope="session")
def testdata():
	"""Load WDIO demo mobile test data."""
	return ConfigParser.load_config("wdio_mobile_test_data_config")


@pytest.fixture()
def driver(request):
	print('-' * 10 + ' Driver - Setup ' + '-' * 10)

	launch_emulator(device_name)

	options = UiAutomator2Options()
	options.platform_name = platform_name
	options.automation_name = automation_name
	options.device_name = device_name
	options.udid = udid
	options.app_package = app_package
	options.app_activity = app_activity

	base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
	apk_absolute_path = os.path.abspath(os.path.join(base_dir, mobile_apk_relative_path))

	if not os.path.exists(apk_absolute_path):
		raise FileNotFoundError(f"APK file not found at path: {apk_absolute_path}")

	options.app = apk_absolute_path
	driver_instance = webdriver.Remote("http://127.0.0.1:4723", options=options)
	driver_instance = EventFiringWebDriver(driver_instance, MyEventListener())
	driver_instance.implicitly_wait(10)

	def teardown():
		print('-' * 10 + ' Driver - Teardown ' + '-' * 10)
		driver_instance.quit()

	request.addfinalizer(teardown)
	return driver_instance
