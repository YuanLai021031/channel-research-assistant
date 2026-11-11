# 营销渠道调研助手

作者：Lai Yuan。提交日期：2026 年 11 月 11 日。

这是一个可在本地运行的 Flask 原型：输入产品简介、目标客户和目标市场，查看候选渠道、公开资料与合作邮件草稿，并保存历史报告。当前实时模式的匹配质量有限，详见下文。

## 安装与运行

需要 Python 3.12 或更新版本及联网安装依赖的环境。Windows PowerShell 中进入本文件所在目录，依次执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

浏览器访问 http://127.0.0.1:5055 。请保持终端运行，按 Ctrl+C 停止。如端口占用，请先停止之前启动的同一服务。macOS/Linux 可使用 python3 创建环境及 .venv/bin/python 启动。

## 使用方法

1. 首次可保留默认的英国小企业任务管理需求，选择示例资料库，点击开始调研。该模式无需 API，资料是预先整理的公开来源，不是实时搜索。
2. 核对每个渠道的公开依据、适合原因和待确认事项。
3. 选择渠道、编辑英文合作草稿，使用复制或导出。工具不会发送邮件。
4. 从历史调研打开报告；报告存入自动创建的 instance/research.db，关闭页面后仍可读取。
5. 如需实时搜索，在项目根目录将 .env.example 复制为 .env，填写自己的 Tavily API 密钥：TAVILY_API_KEY=实际密钥。也可设置同名环境变量，环境变量优先。再选择实时搜索。

实时模式会将产品、客户与市场信息发给 Tavily。需要网络及有效 API 额度，调用可能产生费用。无需大语言模型 API；邮件目前由模板生成。密钥只在服务端读取，不随源码提交。官方接口资料：https://docs.tavily.com/documentation/api-reference/endpoint/search

## 示例与验证

examples/sample_report.json 是示例资料模式生成的报告，不是本次实时搜索结果。examples/outreach_email.txt 是该报告的英文模板草稿。

运行自动化测试：

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

测试覆盖输入校验、历史持久保存、样例场景边界、缺少 API 密钥及模拟搜索去重。实际验证结果记录在 VALIDATION.md。

## 实现结构

- app.py：Flask 接口、输入验证、搜索、模板和 SQLite 保存。
- templates/index.html：网页结构。
- static/app.js、style.css：交互与样式。
- localize.py：中文文案与旧报告显示兼容，后端有依赖，请保留。
- POST /api/research：创建并保存调研报告。
- GET /api/reports：读取最近 50 份报告。

## 已知限制

1. 实时搜索仅进行一次查询、读取最多八条结果，并以关键词和域名去重筛选最多三个候选。可能返回不适合的产品或评测页面，也可能返回零条；这不意味着市场上不存在合适渠道。受众、地区和合作入口未自动充分核实。
2. 示例库仅支持英国小企业任务管理场景，不能当作通用实时推荐。
3. 邮件为固定英文模板，切换渠道主要改变称呼；中文输入不会自动翻译，发送前需人工编辑。输入中的商业主张也需人工核实。
4. 原始报告自动保存，但页面上修改的草稿不自动写回数据库，需要复制或导出。历史列表最多显示 50 份。
5. 前端修改输入后仍可能显示上一份报告，请以报告中的需求与时间为准并重新点击调研。实时模式无结果时的提示仍较笼统。
6. 这是本地单用户原型，未实现账号、并发任务队列和生产部署保护，请勿直接公开到互联网。
7. 公开资料可能变化，联系前应打开来源核实。密钥、用户数据库和个人资料均不包含在本提交包内。

## 外部资料与贡献

依赖 Flask（BSD-3-Clause）及 Python 标准库。示例来源：
- https://smallbusiness.co.uk/contact-us/
- https://smallbusinessbritain.uk/contact
- https://www.smallbusinesspro.co.uk/contact.html

AI 与个人工作详见 CONTRIBUTIONS.md。

## 详细使用说明

最开始三个已有的示例资料库（无需API）输入只要凡是为
产品简介：A task management product for teams of 1–20 people, with task assignment, deadline reminders and project progress tracking.
目标客户：Small business owners and small teams
目标市场：United Kingdom
点击开始调研即可。

资料来源使用实时搜索需要加入API密钥，建议使用Tavily API 密钥，加入app.py同一文件夹中的.env文件中即可。
加入code：“TAVILY_API_KEY=你的实际密钥”

加入示例后可以是
产品简介：A task management tool for teams of 1–20 people, with task assignment, deadline reminders and project progress tracking.
目标客户：Small business owners and small team managers
目标市场：United Kingdom

产品简介：A project management tool that helps small marketing agencies assign client work, track campaign deadlines and monitor project progress.
目标客户：Owners and project managers at small digital marketing agencies
目标市场：United Kingdom

产品简介：A team coordination tool for small online shops to assign daily tasks, track product launch deadlines and manage marketing activities.
目标客户：Small e-commerce business owners and operations managers
目标市场：United Kingdom

等等。。

最后因为是免费版本的api，所以搜索限制较多。