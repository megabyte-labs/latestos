import os
import sys
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from latestos.client.selenium.base import SeleniumClient


class FirefoxClient(SeleniumClient):
    """
    Uses firefox through Selenium.
    """
    PROFILE_PREFERENCES = {
        "network.http.pipelining": True,
        "network.http.proxy.pipelining": True,
        "network.http.pipelining.maxrequests": 8,
        "content.notify.interval": 500000,
        "content.notify.ontimer": True,
        "content.switch.threshold": 250000,
        "browser.cache.memory.capacity": 65536, # Increase the cache capacity
        "browser.startup.homepage": "about:blank",
        "reader.parse-on-load.enabled": False, # Disable reader
        "browser.pocket.enabled": False, # Duck pocket
        "loop.enabled": False,
        "browser.chrome.toolbar_style": 1, # Text on Toolbar instead of icons
        "browser.display.show_image_placeholders": False, # No thumbnails
        "browser.display.use_document_colors": False, # No document colors
        "browser.display.use_document_fonts": 0, # Don't load document fonts
        "browser.display.use_system_colors": True, # Use system colors
        "browser.formfill.enable": False, # Autofill on forms disabled
        "browser.helperApps.deleteTempFileOnExit": True, # Delete temp files
        "browser.shell.checkDefaultBrowser": False,
        "browser.startup.homepage": "about:blank",
        "browser.startup.page": 0, # blank
        "browser.tabs.forceHide": True, # Disable tabs
        "browser.urlbar.autoFill": False, # Disable autofill on URL bar
        "browser.urlbar.autocomplete.enabled": False, # No autocomplete on bar
        "browser.urlbar.showPopup": False, # No list of URLs when typing on bar
        "browser.urlbar.showSearch": False, # Disable search bar
        "extensions.checkCompatibility": False, # Addon update disabled
        "extensions.checkUpdateSecurity": False,
        "extensions.update.autoUpdateEnabled": False,
        "extensions.update.enabled": False,
        "general.startup.browser": False,
        "plugin.default_plugin_disabled": False,
        "permissions.default.image": 2, # Image load disabled again
    }

    def setup_options(self) -> None:
        """
        Setup driver options.
        """
        self.options = Options()
        self.options.headless = True
        self.options.log.level = "TRACE"

        self.profile = FirefoxProfile()
        for pref_name, pref_val in self.__class__.PROFILE_PREFERENCES.items():
            self.profile.set_preference(pref_name, pref_val)

    def init_browser(self) -> None:
        """
        Initilizes a browser instance.
        """
        try:
            self.driver = webdriver.Firefox(
                self.profile,
                options=self.options,
                service_log_path=os.path.devnull
            )
        except WebDriverException:
            print("geckodriver executable needs to be in path")
            sys.exit(1)
