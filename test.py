import base64

import requests
from openai import OpenAI

base_url = "http://localhost:8000/v1/"

hy_source = "web"
hy_user = ""    # 替换为你的用户ID
hy_token = ""   # 替换为你的token

# 新增的Cookie字段（可选，如果有的话可以添加）
_qimei_h38 = ""  # 可选
ptoken = ""  # 可选
_qimei_i_1 = ""  # 可选
ttwid = ""  # 可选
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
