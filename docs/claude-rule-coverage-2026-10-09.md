# Claude 域名与 IP 覆盖检查

> 本文保留修改前 `v0.1.2` 的检查结果。随后按用户选择完成的规则补充与新候选验证，见[补齐报告](claude-rule-supplement-2026-10-09.md)。

核对日期：2026-10-09（Asia/Shanghai）

仓库：`sing-box-ai`；检查时提交：`fb7cf33`；当前本地版本：`v0.1.2`。

**结论：没有全部覆盖。** 按 Claude 对应的 `anthropic.srs` 判断，你提供的 18 条域名/关键词规则中，**7 条完整覆盖、11 条未覆盖**；两条目的 IP 前缀均只覆盖子集；没有配置 `AS399358` 兜底。独立 `anthropic-ip.srs` 虽有 IPv4 `/21`，但它匹配来源地址，不能当成相同范围的目的地址规则。

如果将整个仓库的 OpenAI 规则也纳入观察，Sentry、Datadog、Intercom 有部分相关范围，但仍不能完整覆盖你给出的规则，也不能代表它们已经归入 Claude 分流。

导航：[核对依据](#basis) · [完整域名清单](#domains) · [IP 与 ASN](#ips) · [通用配置](#general) · [结论与后续边界](#conclusion)

<a id="basis"></a>
## 核对依据

以当前实际输出为准，而不是只搜索 YAML 中是否出现过某个字符串：

- [Claude 发布源 JSON](../artifacts/v0.1.2/anthropic.json) 与 [实际 Claude SRS](../dist/anthropic.srs)。
- [独立来源地址 JSON](../artifacts/v0.1.2/anthropic-ip.json) 与 [来源地址 SRS](../dist/anthropic-ip.srs)。
- [OpenAI 发布源 JSON](../artifacts/v0.1.2/openai.json)，用于说明其他产品是否有相关规则。
- [Claude 补充源](../sources/anthropic.yaml)、[来源地址补充源](../sources/anthropic-ip.yaml)、[基线域名](../sources/upstream/dlc-anthropic.txt)、[启用策略](../sources/policy.yaml)、[候选清单](../sources/discovery/pending.yaml)。
- [正式方案](plan.md) 与 [发布 manifest](../artifacts/v0.1.2/manifest.json)。

本次已执行：

1. 比较 `dist/` 三份 SRS 与 `artifacts/v0.1.2/` 对应文件的 SHA-256，全部一致，且匹配 manifest。
2. 用仓库现有 sing-box 原生反编译三份 `dist/` SRS；忽略数组顺序、单元素数组/标量表示及单个主机 IP 的 `/32` 表示差异后，与发布源 JSON 的字段和值一致。
3. 检查 manifest 记录的输入文件哈希，无不一致；发布源 JSON 哈希也与 manifest 一致。
4. 静态比较域名匹配范围、CIDR 包含关系与来源/目的方向。

此处“覆盖”指所需规则的匹配范围被现有规则包含。没有把某个域名一次解析得到的 IP 视为长期域名覆盖；本次也未验证线上消费者配置、出口或真实业务请求。

当前 Claude 输出包含 **14 个精确域名、9 个域名后缀、2 个目的 CIDR**。其中没有 `domain_keyword` 或 ASN 条目。

<a id="domains"></a>
## 完整域名清单

下表“Claude 覆盖”按 `anthropic.srs` 计算；“其他记录”不计入该列。

| # | 你提供的规则 | Claude 覆盖 | 当前依据或其他记录 |
|---|---|---|---|
| 1 | `DOMAIN-SUFFIX,anthropic.com` | **完整** | `anthropic.json` 第 21 行，根域及各级子域均覆盖。 |
| 2 | `DOMAIN-SUFFIX,claude.ai` | **完整** | 同文件第 23 行，根域及各级子域均覆盖。 |
| 3 | `DOMAIN-SUFFIX,claude.com` | **完整** | 同文件第 25 行，根域及各级子域均覆盖。 |
| 4 | `DOMAIN-SUFFIX,clau.de` | **完整** | 同文件第 22 行，根域及各级子域均覆盖。 |
| 5 | `DOMAIN-SUFFIX,claudemcpclient.com` | **完整** | 同文件第 27 行，根域及各级子域均覆盖。 |
| 6 | `DOMAIN-SUFFIX,claudeusercontent.com` | **完整** | 同文件第 29 行，根域及各级子域均覆盖。 |
| 7 | `DOMAIN,servd-anthropic-website.b-cdn.net` | **完整** | 同文件第 16 行，已有相同精确主机规则。 |
| 8 | `DOMAIN,anthropic.com.cdn.cloudflare.net` | **未覆盖** | 不在当前两份产品域名输出中；`anthropic.com` 后缀不会匹配它，因为它的结尾是 `cloudflare.net`。 |
| 9 | `DOMAIN,anthropic.auth0.com` | **未覆盖** | 不在当前两份产品域名输出中，也不是 `anthropic.com` 的子域。 |
| 10 | `DOMAIN,anthropic-com.ghost.io` | **未覆盖** | 不在当前两份产品域名输出中。 |
| 11 | `DOMAIN-SUFFIX,sentry.io` | **未覆盖** | OpenAI 仅有 `o207216.ingest.sentry.io`、`o33249.ingest.sentry.io` 两个精确主机；即使合看全仓库，也只覆盖部分范围。 |
| 12 | `DOMAIN-SUFFIX,statsigapi.net` | **未覆盖** | `statsigapi.net`、`events.statsigapi.net` 仅登记为 OpenAI 的 pending 精确主机，未进入当前输出；OpenAI 的 `oaistatsig.com` 也不是这个域名。 |
| 13 | `DOMAIN,browser-intake-us5-datadoghq.com` | **未覆盖；已登记未启用** | `sources/anthropic.yaml` 第 166 行已有精确主机，第 171 行为 optional；`enabled_optional` 只启用两个字体域名。 |
| 14 | `DOMAIN-KEYWORD,datadog` | **未覆盖** | Claude 源中只有两个未启用的 optional 精确主机；OpenAI 输出也仅有部分精确主机，不等价于匹配所有包含 `datadog` 的域名。 |
| 15 | `DOMAIN-KEYWORD,sift` | **未覆盖** | 当前两份产品域名输出均无该关键词或相关已列主机。 |
| 16 | `DOMAIN-SUFFIX,intercom.io` | **未覆盖** | OpenAI 有 `.intercom.io`，按本仓库 sing-box 语义只匹配子域，不包括根域 `intercom.io`；不属于 Claude 集合。 |
| 17 | `DOMAIN-SUFFIX,intercomcdn.com` | **未覆盖** | OpenAI 有 `.intercomcdn.com`，只匹配子域，不包括根域 `intercomcdn.com`；不属于 Claude 集合。 |
| 18 | `DOMAIN,cdn.usefathom.com` | **未覆盖；候选** | `sources/discovery/pending.yaml` 第 421 行起有 Anthropic 候选，但 `selected_pending: []`，未进入输出。 |

**7 条完整覆盖 = 6 个核心后缀 + 1 个 CDN 精确主机。** 六个核心后缀由基线继承，不能只因补充 YAML 中没有重复列出就判定遗漏。

两个容易混淆的地方：

- Claude 源里的两个 Datadog optional 主机分别是 `http-intake.logs.us5.datadoghq.com`、`browser-intake-us5-datadoghq.com`，当前均未启用。即使以后启用，也只是这两个精确主机，仍不是 `DOMAIN-KEYWORD,datadog`。
- OpenAI 的 Datadog 主机是 `browser-intake-datadoghq.com`、`rum.browser-intake-datadoghq.com`，与用户所列 `browser-intake-us5-datadoghq.com` 不同。另有 OpenAI 规则不代表 Claude 会匹配同一产品规则或走同一出口。

<a id="ips"></a>
## IP 与 ASN

| 用户要求 | 当前仓库输出 | 结论 |
|---|---|---|
| `IP-CIDR,160.79.104.0/21` | Claude 目的集合为 `ip_cidr: 160.79.104.0/23`；独立来源集合为 `source_ip_cidr: 160.79.104.0/21` | **目的范围仅部分覆盖，不能把来源 `/21` 算进去。** |
| `IP-CIDR6,2607:6bc0::/32` | Claude 目的集合为 `ip_cidr: 2607:6bc0::/48` | **仅部分覆盖，`/48` 小于 `/32`。** |
| `IP-ASN,399358` | 当前输出没有 ASN 规则，也没有以该 ASN 全量网段为输入的兜底集合 | **未配置 ASN 兜底，不能认定覆盖该 ASN 的全部地址。** |

IPv4 的具体差异：

- 你提供的 `/21`：`160.79.104.0`—`160.79.111.255`。
- 当前目的 `/23`：`160.79.104.0`—`160.79.105.255`。
- 因此 `160.79.106.0`—`160.79.111.255` 没有被当前这条 Claude **目的 IP** 规则覆盖。例如 `160.79.106.1` 在用户 `/21` 内，但不在仓库目的 `/23` 内。

IPv6 的具体差异：

- 当前 `/48` 的第三组固定为 `0000`，结束于 `2607:6bc0:0:ffff:ffff:ffff:ffff:ffff`。
- 用户 `/32` 包含所有第三组值，结束于 `2607:6bc0:ffff:ffff:ffff:ffff:ffff:ffff`。
- 例如 `2607:6bc0:1::1` 在用户 `/32` 内，但不在仓库 `/48` 内。

这组差异在现有设计中有明确记录。[仓库归档的官方 IP 事实](../sources/official/source-records/anthropic-ip.json) 将 `/23`、IPv6 `/48` 列为 inbound 地址，将 IPv4 `/21` 列为 outbound 地址；[正式方案](plan.md#supplements) 因而区分客户端访问 Anthropic 的目的地址和 Anthropic 访问外部服务时的来源地址。本结论说明仓库已采纳的证据与设计，不声称本次重新抓取了最新官方 IP 清单。

原配置的 `no-resolve` 是消费者侧匹配行为选项，不是额外地址范围；本仓库 SRS 不提供同名选项，不能仅凭地址存在就认为完整复制了原客户端的处理行为。

<a id="general"></a>
## `[General]` 与 `[Proxy]` 的范围

这些项属于客户端配置，不属于本仓库的三个产品规则集：

| 原配置 | 本仓库规则集是否提供等价配置 |
|---|---|
| `bypass-system = true` | 否；系统旁路行为由使用规则集的客户端配置决定。 |
| `skip-proxy` 中的 `127.0.0.1`、`192.168.0.0/16`、`10.0.0.0/8`、`172.16.0.0/12`、`100.64.0.0/10` | 未作为这些产品规则集的通用旁路清单提供。 |
| `skip-proxy` 中的 `localhost`、`*.local` | 未作为这些产品规则集的通用旁路清单提供。 |
| `CLAUDE0409 = direct` | SRS 不定义这个出站名称，也不指定 direct；需要消费者路由自行绑定。 |

因此，即使域名范围完全相同，也不能直接认定两个客户端的出站、旁路、解析和规则优先级行为相同。

<a id="conclusion"></a>
## 结论与后续边界

你这份配置**不能被当前仓库的 Claude 规则完整替代**。差异分为三类：

1. **未进入 Claude 输出的 11 条域名/关键词规则**：详见完整表，其中 Datadog 精确主机为未启用 optional，Fathom 为未选择 pending；OpenAI 的部分相关主机不能算作 Claude 已收录。
2. **IP 范围和方向不同**：目的 IPv4 仅 `/23`，IPv6 仅 `/48`；独立 IPv4 `/21` 为来源识别；没有 ASN 全量兜底。
3. **客户端策略不在 SRS 中**：通用旁路、出站 `direct`、`no-resolve` 等不能用域名收录情况证明等价。

这些差异不都等于维护遗漏。现有方案明确不采用整段 ASN 和宽泛关键词来扩大产品范围，也没有启用所有第三方遥测与候选域名。若后续需要补齐，应先确定目标是“逐条复刻所给配置”，还是“保留仓库当前的产品证据与地址方向约束”；这两种目标会产生不同的规则。

本次只新增本检查报告，未修改规则源、生成产物、启用策略或消费者配置，也未提交、推送或发布。
