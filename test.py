import base64

import requests
from openai import OpenAI

base_url = "http://localhost:8000/v1/"

hy_source = "web"
hy_user = "changhozhao"    # 替换为你的用户ID
hy_token = "8tE8bq6InCxff5mUqQZfc9aGHP6NPD80Cr/k258SiLJ9CYW8HiMzU5pREYyvnbvjeMlQugP5sjBBf6Z6HkeKPmw70gyim1uF7yzAGG5SktN5elniDcbIk281Qd3t9wBwmYiBi9omgQ/TZ8dmzLOH7OUJZkQAHF3eSZP9KHAu72idMXpzhtXSQZx/JRmqKbxiTliC8SW41io0pjrb9niVa/gJ4evBkQl469MZV55jssUPevs9JscuwK9hmWjEbaylii47iTa/VI5sJLzwUSlCNGyAJaruRn5chBmSt0V9OQBY7Thw75ot0KoVFf6aFaLheqW0RXRoU+jiA8qK8NSIX7r1LtedDIEwfJI6s4hP2o81Xny5qHoaPFEwV5h4SiT2sn2/5n3JbHWuDszUVlg3PTOoquchMar4jK0vspxWIsrqcSixQjSv9+t/nEkNzevd6h8/s2rf2t6HIg0prAU9MzWLVnl4wLgVn5KLEmYgzTUJasKG9Xa6fdrFDXlksdbJQOXMVVvOcWOqPN/e3OYjAM9GeVPM8bWJmgMXofZz3KKtDwGVMgvdSFZ3FUn986KhpSkY+mHmx6OgL82Hiu4tQA=="   # 替换为你的token

# 新增的Cookie字段（可选，如果有的话可以添加）
_qimei_h38 = "d941369c80e2f1043d10ddcf0300000e819613"  # 可选
ptoken = "EkzFI4pZ3iVJVzuwJ3SqcOphHY73Nqsm4IlYlNSAmIA"  # 可选
_qimei_i_1 = "4fea5dd69c5e51d8c79ead385bd171b6f6eea0f2465a03d6e0dc7e582593206c6163629d3980e4ddd5bfd481"  # 可选
ttwid = "1%7CuG4oFBnsgZm9i72IikAphhzYWGJe87c8gt0RaX3Yb9Y%7C1751263005%7C8a9c16fccc0c3072b312a8d4eaa5092c5d6b4e99d205f85298121621322cc9b0"  # 可选

agent_id = "naQivTmsDa"
chat_id = ""    # 可选，如果不提供会自动创建

# upload，可选
url = base_url + "upload"

file_name = "example.png"
with open(file_name, "rb") as f:
    file_data = base64.b64encode(f.read()).decode("utf-8")
data = {
    "agent_id": agent_id,
    "hy_source": hy_source,
    "hy_user": hy_user,
    # 添加新的Cookie字段（可选）
    "_qimei_h38": _qimei_h38,
    "ptoken": ptoken,
    "_qimei_i_1": _qimei_i_1,
    "ttwid": ttwid,
    "file": {
        "file_name": file_name,
        "file_data": file_data ,
        "file_type": "image",   # image、doc、excel、pdf等，具体看抓包返回的文件类型
    },
}
headers = {"Authorization": f"Bearer {hy_token}"}
response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    print("File uploaded successfully:", response.json())
    multimedia = [response.json()]
else:
    print("File upload failed:", response.status_code, response.text)
    multimedia = []
print(multimedia)

# chat
client = OpenAI(base_url=base_url, api_key=hy_token)

response = client.chat.completions.create(
    model="deepseek-v3",
    messages=[{"role": "user", "content": "这是什么？"}],
    stream=True,
    extra_body={
        "hy_source": hy_source,
        "hy_user": hy_user,
        "agent_id": agent_id,
        "chat_id": chat_id,
        "should_remove_conversation": False,
        # 添加新的Cookie字段（可选）
        "_qimei_h38": _qimei_h38,
        "ptoken": ptoken,
        "_qimei_i_1": _qimei_i_1,
        "ttwid": ttwid,
        "multimedia": multimedia,
    },
)

for chunk in response:
    print(chunk.choices[0].delta.content or "")
