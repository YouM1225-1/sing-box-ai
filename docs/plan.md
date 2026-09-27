# sing-box-ai 正式方案

> 文档修订：**1.16**；核验日期：2026-09-28（Asia/Shanghai）。
> 主仓库：`YouM1225-1/sing-box-ai`；项目候选版本为 `0.1.0-rc.2`。
> 状态：本轮正在按本方案实现直接 SRS 基线导入、手动构建并同步客户端配置；新批次实机验收与正式发布门槛独立保留。现有 `v0.1.0-rc.1` 是旧实现的预发布。

适用任务：维护 OpenAI 与 Claude 的 sing-box 产品规则，在 **SagerNet/sing-geosite 完整产品 SRS 基线**上增加有依据的缺失域名和地址。本文是正式设计及当前执行计划，供规则维护、配置派生和验收使用，不是 N100 部署授权或可直接执行的安装脚本。

完成终点：固定输入、补充证据、生成器、校验器、manifest 和测试契约一致；生成并审阅同批次三个候选制品；仅对经过该批次验收的环境声明可用。规则集合完整性、消费者分流正确性和真实业务成功分别验收。

本轮授权包含规则仓库重构与 GitHub 同步、手动构建候选制品、仓库三端及 iCloud 派生配置修改和改动审计；不包含 N100 实机部署。禁止修改 N100 配置、重启/重载、切换模式/出站、关闭现有连接、清理缓存或改动防火墙与路由。保留四条产品路由原位置，也保留现有 DNS 顺序。仓库首页 README、Release 正文及发布身份的既有约定不变；候选构建不能标记为已完成正式发布验收。

阅读入口：[规则职责](#scope) → [固定输入与语义](#inputs) → [完整补充清单](#supplements) → [N100 配置与影响](#consumer) → [构建发布契约](#build) → [执行计划](#execution)。

<a id="scope"></a>
## 1. 输出与范围

| 制品 | 唯一职责 | 生成关系 |
|---|---|---|
| `dist/openai.srs` | OpenAI / ChatGPT / Codex 客户端目的规则 | 完整 `geosite-openai.srs` ∪ 缺失域名及官方 Voice 目的地址 |
| `dist/anthropic.srs` | Claude / Anthropic 客户端目的规则 | 完整 `geosite-anthropic.srs` ∪ 缺失域名及官方 inbound 目的地址 |
| `dist/anthropic-ip.srs` | Anthropic 服务出站请求的来源识别 | 独立官方 `source_ip_cidr: 160.79.104.0/21` |

产品 YAML 只维护补充层。不得抄写或筛选上游列表再声称完整继承。SRS 是实际构建输入，DLC 文本保留属性与行级来源并作等价旁证；不一致即停止批次，不改用文本替代 SRS。上游已有的 apex、后缀、正则、共享依赖和遥测分类均继承；社区归类不改标为官方逐项认可。若新基线含不支持结构或不可接受范围，停止采用整批新基线，保留上一受审版本，不静默裁剪。

默认设计范围包含 ChatGPT 网页/客户端、Codex、Voice，以及 Claude Web/API/Code/Desktop、Artifact 和官方所列安装/插件依赖。此范围是规则设计目标，不是所有平台都已验收的声明。第三方登录、支付跳转、用户 MCP、任意插件和外部网页不能由有限产品集合穷举；Realtime SIP 电话接入不属于本次默认范围；另选 Bedrock、Vertex 等 provider 时，须建立对应环境的独立需求，不加入整个云厂商后缀。

`anthropic-ip.srs` 不接入 N100 当前客户端路由或 Hysteria2 入站白名单，也不代替应用鉴权。两个目的集合及该来源集合都不得通过 `rule_set_ip_cidr_match_source` 改写用途。

<a id="inputs"></a>
## 2. 固定输入与版本

### 2.1 当前受审对象

| 对象 | 固定版本或内容 |
|---|---|
| SagerNet/sing-geosite 产品基线 | `e6a8117545c35a17c508e3f37a9a990571234428`；同一提交的两份 SRS |
| DLC 溯源文本 | `bcea25493ed28c387660fe49ce1ceb242d2efca0`；`data/openai`、`data/anthropic` |
| 实测运行时/编译器 | sing-box `v1.15.0-alpha.9`，`132b38e9caaba1a1959354d518e54d2d08419afe` |
| 对应 sing 依赖 | `v0.9.6-0.20260922013359-4ca3bebe0b8e` |
| 2026-09-28 查询所得 testing | `710d7c715b10cf9fc158b1ab7fd7198754962c59`；仅关键源码静态比对，未构建运行 |
| Voice 官方数据 | `chatgpt-voice.json`，23 个 IPv4 `/32`，无 IPv6；`creationTime=2026-03-26T20:12:45.451356+00:00` |

“最新”仅指上述核验时点。1.15 为预览系列；本方案不要求现网升级。格式可读不等于旧版消费者路由语义已验收。testing 的 11 个相关 sing-box 文件及 3 个 sing 依赖文件与 alpha.9 对应文件逐字节一致，支持本文涉及的匹配/编译静态结论；不能将 alpha.9 运行结果记成 testing 实测。

固定输入摘要：

| 输入 | 字节数 / SHA-256 |
|---|---|
| `geosite-openai.srs` | 451 / `aae1fede5b274089b027668ee5d073221332f283ef29f943e8aeaf12261067d1` |
| `geosite-anthropic.srs` | 167 / `aaca1f727c8ca51690d2c81358b9541c8f6c356d5c9a45b2b7da23658a70d906` |
| OpenAI Voice JSON | `8f03f3c594165eeff009915c7e2beb4bdfb9d429fb1955c205e3b33ec781899a` |
| alpha.9 Darwin arm64 编译器 | `fcb47f341e6660a35385ceeffc0cebb2daca3fed4d35c729b7d45f7b66555f9a` |

两份原始 SRS 均为 binary v1，alpha.9 原生反编译成功：OpenAI 为 9 exact、13 root suffix、1 regex；Anthropic 为 1 exact、7 root suffix；均无 IP。反编译结果与固定 DLC 文本逐字段等价核对。v1 不是损坏或必须换源的理由。`domain:x` 与 `domain_suffix:.x` 可等价表示为 `domain_suffix:x`；这种形态变化不代表丢失规则。

原始 SRS 字节、许可证及溯源材料须归档。`rule-set` 分支可能重建；完整 Git SHA 不保证对象永久可取。联网更新发现新对象后先固定、归档和审阅，离线构建仅用登记输入，禁止依赖浮动分支、`latest` 或未登记缓存。

### 2.2 匹配与输出结构

`dist/` 仅用于通过正式发布门槛的发行；本轮手动候选交付在 `artifacts/v0.1.0-rc.2/`，沿用相同三个文件名，不写入正式 dist，也不创建新 Release。

三个输出分别固定为 **source JSON version 2、恰好一条非 invert 的 default rule、binary v2**。目的制品只用 `domain`、`domain_suffix`、`domain_regex`、`ip_cidr`；来源制品只用 `source_ip_cidr`。禁止空规则、未知字段和未经审阅的 logical 结构。

| 写法 | apex `example.com` | 一层/多层子域 | `notexample.com` |
|---|---:|---:|---:|
| `domain: example.com` | 命中 | 不命中 | 不命中 |
| `domain_suffix: .example.com` | 不命中 | 命中 | 不命中 |
| `domain_suffix: example.com` | 命中 | 命中 | 不命中 |

官方 `*.x` 补充映射为 `.x`，不额外扩到 apex；基线本来包含 apex 时完整保留。补充域名规范为小写 IDNA ASCII；末尾根点处理须记录，不能假定所有实际消费者自动执行同样转换。regex 原文保留，使用 Go RE2，不能仅凭首尾锚点证明范围安全。

同一 default 中目的域名与目的 IP 属于同组 OR；来源与目的属于不同组 AND。顶层多规则虽按 OR，**不能由独立匹配等价推导消费者组合等价**：1.15 对可合并的单条 default 和多规则集合走不同消费路径。官方 `TestRuleSetShapeBoundary` 有反例。附加目的条件若要求 AND，应放在 logical-and 的独立子规则，不与 `rule_set` 放在同一 default 中期待 AND。

混合 SRS 的业务路由匹配结果如下（仅目的组，未加其他限制）：

| 域名条件 | 目的 IP 条件 | 集合匹配 |
|---|---|---|
| 命中 | 未命中或未提供 | 命中 |
| 未命中或未提供 | 命中 | 命中 |
| 命中 | 命中 | 命中 |
| 均未命中/未提供 | 均未命中/未提供 | 不命中 |

本轮真实编译的混合 SRS 已覆盖域名单独、IP 单独、联合及负例；不要求同时具备域名和 IP。

DNS 普通查询初始化时通常没有可供匹配的目的地址；当前 AI 查询规则主要靠域名命中。显式 `evaluate → match_response` 可以检查应答 IP，包括 domain+IP 单 default。不得概括为“DNS 总是忽略 ip_cidr”。

alpha.9 存在新旧两条 DNS 路径。`defaultRuleDisablesLegacyDNSMode` 把 `query_type`、`evaluate`、`respond`、`match_response` 等列为关闭 legacy 的条件；当前三端配置具备这些条件，`Exchange` 进入 `exchangeWithRules → walkDNSRules → currentRule.Match`，没有含 IP 集合跳过非地址查询的条件。报告引用的 `WithAddressLimit() && !isAddressQuery` 位于 `matchDNS`，属于 `exchangeLegacy` 调用链，不能套用当前配置。仅刻意构造的 legacy 配置中，含目的 CIDR 的引用会跳过 TXT/SVCB/MX/CNAME；A/AAAA/HTTPS 为其地址查询类别。本轮加入两个模式的正反对照，不为旧路径问题改动现有 DNS 顺序。

固定生成器把支持字段的基线与补充作语义并集，再编译：**v1 输入 → 经校验的 v2 源表示 → 固定编译器 → v2 输出**。`rule-set merge` 拼接 rules 数组，不承担这个单规则合并；不得拼接二进制。compile 对更高源格式有条件降级，v1 不会自动升为 v2。检查 `SRS\x02` 后仍须完整解析，而非只看 magic。

<a id="supplements"></a>
## 3. 完整补充清单

本节列出的都是相对 §2 固定基线的缺口，不是相对旧仓库或 rc.1 的新增差异。已有范围不会重复维护一套人工基础列表。补充层默认 `enabled_optional: []`；该开关不删基线已有项。

### 3.1 OpenAI

以下均由当前 OpenAI 官方网络页列出，按产品网络依赖纳入；共享主机/后缀须在维护数据标记 `shared_dependency: true`，其匹配不局限于 ChatGPT 发起的请求。

**3 个仅子域后缀**：

```text
.ct.sendgrid.net
.intercom.io
.intercomcdn.com
```

**11 个精确主机**：

```text
cdn.openaimerge.com
cdn.workos.com
challenges.cloudflare.com
forwarder.workos.com
humb.apple.com
images.workoscdn.com
js.stripe.com
o207216.ingest.sentry.io
rum.browser-intake-datadoghq.com
setup.workos.com
workos.imgix.net
```

**23 个 Voice 目的地址**（`ip_cidr`；Voice 功能必需）：

```text
102.37.57.54/32
13.71.25.29/32
135.220.40.201/32
172.203.39.49/32
172.207.173.200/32
172.214.226.198/32
191.233.251.27/32
20.162.96.163/32
20.168.48.117/32
20.184.36.134/32
20.203.144.245/32
20.74.221.21/32
4.151.200.38/32
4.155.146.196/32
4.197.172.116/32
4.217.235.100/32
4.245.198.13/32
40.118.236.137/32
51.4.112.173/32
52.143.181.161/32
68.155.152.41/32
72.146.20.246/32
74.248.148.7/32
```

官方 Voice 首选 UDP 3478，受限时回落 TCP 443；本规则的 `ip_cidr` 本身不限端口，属于目的分流，不是端口防火墙。每次来源同步及候选构建前检查 Voice 字节、`creationTime` 和地址集合变化，变化必须进入 semantic diff。读取失败或解析得到空表时停止更新，不能以旧内容冒充新抓取结果；固定历史输入仍可离线重建。现有定时 CI 只做发现与候选校验，不自动采纳来源、提交配置或发布；本轮交付制品由本机手动构建。

当前官方主清单为 **29 项：9 个通配域、20 个 exact**。上述 3+11 补充与完整基线联合覆盖它们；`js.intercomcdn.com` 已由补充 `.intercomcdn.com` 覆盖。`auth.openai.com`、`chatgpt.com`、`openai.com`、`ws.chatgpt.com` 也在基线内。官方注明 ChatGPT WebSocket 为 `wss://ws.chatgpt.com`、Codex 为 `wss://chatgpt.com/`，消费者还需允许 TCP443 升级及持续连接；匹配成功不证明长连接成功。

当前原文未列公共 Statsig 家族，仍列 `*.oaistatsig.com`。旧仓库同时有维护者观察记录，不仅是旧网页/社区来源；这些证据可登记待验证候选，不自动变为当前官方必需项。这仅说明本次页面内容，不能写成永久停用。App Attest 出现在 iOS 排障段，并非主清单强制项，处置见 §4。

### 3.2 Claude / Anthropic 目的补充

**1 个 root suffix**（apex 与子域）：

```text
claude.app
```

**10 个官方功能依赖 exact**：

```text
cdnjs.cloudflare.com
cdn.jsdelivr.net
cdn.tailwindcss.com
code.jquery.com
unpkg.com
github.com
raw.githubusercontent.com
registry.npmjs.org
storage.googleapis.com
formulae.brew.sh
```

前五项为 Artifact 库 CDN；官方未提供库回退，不能和可回退字体一并省略。其余按安装、更新、插件及 Homebrew 路径记录 `features`。这些是共享基础设施，按域名分流会影响其他软件的相同请求；exact `github.com` 不覆盖 `api.github.com` 等子域。

**1 个已经批准的历史兼容 exact**：

```text
challenges.cloudflare.com
```

该项继续为 `compatibility-critical`、`review_status: approved`。维护者明确表示此前已验证，并指定“旧仓库更新日期就是验证日期”。对应旧仓库提交 `1f6e61caa9f8c157771e2e48a9084ded3cb4caa2` 的日期为 2026-09-27；提交只定位用户指定日期，不独立证明运行结果。记录的 `first_seen/last_verified=2026-09-27`、`review_after=2026-10-27` 保留。环境、精确客户端及版本未知，仍为 null；产品标签是兼容项范围，不是逐客户端认证。

`user-confirmation` 支持这条历史兼容项的保留资格；**不代替新制品的登录、Challenge 或实际出口验收**。没有理由因新批次尚未验收就抹掉历史批准。OpenAI 有官方依据也不能自动转为 Claude 官方依据；两份产品分别保留其来源。

**2 段官方 inbound 目的地址**：

```text
160.79.104.0/23
2607:6bc0::/48
```

IPv6 目的前缀保留在集合中；N100 产品路由的 IPv6 reject 是消费者策略，两者职责不同。

### 3.3 独立 Anthropic 来源地址

`anthropic-ip.srs` 只有以下来源规则：

```json
{
  "version": 2,
  "rules": [{"source_ip_cidr": ["160.79.104.0/21"]}]
}
```

不得改为客户端目的 `/21`。以下官方已 phased-out 地址，清空其他域名条件后作为三个制品的来源/目的负例：

```text
34.162.46.92/32
34.162.102.82/32
34.162.136.91/32
34.162.142.92/32
34.162.183.95/32
```

### 3.4 已继承内容与覆盖边界

`clau.de`、`claudemcpclient.com`、`servd-anthropic-website.b-cdn.net`、Claude 内容/MCP 后缀，以及 OpenAI 的 `chat.com`、LiveKit 三段后缀、`sora.com`、`crixet.com`、`chatgpt.site`、基线静态主机和遥测项均继承社区基线，不再手工“补回”或要求它们满足本地兼容项 30 天复核。完整基线不因此等于厂商认可的最小网络白名单。

OpenAI 基线 regex 原样继承：

```text
^chatgpt-async-webps-prod-\S+-\d+\.webpubsub\.azure\.com$
```

`\S+` 可以跨标签；测试其原语言，不擅自改窄，也不据此允许整个 `webpubsub.azure.com`。当前基线中的 `o33249.ingest.sentry.io` 为 exact，不要和旧补充的 US 主机混淆。

### 3.5 是否增加独立 IP 规则集

**结论：保留官方目的 IP 补充，但本次不增加第四、第五个目的 IP 制品。** 当前 `openai.srs` 已并入 23 个 Voice `/32`，`anthropic.srs` 已并入官方目的 `/23` 与 `/48`。它们和域名同属目的组 OR：没有域名元数据时，只要实际目的 IP 命中前缀，集合仍能命中；仍受消费者更早规则与内核旁路影响。

| 选择 | 覆盖与代价 | 决策 |
|---|---|---|
| 目的 IP 并入既有产品 SRS | 两个现有 tag 即可同时消费域名/IP，沿用原 IPv6 reject 和 proxy 位置 | 本次采用 |
| 另建 `openai-destination-ip.srs` / `anthropic-destination-ip.srs` | 不增加这些已包含 CIDR 的覆盖；需要新增引用、缓存和批次一致性管理 | 当前不采用 |
| 把 `anthropic-ip.srs` 的 `/21` 用作客户端目的 | 混淆官方 inbound/outbound，扩大目的范围 | 禁止 |
| 导入整个 ASN、Cloudflare/Azure/AWS 地址或批量固化 DNS 结果 | 共享基础设施和动态地址无法证明专属于产品，误分流范围扩大 | 不采用 |

只有消费者明确需要对目的 IP 采用独立端口、协议或出站策略，才值得单独设计文件，并重新验收组合语义。若把 IPv6 `/48` 从主集合移出，却只把新 tag 加到 proxy 而未覆盖原 IPv6 reject，会改变当前拒绝策略；若两个文件重复保留，只是重复覆盖。拆分也不能让 DNS 查询提前获得目的 IP，或收回 TUN 内核旁路流量。manifest 可按域名/IP 分项列数量和来源，无需为审核拆文件。

OpenAI Voice 是用途明确的客户端目的地址数据；OpenAI 爬虫/代理访问或 connectors/agents 的出站 IP 是 OpenAI 访问客户服务时的来源，不是 ChatGPT 登录目的地址清单。Anthropic inbound 两段与 outbound `/21` 同样必须分开。对 ChatGPT/Claude 网页认证、共享 CDN 未取得可替代域名规则的完整官方目的 IP 清单，不据此抓取一批当前解析 IP 宣称补全。

本轮还核对了现有 IP 规则仓库，不能只按文件名采用：

- SagerNet `sing-geoip` 本次完整 rule-set 树（`7fe82a879ad2666526730c195b55a6d8d9147908`）没有 OpenAI/Anthropic/Claude 专用项。`geoip-ai.srs` 的 `ai` 是安圭拉地区代码，不是人工智能服务；不得把它作为 AI 产品集合。
- KaringX 的 `geo/geoip/openai.srs` 本次样本含 253 个 CIDR，与 Chocolate4U/Iran-sing-box-rules 对应文件字节相同；追溯生成来源最终读取 `chatgpt-user.json`、`searchbot.json`、`gptbot.json`。这是 OpenAI 访问外站的来源集合，不进入本方案客户端目的分流。其文件名不能改变地址方向。
- OpenAI 另有 Realtime SIP 专用媒体目的段：`13.79.45.80/28`、`23.98.140.64/28`、`40.67.149.176/28`、`40.83.204.240/28`。本次未启用 SIP，不混入 ChatGPT Voice 默认补集；以后明确启用时，按该功能当前官方文档单独评估媒体、信令与端口需求，不能把这四段理解为完整 Realtime 网络清单。

## 4. 未加入项的处置

| 项目 | 当前依据和默认处置 | 进入补充层所需依据 |
|---|---|---|
| `register.appattest.apple.com` | 官方 iOS 排障用；不额外纳入默认产品集合 | 对应 iOS 场景的依赖及分流必要性，排除仅诊断探针 |
| `api.statsig.com`、`statsigapi.net`、`events.statsigapi.net`、`featuregates.org`、`prodregistryv2.org`、`featureassets.org` 及旧 `.statsig.com` | 当前 OpenAI 主清单未列；部分主机另有旧仓库维护者观察记录，连同旧副本/社区发现登记 pending | 当前官方明确列出，或对应产品自然会话的请求与功能证据；供应商域名文档本身不证明 ChatGPT 使用 |
| `client-api.arkoselabs.com`、`openai-api.arkoselabs.com` | 旧仓库有；rc.1 和新审阅集合均未含，不能称 rc.1→新批次退出 | 当前认证链路的精确主机及功能证据；不扩整个 Arkose |
| `cdn.growthbook.io` | 旧候选；当前 Claude Code 功能开关通过已覆盖的 `api.anthropic.com` 获取 | 对应产品当前使用此外部 CDN 的证据；不能把 GrowthBook 一概视为无用遥测 |
| `cdn.usefathom.com` | 社区/旧规则候选 | 明确产品用途及保留必要性；仅观察到请求不足以证明功能必需 |
| `o33249.ingest.us.sentry.io` | 旧 OpenAI 候选；不是 `o1158394.ingest.us.sentry.io` | 当前 OpenAI 官方列出或适用的产品证据 |
| `openai-prod.azureedge.net`、`openaicom-api.azureedge.net`、`modelcontextprotocol.io` | 历史发现，无新增批准 | 当前产品/功能用途及受控范围证据 |
| `fonts.googleapis.com`、`fonts.gstatic.com`、Claude 两个 Datadog 主机、Gerrit | 官方可选，基线外默认不额外加入 | 显式选择功能/可选项，固定 manifest 并验收；不因此删基线已覆盖内容 |
| Stripe 其他支付主机、Google/Apple/Microsoft IdP、任意插件/MCP | 未完成对应真实链路验收；不等于已证明业务缺陷，也不等于无其他路由 | 具体使用场景的依赖、首次命中、会话与出口证据，优先 exact；已有通用规则可满足时无需产品补充 |

Issue、社区规则及一次抓包用于发现，不直接批准。已对照 blackmatrix7 的 OpenAI/Claude 文件；其 Statsig、Arkose、Fathom 可作候选，不整体并入共享后缀、关键词或 ASN。人工补充禁止 `domain_keyword`、公共后缀、整个云/CDN 父域、默认路由 CIDR、瞬时 DNS 地址和错误方向。官方明确列出的共享通配范围须逐项登记，不类推扩张。

补充类别为 `required`、`feature-required`、`optional`、`compatibility`、`compatibility-critical`。前两类必须覆盖已声明功能；optional 默认不额外加入。兼容候选状态仅 `pending/approved`，维护 `value/type/product/direction/status/sources/reason/shared_dependency`，功能依赖另列 `features`；兼容项另列 `evidence/first_seen/last_verified/review_after/review_status`。

兼容批准接受有定位信息的真实运行证据；明确维护者确认仅可按固定首次批准锚点用于首次批准。运行证据需日期、环境、版本、方法及结果；确认记录原话、规则、产品、日期来源及已知限制。纯历史收录或一次请求观察不能自动批准。日期为带引号的 UTC `YYYY-MM-DD`；从未验证的 pending 两个复核日期为 null。保留的 approved 满足：

```text
first_seen <= last_verified <= review_as_of < review_after <= last_verified + 30天
```

首次确认锚点在 policy 中固定原 evidence 路径、SHA 和批准日。该条目的首次窗口保留；后续 last_verified 前移必须有新 runtime-validation，包含环境、客户端版本、方法、结果、实际观测及验证日期，不能改原确认日期或新写一份简短陈述续期。元数据验证不能证明证据真实性，维护者仍须审阅。

30 天是项目维护窗口；到期 UTC 当日 00:00 阻断新发布，不能只顺延日期。条目删除/替换须绑定审阅理由及受影响测试；关键兼容项还需替代覆盖或移除后的核心流程证据。不能通过删除、降级或跨产品套用批准消除门槛；旧运行批次不因日历变化自动删除。

<a id="consumer"></a>
## 5. N100 接入与实际分流

### 5.1 保留位置，使用同批次内嵌规则

当前 canonical 单源为系统安装仓库的 `5.sing-box/1.配置文件/config.json` 及配置契约。N100 实机仍引用旧仓库远程规则，本轮不部署。仓库 canonical 的 AWS/AWS-CN 等既有修改保留，不从现场回灌，也不把旧审核整份配置覆盖当前文件。

**本次仓库与 iCloud 接入选择 `type: inline`**：仅将既有 `geosite-openai`、`geosite-anthropic` 两个规则集对象改为内嵌同批次生成源 JSON 的完整 `rules`；这与本批次 SRS 具有相同单 default 结构和匹配语义。不手工另维护一份域名列表，不新增 tag、IP 制品或规则位置。最终校验同时比较三端/iCloud 内嵌内容与构建输入、源 JSON、SRS 反编译语义。

选择理由是跨平台启动可用性：alpha.9 的远程规则缓存按 tag 保存且记录 URLHash。更换固定 commit URL 时，带有不同 URLHash 的旧缓存不会被加载；如果没有可读的 `initial_path`，会在启动时执行首次抓取，失败可使服务启动失败。旧缓存条目是否带 URLHash 不能仅凭运行时间推定，需要实际证据。`initial_path` 可以提供本地初始字节，但路径不存在或内容错误仍会失败，且运行时不按项目发布 SHA 自动校验该文件。

Linux 的本地种子文件方案只有在文件已经按批次分发、权限与摘要核对后才成立；本轮禁止向 N100 分发文件。iOS/TV 配置导入也不能保证一个 Linux 路径或 iCloud 同目录路径能被 App 沙盒读取。因此不将未验证的 `initial_path` 加进三端公共配置。原生 inline 规则无需这两份规则的启动下载，适合本轮只修改仓库/iCloud的约束；它不解决其他既有 remote 集合的冷启动依赖。

代价：这两个产品集合不会自行远程更新；每次采用新规则批次须重新派生并同步配置，设备还需实际加载。固定 commit URL 本来也需要逐批改配置，inline 增加的是受控内容体积，换取明确启动输入。若未来明确要求后台更新，应另行验收各平台本地种子、冷启动、URLHash、缓存与恢复；不能简单换成 mutable main/latest 掩盖加载的是哪一批。

其他远程集合继续继承实际 `proxy-http` 下载链及其现有来源；`geosite-ai` 不变。**route.rules 与 dns.rules 的对象、内容和顺序均保留**，原 DNS 前移建议不属于接入步骤。

四条产品路由继续位于 Google/YouTube 后、通用 `geosite-ai` 前，实际对象如下：

```json
[
  {"rule_set": "geosite-openai", "ip_version": 6, "action": "reject", "no_drop": true},
  {"rule_set": "geosite-openai", "outbound": "proxy"},
  {"rule_set": "geosite-anthropic", "ip_version": 6, "action": "reject", "no_drop": true},
  {"rule_set": "geosite-anthropic", "outbound": "proxy"}
]
```

保留现有 QUIC 规则，不加 AI 专用 QUIC reject。SRS 或 inline 都只是集合；AAAA 空应答/IPv6 reject 来自消费者规则，受模式、更早命中及内核旁路影响，不代表所有 LAN 请求均由产品规则接管。

以后若授权 N100 部署，须以新鲜现场为基准核对受授权差异，不能顺带部署尚未批准的其他 canonical 修改。远程方案回退旧 URL 不保证能恢复旧缓存：新成功抓取可能已经覆盖同 tag 缓存。恢复必须使用已核对的原有效规则内容及配置，不能只假定旧 URL 对应字节仍在 cache.db。本次仅更新文件，不执行这些现场操作。

### 5.2 共有依赖与首次命中

以下是本机回环合成 DNS 实测及条件路由推导。旧指归档旧仓库字节，不是 N100 活动缓存导出；索引从 0 开始，只用于固定观测配置。真实部署按对象定位。

| 范围 | Rule 模式下的新审阅集合行为 | 迁移解释 |
|---|---|---|
| `auth.openai.com`、`chatgpt.com`、`claude.ai`、Challenge、WorkOS、Stripe JS、补充 JS CDN、npm、GitHub apex、raw GitHub 等 | DNS A 首中 16，AAAA 首中 15 并空应答；条件路由命中产品 proxy / IPv6 reject | 所测主机在旧仓库与 rc.1 已具有该策略，不能全部记为本次新增影响 |
| `storage.googleapis.com` | DNS A/AAAA 首中 14/13；条件路由 Google 19/18 | Google 更早；AAAA 已为空，不由产品补充首次改变 |
| `humb.apple.com` | DNS A/AAAA 首中 12；条件路由 Apple 15/proxy，v6 同样先命中 | 合成 AAAA 保留，是“全部产品域禁 IPv6”说法的反例 |
| `api.github.com`、`codeload.github.com`、`objects.githubusercontent.com` | DNS 17、条件路由通用集合 25/proxy；合成 AAAA 保留 | `github.com` exact 不扩子域；不在产品集合仍可经其他规则代理 |
| 两个 Arkose 主机及三个共享根域 `ct.sendgrid.net`、`intercom.io`、`intercomcdn.com` | 不再有旧产品空 AAAA，所测条件下由 DNS 19 evaluate 后续处理；条件路由 final/proxy | 旧仓库→新集合有变化；rc.1→新集合所测结果不变。三条点后缀仍覆盖子域，不含根域 |
| `login.live.com`、`login.microsoftonline.com` | 本次样本条件下 DNS 19、条件路由 final/proxy | 不在产品集合不等于无路由；真实 IdP 会话出口未验收 |

本轮补齐实际旧 SRS 的完整退出范围，逐条处理 102 条旧规则，并用 157 个原生见证核对。完整差异见[迁移清单](../sources/evidence/legacy-to-rc2-coverage.json)。不得用旧 YAML 代替旧 SRS；两者内容并不完全一致。

| 旧产品集合退出范围 | 新批次默认处置与消费者影响 |
|---|---|
| OpenAI 11 个 exact：`client-api.arkoselabs.com`、`openai-api.arkoselabs.com`、`events.statsigapi.net`、`statsigapi.net`、`featureassets.org`、`prodregistryv2.org`、`o33249.ingest.us.sentry.io`、`openai-prod.azureedge.net`、`openaicom-api.azureedge.net`、`itunes.apple.com`、`register.appattest.apple.com` | 登记待验证；Apple 两项仍先由 Apple 规则处理，其余所测条件不再由产品规则空 AAAA |
| OpenAI 3 个 apex：`ct.sendgrid.net`、`intercom.io`、`intercomcdn.com` | 当前官方通配仅支持子域；子域保留，三个 apex 待验证 |
| Claude 6 个 exact：`browser-intake-us5-datadoghq.com`、`http-intake.logs.us5.datadoghq.com`、`cdn.growthbook.io`、`cdn.usefathom.com`、`fonts.googleapis.com`、`fonts.gstatic.com` | Datadog/字体属于官方可选，默认不补；GrowthBook/Fathom 待验证。字体仍先由 Google 规则处理 |
| Claude root suffix `modelcontextprotocol.io` 与全部子域 | 登记待验证；整段语言退出，不能只登记 apex |
| Claude regex `^[a-z0-9-]+-review\.googlesource\.com$` 的完整匹配范围 | 官方可选，默认不补；本次见证先命中 Google，不改变其已有策略 |

27 个退出/边界见证 × 旧/rc.1/新候选 × A/AAAA 共 **162 次回环查询**，另有 **837 次原生会员断言**；候选与 rc.1 在此矩阵无变化。原先只测部分主机的表格不能当作完整迁移结论。`itunes.apple.com` 首中 DNS 11/route 14 direct；`register.appattest.apple.com` 为 DNS 12/route 15 proxy。其余未被前序集合接管的退出见证，旧 AAAA 在 15 空应答，新规则进入 19 evaluate 并取得合成 IPv6，应明确视为策略差异。正则和后缀的无限范围由结构记录，有限样本不等于全集证明。

Direct / Global 模式有更早规则，仍可能越过产品限制。路由表假定 Rule 模式、域名元数据可用、普通 TCP443，且无更早私网/协议/IP 规则或内核旁路；它是条件推导，不是 TUN 或真实出口实测。[消费者证据与最小复现](evidence/round3/consumer/README.md)区分原配置观测、最小机制 fixture 及真实业务验收。

共享域名一旦按产品规则匹配，会影响任何访问该域名的应用；SRS 不知道请求属于哪款软件。保持顺序可以保留现有较早分类，但不能保证零副作用。N100 的内核 GeoIP-CN 旁路先于用户态；移动规则不能收回已旁路流量。客户端→VPS 使用 IPv4，也不能证明 VPS→业务服务为 IPv4。

### 5.3 OpenAI / Claude Challenge 处理

两个目的集合都保留 exact `challenges.cloudflare.com`，经现有 `proxy` 策略处理；不得扩大为整个 Cloudflare。目标是避免遗漏验证依赖和非预期会话出口变化，不能承诺消除正常人机验证。

同一 `proxy` 标签不证明最终公网源 IP 一致；节点选择、DNS、地址族、VPS 上游和客户端代理覆盖都可能影响实际路径。正常会话验收记录主站、认证、Challenge 的实际可观测路径、地址族、出口及结果；单个“查 IP”网站仅证明该查询自身。Cloudflare 明确挑战签发与解答 IP 不一致可能导致无效/循环，但截图本身不能证明根因就是 IPv6。

如自然出现验证，由用户正常完成；不自动解题或反复触发登录。没有出现验证时只能登记“未触发”，不能记该路径通过。若网络路径符合预期仍循环，按 OpenAI 官方排障检查客户端时间、Cookies/JavaScript、扩展、DNS/过滤器、支持地区与服务状态；不靠随机扩域或轮换出口解决。可控目标是依赖可达、路径稳定、证据可定位。

<a id="build"></a>
## 6. 构建、验证与发布契约

### 6.1 最小实现改造

保留现有 `sources/`、`scripts/`、`tests/`、`dist/` 布局，不创建第二套生成链。产品 YAML 缩为补充层；固定 SRS 读取器导入完整基线，canonical 视图为“基线∪有资格补充”。同步更新 sync、generate、validate、manifest schema 和回归。

1. 固定同一提交的两份 SRS，归档原始字节、许可证及 DLC 旁证；固定官方网络事实记录/机器数据快照。
2. 原生解析完整输入。仅接受已审字段和单 default 结构；未知结构、方向、语法、无法接受的范围均停止该批次。DLC 对照不一致先定位差异，不改用文本静默替换 SRS。
3. 先判断补充是否已被基线覆盖，再并集。等价消重保留 provenance；基线 `@ads` 等属性只作旁证，不充当过滤器。
4. 分别输出基线增删、补充增删、exact/后缀/regex/CIDR 变化、方向、覆盖关系、来源及批准状态变化。旧仓库、rc.1、目标新批次分别标明，不能混用比较基准。
5. 写隔离批次目录，不直接覆盖 dist。候选 `build_mode: candidate` 可包含明确选定的 pending 项用于验收，但格式、范围、来源和日期合法性仍必须通过；不得作为正式部署品。
6. 获批后以 `build_mode: release` 重建并复核实际 UTC 日期。如果只有证据元数据改变且最终 SRS 与已验收候选逐字节一致，可关联原验收；任何制品变化重验受影响范围。

上述流程已实现于 `scripts/common.py`、`sync.py`、`generate.py`、`validate.py`。manifest schema 为 2；记录原始基线与解码语义摘要、完整 provenance、选项、补充证据及工具链。新候选版本为 `0.1.0-rc.2`；设计修订号不冒充软件升级。

### 6.2 快照与可复现要求

官方快照保留可审阅的网络事实或机器数据及 `url/retrieved_at/method/page_updated/sha256`，并让结构化事实逐项定位原文；原文响应摘要与事实记录文件自身摘要分别登记。正常 HTTP、官方检索正文、维护者保存均可；验证页、空文档、抽取失败必须停止更新。工具抽取文本明确不是原始 HTML。页面只有相对 Updated 时原样记录，绝对日期为 null；不能推算一个精确日期。同一导出时间不自动证明伪造，但不得冒充逐页抓取时间。

本轮已重新取得 OpenAI 网络页完整工具正文，复查 Claude 网络/桌面/IP 官方页面和 Voice JSON。OpenAI 原文显示 `Updated: last month`；公共 Statsig 未列争议按当前正文闭合。对外受版本控制输入保存完整网络事实、逐项原文定位、取得时间/方式及原文摘要；完整解释性页面仅留本地审阅，不将未获再分发许可的整篇网页公开复制。Voice 机器数据及上游基线原件归档，公开事实记录不冒称原始 HTML。

manifest 记录 schema、项目版本、source_commit、全部构建输入哈希、基线 repo/ref/path/hash、补充输入及证据、编译器平台与 SHA、固定 Go/sing-box/sing 依赖、features、enabled_optional、review_as_of、build_mode、三个源/二进制摘要与大小、binary_version=2、单 default 结构、验证结果和重建证据。`source_commit` 指已存在的输入提交，不自引用尚未产生的发布提交。

至少两次独立干净重建输出字节一致。工具链、依赖和输入全部锁定；离线复现不得暗中联网取新材料。新 v2 输出不要求和上游 v1 字节相同。最终集合通过支持字段保留、受限等价规范化和两侧匹配保证基线不丢失；有限见证例不能证明任意正则全集等价。未知结构阻断，不扩大比较器能力来掩盖差异。

### 6.3 必须通过的测试

| 层级 | 判据 |
|---|---|
| 输入与结构 | 真实解析 SRS；哈希/版本/字段/方向正确；基线完整，补充可追溯；拒绝空制品、未知字段、错误方向及超范围数据 |
| 域名边界 | exact、点后缀、root suffix 的 apex/一层/多层/近似域/错误父域；原始 regex 语言与反例；不以宽匹配追求用例数 |
| IP 方向 | `/23` 内目的命中，`/21` 内而 `/23` 外目的不命中；对应来源命中独立来源制品；两个地址族与五个 phased-out 负例 |
| 组合语义 | source/二进制一致；最终单 default 与外层条件的组合；目的域名+目的 IP、来源与目的、元数据重置；不以独立 OR 等价代替消费者测试 |
| DNS | 真实目标版本的查询/响应阶段，Rule/Direct/Global，旧/新首次命中、resolver、A/AAAA；合成测试与真实 DNS 分开 |
| 元数据反例 | pending/缺字段/未来日期/到期前后/超过窗口/跨产品证据/旧 review_as_of；历史重建可以通过但当前发布仍拒绝过期 |
| 重建 | 两次干净构建一致，完整 manifest 可追溯；同输入得到不同字节时停止发布 |
| 目标消费者 | 实际加载字节、原始配置 check、接管路径、实际出口、登录/长连接及已声明功能、适用的启动与重启持久化 |

`rule-set match -f binary` 仅给目的 IP 或域名赋值，不设置 Source；命中信息在 stderr，未命中通常也退出 0。先查执行错误，再判定匹配输出。来源方向必须用固定模块 harness 的 Source/Destination 独立输入测试，每例新建或正确重置 metadata。

### 6.4 发布门槛与失败处理

既有 `release-review.json` 保持 pending，直到新批次具备真实且绑定摘要的审阅材料。现有 release gate 不只检查该状态，还检查 release 模式、当前复核日期、输入提交/哈希、semantic diff、三个制品摘要和集成证据。仅把 pending 改 approved 不足以放行；规则历史批准不等于发布批准。

门槛包含基线直接输入和完整性核对。所有源、结构、范围、重建及消费者检查通过，semantic diff 被审阅，无 unresolved official conflict，才可发布。集成记录列明平台/版本/环境/方法/地址族/消费者配置摘要/实际出口和结果，并绑定本批次 SRS。声明支持的 OpenAI 登录、Claude 登录、Challenge、稳定出口、DNS、Voice、Artifacts、插件、启动、重启、消费者组合均须有适用证据；未验收功能不能标 passed 或写进 validated_consumers。

无真实会话条件时停留候选；不为通过门槛强迫用户反复验证。N100 的重启持久化本轮禁止测试，保留为后续维护窗口事项，不能写成失败或通过。审阅记录只是可追溯资料，不是证据真实性的密码学证明，维护者仍需核验内容。

源提交准备、两个干净构建、隔离回归和批次验收依次完成，再把三个 SRS 与 manifest 放入同一发布提交。首次接入须先确认原有效配置及旧 SRS 可恢复、当前配置漂移已登记、目标版本检查通过。本轮授权手动构建及仓库同步；正式 Release 发布与设备部署仍需完成相应验收及对应授权。失败保留原运行输入，不清空 cache.db、不盲重载、不覆盖上一批准批次。关键域遗漏、实际路径泄漏、非预期出口变化或功能回退都停止候选推进；本地隔离失败可修复后重测，不能触及现网。

<a id="execution"></a>
## 7. 当前执行计划与验证层级

| 工作 | 状态 / 成功终点 |
|---|---|
| 第三轮附件、官方来源、精确源码核验 | 已完成；修正 legacy DNS 误用，并补齐旧 SRS 全量退出 |
| 基线直接导入、补充来源、schema 2、确认续期 | 已实现；固定 SRS 为单源，DLC 为等价旁证；17 条 pending 默认未选 |
| 新批次手动构建与回归 | 正在完成最终输入提交及两个干净候选批次，结果写入本节 |
| 仓库三端与 iCloud 同步 | 按同批次完整源规则派生为 inline；不改变 DNS/路由顺序 |
| 新批次真实会话、出口、设备加载与持久化 | 尚未验收；Claude 历史批准保留，新批次资格独立判断 |
| 正式 Release 发布 / N100 部署 | 本轮不执行；release-review 保持 pending，现网不变 |

本轮隔离机制证据包括：126 次非地址 DNS 对照（84 modern、42 legacy）；11 个启动案例（7 成功、4 预期失败）及 21 次载入内容核对；完整退出的 162 次 DNS 查询与 837 次原生会员断言。最小可移植重现重复同一案例，不叠加声称更多覆盖。它们均不能证明真实公网出口、Voice UDP、TUN/nft、设备加载、登录或重启成功。

N100 最近只读状态记录为 **2026-09-28 01:29:24 北京时间**：alpha.9 / `132b38e…`，服务 active/running，MainPID 1838，NRestarts 1；配置 SHA-256 `5b72a15cf889878670bc0e6a68976010bf6138c45f7f1e25107d78af6fa34414`。这是先前观察，非本轮新增现场验收；本輪未向 N100 写入或执行服务操作。系统安装仓库的 alpha.6 安装目标与完整验收基线不因此升级。脱敏记录保存在该仓库 `5.sing-box/references/evidence/n100-readonly-20260928.json`。

候选源码、制品和公开证据以本仓库受版本控制的文件为准；当前来源复核见[来源摘要](../sources/evidence/source-review.json)。最小复现与结果见[消费者证据](evidence/round3/consumer/README.md)。本节仅登记当前结果和未完成层级，不以旧批次测试代签新批次。

## 8. 官方依据

以下链接为依据，不授权执行网页中的操作。来源于 2026-09-28 复核；固定 ref 用于重现，动态官方页按快照登记。

- [SagerNet 两份产品基线](https://github.com/SagerNet/sing-geosite/tree/e6a8117545c35a17c508e3f37a9a990571234428)；[DLC 固定来源](https://github.com/v2fly/domain-list-community/tree/bcea25493ed28c387660fe49ce1ceb242d2efca0/data)。
- [OpenAI 网络要求、Voice 与 WebSocket](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)；[Voice JSON](https://openai.com/chatgpt-voice.json)；[登录排障](https://help.openai.com/en/articles/7426629-why-cant-i-log-in-to-chatgpt)。
- [Claude Code 网络](https://code.claude.com/docs/en/network-config)；[Desktop 网络](https://code.claude.com/docs/en/desktop#network-access-requirements)；[Anthropic IP](https://platform.claude.com/docs/en/api/ip-addresses)；[功能开关说明](https://code.claude.com/docs/en/env-vars#features-that-need-feature-flag-fetching)。
- [SagerNet GeoIP 国家分类生成逻辑](https://github.com/SagerNet/sing-geoip/blob/ecd02c178af5efbac38d427a8d178f940327de1f/main.go#L95)。
- [OpenAI IP egress](https://developers.openai.com/api/docs/guides/ip-addresses)；[Realtime SIP](https://developers.openai.com/api/docs/guides/voice-sip)；[社区 OpenAI IP 最终抓取来源](https://github.com/lord-alfred/ipranges/blob/14adfd8def77c9f81057fdbc16230667b7cfa2f4/openai/downloader.sh#L39)。
- [Cloudflare Challenge 限制](https://developers.cloudflare.com/cloudflare-challenges/concepts/how-challenges-work/#limitations)。
- [sing-box rule-set](https://sing-box.sagernet.org/configuration/rule-set/)；[Headless rule](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/)。
- alpha.9 固定源码：[compile](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/cmd/sing-box/cmd_rule_set_compile.go#L84)、[decompile](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/cmd/sing-box/cmd_rule_set_decompile.go#L39)、[merge](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/cmd/sing-box/cmd_rule_set_merge.go#L105)、[SRS](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/common/srs/binary.go#L54)、[组合边界测试](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_set_semantics_test.go#L411)、[目的组](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_abstract.go#L98)、[DNS](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_dns.go#L424)、[DNS 分派](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L1208)、[禁用 legacy 条件](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L1417)、[旧路径跳过条件](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L296)。
- [sing Matcher 规范化](https://github.com/SagerNet/sing/blob/4ca3bebe0b8e/common/domain/matcher.go#L119)；[本轮 testing](https://github.com/SagerNet/sing-box/tree/710d7c715b10cf9fc158b1ab7fd7198754962c59)。
- 社区发现旁证：[blackmatrix OpenAI](https://github.com/blackmatrix7/ios_rule_script/blob/0fa60782abfe70f58da510e90d9086136cf0d855/rule/Clash/OpenAI/OpenAI.list)、[Claude](https://github.com/blackmatrix7/ios_rule_script/blob/0fa60782abfe70f58da510e90d9086136cf0d855/rule/Clash/Claude/Claude.list)。仅用于发现候选，不作为官方批准或新的基础输入。
