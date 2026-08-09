"""
测试简化的 click + type 接口
"""
import asyncio
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_simple_actions():
    """测试简化的 click + type 接口 - 携程机票搜索"""
    print("=" * 80)
    print("测试简化的 click + type 接口")
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
        await asyncio.sleep(3)

        # 确保使用单程模式
        print("\n[Step 1.5] 确保单程模式...")
        result = await browser_tool.execute(
            action="click",
            element_description="单程"
        )
        print(f"  结果: {result.output if result.output else result.error}")
        await asyncio.sleep(1)

        # Step 2: 点击出发城市区域（点击城市名称部分，如"新加坡"）
        print("\n[Step 2] 点击出发城市（当前城市名）...")
        context = await browser_tool._ensure_browser_initialized()
        page = await context.get_current_page()

        # 使用坐标点击出发地区域（根据截图分析）
        await page.mouse.click(150, 225)
        await asyncio.sleep(1.5)
        print("  结果: 直接点击出发地区域 (150, 225)")

        # Step 3: 输入上海
        print("\n[Step 3] 输入: 上海...")
        await page.keyboard.type("上海")
        await asyncio.sleep(1)
        print("  结果: 键盘输入 '上海'")

        # Step 4: 按 Enter 确认
        print("\n[Step 4] 按 Enter 确认...")
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)
        print("  结果: 按 Enter")

        # Step 5: 点击目的地区域
        print("\n[Step 5] 点击目的地区域...")
        await page.mouse.click(400, 225)
        await asyncio.sleep(1.5)
        print("  结果: 直接点击目的地区域 (400, 225)")

        # Step 6: 输入北京
        print("\n[Step 6] 输入: 北京...")
        await page.keyboard.type("北京")
        await asyncio.sleep(1)
        print("  结果: 键盘输入 '北京'")

        # Step 7: 按 Enter 确认
        print("\n[Step 7] 按 Enter 确认...")
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)
        print("  结果: 按 Enter")

        # Step 8: 点击日期区域
        print("\n[Step 8] 点击日期区域...")
        await page.mouse.click(650, 225)  # 日期区域
        await asyncio.sleep(2)
        print("  结果: 直接点击日期区域 (650, 225)")

        # Step 9: 点击日期 30（在日历底部行）
        print("\n[Step 9] 点击日期 30...")
        # 根据截图分析，30号在日历底部行，大约位置 (530, 560)
        # 使用 Playwright locator 直接找 30
        try:
            locator = page.locator("text=30").last  # 取最后一个，即日历中的 30
            if await locator.is_visible():
                await locator.click()
                print("  结果: Playwright 定位到 '30' 并点击")
            else:
                # 回退到直接坐标
                await page.mouse.click(530, 558)
                print("  结果: 直接点击坐标 (530, 558)")
        except Exception as e:
            await page.mouse.click(530, 558)
            print(f"  结果: 直接点击坐标 (530, 558), 异常: {e}")
        await asyncio.sleep(2)

        # Step 10: 点击搜索按钮
        print("\n[Step 10] 点击搜索按钮...")
        # 搜索按钮的橙色按钮位置
        await page.mouse.click(610, 290)
        await asyncio.sleep(5)
        print("  结果: 直接点击搜索按钮 (610, 290)")

        # Step 11: 获取页面状态
        print("\n[Step 11] 获取页面状态...")
        state_result = await browser_tool.get_current_state()
        if state_result.output:
            import json
            state_info = json.loads(state_result.output)
            print(f"  URL: {state_info.get('url', 'N/A')}")
            print(f"  Title: {state_info.get('title', 'N/A')}")

        print("\n" + "=" * 80)
        print("测试完成!")
        print("=" * 80)

    except Exception as e:
        logger.error(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n清理资源...")
        await browser_tool.cleanup()
        print("资源已清理。")


if __name__ == "__main__":
    asyncio.run(test_simple_actions())

