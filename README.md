用途:
检查chromedriver.exe版本是否匹配chrome.exe,若版本不一,则尝试更新chromedriver到同版本,以便无抛错连续调用chrome.exe

用法:
```
import update_chromedriver
update_chromedriver.update_exe()  # 强制下载更新同版本的chromedriver.exe
# 比对版本后再创建对象:
# from selenium import webdriver
# driver1 = webdriver.Chrome()
```
