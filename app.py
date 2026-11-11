"""Local, single-user channel research prototype. No mail is sent."""
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit

from flask import Flask, jsonify, render_template, request
from localize import translate_report

ROOT = Path(__file__).parent


class ResearchError(Exception):
    pass


def search_channels(brief):
    key = os.getenv('TAVILY_API_KEY')
    if key is None:
        env_file = ROOT / '.env'
        if env_file.is_file():
            for line in env_file.read_text(encoding='utf-8').splitlines():
                if line.startswith('TAVILY_API_KEY='):
                    key = line.partition('=')[2].strip().strip('\"').strip("'")
                    break
    if not key:
        raise ResearchError('实时搜索尚未配置。请在服务端设置 TAVILY_API_KEY，或选择示例资料模式。')
    query = f"{brief['market']} {brief['audience']} {brief['product']} newsletter community publication contribute partnership"
    req = Request('https://api.tavily.com/search', data=json.dumps({
        'query': query, 'max_results': 8, 'search_depth': 'basic',
        'include_answer': False,
    }).encode(), headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        with urlopen(req, timeout=25) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise ResearchError(f'搜索服务返回 HTTP {exc.code}。请检查 API 密钥或额度后重试。') from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise ResearchError('搜索暂不可用，请检查网络后重试。已经保存的报告不受影响。') from exc
    results, seen = [], set()
    for item in data.get('results', []):
        url = item.get('url', '')
        parsed = urlsplit(url)
        host = parsed.hostname or ''
        content = item.get('content', '')
        if parsed.scheme != 'https' or not host or host in seen or not content:
            continue
        # Conservative first version: only retain snippets with a channel signal.
        if not any(term in content.lower() for term in ('newsletter', 'community', 'contributor', 'editorial', 'publication', 'partnership')):
            continue
        seen.add(host)
        results.append({
            'name': item.get('title') or host, 'url': url,
            'evidence': content[:900], 'source': url,
            'reason': f"面向{brief['market']}的{brief['audience']}找到的候选渠道。搜索摘要提到出版、社群或合作活动；是否适合该产品仍需人工核实。",
            'unknown': '受众地区、投稿规则、最新联系方式及是否接受产品相关内容尚未独立核实。',
        })
        if len(results) == 3:
            break
    return results


def sample_channels(brief):
    market = brief['market'].lower()
    audience = brief['audience'].lower()
    product = brief['product'].lower()
    uk = any(x in market for x in ('uk', 'united kingdom', '英国', 'britain'))
    small = any(x in audience for x in ('small business', 'small team', '小企业', '小团队', 'sme'))
    tasks = any(x in product for x in ('task', 'project management', '任务', '项目管理'))
    if not (uk and small and tasks):
        return []
    return [
        {'name': 'Small Business UK', 'url': 'https://smallbusiness.co.uk/',
         'source': 'https://smallbusiness.co.uk/contact-us/',
         'evidence': '联系页面说明其服务对象包括员工不超过 50 人的企业负责人，并会考虑合适的单篇投稿。资料核对日期：2026 年 11 月 9 日。',
         'reason': '其企业负责人受众与英国小企业客户有交集。可尝试提出任务分配和截止日期管理的实用文章。这是基于资料的推断，并非该媒体的认可或承诺。',
         'unknown': '需确认是否接稿、编辑要求和商业条款；其受众范围大于 1–20 人团队。'},
        {'name': 'Small Business Britain', 'url': 'https://smallbusinessbritain.uk/',
         'source': 'https://smallbusinessbritain.uk/contact',
         'evidence': '联系页面欢迎有合作意向的机构接洽，并提供小企业活动、项目和事件的邮件通讯。资料核对日期：2026 年 11 月 9 日。',
         'reason': '该机构关注英国小企业，可以探索团队协作主题的教学分享。产品演示只是合作建议，尚未得到对方确认。',
         'unknown': '商业产品能否参与、是否可刊登邮件通讯及受众团队规模均待确认。'},
        {'name': 'SmallBusinessPro', 'url': 'https://www.smallbusinesspro.co.uk/',
         'source': 'https://www.smallbusinesspro.co.uk/contact.html',
         'evidence': '联系页面邀请作者通过联系表单提交原创文章。资料核对日期：2026 年 11 月 9 日。',
         'reason': '该小企业媒体提供文章投稿入口，可尝试提交截止日期与任务职责管理方面的实用指南。',
         'unknown': '目前的编辑活跃度、推广内容政策、读者规模和是否接稿尚待确认。'},
    ]


def draft_email(brief, channel):
    return (f"Subject: Practical content collaboration enquiry\n\nHello {channel['name']} team,\n\n"
            f"I am getting in touch about a product described as follows: {brief['product']}\n\n"
            f"It is intended for {brief['audience']} in {brief['market']}. We are exploring relevant channels and would like to ask whether a practical educational article or a short product demonstration could be suitable for your audience.\n\n"
            "Would you be open to reviewing a brief outline? Please let us know your submission guidelines, the appropriate contact, and any applicable commercial terms. We would be happy to adapt the proposal to your editorial requirements.\n\n"
            "Kind regards,\n[Your name]\n[Product / company]\n[Contact details]")


def create_app(database=None):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16000
    path = Path(database or ROOT / 'instance' / 'research.db')
    path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect():
        conn = sqlite3.connect(path)
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    with connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, created TEXT NOT NULL, body TEXT NOT NULL)')

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/api/reports')
    def history():
        with connect() as conn:
            rows = conn.execute('SELECT body FROM reports ORDER BY created DESC LIMIT 50').fetchall()
        return jsonify([translate_report(json.loads(row[0])) for row in rows])

    @app.post('/api/research')
    def research():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error='请提交有效的 JSON 格式需求。'), 400
        brief = {}
        for field in ('product', 'audience', 'market'):
            value = data.get(field)
            if not isinstance(value, str) or not 2 <= len(value.strip()) <= 1500:
                label = {'product': '产品简介', 'audience': '目标客户', 'market': '目标市场'}[field]
                return jsonify(error=f'{label}：请输入 2–1500 个字符。'), 400
            brief[field] = value.strip()
        mode = data.get('mode', 'sample')
        if mode not in ('sample', 'live'):
            return jsonify(error='无法识别调研模式。'), 400
        try:
            channels = sample_channels(brief) if mode == 'sample' else search_channels(brief)
        except ResearchError as exc:
            return jsonify(error=str(exc)), 502
        report = {'id': str(uuid.uuid4()), 'created': datetime.now(timezone.utc).isoformat(),
                  'brief': brief, 'mode': mode, 'channels': channels,
                  'notice': ('示例资料库，资料核对日期为 2026 年 11 月 9 日。仅支持英国小企业任务管理场景，本次未执行实时搜索。' if mode == 'sample' else '当前结果基于搜索摘要，候选渠道尚未充分核实。联系对方前请打开来源，确认受众和合作方式是否适合。'),
                  'draft': draft_email(brief, channels[0]) if channels else '',
                  'next_step': '' if channels else '当前资料无法支持渠道推荐。请调整需求或配置实时搜索；这不代表市场上没有合适渠道。'}
        try:
            with connect() as conn:
                conn.execute('INSERT INTO reports VALUES (?, ?, ?)', (report['id'], report['created'], json.dumps(report, ensure_ascii=False)))
        except sqlite3.Error:
            return jsonify(error='报告保存失败。请检查磁盘空间和数据库访问权限后重试。'), 500
        return jsonify(report), 201

    @app.errorhandler(413)
    def too_large(error):
        return jsonify(error='提交内容过长，请精简后重试。'), 413

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=5055, debug=False)
