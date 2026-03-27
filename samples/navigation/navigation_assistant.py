"""
智能导航助手 - 基于 oMLX + Qwen2.5-0.5B

功能：
- 理解用户自然语言输入
- 识别意图并映射到应用功能
- 支持 Function Calling 提高准确性
- 缓存优化减少重复请求
"""

from openai import OpenAI
from functools import lru_cache
from typing import Dict, List, Optional
import json
import time


class NavigationAssistant:
    """基础导航助手（简单版）"""

    def __init__(
        self,
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "2348",
        model: str = "Qwen2.5-0.5B-Instruct"
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=5.0
        )
        self.model = model

        # 定义应用功能映射
        self.functions = {
            "查看订单": "/orders",
            "个人设置": "/settings",
            "帮助中心": "/help",
            "联系客服": "/contact",
            "商品搜索": "/search",
            "购物车": "/cart",
            "退出登录": "/logout",
            "账户安全": "/security",
        }

        # 构建系统提示
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        functions_list = '\n'.join(f'- {name}' for name in self.functions.keys())

        return f"""你是一个应用导航助手。
用户会描述他们想做什么，你需要理解意图并返回对应的功能名称。

可用功能：
{functions_list}

规则：
1. 只返回功能名称，不要额外解释
2. 如果意图不清楚，返回"需要更多信息"
3. 如果没有匹配功能，返回"未找到相关功能"
"""

    def navigate(self, user_query: str) -> Dict:
        """导航到功能

        Args:
            user_query: 用户输入

        Returns:
            {
                "success": bool,
                "function": str,      # 功能名称
                "route": str,         # 路由路径
                "confidence": float   # 置信度（可选）
            }
        """
        try:
            start_time = time.time()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=50,
                temperature=0.1
            )

            function_name = response.choices[0].message.content.strip()
            elapsed = time.time() - start_time

            # 映射到路径
            if function_name in self.functions:
                return {
                    "success": True,
                    "function": function_name,
                    "route": self.functions[function_name],
                    "elapsed_ms": int(elapsed * 1000)
                }
            else:
                return {
                    "success": False,
                    "message": function_name,
                    "elapsed_ms": int(elapsed * 1000)
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"服务错误: {str(e)}"
            }


class SmartNavigator(NavigationAssistant):
    """智能导航助手（Function Calling 版）"""

    def navigate(self, user_query: str) -> Dict:
        """使用 Function Calling 进行导航"""
        try:
            start_time = time.time()

            # 定义工具
            tools = [{
                "type": "function",
                "function": {
                    "name": "navigate_to",
                    "description": "导航到应用的特定功能",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "function": {
                                "type": "string",
                                "enum": list(self.functions.keys()),
                                "description": "要导航到的功能"
                            },
                            "confidence": {
                                "type": "number",
                                "description": "意图识别的置信度（0-1）",
                                "minimum": 0,
                                "maximum": 1
                            }
                        },
                        "required": ["function", "confidence"]
                    }
                }
            }]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": f"用户说：{user_query}"
                }],
                tools=tools,
                tool_choice="auto"
            )

            elapsed = time.time() - start_time

            # 解析工具调用
            if response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                args = json.loads(tool_call.function.arguments)

                function_name = args["function"]
                confidence = args.get("confidence", 0.5)

                return {
                    "success": True,
                    "function": function_name,
                    "route": self.functions[function_name],
                    "confidence": confidence,
                    "elapsed_ms": int(elapsed * 1000)
                }
            else:
                return {
                    "success": False,
                    "message": "无法理解意图",
                    "elapsed_ms": int(elapsed * 1000)
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"服务错误: {str(e)}"
            }


class CachedNavigator(SmartNavigator):
    """带缓存的导航助手"""

    def __init__(self, *args, cache_size: int = 100, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_size = cache_size

        # 使用 lru_cache 包装 navigate 方法
        self._cached_navigate = lru_cache(maxsize=cache_size)(
            self._navigate_internal
        )

    def _navigate_internal(self, user_query: str) -> str:
        """内部导航方法（用于缓存）"""
        result = super().navigate(user_query)
        return json.dumps(result)

    def navigate(self, user_query: str) -> Dict:
        """带缓存的导航"""
        result_json = self._cached_navigate(user_query)
        return json.loads(result_json)

    def clear_cache(self):
        """清除缓存"""
        self._cached_navigate.cache_clear()

    def cache_info(self):
        """获取缓存信息"""
        return self._cached_navigate.cache_info()


# ============ 使用示例 ============

if __name__ == "__main__":
    # 示例1：基础导航助手
    print("=" * 60)
    print("示例1：基础导航助手")
    print("=" * 60)

    assistant = NavigationAssistant()

    test_queries = [
        "我想看看我买的东西",
        "修改个人信息",
        "找客服",
        "退出",
        "不知道干什么"
    ]

    for query in test_queries:
        result = assistant.navigate(query)
        print(f"\n用户输入: {query}")
        print(f"识别结果: {result}")

    # 示例2：智能导航助手（Function Calling）
    print("\n" + "=" * 60)
    print("示例2：智能导航助手（Function Calling）")
    print("=" * 60)

    smart_assistant = SmartNavigator()

    for query in test_queries[:3]:
        result = smart_assistant.navigate(query)
        print(f"\n用户输入: {query}")
        print(f"识别结果: {result}")
        if result.get("success"):
            print(f"  → 功能: {result['function']}")
            print(f"  → 路由: {result['route']}")
            print(f"  → 置信度: {result.get('confidence', 'N/A')}")
            print(f"  → 耗时: {result['elapsed_ms']}ms")

    # 示例3：带缓存的导航助手
    print("\n" + "=" * 60)
    print("示例3：带缓存的导航助手")
    print("=" * 60)

    cached_assistant = CachedNavigator(cache_size=50)

    # 第一次请求（无缓存）
    result1 = cached_assistant.navigate("我想看订单")
    print(f"\n第一次请求: {result1['elapsed_ms']}ms")

    # 第二次请求（命中缓存）
    result2 = cached_assistant.navigate("我想看订单")
    print(f"第二次请求: {result2['elapsed_ms']}ms (缓存命中)")

    # 缓存统计
    print(f"\n缓存信息: {cached_assistant.cache_info()}")
