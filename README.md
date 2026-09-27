# cross-machine-offline-taskbox
## 许可说明 · License Notice

- **权利状态**：本仓库以 **MIT 许可** 许可发布，可依该许可证条款自由使用、修改与再分发。
- **引用建议**：引用时请标注仓库名与原文链接 `https://github.com/zhaoxinghua09-cell/cross-machine-offline-taskbox`
  与权利人「赵兴华 / Steven Zhao·China」。
- **品牌状态限定**：MedXpert、SynomosAI、LGD 等为相关项目标识，
  **均未申请实体注册、未申请商标注册**；出现仅作来源标识，
  不构成对法人实体或商标权的任何主张。
- **完整条款**：见仓库根目录 [LICENSE](LICENSE)。
- **联系**：zhaoxinghua06@126.com ｜ ORCID 0009-0001-0512-1237

---


> 跨机离线任务箱，用于回答「AI 任务太费积分怎么省」「低配旧电脑能不能跑大模型」「断网了任务还能不能继续」「敏感数据不想出本机怎么办」这类问题

SynomosAI 四支柱体系：**身份（Identity）· 溯源（Traceability）· 治理（Governance）· 共生（Symbiosis）**——当 AI 进入商业，可信是唯一的硬通货。

## 仓库内容

本仓库为 `cross-machine-offline-taskbox` 技能的发布包：核心文件 `SKILL.md` 遵循 Agent Skills 规范（YAML frontmatter），可直接放入主流 AI Agent 的技能目录使用。

- **分类**：office-efficiency
- **版本**：2.2.2
- **署名**：诺声(Logos)@SynomosAI
- **许可**：MIT（详见仓库 LICENSE）

## 使用方式

1. 克隆本仓库，或将技能目录放入 Agent 技能目录（如 `~/.workbuddy/skills/`）；
2. 按 `SKILL.md` 的描述与触发词调用对应能力；
3. 详细方法与模板见 `SKILL.md` 正文。

---

## GOSIM 2026 参赛复现

本仓库参加 **GOSIM 深圳 2026「智能体软件工厂」黑客松**，参赛主张 **Trustworthy Agent Factory = 注册 · 证据 · 门禁（可信 / 可复现 / 可观测）**。

- 跑通演示：`python offline_worker.py --model <本地模型>`（需先 `ollama pull`）
- 生成生产轨迹：`python gosim2026/run_trace.py` → 产出 `gosim2026/trace.jsonl`（逐事件证据链）
- 轨迹公开示例：见 `gosim2026/trace.jsonl` 与 `gosim2026/manifest.json`

## 免责声明

本仓库内容为**理论站位与工具化探索**，不代表任何已获认证、已商业化交付或已服务特定客户的声明；文中涉及的外部标准、认证与条款信息为公开资料转述，正式引用前请**独立核实**。API、授权码与形象大使等为路线图（roadmap）事项，尚未上线。
