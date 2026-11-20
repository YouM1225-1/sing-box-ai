# Claude 分流规则分析与重整

核对日期：2026-11-12（Asia/Shanghai）。比较对象：[one-exit 固定提交 b9d9f8a](https://github.com/wquguru/one-exit/commit/b9d9f8ab6687401f7588dfa7d7023cd58ffb4032)与本地 **sing-box-ai v0.1.12**。

**结论：当前 Claude 规则已经吸收了这次提交中多数值得保留的域名补充，不需要再整包照搬。现在更需要把产品域名、共享依赖、宽范围兼容项、目的 IP 和消费端策略分别说明。** 本文完成用途分类和完整清单重整，保留现有规则覆盖范围；没有修改发布制品、设备配置或发布新版本。

- 提交新增的 **17 条域名表达式**，当前 Claude 规则完整覆盖 **11 条**、部分覆盖 **6 条**，完全无对应服务覆盖为 **0 条**。部分覆盖主要来自关键词、根后缀与精确主机之间的范围差异。
- 提交后全部 **32 条域名表达式**，当前 Claude 规则完整覆盖 **17 条**、部分覆盖 **8 条**、无对应服务规则 **7 条**；后者主要是 Google、MCP 文档站和代理服务商等扩展场景。
- 两段 IPv6 `/48` 都已被当前 `/32` 匹配范围包含，但 **“匹配该 IP”不等于“拒绝 IPv6”**。拒绝、代理出口和 DNS 策略必须在消费端另行判断。

阅读导航：[提交含义](#commit) · [完整分类清单](#inventory) · [IP 方向](#ip) · [32 条逐项对照](#comparison) · [6 条部分覆盖是否要补](#partial-six) · [处理结论](#decisions) · [出口与优先级](#routing) · [验证和证据](#verification)

<a id="commit"></a>

## 1. 这次提交实际改变了什么

提交发生于 **2026-10-21 09:35:18（北京时间）**，修改 README、三个客户端模板及检查脚本。主要变化如下：

| 变化 | 含义 |
| --- | --- |
| 在域名规则前拒绝 `2607:6bc0::/48` 和 `2607:6bc0:11::/48` | 作者针对其住宅代理访问这些 IPv6 地址返回 502 的处理；不证明所有代理都存在此故障 |
| 补入支付、验证码、遥测与风控服务 | 将相关请求统一送往 `SG_Residential`，扩大固定出口的覆盖范围 |
| 增补 `claude`、`anthropic`、`browser-intake` 等关键词 | 减少部分主机漏配，也扩大了非 Claude 域名被匹配的范围 |
| 调整模板检查器 | 检查到的 IPv6 规则必须指向 REJECT；不是出口一致、业务成功或 IPv4 回退的实测 |

17 条指“在至少一个模板中新加的域名表达式”的去重并集。其中 `claude`、`anthropic` 在旧 FlClash 中已存在；按三个旧模板的并集计算，真正首次出现的是 15 条。Persona、Google 和 `modelcontextprotocol` 相关项也并非全部由本次提交新增。

三个模板并不完全相同：Clash Party 与 Shadowrocket 的提交后规则列表相同；FlClash 使用更多关键词，并保留 Claude、Google Play、Google Wallet 的三个进程/包名条件。FlClash 的 `pin.concat(config.rules || [])` 会把这些规则放在原规则前。完整并集为 **39 条：32 条域名、3 条 CIDR、1 条 ASN、3 条进程条件**。依据：[本次重新获取的提交和模板](evidence/claude-rules-reorganized-2026-11-12/upstream-fetch.json)、[逐条模板定位](evidence/one-exit-b9d9f8a-2026-10-21/extracted-template-rules.json)。

作者的目标是让 Claude、Google、Persona 等多类服务统一使用住宅出口。本仓库的 SRS 只保存匹配条件，两者职责不同；住宅节点是该模板的选择，不是 Claude 官方统一网络要求。

<a id="inventory"></a>

## 2. 当前规则的完整分类清单

本节逐项列出 v0.1.12 的 **48 条域名表达式**；第 3 节列出另外 **4 条目的 CIDR、2 条来源 CIDR**。用途分类用于阅读和维护，不把 SRS 拆成多个顶层规则，也不改写已批准条目的证据身份。

| 字段 | 数量 | 匹配范围 |
| --- | ---: | --- |
| `domain` | 23 | 仅所列主机 |
| `domain_suffix` | 22 | 本批均无前导点，覆盖根域及子域 |
| `domain_keyword` | 3 | 域名任意位置包含关键词 |
| `ip_cidr` | 4 | 目的地址，第 3 节列全 |
| `source_ip_cidr` | 2 | 独立的服务来源地址集合，第 3 节列全 |

证据身份沿用 [v0.1.12 manifest](../artifacts/v0.1.12/manifest.json) 和 [Anthropic 补充来源](../sources/anthropic.yaml)：社区基线、官方功能依赖、历史兼容项、用户指定项分别保留。“已收录”不等于“每次聊天必需”；同一主机被其他软件访问时，也会命中同一规则。

### 2.1 产品主域与内容：9 条后缀

```text
anthropic.com
clau.de
claude.ai
claude.app
claude.com
claude.dev
claudemcpclient.com
claudemcpcontent.com
claudeusercontent.com
```

`claude.app` 为官方网络依赖补充，其余 8 条来自固定社区产品基线。保留具体后缀，不扩成 `claude`、`anthropic` 任意位置关键词。`api.anthropic.com`、`portal.anthropic.com` 等子域已由 `anthropic.com` 覆盖，不必重复加入。

### 2.2 官网和身份服务扩展：4 条后缀

```text
anthropic-com.ghost.io
anthropic.auth0.com
anthropic.com.cdn.cloudflare.net
servd-anthropic-website.b-cdn.net
```

这些后缀范围属于历史用户指定补充，不扩成整个 `ghost.io`、`auth0.com`、`cloudflare.net` 或 `b-cdn.net`。其中 `servd-anthropic-website.b-cdn.net` 的精确主机也存在于社区基线，最终被同名后缀覆盖。

### 2.3 身份验证与验证码：3 条

| 类型 | 值 | 证据身份 |
| --- | --- | --- |
| 后缀 | `withpersona.com` | 官方身份验证功能的共享依赖 |
| 后缀 | `hcaptcha.com` | 用户指定共享服务 |
| 精确 | `challenges.cloudflare.com` | 历史兼容条目，保留原复核日期及本版例外 |

Claude 官方确认使用 Persona；Persona 官方网络清单中的主机及自定义子域均可由 `withpersona.com` 后缀覆盖。这里证明服务关系与域名范围，不证明任何一次验证失败的原因。[Claude 身份验证说明](https://support.claude.com/en/articles/14328960-identity-verification-on-claude)、[Persona 网络要求](https://docs.withpersona.com/security)

`challenges.cloudflare.com` 当前是精确主机，不能宣称覆盖 `a.challenges.cloudflare.com`；也不需要因此扩大成整个 `cloudflare.com`。

### 2.4 支付与结账：8 条

**6 条精确主机：**

```text
api.stripe.com
billing.stripe.com
checkout.stripe.com
js.stripe.com
m.stripe.com
r.stripe.com
```

**2 条后缀：**

```text
stripe.network
stripecdn.com
```

均沿用用户指定项身份。Stripe 官方案例确认 Anthropic 使用其订阅、支付和结账产品；上述 Stripe 主机也见于供应商域名清单，但这不构成逐主机的 Claude 运行抓包证据。[Stripe 的 Anthropic 案例](https://stripe.com/customers/anthropic)、[Stripe 域名清单](https://docs.stripe.com/ips#stripe-domains)

**当前没有整个 `stripe.com` 后缀。** 裸域以及 `buy.stripe.com` 等其他主机仍可能不命中本产品规则。进一步核对官方支付集成文档后，建议优先补强 `hooks.stripe.com` 和 `js.stripe.com` 子域范围，具体优先级与依据见[6 条部分覆盖是否要补](#partial-six)。需要整个 Stripe 统一出口时，应明确按共享支付服务扩大范围。

### 2.5 客服：3 条

```text
后缀：intercom.io
后缀：intercomcdn.com
精确：static.intercomassets.com
```

前两条为用户指定的共享后缀；最后一条是已启用的可选客服依赖。`api-iam.intercom.io`、`widget.intercom.io`、`js.intercomcdn.com`、`downloads.intercomcdn.com` 已被后缀覆盖；它们的原始官方依赖记录仍保留在 manifest 中，无需在最终规则重复出现。

### 2.6 遥测、实验与风控共享服务：7 条

```text
后缀：growthbook.io
后缀：segment.io
后缀：statsigapi.net
精确：cdn.usefathom.com
关键词：datadog
关键词：sentry
关键词：sift
```

全部沿用用户指定项身份，不能统一标成 Claude 核心必需。原本选中的两个 Datadog 精确遥测主机已经被 `datadog` 关键词覆盖。

三个关键词是当前较宽的匹配条件：`datadoghq.com`、`sentry.io`、`siftscience.com` 都已覆盖；`unrelated-sentry.invalid` 等仅含关键词的合成域名也会命中。此次还实测确认 `audit.datadog.pool.ntp.org` 命中。因此，“未单独添加 NTP 域名”不能写成“当前规则排除了 NTP”。如果日后需要缩小范围，应保留真实使用主机，再单独验证和发布范围变更。

`cdn.usefathom.com` 仍为精确匹配；不自动扩为整个 `usefathom.com`。

### 2.7 Artifacts 库与字体：7 条精确主机

```text
cdn.jsdelivr.net
cdn.tailwindcss.com
cdnjs.cloudflare.com
code.jquery.com
unpkg.com
fonts.googleapis.com
fonts.gstatic.com
```

前 5 条为所选 Artifacts 功能依赖；最后 2 条为已启用的可选字体依赖。这些是共享资源主机，匹配全部 URL 路径，不只匹配 Claude 页面发出的请求。

### 2.8 安装与插件：5 条精确主机

```text
formulae.brew.sh
github.com
raw.githubusercontent.com
registry.npmjs.org
storage.googleapis.com
```

沿用官方功能依赖身份：`formulae.brew.sh` 对应所选安装功能，其余 4 条对应所选插件功能。范围不等于整个 Homebrew、GitHub、npm 或 Google Cloud 生态，也不保证任意插件、用户 MCP 服务的网络需求均已覆盖。

### 2.9 推送候选保留：1 条精确主机

```text
fcmtoken.googleapis.com
```

来自用户指定截图条目；保留为共享主机，不升级成已证实的 Claude 普通聊天必需依赖。

### 2.10 可选外部集成：1 条精确主机

```text
api.revenuecat.com
```

v0.1.11 已按用户要求补入。此前证据对应 RevenueCat MCP/OAuth 的条件性集成，不能据此认定 Claude 自身订阅由 RevenueCat 处理，或默认客户端每次都会访问。详见[原关联审阅](loc-sens-claude-gaps-2026-11-10.md)；该历史文档中的“未覆盖”仅描述当时 v0.1.10，已由后续版本解决。

<a id="ip"></a>

## 3. IP 规则必须保留方向和范围依据

### 3.1 客户端目的地址：anthropic.srs 的全部 4 条

| 当前 `ip_cidr` | 范围依据 | 本次处理 |
| --- | --- | --- |
| `153.61.224.0/22` | 官方接收请求的 IPv4 地址，v0.1.12 新增 | 保留 |
| `160.79.104.0/21` | 用户指定较宽范围，包含官方目的 `160.79.104.0/23` | 保留原身份，不把整个 /21 标成官方目的清单 |
| `2607:6bc0::/32` | 用户指定较宽范围，包含官方目的 `2607:6bc0::/48` 和历史公告补充 `2607:6bc0:11::/48` | 保留匹配范围；不由此生成整个 /32 的拒绝动作 |
| `34.8.0.0/16` | 用户指定截图网段，登记为共享范围 | 保留；不宣称网段内所有地址都是 Claude 专用 |

本次在线核对的 [Anthropic 官方 IP 文档](https://platform.claude.com/docs/en/api/ip-addresses)仍列出两个目的 IPv4 前缀 `160.79.104.0/23`、`153.61.224.0/22`，以及目的 IPv6 `2607:6bc0::/48`。当前较宽 /21、/32 的额外部分来自本仓库既有策略，不应混淆。

one-exit 的 `160.79.104.0/21` 以及两个 `/48` 都被当前目的规则包含。无需为匹配范围再重复加 IP；`IP-ASN,399358` 是另一种依赖 ASN 数据库的条件，不能与这几条固定 CIDR 宣称永久等价。

### 3.2 服务对外请求的来源地址：anthropic-ip.srs 的全部 2 条

```text
source_ip_cidr: 160.79.104.0/21
source_ip_cidr: 153.61.208.0/20
```

它们用于识别 Anthropic 服务向外部服务发起请求时的来源，不是手机或电脑访问 Claude 的目的地址清单。`160.79.104.0/21` 在两个文件中出现时承担不同方向的职责；不要把来源集合并入客户端目的路由，也不要用匹配字段转换把其用途反转。来源识别本身不代替应用鉴权。[官方入站与出站地址说明](https://platform.claude.com/docs/en/api/ip-addresses)、[独立来源规则](../artifacts/v0.1.12/anthropic-ip.json)

<a id="comparison"></a>

## 4. one-exit 的 32 条域名表达式逐项对照

以下只比较 **当前 Anthropic 规则本身**，不借用 OpenAI 规则或其他订阅规则来补覆盖。“完整”依据整个匹配范围的包含关系；“部分”表示覆盖具体主机或子范围；“无对应”不排除某个合成子域偶然含现有关键词，也不意味着实际连接一定直连。

### 4.1 在至少一个模板中新加的 17 条

| one-exit 表达式 | 当前覆盖 | 整理后的处理 |
| --- | --- | --- |
| 关键词 `anthropic` | 部分 | 保留已有具体域名，不扩大为任意位置匹配 |
| 关键词 `claude` | 部分 | 同上 |
| 关键词 `browser-intake` | 部分 | 已覆盖有依据的 Datadog intake 主机；不覆盖任意供应商的同名模式 |
| 后缀 `claudemcpcontent.com` | 完整 | 保留，无需重复 |
| 后缀 `sentry.io` | 完整 | 已被 `sentry` 关键词包含 |
| 后缀 `datadoghq.com` | 完整 | 已被 `datadog` 关键词包含 |
| 后缀 `growthbook.io` | 完整 | v0.1.7 已补入 |
| 后缀 `usefathom.com` | 部分 | 当前仅精确 `cdn.usefathom.com` |
| 后缀 `hcaptcha.com` | 完整 | v0.1.7 已补入 |
| 后缀 `stripe.com` | 部分 | 当前 6 个精确主机，不等于根后缀 |
| 后缀 `stripe.network` | 完整 | v0.1.7 已补入 |
| 后缀 `stripecdn.com` | 完整 | v0.1.7 已补入 |
| 后缀 `intercom.io` | 完整 | 已覆盖根域及子域 |
| 后缀 `intercomcdn.com` | 完整 | 已覆盖根域及子域 |
| 后缀 `challenges.cloudflare.com` | 部分 | 当前精确主机已覆盖，子域未一并扩入 |
| 后缀 `siftscience.com` | 完整 | 已被 `sift` 关键词包含 |
| 后缀 `segment.io` | 完整 | v0.1.7 已补入 |

合计：完整 **11**、部分 **6**、无对应 **0**。其中部分覆盖不应直接表述为“还漏了 6 项必需依赖”。

<a id="partial-six"></a>

### 4.1.1 这 6 条具体是什么，哪些值得补

补充核对：2026-11-12。**建议其余 5 条维持现状，Stripe 优先补有明确用途的支付子范围；没有证据证明这 6 条必须全部扩成 one-exit 的完整范围。** “部分覆盖”是与对方表达式的范围比较，不是发现了 6 个实际连接故障。

| 原表达式 | 当前为什么算部分覆盖 | 是否补齐整条 |
| --- | --- | --- |
| `DOMAIN-KEYWORD,anthropic` | 已有 `anthropic.com`、特定 Auth0/CDN 等域名；没有匹配任意含该单词的第三方域名 | **不建议。** 有实际新主机时补域名，不加无限定关键词 |
| `DOMAIN-KEYWORD,claude` | 已覆盖 Claude 主域、内容域和其他已选后缀；未覆盖任意含 `claude` 的域名 | **不建议。** 关键词还会匹配无关站点，如合成示例 `claude-fan.example.org` |
| `DOMAIN-KEYWORD,browser-intake` | 现有 `datadog` 关键词覆盖已知 Datadog intake 主机；不覆盖不含 `datadog` 的任意同名模式 | **不建议。** Claude Code 官方列出的 `browser-intake-us5-datadoghq.com` 已覆盖，并被官方标为可选错误报告 |
| `DOMAIN-SUFFIX,challenges.cloudflare.com` | 已精确覆盖该主机，只缺它的子域范围 | **目前不需要。** Turnstile 官方脚本及 CSP 使用该精确主机，没有据此扩大所有子域的必要 |
| `DOMAIN-SUFFIX,usefathom.com` | 已覆盖 `cdn.usefathom.com`，未覆盖根域和其他子域 | **目前不需要。** 官方标准嵌入脚本就在现有 CDN 主机上；整个供应商网站不等于 Claude 必需依赖 |
| `DOMAIN-SUFFIX,stripe.com` | 已有 6 个精确主机，但支付集成还存在其他主机和脚本子域 | **优先补支付子范围；整域按需。** 更具体的建议见下表 |

以上必要性判断分别依据 [Claude Code 网络文档](https://code.claude.com/docs/en/network-config)、[Turnstile CSP](https://developers.cloudflare.com/turnstile/reference/content-security-policy/)、[Fathom 标准嵌入脚本](https://usefathom.com/docs/script/embed)。它们支持已知端点的用途与范围，不证明每个 Claude 会话都使用这些服务。

**Stripe 建议分两级补强：**

| 建议项 | 优先级与理由 | 当前状态 |
| --- | --- | --- |
| 增加精确 `hooks.stripe.com` | **优先。** Stripe.js 官方 frame-src 清单包含它；某些重定向支付方式（如可能涉及 3D Secure 的卡支付）明确需要它 | 本次原生匹配未命中 |
| 将精确 `js.stripe.com` 扩为同名后缀，覆盖根主机和其子域 | **兼容性补强。** 官方允许 `*.js.stripe.com` 承载不同来源的脚本和框架，并说明有性能优化用途；不能称为所有支付的硬性前提 | 根主机命中，合成子域样例 `audit.js.stripe.com` 未命中 |

依据：[Stripe.js 与支付重定向的官方 CSP 要求](https://docs.stripe.com/security/guide#content-security-policy)。Anthropic 使用 Stripe Elements 的服务关系已有[官方客户案例](https://stripe.com/customers/anthropic)支持；据此建议补强支付兼容性，但尚未从用户设备日志证实上述端点参与了具体一次付款。

如果目标是整个 Stripe 服务始终走同一出口，也可以选择 `domain_suffix: stripe.com`，它会一并覆盖上述两个缺口及其他 Stripe 主机，代价是其他网站访问 Stripe 的流量也会命中。这是更宽的共享支付策略，不是已被证实必须采用的 Claude 产品规则。即使补整个后缀，也不能保证覆盖 Link 钱包、银行验证等所有支付链路。

本轮新增 9 个域名原生匹配检查，结果见[补充核对证据](evidence/claude-rules-reorganized-2026-11-12/partial-scope-followup.json)。子域样例只验证匹配范围，不表示该合成域名真实存在。本轮只更新分析，没有执行上述规则变更。

### 4.2 其余 15 条既有表达式

| one-exit 表达式 | 当前覆盖 | 整理后的处理 |
| --- | --- | --- |
| 后缀 `claude.ai` | 完整 | 产品域名 |
| 后缀 `claude.com` | 完整 | 产品域名 |
| 后缀 `clau.de` | 完整 | 产品域名 |
| 后缀 `anthropic.com` | 完整 | 产品域名 |
| 后缀 `claudeusercontent.com` | 完整 | 产品内容域名 |
| 后缀 `modelcontextprotocol.io` | 无对应 | 文档/生态场景单列，不代表任意 MCP 服务器 |
| 关键词 `modelcontextprotocol` | 无对应 | 不新增宽关键词 |
| 后缀 `google.com` | 无对应 | Google 独立场景，不整体并入 Claude |
| 后缀 `googleapis.com` | 部分 | 已有 `fonts`、`storage`、`fcmtoken` 三个精确主机 |
| 后缀 `gstatic.com` | 部分 | 已有精确 `fonts.gstatic.com` |
| 后缀 `gmail.com` | 无对应 | Gmail 独立场景 |
| 后缀 `googleusercontent.com` | 无对应 | 不整体并入 Claude |
| 后缀 `recaptcha.net` | 无对应 | 依具体验证码流程再确认 |
| 后缀 `withpersona.com` | 完整 | v0.1.9 已补入身份验证依赖 |
| 后缀 `webshare.io` | 无对应 | 代理服务商/出口检查场景，不是 Claude 产品主域 |

合计：完整 **6**、部分 **2**、无对应 **7**。两表合计完整 **17**、部分 **8**、无对应 **7**，共 **32** 条。

当前规则也包含该提交没有显式列全的 Artifacts 库、安装插件、客服资源、`statsigapi.net` 等范围。不能用 one-exit 的较短模板替换当前规则后，仍声称原覆盖完整保留。

<a id="decisions"></a>

## 5. 重整后的处理结论

| 项目 | 结论 |
| --- | --- |
| Claude 主域、内容、Persona、现有精确支付主机 | 保留；旧报告中的相关缺项已由后续版本解决 |
| GrowthBook、hCaptcha、Segment、Stripe 两个资源后缀 | 保留用户指定身份，不重复加入，也不改标为官方必需 |
| `stripe.com`、`usefathom.com`、Challenge 的更宽后缀 | Stripe 优先考虑明确的支付子范围；其余维持当前精确范围，整域扩展需有具体需求 |
| `claude`、`anthropic`、`browser-intake`、`modelcontextprotocol` 关键词 | 本次不新增；具体域名比任意位置关键词更容易核对边界 |
| 现有 `datadog`、`sentry`、`sift` | 保留历史范围并标明广泛匹配；如需收紧，另做有明确增删清单的版本 |
| Google 全域、Gmail、Wallet、Webshare | 归入独立场景，不混成 Claude 默认依赖 |
| 两段 IPv6 REJECT、ASN 和进程匹配 | 属于消费端策略，另行验证适用性，不写成当前 SRS 已具备的行为 |
| 目的与来源 IP | 保持独立；新目的 `153.61.224.0/22` 与新来源 `153.61.208.0/20` 已在 v0.1.12 中分开处理 |

本次不需要仅为分类重整发布 v0.1.13。规则覆盖发生变化、复核过期项或客户端策略发生变化时，再按对应范围构建和验收。

另有两个应继续跟踪的历史复核项：`challenges.cloudflare.com` 的原复核期限为 2026-10-27，`2607:6bc0:11::/48` 公告补充的原复核期限为 2026-11-08。v0.1.12 按[该版保留条目例外](../sources/evidence/release-v0.1.12-preserved-entry-exception.json)继续沿用；本次域名/IP 匹配检查不刷新这些条目的业务或公告复核日期。

<a id="routing"></a>

## 6. 固定出口、DNS 与优先级如何理解

### 6.1 多个产品共用主机时，规则不会识别调用它的应用

`js.stripe.com`、`challenges.cloudflare.com`、`github.com`、`registry.npmjs.org` 等同时出现在本仓库 OpenAI 与 Claude 目的范围中。如果两个产品规则指向不同出口，先匹配到的路由会决定这些共享请求的路径，单凭域名不能知道是 Claude 还是 OpenAI 发起的。

如果要求这些服务都固定到同一个出口，消费端应把产品流量与选定共享依赖的路径安排一致；如果要求不同应用使用不同出口，需要有可验证的应用、设备或入站隔离条件。不能靠继续扩大域名列表解决归属冲突。上游的进程条件也不能直接照抄到所有平台：sing-box 的 `process_name` 适用于 Linux、Windows、macOS；Android 包名另有字段，iPhone 不能照搬 Android 条目。[sing-box 匹配字段](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/)

### 6.2 仅在需要故障规避时增加 IPv6 策略

one-exit 对两个 `/48` 采用 REJECT，是其作者针对特定住宅代理 502 的处理。以下三个结论不能从提交直接推出：

1. **`no-resolve` 不等于禁用 AAAA。** 它表示不为该目的 IP 规则额外触发解析，已有目的地址仍可被匹配。[Mihomo 路由参数](https://wiki.metacubex.one/config/rules/#no-resolve)
2. **REJECT 不保证应用改用 IPv4。** 它拒绝连接，后续是否重试取决于应用及连接路径；需要独立观察。[sing-box 拒绝动作](https://sing-box.sagernet.org/configuration/route/rule_action/#reject)
3. **本地拒绝规则不保证控制远端代理解析。** HTTP CONNECT 等路径如果将域名交给代理端解析，本地可能看不到最终 IPv6 目标；这是需要按实际代理链验证的条件。

若实际确认是 IPv6 路径故障，应结合解析位置、代理能力和客户端内核版本选择 DNS 或路由处理；只对被证实的范围采取措施，不把当前 `2607:6bc0::/32` 匹配项直接整体转换为拒绝规则。本文没有获取当前 iPhone/N100 生效配置，不给出可直接覆盖设备的片段。

### 6.3 消费端只做相对优先级核对

| 位置关系 | 核对内容 |
| --- | --- |
| 已有基础规则 | 保留必要的 DNS 劫持、嗅探及内网例外；不能照搬一个模板的置顶数组覆盖整个设计 |
| 明确的局部拒绝规则 | 如果确实启用，必须能在相关放行/代理规则之前获得匹配机会 |
| Claude 与选定共享依赖 | 在会抢先匹配它们的通用服务、地区或兜底规则之前处理；尊重已有明确直连例外 |
| DNS | 确认同一批域名落入预期解析路径；如果现有设计抑制代理域名的 AAAA/HTTPS/SVCB，新增域名也须保持覆盖一致 |
| 最终验收 | 检查首个有效规则、实际出站、DNS 和请求结果；SRS 单独命中不能替代这些证据 |

用途分类只改变阅读方式。仓库约定保持一个 default rule；拆成多个规则后，即使单独匹配结果看似相同，也不能据此断言在 DNS/路由组合中的消费行为完全等价。[现有规则形态契约](plan.md#inputs)

<a id="verification"></a>

## 7. 验证结果与交付边界

此次完成：

- 重新读取指定 GitHub commit 和三份模板；核对 Git blob SHA，且三份模板均与历史固定 SHA 归档逐字节一致。
- 本地 v0.1.12 的 JSON/SRS 与 manifest 哈希一致，`dist/` 三份 SRS 与对应版本归档一致。本次没有重新下载远端 Release，因此这里的当前基线特指本地 v0.1.12。
- 分类目录与实际目的 JSON 做集合相等检查：**52 项逐项覆盖、无重复、无遗漏**；另核对来源 CIDR **2 项**。
- 使用仓库固定的 sing-box 原生匹配代码和 Go 工具链，执行 **728 项检查，0 失败**：256 个域名样例的 JSON/SRS 各一次（512 项）、26 个 IP 样例的来源/目的方向及两个制品两种格式（208 项）、域名与目的 IP 的 OR 组合（8 项）。
- 运行前后对 114 个相关文件校验哈希，源规则、v0.1.12 归档、dist、生成脚本和既有方案文件保持不变。

这些检查证明本地制品匹配和清单整理正确，不证明当前设备已经加载对应版本，也不证明出口一致、IPv4 回退、支付或身份验证已成功。本次没有改变 N100、iPhone、UniFi 或系统网络设置。

| 制品 | SHA-256 |
| --- | --- |
| `anthropic.srs` | `19ba1228b9b664d1cff15b510e4b6c56e710e37c05aba6231c27c9efe6ac807b` |
| `anthropic-ip.srs` | `819dcba59e171957aff80c4ddf6c0dd9fd984620e2ee0a7f363deb879828261a` |

证据入口：

- [分类目录与逐项来源](evidence/claude-rules-reorganized-2026-11-12/inventory.json)：资料目录，不能直接当作 sing-box 配置加载。
- [本次覆盖统计与校验结果](evidence/claude-rules-reorganized-2026-11-12/audit-results.json)
- [原生用例](evidence/claude-rules-reorganized-2026-11-12/native-cases.json)及[逐项原生结果](evidence/claude-rules-reorganized-2026-11-12/native-results.jsonl)
- [本次在线取得的提交与模板](evidence/claude-rules-reorganized-2026-11-12/upstream-fetch.json)
- [可重跑的只读核对脚本](evidence/claude-rules-reorganized-2026-11-12/audit.py)：以现有本地固定批次为输入，只写核对证据和本地验证工具。
- [v0.1.12 目的 JSON](../artifacts/v0.1.12/anthropic.json)、[来源 JSON](../artifacts/v0.1.12/anthropic-ip.json)、[发布归档说明](evidence/release-v0.1.12/README.md)

历史报告继续保留其当时版本结论，不重写旧证据。需要查看当前 Claude 分类和 one-exit 差异时，以本文的 v0.1.12 基线为准。
