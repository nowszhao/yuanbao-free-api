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
        "Cookie": cookie_string,
        "Origin": "https://yuanbao.tencent.com",
        "Referer": f"https://yuanbao.tencent.com/chat/{request['agent_id']}",
        "X-Agentid": request["agent_id"],
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }
