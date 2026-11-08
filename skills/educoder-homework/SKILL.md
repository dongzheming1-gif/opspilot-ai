---
name: educoder-homework
description: 头歌(EduCoder)实训/作业自动通关手册——从教学计划找未交任务、抓关卡链与判分脚本、剪贴板粘贴提交、只认点击后新增的 game_status
whenToUse: 用户说"帮我做头歌""头歌某关过一下""educoder 作业还没交"或需要查头歌成绩、关卡状态、判分规则时
metadata:
  version: 1
  updated: 2026-11-03
---

# 头歌（EduCoder）实训自动通关

工具包已在磁盘上跑通 45 条教学计划，**不要重写脚本**，按下面命令直接调。细节在 `references/educoder-api.md`。

## 0. 铁律

1. **不要直连 `update_file.json` 写仓库**：报 `game_id为空` 或返回 `content_modified:0`，写了不生效。必须走页面编辑器。
2. **必须先点「代码」标签**：右侧默认停在「预览」（只显示 base64 原文，没有编辑器）；不点就永远找不到 `.monaco-editor textarea.inputarea`。
3. **Monaco 只能剪贴板粘贴**：`insertText` 多行会把缩进级联（每行 +4 空格、末尾残留旧 `}`），服务端 execjs 直接 `SyntaxError`。用 `edu_run3.js`（已实现剪贴板方案）。
4. **评测只认点击「评测」之后新增的 `game_status.json`**：否则读到上一次的 FAIL 误判。
5. **`rep_content.json` 只能让页面自己发**：页内 `fetch` 或直连会报 `{"status":-102,"服务器时间与您的设备时间不匹配"}` → 用文件树点击法（`edu_read_tree5.js`）。
6. **每关 identifier 不同**：`.../tasks/<coursesId>/<hwid>/<game_ident>`，点「下一关」会换；不要拿第一关的 URL 套到第二关。

## 1. 工具包位置

| 用途 | 路径 |
|---|---|
| 工具包 | `C:\Users\18032\educoder-helper` |
| 登录态 | `C:\Users\18032\educoder-helper\profile\`（Edge 持久化配置；过期就手工登一次） |
| 答案 | `solutions/task_<hwid>/<文件名>` |
| 题目/模板/评测结果 | `data/`（`batch_log.txt` 是执行日志） |
| 文件索引 | 工具包下 `INDEX.md` |

## 2. 标准链路（找没交的 → 通关）

```bash
cd C:/Users/18032/educoder-helper

# ① 教学计划滚到底，落盘 data/plan_full.txt；grep "a/b" 里 a!=b 就是没做完
node edu_plan_scroll.js

# ② 计划页点条目 → 打印 hwid 与 TAB URL
node click_item.js "JavaScript学习手册三：JS运算符"

# ③ 详情页 → shixun_identifier + 各关链接（data/detail_<hwid>.txt）
node edu_detail.js 4271268

# ④ 点「开启挑战」进第一关，抓 /api/tasks/<game>.json
node edu_start_shixun.js 4271268 fx7q35fr t3

# ⑤ 沿 next_game 抓完整条链的 task_pass（任务描述/编程要求/测试说明）
node edu_chain_spec.js 4271268 sjfrf46zpcw9 data/spec_4271268.json

# ⑥ 点文件树抓仓库全部文件，含判分脚本 *Test.py（单/双层 base64 自适应）
node edu_read_tree5.js "<第一关 game_url>" j3        # → data/repo_j3/

# ⑦ 逐关执行（主力执行器，剪贴板粘贴版）
node edu_run3.js 4271268 "<game_url>" "step1/ArithSymbol.js" solutions/task_4271268/ArithSymbol.js

