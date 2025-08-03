import logging
import os
import re
import time
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

APPID = "wx12b75947931a04ec"
HEADERS = {
    "x-token": "",
    "x-instance-id": "1",
    "x-language": "zh-CN",
    "x-requested-with": "XMLHttpRequest",
    "x-operationsystem": "win",
    "x-channel": "10014",
    "x-id": "",
    "x-product": "bot",
    "x-appversion": "1.8.1",
    "x-source": "web",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0 app_lang/zh-CN product_id/TM_Product_App app_instance_id/2 os_version/10.0.19045 app_short_version/1.8.1 package_type/publish_release app/tencent_yuanbao app_full_version/1.8.1.610 app_theme/system app_version/1.8.1 os_name/windows c_district/0",
    "x-a3": "c2ac2b24fe3303043553b2b0300019319312",
}

TIMEOUT = 30


class YuanbaoLogin:
    def __init__(self):
        self.headers = {"User-Agent": HEADERS["user-agent"]}
        self.uuid: Optional[str] = None
        self.wx_code: Optional[str] = None
        self.qrcode_path = "qrcode.jpg"

    def get_qrcode(self) -> bool:
        """获取微信登录二维码并显示

        Returns:
            bool: 获取二维码是否成功
        """
        try:
            url = "https://open.weixin.qq.com/connect/qrconnect"
            params = {
                "appid": APPID,
                "scope": "snsapi_login",
                "redirect_uri": "https://yuanbao.tencent.com/desktop-redirect.html?&&bindType=wechat_login",
                "state": "",
                "login_type": "jssdk",
                "self_redirect": "true",
                "styletype": "",
                "sizetype": "",
                "bgcolor": "",
                "rst": "",
                "href": "",
            }
            response = requests.get(url, params=params, headers=self.headers, timeout=TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            qrcodes = soup.find_all("img", class_="js_qrcode_img web_qrcode_img")

            if not qrcodes:
                logger.error("未找到二维码元素")
                return False

            qrcode_src = qrcodes[0].get("src")
            self.uuid = qrcode_src.split("/")[-1]

            qrcode_url = f"https://open.weixin.qq.com{qrcode_src}"
            qrcode_response = requests.get(qrcode_url, headers=self.headers, timeout=TIMEOUT)
            qrcode_response.raise_for_status()

            with open(self.qrcode_path, "wb") as f:
                f.write(qrcode_response.content)

            logger.info("二维码已保存到 %s，请扫描登录", self.qrcode_path)
            return True

        except requests.RequestException as e:
            logger.error("获取二维码失败: %s", str(e))
            return False
        except Exception as e:
            logger.error("处理二维码时出错: %s", str(e))
            return False

    def check_scan_status(self) -> bool:
        """检查二维码扫描状态

        Returns:
            bool: 是否成功获取到微信授权码
        """
        if not self.uuid:
            logger.error("UUID未初始化，请先获取二维码")
            return False

        url = "https://lp.open.weixin.qq.com/connect/l/qrconnect"
        params = {"uuid": self.uuid, "_": int(time.time() * 1000)}
        pattern = r"window\.wx_errcode=(\d*);window\.wx_code='(.*)';"

        self.wx_code = ""
        try:
            for attempt in range(20):
                response = requests.get(url, params=params, headers=self.headers, timeout=TIMEOUT)
                response.raise_for_status()

                logger.debug("扫码状态响应: %s", response.text)
                match = re.search(pattern, response.text)
                if match:
                    errcode, self.wx_code = match.groups()
                    if self.wx_code:
                        logger.info("用户已确认登录")
                        return True

                    if errcode == "403":
                        logger.warning("用户拒绝授权")
                        return False
                    elif errcode == "402":
                        logger.warning("二维码已过期")
                        return False
                    elif errcode == "408":
                        logger.info("等待用户扫描 (%d/20)", attempt + 1)
                    elif errcode == "404":
                        logger.info("用户已扫码，等待确认 (%d/20)", attempt + 1)
                        params["last"] = errcode

                time.sleep(1)

            logger.warning("扫码超时")
            return False

        except requests.RequestException as e:
            logger.error("检查扫码状态失败: %s", str(e))
            return False
        except Exception as e:
            logger.error("处理扫码状态时出错: %s", str(e))
            return False

    def login(self) -> Dict[str, str]:
        """使用微信授权码登录元宝平台

        Returns:
            Dict[str, str]: 登录成功后的cookies
        """
        if not self.wx_code:
            logger.error("微信授权码未获取，无法登录")
            return {}

        url = "https://yuanbao.tencent.com/api/joint/login"
        data = {"type": "wx", "jsCode": self.wx_code, "appid": APPID}

        try:
            response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            cookies = response.cookies.get_dict()

            if cookies:
                logger.info("登录成功")
                logger.info("注意：此脚本只能获取基本的登录cookies（hy_user, hy_token等）")
                logger.info("如需获取完整的Cookie字段（_qimei_h38, ptoken, _qimei_i_1, ttwid），")
                logger.info("请在浏览器中手动访问 https://yuanbao.tencent.com 并从开发者工具中复制完整Cookie")
                return cookies
            else:
                logger.warning("登录响应中没有cookies")
                return {}

        except requests.RequestException as e:
            logger.error("登录请求失败: %s", str(e))
            return {}
        except Exception as e:
            logger.error("登录过程中出错: %s", str(e))
            return {}


if __name__ == "__main__":
    yuanbao_login = YuanbaoLogin()

    if yuanbao_login.get_qrcode():
        if yuanbao_login.check_scan_status():
            login_cookies = yuanbao_login.login()
            if login_cookies:
                print("登录成功，获取到的cookies:")
                print(login_cookies)
            else:
                print("登录失败，未获取到cookies")
        else:
            print("微信扫码失败或超时")
    else:
        print("获取二维码失败")

    if os.path.exists(yuanbao_login.qrcode_path):
        try:
            os.remove(yuanbao_login.qrcode_path)
        except Exception as e:
            logger.warning("清理二维码文件失败: %s", str(e))
