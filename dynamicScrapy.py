# ���� webdriver
from selenium import webdriver

# Ҫ����ü��̰���������Ҫ����keys��
from selenium.webdriver.common.keys import Keys

# ���û�������ָ����PhantomJS������������������
driver = webdriver.PhantomJS(executable_path=r'C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')

# ���û���ڻ�������ָ��PhantomJSλ��
# driver = webdriver.PhantomJS(executable_path="./phantomjs"))

# get������һֱ�ȵ�ҳ�汻��ȫ���أ�Ȼ��Ż��������ͨ�����Ի�������ѡ�� time.sleep(2)
url = 'http://bj.tianyancha.com/search'
driver.get(url)

# ��ȡҳ����Ϊ wrapper��id��ǩ���ı�����
data = driver.find_elements_by_class_name("ng-binding")

# ��ӡ��������
for i in data:
    print i.text

# ��ӡҳ����� "�ٶ�һ�£����֪��"
print driver.title

# ���ɵ�ǰҳ����ղ�����
driver.save_screenshot("baidu.png")

# id="kw"�ǰٶ���������������ַ���"����"
driver.find_element_by_id("kw").send_keys(u"����")

# id="su"�ǰٶ�������ť��click() ��ģ����
driver.find_element_by_id("su").click()

# ��ȡ�µ�ҳ�����
driver.save_screenshot("����.png")

# ��ӡ��ҳ��Ⱦ���Դ����
print driver.page_source

# ��ȡ��ǰҳ��Cookie
print driver.get_cookies()

# ctrl+a ȫѡ���������
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')

# ctrl+x �������������
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')

# �����������������
driver.find_element_by_id("kw").send_keys("jiyi.cn")

# ģ��Enter�س���
driver.find_element_by_id("su").send_keys(Keys.RETURN)

# ������������
driver.find_element_by_id("kw").clear()

# �����µ�ҳ�����
driver.save_screenshot("jiyi.png")

# ��ȡ��ǰurl
print driver.current_url

# �رյ�ǰҳ�棬���ֻ��һ��ҳ�棬��ر������
# driver.close()

# �ر������
driver.quit()