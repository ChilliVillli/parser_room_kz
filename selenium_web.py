# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from time import sleep
#
# try:
#     driver = webdriver.Chrome()
#     driver.get('https://store-old.bezlimit.ru/app/login')
#     login_input = driver.find_element(By.ID, 'loginform-login')
#     login_input.clear()
#     login_input.send_keys('519891')
#     sleep(3)
#     password_input = driver.find_element(By.ID, 'loginform-password')
#     password_input.clear()
#     password_input.send_keys('4qt')
#     sleep(3)
#     password_input.send_keys(Keys.ENTER)
#     sleep(3)
#     search = driver.find_element(By.LINK_TEXT, 'Поиск номера').click()
#     sleep(5)
#     button = driver.find_element(By.CSS_SELECTOR, 'button.btn,btn_big,btn_wide,btn_purple,btn_mt,preloader').click()
#     sleep(5)
#     numbers = driver.find_element(By.CLASS_NAME, 'reserved-phones_count').text
#     all_num = re.findall(r'\b\d+\b', numbers)
#     all_numbers = int(all_num[0]+all_num[1])
#
# except Exception as ex:
#     print(ex)
# finally:
#     driver.close()
#     driver.quit()