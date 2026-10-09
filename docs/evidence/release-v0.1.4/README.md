# v0.1.4：补齐 AS399358 可见公告前缀

**已发布为 [v0.1.4](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.4)，并设为 [Latest](https://github.com/YouM1225-1/sing-box-ai/releases/latest)。**

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

## 验证与发布结果

| 检查 | 结果 |
|---|---|
| 原生 JSON/SRS 匹配与方向/边界 | 两次正式构建各 **2,252 项通过，0 失败**。 |
| 完整回归 | **56 项通过，0 失败、0 跳过**。 |
| 可重复构建 | 两次构建的 3 SRS、3 JSON 和 manifest 字节一致。 |
| 变更范围 | 相对 v0.1.3 仅增加指定 IPv6 `/48`；域名及其他两个制品不变。 |
| 固定下载 / Latest 下载 | 各 6 个资产，全部与本地大小、SHA-256 一致。 |
| 原生空缓存加载 | 三份公开远程 SRS 正确下载和缓存，**39 项断言通过**，进程退出 0、监听关闭。 |
| 历史发布 | 既有 5 个 Release 的元数据和资产身份/大小/摘要不变。 |

空缓存断言包含 27 个域名、8 个 IPv6 SOCKS ATYP 4 请求和 4 个 IPv4 ATYP 1 请求；直接使用 IP 的测试不依赖 DNS。每项同时核对目的地址、匹配规则索引和拒绝结果，不把默认拒绝误算为产品命中。业务探测在回环监听处全部拒绝，没有向这些 IP 发起业务连接。

输入提交：`6a9e17531f7892da6dfd42b241f0d2a0df8a5591`。版本标签提交：`e3e32c2`。最终发布回执另行提交，不移动版本标签。源码 ZIP 固定在标签，其内报告保留上传前状态；主分支报告包含最终结果。

此前 v0.1.3 的 VPS 消费者验收不冒用为本次新网段的生产或业务验证。新 manifest 继续保持 `validated_consumers=[]`、`integration_evidence=[]`、`deployment_status=pending`。

## 下载与证据

- [Claude Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [固定 v0.1.4 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.4/anthropic.srs)。
- [发布文件摘要](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.4/SHA256SUMS) · [源码 ZIP](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.4/sing-box-ai-v0.1.4.zip)。
- [两次构建记录](build-results.json) · [完整测试日志](unit-tests.log) · [语义差异](semantic-diff.json)。
- [正式 manifest](../../../artifacts/v0.1.4/manifest.json) · [批次文件摘要](../../../artifacts/v0.1.4/SHA256SUMS)。
- [发布汇总](publication-results.json) · [Latest API 回执](release-final-status.json)。
- [固定下载核验](fixed-downloads.json) · [Latest 下载核验](latest-downloads.json)。
- [原生空缓存结果](remote/results.json) · [运行日志](remote/runtime.log) · [探测脚本](remote-probe.py)。

`anthropic.srs` SHA-256：

```text
a1952bbfe2cafb39cc89c8b3db0f1930f6a2ac029ebe7493463d6b5742488035
```
