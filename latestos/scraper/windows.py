import re
import sys
from typing import Tuple
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from latestos.scraper.base import BaseScraper
from latestos.client.selenium.firefox import FirefoxClient
from latestos.client.selenium.base import BROWSER_TIMEOUT as TIMEOUT


ISO_DOWNLOAD = "https://www.microsoft.com/en-us/software-download/windowsinsi" \
               "derpreviewiso?wa=wsignin1.0"


SELECTORS = {
    # Usually appears when not logged in yet
    "PROGRESS": "#progressLoadingMessage",
    # Appears when submitting edition options
    "ANOTHER_PROGRESS": "#progressModalMessage",
    "ISO_DOWNLOAD_HOME_LOGIN_BTN": "#mectrl_main_trigger",
    "LOGIN_PAGE_EMAIL": "#i0116",
    "LOGIN_PAGE_EMAIL_NEXT": "#idSIButton9",
    "LOGIN_PAGE_EMAIL_ERROR": "#usernameError",
    "PERSONAL_ACCOUNT": "#msaTile",
    "LOGIN_PAGE_PASSWORD": "#i0118",
    "LOGIN_PAGE_PASSWORD_NEXT": "#idSIButton9",
    "LOGIN_PAGE_PASSWORD_ERROR": "#passwordError",
    "DOWNLOAD_PAGE_HEADER": "#headerArea",
    "SELECT_EDITION": "#product-edition",
    "SUBMIT_EDITION": "#submit-product-edition",
    "SELECT_LANGUAGE": "#product-languages",
    "SUBMIT_LANGUAGE": "#submit-sku",
    "DOWNLOAD_URLS": "#card-info-content > div > div > div > a",
    "DOWNLOAD_NAMES": "#card-info-content > div > div > div > a > span",
    "DOWNLOAD_ERROR": "#errorModalTitle",
    "64BIT_DOWNLOAD": "#card-info-content > div > div:nth-child(1) > div > a",
    "ACCOUNT_BUTTON": "#meControl",
    "SIGN_OUT_BUTTON": "#mectrl_body_signOut",
}


