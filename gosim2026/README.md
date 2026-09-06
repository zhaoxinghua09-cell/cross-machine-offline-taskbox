# GOSIM 2026 生产轨迹（ARC-Bench 风格）

本目录包含 `cross-machine-offline-taskbox` 参加 **GOSIM 深圳 2026「智能体软件工厂」黑客松** 的生产轨迹与可复现脚本。

## 主张

**Trustworthy Agent Factory = 注册 · 证据 · 门禁（Registry · Evidence · Gates）**
——可信（人在回路）/ 可复现（一键脚本）/ 可观测（逐事件证据链）。

## 文件

- `trace.jsonl`：生产轨迹，14 个事件 / 2 个任务。每行一个 JSON 事件：`{ts, step, event, actor, detail}`。
  事件类型（7 类）：`human_task_submit` / `agent_plan` / `prompt_build` / `tool_call_ollama` / `model_output` / `result_store` / `human_review`。
  还原流程：**人工派活 → agent 规划 → 构造 prompt → 调本机 Ollama → 模型返回 → 写回任务箱 → 人工复核**。
- `manifest.json`：轨迹元数据（schema / 事件类型 / 角色说明 / 任务数 / 去敏声明 / 生成时间）。
- `run_trace.py`：可复现生成器。在装有 Ollama 的机器直接 `python run_trace.py` 即可实时重跑出等价轨迹。

## 复现

```bash
# 1) 本机需有 Ollama 且已拉取模型
ollama pull qwen3.5:4b-8k          # 或任意本地生成模型
# 2) 跑轨迹生成器（自动调用本地 Ollama，断网可用）
python run_trace.py                # 产出 trace.jsonl + manifest.json
```

## 去敏

轨迹全程未出现雇主名、内部绝对路径、真名、内部代号；任务均为通用示例；模型为本机已装的小模型，敏感数据不出本机。
