# UniFi Claude 域名补充分析

核对日期为 2026 年 11 月 18 日。

## 网关保存与读回

**2026 年 11 月 18 日 12:16（北京时间），已将下列 9 个域名追加到 UniFi 的 `AI-DirectBlock-Domains` 静态表。** 网关回读为 90 条，保留原 81 条，包含截图全部 17 个根域。9 项增量均为截图缺项，`github.com` 已在原表中。 [网关回读的 90 条域名](../build/unifi-domain-append-2026-11-18.pslejpy8/domains.txt) · [原始 81 条导出](../dist/unifi/domains.txt)

修改前后核对了 75 条防火墙策略，配置字段一致，域名阻断策略仍启用且引用同一个静态表。读回确认的是控制器配置，实机转发和 DNS 命中沿用上次验收边界。 [原有 UniFi 配置记录](unifi.md)

## 已追加的 9 个域名

| 根域 | 补充依据 |
| --- | --- |
| `ant.dev` | 同步 v0.1.14 新增后缀 |
| `antspace.dev` | 同步 v0.1.14 新增后缀 |
| `anthropic.team` | 补齐截图，SRS 通过 `anthropic` 关键词覆盖 |
| `chatbotclaude.com` | 补齐截图，SRS 通过 `claude` 关键词覆盖 |
| `claude.new` | 补齐截图，SRS 通过 `claude` 关键词覆盖 |
| `claude.site` | 补齐截图，SRS 通过 `claude` 关键词覆盖 |
| `claudeacademy.com` | 补齐截图，SRS 通过 `claude` 关键词覆盖 |
| `claudepages.dev` | 补齐截图，SRS 通过 `claude` 关键词覆盖 |
| `claudestudio.com` | 补齐截图，SRS 通过 `claude` 关键词覆盖 |

v2fly 的 Anthropic 社区清单已收录这 9 个根域。这里只据此补齐域名范围，各域在实际 Claude 会话中的用途和必要性仍待验证。 [v2fly 上游合并记录](https://github.com/v2fly/domain-list-community/pull/4116/files)

现有表已覆盖 `claude.ai`、`anthropic.com`、`clau.de`、`claude.app`、`claude.com`、`claude.dev`、`claudemcpclient.com` 和 `claudemcpcontent.com`。 [现有导出清单](../dist/unifi/domains.txt)

## 从新版 SRS 重导出的影响

| 处理方式 | 域名表条数 | 截图覆盖 |
| --- | ---: | ---: |
| 变更前静态表 | 81 | 8／17 |
| 只追加 v0.1.14 的两条后缀 | 83 | 10／17 |
| 本次追加截图缺少的 9 条 | 90 | 17／17 |
| 用现有导出器从 v0.1.14 生成并整表替换 | 67 | 3／17 |

我用本地导出器试算了 v0.1.14 的正式归档。结果新增 4 行、移除 18 行。新版 SRS 已将一批具体域名并入关键词匹配，而 UniFi 导出器会跳过关键词，因此直接替换会丢掉 `claude.ai`、`anthropic.com`、`claude.com` 等既有覆盖，还会把 Stripe 和 Fathom 扩大到其根域。试算的 IPv4、IPv6 文件与现有文件逐字节一致。 [UniFi 导出逻辑](../scripts/export_unifi.py) · [v0.1.14 规则 JSON](https://github.com/YouM1225-1/sing-box-ai/blob/v0.1.14/artifacts/v0.1.14/anthropic.json)

评论里的 `datadoghq.com` 与两条 Claude Code Datadog 主机在当前 UniFi 表均未命中。Claude Code 官方将这两个入口列为可选遥测。考虑到这套静态表用于 N100 重启时限制 AI 直连，同时保留其他服务的直连，建议本轮暂不增补 Datadog 全域。 [Claude Code 遥测说明](https://code.claude.com/docs/en/network-config)

## UniFi 侧的覆盖边界

现有静态对象由 Internal → External 防火墙策略引用，下发通过 dnsmasq 学习目的 IP。以普通域名写一行即可匹配根域及其子域。表中的覆盖数量是域名匹配核对，实际阻断取决于网关能否从 DNS 查询中学习对应目的 IP。GitHub Latest 的更新不会自动同步到静态对象。 [本地 UniFi 配置记录](unifi.md) · [dnsmasq 手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html) · [UniFi 区域防火墙文档](https://help.ui.com/hc/en-us/articles/115003173168-Zone-Based-Firewalls-in-UniFi)
