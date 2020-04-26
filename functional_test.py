import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import unittest


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Edge("msedgedriver.exe")

    def tearDown(self):
        self.browser.quit()

    def another_user_can_see_images_and_new_image_when_user_add_new_image(self):
        # Kitsanapong login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kitsanapong')
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()
        time.sleep(2)
        # He go to student and tutor list
        student_and_tutor_list_btn = self.browser.find_element_by_id('student_and_tutor_list')
        student_and_tutor_list_btn.click()
        time.sleep(2)
        # He click on Nattakrit profile
        nattakrit_profile_btn = self.browser.find_element_by_id('user_nattakrit')
        nattakrit_profile_btn.click()
        time.sleep(2)
        # He saw 3 images from Nattakrit profile
        self.browser.find_element_by_id('pic_1')
        self.browser.find_element_by_id('pic_2')
        self.browser.find_element_by_id('pic_3')
        time.sleep(2)
        # Nattakrit login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('nattakrit')
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
        # Kitsanapong login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kitsanapong')
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()
        time.sleep(2)
        # He go to student and tutor list
        student_and_tutor_list_btn = self.browser.find_element_by_id('student_and_tutor_list')
        student_and_tutor_list_btn.click()
        time.sleep(2)
        # He click on Nattakrit profile
        nattakrit_profile_btn = self.browser.find_element_by_id('user_nattakrit')
        nattakrit_profile_btn.click()
        time.sleep(2)
        # He saw 3 old images and 1 new image from Nattakrit profile
        self.browser.find_element_by_id('pic_1')
        self.browser.find_element_by_id('pic_2')
        self.browser.find_element_by_id('pic_3')
        self.browser.find_element_by_id('pic_4')
        time.sleep(2)

    def test_user_can_comment_and_delete_comment_on_another_profile(self):
        # Kitsanapong login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kitsanapong')
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()
        time.sleep(2)
        # He go to student and tutor list
        student_and_tutor_list_btn = self.browser.find_element_by_id('student_and_tutor_list')
        student_and_tutor_list_btn.click()
        time.sleep(2)
        # He click on Nattakrit profile
        nattakrit_profile_btn = self.browser.find_element_by_id('user_nattakrit')
        nattakrit_profile_btn.click()
        time.sleep(2)
        # He type "Nattakrit is a fast learner, I taught Math to him and he is understand very fast!"
        comment_textbox = self.browser.find_element_by_id('id_comment')
        comment_textbox.send_keys("Nattakrit is a fast learner, I taught Math to him and he is understand very fast!")
        time.sleep(2)
        # So, He give Nattakrit 5 star
        self.browser.find_element_by_xpath("//select[@name='star']/option[text()='5']").click()
        time.sleep(2)
        # After all that, He submit comment
        comment_btn = self.browser.find_element_by_id('comment_submit_btn')
        comment_btn.click()
        time.sleep(2)
        # He saw comment he posted
        comment_data = self.browser.find_element_by_id('comment_kitsanapong').text
        self.assertIn(comment_data,
                      "Comment : Nattakrit is a fast learner, "
                      "I taught Math to him and he is understand very fast!")
        time.sleep(2)
        # He try to add more comment to Nattakrit profile
        # He type "Also he taught me Software Development very clear. Recommend!"
        comment_textbox = self.browser.find_element_by_id('id_comment')
        comment_textbox.send_keys("Also he taught me Software Development very clear. Recommend!")
        time.sleep(2)
        # So, He give Nattakrit 5 star
        self.browser.find_element_by_xpath("//select[@name='star']/option[text()='5']").click()
        time.sleep(2)
        # After all that, He submit comment
        comment_btn = self.browser.find_element_by_id('comment_submit_btn')
        comment_btn.click()
        time.sleep(2)
        # He saw alert that he can't comment more than one on Nattakrit profile
        alert = self.browser.switch_to.alert
        time.sleep(2)
        # so he accept alert and return to Nattakrit profile
        alert.accept()
        time.sleep(2)
        # Nattakrit login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('nattakrit')
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()
        time.sleep(2)
        # Then, He go to his profile page
        my_profile_btn = self.browser.find_element_by_id('profile_btn')
        my_profile_btn.click()
        time.sleep(2)
        # He saw new comment from Kitsanapong
        comment_data = self.browser.find_element_by_id('comment_kitsanapong').text
        self.assertIn(comment_data,
                      "Comment : Nattakrit is a fast learner, "
                      "I taught Math to him and he is understand very fast!")
        time.sleep(2)
        # Kitsanapong think he's over compliment so
        # he login to Match and Learn website and delete his comment
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kitsanapong')
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()
        time.sleep(2)
        # He go to student and tutor list
        student_and_tutor_list_btn = self.browser.find_element_by_id('student_and_tutor_list')
        student_and_tutor_list_btn.click()
        time.sleep(2)
        # He click on Nattakrit profile
        nattakrit_profile_btn = self.browser.find_element_by_id('user_nattakrit')
        nattakrit_profile_btn.click()
        time.sleep(2)
        comment_delete_btn = self.browser.find_element_by_id('delete_comment_btn_kitsanapong')
        comment_delete_btn.click()
        time.sleep(2)
        # He saw his comment is deleted (which mean element is gone)
        element_gone = len(self.browser.find_elements_by_id('comment_kitsanapong'))
        self.assertEqual(element_gone, 0)
        time.sleep(2)
        # Now he can comment to Nattakrit again
        self.browser.find_element_by_id('id_comment')
        self.browser.find_element_by_id('comment_submit_btn')
        time.sleep(2)
        # He type "Nattakrit is a fast learner."
        comment_textbox = self.browser.find_element_by_id('id_comment')
        comment_textbox.send_keys("Nattakrit is a fast learner.")
        time.sleep(2)
        # So, He give Nattakrit 3 star
        self.browser.find_element_by_xpath("//select[@name='star']/option[text()='3']").click()
        time.sleep(2)
        # After all that, He submit comment
        comment_btn = self.browser.find_element_by_id('comment_submit_btn')
        comment_btn.click()
        time.sleep(2)
        # He saw comment he posted
        comment_data = self.browser.find_element_by_id('comment_kitsanapong').text
        self.assertIn(comment_data, "Comment : Nattakrit is a fast learner.")
        time.sleep(2)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
