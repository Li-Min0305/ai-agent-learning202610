from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class NumberState(TypedDict):
    value: int
    result_msg: str

def process_even(state: NumberState):
    print(f"  🟢 [偶数分流车间] 收到数字 {state['value']}")
    return {"result_msg": f"{state['value']} 是一个偶数，已通过偶数通道处理！"}

def process_odd(state: NumberState):
    print(f"  🟡 [奇数分流车间] 收到数字 {state['value']}")
    return {"result_msg": f"{state['value']} 是一个奇数，已通过奇数通道处理！"}

def check_odd_or_even(state: NumberState) -> str:
    if state["value"] % 2 == 0:
        return "go_even"
    else:
        return "go_odd"

builder = StateGraph(NumberState)

builder.add_node("odd_node", process_odd)
builder.add_node("even_node", process_even)

builder.add_conditional_edges(
    START,
    check_odd_or_even,
    {
        "go_even": "even_node",
        "go_odd": "odd_node"
    }
)

builder.add_edge("even_node", END)
builder.add_edge("odd_node", END)

graph = builder.compile()

print(">>> 测试 1:输入 42:")

res1 = graph.invoke({"value": 42, "result_msg": ""})
print(f"最终输出: {res1['result_msg']}\n")

print(">>> 测试 2:输入 77:")

res2 = graph.invoke({"value": 77, "result_msg": ""})
print(f"最终输出: {res2['result_msg']}\n")