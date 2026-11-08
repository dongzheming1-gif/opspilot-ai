# OpsPilot AI — Stage8 源码归档 + 学习通/头歌 Skill

本仓库归档三份内容：OpsPilot AI 第 8 阶段的完整源码压缩包，以及两个 DSH（DeepSeek Harness）技能包。

## 目录结构

```
stage8/opspilot-ai-stage8-source.zip         OpsPilot AI Stage8 源码包（114 个条目）
skills/chaoxing-educoder-homework/           学习通 + 头歌 作业自动答题技能（v2, 2026-11-02）
  SKILL.md
  references/answers-index.md
  references/chaoxing.md
  references/educoder.md
  scripts/cx_courses.js
  scripts/remap_answers.py
skills/educoder-homework/                    头歌实训/作业自动通关技能（v1, 2026-11-03）
  SKILL.md
  references/educoder-api.md
```

## 源码包

- 文件：`stage8/opspilot-ai-stage8-source.zip`
- 大小：266,255 字节
- SHA-256：`11f0bb4939253d479e541f442cf59268b654d2f39843a3ac95d171531fb04820`
- 解压后顶层目录：`opspilot-ai/`

解压：

```bash
unzip stage8/opspilot-ai-stage8-source.zip -d .
cd opspilot-ai
```

包内含 `agent/`（采集与上报）、`backend/`（FastAPI 接口、AI 引擎、诊断/告警/审计）、容器化与 compose 配置等。敏感值以 `.env.example` / `.env.compose.example` 形式给出，实际 `.env` 不入库。

## 技能包

两个技能均为纯文本 Markdown + 脚本，可直接复制到 DSH 技能根目录使用：

```bash
cp -r skills/chaoxing-educoder-homework "$HOME/.dsh/skills/"
cp -r skills/educoder-homework "$HOME/.dsh/skills/"
```

- `chaoxing-educoder-homework`：学习通/头歌账号、命令、判分规律与踩坑速查；脚本位于技能内 `scripts/`，禁止重写，按手册直接调用。
- `educoder-homework`：从教学计划定位未交任务、抓关卡链与判分脚本、剪贴板粘贴提交、只认点击后新增的 `game_status`。

## 说明

- 技能内脚本涉及自动化登录与提交作业，仅用于本人账号的本地学习辅助，运行前自行确认目标站点与账号归属。
- 仓库为私有，如后续需公开，请在 Settings → General → Danger Zone 中调整可见性。
