# Net.Coffee Claude 清单与现有规则核对

> 本文保留修改前 `v0.1.4` 的核对结果。用户随后要求补齐除 NTP 外全部范围，更新结果见[补齐报告](net-coffee-claude-supplement-2026-10-15.md)。

核对日期：2026-10-15（Asia/Shanghai）。工作区：`sing-box-ai`；提交：`55b63a0`；本地版本：`v0.1.4`。

**没有全部包含，但网站列出的 7 个核心域名后缀全部覆盖。** 以网站主要配置的 19 条域名／关键词规则为口径，当前 Claude 规则为 **9 条完整覆盖、3 条部分覆盖、7 条未覆盖**。正文另列的 `sentry` 关键词也未纳入 Claude 规则；加入这一项后，整页去重后的域名／关键词要求为 **20 条：9 完整、3 部分、8 未覆盖**。

这里比较的是匹配范围，不是“必需功能缺失”的数量。网站混合了核心服务、共享第三方服务、IP 范围和 NTP 建议，其中部分技术解释不准确。**不建议仅凭这篇文章，把所有关键词和大网段直接补进规则。**

导航：[核对依据](#basis) · [19 条完整对照](#domains) · [正文其他项目](#extra) · [IP 与 ASN](#ip) · [网站可靠性](#quality) · [处理建议](#next) · [验证记录](#verification)

<a id="basis"></a>
## 核对依据与口径

网页来源：[Net.Coffee：Claude Code 域名分流规则大全](https://ip.net.coffee/claude/site.html)。网页的四种配置并不完全相同，本报告以类型前缀／YAML／JSON 中共同列出的 19 条域名与关键词为主表，另列正文、纯域名列表和兜底段的补充内容，避免漏项或重复计数。

本地依据：

- [Claude 发布 JSON](../artifacts/v0.1.4/anthropic.json) 与 [当前 Claude SRS](../dist/anthropic.srs)。
- [OpenAI 发布 JSON](../artifacts/v0.1.4/openai.json)，仅用于说明其他产品是否有相关覆盖。
- [Anthropic 来源 IP JSON](../artifacts/v0.1.4/anthropic-ip.json)。
- [启用策略](../sources/policy.yaml)、[Claude 补充源](../sources/anthropic.yaml)与[发布摘要](../artifacts/v0.1.4/SHA256SUMS)。

“完整”表示网页要求的匹配范围被包含；“部分”表示只收录其中具体主机或子网；“未覆盖”表示未在当前 Claude 输出中找到相应域名匹配。没有把域名临时解析出的 IP 当成长期域名覆盖。

本次检查的是仓库 `v0.1.4` 及本地 `dist/`，没有读取运行中客户端配置或流量。因此，不能由这份结果推断设备已加载哪个版本、命中哪条优先规则，或实际使用哪个出口。

<a id="domains"></a>
## 19 条域名／关键词完整对照

表中结论仅按 `anthropic.srs` 计算。后缀规则覆盖根域及子域；精确规则只覆盖该主机。

| # | 网页规则 | 当前 Claude 覆盖 | 依据或差异 |
|---|---|---|---|
| 1 | 后缀 `anthropic.com` | 完整 | 已有相同后缀。 |
| 2 | 后缀 `claude.ai` | 完整 | 已有相同后缀。 |
| 3 | 后缀 `claude.com` | 完整 | 已有相同后缀。 |
| 4 | 后缀 `clau.de` | 完整 | 已有相同后缀。 |
| 5 | 后缀 `claudemcpclient.com` | 完整 | 已有相同后缀。 |
| 6 | 后缀 `claudemcpcontent.com` | 完整 | 已有相同后缀。 |
| 7 | 后缀 `claudeusercontent.com` | 完整 | 已有相同后缀。 |
| 8 | 精确 `servd-anthropic-website.b-cdn.net` | 完整 | 已有相同精确主机。 |
| 9 | 精确 `anthropic.com.cdn.cloudflare.net` | 未覆盖 | 结尾是 `cloudflare.net`，不会命中 `anthropic.com` 后缀。 |
| 10 | 精确 `anthropic.auth0.com` | 未覆盖 | 不属于已有 Anthropic 后缀。 |
| 11 | 精确 `anthropic-com.ghost.io` | 未覆盖 | 当前输出没有相应主机。 |
| 12 | 后缀 `sentry.io` | 未覆盖 | Claude 集合没有；OpenAI 集合仅有两个精确主机。 |
| 13 | 后缀 `statsigapi.net` | 未覆盖 | 不等于 `statsig.anthropic.com`，也不等于 OpenAI 的 `oaistatsig.com`。 |
| 14 | 精确 `browser-intake-us5-datadoghq.com` | 完整 | 已启用，进入正式输出。 |
| 15 | 关键词 `datadog` | 部分 | 收录两个具体 Datadog 主机，没有任意字符串匹配。 |
| 16 | 关键词 `sift` | 未覆盖 | 没有该关键词或相关主机。 |
| 17 | 后缀 `intercom.io` | 部分 | 仅 `api-iam.intercom.io`、`widget.intercom.io`。 |
| 18 | 后缀 `intercomcdn.com` | 部分 | 仅 `js.intercomcdn.com`、`downloads.intercomcdn.com`。 |
| 19 | 精确 `cdn.usefathom.com` | 未覆盖 | 未进入当前输出。 |

**9 条完整 = 7 个核心后缀 + 1 个 CDN 精确主机 + 1 个遥测精确主机。**

当前 Claude 的两个 Datadog 精确主机是：

- `http-intake.logs.us5.datadoghq.com`
- `browser-intake-us5-datadoghq.com`

另有客服静态资源 `static.intercomassets.com`，不属于表中两个 Intercom 后缀。上述精确规则已经启用，不是仅登记在候选清单中。

如果理论上合并观察 OpenAI 与 Claude 两份集合，主表会变为 **9 条完整、4 条部分、6 条未覆盖**：变化仅是 `sentry.io` 从未覆盖变成部分覆盖，因为 OpenAI 有 `o207216.ingest.sentry.io` 和 `o33249.ingest.sentry.io`。

OpenAI 还有 `.intercom.io`、`.intercomcdn.com`。按本仓库固定 sing-box 的语义，带前导点的后缀覆盖子域，不覆盖裸域，故合并后仍不能称作网站整后缀范围已完整覆盖。语义约定见[项目方案](plan.md#inputs)。两份集合的理论并集也不代表客户端会给它们分配相同出口。

<a id="extra"></a>
## 正文与其他配置形式中的项目

| 项目 | 当前结果 | 说明 |
|---|---|---|
| `cdn.anthropic.com` | 完整 | 由 `anthropic.com` 后缀覆盖。 |
| `mcp.anthropic.com` | 完整 | 同上。 |
| `console.anthropic.com` | 完整 | 同上。 |
| `workbench.anthropic.com` | 完整 | 同上。 |
| 正文提到的 `api.anthropic.com` | 完整 | 同上，不需要重复精确列入。 |
| 关键词 `sentry` | 未覆盖 | 正文／底部兜底单列，未出现在主要配置中；范围比 `sentry.io` 后缀更大。 |
| `geosite:anthropic` | 有固定上游基线 | 本项目继承固定的 Anthropic geosite 基线；不是运行时解析该字符串，也不保证等同于任意第三方当前版本。 |
| `geosite:category-ntp` | 产品集合未提供 | 三个产品 JSON 没有 NTP 分类；实际客户端是否有通用 NTP 策略，本次未检查。 |
| `keyword:datadog`、`keyword:sift` | 已在主表计数 | 兜底段重复出现，不再重复统计。 |

纯域名列表把若干 CDN／认证主机也按后缀形式表达，而主要配置将其设为精确匹配。若严格采用那份纯列表的“所有子域也匹配”解释，`servd-anthropic-website.b-cdn.net` 在你的规则中也只能算精确主机覆盖，不能视为整个后缀覆盖。这也是不能把四种格式视为完全等价的原因。

<a id="ip"></a>
## IP 与 ASN 的差异

| 网页要求的目的范围 | 当前规则 | 判断 |
|---|---|---|
| `160.79.104.0/21` | Claude 目的 `160.79.104.0/23` | 部分：覆盖 `160.79.104.0`—`160.79.105.255`；未覆盖该 `/21` 中余下的 `160.79.106.0`—`160.79.111.255`。 |
| `2607:6bc0::/32` | Claude 目的 `2607:6bc0::/48`、`2607:6bc0:11::/48` | 部分：只有两个 `/48`，不是整个 `/32`。 |
| `AS399358` | 没有动态 ASN 匹配规则 | 当前三个目的前缀覆盖仓库 2026-10-09 的 RIS 观测快照，不能声称覆盖当前及未来全部公告。 |

独立 `anthropic-ip.srs` 的确包含 `160.79.104.0/21`，但字段是 **`source_ip_cidr`**，用于匹配来源 IP，不能计为上述目的范围已覆盖。[sing-box 字段定义](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/#source_ip_cidr)

本次重新打开的官方 IP 文档仍把 `160.79.104.0/23`、`2607:6bc0::/48` 列为接收访问的入口，把 `160.79.104.0/21` 列为 Anthropic 向外发起请求时使用的来源范围。因此，网站使用更大的目的范围是一种额外覆盖选择，不能由该官方文档推出其为客户端必需。[Claude 官方 IP 地址](https://platform.claude.com/docs/en/api/ip-addresses)

新增的 `2607:6bc0:11::/48` 是仓库已批准的网络覆盖补充，其依据与业务必需域名不同，见[v0.1.4 发布记录](evidence/release-v0.1.4/README.md)。本次未重新采集 ASN 公告。

<a id="quality"></a>
## 网站哪些判断可信，哪些需要纠正

### 1. 域名匹配边界的提醒有价值

`browser-intake-us5-datadoghq.com` 不是 `datadoghq.com` 的子域，单独写 `datadoghq.com` 后缀确实不会覆盖它。你的规则已经精确包含这个主机。类似地，`anthropic.com` 也不会覆盖 `anthropic.com.cdn.cloudflare.net`。

### 2. 共享关键词不是官方必需清单

当前 Claude Code 官方网络文档明确列出前述两个 Datadog 主机，并标为可选遥测／错误报告。你的规则已覆盖二者。官方未要求用 `datadog` 关键词匹配所有相关字符串，也未在当前网络要求中要求整段 `sentry.io`、`statsigapi.net` 或 `sift` 关键词。[官方网络要求](https://code.claude.com/docs/en/network-config#network-access-requirements)

这不能证明所有历史版本、Web、Desktop 或某个实验功能永远不会访问这些服务，但不足以把它们写成 Claude Code 的普遍必需依赖。官方也把遥测服务列为可选；本次查阅的一手资料没有支持“第三方出口不一致会触发风控”的具体因果判断。[官方数据使用与遥测](https://code.claude.com/docs/en/data-usage#telemetry-services)

### 3. NTP 返回地区时区的说法错误

NTP 同步的是 UTC 时间；本地时区和夏令时由系统另行处理。把 NTP 请求送到另一地区，不会因此把系统时区变成代理出口时区。网页据此提出的时区检测解释不成立，也没有给出 Claude Code 执行该检测的一手证据。[NTP 官方说明](https://www.ntp.org/documentation/4.2.8-series/warp/) · [RFC 5905 §4](https://www.rfc-editor.org/rfc/rfc5905.html#section-4)

### 4. 这不是所有产品、所有功能的穷尽清单

官方区分 CLI、Desktop 与 claude.ai 的网络依赖。你的现有规则还包括 `claude.app`、`claude.dev`，以及 `storage.googleapis.com`、`registry.npmjs.org`、GitHub、Homebrew 和多种前端资源主机；其中多项不在网站的精确清单中。不能用“与网站一模一样”作为覆盖完整性的唯一标准。[官方网络要求及产品差异](https://code.claude.com/docs/en/network-config)

<a id="next"></a>
## 处理建议

目前最合理的结论是：**核心后缀已齐；网站中有 10 条主要规则的范围没有完整复刻，但这不等于有 10 项必要功能漏配。**

优先核实尚未收录的四个具体主机：`anthropic.com.cdn.cloudflare.net`、`anthropic.auth0.com`、`anthropic-com.ghost.io`、`cdn.usefathom.com`。如果实际使用的 Claude 产品或官方页面出现对它们的请求，再按用途纳入精确匹配。本次没有取得足够证据把它们认定为当前必需依赖，也没有认定它们已经停用。

对于 Sentry、Statsig、Sift，先确定实际请求主机和用途。已验证的 Datadog、Intercom 精确主机可继续保留；仅为追求与网页一致而扩展整个共享后缀或关键词，会扩大到其他应用的流量。

不应依据网页的 NTP 时区论述新增规则，也不应把来源 `/21` 与客户端目的范围混用。若要判断“真实请求是否全部走指定出口”，需要另看客户端加载版本、DNS 与路由顺序以及请求记录；规则文件成员关系本身不能证明这一点。

<a id="verification"></a>
## 本次验证记录

| 验证项目 | 结果 |
|---|---|
| 当前版本与提交 | `VERSION=0.1.4`；`55b63a0`；检查开始时工作树干净。 |
| 发布摘要 | `artifacts/v0.1.4/SHA256SUMS` 的 9 个条目全部核对一致。 |
| 本地当前 SRS | `dist/` 三个 SRS 与 `artifacts/v0.1.4/` 对应 SRS 的 SHA-256 全部一致。 |
| 原生反编译 | 使用现有 sing-box `1.15.0-alpha.9`，三个 SRS 的反编译内容与发布 JSON 规范化后全部一致。规范化仅忽略数组顺序、单值／数组表示和单 IP 的 CIDR 表示差异。 |
| Claude 输出规模 | 21 个精确域名、9 个后缀、3 个目的 CIDR；没有 `domain_keyword`。 |
| 完整清单复核 | 19 条主规则已逐项核对，并由独立复核得到相同计数。 |
| 实际消费者 | 未核验在线加载、真实公网出口或登录／对话行为。 |
| 本轮变更 | 仅新增本报告；未修改规则、策略、发布产物或客户端配置。 |

当前 Claude SRS 的 SHA-256：

```text
a1952bbfe2cafb39cc89c8b3db0f1930f6a2ac029ebe7493463d6b5742488035
```

本报告以工作区真实 Markdown 文件交付；本地引用使用相对路径。没有公开上传本文，也没有将文件入口的存在描述为手机另存或下载已实测成功。
