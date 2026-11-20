# Claude 截图域名核对与 UniFi 同步

## UniFi 最终读回

2026 年 11 月 18 日 15:01（北京时间），已追加后文核对出的 7 条规则。控制器与网关 dnsmasq 均读回 **101 条**，原 94 条完整保留，截图中可完整辨认的 **23 个域名全部覆盖**。`sentry.io` 同时覆盖 `o1158394.ingest.us.sentry.io`。本机旧基线的候选也补入了 `browser-intake-ddog-gov.com`，原有 40 个 IPv4 学习地址在读回时均保留。 [网关读回清单](../build/unifi-telemetry-2026-11-18.C1qUKR/domains.txt)

## v0.1.15 发布

远端 `main` 已更新，GitHub Latest 为 **v0.1.15**。新版补录 6 条显式 Anthropic 源记录，三份 SRS 与 v0.1.14 逐字节一致，现有关键词已覆盖这些域名。92 项回归通过，两次正式构建各通过 6,268 项原生检查。固定版与 Latest 各验证了 6 个附件及 797 项空缓存加载后的回环请求。本次 UniFi 验收确认域名表下发和规则引用，实际逐域直连阻断未复测。 [GitHub Release](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.15) · [发布核验](https://github.com/YouM1225-1/sing-box-ai/blob/7ea8a1c0be9c761959d941269640fb9be9e9b129/docs/evidence/release-v0.1.15/README.md)

## 增补前核对

2026 年 11 月 18 日。规则验证使用 sing-box v0.1.14 已发布的 Anthropic SRS、本机 v0.1.12 基线生成的候选 SRS，以及 UniFi 控制器的实际读回清单。

**v0.1.14 覆盖截图可完整辨认的 23 个域名。UniFi 同步两条 Datadog 域名后，仍有 8 个截图域名未覆盖。** 第二张补充截图底部还有两行被遮挡，表中按可见片段与仓库既有项对照列出。 [v0.1.14 正式规则](https://github.com/YouM1225-1/sing-box-ai/blob/v0.1.14/artifacts/v0.1.14/anthropic.json)

## 本次同步

- Anthropic 源清单已显式登记 `datadoghq.com` 为后缀，`http-intake.logs.us5.datadoghq.com` 沿用已启用的精确域名记录。既有 `datadog` 关键词已经覆盖二者，规范化去重后，本地三份候选 JSON 和 SRS 与其 v0.1.12 基线逐字节一致，6,098 项原生匹配检查及 8 项 UniFi 导出测试通过。 [源规则](../sources/anthropic.yaml) · [补充依据](../sources/evidence/claude-datadog-coverage-request-2026-11-18.json)
- UniFi `AI-DirectBlock-Domains` 新增上述两个字面值，控制器和网关 dnsmasq 均读回 94 项。更新前预热的 40 个 IPv4 地址在后续网关复查中仍全部存在。域名实际阻断仍依赖静态或学习到的目的地址命中。 [网关回读清单](../build/unifi-datadog-2026-11-18.N0JdNd/domains.txt)
- Claude Code 官方将该精确主机列为可选遥测入口。UniFi 使用根域 `datadoghq.com` 时，所有该根域的子域都会纳入匹配范围。 [Claude Code 网络配置](https://code.claude.com/docs/en/network-config) · [Datadog 站点说明](https://docs.datadoghq.com/getting_started/site/)

## 原 UniFi 94 条清单的缺项

- `sentry.io`
- `browser-intake-us5-datadoghq.com`
- `browser-intake-us3-datadoghq.com`
- `browser-intake-ap1-datadoghq.com`
- `browser-intake-ap2-datadoghq.com`
- `browser-intake-datadoghq.eu`
- `browser-intake-ddog-gov.com`
- `o1158394.ingest.us.sentry.io`

按 UniFi 的根域与子域匹配，补齐上面 8 项最少需要 7 条。加入 `sentry.io` 就会覆盖 `o1158394.ingest.us.sentry.io`。六个 `browser-intake-…` 主机各自需要独立匹配，因为这类连字符域名处于 `datadoghq.com` 的子域范围之外。

## 逐项结果

| 域名 | 截图匹配要求 | 正式 v0.1.14 | 本地 v0.1.12 候选 | UniFi 94 条静态表 |
| --- | --- | --- | --- | --- |
| `datadoghq.com` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `http-intake.logs.us5.datadoghq.com` | 精确主机 | 覆盖 | 覆盖 | 覆盖 |
| `sentry.io` | 后缀 | 覆盖 | 覆盖 | **缺失** |
| `statsigapi.net` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `intercom.io` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `intercomcdn.com` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `cdn.usefathom.com` | 精确主机 | 覆盖 | 覆盖 | 覆盖 |
| `anthropic.com` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `claude.ai` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `claude.com` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `clau.de` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `claudemcpclient.com` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `claudeusercontent.com` | 后缀 | 覆盖 | 覆盖 | 覆盖 |
| `servd-anthropic-website.b-cdn.net` | 精确主机 | 覆盖 | 覆盖 | 覆盖 |
| `anthropic.com.cdn.cloudflare.net` | 精确主机 | 覆盖 | 覆盖 | 覆盖 |
| `browser-intake-us5-datadoghq.com` | 精确主机 | 覆盖 | 覆盖 | **缺失** |
| `browser-intake-datadoghq.com` | 精确主机 | 覆盖 | 覆盖 | 覆盖 |
| `browser-intake-us3-datadoghq.com` | 精确主机 | 覆盖 | 覆盖 | **缺失** |
| `browser-intake-ap1-datadoghq.com` | 精确主机 | 覆盖 | 覆盖 | **缺失** |
| `browser-intake-ap2-datadoghq.com` | 精确主机 | 覆盖 | 覆盖 | **缺失** |
| `browser-intake-datadoghq.eu` | 精确主机 | 覆盖 | 覆盖 | **缺失** |
| `browser-intake-ddog-gov.com` | 精确主机 | 覆盖 | **缺失** | **缺失** |
| `o1158394.ingest.us.sentry.io` | 精确主机 | 覆盖 | 覆盖 | **缺失** |
| `anthropic.auth0.com` | 部分遮挡，按既有项对照 | 覆盖 | 覆盖 | 覆盖 |
| `anthropic-com.ghost.io` | 部分遮挡，按既有项对照 | 覆盖 | 覆盖 | 覆盖 |


截图的 `datadog`、`sift` 关键词和两个目的 IP 网段 `160.79.104.0/21`、`2607:6bc0::/32` 已包含在 v0.1.14。两个网段也在 UniFi 的静态 IP 清单中。关键词、ASN 和 `FINAL` 动作按其各自语义处理，本表统计的是域名。
