# v0.1.5 发布结果与完整覆盖清单

**已发布 [v0.1.5](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.5)，并设为 [Latest](https://github.com/YouM1225-1/sing-box-ai/releases/latest)。** 原 Latest 订阅 URL 保持有效，使用该入口的客户端下次刷新规则时可取得新版。

按你的要求，已完整覆盖 [Net.Coffee 网页](https://ip.net.coffee/claude/site.html)本次核对时各配置格式的并集：**20 项域名／关键词要求、2 个目的 CIDR；排除 NTP**。OpenAI 和 Anthropic 来源规则与上一版字节一致。

导航：[下载](#downloads) · [完整清单](#coverage) · [验证](#verification) · [发布身份与证据](#evidence)

<a id="downloads"></a>
## 下载

- [Claude Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [固定 v0.1.5 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.5/anthropic.srs)
- [OpenAI Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs)
- [发布校验和](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.5/SHA256SUMS) · [源码 ZIP](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.5/sing-box-ai-v0.1.5.zip)

`anthropic.srs` 为 488 字节，SHA-256：

```text
0d8e26718c663ffdb03d0d32a2cf42bf61be540787c46fa7684bf1a70a23c5f1
```

<a id="coverage"></a>
## 完整覆盖清单

| # | 要求 | v0.1.5 覆盖方式 | 结果 |
|---|---|---|---|
| 1 | `anthropic.com` 及子域 | 原有后缀 | 完整 |
| 2 | `claude.ai` 及子域 | 原有后缀 | 完整 |
| 3 | `claude.com` 及子域 | 原有后缀 | 完整 |
| 4 | `clau.de` 及子域 | 原有后缀 | 完整 |
| 5 | `claudemcpclient.com` 及子域 | 原有后缀 | 完整 |
| 6 | `claudemcpcontent.com` 及子域 | 原有后缀 | 完整 |
| 7 | `claudeusercontent.com` 及子域 | 原有后缀 | 完整 |
| 8 | `servd-anthropic-website.b-cdn.net` 及子域 | 新增后缀，包含原精确主机 | 完整 |
| 9 | `anthropic.com.cdn.cloudflare.net` 及子域 | 新增后缀 | 完整 |
| 10 | `anthropic.auth0.com` 及子域 | 新增后缀 | 完整 |
| 11 | `anthropic-com.ghost.io` 及子域 | 新增后缀 | 完整 |
| 12 | `sentry.io` 及子域 | 被新增 `sentry` 关键词完整包含 | 完整 |
| 13 | `statsigapi.net` 及子域 | 新增后缀 | 完整 |
| 14 | `browser-intake-us5-datadoghq.com` | 被新增 `datadog` 关键词包含 | 完整 |
| 15 | 所有含 `datadog` 的域名 | 新增原生关键词 | 完整 |
| 16 | 所有含 `sift` 的域名 | 新增原生关键词 | 完整 |
| 17 | `intercom.io` 及子域 | 新增后缀，含裸域和原有具体主机 | 完整 |
| 18 | `intercomcdn.com` 及子域 | 新增后缀，含裸域和原有具体主机 | 完整 |
| 19 | `cdn.usefathom.com` | 新增精确主机 | 完整 |
| 20 | 所有含 `sentry` 的域名 | 新增原生关键词 | 完整 |

| 目的地址要求 | 已发布范围 | 结果 |
|---|---|---|
| IPv4 `160.79.104.0/21` | `160.79.104.0`—`160.79.111.255` | 完整 |
| IPv6 `2607:6bc0::/32` | `2607:6bc0::`—`2607:6bc0:ffff:ffff:ffff:ffff:ffff:ffff` | 完整 |

核心后缀覆盖 CDN、API、MCP、Console、Workbench 等子域。项目原有 Anthropic 基线完整保留。去重后 Claude JSON 包含 15 个精确域名、16 个后缀、3 个关键词、2 个目的 CIDR；原始来源与用途保留在 manifest。

2026-10-15 08:00 UTC 的 RIPE 快照中，AS399358 可见的 `160.79.104.0/23`、`2607:6bc0::/48`、`2607:6bc0:11::/48` 均被上述范围包含。静态集合不会自动跟踪未来 ASN 公告。关键词采用字符串包含语义，其他应用使用的相关第三方域名也会匹配。

独立 `anthropic-ip.srs` 仍仅匹配来源地址。没有添加 NTP 分类、协议或时间服务器规则。本清单的完整性限于上述网页及观测范围，不表示所有第三方依赖或实际设备业务都已验证。

<a id="verification"></a>
## 验证结果

| 检查 | 结果 |
|---|---|
| 原生 JSON/SRS 匹配、边界与方向 | 两次正式构建各 **2,636 项通过，0 失败**。 |
| 完整回归 | **64 项通过，0 失败、0 跳过**。 |
| 可重复构建 | 两次构建的 3 SRS、3 JSON 和 manifest 字节一致；六份产品文件与候选一致。 |
| 固定版本 / Latest 下载 | 各 **6 个资产**返回 200，与本地字节及 SHA-256 全部一致。 |
| 原生空缓存加载 | 三份公开远程 SRS 下载、缓存正确；**152 项断言通过**。 |
| 测试进程清理 | 进程退出 0，两个回环监听均关闭。 |
| 历史发行保留 | 既有 **6 个 Release** 的元数据、资产身份、大小和摘要未变。 |

空缓存测试使用固定 sing-box alpha.9，主入口包含 131 个域名、6 个 IPv4 和 9 个 IPv6 请求；另有 6 个独立来源方向请求。每项核对入口、目的地址、唯一规则索引和拒绝结果，覆盖关键词、后缀边界、CIDR 端点、NTP 排除及来源／目的隔离。业务请求均在回环监听拒绝，没有向这些目标发起业务连接。

这次完成静态发行和本机隔离验证；未宣称现网设备已经刷新。manifest 保持 `validated_consumers=[]`、`integration_evidence=[]`、`deployment_status=pending`。

<a id="evidence"></a>
## 发布身份与证据

发布时间：`2026-10-15T12:26:52Z`；发布者：`YouM1225-1`；Release ID：`413782827`。发行正文按仓库约定留空，详情保存在本文。

输入提交：`66f228557a5ee0e82d34a1be25331d7eccd3bf89`。版本标签提交：`cd48e23e39ac01371bf7e376a791e687fcf418ec`。最终回执另行提交到 main，不移动标签。源码 ZIP 固定于标签，其中报告保留上传前状态。


- [发布汇总](publication-results.json) · [Latest API 回执](release-final-status.json) · [资产身份与摘要](local-assets.json)
- [固定下载核验](fixed-downloads.json) · [Latest 下载核验](latest-downloads.json) · [历史发行核验](historical-releases-verification.json)
- [原生空缓存结果](remote/results.json) · [运行日志](remote/runtime.log) · [探测脚本](remote-probe.py)
- [构建结果](build-results.json) · [完整回归日志](unit-tests.log) · [语义差异](semantic-diff.json) · [独立复审](independent-review.json)
- [正式 JSON 清单](../../../artifacts/v0.1.5/anthropic.json) · [正式 manifest](../../../artifacts/v0.1.5/manifest.json) · [批次校验和](../../../artifacts/v0.1.5/SHA256SUMS)
- [补齐与来源说明](../../net-coffee-claude-supplement-2026-10-15.md) · [发布授权](../../../sources/evidence/release-v0.1.5-authorization.json) · [语义审批](../../../sources/evidence/release-v0.1.5-review.json)
