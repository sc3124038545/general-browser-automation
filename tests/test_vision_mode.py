# -*- coding: utf-8 -*-
"""测试纯视觉模式的机票查询"""
import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_vision_flight_search():
    print("=" * 80)
    print("测试纯视觉模式的机票查询")
    print("=" * 80)

    browser_tool = BrowserUseTool()

    try:
        # Step 1: 导航到携程机票页面
        print("\n[Step 1] 导航到携程机票页面...")
        result = await browser_tool.execute(
            action="go_to_url",
            url="https://flights.ctrip.com/online/channel/domestic"
        )
        print(f"结果: {result.output or result.error}")
        await asyncio.sleep(3)

        # Step 2: 使用视觉输入出发地
        print("\n[Step 2] 视觉输入出发地: 上海...")
        result = await browser_tool.execute(
            action="vision_type",
            vision_instruction="在出发城市输入框中输入'上海'，如果已有内容先清空"
        )
        print(f"结果: {result.output or result.error}")
        await asyncio.sleep(2)

        # Step 3: 使用视觉输入目的地
        print("\n[Step 3] 视觉输入目的地: 北京...")
        result = await browser_tool.execute(
            action="vision_type",
            vision_instruction="在到达城市或目的地输入框中输入'北京'"
        )
        print(f"结果: {result.output or result.error}")
        await asyncio.sleep(2)

        # Step 4: 使用视觉点击日期输入框
        print("\n[Step 4] 视觉点击日期输入框...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击出发日期输入框，打开日期选择器"
        )
        print(f"结果: {result.output or result.error}")
        await asyncio.sleep(2)

        # Step 5: 使用视觉选择日期
        print("\n[Step 5] 视觉选择日期: 1月30日...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="在日历中点击1月30日"
        )
        print(f"结果: {result.output or result.error}")
        await asyncio.sleep(2)

        # Step 6: 使用视觉点击搜索按钮
        print("\n[Step 6] 视觉点击搜索按钮...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击搜索按钮（蓝色或橙色的搜索/查询按钮）"
        )
        print(f"结果: {result.output or result.error}")
        await asyncio.sleep(5)

        # Step 7: 获取结果
        print("\n[Step 7] 提取搜索结果...")
        result = await browser_tool.execute(
            action="extract_content",
            goal="提取页面上显示的航班信息，包括航班号、时间、价格等"
        )
        print(f"结果: {result.output or result.error}")

        print("\n" + "=" * 80)
        print("测试完成!")
        print("=" * 80)

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n清理资源...")
        await browser_tool.cleanup()
        print("资源已清理。")


if __name__ == "__main__":
    asyncio.run(test_vision_flight_search())

