import json
from appbuilder.core._client import HTTPClient
from appbuilder.core.component import Message
from appbuilder.core.console.base import ConsoleCompletionResponse


class RAG:
    """
    console RAG组件，利用console端RAG应用进行问答。
    Examples:
        .. code-block:: python
            import appbuilder
            import os

            os.environ["APPBUILDER_TOKEN"] = '...'
            conversation_id = '...'
            app_id = '...' # 线上知识库ID
            conversation_id = '...' # 会话ID，可选参数，不传默认新建会话
            rag_app = appbuilder.console.RAG(app_id)
            query = "中国2023年的人均GDP是多少"
            answer = rag_app.integrated(appbuilder.Message(query), conversation_id)
            print(answer)
    """
    name = "rag"
    integrated_url: str = "/v1/ai_engine/agi_platform/v2/instance/integrated"
    # debug_url: str = "/debug"

    def __init__(self, app_id: str = ""):
        super().__init__()
        self.app_id = app_id
        self._http_client = None

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = HTTPClient()
        return self._http_client

    def integrated(self, query: Message, conversation_id: str = "", stream: bool = False):
        """
        RAG问答
        传参：
            query: 用户输入的文本
            stream: 是否开启流式模式
            conversation_id: 会话ID，不传表示新建对话
        返回：
            rag答案
        """
        response_mode = "streaming" if stream else "blocking"
        payload = json.dumps({"query": query.content, "app_id": self.app_id,
                              "response_mode": response_mode, "conversation_id": conversation_id})
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.integrated_url),
                                                 headers=headers, data=payload)
        response = ConsoleCompletionResponse(response, stream)
        return response.to_message()

    def debug(self, query: Message):
        pass
