# Claude 网站清单补齐结果

日期：2026-10-15（Asia/Shanghai）。新候选：**`v0.1.5-rc.1`**；修改前：`v0.1.4`。

**已按你的要求补齐除 NTP 外的网页域名和 IP 范围。** 按各配置格式的并集核对，**20 项域名／关键词要求全部覆盖，两个目的 CIDR 全部覆盖**；当前观测到的 AS399358 三个公告前缀也都包含在其中。

已通过 **2,636 项原生 JSON/SRS 匹配检查、64 项回归测试**，均无失败，回归无跳过。新制品已生成在本工作区；尚未发布到 GitHub，`dist/` 保持正式 `v0.1.4`，没有修改运行中的客户端。

文件入口：[新 Claude SRS](../artifacts/v0.1.5-rc.1/anthropic.srs) · [完整 JSON 清单](../artifacts/v0.1.5-rc.1/anthropic.json) · [批次 manifest](../artifacts/v0.1.5-rc.1/manifest.json) · [SHA256SUMS](../artifacts/v0.1.5-rc.1/SHA256SUMS)

导航：[完整覆盖清单](#coverage) · [IP 与 ASN](#ip) · [实现与验证](#verification) · [使用范围](#scope)

<a id="coverage"></a>
## 完整覆盖清单

依据：[Net.Coffee 网页](https://ip.net.coffee/claude/site.html)。四种展示格式存在差异；这次覆盖它们的并集，包括纯域名列表声明的子域通配，以及正文额外的 `sentry` 关键词。核心后缀下的 CDN、API、MCP、Console、Workbench 主机无需重复列入。

| # | 要求 | 新候选的覆盖方式 | 结果 |
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

`cdn.anthropic.com`、`api.anthropic.com`、`mcp.anthropic.com`、`console.anthropic.com`、`workbench.anthropic.com` 均由第一条覆盖，并有原生匹配见证。项目原有固定 Anthropic geosite 基线完整保留。

新增源记录共 **14 条**：8 条后缀、1 条精确主机、3 条关键词、2 条目的 CIDR。生成器去掉重复覆盖后，Claude JSON 为 **15 个精确域名、16 个后缀、3 个关键词、2 个目的 CIDR**。字段数量变少的条目已被较宽规则包含，不是删除覆盖范围；原始用途与来源仍保留在 manifest。

<a id="ip"></a>
## IP 与 ASN

| 要求 | 新候选目的范围 | 结果 |
|---|---|---|
| IPv4 `160.79.104.0/21` | `160.79.104.0`—`160.79.111.255` | 完整 |
| IPv6 `2607:6bc0::/32` | `2607:6bc0::`—`2607:6bc0:ffff:ffff:ffff:ffff:ffff:ffff` | 完整 |

此前的 `/23` 及两个 IPv6 `/48` 都是上述范围的子集，生成结果将它们去重，源证据保留。独立 `anthropic-ip.srs` 仍然使用 `source_ip_cidr: 160.79.104.0/21`，没有把来源集合改作目的集合。

本轮重新核查 RIPE：截至 **2026-10-15 08:00 UTC（北京时间 16:00）**，AS399358 的当前可见公告为：

```text
160.79.104.0/23
2607:6bc0::/48
2607:6bc0:11::/48
```

三条均被新 `/21`、`/32` 覆盖。默认时间窗口、最近一天且降低可见 peer 阈值的查询结果一致，routing-status 也显示 1 条 IPv4、2 条 IPv6。原始响应与摘要见[公告快照](../sources/network/as399358-announced-prefixes-2026-10-15.json)及[观测元数据](../sources/network/as399358-announced-prefixes-2026-10-15.metadata.json)。API 语义见[RIPE 公告前缀说明](https://stat.ripe.net/docs/data-api/api-endpoints/announced-prefixes)。

这里提供的是网页 CIDR 的完整覆盖，以及该时点 ASN 可见前缀的覆盖。SRS 没有动态 ASN 匹配字段；没有把静态集合描述成会自动跟踪未来 ASN 公告。

<a id="verification"></a>
## 实现与验证

新增项标为 `user-requested`，绑定[你的指令原文与准确清单](../sources/evidence/net-coffee-coverage-request-2026-10-15.json)及 SHA-256。它们属于你要求的覆盖范围，不改标为官方必需依赖或已完成真实业务验证。

构建链新增原生 `domain_keyword` 的规范化、包含关系去重、语义比较与原生测试。保留原官方事实校验、原兼容审核、来源／目的方向约束及禁止默认路由的规则。同步调整了原来假定 `/21`、`/32` 外扩不应匹配的测试；旧窄范围仍独立验证，新组合另有明确正负例。

| 检查 | 结果 |
|---|---|
| 网页全部域名／关键词要求 | 20/20 完整覆盖；包括纯列表较宽后缀与正文关键词。 |
| 网页两个目的 CIDR | 2/2 完整覆盖。 |
| 当前 AS399358 公告 | 3/3 已覆盖，限定上述观测时点。 |
| JSON 与 SRS 原生匹配 | **2,636 项通过，0 失败**；含关键词位置、大小写、FQDN、后缀边界、地址段首尾、相邻地址、来源／目的方向与 NTP 示例。 |
| 完整回归 | **64 项通过，0 失败、0 跳过**；包含制品篡改和用户覆盖指令约束。 |
| 二进制验证 | 原生反编译与 JSON 语义一致；独立重新编译字节一致；隔离配置加载通过。 |
| 独立生成 | 第二次生成的 3 份 JSON、3 份 SRS 与候选逐字节一致。 |
| 其他两个产品制品 | OpenAI 与独立来源 IP 的 JSON/SRS 均与 `v0.1.4` 逐字节一致。 |
| 输入身份 | 候选 manifest 的输入哈希与当前工作树一致；工作树尚未提交。 |
| NTP | 没有添加 NTP 分类、协议或时间服务器规则；典型 NTP 主机负例通过。 |

详细证据：[完整结果与逐项映射](evidence/net-coffee-coverage-2026-10-15/results.json) · [原生验证日志](evidence/net-coffee-coverage-2026-10-15/validate.log) · [完整回归日志](evidence/net-coffee-coverage-2026-10-15/unit-tests.log) · [全部原生匹配结果](../artifacts/v0.1.5-rc.1/matches.jsonl)

新 `anthropic.srs`：**488 字节**，SHA-256：

```text
0d8e26718c663ffdb03d0d32a2cf42bf61be540787c46fa7684bf1a70a23c5f1
```

<a id="scope"></a>
## 当前交付范围

已经完成规则源、生成器、测试及可使用的本地候选制品。线上发布入口及客户端尚未切换，因此现有设备不会仅因本地文件生成而自动获得这些新增规则。

“完整覆盖”限定为这份网页在本次核对时的域名／关键词／CIDR 清单及已观测 ASN 前缀，不表示未来出现的任意域名必定命中，也不表示所有请求已在实际设备上走指定出口。关键词依照你的要求采用字符串包含语义，例如其他应用访问含 `datadog` 的域名也会匹配该集合。

本文为当前工作区真实 Markdown 文件，所有本地引用均为相对路径。修改前的差异保留在[原核对报告](net-coffee-claude-coverage-2026-10-15.md)。
