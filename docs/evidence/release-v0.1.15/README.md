# v0.1.15 Claude 遥测域名规则发布

2026 年 11 月 18 日，v0.1.15 已推送到 `main` 并设为 GitHub Latest。此次发布把用户指定的 Datadog 根域和 5 个遥测主机登记为显式源规则。Datadog US5 的两个既有遥测主机和 `sentry.io` 已有源记录。 [GitHub Release](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.15)

## 本次源规则增量

| 匹配方式 | 域名 |
| --- | --- |
| 后缀 | `datadoghq.com` |
| 精确 | `browser-intake-us3-datadoghq.com` |
| 精确 | `browser-intake-ap1-datadoghq.com` |
| 精确 | `browser-intake-ap2-datadoghq.com` |
| 精确 | `browser-intake-datadoghq.eu` |
| 精确 | `browser-intake-ddog-gov.com` |

这些域名均已命中 v0.1.14 的关键词规则。规范化去重后，v0.1.15 的三份 JSON 与三份 SRS 均与 v0.1.14 逐字节一致。新增源条目可在发布 manifest 的 provenance 中查看。 [语义差异](semantic-diff.json) · [发布 manifest](../../../artifacts/v0.1.15/manifest.json)

## 验证结果

- 92 项回归全部通过。两次正式构建各通过 6,268 项原生检查，9 个构建输出逐字节一致。 [构建结果](build-results.json)
- 固定版和 Latest 均验证了 6 个发布附件及 797 项空缓存加载后的回环请求。其中 10 个本轮核对的遥测域名均命中 Anthropic 规则。 [匹配样本](screenshot-matches.json) · [发布验证](publication-results.json)
- 旧 Release 和标签已对照发布前记录核验。此次验收范围为规则文件和本机加载，消费者运行验收保持 pending。

[固定版 Anthropic SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.15/anthropic.srs) · [Latest Anthropic SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs)
