# -*- coding: utf-8 -*-
"""电商滚动比价场景实测：mock 无限滚动商品列表页，调 scroll_and_collect 收集全部商品"""
import asyncio
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        mock_url = Path("debug_html/mock_scroll_list.html").resolve().as_uri()
        print("[1] 打开 mock 滚动列表页:", mock_url)
        r = await tool.execute(action="go_to_url", url=mock_url)
        print("    ", r.output or r.error)
        await asyncio.sleep(2)

        print("[2] 调用 scroll_and_collect 滚动加载并抽取商品...")
        r = await tool.execute(
            action="scroll_and_collect",
            goal="商品标题、价格、店铺",
        )
        print("    结果:", r.output or r.error)

    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        await tool.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
