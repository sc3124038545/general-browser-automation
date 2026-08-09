# -*- coding: utf-8 -*-
"""
测试纯 GUI-Plus 视觉模式的机票查询
简化版本 - 直接测试输入和日期选择
"""
import asyncio
import sys

# 确保 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_flight_search():
    """测试携程机票搜索"""
    print("=" * 80)
    print("测试纯 GUI-Plus 视觉模式的机票查询")
    print("=" * 80)

    browser_tool = BrowserUseTool()

    try:
        # Step 1: 打开携程机票页面
        print("\n[Step 1] 打开携程机票页面...")
        result = await browser_tool.execute(
            action="go_to_url",
            url="https://flights.ctrip.com/online/channel/domestic"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(5)  # 多等待让页面加载

        # Step 2: 输入出发地
        print("\n[Step 2] 输入出发地: 上海...")
        result = await browser_tool.execute(
            action="vision_type",
            vision_instruction="在出发地输入框中(显示当前城市名的白色文本区域)输入'上海'"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 3: 选择城市列表中的上海
        print("\n[Step 3] 选择上海...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击城市列表中的'上海'选项"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 4: 输入目的地
        print("\n[Step 4] 输入目的地: 北京...")
        result = await browser_tool.execute(
            action="vision_type",
            vision_instruction="在目的地输入框中(显示目的地城市名的白色文本区域)输入'北京'"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 5: 选择城市列表中的北京
        print("\n[Step 5] 选择北京...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击城市列表中的'北京'选项"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 6: 点击日期输入框
        print("\n[Step 6] 点击日期输入框...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击出发日期区域，打开日历选择器"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 7: 选择日期
        print("\n[Step 7] 选择1月30日...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="在日历中点击30号（1月30日）"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 8: 搜索
        print("\n[Step 8] 点击搜索按钮...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击橙色的搜索按钮"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(5)

        # 获取结果页面
        print("\n[Step 9] 获取页面信息...")
        result = await browser_tool.get_current_state()
        if result.output:
            import json
            state = json.loads(result.output)
            print(f"  URL: {state.get('url', 'N/A')}")
            print(f"  Title: {state.get('title', 'N/A')}")

        print("\n" + "=" * 80)
        print("测试完成!")
        print("=" * 80)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n清理资源...")
        await browser_tool.cleanup()
        print("资源已清理。")


if __name__ == "__main__":
    asyncio.run(test_flight_search())
