# 答案与成绩索引

更新于 2026-11-02。**只列已确认的答案文件**，拿不准的标注出来。

## 学习通

### Java Web程序设计（266504945 / 153093101 / 433021318）

| 作业 | 答案文件 | 成绩 | 备注 |
|---|---|---|---|
| 第三章 JSP基本语法 | — | 已完成（早期人工） | 无答案存档 |
| 第四章 JSP内置对象 | — | 已完成（早期人工） | 无答案存档 |
| 第五章 JSP与JavaBean | `answers_ch5.json` | **93.8** | 30 题满分，Q16/Q19 错；重做已用完。Q16 标答 ABC、Q19 标答 setter/getter（已修正进文件） |
| 第六章 Servlet练习题 | `answers_ch6.json`（主用号题号） | **98** | 51 题只错填空「两个常用方法」，重做已用完 |
| 第六章（第二账号） | `answers_ch6_new.json` | **98** | 题号不同，由 `remap_answers.py` 生成；同样只错那题 |

### 《新思想》概论（266119878 / 156364530 / 433021318）

| 作业 | 答案文件 | 成绩 | 备注 |
|---|---|---|---|
| 第一次作业 | — | 93（历史） | 30 题，错 1 道单选（Q3 应 A） |
| 第二次作业 | `answers_xs2_verified.json`（平台标答原文）、`answers_xs2.json` | **88** | 35 题；17/19/23 三道多选错，无重做入口 |

## 头歌

| 作业 | 答案位置 | 状态 |
|---|---|---|
| 4088582 / 4088605 / 4088606 / 4088608 / 4088609 / 4088611 / 4088612 | `solutions/task_<hwid>/` | PASS（2026-10） |
| 4088617 / 4088618 / 4088620 | 同上 | PASS（2026-10-21） |
| 4088621 表格边框 | `solutions/task_4088621/style.css` | PASS 1/1 |
| 4088623 表格颜色、文字与大小 | `solutions/task_4088623/style.css` | PASS 1/1 |
| 4271266 JavaScript学习手册一 | `solutions/task_4271266/{Hello.html, JavaScriptEmbed.html, Variable.js}` | PASS 3/3（关1: 1 点、关2: 1 点、关3: 4 点） |
| 4271267 JavaScript学习手册二：JS数据类型 | `solutions/task_4271267/{DataKind.js, DataKindConvert.js}` | **80/80，2/2**（2026-11-03） |
| 4271268 JavaScript学习手册三：JS运算符 | `solutions/task_4271268/{ArithSymbol.js, LoginBoolSymbol.js, ConditionSymbol.js, Priority.js}` | **80/80，4/4**，四关均一次通过（2026-11-03） |

## 复用到新作业的顺序

1. 先 `list` / 教学计划确认哪份没交、还剩多久。
2. `dump` 出新题 → 和上面同章节的旧 `answers_*.json` 比对：**题干相同就直接抄，题号不同就跑 `remap_answers.py`**。
3. 只对新题单独查资料，别把整份重做一遍。
4. 交完看详情页有没有公开正确答案，有就存一份 `answers_<课>_verified.json` 供下次复用。
