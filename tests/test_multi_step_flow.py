# -*- coding: utf-8 -*-
"""多步骤长流程场景实测：mock 电商下单流程（选商品 -> 填收货信息(含省市区级联) -> 选支付 -> 提交 -> 成功页）
全程串联 click/type/get_dropdown_options/select_dropdown_option 等既有 action，验证跨步骤、跨页面状态延续。
"""
import asyncio
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from app.tool.browser_use_tool import BrowserUseTool


async def main():
    tool = BrowserUseTool()
    try:
        mock_url = Path("debug_html/mock_checkout_flow.html").resolve().as_uri()
        print("[1] 打开下单流程页:", mock_url)
        r = await tool.execute(action="go_to_url", url=mock_url)
        print("    ", r.output or r.error)
        await asyncio.sleep(1)

        print("[2] 第1步：选商品「智能手表」")
        r = await tool.execute(action="click", element_description="智能手表")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)
        r = await tool.execute(action="click", element_description="下一步")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        print("[3] 第2步：填收货人姓名 + 手机号码")
        r = await tool.execute(action="type", element_description="收货人姓名", text="张三")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)
        r = await tool.execute(action="type", element_description="手机号码", text="13800138000")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        print("[4] 第2步：省/市/区级联选择")
        r = await tool.execute(action="get_dropdown_options", element_description="省份")
        print("    ", r.output or r.error)
        r = await tool.execute(action="select_dropdown_option", element_description="省份", option="广东省")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)
        r = await tool.execute(action="select_dropdown_option", element_description="城市", option="深圳市")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)
        r = await tool.execute(action="select_dropdown_option", element_description="区县", option="南山区")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)
        r = await tool.execute(action="click", element_description="下一步")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        print("[5] 第3步：选支付方式「微信支付」")
        r = await tool.execute(action="click", element_description="微信支付")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)
        r = await tool.execute(action="click", element_description="下一步")
        print("    ", r.output or r.error)
        await asyncio.sleep(0.5)

        print("[6] 第4步：提交订单")
        r = await tool.execute(action="click", element_description="提交订单")
        print("    ", r.output or r.error)
        await asyncio.sleep(2)

        print("[7] 校验成功页结果...")
        context = await tool._ensure_browser_initialized()
        page = await context.get_current_page()
        detail = await page.evaluate("() => document.getElementById('detail')?.innerText || ''")
        url = page.url
        print("    当前 URL:", url)
        print("    成功页内容:")
        for line in detail.split("\n"):
            print("      ", line)

        # 逐项断言
        checks = {
            "跳转到成功页": "mock_order_success.html" in url,
            "订单号": "订单号" in detail and "ORDER" in detail,
            "商品=智能手表": "智能手表" in detail,
            "收货人=张三": "张三" in detail,
            "手机=13800138000": "13800138000" in detail,
            "地址=广东省深圳市南山区": "广东省深圳市南山区" in detail,
            "支付方式=微信支付": "微信支付" in detail,
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
