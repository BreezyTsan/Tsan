from selenium import webdriver  # pip install selenium
from os import rename, remove
from os.path import join as osjoin, dirname, basename, isfile, splitext
from sys import executable, argv as sys_argv
from urllib import request
import winreg
from re import findall as re_findall
import zipfile
import GetFileVersionInfo
from Logger import Logger  # 记录日志文档

if 'log' not in globals():
    log = Logger(f'{splitext(sys_argv[0])[0]}.log', level='debug')


def unzip_single(src_file, member, dest_dir, password=None):
    log.logger.info(f'解压到目录[{dest_dir}]')
    if password:
        password = password.encode()
    with zipfile.ZipFile(src_file, 'r') as zf:
        try:
            zf.extract(member=member, path=dest_dir, pwd=password)              # zf.extractall(path=dest_dir, pwd=password)
            log.logger.info('解压缩成功')  # print('Extract successfully. ')
        except RuntimeError as e:
            raise OSError('Occurred an exception while extracting zip file. ' + str(e))


def update_exe(dest_dir=osjoin(dirname(executable), 'Scripts')):
    try:
        open_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe')
        ChromeFullPath = winreg.QueryValueEx(open_key, '')[0]  # 'C:\\Users\\hn2018\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
    finally:
        try:
            winreg.CloseKey(open_key)
        finally:
            pass
    version_full = GetFileVersionInfo.getFileVersionInfo(ChromeFullPath)['FileVersion']  # '94.0.xxxx.xx' 本机现有的
    version_main = version_full.split('.')[0]  # '94' 主版本号
    url_base = 'https://googlechromelabs.github.io/chrome-for-testing/'
    try:
        html = request.urlopen(url_base).read().decode()  # 应该是个json文本
    except:
        log.logger.error(f"无法连接到ChromeDriver更新服务器 {url_base}")
        raise ConnectionError("Can't connect to the server")
    else:
        pattern = r"https://edgedl\.me\.gvt1\.com/edgedl/chrome/chrome-for-testing/[0-9\.]+/win64/chromedriver-win64\.zip"
        matches = re_findall(pattern, html)
    v_dict = {re_findall(r"/([0-9\.]+)/", c)[0]: c for c in matches}  # {'完整版本号xxx.x.xxxx.xx': url, ...}
    available_versions = {c.split('.')[0]: v_dict[c] for c in v_dict.keys()}  # {'主版本号': url, ...}
    if version_main not in available_versions:
        log.logger.error(f'版本不适 本地谷歌浏览器[{version_full}],服务器chromedriver[{".".join(available_versions.keys())}]')
        raise KeyError("There isn't has a chromedriver that supports your Chrome version. ")
    zip_download = f'{available_versions[version_main]}'
    zip_name = basename(zip_download)
    log.logger.info(f'开始下载 [{zip_download}]')
    try:
        request.urlretrieve(zip_download, zip_name)
    except:
        log.logger.error(f'下载失败 [{zip_name}]')
    else:
        member_file = 'chromedriver-win64/chromedriver.exe'
        unzip_single(src_file=zip_name, member=member_file, dest_dir=dest_dir)
        if isfile(f'{dest_dir}/{basename(member_file)}'):  # 移动文件讲究先判断删旧再移新
            remove(f'{dest_dir}/{basename(member_file)}')  # 删除命令
        dst = f'{dest_dir}/{basename(member_file)}'
        rename(src=f'{dest_dir}/{member_file}', dst=dst)  # 移动方法即改名方法
        log.logger.info(f'更新成功 [{dst}]')


def test_webdriver():
    try:
        driver1 = webdriver.Chrome()  # 调用谷歌浏览器 - 开始
    except Exception as e:
        log.logger.info('需要更新 chromedriver.exe')
        update_exe()  # 强制下载更新同版本的chromedriver.exe
        driver1 = webdriver.Chrome()
    finally:
        if 'driver1' in locals():
            driver1.close()
            driver1.quit()  # 调用谷歌浏览器 - 结束


if __name__ == '__main__':
    # log = Logger(f'{splitext(sys_argv[0])[0]}.log', level='debug')
    update_exe(dest_dir=osjoin(dirname(executable), 'Scripts'))
