# -*- coding: utf-8 -*-
"""
测试直接坐标点击 - 绕过 GUI-Plus 模型的坐标问题
根据页面截图分析得出的精确坐标
"""
import asyncio
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_direct_click():
    """使用直接坐标测试携程机票搜索"""
    print("=" * 80)
    print("测试直接坐标点击 - 携程机票搜索")
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

        # 获取当前页面 - 使用 browser_tool.context
        context = browser_tool.context
        if not context:
            print("  错误: 浏览器上下文未初始化")
            return
        page = await context.get_current_page()

        # Step 2: 直接点击出发地输入框中心 (根据截图分析: 大约 200, 225)
        print("\n[Step 2] 点击出发地输入框...")
        await page.mouse.click(200, 225)
        await asyncio.sleep(1)

        # 全选并输入
        print("  输入 '上海'...")
        await page.keyboard.press("Control+a")
        await page.keyboard.type("上海")
        await asyncio.sleep(1)

        # 截图查看结果
        screenshot = await page.screenshot()
        with open("debug_html/step2_after_input.png", "wb") as f:
            f.write(screenshot)
        print("  截图已保存: debug_html/step2_after_input.png")

        # Step 3: 按 Enter 或点击选项
        print("\n[Step 3] 按 Enter 选择...")
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)

        # 截图
        screenshot = await page.screenshot()
        with open("debug_html/step3_after_enter.png", "wb") as f:
            f.write(screenshot)
        print("  截图已保存: debug_html/step3_after_enter.png")

        # Step 4: 点击目的地输入框 (大约 440, 225)
        print("\n[Step 4] 点击目的地输入框...")
        await page.mouse.click(440, 225)
        await asyncio.sleep(1)

        # 输入北京
        print("  输入 '北京'...")
        await page.keyboard.press("Control+a")
        await page.keyboard.type("北京")
        await asyncio.sleep(1)

        # Step 5: 按 Enter
        print("\n[Step 5] 按 Enter 选择...")
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)

        # 截图
        screenshot = await page.screenshot()
        with open("debug_html/step5_cities_done.png", "wb") as f:
            f.write(screenshot)
        print("  截图已保存: debug_html/step5_cities_done.png")

        # Step 6: 点击日期输入框 (大约 620, 225)
        print("\n[Step 6] 点击日期输入框...")
        await page.mouse.click(620, 225)
        await asyncio.sleep(2)

        # 截图查看日历
        screenshot = await page.screenshot()
        with open("debug_html/step6_calendar.png", "wb") as f:
            f.write(screenshot)
        print("  截图已保存: debug_html/step6_calendar.png")

        # Step 7: 使用 vision_click 选择 1月30日
        print("\n[Step 7] 使用 vision_click 选择1月30日...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击日历中显示数字30的日期格子"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(2)

        # Step 8: 点击搜索按钮
        print("\n[Step 8] 点击搜索按钮...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="点击页面中间的橙色搜索按钮"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(5)

        # Step 9: 获取结果
        print("\n[Step 9] 获取搜索结果...")
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
    asyncio.run(test_direct_click())
