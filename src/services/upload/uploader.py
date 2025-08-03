import base64
from typing import Dict

import httpx

from src.schemas.upload import File
from src.utils.upload import generate_headers, get_file_info

UPLOAD_HOST = "hunyuan-prod-1258344703.cos.accelerate.myqcloud.com"

DEFAULT_TIMEOUT = 60


class UploadFileToCosError(Exception):
    pass


async def upload_file_to_cos(
    file: File,
    upload_info: Dict,
    user_agent: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict:
    try:
        url = f"https://{UPLOAD_HOST}{upload_info['location']}"

        file_data_bytes = base64.b64decode(file.file_data)
        content_length = len(file_data_bytes)
        headers = generate_headers(file.file_type, content_length, UPLOAD_HOST, upload_info, user_agent)

        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, data=file_data_bytes, timeout=timeout)
            if response.status_code != 200:
                raise Exception(f"Request failed. Status code: {response.status_code}, Response: {response.text}")

            return get_file_info(
                file.file_type,
                file.file_name,
                content_length,
                upload_info["resourceUrl"],
                response.text,
            )

    except Exception as e:
        raise UploadFileToCosError(e)
