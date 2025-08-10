from typing import AsyncGenerator, Dict

import httpx

from src.schemas.chat import YuanBaoChatCompletionRequest
from src.services.chat.conversation import remove_conversation
from src.utils.chat import process_response_stream

CHAT_URL = "https://yuanbao.tencent.com/api/chat/{}"

DEFAULT_TIMEOUT = 60


class ChatCompletionError(Exception):
    pass


async def create_completion_stream(
    chat_request: YuanBaoChatCompletionRequest,
    headers: Dict[str, str],
    should_remove_conversation: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> AsyncGenerator[str, None]:
    multimedia = [m.model_dump() for m in chat_request.multimedia]
    body = {
        "model": "gpt_175B_0404",
        "prompt": chat_request.prompt,
        "plugin": "Adaptive",
        "displayPrompt": chat_request.prompt,
        "displayPromptType": 1,
        "options": {"imageIntention": {"needIntentionModel": True, "backendUpdateFlag": 2, "intentionStatus": True}},
        "multimedia": multimedia,
        "agentId": chat_request.agent_id,
        "supportHint": 1,
        "version": "v2",
        isTemporary: true,
        "chatModelId": chat_request.chat_model_id,
    }
    if chat_request.support_functions:
        body["supportFunctions"] = chat_request.support_functions

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                CHAT_URL.format(chat_request.chat_id),
                json=body,
                headers=headers,
                timeout=timeout,
            ) as response:
                async for chunk in process_response_stream(response, chat_request.chat_id):
                    yield chunk

    except Exception as e:
        raise ChatCompletionError(e)

    finally:
        if should_remove_conversation:
            await remove_conversation(chat_request.chat_id, headers)
