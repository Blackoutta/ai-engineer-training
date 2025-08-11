"""
企业级多智能体协同系统 - 电商客服订单处理案例
使用 AutoGen 框架实现多任务协同，包括：
1. 客服流程拆解
2. 数据查询联动  
3. 跨部门协作调度

适用场景：电商客服系统订单问题处理
"""

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
import json
import time
import os
import asyncio
from typing import Dict
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
api_key = os.getenv('V3_API_KEY')

# 配置模型客户端 - 千问模型
model_client = OpenAIChatCompletionClient(
    model="Qwen/Qwen3-235B-A22B",
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1",  # 硅基流动
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "qwen",
        "structured_output": True
    }
)


# 模拟企业数据库和API接口
class EnterpriseDataService:
    """企业数据服务模拟类"""

    def __init__(self):
        # 模拟订单数据
        self.orders = {
            "ORD001": {
                "order_id": "ORD001",
                "customer_id": "CUST001",
                "status": "已发货",
                "items": [{"product": "iPhone 15", "quantity": 1, "price": 7999}],
                "total": 7999,
                "shipping_address": "北京市朝阳区xxx街道",
                "tracking_number": "SF1234567890",
                "order_date": "2024-01-15",
                "expected_delivery": "2024-01-18"
            },
            "ORD002": {
                "order_id": "ORD002",
                "customer_id": "CUST002",
                "status": "处理中",
                "items": [{"product": "MacBook Pro", "quantity": 1, "price": 15999}],
                "total": 15999,
                "shipping_address": "上海市浦东新区xxx路",
                "tracking_number": None,
                "order_date": "2024-01-16",
                "expected_delivery": None
            }
        }

        # 模拟库存数据
        self.inventory = {
            "iPhone 15": {"stock": 100, "warehouse": "华北仓"},
            "MacBook Pro": {"stock": 0, "warehouse": "华东仓"}
        }

        # 模拟物流数据
        self.logistics = {
            "SF1234567890": {
                "status": "运输中",
                "current_location": "北京分拣中心",
                "estimated_arrival": "2024-01-18 14:00"
            }
        }

    def get_order_info(self, order_id: str) -> Dict:
        """查询订单信息"""
        return self.orders.get(order_id, {})

    def get_inventory_info(self, product: str) -> Dict:
        """查询库存信息"""
        return self.inventory.get(product, {})

    def get_logistics_info(self, tracking_number: str) -> Dict:
        """查询物流信息"""
        return self.logistics.get(tracking_number, {})

    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """更新订单状态"""
        if order_id in self.orders:
            self.orders[order_id]["status"] = new_status
            return True
        return False


# 初始化企业数据服务
data_service = EnterpriseDataService()


async def get_order_info(order_id: str) -> str:
    """获取订单信息的工具函数"""
    try:
        order_info = data_service.get_order_info(order_id)
        if order_info:
            return f"订单信息查询成功：\n{json.dumps(order_info, ensure_ascii=False, indent=2)}"
        else:
            return f"未找到订单号 {order_id} 的信息，请检查订单号是否正确。"
    except Exception as e:
        return f"查询订单信息时出错：{str(e)}"


async def get_inventory_info(product: str) -> str:
    """获取库存信息的工具函数"""
    try:
        inventory_info = data_service.get_inventory_info(product)
        if inventory_info:
            return f"库存信息查询成功：\n{json.dumps(inventory_info, ensure_ascii=False, indent=2)}"
        else:
            return f"未找到产品 {product} 的库存信息。"
    except Exception as e:
        return f"查询库存信息时出错：{str(e)}"


async def get_logistics_info(tracking_number: str) -> str:
    """获取物流信息的工具函数"""
    try:
        logistics_info = data_service.get_logistics_info(tracking_number)
        if logistics_info:
            return f"物流信息查询成功：\n{json.dumps(logistics_info, ensure_ascii=False, indent=2)}"
        else:
            return f"未找到运单号 {tracking_number} 的物流信息。"
    except Exception as e:
        return f"查询物流信息时出错：{str(e)}"


# 定义智能体角色

