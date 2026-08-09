# -*- coding: utf-8 -*-
"""
测试智能操作模式（smart_click + smart_input）
通过 HTML 分析自动定位元素，比视觉坐标更精确
"""
import asyncio
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_smart_mode():
    """测试智能模式的携程机票搜索"""
    print("=" * 80)
    print("测试智能操作模式 - 携程机票搜索")
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
        await asyncio.sleep(5)

        # 使用直接坐标点击的方式（已验证有效）
        context = browser_tool.context
        if not context:
            print("  错误: 浏览器上下文未初始化")
            return
        page = await context.get_current_page()

        # Step 2: 直接点击出发地区域 (坐标来自之前成功的测试)
        print("\n[Step 2] 直接点击出发地区域...")
        await page.mouse.click(200, 225)
        await asyncio.sleep(1)

        # Step 3: 智能输入出发地
        print("\n[Step 3] 智能输入出发地: 上海...")
        result = await browser_tool.execute(
            action="smart_input",
            element_description="城市输入框",
            text="上海"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(1)

        # Step 4: 按 Enter 确认
        print("\n[Step 4] 按 Enter 确认...")
        result = await browser_tool.execute(
            action="send_keys",
            keys="Enter"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(1)

        # Step 5: 直接点击目的地区域
        print("\n[Step 5] 直接点击目的地区域...")
        await page.mouse.click(440, 225)
        await asyncio.sleep(1)

        # Step 6: 智能输入目的地
        print("\n[Step 6] 智能输入目的地: 北京...")
        result = await browser_tool.execute(
            action="smart_input",
            element_description="城市输入框",
            text="北京"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(1)

        # Step 7: 按 Enter 确认
        print("\n[Step 7] 按 Enter 确认...")
        result = await browser_tool.execute(
            action="send_keys",
            keys="Enter"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(1)

        # Step 8: 点击日期区域
        print("\n[Step 8] 点击日期区域...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击出发日期区域（显示日期的输入框）"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 9: 视觉选择1月30日
        print("\n[Step 9] 视觉选择1月30日...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="在日历中点击数字30"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 10: 点击搜索按钮（使用视觉模式，因为按钮有特定样式）
        print("\n[Step 10] 点击搜索按钮...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击橙色的搜索按钮"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(5)

        # Step 11: 获取结果
        print("\n[Step 11] 获取搜索结果...")
        state = await browser_tool.get_current_state()
        if state.output:
            import json
            state_info = json.loads(state.output)
            print(f"  URL: {state_info.get('url', 'N/A')}")
            print(f"  Title: {state_info.get('title', 'N/A')}")

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
    asyncio.run(test_smart_mode())

