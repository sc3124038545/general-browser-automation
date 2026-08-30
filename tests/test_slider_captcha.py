# -*- coding: utf-8 -*-
"""滑块验证码实测：12306 登录页（易盾滑块，只测拖拽第一步，不碰短信验证）

流程：填假账号 → 点登录 → 切「滑动验证」tab 触发易盾滑块 → 调 solve_slider_captcha。
易盾服务端会反自动化拒绝（error: TJX9v），所以预期结果不是「通过」，而是「正确识别并拖拽到位后服务端拒绝」。
"""
import asyncio
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        print("[1] 打开 12306 登录页...")
        r = await tool.execute(
            action="go_to_url",
            url="https://kyfw.12306.cn/otn/resources/login.html",
        )
        print("    ", r.output or r.error)
        await asyncio.sleep(6)

        # 触发易盾滑块：填假账号 → 点登录 → 切「滑动验证」tab
        context = await tool._ensure_browser_initialized()
        page = await context.get_current_page()
        print("[2] 填假账号 + 点登录 + 切「滑动验证」tab...")
        await page.evaluate(
            """
            () => {
                const set = (sel, v) => {
                    const e = document.querySelector(sel);
                    if (e) { e.value = v; e.dispatchEvent(new Event('input', {bubbles: true})); }
                };
                set('#J-userName', '13000000000');
                set('#J-password', 'abc12345');
            }
            """
        )
        await asyncio.sleep(0.5)
        await page.evaluate("() => { document.querySelector('#J-login').click(); }")
        await asyncio.sleep(5)
        await page.evaluate(
            """
            () => {
                const els = Array.from(document.querySelectorAll('a, li, div, span, button'));
                const el = els.find(e => /滑动验证|滑块验证/.test((e.innerText || '').trim()));
                if (el) el.click();
            }
            """
        )
        await asyncio.sleep(4)

        print("[3] 调用 solve_slider_captcha 求解滑块验证码...")
        r = await tool.execute(action="solve_slider_captcha")
        print("    结果:", r.output or r.error)

    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        await tool.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
