# v0.1.4：补齐 AS399358 可见公告前缀

本轮在用户明确授权下，将 `2607:6bc0:11::/48` 加入 Claude 目的规则。其身份是经审核的网络覆盖补充，不能等同于已验证的 Claude 业务依赖。

## 范围

| 目的网段 | 依据 |
|---|---|
| `160.79.104.0/23` | 已有官方入口范围。 |
| `2607:6bc0::/48` | 已有官方入口范围。 |
| `2607:6bc0:11::/48` | 新增；用户授权与 ARIN / RIPE 原始证据。 |

三条合计覆盖归档的 AS399358 RIS 观测中全部三个公告前缀。观测快照为 2026-10-09 00:00 UTC，采集存在可见度边界；不保证未来所有路由或所有 Claude 第三方依赖。来源 IPv4 `/21` 独立保留，目的 `/21`、IPv6 `/32` 未扩大。

## 来源和授权

- [研究报告](../../claude-ip-research-2026-10-09.md)。
- [精确网段授权](../../../sources/evidence/anthropic-network-coverage-2026-10-09.json)。
- [ASN 注册原件](../../../sources/network/as399358-rdap-2026-10-09.json)。
- [IPv6 分配原件](../../../sources/network/anthropic-ipv6-rdap-2026-10-09.json)。
- [RIS 公告原件](../../../sources/network/as399358-announced-prefixes-2026-10-09.json)。
- [RIS 状态原件](../../../sources/network/as399358-routing-status-2026-10-09.json)。

## 当前状态

源规则、原始证据和测试正在准备，正式构建、发布及下载回执尚待完成。此前 v0.1.3 的 VPS 消费者验收不冒用为本次新网段的生产或业务验证。新 manifest 继续保持消费者为空、部署 pending。
