# 头歌（educoder）细节

工具目录：`C:\Users\18032\educoder-helper`

## 1. 关键文件

| 文件 | 作用 |
|---|---|
| `edu_run.js` | **主执行器**：开页 → 点「代码」标签 → Monaco 粘贴 → 评测 → 轮询（只认点击后的响应） |
| `do_one.js` | 老执行器（文件树 + Monaco 粘贴），对 CSS 类老任务仍可用；对"默认停在预览标签"的新任务失效 |
| `edu_read_tree3.js` / `edu_read_tree4.js` | 点文件树，抓页面自身 `rep_content.json`，**用来偷评测脚本 `*Test.py`** |
| `edu_next.js` | 点「下一关」，取新关卡文本 + URL |
| `verify_final3.js` | 核验教学计划完成度 + 平台成绩 |
| `edu_plan_scroll.js` | 滚动加载教学计划全量条目 |
| `profile/` | Edge 持久化登录态；过期就手工登一次 |
| `solutions/task_<hwid>/` | 各作业答案文件 |
| `data/` | 题目文本、模板、评测结果、`batch_log.txt` |

## 2. 页面机制

- 游戏页：`https://www.educoder.net/tasks/<coursesId>/<hwid>/<game_ident>?coursesId=<coursesId>`
  - `<game_ident>` **按关卡不同**（4271266：关1 `tm5bhvrgu9ie`、关2 `vbcrathfn75o`、关3 `ruz7nhwbvm6y`）。
  - 点「下一关」会自动换 identifier；也可以从 `tasks/<game>.json` 的 `next_game` 拿。
- 右侧代码区默认停在 **「预览」** 标签，里面显示的是文件的 base64 原文，**没有编辑器**。
  → 必须先点 **「代码」/「代码文件」** 标签，Monaco 才会渲染，出现 `.monaco-editor textarea.inputarea`。
- 编辑器 data-uri 常是 `inmemory://model/1`，**按文件名匹配选择器永远超时**，用"第一条可见的 `.monaco-editor textarea.inputarea`"。
- 文件树：`a[title="显示目录"]` 打开抽屉，`.ant-tree-switcher_close` 展开，`.ant-tree-title` 点文件。

## 3. API（都在页面上下文里用 XHR 发，站点会自己加签名）

| 接口 | 用途 |
|---|---|
| `GET /api/tasks/<game>.json?homework_common_id=<hwid>` | 关卡元信息，含 `myshixun.identifier`、`game_count`、`next_game` |
| `GET /api/tasks/<game>/rep_content.json?path=<repo>&homework_common_id=<hwid>&exercise_id=&zzud=<zzud>` | 文件内容（**双层 base64**；手工 XHR 偶尔 401，点文件树最稳） |
| `POST /api/myshixuns/<ident>/update_file.json` | ⚠️ 写入无效：报 `game_id为空` 或返回 `content_modified:0`，**不要用** |
| `GET /api/tasks/<game>/game_status.json?...` | 评测结果：`test_sets[].result` 全为 true 且 `sets_error_count==0` 即 PASS |
| `GET /api/shixun_homeworks/<hwid>/student_works.json?...` | 平台成绩（有时返回空对象，以教学计划页为准） |

`zzud` 从任意请求 URL 里抓 `zzud=([a-z0-9]+)`。

## 4. 评测脚本就在仓库里（决定性的调试手段）

每个 step 目录常带 `*Test.py`，直接读出判分逻辑：

```
step1/Hello.html + step1/HelloTest.py
step2/JavaScriptEmbed.html + step2/JavaScriptEmbedTest.py
step3/Variable.js + step3/VariableTest.py
```

- `HelloTest.py`：`pq(html).text()` 必须**严格等于** `document.write("Hello,JavaScript!");`
  → 字符串里不能有空格（`" Hello,JavaScript! "` 判 FALSE），不能多写注释文字。
- `JavaScriptEmbedTest.py`：必须等于 `console.log("如何在HTML代码中嵌入JavaScript代码");`
- `VariableTest.py`：`execjs` 调用 `variableTest(c)`；需求是"全局变量 b=100、函数内局部变量 a=10 覆盖全局 a，返回 100+10*c"。

已通过的答案在 `solutions/task_4271266/`（Hello.html / JavaScriptEmbed.html / Variable.js），三关实测 1/1、1/1、4/4 全 PASS。

## 5. 执行与判定

```bash
node edu_run.js <hwid> "<game_url>" <repo_path> <answer_file>
```

输出 `OUTCOME: PASS/FAIL` + `EVIDENCE`。要点：
- 轮询只看**点击「评测」之后**新增的 `game_status.json`，否则拿到上一次的 FAIL。
- 评测约 5–8 秒出结果；单任务全程 40–90 秒（页面加载 16–18 秒是固定成本）。
- 提交次数限制 200，随便重试。

## 6. 作业状态怎么看

教学计划页 `https://www.educoder.net/classrooms/n24qmcx8/teaching_plan`：
每条任务显示 `已完成关卡/总关卡`（`3/3`、`1/1`）+ 剩余时间 + 状态（进行中 / 已截止）。
`edu_plan_scroll.js` 会滚动加载全量条目并落盘 `data/plan_full.txt`；判断"有没有漏做"直接 grep `n/m`，只要出现 `a != b` 就是没做完。

## 7. 从教学计划到 game id 的完整链路（2026-11-03 补）

```bash
cd C:/Users/18032/educoder-helper

# ① 计划页看谁没做完（滚到底，落盘 data/plan_full.txt）
node edu_plan_scroll.js
# 判读：grep 出来的 "a/b" 里 a!=b 就是没做的

# ② 计划页点条目拿 hwid + TAB URL（打印 .../shixun_homework/<hwid>/detail?tabs=1）
node click_item.js "JavaScript学习手册三：JS运算符"

# ③ 详情页给 shixun_identifier（也可直接读 /api/homework_commons/<hwid>.json）
node edu_detail.js 4271268

# ④ 详情页点「开启挑战」，落到第一关 URL、抓 /api/tasks/<game>.json
node edu_start_shixun.js 4271268 fx7q35fr t3

# ⑤ 沿 next_game 把整条链的 task_pass（任务描述/编程要求/测试说明）一次抓全
node edu_chain_spec.js 4271268 sjfrf46zpcw9 data/spec_4271268.json

# ⑥ 抓仓库全部文件（含判分用的 *Test.py）
node edu_read_tree5.js "<第一关 game_url>" j3     # → data/repo_j3/

# ⑦ 逐关执行
node edu_run3.js 4271268 "<game_url>" "step1/ArithSymbol.js" solutions/task_4271268/ArithSymbol.js
```

**新增脚本一览**

| 脚本 | 作用 |
|---|---|
| `click_item.js "<作业名>"` | 计划页点条目，打印 hwid 与 TAB URL |
| `edu_detail.js <hwid>` | 详情页 JSON + 各关链接，落 `data/detail_<hwid>.txt` |
| `edu_start_shixun.js <hwid> <shixun_id> <tag>` | 点「开启挑战」进第一关 |
| `edu_chain_spec.js <hwid> <first_game> <out>` | 走完 next_game 链，抓每关 task_pass |
| `edu_read_tree5.js <game_url> <tag>` | 点文件树抓 rep_content，**单/双层 base64 自适应**（旧的 tree3 无脑解两次会写出 13 字节垃圾） |
| `edu_dump_text.js <game_url> <tag>` | dump 正文 + task json |
| `edu_run3.js <hwid> <game_url> <repo_path> <answer_file>` | **当前主力执行器**，剪贴板粘贴版 |

**踩坑（2026-11-03 新）**
- 页内 `fetch` `rep_content.json` 报 `{"status":-102,"message":"服务器时间与您的设备时间不匹配..."}` → 必须让页面自己发请求（文件树点击法），别直连。
- **Monaco 多行 `insertText` 会把缩进级联**（每行 +4 空格、末尾残留旧 `}`），服务器端 execjs 报 `SyntaxError: missing ) after argument list`。`window.monaco` 未暴露，setValue 走不通。
- 正解 = 剪贴板：`ctx.grantPermissions(['clipboard-read','clipboard-write'])` → `navigator.clipboard.writeText(code)` → 点 `textarea.inputarea` → Ctrl+A → Backspace → Ctrl+V → 回读 `.view-lines` 校验。`edu_run3.js` 已实现，多关一次过。
- 详情页才是成绩真相：`总成绩 / 已通过数 / 未通过 / 每关我的得分 + 评测次数`（一次就过说明答案没试错）。
- 失败时 `game_status.json` 的 `test_sets[].output` 是 expected、`actual_output` 是实际输出，可直接反推判分规则。

## 8. 已完成的作业（2026-11-03 状态）

教学计划 45 条全部 `n/n`，无未交项。
- HTML 系列、CSS 系列：4088582 / 4088605 / 4088606 / 4088608 / 4088609 / 4088611 / 4088612 / 4088617 / 4088618 / 4088620
- 表格边框(4088621)、表格颜色(4088623)：各 1/1
- JS 学习手册一(4271266)：3/3
- **JS 学习手册二：JS 数据类型(4271267)：2/2，80 分**
- **JS 学习手册三：JS 运算符(4271268)：4/4，80 分，四关均一次通过**

### 4271267 答案（`solutions/task_4271267/`）
- `DataKind.js`：`aType..fType` = `object/array/number/string/bool/undefined`，输出要求 `object,array,number,string,bool,undefined`
- `DataKindConvert.js`：`parseInt(args1)`、`parseInt(args2,16)`、`parseFloat(args3)`，最后 `return a+b+c;`

### 4271268 答案（`solutions/task_4271268/`）
四关模板都是 `mainJs(a,b)`，`*Test.py` 用 execjs 调用、stdin 按逗号切成两个字符串参数。

| 关 | 文件 | 关键代码 |
|---|---|---|
| 1 算术运算符 | `ArithSymbol.js` | `var c = parseInt(a) % parseInt(b);` 保留原 `return a+b+c;`（字符串拼接） |
| 2 比较和逻辑运算符 | `LoginBoolSymbol.js` | `if (a > b) { return a && b; } else { return !a; }` |
| 3 条件和赋值运算符 | `ConditionSymbol.js` | `return a > b ? a : b;` |
| 4 优先级与结合性 | `Priority.js` | `var c = (--a+b)*b==24?1:0; var d = 4; var e = c*d+d;` |

第 4 关注意：模板给的 `var e = c*=d+d;` 会算出 0/8，与样例 `6,3→8`、`5,1→4` 不符；直接写 `c*d+d` 才过（判分只看返回值）。
