import sys
import subprocess
from typing import Dict, Any

class SafeCodeSandbox:
    """
    安全的轻量级执行沙箱：为大模型代码建立防爆舱
    """
    def __init__(self, timeout_seconds: int = 3):
        self.timeout = timeout_seconds

    def execute(self, code_str: str) -> Dict[str, Any]:
        """
        将不受信任的代码放入独立子进程执行，并启动超时守卫
        """
        cmd = [sys.executable, "-c", code_str]
        try:
            completed = subprocess.run(cmd, capture_output=True, timeout=self.timeout, text=True)

            return {"status": "success", "output": completed.stdout}
        except subprocess.TimeoutExpired:
            return {"status": "error", "output": f"安全拦截: 代码运行超时 (超过 {self.timeout} 秒)！"}           

if __name__ == "__main__":
    sandbox = SafeCodeSandbox(timeout_seconds=2)

    print("--- 实验 1: 正常代码执行 ---")
    res1 = sandbox.execute("print('Hello, 智能体防爆沙箱启动成功!')")
    print("结果:", res1)

    print("\n--- 实验 2: 恶意死循环拦截测试 ---")
    bad_code = "while True: pass"
    res2 = sandbox.execute(bad_code)
    print("结果:", res2)

