# 验证记录

2026 年 11 月 11 日：对提交目录运行五项 unittest，全部通过；Flask 测试客户端首页返回 200，示例报告创建返回 201，生成三条示例渠道。上述测试使用当前电脑已有 Python/Flask 环境，不等于已完成全新虚拟环境安装或完整浏览器验收。

2026 年 11 月 9 日：真实 Tavily 请求经项目后端返回 201，得到一条软件评测页面；只证明 API 连通，不能证明推荐质量。最终打包未再次调用收费 API。

自动化测试输出：

```text
test_changed_market_does_not_reuse_uk_recommendations (test_app.WorkflowTests.test_changed_market_does_not_reuse_uk_recommendations) ... ok
test_live_candidates_are_limited_and_deduplicated (test_app.WorkflowTests.test_live_candidates_are_limited_and_deduplicated) ... ok
test_missing_and_wrong_type_inputs (test_app.WorkflowTests.test_missing_and_wrong_type_inputs) ... ok
test_missing_key_reports_failure_without_fake_results (test_app.WorkflowTests.test_missing_key_reports_failure_without_fake_results) ... ok
test_saved_result_survives_app_restart (test_app.WorkflowTests.test_saved_result_survives_app_restart) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.074s

OK

```
