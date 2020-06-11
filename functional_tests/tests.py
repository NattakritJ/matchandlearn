import os
from selenium import webdriver
from django.test import LiveServerTestCase
import time
import unittest


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self, username):
        self.browser.get(self.live_server_url + '/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys(username)
        password_box.send_keys("1qaz2wsx3edc4rfv5tgb")
        login_button = self.browser.find_element_by_id('login_btn')
        login_button.click()

    def anonymous_can_signup(self, username, first_name, last_name, email):
        # Kitsanapong found Match and Learn website
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)
        time.sleep(2)
        # He saw he need to register before using this website
        signup_link = self.browser.find_element_by_id('signup_link')
        signup_link.click()
        time.sleep(2)
        # He type his information on website
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password1')
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        first_name_input = self.browser.find_element_by_id('id_first_name')
        last_name_input = self.browser.find_element_by_id('id_last_name')
        age_input = self.browser.find_element_by_id('id_age')
        gender_input = self.browser.find_element_by_xpath("//select[@name='gender']/option[text()='Male']")
        email_input = self.browser.find_element_by_id('id_email')
        college_input = self.browser.find_element_by_id('id_college')
        username_input.send_keys(username)
        password_input.send_keys("1qaz2wsx3edc4rfv5tgb")
        password_confirm_input.send_keys("1qaz2wsx3edc4rfv5tgb")
        first_name_input.send_keys(first_name)
        last_name_input.send_keys(last_name)
        age_input.send_keys('20')
        gender_input.click()
        email_input.send_keys(email)
        college_input.send_keys('KMUTNB')
        time.sleep(2)
        # he click sign up button
        submit_btn = self.browser.find_element_by_id('signup_btn')
        submit_btn.click()
        time.sleep(2)
        # he saw that he need to confirm his account by click link on email sent to him
        confirm_email_alert = self.browser.find_element_by_id('confirm_msg').text
        self.assertIn(confirm_email_alert, "Please confirm your email address\nto complete the registration.")
        time.sleep(2)

    def add_expertise_subject(self, username, check_profile, subject, subject_element, subject_element_result):
        self.browser.maximize_window()
        # Kitsanapong login to Match and Learn website
        self.login(username)
        time.sleep(2)
        # he go to his profile page
        profile_btn = self.browser.find_element_by_id('profile_btn')
        profile_btn.click()
        time.sleep(2)
        # he saw his profile page
        profile_full_name = self.browser.find_element_by_id('profile_fullname').text
        self.assertIn(profile_full_name, check_profile)
        # he add 'Math' into his expertise subject
        expertise_input = self.browser.find_element_by_id('subject_good_id')
        expertise_input.send_keys(subject)
        # he click submit expertise subject
        submit_btn = self.browser.find_element_by_id('add_subject')
        submit_btn.click()
        time.sleep(2)
        # he saw Math is appear on his expertise subject section
        expertise_subject = self.browser.find_element_by_id(subject_element).text
        self.assertIn(expertise_subject, subject_element_result)
        # after that, He logout
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def delete_expertise_subject_and_add_new_one(self):
        self.browser.maximize_window()
        # Kitsanapong login to Match and Learn website
        self.login("kitsanapong")
        time.sleep(2)
        # he go to his profile page
        profile_btn = self.browser.find_element_by_id('profile_btn')
        profile_btn.click()
        time.sleep(2)
        # he saw his profile page
        profile_full_name = self.browser.find_element_by_id('profile_fullname').text
        self.assertIn(profile_full_name, 'Kitsanapong Rodjing')
        # he select 'Math' from his expertise subject
        self.browser.find_element_by_id('subject_name:1').click()
        # he click remove expertise subject
        remove_btn = self.browser.find_element_by_id('remove_button_id')
        remove_btn.click()
        time.sleep(2)
        # he saw Math is disappear from his expertise subject section
        expertise_subject = len(self.browser.find_elements_by_id('subject_Math'))
        self.assertEqual(expertise_subject, 0)
        # he add 'English' into his expertise subject
        expertise_input = self.browser.find_element_by_id('subject_good_id')
        expertise_input.send_keys('English')
        # he click submit expertise subject
        submit_btn = self.browser.find_element_by_id('add_subject')
        submit_btn.click()
        time.sleep(2)
        # he saw Math is appear on his expertise subject section
        expertise_subject = self.browser.find_element_by_id('subject_English').text
        self.assertIn(expertise_subject, '1: English')
        # after that, He logout
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def user_can_add_image(self):
        self.browser.maximize_window()
        # Kitsanapong login to Match and Learn website
        self.login("kitsanapong")
        time.sleep(2)
        # Then, He go to his profile page
        my_profile_btn = self.browser.find_element_by_id('profile_btn')
        my_profile_btn.click()
        time.sleep(2)
        # He saw that he doesn't have any image in his gallery
        no_image_message = self.browser.find_element_by_id('no_image_msg').text
        self.assertIn(no_image_message, '''You don't have image in your gallery.''')
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
        # After that, he saw one image appear on his gallery
        self.browser.find_element_by_id('pic_1')
        time.sleep(2)
        # He logout from Match and Learn
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def search_and_match_other_user(self):
        self.browser.maximize_window()
        # Kitsanapong login to Match and Learn website
        self.login('kitsanapong')
        time.sleep(2)
        # he search subject that he want someone to teach 'Software Development 2'
        subject_search_input = self.browser.find_element_by_id('subject_find_id')
        subject_search_input.send_keys('Software Development 2')
        # then he click on search button
        submit_btn = self.browser.find_element_by_id('search_submit_btn')
        submit_btn.click()
        time.sleep(2)
        # he saw Nattakrit on search result
        result_name = self.browser.find_element_by_id('name_nattakrit').text
        self.assertIn(result_name, 'Nattakrit Jatupattaradit')
        # he click on Nattakrit
        profile_box = self.browser.find_element_by_id('result_nattakrit')
        profile_box.click()
        time.sleep(2)
        # he saw he can send match request to Nattakrit and can send short text to Nattakrit
        request_short_text = self.browser.find_element_by_id('text_request')
        request_short_text.send_keys('''Hi, I'm Kay. I want to learn Software Dev 2. Pls teach me!''')
        # he click on Match button
        match_btn = self.browser.find_element_by_id('match_btn')
        match_btn.click()
        time.sleep(2)
        # he saw that he sent match request. And can change his mind
        change_mind_msg = self.browser.find_element_by_id('change_match').text
        self.assertIn(change_mind_msg, 'Want to change your mind?')
        time.sleep(2)
        # he doesn't want to change his mind so he logout
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def accept_match_request(self):
        self.browser.maximize_window()
        # Nattakrit login to Match and Learn website
        self.login('nattakrit')
        time.sleep(2)
        # he notice by notification that someone was sent matching request to him
        notification_count = self.browser.find_element_by_id('notification_alert').text
        self.assertIn(notification_count, '1')
        # then, he click on student request page
        student_request_page = self.browser.find_element_by_id('student_request')
        student_request_page.click()
        time.sleep(2)
        # he saw Kitsanapong is the one who was sent request to him
        request_name = self.browser.find_element_by_id('request_name_kitsanapong').text
        self.assertIn(request_name, 'Kitsanapong Rodjing')
        # he click on Kitsanapong box
        request_box = self.browser.find_element_by_id('request_kitsanapong')
        request_box.click()
        # then he saw that he can choose to accept request or decline request. He choose accept
        accept_button = self.browser.find_element_by_id('accept_btn')
        accept_button.click()
        time.sleep(2)
        # he saw that now he's match with Kitsanapong.
        # He can now choose to unmatched but he don't want to do it.
        self.browser.find_element_by_id('unmatched_btn')
        # he logout from Match and Learn
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def user_can_see_another_profile(self):
        self.browser.maximize_window()
        # Kitsanapong login to Match and Learn website
        self.login('kitsanapong')
        time.sleep(2)
        # He go to student and tutor list to see Nattakrit is accepted him or not
        student_and_tutor_list_btn = self.browser.find_element_by_id('student_and_tutor_list')
        student_and_tutor_list_btn.click()
        time.sleep(2)
        # He saw Nattakrit profile is appear on his list so he click on Nattakrit profile
        nattakrit_profile_btn = self.browser.find_element_by_id('user_nattakrit')
        nattakrit_profile_btn.click()
        time.sleep(2)
        # He saw no image from Nattakrit profile
        nattakrit_no_image = self.browser.find_element_by_id('Nattakrit_no_image').text
        self.assertIn(nattakrit_no_image, '''Nattakrit doesn't have image in gallery''')
        time.sleep(2)
        # he logout from match and learn
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def user_can_comment_on_another_profile(self):
        self.browser.maximize_window()
        # Kitsanapong login to Match and Learn website
        self.login('kitsanapong')
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
        comment_textbox.send_keys("Nattakrit is a good teacher, He taught me Soft Dev 2 and I understand very fast!")
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
                      "Comment : Nattakrit is a good teacher, " +
                      "He taught me Soft Dev 2 and I understand very fast!")
        time.sleep(2)
        # He try to add more comment to Nattakrit profile but comment section is gone
        comment_element_gone = len(self.browser.find_elements_by_id('id_comment'))
        self.assertEqual(comment_element_gone, 0)
        # He logout from Match and Learn
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def user_can_view_comment_on_user_profile(self):
        self.browser.maximize_window()
        # Nattakrit login to Match and Learn website
        self.login('nattakrit')
        time.sleep(2)
        # Then, He go to his profile page
        my_profile_btn = self.browser.find_element_by_id('profile_btn')
        my_profile_btn.click()
        time.sleep(2)
        # He saw new comment from Kitsanapong
        comment_data = self.browser.find_element_by_id('comment_kitsanapong').text
        self.assertIn(comment_data,
                      "Comment : Nattakrit is a good teacher, " +
                      "He taught me Soft Dev 2 and I understand very fast!")
        time.sleep(2)
        # He logout from Match and Learn
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def user_can_delete_comment_and_re_comment_on_another_profile(self):
        self.browser.maximize_window()
        # Kitsanapong think he's over compliment so
        # he login to Match and Learn website and delete his comment
        self.login('kitsanapong')
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
        # He type "Nattakrit is a good teacher."
        comment_textbox = self.browser.find_element_by_id('id_comment')
        comment_textbox.send_keys("Nattakrit is a good teacher.")
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
        self.assertIn(comment_data, "Comment : Nattakrit is a good teacher.")
        time.sleep(2)
        # He logout from Match and Learn
        logout_btn = self.browser.find_element_by_id('logout_btn')
        logout_btn.click()
        # He see login page, which means he's successfully logout from Match and Learn
        signup_link = self.browser.find_element_by_id('signup_link').text
        self.assertIn(signup_link, "New to Match and Learn? Sign up now!")
        time.sleep(2)

    def test_run_all(self):
        # Kitsanapong signup
        self.anonymous_can_signup('kitsanapong', 'Kitsanapong', 'Rodjing', 'mr.kitsanapong@gmail.com')
        # Nattakrit signup
        self.anonymous_can_signup('nattakrit', 'Nattakrit', 'Jatupattaradit', 'tongu20068@hotmail.com')
        # Kitsanapong add expertise subject
        #self.add_expertise_subject('kitsanapong', 'Kitsanapong Rodjing', 'Math', 'subject_Math', '1: Math')
        # Nattakrit add expertise subject
        #self.add_expertise_subject('nattakrit', 'Nattakrit Jatupattaradit', 'Software Development 2',
                                   'subject_Software Development 2', '1: Software Development 2')
        # Kitsanapong delete expertise subject and add new subject
        #self.delete_expertise_subject_and_add_new_one()
        # Kitsanapong add image
        #self.user_can_add_image()
        # Kitsanapong search and match Nattakrit
        #self.search_and_match_other_user()
        # Nattakrit accept match request
        #self.accept_match_request()
        # Kitsanapong see Nattakrit profile
        #self.user_can_see_another_profile()
        # Kitsanapong comment on Nattakrit profile
        #self.user_can_comment_on_another_profile()
        # Nattakrit view Kitsanapong comment
        #self.user_can_view_comment_on_user_profile()
        # Kitsanapong delete and re comment on Nattakrit profile
        #self.user_can_delete_comment_and_re_comment_on_another_profile()


if __name__ == '__main__':
    unittest.main(warnings='ignore')
