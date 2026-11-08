# 学习通（超星）细节

工具目录：`C:\Users\18032\chaoxing-helper`

## 1. 关键文件

| 文件 | 作用 | 该不该改 |
|---|---|---|
| `work_tool.js` | 唯一入口：list / dump / score / fill | 只在平台改版时改 |
| `nav.js` | 进课程 → 点「作业」→ 返回作业列表 iframe；课程参数读 `CX_COURSE`/`CX_CLASS`/`CX_CPI` | 一般不动 |
| `state.json` | 登录 cookie（storageState） | 只由 `login.js` 写 |
| `login.js` | 弹窗登录，4 分钟内检测 `_uid` 后存 state.json | 换号时用 |
| `remap_answers.py` | 换号后按题干+选项文本重映射答案 | 复用 |
| `captcha.txt` | 验证码输入通道（脚本轮询，外部写入） | 人工写 |

调试/一次性脚本都在 `_archive/`，不要参考。

## 2. 页面结构（判分位置）

| 元素 | 说明 |
|---|---|
| `div.questionLi[typename]` | 题目容器，typename ∈ 单选题/多选题/填空题/判断题/排序题 |
| `h3` | 「题号. (类型, X分) 题干」，题号取 `split('.')[0]` |
| `span[data="X"]` | 选项标记，**data 字母 = 题库原字母**，与屏幕显示顺序无关 |
| `input#answer{qid}` | 隐藏答案框；单选/判断存单字母（判断是 `true`/`false`），**多选存 `AB` 无逗号** |
| `div.Answer textarea` | 填空题输入（UEditor 的原始 textarea，直接写 value 即可） |
| `#popok` | 提交确认弹窗的「确定」 |

**排序题实测**：UI 是单选行为——连点多个选项是**替换**不是追加，hidden 只留最后一个字母。所以 `sort` 写一个字母即可（Java Web 第六章那题正确字母 D = 2 分）。

## 3. 提交通道与验证码

点「提交」→ `#popok` 确认 → 可能弹验证码。`work_tool.js` 会：
1. 截 `captcha.png`；
2. 轮询 `captcha.txt`（最多 5 分钟）；
3. 读到内容后填入并点确定。

人工只需：看图 → 把 4 位码写进 `captcha.txt`。

## 4. 成绩与重做

- 提交后跳到 `.../work/prompt?...`，页面上写「作业 XX分　提交时间…」，并提示「本次作业允许重做 N次，已重做 M次」以及「重做」按钮。
- 详情页 `/mooc-ans/mooc2/work/view?...` 列出每题：我的答案、**正确答案（老师开放时才有）**、得分。
- 平台**取最高分**：重做翻车不会拉低最终成绩（Java Web 第五章 93.8 与 84.5 并存、第六章 92.1 → 98 都验证过）。
- 没有重做入口的作业（《新思想》）：列表和详情页都没有「重做」，直接开 `dowork` 页报「作答状态异常！」——一次性定终身。

## 5. 已知课程参数

| 课程 | courseid | clazzid | cpi |
|---|---|---|---|
| Java Web程序设计（王威） | 266504945 | 153093101 | 433021318（主用号）/ 433021360（第二账号） |
| 2026-2027-1《习近平新时代中国特色社会主义思想概论》（魏丽） | 266119878 | 156364530 | 433021318 |
| 计算机组成原理（刘爱军） | 227830287 | 157337817 | 433021360 |
| 路由与交换技术（杜红乐） | 266413305 | 152823112 | 433021318 |
| 马克思主义基本原理概论（熊晓琳等） | 208917453 | 127066918 | 433021318 |
| 形势与政策 2025-2026(2)（张路） | 263917168 | 147278824 | 433021318 |
| 现代艺术设计鉴赏（李斌） | 261596316 | 142212357 | 433021318 |
| 线性代数（网络）2024-2025-2（王念良） | 231531493 | 115637304 | 433021318 |

（后四门只登记过参数，没做过作业；用时先 `list` 看有没有作业。）

## 6. 填空判分实测（Java Web 第六章）

| 题目 | 写法 | 结果 |
|---|---|---|
| web.xml 两组标签 | `servlet` / `servlet-mapping` | ✅ 2 分 |
| 同上 | `<servlet>` / `<servlet-mapping>` | ❌ 0（尖括号被判分吃掉） |
| 表单 action / input type | `RegistServlet` / `submit` | ✅ 2 分 |
| 乱码处理提交方式 | `get` | ✅ 2 分 |
| 得到 Session 的方法 | `getSession()` | ✅ 2 分 |
| 应用程序上下文对象 | `application` | ✅ 2 分 |
| JSP 内置对象类型 | `javax.servlet.ServletContext` / `javax.servlet.jsp.JspWriter` / `javax.servlet.http.HttpServletRequest` / `javax.servlet.http.HttpServletResponse` / `javax.servlet.http.HttpSession` | ✅ 2 分（只写 `ServletContext` 等简名判 0） |
| **接收表单数据的两个常用方法** | `getParameter`/`getParameterValues`、`getParameter()`/`getParameterValues()`、`request.getParameter()`/`request.getParameterValues()`、`getParameter(String name)`/`getParameterValues(String name)` | ❌ 四种全 0，**标答未知**，别浪费时间猜 |

## 7. 题库风格（影响猜题）

- **Java Web（王威）**：爱用"近似错项"做陷阱。例：`建成社会主义现代化国家` vs `实现社会主义现代化国家`；`农业现代化` vs `农村现代化`；`十二个坚持` vs 实际个数。
- **《新思想》（魏丽）**：多选倾向**全包**——能沾边就选。三道丢分题标答都是"比我猜的更大"：Q17/Q19 标答 ABCD、Q23 标答 ABC。
- 结论：做《新思想》先全选再看有没有明显错的；做 Java Web 逐字扣细节。
