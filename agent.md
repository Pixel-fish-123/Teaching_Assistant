# Agent 操作边界（AI 助教项目）

## 1. 项目目标概览

- 比赛：郑州大学首届 AI 智能体创新应用大赛。
- 选题：A2｜AI 助教·“教、学、评”闭环与个性化学习。
- 课程：以《深度学习》选段为测试课程，参考书在 `reference_material/`。
- 7 天目标：一人做出“带出处的问答 → 章节诊断 → 7 天计划”的可演示原型。
- 当前阶段：D1-1 环境与 DeepSeek 连通；尚未开始业务代码。
- 不做：真实用户/教师盲评、真实学习增益、教师后台、向量库、微调、多智能体、多课程。

正式计划见 `docs/plan.md`；当前检查点见 `checkpoint/current.md`。

## 2. 技术边界

- Python 默认 3.14；只有某个包装不上时，才降 3.12/3.11。
- UI 只用 Streamlit 单体；不引入 FastAPI 双进程。
- LLM 只用 DeepSeek `deepseek-flash`；运行期只读 `.env` 里的 `DEEPSEEK_API_KEY`。
- `deepseek-chat` / `deepseek-reasoner` 是已停用的旧别名，不要使用。
- 检索只用 BM25 + jieba；不引入向量库、embedding、Chroma、torch。
- 数据库只用 SQLite；图表只用 Plotly。
- 运行依赖只保留：`streamlit`、`openai`、`python-dotenv`、`pandas`、`plotly`、`jieba`、`rank-bm25`。
- 不新增框架/依赖；确实需要时先说明理由，等用户确认。

## 3. 文件与操作边界

允许读取：项目内所有文件；`reference_material/` 只读。

允许修改（仅在用户明确要求时）：

- `app.py`、`core/`、`prompts/`、`data/seed/`、`eval/`、`scripts/`
- `docs/plan.md`、`docs/course/*.md`
- `checkpoint/current.md`、`agent.md`、`README.md`

禁止修改/删除：

- `reference_material/` 里的 PDF、原书整理稿和原始资料
- `docs/附件1/2/3`
- `.env`、`.venv/`、`.git/`、`data/app.db`
- 用户的其它未授权文件

禁止操作：

- 不安装/升级依赖，不启动服务，不执行环境配置命令；这些由用户实操，agent 只给步骤和验收标准。
- 不 `git commit`、`git push`、`git reset`、`git checkout`，除非用户明确要求。
- 不把密钥写进代码、文档、日志或截图。
- 不复制参考书原文；只做自制摘要。
- 不伪造测试结果、指标或“已完成”。

## 4. 工作方式

- 先读相关文件，再修改；不要凭记忆猜项目状态。
- 一次只解决一个检查点，只改必要文件；不整项目重写，不顺手重构。
- 修改前说明要改哪些文件；修改后说明如何验证。
- 优先用标准库和现有依赖；不为了“看起来专业”加框架。
- 遇到不确定的需求，先问；不要自行扩大范围。
- 用户说“我来实操”时，只输出命令、检查点、预期输出和排错方法，不替用户执行。

## 5. 检查点协议

- 一次只保留一个当前检查点：`checkpoint/current.md`。
- 检查点只针对当前计划的一小步：0.5—2 小时、3—5 条验收。
- 不预写未来检查点；完成当前这一步，再开下一个。
- 全部验收满足后：
  1. 把证据写进 `docs/plan.md` §17；
  2. 勾选对应进度项；
  3. 删除 `checkpoint/current.md`；
  4. 告知用户已完成。
- 没有全部满足：保留文件，写清阻塞，不勾选、不删除。
- 检查点未完成时，不得开始下一步功能。

## 6. 数据与合规

- 只用模拟学生、模拟答题记录；不出现真实姓名、学号、联系方式。
- 课程资料分两层：
  - 原文层：`reference_material/book_md/`，只在本机检索，不提交。
  - 摘要层：`docs/course/`，自制教学摘要，可提交。
- **摘要不是事实源，原文才是**；摘要与原文冲突时，以原文为准并修摘要。
- 参考书只作学习参考；不复制原书长段，不把原书全文放进仓库。
- 指标必须带样本量和“模拟/自检”说明；不声称真实教学效果。
- 不连接学校教务/学习通/超星等系统；不上传学校内部数据。

## 7. 文档与版本控制

- `docs/` 纳入 git：`plan.md`、比赛附件、`docs/course/*.md`。
- `reference_material/` 不提交：PDF 大、版权敏感；`book_md/` 也不提交。
- `checkpoint/` 不提交：临时检查点，完成即删。
- `.env`、`.venv/`、`data/app.db`、`__pycache__/` 不提交。
- 修改计划时保持简洁；不写未验证的数字，不把“计划”写成“已完成”。

## 8. 当前任务

**D1-1 已完成**（2026-10-21）：Python 3.14.0、7 个依赖 import ok、`pip check` 通过、`deepseek-flash` 返回 `pong`。

下一步是 **D1-2：Streamlit 聊天页 + 第 1 单元讲义**。开始前先按 `checkpoint/README.md` 创建新的 `checkpoint/current.md`，不要直接写代码。

D1-2 范围：

- 只做最小聊天页和第一单元资料
- 不提前做 BM25、诊断、计划、数据库
- 不新增依赖

## 9. 交接状态（2026-10-21）

### 已完成

- **D1-1：环境与 DeepSeek 连通**
  - Python 3.14.0
  - 项目根目录 `.venv` 已创建并激活
  - 7 个依赖安装成功，`pip check` 无冲突
  - `scripts/test_deepseek.py` 调用 `deepseek-flash` 返回 `pong`
  - `requirements.txt` 已生成
  - `.env` 在项目根目录，已被 `.gitignore` 忽略

### 尚未开始

- D1-2：Streamlit 聊天页 + 第 1 单元讲义
- 尚未创建 `app.py`、`core/` 业务模块、课程 md、数据库
- `reference_material/book_md/` 尚未整理
- `docs/course/` 目前只有 README

### 如何接着做

1. 打开 cmd，进入项目：

   ```bat
   cd /d D:\MyProject\AI_teacher
   ```

2. 激活虚拟环境：

   ```bat
   .venv\Scripts\activate.bat
   ```

3. 跑一次连通测试，确认环境没坏：

   ```bat
   python scripts\test_deepseek.py
   ```

   应输出 `pong` 和 usage。

4. 读 `docs/plan.md` §6 的 D1-2，按 `checkpoint/README.md` 建 `checkpoint/current.md`，再开始写代码。

### 交接时必须知道

- 运行模型是 `deepseek-flash`；`deepseek-chat` / `deepseek-reasoner` 已停用。
- `.env` 不提交，换电脑要自己补 key。
- `reference_material/` 和 `book_md/` 不提交，换电脑没有原书就只能跑摘要层。
- `checkpoint/` 是临时目录，完成即删，不提交。
- 当前没有向量库，检索方案是 BM25 + jieba。
- 当前没有 FastAPI，UI 用 Streamlit 单体。
- `deepseek-flash` 默认开启思考模式，简单问答也会产生 reasoning tokens；这不是故障。
- `openai` 3.x、`pandas` 3.x 是新大版本，写代码时按当前 API，不照搬旧教程。
