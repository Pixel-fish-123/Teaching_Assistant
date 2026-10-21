# Teaching_Assistant

郑州大学首届 AI 智能体创新应用大赛 A2 项目：课程级 AI 助教原型。

## 当前状态（2026-10-21）

- **D1-1 已完成**：Python 3.14.0 + `.venv` + 7 个依赖 + `deepseek-flash` 连通测试通过。
- **下一步 D1-2**：Streamlit 聊天页 + 第 1 单元讲义。
- 尚未创建业务代码、课程 md、数据库。
- 当前没有向量库，检索计划用 BM25 + jieba；UI 计划用 Streamlit 单体。

## 快速开始

```bat
cd /d D:\MyProject\AI_teacher
.venv\Scripts\activate.bat
python scripts\test_deepseek.py
```

看到 `pong` 说明环境正常。`.env` 需要自己补 `DEEPSEEK_API_KEY`，不要提交。

## 文档

- 计划：`docs/plan.md`
- 模型操作边界与交接：`agent.md`
- 检查点机制：`checkpoint/README.md`
- 参考书：`reference_material/深度学习.pdf`（只读，不提交）
- 原文层：`reference_material/book_md/`（本地检索，不提交）
- 摘要层：`docs/course/`（教学摘要，可提交）
