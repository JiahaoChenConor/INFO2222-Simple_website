import sys
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from VirtualUser import AllVirtualUsers

default_target = "http://localhost:8001/"


def enter_register_username_password(driver, username, password, password_again):
    driver.find_element_by_id("inputEmail3").send_keys(username)
    driver.find_element_by_id("inputPassword3").send_keys(password)
    driver.find_element_by_id("inputPassword4").send_keys(password_again)
    driver.find_element_by_id("button_register").click()


def register(target_url, chrome_options, virtual_user, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    driver.get(target_url)
    driver.find_element_by_id("login_header").click()
    driver.find_element_by_id("register").click()

    #######################################
    # Register two password are different #
    #######################################
    print("Testing passwords are not matched:")

    enter_register_username_password(driver, virtual_user.username, virtual_user.password, 'different')

    response = driver.find_element_by_id("response").text
    if response == 'Registration failed, password not match!':
        print("----Success")

    driver.find_element_by_id("return").click()

    ####################
    # Register Success #
    ####################

    print("Testing register Successful:")
    enter_register_username_password(driver, virtual_user.username, virtual_user.password, virtual_user.password)

    response = driver.find_element_by_id("response").text
    if response == 'Registration complete, please login using your credentials':
        print("----success")

    driver.find_element_by_id("return").click()

    #######################
    # Register Duplicated #
    #######################
    print("Testing register duplicated:")

    driver.find_element_by_id("register").click()

    enter_register_username_password(driver, virtual_user.username, virtual_user.password, virtual_user.password)

    response = driver.find_element_by_id("response").text
    if response == 'Registration failed, duplicated username':
        print("----Success")

    driver.find_element_by_id("return").click()
    driver.close()


def login(target_url, chrome_options, virtual_user, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    driver.get(target_url)
    #################
    # Login Success #
    #################
    virtual_user.set_sample_user()
    print("Testing login Successful:")
    driver.find_element_by_id('login_header').click()

    driver.find_element_by_id('inputEmail3').send_keys(virtual_user.username)
    driver.find_element_by_id('inputPassword3').send_keys(virtual_user.password)
    driver.find_element_by_id('login').click()
    response = driver.find_element_by_id("response").text

    if response == 'This username-password combination is valid, welcome!':
        print("---Success")

    driver.find_element_by_id("return")

    #################
    # Login Failure #
    #################
    print("Testing login Fail:")
    driver.find_element_by_id('login_header').click()

    driver.find_element_by_id('inputEmail3').send_keys(virtual_user.username)
    driver.find_element_by_id('inputPassword3').send_keys('wrong_password123')


    driver.find_element_by_id('login').click()
    response = driver.find_element_by_id("response").text
    if response == 'This username-password combination is invalid, try again!':
        print("---Success")

    driver.find_element_by_id("return")

    ##################
    # Login As Admin #
    ##################
    print("Testing login As admin:")
    virtual_user.set_admin()
    driver.find_element_by_id('login_header').click()
    driver.find_element_by_id('inputEmail3').send_keys(virtual_user.username)
    driver.find_element_by_id('inputPassword3').send_keys(virtual_user.password)

    driver.find_element_by_id('login').click()

    response = driver.find_element_by_id("response").text
    if response == 'This username-password combination is valid, welcome!':
        print("---Success")

    driver.find_element_by_id("return")

    driver.close()


# https://stackoverflow.com/questions/62003082/elementnotinteractableexception-element-not-interactable-element-has-zero-size
def click_item_outside_viewport(driver, id):
    element = driver.find_element_by_id(id)
    ActionChains(driver).move_to_element(element).perform()
    element.click()


def browse_knowledge_page(target_url, chrome_options, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    driver.get(target_url)
    ####################
    # Browse Knowledge #
    ####################

    print("Testing browse knowledge:")
    driver.find_element_by_id("knowledge_header").click()
    print("--Success")
    print("Testing click basic_knowledge")
    click_item_outside_viewport(driver, "basic_knowledge")
    print("--Success")

    print("Testing click html_basic")
    click_item_outside_viewport(driver, "click_html_basic")
    print("--Success")

    print("Testing click css_basic")
    click_item_outside_viewport(driver, "click_css_basic")
    print("--Success")

    print("Testing click js_basic")
    click_item_outside_viewport(driver, "click_js_basic")
    print("--Success")

    print("Testing click inter_knowledge")
    click_item_outside_viewport(driver, "inter_knowledge")
    print("--Success")

    print("Testing click html_inter")
    click_item_outside_viewport(driver, "click_html_inter")
    print("--Success")

    print("Testing click css_inter")
    click_item_outside_viewport(driver, "click_css_inter")
    print("--Success")

    print("Testing click js_inter")
    click_item_outside_viewport(driver, "click_js_inter")
    print("--Success")

    print("Testing click adv_knowledge")
    click_item_outside_viewport(driver, "adv_knowledge")
    print("--Success")

    print("Testing click html_adv")
    click_item_outside_viewport(driver, "click_html_adv")
    print("--Success")

    print("Testing click css_adv")
    click_item_outside_viewport(driver, "click_css_adv")
    print("--Success")

    print("Testing click js_adv")
    click_item_outside_viewport(driver, "click_js_adv")
    print("--Success")

    print("Testing click go_top")
    click_item_outside_viewport(driver, "go_top")
    print("--Success")

    driver.close()


def post_and_reply(target_url, chrome_options, virtual_user, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    print("Testing post:")
    driver.get(target_url)
    driver.find_element_by_id("login_header").click()
    driver.find_element_by_id("register").click()
    enter_register_username_password(driver, virtual_user.username, virtual_user.password, virtual_user.password)

    driver.find_element_by_id("return").click()

    driver.find_element_by_id('login_header').click()
    driver.find_element_by_id('inputEmail3').send_keys(virtual_user.username)
    driver.find_element_by_id('inputPassword3').send_keys(virtual_user.password)
    driver.find_element_by_id('login').click()
    driver.find_element_by_id("return").click()

    driver.find_element_by_id('post_header').click()
    driver.find_element_by_id('subject').send_keys("HTML")
    driver.find_element_by_id('content').send_keys("HELLO!")
    driver.find_element_by_id('button_post').click()
    response = driver.find_element_by_id("response").text
    if response == 'Post successful':
        print("---Success")

    print("Testing reply:")
    driver.find_element_by_id('return').click()
    driver.find_element_by_link_text('HTML').click()
    driver.find_element_by_id('comment').send_keys('Hello!!!')
    driver.find_element_by_id('post').click()

    response = driver.find_element_by_id("response").text
    if response == 'Reply successful!':
        print("---Success")

    driver.find_element_by_id("return").click()

    driver.close()


def admin_delete_post(target_url, chrome_options, virtual_user, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    driver.get(target_url)
    virtual_user.set_admin()
    driver.find_element_by_id('login_header').click()
    driver.find_element_by_id('inputEmail3').send_keys(virtual_user.username)
    driver.find_element_by_id('inputPassword3').send_keys(virtual_user.password)
    driver.find_element_by_id('login').click()
    driver.find_element_by_id("return").click()

    driver.find_element_by_id("forumtopic_header").click()
    driver.find_element_by_id("delete_post").click()
    print("Testing Restoration/Deletion post by admin")
    if driver.find_element_by_id("response").text == 'Restoration/Deletion successful':
        print("---Success")
    driver.close()


def admin_delete_user(target_url, chrome_options, virtual_user, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    driver.get(target_url)
    virtual_user.set_admin()
    driver.find_element_by_id('login_header').click()
    driver.find_element_by_id('inputEmail3').send_keys(virtual_user.username)
    driver.find_element_by_id('inputPassword3').send_keys(virtual_user.password)
    driver.find_element_by_id('login').click()
    driver.find_element_by_id("return").click()

    driver.find_element_by_id("this_user_header").click()
    driver.find_element_by_id("Mute/Unmute").click()
    print("Testing Mute/unmute by admin")
    if driver.find_element_by_id("response").text == 'Mute/unmute successful':
        print("---Success")
    driver.close()


def browse_about_us(target_url, chrome_options, chrome_path):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
    driver.get(target_url)
    print("Testing about us page and contact link:")
    driver.find_element_by_id('about_header').click()
    driver.find_element_by_id('contact_CEO').click()
    print("--Success")
    driver.close()


def setup_headless_browser():
    """
       Set up headless browser
   """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    return chrome_options


def setup_virtual_users():
    """
        Set up virtual users
    """
    all_virtual_users = AllVirtualUsers()
    all_virtual_users.setup_virtual_users()
    return all_virtual_users


def select_random_virtual_user(all_virtual_users):
    """
        Select a random user
    """
    index = random.randint(0, len(all_virtual_users.users_ls) - 1)
    virtual_user = all_virtual_users.users_ls[index]
    all_virtual_users.users_ls.remove(virtual_user)
    return virtual_user


if __name__ == '__main__':
    if len(sys.argv) == 1:
        target_url = default_target
    else:
        target_url = sys.argv[1]

    chrome_options = setup_headless_browser()
    chrome_path = '/Users/jiahaochen/Downloads/chromedriver'
    all_virtual_users = setup_virtual_users()

    virtual_user = select_random_virtual_user(all_virtual_users)
    register(target_url, chrome_options, virtual_user, chrome_path)

    virtual_user = select_random_virtual_user(all_virtual_users)
    login(target_url, chrome_options, virtual_user, chrome_path)

    browse_knowledge_page(target_url, chrome_options, chrome_path)

    virtual_user = select_random_virtual_user(all_virtual_users)
    post_and_reply(target_url, chrome_options, virtual_user, chrome_path)

    admin_delete_post(target_url, chrome_options, virtual_user, chrome_path)
    admin_delete_user(target_url, chrome_options, virtual_user, chrome_path)

    browse_about_us(target_url, chrome_options, chrome_path)

