from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class WorkflowState(TypedDict):
    number: int
    log: list[str]

def add_five(state: WorkflowState):
    current = state["number"]
    new_val = current + 5
    print(f"[工人A(plus) Typing] {current} -> 计算得到 {new_val}")
    return {
        "number": new_val,
        "log": state["log"] + ["执行了+5运算"]
    }

def multiply_two(state: WorkflowState):
    current = state["number"]
    new_val = current * 2
    print(f"[工人B(multipy) Typing] {current} -> 计算得到 {new_val}")
    return {
        "number": new_val,
        "log": state["log"] + ["执行*2运算"]
    }

builder = StateGraph(WorkflowState)

builder.add_node("step_add", add_five)
builder.add_node("step_multipy", multiply_two)


builder.add_edge(START, "step_add")
builder.add_edge("step_add", "step_multipy")
builder.add_edge("step_multipy", END)

graph = builder.compile()

print(">>> 启动 LangGraph 流水线（初始输入: number = 10）：\n")
initial_input = {"number": 10, "log": []}
final_state = graph.invoke(initial_input)

print(f"最终数值: {final_state['number']}")
print(f"流水线审计日志: {final_state['log']}")