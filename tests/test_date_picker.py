"""
测试日期选择器元素提取和编号的脚本

此脚本专门用于测试日期选择器元素的提取、格式化和编号功能。
它会：
1. 打开携程网站
2. 导航到机票查询页面
3. 点击日期输入框打开日期选择器
4. 提取日期选择器元素
5. 检查是否能正确识别1月30日及编号
"""

import asyncio
import json
from app.tool.browser_use_tool import BrowserUseTool
from app.logger import logger


async def test_date_picker_extraction():
    """测试日期选择器元素提取功能"""
    browser_tool = BrowserUseTool()

    try:
        logger.info("=" * 80)
        logger.info("开始测试日期选择器元素提取和编号")
        logger.info("=" * 80)

        # Step 1: 打开携程网站
        logger.info("\n[Step 1] 打开携程网站...")
        result = await browser_tool.execute(action="go_to_url", url="https://www.ctrip.com")
        logger.info(f"导航结果: {result.output}")

        # 等待页面加载
        await asyncio.sleep(2)

        # Step 2: 获取当前状态，查看元素
        logger.info("\n[Step 2] 获取页面状态...")
        state_result = await browser_tool.get_current_state()
        if state_result.error:
            logger.error(f"获取状态失败: {state_result.error}")
            return

        state_info = json.loads(state_result.output)
        logger.info(f"当前 URL: {state_info['url']}")
        logger.info(f"当前标题: {state_info['title']}")
        logger.info(f"交互元素数量: {state_info.get('interactive_elements', '').count('[')}")

        # Step 3: 点击"机票"按钮
        logger.info("\n[Step 3] 点击'机票'按钮...")
        result = await browser_tool.execute(action="click_element", index=2)
        logger.info(f"点击结果: {result.output}")

        # 等待页面加载
        await asyncio.sleep(3)

        # Step 4: 获取机票页面状态
        logger.info("\n[Step 4] 获取机票页面状态...")
        state_result = await browser_tool.get_current_state()
        if state_result.error:
            logger.error(f"获取状态失败: {state_result.error}")
            return

        state_info = json.loads(state_result.output)
        logger.info(f"当前 URL: {state_info['url']}")
        logger.info(f"交互元素数量: {state_info.get('interactive_elements', '').count('[')}")

        # 查找日期输入框的索引（通常在元素列表中）
        interactive_elements = state_info.get('interactive_elements', '')
        lines = interactive_elements.split('\n')

        # 查找"出发日期"相关的输入框
        date_input_index = None
        for i, line in enumerate(lines):
            if '出发日期' in line or ('input' in line.lower() and i > 35):
                # 尝试提取索引
                import re
                match = re.search(r'\[(\d+)\]', line)
                if match:
                    potential_index = int(match.group(1))
                    # 检查是否是输入框
                    if '<input' in line.lower():
                        date_input_index = potential_index
                        logger.info(f"找到日期输入框，索引: {date_input_index}, 元素: {line[:100]}")
                        break

        if date_input_index is None:
            logger.warning("未找到日期输入框，尝试使用常见的索引...")
            # 根据之前的日志，日期输入框通常在索引 39 或 44 附近
            date_input_index = 39

        # Step 5: 点击日期输入框，打开日期选择器
        logger.info(f"\n[Step 5] 点击日期输入框（索引 {date_input_index}）打开日期选择器...")
        result = await browser_tool.execute(action="click_element", index=date_input_index)
        logger.info(f"点击结果: {result.output}")

        # 等待日期选择器打开（增加等待时间）
        logger.info("等待日期选择器打开...")
        await asyncio.sleep(3)

        # 再次检查元素数量变化
        state_result_temp = await browser_tool.get_current_state()
        if not state_result_temp.error:
            state_info_temp = json.loads(state_result_temp.output)
            element_count_temp = state_info_temp.get('interactive_elements', '').count('[')
            logger.info(f"点击后元素数量: {element_count_temp}")

        # Step 6: 获取日期选择器打开后的状态
        logger.info("\n[Step 6] 获取日期选择器打开后的状态...")
        state_result = await browser_tool.get_current_state()
        if state_result.error:
            logger.error(f"获取状态失败: {state_result.error}")
            return

        state_info = json.loads(state_result.output)
        interactive_elements = state_info.get('interactive_elements', '')
        element_count = interactive_elements.count('[')
        logger.info(f"交互元素总数: {element_count}")

        # Step 7: 查找1月30日的元素
        logger.info("\n[Step 7] 查找1月30日的元素...")
        lines = interactive_elements.split('\n')

        target_date_found = False
        target_date_index = None

        for line in lines:
            # 查找包含"1月30日"或"30日"的元素
            if '1月30日' in line or ('30' in line and '月' in line):
                import re
                match = re.search(r'\[(\d+)\]', line)
                if match:
                    index = int(match.group(1))
                    logger.info(f"✅ 找到目标日期元素: {line.strip()}")
                    logger.info(f"   索引: {index}")
                    target_date_found = True
                    target_date_index = index
                    break

        # 如果没找到"1月30日"，尝试查找"30日"或"30"
        if not target_date_found:
            logger.info("未找到'1月30日'，尝试查找'30日'或'30'...")
            for line in lines:
                if '30日' in line or (line.count('30') > 0 and '<div' in line.lower()):
                    import re
                    match = re.search(r'\[(\d+)\]', line)
                    if match:
                        index = int(match.group(1))
                        logger.info(f"找到包含'30'的元素: {line.strip()}")
                        logger.info(f"   索引: {index}")
                        # 检查是否是日期选择器中的元素（通常索引较大）
                        if index > 100:  # 日期选择器元素通常追加在末尾
                            target_date_found = True
                            target_date_index = index
                            logger.info(f"✅ 可能是目标日期元素（索引较大）: {line.strip()}")
                            break

        # Step 8: 显示所有日期选择器元素的示例
        logger.info("\n[Step 8] 显示日期选择器元素示例...")
        date_elements = []
        for line in lines:
            if '月' in line and '日' in line:
                import re
                match = re.search(r'\[(\d+)\]', line)
                if match:
                    index = int(match.group(1))
                    date_elements.append((index, line.strip()))

        if date_elements:
            logger.info(f"找到 {len(date_elements)} 个包含'月'和'日'的元素:")
            for idx, (index, line) in enumerate(date_elements[:20]):  # 显示前20个
                logger.info(f"  [{index}] {line[:80]}")
        else:
            logger.warning("未找到包含'月'和'日'的元素")
            # 显示所有元素的前50个，用于调试
            logger.info("显示前50个交互元素:")
            for i, line in enumerate(lines[:50]):
                if '[' in line:
                    logger.info(f"  {line[:80]}")

        # Step 9: 测试点击目标日期（如果找到）
        if target_date_found and target_date_index:
            logger.info(f"\n[Step 9] 测试点击目标日期（索引 {target_date_index}）...")
            result = await browser_tool.execute(action="click_element", index=target_date_index)
            if result.error:
                logger.error(f"点击失败: {result.error}")
            else:
                logger.info(f"✅ 点击成功: {result.output}")
                await asyncio.sleep(1)

                # 检查日期是否被选中
                state_result = await browser_tool.get_current_state()
                if not state_result.error:
                    state_info = json.loads(state_result.output)
                    logger.info(f"点击后的 URL: {state_info['url']}")
                    # 检查 URL 中是否包含日期信息
                    if '2026-01-30' in state_info['url'] or 'depdate=2026-01-30' in state_info['url']:
                        logger.info("✅ 日期选择成功！URL 中包含目标日期")
                    else:
                        logger.warning("⚠️ URL 中未包含目标日期，可能需要进一步检查")
        else:
            logger.warning("⚠️ 未找到目标日期元素，无法测试点击功能")

        # 总结
        logger.info("\n" + "=" * 80)
        logger.info("测试总结:")
        logger.info("=" * 80)
        logger.info(f"✅ 日期选择器元素提取: {'成功' if element_count > 100 else '可能失败'}")
        logger.info(f"✅ 找到1月30日元素: {'是' if target_date_found else '否'}")
        if target_date_found:
            logger.info(f"✅ 1月30日的索引: {target_date_index}")
        logger.info(f"✅ 日期元素总数: {element_count}")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)
    finally:
        # 清理资源
        logger.info("\n清理浏览器资源...")
        if browser_tool.browser:
            try:
                await browser_tool.browser.close()
            except:
                pass
        logger.info("测试完成")


if __name__ == "__main__":
    asyncio.run(test_date_picker_extraction())

