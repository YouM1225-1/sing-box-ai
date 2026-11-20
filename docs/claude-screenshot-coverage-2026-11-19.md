# Claude 截图域名覆盖核对

2026 年 11 月 19 日核对。**sing-box 最新发布版 v0.1.15 的 `anthropic.srs` 完整覆盖截图的 20 条域名规则**，包括 12 条后缀、6 条精确主机和 2 条关键词。本地工作区的 v0.1.12 也覆盖全部 20 条。

## sing-box 逐项结果

下表列出 v0.1.15 实际生效的匹配方式。后缀覆盖根域及其子域，关键词匹配主机名中出现的对应字符串。

| 截图内容 | 截图匹配方式 | v0.1.15 如何命中 |
| --- | --- | --- |
| `anthropic.com` | 后缀 | 关键词 `anthropic` |
| `claude.ai` | 后缀 | 关键词 `claude` |
| `claude.com` | 后缀 | 关键词 `claude` |
| `claude.app` | 后缀 | 关键词 `claude` |
| `clau.de` | 后缀 | 后缀 `clau.de` |
| `claudemcpclient.com` | 后缀 | 关键词 `claude` |
| `claudemcpcontent.com` | 后缀 | 关键词 `claude` |
| `claudeusercontent.com` | 后缀 | 关键词 `claude` |
| `servd-anthropic-website.b-cdn.net` | 精确主机 | 关键词 `anthropic` |
| `anthropic.com.cdn.cloudflare.net` | 精确主机 | 关键词 `anthropic` |
| `anthropic.auth0.com` | 精确主机 | 关键词 `anthropic` |
| `anthropic-com.ghost.io` | 精确主机 | 关键词 `anthropic` |
| `fcmtoken.googleapis.com` | 精确主机 | 精确主机 `fcmtoken.googleapis.com` |
| `sentry.io` | 后缀 | 关键词 `sentry` |
| `statsigapi.net` | 后缀 | 后缀 `statsigapi.net` |
| `datadog` | 关键词 | 关键词 `datadog` |
| `sift` | 关键词 | 关键词 `sift` |
| `intercom.io` | 后缀 | 后缀 `intercom.io` |
| `intercomcdn.com` | 后缀 | 后缀 `intercomcdn.com` |
| `cdn.usefathom.com` | 精确主机 | 后缀 `usefathom.com` |

用 sing-box 原生匹配器对发布的二进制规则集测试了 32 个域名样例，包括 12 个后缀根域及各自的子域、6 个精确主机和 2 个含关键词的测试主机，全部命中。无关域名对照未命中。截图中两个目的 IP 网段 `160.79.104.0/21`、`2607:6bc0::/32` 也在规则集中。`anthropic.srs` 不含截图中的 macOS 进程路径或 ASN 399358 匹配条件。具体设备使用哪个出口，由客户端路由配置决定。 [v0.1.15 发布页](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.15) · [v0.1.15 规则明细](https://github.com/YouM1225-1/sing-box-ai/blob/v0.1.15/artifacts/v0.1.15/anthropic.json) · [本地 v0.1.12 规则明细](../artifacts/v0.1.12/anthropic.json)

## UniFi 网关

11 月 18 日 15:01 的网关读回清单中，截图里的 **18 个具名域名全部逐字在列**。UniFi 使用静态域名及子域匹配。`datadog` 只覆盖已列出的域名及其子域，例如 `datadoghq.com` 和 `browser-intake-us5-datadoghq.com`。`sift` 没有专门条目。此结论以该次 101 条读回清单为准，本次未复测设备流量。 [网关读回清单](../build/unifi-telemetry-2026-11-18.C1qUKR/domains.txt) · [同步记录](claude-datadog-unifi-coverage-2026-11-18.md)
