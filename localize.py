"""One-time interface translation and display compatibility for saved reports."""
from pathlib import Path

TRANSLATIONS = {
 'Research workspace · Prototype': '调研工作台 · 初版',
 'Channel Notes · Research workspace': '营销渠道调研助手',
 '◈ CHANNEL NOTES': '◈ 渠道调研助手',
 'FROM PRODUCT BRIEF TO FIRST CONVERSATION': '从产品需求到合作沟通',
 'Find a relevant audience.<br>Start with the evidence.': '找到合适的推广渠道。<br>每个判断都有依据。',
 'Explore up to three channels, review the sources, and prepare a thoughtful introduction.': '筛选最多三个渠道，核对公开资料，准备合作介绍草稿。',
 '01 / Your brief': '01 / 调研需求',
 'Product description': '产品简介', 'Target customers': '目标客户', 'Target market': '目标市场',
 'Research source': '资料来源',
 'Sample evidence library · no API needed': '示例资料库 · 无需 API',
 'Live search · requires server API key': '实时搜索 · 需要配置 API 密钥',
 'Sample mode covers the supplied UK task-management scenario only. Live mode sends your brief to Tavily; avoid confidential information.': '示例模式仅覆盖英国小企业任务管理场景。实时模式会将需求发送给 Tavily 搜索服务，请勿输入机密信息。',
 'Research channels →': '开始调研 →', 'Saved research': '历史调研',
 'Saved automatically on this computer. Reopen after closing your browser.': '报告自动保存在本机，关闭浏览器后仍可重新查看。',
 '02 / RESEARCH DESK': '02 / 调研结果', 'A useful shortlist starts here.': '从这里开始筛选合作渠道。',
 'Describe your product, then review the evidence behind each possible introduction.': '填写产品需求，查看各个候选渠道的推荐依据与待确认信息。',
 'Define the audience': '明确目标客户', 'Check the source and uncertainties': '核对资料来源和未知事项',
 'Edit your outreach draft': '编辑合作介绍草稿', 'Channel shortlist': '候选渠道', 'Export JSON': '导出报告 JSON',
 '03 / First introduction': '03 / 合作介绍', 'Choose a channel': '选择渠道', 'English email draft': '英文合作邮件草稿',
 'Review facts, replace placeholders and translate any non-English brief text before sending. Edits here are not saved; copy them before leaving.': '发送前请核对事实、替换占位内容，并将非英文的需求文字译成英文。此处编辑不会自动保存，请及时复制或导出。',
 'Copy draft': '复制草稿', 'Evidence before outreach. No messages are sent by this tool.': '先核实依据，再开展合作。本工具不会实际发送邮件。',
 'Request failed. Please retry.': '请求失败，请重试。',
 'CHANNEL ${': '渠道 ${', 'Visit channel ↗': '访问渠道网站 ↗', 'Read supporting source ↗': '查看公开依据 ↗',
 'Unconfirmed: ${': '待确认：${', 'No saved reports yet.': '暂无已保存的报告。',
 'Could not load history. Refresh to retry.': '历史记录加载失败，请刷新重试。',
 'Researching and saving…': '正在调研并保存，请稍候…',
 'Saved. Review the evidence and open questions below.': '报告已保存。请核对下方依据和待确认事项。',
 'Copied.': '已复制。', 'Select the text and press Ctrl+C to copy.': '请选中文字并按 Ctrl+C 复制。',
 'Live search is not configured. Set TAVILY_API_KEY on the server, or choose the clearly labelled sample mode.': '实时搜索尚未配置。请在服务端设置 TAVILY_API_KEY，或选择示例资料模式。',
 'Search provider returned HTTP {exc.code}. Check the API key or quota and retry.': '搜索服务返回 HTTP {exc.code}。请检查 API 密钥或额度后重试。',
 'Search is unavailable. Check your connection and retry; existing saved reports are unaffected.': '搜索暂不可用，请检查网络后重试。已经保存的报告不受影响。',
 "Discovery candidate for {brief['audience']} in {brief['market']}. The search excerpt mentions a publishing, community or partnership activity; product suitability still needs manual review.": "面向{brief['market']}的{brief['audience']}找到的候选渠道。搜索摘要提到出版、社群或合作活动；是否适合该产品仍需人工核实。",
 'Audience geography, submission rules, current contact and acceptance of product-related content have not been independently verified.': '受众地区、投稿规则、最新联系方式及是否接受产品相关内容尚未独立核实。',
 'The contact page describes support for owner-managers of businesses with up to 50 employees and considers suitable one-off contributor articles. Source reviewed on 9 November 2026.': '联系页面说明其服务对象包括员工不超过 50 人的企业负责人，并会考虑合适的单篇投稿。资料核对日期：2026 年 11 月 9 日。',
 'Its owner-manager audience overlaps with UK small-business buyers. A practical article about assigning tasks and tracking deadlines is a plausible editorial pitch; this is our inference, not a publisher endorsement.': '其企业负责人受众与英国小企业客户有交集。可尝试提出任务分配和截止日期管理的实用文章。这是基于资料的推断，并非该媒体的认可或承诺。',
 'Acceptance, editorial requirements and any commercial terms must be confirmed. The audience is broader than teams of 1–20.': '需确认是否接稿、编辑要求和商业条款；其受众范围大于 1–20 人团队。',
 'The contact page invites organisations interested in working with the team and offers a newsletter about small-business campaigns, programmes and events. Source reviewed on 9 November 2026.': '联系页面欢迎有合作意向的机构接洽，并提供小企业活动、项目和事件的邮件通讯。资料核对日期：2026 年 11 月 9 日。',
 'The UK small-business focus makes an educational session on team coordination worth exploring. A product demonstration is a proposed idea, not a confirmed opportunity.': '该机构关注英国小企业，可以探索团队协作主题的教学分享。产品演示只是合作建议，尚未得到对方确认。',
 'Commercial product eligibility, newsletter placement and audience team sizes are unconfirmed.': '商业产品能否参与、是否可刊登邮件通讯及受众团队规模均待确认。',
 'The contact page invites prospective authors and original articles through its contact form. Source reviewed on 9 November 2026.': '联系页面邀请作者通过联系表单提交原创文章。资料核对日期：2026 年 11 月 9 日。',
 'A small-business publication with a stated article submission route may suit a useful guide to managing deadlines and responsibilities.': '该小企业媒体提供文章投稿入口，可尝试提交截止日期与任务职责管理方面的实用指南。',
 'Current editorial activity, promotional-content policy, readership and acceptance are unconfirmed.': '目前的编辑活跃度、推广内容政策、读者规模和是否接稿尚待确认。',
 'Please submit a valid JSON brief.': '请提交有效的 JSON 格式需求。',
 '{field}: enter between 2 and 1500 characters.': '{field}：请输入 2–1500 个字符。',
 'Unknown research mode.': '无法识别调研模式。',
 'Sample evidence library, reviewed 9 November 2026. Supports UK small-business task-management briefs only. No live search was performed.': '示例资料库，资料核对日期为 2026 年 11 月 9 日。仅支持英国小企业任务管理场景，本次未执行实时搜索。',
 'Search excerpts only. Candidates are not fully verified recommendations. Open each source and confirm fit before contacting anyone.': '当前结果基于搜索摘要，候选渠道尚未充分核实。联系对方前请打开来源，确认受众和合作方式是否适合。',
 'No supported channels found. Refine the brief or configure live search. Do not infer that no suitable channels exist.': '当前资料无法支持渠道推荐。请调整需求或配置实时搜索；这不代表市场上没有合适渠道。',
 'The report could not be saved. Check disk space and database permissions, then retry.': '报告保存失败。请检查磁盘空间和数据库访问权限后重试。',
 'The brief is too large. Shorten the input and retry.': '提交内容过长，请精简后重试。',
}


def translate_report(value):
    if isinstance(value, list):
        return [translate_report(item) for item in value]
    if isinstance(value, dict):
        return {k: (v if k in ('brief', 'draft') else translate_report(v)) for k, v in value.items()}
    return TRANSLATIONS.get(value, value) if isinstance(value, str) else value


if __name__ == '__main__':
    root = Path(__file__).parent
    for name in ('templates/index.html', 'static/app.js', 'app.py'):
        path = root / name
        content = path.read_text(encoding='utf-8')
        for old, new in TRANSLATIONS.items():
            content = content.replace(old, new)
        if name.endswith('.html'):
            content = content.replace('lang="en"', 'lang="zh-CN"')
        path.write_text(content, encoding='utf-8')
