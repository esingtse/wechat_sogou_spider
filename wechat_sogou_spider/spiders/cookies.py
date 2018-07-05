#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 09:18
# @Author  : Esing
# @File    : cookies.py
# @Software: PyCharm

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
import redis,logging,time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from wechat_sogou_spider.config import DEFAULT_BROWSER,PHANTOMJS_PATH,QR_CODE_PATH


class CookiesManager(object):
    def __init__(self,browser_type=DEFAULT_BROWSER):
        self.browser_type = browser_type

    def _init_browser(self):
        broswer = webdriver.Chrome(executable_path=PHANTOMJS_PATH)
        broswer.set_window_size(1024,768)
        return broswer

    def get_cookies_from_mp(self, driver):
        print u'进入微信公众号登录页面...'
        broswer = driver
        broswer.delete_all_cookies()
        broswer.get('https://mp.weixin.qq.com/')
        wait = WebDriverWait(broswer,13)
        try:
            login_name = wait.until(EC.presence_of_element_located((By.NAME,"account")))
            password = wait.until(EC.presence_of_element_located((By.NAME,"password")))
            submit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"btn_login")))
            login_name.clear()
            login_name.send_keys(str('13143113435@139.com'))
            password.send_keys(str('Xie199210'))
            submit.click()
            self.is_login(broswer)
        except Exception as e:
            logging.error(e)

    def is_login(self, driver):
        browser = driver
        i = 13
        time.sleep(3)
        text = browser.find_element_by_xpath('//h2[@class="weui-desktop-page__title"]').text
        time.sleep(3)
        while i>0:
            if text == u'安全保护':
                print 'success login, and redirect to QR code page.'
                time.sleep(3)
                driver.get_screenshot_as_file(
                    QR_CODE_PATH + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '.png')
                time.sleep(100)
                return True
        return False


    def init_all_cookies(self, rconn):
        browser = self._init_browser()
        if not isinstance(rconn, type(redis.Redis())):
            logging.info('rconn不是一个Redis连接实例')
            return False
        cookies = self.get_cookies_from_mp(browser)
        if cookies:
            rconn.hset('wechat:cookie', '13143113435@139.com', cookies)
            print('{}存入Redis成功'.format('13143113435@139.com'))
            browser.quit()
            return True
        else:
            return False

    def updateCookie(self, account, rconn):
        browser = self._init_browser()
        cookies = self.get_cookies_from_mp(browser)
        browser.quit()
        if cookies:
            logging.info("updated cookie of %s " % account)
            hkey = 'weibo:cookie'
            rconn.set(hkey, account, cookies)
        else:
            logging.info('updated cookie of %s failed, Removing ' % account)
            self.removeCookie(account, rconn)

if __name__ == '__main__':
    ck = CookiesManager()
    ck.init_all_cookies(redis.Redis())