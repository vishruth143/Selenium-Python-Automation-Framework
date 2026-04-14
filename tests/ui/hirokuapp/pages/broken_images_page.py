# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.ui.base_page import BasePage


class BrokenImagesPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------

    # ------------------------------------------------------Texts-------------------------------------------------------
    _page_heading_txt = (By.XPATH, "//h3[normalize-space()='Broken Images']")

    # ------------------------------------------------------Images------------------------------------------------------
    # All <img> tags inside the main content div (excludes the GitHub banner image)
    _all_content_imgs = (By.XPATH, "//div[@id='content']//img")

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def page_heading_txt(self):
        return self.find_element(*self._page_heading_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------Images------------------------------------------------------
    @property
    def all_content_imgs(self):
        return self.find_elements(*self._all_content_imgs)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_page_loaded(self):
        return self.is_element_visible(*self._page_heading_txt)

    # -----------------------------------------------------Get Data-----------------------------------------------------
    def get_image_report(self):
        """
        Inspects every <img> inside the content div using JavaScript's
        naturalWidth property. An image that failed to load will have
        naturalWidth == 0 even though img.complete == True.

        Returns a tuple:
            broken  : list of dicts  { src, naturalWidth }  for broken images
            valid   : list of dicts  { src, naturalWidth }  for valid images
        """
        images = self.all_content_imgs
        broken = []
        valid = []

        for img in images:
            src = img.get_attribute("src") or "(no src)"
            # Execute JS against each individual element to read naturalWidth
            natural_width = self.driver.execute_script(
                "return arguments[0].naturalWidth;", img
            )
            entry = {"src": src, "naturalWidth": natural_width}
            if natural_width == 0:
                broken.append(entry)
            else:
                valid.append(entry)

        return broken, valid

