# -*- coding: utf-8 -*-
"""测试 vision_click 功能"""
import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_vision_click():
    print("=" * 80)
    print("测试 vision_click 功能")
    print("=" * 80)

    browser_tool = BrowserUseTool()

    try:
        # Step 1: 导航到携程网站
        print("\n[Step 1] 导航到携程机票页面...")
        result = await browser_tool.execute(
            action="go_to_url",
            url="https://flights.ctrip.com/online/channel/domestic"
        )
        print(f"导航结果: {result.output or result.error}")
        await asyncio.sleep(3)  # 等待页面加载

        # Step 2: 点击出发日期输入框（使用普通点击）
        print("\n[Step 2] 获取页面状态...")
        state_result = await browser_tool.get_current_state()
        if state_result.error:
            print(f"获取状态失败: {state_result.error}")
        else:
            import json
            state_info = json.loads(state_result.output)
            print(f"当前 URL: {state_info.get('url')}")
            interactive_elements = state_info.get('interactive_elements', '')
            element_count = interactive_elements.count('[')
            print(f"交互元素数量: {element_count}")

            # 查找出发日期输入框
            for line in interactive_elements.split('\n'):
                if '出发日期' in line or 'departure' in line.lower():
                    print(f"找到日期相关元素: {line}")

        # Step 3: 点击出发日期输入框
        print("\n[Step 3] 点击出发日期输入框...")
        # 假设索引为 39（需要根据实际情况调整）
        result = await browser_tool.execute(action="click_element", index=39)
        print(f"点击结果: {result.output or result.error}")
        await asyncio.sleep(2)  # 等待日期选择器打开

        # Step 4: 使用 vision_click 选择日期
        print("\n[Step 4] 使用 vision_click 选择 1月30日...")
        result = await browser_tool.execute(
            action="vision_click",
            vision_instruction="帮我选择 1月30日的出发日期"
        )
        print(f"vision_click 结果: {result.output or result.error}")
        await asyncio.sleep(2)

        # Step 5: 验证结果
        print("\n[Step 5] 获取最终页面状态...")
        final_state = await browser_tool.get_current_state()
        if final_state.error:
            print(f"获取状态失败: {final_state.error}")
        else:
            final_info = json.loads(final_state.output)
            print(f"最终 URL: {final_info.get('url')}")

        print("\n测试完成!")

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n清理资源...")
        await browser_tool.cleanup()
        print("资源已清理。")


if __name__ == "__main__":
    asyncio.run(test_vision_click())

