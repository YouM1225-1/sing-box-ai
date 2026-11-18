# v0.1.14 Claude 域名补充与发布

2026 年 11 月 18 日，v0.1.14 推送到 `main` 并设为 GitHub Latest。Anthropic 目的规则增加 `ant.dev` 和 `antspace.dev` 两条 `domain_suffix`，覆盖根域和全部子域。截图 17 个域名全部命中。 [正式发布页](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.14)

## 规则差异

- Anthropic 归档中的后缀从 13 条增至 15 条。精确域名、关键词、目的 CIDR 及旧条目证据沿用 v0.1.13。 [语义差异](semantic-diff.json) · [正式规则 JSON](../../../artifacts/v0.1.14/anthropic.json)
- OpenAI 和 Anthropic 独立来源 IP 的 JSON、SRS 与 v0.1.13 逐字节一致。 [正式 manifest](../../../artifacts/v0.1.14/manifest.json)
- 本次按截图覆盖请求登记，旧兼容条目继续使用原证据和复核日期。 [用户请求记录](../../../sources/evidence/claude-two-domains-coverage-request-2026-11-18.json) · [历史证据保留记录](../../../sources/evidence/release-v0.1.14-preserved-entry-exception.json)

## 发布验证

| 检查 | 结果 |
| --- | --- |
| 完整回归 | 92 项通过 |
| 两次正式构建 | 各 6,184 项原生检查通过，9 个输出逐字节一致 |
| 截图及边界 | 17 个域名和 34 个测试子域命中，6 个近似域未命中 |
| 固定版和 Latest | 各核验 6 个附件及 791 项空缓存加载后的回环请求 |
| 历史记录 | 15 个旧 Release 和 18 个旧标签引用在本次发布中保持原样 |

本机空缓存测试核验下载字节、规则命中和来源方向，业务请求全部在回环测试中拒绝。消费者运行验收仍为 pending。 [构建结果](build-results.json) · [截图与边界匹配结果](screenshot-matches.json) · [发布核验](publication-results.json)

固定版及 Latest 的 `anthropic.srs` SHA-256 均为 `8482de1a08ceb770344380d94d47ba2e1f6df1ec159f0f771c98c7594f231396`。 [固定版 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.14/anthropic.srs) · [Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs)
