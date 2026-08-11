from app.tool.base import BaseTool


_TERMINATE_DESCRIPTION = """当请求已满足或助手无法继续执行任务时终止交互。
当你完成所有任务后，调用此工具来结束工作。
**重要**: 必须在 `output` 参数中向用户提供最终的答案、报告内容或结果摘要。
如果你创建了文件，请在 output 中说明文件路径和内容概要。
如果你搜索了信息并得出结论，请在 output 中给出完整的回答。"""


class Terminate(BaseTool):
    name: str = "terminate"
    description: str = _TERMINATE_DESCRIPTION
    parameters: dict = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "交互的完成状态。",
                "enum": ["success", "failure"],
            },
            "output": {
                "type": "string",
                "description": "给用户的最终回复。必须包含完整的答案、报告全文、或任务结果摘要。这是用户唯一能看到的内容，务必完整。",
            },
        },
        "required": ["status", "output"],
    }

    async def execute(self, status: str, output: str = "") -> str:
        """完成当前执行"""
        if output:
            return output
        return f"The interaction has been completed with status: {status}"
