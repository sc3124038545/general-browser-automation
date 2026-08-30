# -*- coding: utf-8 -*-
"""iframe / Shadow DOM 场景实测：跨 iframe 与 open shadow DOM 的点击 + 下拉框选择"""
import asyncio
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        mock_url = Path("debug_html/mock_iframe_shadow.html").resolve().as_uri()
        print("[1] 打开 iframe/Shadow DOM 演示页:", mock_url)
        r = await tool.execute(action="go_to_url", url=mock_url)
        print("    ", r.output or r.error)
        await asyncio.sleep(1.5)

        # ---- iframe 部分 ----
        print("[2] 点击 iframe 内的「iframe登录」按钮...")
        r = await tool.execute(action="click", element_description="iframe登录")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        print("[3] 查看 iframe 内的「语言」下拉框...")
        r = await tool.execute(action="get_dropdown_options", element_description="语言")
        print("    ", r.output or r.error)

        print("[4] 选择 iframe 内的「语言」= 英文...")
        r = await tool.execute(action="select_dropdown_option", element_description="语言", option="英文")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        # ---- shadow DOM 部分 ----
        print("[5] 点击 shadow DOM 内的「确认」按钮...")
        r = await tool.execute(action="click", element_description="确认")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        print("[6] 查看 shadow DOM 内的「主题」下拉框...")
        r = await tool.execute(action="get_dropdown_options", element_description="主题")
        print("    ", r.output or r.error)

        print("[7] 选择 shadow DOM 内的「主题」= 深色...")
        r = await tool.execute(action="select_dropdown_option", element_description="主题", option="深色")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        # ---- 校验 ----
        print("[8] 校验最终状态...")
        context = await tool._ensure_browser_initialized()
        page = await context.get_current_page()

        # iframe 内部状态（用 frame_locator 读取）
        iframe = page.frame_locator("#frame")
        iframe_btn = await iframe.locator("#login-btn").text_content()
        iframe_result = await iframe.locator("#iframe-result").text_content()
        iframe_lang = await iframe.locator("#lang").input_value()

        # shadow DOM 内部状态（open shadow root 可直接读）
        shadow_btn, shadow_result, shadow_theme = await page.evaluate(
            """
            () => {
                const root = document.querySelector('confirm-widget').shadowRoot;
                return [
                    root.querySelector('#confirm-btn').textContent,
                    root.querySelector('#shadow-result').textContent,
                    root.querySelector('#theme').value,
                ];
            }
            """
        )

        print("    iframe 按钮:", iframe_btn, "| iframe 反馈:", iframe_result, "| iframe 语言:", iframe_lang)
        print("    shadow 按钮:", shadow_btn, "| shadow 反馈:", shadow_result, "| shadow 主题:", shadow_theme)

        checks = {
            "iframe 按钮被点击": iframe_btn == "已登录" and iframe_result == "iframe 登录按钮被点击",
            "iframe 下拉框选中英文": iframe_lang == "en",
            "shadow 按钮被点击": shadow_btn == "已确认" and shadow_result == "shadow 确认按钮被点击",
            "shadow 下拉框选中深色": shadow_theme == "dark",
        }
        print("\n    校验结果:")
        all_ok = True
        for k, v in checks.items():
            print(f"      {'[通过]' if v else '[失败]'} {k}")
            all_ok = all_ok and v
        print("\n    总判定:", "全部通过" if all_ok else "存在失败项")

    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        await tool.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
