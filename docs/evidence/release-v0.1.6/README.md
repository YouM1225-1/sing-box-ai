# v0.1.6 发布准备与验证

本文件当前记录上传前状态。正式发布回执会在完成固定下载、原生空缓存验证和 Latest 切换后更新到 main；标签及源码 ZIP 保留其固定时点的状态。

本版新增精确域名 `frontend-apps-multi-region.workos.com`，官方网络主清单覆盖由 30/31 提升至 31/31。`cdn.platform.openai.com` 已由 `openai.com` 后缀覆盖，仅刷新来源事实；`openai.org` 记录为待核候选，未进入发布规则。Anthropic 两份 SRS 与 v0.1.5 保持字节一致，Voice 23 个 IP 未变。

候选原生验证 2,650 项通过，另有官方清单、WebSocket 与精确范围的 42 个见证全部符合预期。后续正式构建、下载与远端空缓存结果以生成的证据记录为准；当前不声称已发布或生产设备已刷新。

- [语义差异](semantic-diff.json)
- [官方覆盖与Voice核对](source-coverage.json)
- [候选原生验证](candidate-validate.log)
- [候选完整回归](candidate-unit-tests.log)
- [更新前完整审计](../../openai-domain-coverage-2026-10-19.md)

本次范围为 GitHub 静态规则发布，不包含远端设备配置更改、重启或账户业务验收。
