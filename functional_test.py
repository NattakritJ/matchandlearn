import os
from selenium import webdriver
import time
import unittest


class UploadImageToGallery(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Edge("msedgedriver.exe")

    def tearDown(self):
        self.browser.quit()

    def test_can_add_image(self):
        # Nattakrit login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('tongu20068')
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()
        time.sleep(2)
        # Then, He go to his profile page
        my_profile_btn = self.browser.find_element_by_id('profile_btn')
        my_profile_btn.click()
        time.sleep(2)
        # He saw 3 images from his gallery
        self.browser.find_element_by_id('pic_1')
        self.browser.find_element_by_id('pic_2')
        self.browser.find_element_by_id('pic_3')
        time.sleep(2)
        # He want to add image to his gallery
        add_image_btn = self.browser.find_element_by_id('add_img_btn')
        add_image_btn.click()
        time.sleep(2)
        # He select image from his system
        file_field = self.browser.find_element_by_id("id_images")
        file_field.send_keys(os.getcwd() + "/image.jpg")
        time.sleep(2)
        # and submit image to website
        add_image_submit_button = self.browser.find_element_by_id('add_image_submit_btn')
        add_image_submit_button.click()
        time.sleep(2)
        # After that, he saw one image appear on his gallery. The total of images is four.
        self.browser.find_element_by_id('pic_1')
        self.browser.find_element_by_id('pic_2')
        self.browser.find_element_by_id('pic_3')
        self.browser.find_element_by_id('pic_4')
        time.sleep(2)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
