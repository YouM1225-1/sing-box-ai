# Claude IP 是否需要补全：联网复核

查询日期：2026-10-09。比较基线：已发布的 v0.1.3；仓库提交 `2e493c7c1c8dc9b38fbfc73298350213ab284110`。

> 后续决定：用户随后明确要求“也加入 确保完全覆盖 避免遗漏”。因此 v0.1.4 已将 `2607:6bc0:11::/48` 作为经授权的目的网络覆盖补充；以下保留当时研究结论及证据局限，执行结果见[发布记录](evidence/release-v0.1.4/README.md)。

## 研究时的结论

**针对客户端访问 Claude 的默认目的地址规则，当前没有充分依据扩成 IPv4 `/21`、IPv6 `/32` 或整个 AS399358。建议保留现有官方目的范围。**

本次发现一个现有规则之外、由 AS399358 公告的前缀：`2607:6bc0:11::/48`。其归属和路由可核验，客户端服务用途尚未核实，应列为候选；不能把“属于 Anthropic”直接当作“Claude 客户端必需目的地址”。

本轮仅新增这份研究报告，没有修改规则、版本标签或发布资产。

导航：[逐项判断](#decisions) · [官方用途](#official) · [注册与路由](#routing) · [补全条件](#next) · [仓库证据](#local)

<a id="decisions"></a>
## 逐项判断

| 项目 | 核验结论 | 默认规则建议 |
|---|---|---|
| 目的 IPv4 `160.79.104.0/23` | 官方服务接收连接范围；v0.1.3 已有。 | 保留。 |
| 目的 IPv6 `2607:6bc0::/48` | 官方服务接收连接范围；v0.1.3 已有。 | 保留。 |
| `160.79.104.0/21` | 官方列为 Anthropic 主动请求外部服务器时的出口范围；仓库已有对应来源规则。 | 保留来源语义，不扩成目的 `/21`。 |
| `2607:6bc0::/32` | ARIN 注册分配范围，不能据此确认整个范围的服务用途。 | 不并入默认目的规则。 |
| `AS399358` | 注册为 Anthropic；RIS 可见公告比现有目的规则多一个 IPv6 `/48`。 | 不用整个 ASN 替代已核验的服务前缀。 |
| `2607:6bc0:11::/48` | 已公告且归属明确，但官方 IP 页没有把它列为服务入口。 | 列为待核验候选，暂不发布为必需目的规则。 |

以上决策采用此前确认的“核验用途后补齐”口径；如果目标改为所有 Anthropic 自有网络，范围和维护方式需要另行定义。

<a id="official"></a>
## 官方资料如何区分方向

直接读取的 [Anthropic 官方 IP 文档](https://platform.claude.com/docs/en/api/ip-addresses)仍分别列出入口 IPv4 `/23`、入口 IPv6 `/48` 和出口 IPv4 `/21`。从用户客户端看，服务入口是连接的**目的地址**；从自建 MCP 服务看，Anthropic 出口可能是收到连接的**来源地址**。二者不能互换。

该页还说明 Claude Platform on AWS 的入口使用 AWS 地址范围。这表明扩大 Anthropic 自有网段不能保证覆盖所有接入方式。官方 [Claude Code 网络配置](https://code.claude.com/docs/en/network-config#network-access-requirements)按服务域名列出网络依赖，因此默认分流仍应以经核验的域名为主，目的 CIDR 辅助匹配。

另有一处需要记录的官方文档差异：[Anthropic 官方 MCP 插件的滥用防护参考](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/mcp-server-dev/skills/build-mcp-app/references/abuse-protection.md)在来源限流示例中同时使用 IPv4 `/21` 和 IPv6 `2607:6bc0::/48`，而 IP 主文档的出口章节仅列 IPv4。若未来完善服务端 IPv6 来源白名单，应核实此处差异；它不构成扩大客户端目的 IPv6 为 `/32` 的依据。

<a id="routing"></a>
## 注册范围与实际路由

一手 API 查询时间为 **2026-10-09 06:48:57 UTC（北京时间 14:48:57）**。

| 数据源 | 读取结果 | 能证明什么 |
|---|---|---|
| [ARIN ASN RDAP](https://rdap.arin.net/registry/autnum/399358) | `AS399358`，Anthropic, PBC，名称 ANTHROPIC。 | ASN 注册归属。 |
| [ARIN IPv4 RDAP](https://rdap.arin.net/registry/ip/160.79.104.0) | `160.79.104.0/21`，从 `.104.0` 到 `.111.255`。 | 地址注册分配范围。 |
| [ARIN IPv6 RDAP](https://rdap.arin.net/registry/ip/2607:6bc0::) | `2607:6bc0::/32`。 | 地址注册分配范围。 |
| [RIPEstat 公告前缀](https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS399358) | `160.79.104.0/23`、`2607:6bc0::/48`、`2607:6bc0:11::/48`。 | RIS 观察到的路由公告。 |
| [RIPEstat 路由状态](https://stat.ripe.net/data/routing-status/data.json?resource=AS399358) | IPv4 1 条、512 个地址；IPv6 2 条、2 个 `/48`。 | 交叉核对公告数量。 |

RIPEstat 公告前缀接口本次返回的观察区间为 **2026-09-25 00:00:00 至 2026-10-09 00:00:00 UTC**，最新快照也是后者。默认排除不足 10 个 RIS full-feed peers 可见的公告；它是有时间和可见度边界的观测，不是无盲区的实时全球路由表。参见 [RIPE 官方接口说明](https://m.stat.ripe.net/docs/data-api/api-endpoints/announced-prefixes.html)。

把上述可见公告与 v0.1.3 的目的范围比较，差集只有 `2607:6bc0:11::/48`。这说明 ASN 兜底并非完全重复，但仍不能证明差集是用户连接所需。实际客户端 ASN 数据库的展开范围取决于数据来源和更新时点，也不保证与这份 RIS 快照一致。

定向搜索未找到 Anthropic/Claude 官方文档对该新增 `/48` 的客户端服务用途说明。“没有找到”不是证明它永不用于客户端；因此保留为候选，不将未知用途断言为无用。

<a id="next"></a>
## 什么时候应该补

1. 官方入口 IP 文档新增服务前缀：按新增的具体前缀更新目的规则。
2. 可复核的真实客户端记录显示必要服务连接到当前范围之外：核对域名、DNS、目的 IP、所属前缀和操作场景，再决定补域名还是补 CIDR。
3. 自建 MCP 服务需要接收 Anthropic 请求：在服务器侧维护来源允许范围，独立于客户端目的分流规则。

对 `2607:6bc0:11::/48`，下一步有效证据是官方用途说明或真实必要服务连接记录。仅凭注册归属、BGP 公告、IP 数据库分类，尚不足以按当前收录口径补入默认规则。

此前上传的 VPS 验收证明候选规则的匹配和加载行为；隔离测试中的合成请求不能单独证明新增网络是 Claude 真实业务依赖。

<a id="local"></a>
## 仓库核对入口

- [v0.1.3 Claude 规则 JSON](../artifacts/v0.1.3/anthropic.json)：`ip_cidr` 为 `160.79.104.0/23`、`2607:6bc0::/48`。
- [v0.1.3 Anthropic 来源规则 JSON](../artifacts/v0.1.3/anthropic-ip.json)：`source_ip_cidr` 为 `160.79.104.0/21`。
- [完整发布与验收记录](evidence/release-v0.1.3/README.md)。
- [此前域名补全与 IP 取舍报告](claude-rule-supplement-2026-10-09.md)。

字段语义参见 [sing-box 官方 Headless Rule 文档](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/)；来源匹配与目的匹配是不同字段。
