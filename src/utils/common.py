from typing import Dict


def generate_headers(request: dict, token: str) -> Dict[str, str]:
    # 构建Cookie字符串，支持新的Cookie格式
    cookie_parts = [f"hy_source={request['hy_source']}", f"hy_user={request['hy_user']}", f"hy_token={token}"]
    
    # 添加可选的Cookie字段
    optional_cookies = ['_qimei_h38', 'ptoken', '_qimei_i_1', 'ttwid']
    for cookie_name in optional_cookies:
        if cookie_name in request and request[cookie_name]:
            cookie_parts.append(f"{cookie_name}={request[cookie_name]}")
    
    cookie_string = "; ".join(cookie_parts)
    
    return {
        #"Cookie": "hy_source=web;_qimei_h38=d941369c80e2f1043d10ddcf0300000e819613;hy_user=changhozhao;ptoken=EkzFI4pZ3iVJVzuwJ3SqcOphHY73Nqsm4IlYlNSAmIA;hy_token=8tE8bq6InCxff5mUqQZfc9aGHP6NPD80Cr/k258SiLJ9CYW8HiMzU5pREYyvnbvjeMlQugP5sjBBf6Z6HkeKPmw70gyim1uF7yzAGG5SktN5elniDcbIk281Qd3t9wBwmYiBi9omgQ/TZ8dmzLOH7OUJZkQAHF3eSZP9KHAu72idMXpzhtXSQZx/JRmqKbxiCqdogE6LIxYQxI7kTcyH2i/eZ2Jx15uRJSWJtjIdoDjkgDjvn9YbMM1X02xHbXdUF7uvIHykm5+8ViMhD0XcNOq3r2rl2ylh5kr0v3ggDZYj8dDgcN/VPRFbVlRnol2u4Rjl7PkwXh5c+SODtiVkLcBpNsp3PU7awhx6xouIVqsbsj8yEcLETtOLizXZArugjYbJ9G2UgnfPpbI04U1aHfpuEohb1Y1ZMhxMMpJ0L6LH/ms1OG8t236CqInb1ZbHLACoCZXCgpii7cCAjOkw4iGmYp3sCi9Yj5BDj7voQfk1AgUr+hNeMQwrSdDUUNNfS4Z4aPeUBRttX1NlRgQkwslwKE+wKsq1qMtYGzxXTBRngTXbrPRPBs/UApNSaqelCvscmMfLdZK9bOBo5+NXCQ==;_qimei_i_1=4fea5dd69c5e51d8c79ead385bd171b6f6eea0f2465a03d6e0dc7e582593206c6163629d3980e4ddd5bfd481;ttwid=1%7CuG4oFBnsgZm9i72IikAphhzYWGJe87c8gt0RaX3Yb9Y%7C1751263005%7C8a9c16fccc0c3072b312a8d4eaa5092c5d6b4e99d205f85298121621322cc9b0;",
        "Cookie": cookie_string,
        "Origin": "https://yuanbao.tencent.com",
        "Referer": f"https://yuanbao.tencent.com/chat/{request['agent_id']}",
        "X-Agentid": request["agent_id"],
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }
