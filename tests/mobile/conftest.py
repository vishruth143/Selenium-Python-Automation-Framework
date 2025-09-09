import os
import pytest
from appium.webdriver.appium_service import AppiumService
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.events import EventFiringWebDriver

from framework.listeners.event_listeners import MyEventListener
from config.config_parser import ConfigParser
from framework.utilities.emulator_launcher import launch_emulator

if os.environ["MOBILE_APP_NAME"].upper() == "KWA":
    mobile_test_env_config = ConfigParser.load_config("kwa_mobile_test_env_config")
    platform_name = mobile_test_env_config['KWA'].get("PLATFORM_NAME", "Android")
    automation_name = mobile_test_env_config['KWA'].get("AUTOMATION_NAME", "uiautomator2")
    device_name = mobile_test_env_config['KWA'].get("DEVICE_NAME", "Pixel 9 Pro XL")
    udid = mobile_test_env_config['KWA'].get("UDID", "emulator-5554")
    app_package = mobile_test_env_config['KWA'].get("APP_PACKAGE", "com.code2lead.kwad")
    app_activity = mobile_test_env_config['KWA'].get("APP_ACTIVITY", "com.code2lead.kwad.MainActivity")
    mobile_apk_relative_path = mobile_test_env_config['KWA'].get("APP_PATH", "framework/app_apk/Android_Demo_App.apk")

@pytest.fixture(scope="session")
def testdata():
    if os.environ["MOBILE_APP_NAME"].upper() == "KWA":
        return ConfigParser.load_config("kwa_mobile_test_data_config")
    return None

@pytest.fixture(scope="session", autouse=True)
def appium_server():
    print('-' * 10 + ' Starting Appium Server ' + '-' * 10)
    appium_service = AppiumService()
    appium_service.start()
    print(f"Appium service is running? - {appium_service.is_running}")
    print(f"Appium service is listening? - {appium_service.is_listening}")

    if not appium_service.is_running:
        raise RuntimeError("Appium server failed to start.")

    yield appium_service

    print('-' * 10 + ' Stopping Appium Server ' + '-' * 10)
    appium_service.stop()
    print(f"Appium service is running? - {appium_service.is_running}")
    print(f"Appium service is listening? - {appium_service.is_listening}")

@pytest.fixture()
def driver(request):
    print('-' * 10 + ' Driver - Setup ' + '-' * 10)

    run_on_cloud = mobile_test_env_config.get("RUN_ON_CLOUD", False)
    cloud_provider = mobile_test_env_config.get("CLOUD_PROVIDER", "").lower()

    if run_on_cloud:
        if cloud_provider == "lambdatest":
            lt_user = mobile_test_env_config.get("LAMBDATEST_USERNAME")
            lt_key = mobile_test_env_config.get("LAMBDATEST_ACCESS_KEY")
            is_virtual_device = mobile_test_env_config.get("IS_VIRTUAL_DEVICE", False)
            app_url = mobile_test_env_config.get("APP")

            remote_url = (
                f"https://{lt_user}:{lt_key}@"
                f"{'hub.lambdatest.com/wd/hub' if is_virtual_device else 'mobile-hub.lambdatest.com/wd/hub'}"
            )

            options = UiAutomator2Options()
            options.platform_name = mobile_test_env_config.get("PLATFORM_NAME", "Android")
            options.device_name = mobile_test_env_config.get("DEVICE_NAME", "Pixel 8 Pro")
            options.platform_version = mobile_test_env_config.get("PLATFORM_VERSION", "16")
            options.appium_version = mobile_test_env_config.get("APPIUM_VERSION", "2.16.2")
            options.app = app_url
            options.automation_name = "UiAutomator2"

            lt_options = {
                "platformName": "Android",
                "appium:deviceName": "Pixel 8 Pro",
                "appium:appiumVersion": "2.1.3",
                "appium:platformVersion": "16",
                "app": app_url,
                "appium:devicelog": "true",
                "appium:visual": "true",
                "appium:network": "true",
                "appium:video": "true",
                "appium:build": "Appium Mobile Automation",
                "appium:name": "test_kwa_demo",
                "appium:project": "KWA Demo",
                "appium:deviceOrientation": "portrait"
            }
            options.set_capability("LT:Options", lt_options)

        else:
            raise ValueError(f"Unsupported cloud provider: {cloud_provider}")

        driver_instance = webdriver.Remote(remote_url, options=options)

    else:
        launch_emulator()  # Ensure emulator is running before driver init

        options = UiAutomator2Options()
        options.platform_name = platform_name
        options.automation_name = automation_name
        options.device_name = device_name
        options.udid = udid
        options.app_package = app_package
        options.app_activity = app_activity

        apk_relative_path = mobile_apk_relative_path
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        apk_absolute_path = os.path.abspath(os.path.join(base_dir, apk_relative_path))

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
