import time
from configobj import ConfigObj
from selenium import webdriver

conf = ConfigObj('config.ini', encoding='utf-8')
text = conf['CSDN']['text']
username = conf['CSDN']['username']
password = conf['CSDN']['password']

# 用来判断加载完没有
def Wait(driver, text):
    while not text in driver.execute_script("return document.documentElement.outerHTML"):
        pass

def AddSomethingToYourBlog(text, username, password):
    driver = webdriver.Chrome()
    driver.get('https://mp.csdn.net/postlist/')
    driver.find_element_by_css_selector('#app > div > div > div > div.main-login > div.main-select > ul > li:nth-child(1) > a').click()
    Wait(driver, '手机号/邮箱/用户名')
    driver.find_element_by_css_selector('#all').send_keys(username)
    driver.find_element_by_css_selector('#password-number').send_keys(password)
    driver.find_element_by_css_selector('#app > div > div > div > div.main-login > div.main-process-login > form > div > div:nth-child(6) > div > button').click()
    Wait(driver, '开始创作')
    driver.find_element_by_css_selector('#btnStart').click()

    while True:
        div = driver.find_elements_by_css_selector('.article-list-item')
        for nth in range(len(div)):
            div[nth].find_element_by_css_selector('div.list-item-title > p > a').click()
            driver.switch_to.window(driver.window_handles[-1])

            if '富文本编辑器' in driver.execute_script("return document.documentElement.outerHTML"):
                driver.switch_to.frame(0)
                driver.execute_script("document.getElementsByClassName('htmledit_views cke_editable cke_editable_themed cke_contents_ltr cke_show_borders')[0].innerHTML='<h3><span style=\"color:#f33b45;\"><strong>%s</strong></span></h3>' + document.getElementsByClassName('htmledit_views cke_editable cke_editable_themed cke_contents_ltr cke_show_borders')[0].innerHTML" % text)
                driver.switch_to.default_content()
                driver.find_element_by_css_selector('#radChl > option:nth-child(13)').click()
                driver.find_element_by_css_selector('#btnPublish').click()
                Wait(driver, '<div class="alert-container finished-box" id="alertSuccess" style="display: block;">')
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            else:
                pre = driver.find_element_by_css_selector('body > div.app.app--light > div.layout > div.layout__panel.flex.flex--row > div.layout__panel.flex.flex--column > div.layout__panel.flex.flex--row > div.layout__panel.layout__panel--editor > div.editor > pre')
                driver.execute_script("var div=document.createElement('div');div.className='cledit-section';div.innerHTML='<span class=\"token url\"># %s \\n</span><span class=\"lf\"><br><span class=\"hd-lf\" style=\"display: none\"></span></span><span class=\"lf\"><br><span class=\"hd-lf\" style=\"display: none\"></span></span>';arguments[0].insertBefore(div, document.getElementsByClassName('cledit-section')[0]);" % text, pre)

                driver.find_element_by_css_selector('body > div.app.app--light > div.layout > div.layout__panel.layout__panel--articletitle-bar > div > div.article-bar__user-box.flex.flex--row > button').click()
                Wait(driver, '保存为草稿')
                driver.find_element_by_css_selector('body > div.app.app--light > div.modal > div > div > div.modal__button-bar > button.button.btn-c-blue').click()
                Wait(driver, '<div id="alertSuccess" class="finished-box" style="">')
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
        next_page = driver.find_element_by_css_selector('#pills-tabContent > div.pagination-wrapper > nav > ul > li:last-child > a')
        if next_page.text == '':
            next_page.click()
            time.sleep(1)
        else:
            print('全部文章已添加完成')
            input('按任意键退出...')
            driver.quit()
            break

if __name__ == '__main__':
    AddSomethingToYourBlog(text, username, password)
