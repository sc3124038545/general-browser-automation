# -*- coding: utf-8 -*-
"""级联表单真实页验证：12306 注册页的原生 <select>（证件类型 / 旅客类型）走 get/select 全流程"""
import asyncio
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        print("[1] 打开 12306 注册页...")
        r = await tool.execute(action="go_to_url", url="https://kyfw.12306.cn/otn/regist/init")
        print("    ", r.output or r.error)
        await asyncio.sleep(4)

        print("[2] 查看「证件类型」下拉框可选项...")
        r = await tool.execute(action="get_dropdown_options", element_description="证件类型")
        print("    ", r.output or r.error)

        print("[3] 选择「证件类型」= 港澳居民居住证...")
        r = await tool.execute(action="select_dropdown_option", element_description="证件类型", option="港澳居民居住证")
        print("    ", r.output or r.error)

        print("[4] 查看「旅客类型」下拉框可选项...")
        r = await tool.execute(action="get_dropdown_options", element_description="旅客类型")
        print("    ", r.output or r.error)

        print("[5] 选择「旅客类型」= 学生...")
        r = await tool.execute(action="select_dropdown_option", element_description="旅客类型", option="学生")
        print("    ", r.output or r.error)

        print("[6] 校验最终选择结果...")
        context = await tool._ensure_browser_initialized()
        page = await context.get_current_page()
        final = await page.evaluate(
            """
            () => {
                const sel = id => {
                    const el = document.getElementById(id);
                    return el ? el.options[el.selectedIndex].text.trim() : null;
                };
                return { cardType: sel('cardType'), passengerType: sel('passengerType') };
            }
            """
        )
        print("    最终选择:", final)

    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        await tool.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
