import os
import subprocess
from typing import TypedDict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

class AgentState(TypedDict):
    task: str
    code: str
    error: Optional[str]
    output: Optional[str]
    attempts: int

def code_generator(state: AgentState):
    print("🤖 [生成节点] 正在为任务编写初始 Python 代码...")
    prompt = f"""你是一个 Python 程序员。请根据需求编写一段可以直接运行的代码。
【需求】： {state['task']}
【硬性需求】：
1. 必须使用print()输出计算结果。
2. 只输出纯 Python 代码，绝对不要包含任何 Markdown 格式 (如```python 等), 也不要任何解释性文字！
"""
    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = [
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    code = response.choices[0].message.content.strip()
    return {"code": code, "attempts": 0}

def code_executor(state: AgentState):
    current_code = state["code"]
    print(f"\n[执行节点 (第 {state['attempts']+1} 次运行)] 正在本地执行代码...")

    try:
        res = subprocess.run(
            ["python3", "-c", current_code],
            capture_output=True,
            text=True,
            timeout=5
        )
        if res.returncode == 0:
            print("代码运行成功")
            return {"error": None, "output": res.stdout.strip()}
        else:
            print(f"  ❌ 代码运行报错！捕获错误堆栈:\n{res.stderr.strip()}")
            return {"error": res.stderr.strip(), "output": None}

    except Exception as e:
        return {"error": str(e), "output": None}

def code_reflector(state: AgentState):
    new_attempts = state["attempts"] + 1
    print(f"\n [反思修复节点] 大模型正在审视报错堆栈，尝试第 {new_attempts} 次修复...")

    prompt = f"""你的代码运行报错了！仔细分析错误原因并修复它。
【原始需求】：{state["task"]}
【出错代码】：{state["code"]}
【报错信息】：{state["error"]}
【硬性要求】：
1. 找出报错的根本原因，给出修复后的完整正确代码。
2. 只输出修复后的纯 Python 代码，严禁包含任何 Markdown 符号或废话！"""
    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    fixed_code = response.choices[0].message.content.strip()
    return {"code": fixed_code, "attempts": new_attempts}

def check_execution(state: AgentState) -> str:
    if state["error"] is None:
        return "success"

    if state["attempts"] < 3:
        return "retry"

    return "give_up"

builder = StateGraph(AgentState)

builder.add_node("generator", code_generator)
builder.add_node("executor", code_executor)
builder.add_node("reflector", code_reflector)

builder.add_edge(START, "generator")
builder.add_edge("generator", "executor")

builder.add_conditional_edges(
    "executor",
    check_execution,
    {
        "success": END,
        "retry": "reflector",
        "give_up": END
    }
)

builder.add_edge("reflector", "executor")
agent = builder.compile()

my_task = """
计算以下所有学生的平均分并打印出来：
Alice：90
Bob：
Charlie：80
缺少的按0分算
"""

print(f"下达任务{my_task}")
result = agent.invoke({
    "task": my_task,
    "code": "",
    "error": None,
    "output": None,
    "attempts": 0
})

print(f"任务结果：\n")
print(f"状态：{'成功 ✅' if result['error'] is None else '失败 ❌'}\n")
print(f"重试次数{result["attempts"]}\n")
print(f"最终输出：{result["output"]}\n")
print(f"最终输出：{result["output"]}\n")
print(f"code: {result["code"]}\n")