class WindowsInsidersPreviewScraper(BaseScraper):
    def get_latest_release_data(self) -> Tuple[str, str, str]:
        """
        Gets latest OS release data.

        Returns:
            (str, str, str): iso url, checksum url, os version
        """
        # Extract data from latest release
        iso_url = self.get_iso_url()
        checksum_url = None
        version = self.get_iso_version(iso_url)

        return iso_url, checksum_url, version

    def get_iso_url(self) -> str:
        client = FirefoxClient()

        self._open_download_page(client)
        self._open_login_page(client)
        self._submit_email(client)
        self._select_personal_account(client)
        self._submit_password(client)
        self._select_product_edition(client)
        self._select_product_language(client)
        iso_url = self._get_download_link(client)

        self._attempt_logout(client)

        return iso_url

    def _open_download_page(self, client: FirefoxClient) -> None:
        try:
            client.get(ISO_DOWNLOAD)
            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, SELECTORS["PROGRESS"])
                )
            )
        except Exception as e:
            self._handle_client_error(
                client, e, f"Error while loading {ISO_DOWNLOAD}")

    def _open_login_page(self, client: FirefoxClient) -> None:
        try:
            login_button = client.driver.find_element_by_css_selector(
                SELECTORS["ISO_DOWNLOAD_HOME_LOGIN_BTN"])
            login_button.click()

            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, SELECTORS["LOGIN_PAGE_EMAIL"])
                )
            )
        except Exception as e:
            self._handle_client_error(
                client, e, f"Error while loading login form")

    def _submit_email(self, client: FirefoxClient) -> None:
        try:
            valid_email = False
            while not valid_email:
                valid_email = self._enter_and_validate_email(client)
        except Exception as e:
            self._handle_client_error(
                client, e, f"Error while submitting email")

    def _enter_and_validate_email(self, client: FirefoxClient) -> bool:
        email_input = client.driver.find_element_by_css_selector(
                SELECTORS["LOGIN_PAGE_EMAIL"])
        email = input("Enter your Microsoft's account email: ")
        email_input.send_keys(email)

        email_next = client.driver.find_element_by_css_selector(
            SELECTORS["LOGIN_PAGE_EMAIL_NEXT"])
        email_next.click()

        _ = WebDriverWait(client.driver, TIMEOUT).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                f"{SELECTORS['LOGIN_PAGE_EMAIL_ERROR']}, " \
                f"{SELECTORS['PERSONAL_ACCOUNT']}, " \
                f"{SELECTORS['LOGIN_PAGE_PASSWORD']}"
            ))
        )

        # Check if there was an error
        try:
            _ = client.driver.find_element_by_css_selector(
                SELECTORS["LOGIN_PAGE_EMAIL_ERROR"])
            return False
        except Exception:
            return True

    def _select_personal_account(self, client: FirefoxClient) -> None:
        try:
            personal_account = client.driver.find_element_by_css_selector(
                SELECTORS["PERSONAL_ACCOUNT"])
            personal_account.click()

            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, SELECTORS["LOGIN_PAGE_PASSWORD"])
                )
            )
        except NoSuchElementException as e:
            return
        except Exception as e:
            self._handle_client_error(
                client, e, f"Error while selecting account")

    def _submit_password(self, client: FirefoxClient) -> None:
        try:
            valid_password = False
            while not valid_password:
                valid_password = self._enter_and_validate_password(client)
        except Exception as e:
            self._handle_client_error(
                client, e, f"Error while submitting password")

    def _enter_and_validate_password(self, client: FirefoxClient) -> bool:
        password_input = client.driver.find_element_by_css_selector(
                SELECTORS["LOGIN_PAGE_PASSWORD"])
        password = input("Enter your Microsoft's account password: ")
        password_input.send_keys(password)

        password_next = client.driver.find_element_by_css_selector(
            SELECTORS["LOGIN_PAGE_PASSWORD_NEXT"])
        password_next.click()

        _ = WebDriverWait(client.driver, TIMEOUT).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                f"{SELECTORS['LOGIN_PAGE_PASSWORD_ERROR']}, " \
                f"{SELECTORS['DOWNLOAD_PAGE_HEADER']}"
            ))
        )

        # Check if there was an error
        try:
            _ = client.driver.find_element_by_css_selector(
                SELECTORS["LOGIN_PAGE_PASSWORD_ERROR"])
            return False
        except Exception:
            return True

    def _select_product_edition(self, client: FirefoxClient) -> None:
        try:
            edition = Select(client.driver.find_element_by_css_selector(
                SELECTORS["SELECT_EDITION"]))
            edition.select_by_index(4) # Enterprise Dev Channel
            edition_submit = client.driver.find_element_by_css_selector(
                SELECTORS["SUBMIT_EDITION"])
            edition_submit.click()

            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, SELECTORS["SELECT_LANGUAGE"])
                )
            )
        except Exception as e:
            self._handle_client_error(
                client, e, "Error while selecting product edition")

    def _select_product_language(self, client: FirefoxClient) -> None:
        try:
            language = Select(client.driver.find_element_by_css_selector(
                SELECTORS["SELECT_LANGUAGE"]))
            language.select_by_index(8) # English
            language_submit = client.driver.find_element_by_css_selector(
                SELECTORS["SUBMIT_LANGUAGE"])
            language_submit.click()

            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    f"{SELECTORS['64BIT_DOWNLOAD']}, " \
                    f"{SELECTORS['DOWNLOAD_ERROR']}"
                ))
            )

            try:
                _ = client.driver.find_element_by_css_selector(
                    SELECTORS["64BIT_DOWNLOAD"])
            except Exception as e:
                raise e
        except Exception as e:
            self._handle_client_error(
                client, e, "Error while selecting product language")

    def _get_download_link(self, client: FirefoxClient) -> str:
        try:
            link = client.driver.find_element_by_css_selector(
                SELECTORS["64BIT_DOWNLOAD"])
            return link.get_attribute("href")
        except Exception as e:
            self._handle_client_error(
                client, e, "Error while extracting download link")

    def _attempt_logout(self, client: FirefoxClient) -> None:
        try:
            # client.driver.save_screenshot("./download-page.png")
            self._logout(client)
            # client.driver.save_screenshot("./logged-out.png")
            client.close()
        except Exception:
            pass

    def _logout(self, client: FirefoxClient) -> None:
        try:
            # Look for sign out button
            account = client.driver.find_element_by_css_selector(
                SELECTORS["ACCOUNT_BUTTON"])
            account.click()

            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, SELECTORS["SIGN_OUT_BUTTON"])
                )
            )

            # Click sign out button
            sign_out = client.driver.find_element_by_css_selector(
                SELECTORS["SIGN_OUT_BUTTON"])
            sign_out.click()

            # Wait until logged out
            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, SELECTORS["PROGRESS"])
                )
            )
            _ = WebDriverWait(client.driver, TIMEOUT).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, SELECTORS["PROGRESS"])
                )
            )
        except Exception as e:
            self._handle_client_error(
                client, e, f"Error while logging out")

    def _handle_client_error(
        self, client: FirefoxClient, e: Exception, msg: str
    ) -> None:
        """
        Handles a web client error

        Args:
            client ([type]): webclient
            msg (str): additional message
            e (Exception): the raised exception

        Raises:
            Exception: exception
        """
        client.driver.save_screenshot("./error.png")
        client.close()
        print(f"{msg} - {e}")
        sys.exit(1)

    def get_iso_version(self, iso_url: str) -> str:
        """
        Extracts Windows Insiders Preview ISO version from the ISO url

        Args:
            iso_url (str): iso url

        Raises:
            ValueError: error at extracting iso version

        Returns:
            str: iso version
        """
        # This pattern will find the version, preceded by language
        # Example: en-us_19043_928
        pattern = r"(?<=Windows10_InsiderPreview_Client_x\d\d_)(.*)(?=.iso)"

        res = re.findall(pattern, iso_url)

        if not res:
            raise ValueError(f"Could not extract WIP version from {iso_url}")

        version_with_lang = res[0]

        # Extract the number, then replace _ with .
        try:
            return version_with_lang.split("_", 1)[1].replace("_", ".")
        except Exception:
            raise ValueError(
                f"Could not extract WIP version from {version_with_lang}")
