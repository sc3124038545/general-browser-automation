# -*- coding: utf-8 -*-
"""级联表单场景实测：mock 省/市/区三级联动下拉框，走「查看选项 -> 选择 -> 依赖刷新」全流程"""
import asyncio
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        mock_url = Path("debug_html/mock_cascading_form.html").resolve().as_uri()
        print("[1] 打开 mock 级联表单页:", mock_url)
        r = await tool.execute(action="go_to_url", url=mock_url)
        print("    ", r.output or r.error)
        await asyncio.sleep(1)

        print("[2] 查看「省份」下拉框可选项...")
        r = await tool.execute(action="get_dropdown_options", element_description="省份")
        print("    ", r.output or r.error)

        print("[3] 选择「省份」= 广东省...")
        r = await tool.execute(action="select_dropdown_option", element_description="省份", option="广东省")
        print("    ", r.output or r.error)

        print("[4] 查看「城市」下拉框可选项（应已刷新为广东的城市）...")
        r = await tool.execute(action="get_dropdown_options", element_description="城市")
        print("    ", r.output or r.error)

        print("[5] 选择「城市」= 深圳市...")
        r = await tool.execute(action="select_dropdown_option", element_description="城市", option="深圳市")
        print("    ", r.output or r.error)

        print("[6] 查看「区县」下拉框可选项（应已刷新为深圳的区）...")
        r = await tool.execute(action="get_dropdown_options", element_description="区县")
        print("    ", r.output or r.error)

        print("[7] 选择「区县」= 南山区...")
        r = await tool.execute(action="select_dropdown_option", element_description="区县", option="南山区")
        print("    ", r.output or r.error)

        print("[8] 校验最终选择结果...")
        context = await tool._ensure_browser_initialized()
        page = await context.get_current_page()
        final = await page.evaluate(
            """
            () => {
                const g = id => document.getElementById(id).value;
                return { province: g('province'), city: g('city'), district: g('district') };
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