# 1. 客服接待智能体
customer_service_agent = AssistantAgent(
    # 用中文好像有问题
    name="customer_service_agent",
    model_client=model_client,
    system_message="""你是一名专业的电商客服接待员。你的职责是：
1. 友好接待客户，了解客户问题
2. 对问题进行初步分类（订单查询、退换货、物流问题、产品咨询等）
3. 收集必要的订单信息（订单号、客户信息等）
4. 将问题转交给相应的专业团队处理

请用简洁明了的语言与客户沟通。当客户提到具体订单号时，请直接转交给订单查询专员处理。
如果问题涉及多个方面，请协调相关专员共同解决。

回复格式：简洁专业，直接回答客户问题。""",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# 2. 订单查询智能体
order_query_agent = AssistantAgent(
    name="order_query_agent",
    model_client=model_client,
    tools=[get_order_info],
    system_message="""你是订单查询专员，负责处理所有订单相关的查询。你的职责包括：
1. 根据订单号查询订单详细信息
2. 解释订单状态和处理进度
3. 提供预计发货和到货时间
4. 识别需要其他部门协助的问题

当客户提供订单号时，请立即使用 get_order_info 函数查询订单信息。
根据查询结果，如果发现需要物流或库存部门协助，请主动通知相关专员。

回复格式：提供详细的订单信息，包括状态、商品、金额等关键信息。。""",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# 3. 物流跟踪智能体
logistics_agent = AssistantAgent(
    name="logistics_agent",
    model_client=model_client,
    tools=[get_logistics_info],
    system_message="""你是物流跟踪专员，专门处理配送和物流相关问题。你的职责包括：
1. 查询包裹物流状态和位置
2. 提供准确的配送时间预估
3. 处理配送异常和延误问题
4. 协调配送地址修改

当需要查询物流信息时，请使用 get_logistics_info 函数。
请提供实时、准确的物流信息，并主动提醒客户注意事项。

回复格式：提供详细的物流状态，包括当前位置、预计到达时间等。""",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# 4. 库存管理智能体
inventory_agent = AssistantAgent(
    name="inventory_agent",
    model_client=model_client,
    tools=[get_inventory_info],
    system_message="""你是库存管理专员，负责处理库存相关问题。你的职责包括：
1. 查询产品库存状态
2. 预估补货时间
3. 协调缺货订单处理
4. 提供替代产品建议

当需要查询库存信息时，请使用 get_inventory_info 函数。
请提供准确的库存信息，并为缺货情况提供合理的解决方案。

回复格式：提供库存状态，如果缺货请说明预计补货时间。""",
    reflect_on_tool_use=True,
    model_client_stream=True,
)


# 5. 用户智能体 - 模拟用户行为
# 自动回复"已解决"或"谢谢您的帮助"
def auto_reply_input() -> str:
    return "谢谢您的帮助，问题已解决！"


user_agent = UserProxyAgent(
    name="user_agent",
    description="模拟用户行为，用于自然结束对话",
    input_func=auto_reply_input
)


# 轮询聊天
def create_group_chat():
    """创建自动选择式群组聊天"""
    # 添加终止条件
    from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

    # 创建一个文本提及终止条件，当消息中包含特定文本时终止
    text_termination = (
            TextMentionTermination("谢谢您的帮助") |
            TextMentionTermination("问题已解决") |
            TextMentionTermination("已解决")
    )

    # 创建一个最大消息数终止条件，作为备用终止条件，防止无限轮询
    max_msg_termination = MaxMessageTermination(max_messages=12)

    # 组合终止条件，满足任一条件即终止
    termination_condition = text_termination | max_msg_termination

    return SelectorGroupChat(
        [customer_service_agent, order_query_agent, logistics_agent, inventory_agent, user_agent],
        model_client=model_client,
        termination_condition=termination_condition
    )


# 企业级客服场景测试
async def run_scenario_with_autogen(scenario_name: str, customer_message: str):
    """使用 AutoGen 运行客服场景"""
    print(f"\n{'=' * 60}")
    print(f"🎯 {scenario_name}")
    print(f"{'=' * 60}")
    print(f"客户问题：{customer_message}")
    print(f"\n🤖 AutoGen 多智能体协作处理：")
    print("-" * 50)
    # 创建群组聊天
    group_chat = create_group_chat()
    # 开始对话并流式输出到控制台
    await Console(group_chat.run_stream(task=customer_message))
    print(f"\n✅ 场景处理完成")


async def main():
    """主函数 - 演示企业级多智能体协同"""
    print("🏢 企业级多智能体协同系统 - 电商客服订单处理演示")
    print("基于 AutoGen 框架实现")
    print("=" * 80)
    print("系统特性：")
    print("✅ 1. 客服流程自动拆解")
    print("✅ 2. 多数据源联动查询")
    print("✅ 3. 跨部门智能协作")
    print("✅ 4. 问题升级和路由")
    print("✅ 5. AutoGen 框架支持")

    try:
        # 测试场景
        scenarios = [
            ("场景1：订单状态查询", "你好，我想查询一下我的订单ORD001的状态，什么时候能到货？"),
            ("场景2：缺货问题处理", "我下单的MacBook Pro订单ORD002一直显示处理中，什么时候能发货？"),
            ("场景3：物流延误处理", "我的订单ORD001已经超过预计到货时间了，但还没收到货，这是怎么回事？")
        ]

        # 运行所有场景
        for scenario_name, scenario_message in scenarios:
            await run_scenario_with_autogen(scenario_name, scenario_message)
            time.sleep(2)  # 避免API调用过于频繁

        print(f"\n{'=' * 80}")
        print("🎉 企业级多智能体协同演示完成！")
        print("💡 该系统基于 AutoGen 框架，展示了电商客服系统中的多任务协同和跨部门协作")

    finally:
        # 关闭模型客户端连接
        await model_client.close()


if __name__ == "__main__":
    # 使用 asyncio.run() 来运行异步主函数
    asyncio.run(main())
