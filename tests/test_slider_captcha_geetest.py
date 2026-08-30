# -*- coding: utf-8 -*-
"""滑块验证码实测：极验 Geetest demo（滑动模式，触发雷达按钮后出拼图）"""
import asyncio
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        print("[1] 打开 Geetest demo...")
        r = await tool.execute(action="go_to_url", url="https://www.geetest.com/demo/")
        print("    ", r.output or r.error)
        await asyncio.sleep(4)

        context = await tool._ensure_browser_initialized()
        page = await context.get_current_page()

        print("[2] 点击「滑动模式-float」入口...")
        clicked = await page.evaluate("""
            () => {
                const els = Array.from(document.querySelectorAll('a, button, [class*="btn"]'));
                const el = els.find(e => /滑动模式-float|滑动模式/.test(e.innerText || ''));
                if (el) { el.click(); return (el.innerText||'').trim(); }
                return null;
            }
        """)
        print("    入口:", clicked)
        await asyncio.sleep(3)

        print("[3] 点击雷达按钮（触发拼图）...")
        clicked2 = await page.evaluate("""
            () => {
                const btn = document.querySelector('.geetest_radar_btn');
                if (btn) { btn.click(); return true; }
                return false;
            }
        """)
        print("    雷达按钮:", clicked2)
        # 等 canvas 出现（最多 8 秒）
        for i in range(16):
            has_canvas = await page.evaluate(
                "() => !!document.querySelector('.geetest_canvas_bg')"
            )
            if has_canvas:
                print(f"    拼图 canvas 已出现（等待 {i*0.5:.1f}s）")
                break
            await asyncio.sleep(0.5)

        print("[4] 调用 solve_slider_captcha...")
        r = await tool.execute(action="solve_slider_captcha")
        print("    结果:", r.output or r.error)

    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        await tool.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
