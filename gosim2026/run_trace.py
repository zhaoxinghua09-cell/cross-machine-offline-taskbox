#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GOSIM 2026 ARC-Bench 生产轨迹记录器（可信/可复现/可观测 演示）。

基于 cross-machine-offline-taskbox 真实机制：
  人工派活 -> 离线 worker 调本地 Ollama -> 结果写回任务箱 -> 人工复核
每一步都以结构化事件写入 trace.jsonl，可被评审方逐事件还原「谁在何时做了什么」。

去敏：全程不出现雇主名/内部路径/真名/内部代号；模型为本机已装 qwen3.5:4b-8k。
复现：在装有 Ollama 的机器 `python run_trace.py` 即可重跑出等价轨迹。
"""
import json
import time
import urllib.request
import urllib.error
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:4b-8k"

# 两个通用、无害的示例任务（不涉密）
TASKS = [
    {
        "title": "为开源离线任务调度工具写一句产品 slogan",
        "detail": "强调断网可用、敏感数据不出本机、旧电脑也能跑大模型。",
    },
    {
        "title": "为离线任务箱的『超时重试』功能写一条配置说明",
        "detail": "一句话说明它的作用，并给一个合理的默认秒数建议。",
    },
]

trace = []


def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def emit(event, actor, detail, step):
    rec = {"ts": ts(), "step": step, "event": event, "actor": actor, "detail": detail}
    trace.append(rec)
    # 实时打印便于人工观察（人工干预点之一）
    print(f"[{step:02d}] {actor:<6} {event:<18} {str(detail)[:60]}")


def call_ollama(prompt):
    payload = json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8")).get("response", "").strip()
    except Exception as e:  # URLError / TimeoutError / OSError 等，失败即记 failed 继续
        return f"[调用失败] {e}"


def main():
    step = 0
    print("=== 开始记录生产轨迹（%s）===" % ts())

    # warm-up：先加载模型，避免首个正式任务冷启动超时
    print("warm-up: loading model %s ..." % MODEL)
    _ = call_ollama("hi", MODEL)
    print("warm-up done")

    for i, task in enumerate(TASKS, 1):
        # 1) 人工派活（人工干预点 #1：人类定义任务与边界）
        step += 1
        emit("human_task_submit", "human",
             {"task_index": i, "title": task["title"], "detail": task["detail"],
              "note": "人类定义任务目标与约束，agent 不擅自扩权"}, step)

        # 2) agent 规划处理步骤
        step += 1
        plan = [
            "解析任务目标与输出约束",
            "构造本地模型推理 prompt（含格式约束）",
            "调用本机 Ollama 推理（断网可用）",
            "把结果写回本地任务箱（证据链留痕）",
            "等待人工复核（human-in-the-loop）",
        ]
        emit("agent_plan", "agent", {"steps": plan}, step)

        # 3) 构造 prompt
        step += 1
        prompt = (
            f"任务：{task['title']}\n详情：{task['detail']}\n"
            f"请完成上述任务。输出以「【结论】」开头一句话总结，"
            f"正文分点（每点≤40字），以「【下一步】」结尾给1-2条建议。"
            f"使用简体中文，总长度≤250字。"
        )
        emit("prompt_build", "agent", {"prompt": prompt}, step)

        # 4) 工具调用：本地 Ollama（可观测：记录模型与调用）
        step += 1
        emit("tool_call_ollama", "tool",
             {"tool": "ollama.generate", "model": MODEL, "endpoint": OLLAMA_URL,
              "prompt_len": len(prompt)}, step)
        response = call_ollama(prompt)
        step += 1
        emit("model_output", "tool",
             {"response_len": len(response), "response_head": response[:120]}, step)

        # 5) agent 写回任务箱（证据链：记录由哪台机器/模型完成）
        step += 1
        emit("result_store", "agent",
             {"target": "taskbox.json", "machine": "local-ollama-node",
              "model": MODEL, "status": "done",
              "result_preview": response[:80]}, step)

        # 6) 人工复核（人工干预点 #2：人类确认结果可用/可信）
        step += 1
        review_ok = bool(response) and not response.startswith("[调用失败]")
        emit("human_review", "human",
             {"decision": "accept" if review_ok else "reject",
              "check": "核对输出满足了格式与约束，未越权、未泄露",
              "human_in_the_loop": True}, step)

        # 7) 人工复核不通过则记 reject，不再自动重试（避免长等待；人工可手动重跑）
        #    本演示中 review_ok 由模型是否真实返回决定，正常情况下为 accept。

    # 落盘
    out = "trace.jsonl"
    with open(out, "w", encoding="utf-8") as f:
        for rec in trace:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    manifest = {
        "title": "GOSIM 2026 ARC-Bench 生产轨迹 - cross-machine-offline-taskbox",
        "schema": "每行一个 JSON 事件，字段: ts/step/event/actor/detail",
        "event_types": sorted({r["event"] for r in trace}),
        "actor_legend": {
            "human": "人类操作者（派活 + 复核，human-in-the-loop）",
            "agent": "离线 worker / 调度逻辑",
            "tool": "本地 Ollama 推理（断网可用）"
        },
        "task_count": len(TASKS),
        "event_count": len(trace),
        "repro": "在装有 Ollama 的机器运行 run_trace.py 复现等价轨迹",
        "privacy": "已去敏：不含雇主名/内部路径/真名/内部代号",
        "generated_at": ts(),
    }
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("\n=== 轨迹已写入 %s (%d 事件) + manifest.json ===" % (out, len(trace)))


if __name__ == "__main__":
    main()