# 批量：一个 PASS 自动下一个（data/batch_tasks.json 驱动）
node run_batch.js
```

## 3. 判分脚本就在仓库里（决定性手段）

每个 step 目录常带 `*Test.py`，读出来就知道判分边界，比猜快十倍：

```
step1/Hello.html      + step1/HelloTest.py
step2/Variable.js     + step2/VariableTest.py
```

实例：`HelloTest.py` 里 `pq(html).text()` 必须**严格等于** `document.write("Hello,JavaScript!");`
→ 多一个空格、多一行注释就判 FALSE。用 `edu_read_tree5.js` 抓下来读一遍再写答案。

## 4. 页面机制 / API 速查

| 接口 | 用途 |
|---|---|
| `GET /api/tasks/<game>.json?homework_common_id=<hwid>` | 关卡元信息：`myshixun.identifier`、`game_count`、`next_game` |
| `GET /api/tasks/<game>/rep_content.json?path=<repo>&homework_common_id=<hwid>&exercise_id=&zzud=<zzud>` | 文件内容（**双层 base64**，偶尔 401，点文件树最稳） |
| `GET /api/tasks/<game>/game_status.json?...` | 评测结果：`test_sets[].result` 全 true 且 `sets_error_count==0` 即 PASS |
| `GET /api/shixun_homeworks/<hwid>/student_works.json?...` | 平台成绩（有时返回空对象，以教学计划页为准） |
| `POST /api/myshixuns/<ident>/update_file.json` | ⚠️ 无效，别用 |

- `zzud` 从任意请求 URL 抓 `zzud=([a-z0-9]+)`。
- 编辑器 data-uri 常是 `inmemory://model/1`，**按文件名选选择器永远超时**；用「第一条可见的 `.monaco-editor textarea.inputarea`」。
- 文件树：`a[title="显示目录"]` 打开 → `.ant-tree-switcher_close` 展开 → `.ant-tree-title` 点文件。

## 5. 执行与判定

`edu_run3.js` 输出 `OUTCOME: PASS/FAIL` + `EVIDENCE`，流程：开页 → 点「代码」→ `navigator.clipboard.writeText` → 点 textarea → Ctrl+A → Backspace → Ctrl+V → 回读 `.view-lines` 校验 → 点「评测」→ 轮询新增 `game_status.json`。

- 评测约 5–8 秒出结果；单关全程 40–90 秒（页面加载 16–18 秒是固定成本）。
- 提交次数上限 200，失败可重试。
- 失败时 `test_sets[].output` 是 expected、`actual_output` 是实际输出 → 直接反推判分规则。
- 详情页才是成绩真相：总成绩 / 已通过数 / 每关我的得分 + 评测次数。

## 6. 故障速查

| 现象 | 原因 / 处理 |
|---|---|
| `PASTE FAIL` / `OUTCOME: FAIL` 秒返回 | 没点「代码」标签；或轮询读到点击前的旧 `game_status` |
| `game_id为空` | 想直连 `update_file.json`，改走 `edu_run3.js` |
| `{"status":-102,...时间不匹配}` | 直连或页内 fetch 了 `rep_content.json`，改用文件树点击法 |
| 服务端 `SyntaxError: missing ) after argument list` | Monaco `insertText` 缩进级联污染的旧代码，必须剪贴板粘贴 |
| 找不到 `.monaco-editor textarea.inputarea` | 还在「预览」标签；或任务用的是老式 CSS 编辑器（改 `do_one.js`） |
| 抓到 13 字节垃圾文件 | 用无脑解两次 base64 的旧脚本，换 `edu_read_tree5.js` |
| 登录态失效 | `profile/` 过期，手工在弹窗里登一次再跑 |

## 7. 交付话术

汇报三件事：**作业名（hwid）+ 几关几关全 PASS + 平台分数**，再补一句还剩哪些没做。别报脚本细节。

## 8. 已完成记录

教学计划 45 条全 `n/n`（2026-11-03 核验）：HTML/CSS 系列 4088582 / 4088605 / 4088606 / 4088608 / 4088609 / 4088611 / 4088612 / 4088617 / 4088618 / 4088620；表格 4088621、4088623（各 1/1）；JS 手册一 4271266（3/3）、手册二 4271267（2/2，80 分）、手册三 4271268（4/4，80 分）。答案在 `solutions/task_<hwid>/`。
