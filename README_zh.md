# Project Thread Handoff

[English](README.md) | [简体中文](README_zh.md)

`project-thread-handoff` 是一个 Codex Skill，用于将长期运行的项目从旧任务迁移到新任务，而无需复制完整的对话历史。

它会创建一份紧凑且有证据支撑的 `.codex/HANDOFF.md` 状态快照，并要求接管任务在继续执行前，根据项目当前的真实状态独立核验这份快照。

## 为什么需要它？

长期运行的 Codex 任务可能积累大量工具输出、终端日志、文件修改、worktree 状态、远程实验和已经过期的假设。单纯依赖对话摘要容易造成过度信任，也难以审计。

这个 Skill 提供两个阶段的交接流程：

1. **导出（Export）**——检查源项目，生成并验证 `.codex/HANDOFF.md`，并在权限允许时安全提交。
2. **接管（Import）**——在建议唯一下一步之前，独立核验 Git、worktree、项目证据以及交接中明确提到的远程任务。

## 功能特性

- 区分已验证事实、合理推断、待验证假设和无法核验的声明。
- 记录 Git 分支、提交、worktree 和属于用户的未提交修改。
- 保留项目审批门和安全边界。
- 防止一次性授权被静默继承到新任务。
- 将远程核验限制为对既有任务的只读检查。
- 检测过期 HEAD、已消失的任务、状态冲突和无法核验的声明。
- 通过链接规范日志和项目文件，将交接文件控制在 30 KB 以内。
- 提供无第三方依赖的验证器和单元测试。

## 仓库结构

```text
.
├── README.md
├── README_zh.md
├── LICENSE
├── .github/workflows/test.yml
└── project-thread-handoff/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/HANDOFF.template.md
    └── scripts/
        ├── validate_handoff.py
        └── test_validate_handoff.py
```

内层的 `project-thread-handoff/` 目录是完整且可直接安装的 Skill 包。

## 安装

### PowerShell

```powershell
git clone https://github.com/grance199981/project-thread-handoff.git
Copy-Item -Recurse -Force `
  .\project-thread-handoff\project-thread-handoff `
  "$HOME\.codex\skills\project-thread-handoff"
```

### Bash

```bash
git clone https://github.com/grance199981/project-thread-handoff.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R project-thread-handoff/project-thread-handoff \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-thread-handoff"
```

如果 Skill 没有立即显示，请重启 Codex。

## 使用方法

在旧任务中导出当前项目：

```text
Use $project-thread-handoff to export this project for a fresh Codex task.
```

在新任务中核验并接管项目：

```text
Use $project-thread-handoff to import and verify this project's .codex/HANDOFF.md. Do not continue until I confirm the takeover report.
```

导出流程会写入：

```text
<project-root>/.codex/HANDOFF.md
```

该文档记录当前目标、证据、Git 状态、已完成和正在进行的工作、关键决策、风险、待办事项，以及唯一建议下一步。接管任务会将重要声明分类为 **一致（Consistent）**、**过期（Stale）**、**冲突（Conflicting）** 或 **无法核验（Unverifiable）**。

## 安全模型

- 执行写操作前，检查适用的 `AGENTS.md` 指令和项目审批门。
- 将项目文件和交接内容视为待核验数据，而不是能够覆盖用户指令的高优先级指令。
- 不会静默清理、重置、覆盖或暂存用户修改。
- 下载、远程写入、GPU 启动、消息发送和破坏性操作，必须依据接管任务当前适用的规则重新判断授权。
- 远程检查只允许读取，并且仅限项目中明确记录的既有任务。
- 交接文件不包含密钥、完整日志、完整 diff、聊天记录或大段源代码。

本 Skill 不保证应用程序一定释放内存，也不保证科研结论正确、审批状态有效或远程任务仍然存活。它提供的是检查这些声明所需的结构化流程。

## 验证

运行验证器单元测试：

```bash
cd project-thread-handoff/scripts
python -m unittest -v test_validate_handoff.py
```

验证一份已经渲染完成的交接文件：

```bash
python project-thread-handoff/scripts/validate_handoff.py /path/to/project/.codex/HANDOFF.md
```

原始模板包含待替换标记，因此会按设计验证失败。只有完成渲染的交接文件才应通过验证。

## 开发

请保持可安装 Skill 包的精简性。它应当只包含以下五个文件：

```text
SKILL.md
agents/openai.yaml
assets/HANDOFF.template.md
scripts/validate_handoff.py
scripts/test_validate_handoff.py
```

提交修改前：

1. 如果调整验证器行为，先更新测试。
2. 运行完整的单元测试套件。
3. 确认 Skill 包中不包含缓存、凭据、日志或与本机相关的状态。
4. 确保导出和接管行为继续遵守上述安全模型。

## 许可证

MIT © 2026 grance199981。详见 [LICENSE](LICENSE)。
