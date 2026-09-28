# sing-box-ai 正式方案

> 文档修订：**1.21**；核验日期：2026-09-28（Asia/Shanghai）。
> 主仓库：`YouM1225-1/sing-box-ai`；正式构建版本 `0.1.1`，`dist/` 已更新；GitHub 发布进度见 §7。
> 当前任务：提交受审输入、手动重建、核验后上传 GitHub 正式 Release 并更新 Latest；不访问或操作 N100。

适用任务：维护 OpenAI 与 Claude 的 sing-box 产品规则，在 **SagerNet/sing-geosite 完整产品 SRS 基线**上增加有依据的缺失域名和地址。本文是正式设计及当前执行计划，供规则维护、配置派生和验收使用，不是 N100 部署授权或可直接执行的安装脚本。

完成终点：固定输入、补充证据、生成器、校验器、manifest 和测试契约一致；构建并审阅同批次三个制品，按授权发布静态发行；仅对经过该批次运行验收的环境声明可用。规则集合完整性、消费者分流正确性和真实业务成功分别验收。

本次新增授权为手动构建并发布 `0.1.1`；范围为已验收的四个 OpenAI Codex 安装 exact 和两个 Anthropic 字体 optional。保留产品路由及 DNS 原位置，现有配置与 iCloud 不改；不访问或修改 N100，不重启/重载，不改系统 DNS、路由或防火墙。新发布授权与语义审阅单独绑定 `0.1.1` 的指定摘要，旧批准不沿用。更新 Latest 后在线订阅者可能自动下载新规则，这不代表 N100 已接受或完成运行验收。

阅读入口：[规则职责](#scope) → [固定输入与语义](#inputs) → [完整补充清单](#supplements) → [N100 配置与影响](#consumer) → [构建发布契约](#build) → [执行计划](#execution)。

<a id="scope"></a>
## 1. 输出与范围

| 制品 | 唯一职责 | 生成关系 |
|---|---|---|
| `dist/openai.srs` | OpenAI / ChatGPT / Codex 客户端目的规则 | 完整 `geosite-openai.srs` ∪ 缺失域名及官方 Voice 目的地址 |
| `dist/anthropic.srs` | Claude / Anthropic 客户端目的规则 | 完整 `geosite-anthropic.srs` ∪ 缺失域名及官方 inbound 目的地址 |
| `dist/anthropic-ip.srs` | Anthropic 服务出站请求的来源识别 | 独立官方 `source_ip_cidr: 160.79.104.0/21` |

产品 YAML 只维护补充层。不得抄写或筛选上游列表再声称完整继承。SRS 是实际构建输入，DLC 文本保留属性与行级来源并作等价旁证；不一致即停止批次，不改用文本替代 SRS。上游已有的 apex、后缀、正则、共享依赖和遥测分类均继承；社区归类不改标为官方逐项认可。若新基线含不支持结构或不可接受范围，停止采用整批新基线，保留上一受审版本，不静默裁剪。

默认设计范围包含 ChatGPT 网页/客户端、Codex 运行及选定 `codex-install` 安装路径、Voice，以及 Claude Web/API/Code/Desktop、Artifacts（含所选 Google Fonts）和官方所列安装/插件依赖。此范围是规则设计目标，不是所有平台都已验收的声明。第三方登录、支付跳转、用户 MCP、任意插件和外部网页不能由有限产品集合穷举；Realtime SIP 电话接入不属于本次默认范围；另选 Bedrock、Vertex 等 provider 时，须建立对应环境的独立需求，不加入整个云厂商后缀。

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

`dist/` 仅存通过静态制品发布门槛的三个发行 SRS；已通过静态发布门槛并更新为 `v0.1.1`。`artifacts/v0.1.1-rc.1/` 保留本地候选及其原始验收身份。`artifacts/v0.1.0-rc.2/` 保留其受摘要绑定的候选对照证据，不冒充 GitHub 已有 Release。

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

此前固定 alpha.9 原生核查的混合 SRS 已覆盖域名单独、IP 单独、联合及负例；不要求同时具备域名和 IP。

DNS 普通查询初始化时通常没有可供匹配的目的地址；当前 AI 查询规则主要靠域名命中。显式 `evaluate → match_response` 可以检查应答 IP，包括 domain+IP 单 default。不得概括为“DNS 总是忽略 ip_cidr”。

alpha.9 存在新旧两条 DNS 路径。`defaultRuleDisablesLegacyDNSMode` 把 `query_type`、`evaluate`、`respond`、`match_response` 等列为关闭 legacy 的条件；当前三端配置具备这些条件，`Exchange` 进入 `exchangeWithRules → walkDNSRules → currentRule.Match`，没有含 IP 集合跳过非地址查询的条件。报告引用的 `WithAddressLimit() && !isAddressQuery` 位于 `matchDNS`，属于 `exchangeLegacy` 调用链，不能套用当前配置。仅刻意构造的 legacy 配置中，含目的 CIDR 的引用会跳过 TXT/SVCB/MX/CNAME；A/AAAA/HTTPS 为其地址查询类别。此前固定批次已加入两个模式的正反对照，不为旧路径问题改动现有 DNS 顺序。

固定生成器把支持字段的基线与补充作语义并集，再编译：**v1 输入 → 经校验的 v2 源表示 → 固定编译器 → v2 输出**。`rule-set merge` 拼接 rules 数组，不承担这个单规则合并；不得拼接二进制。compile 对更高源格式有条件降级，v1 不会自动升为 v2。检查 `SRS\x02` 后仍须完整解析，而非只看 magic。

<a id="supplements"></a>
## 3. 完整补充清单

本节列出的都是相对 §2 固定基线的缺口，不是相对旧仓库或 rc.1 的新增差异。已有范围不会重复维护一套人工基础列表。`0.1.1` 的 `enabled_optional` 只包含 `fonts.googleapis.com`、`fonts.gstatic.com`；五个 optional 的源身份不变。该开关不删基线已有项，17 条 pending 仍全部未选。

### 3.1 OpenAI

下述 3 个点后缀和 11 个网络依赖 exact 来自已归档的 OpenAI 官方网络页，按产品网络依赖纳入；共享主机/后缀须在维护数据标记 `shared_dependency: true`，其匹配不局限于 ChatGPT 发起的请求。

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

**4 个 Codex 安装 exact**（本版新增；`feature-required`、`features: [codex-install]`、共享依赖）：

```text
github.com
api.github.com
release-assets.githubusercontent.com
registry.npmjs.org
```

官方固定安装器明确使用 GitHub API/Release；官方 Release 资产的实际跳转补足资产主机证据；官方 npm 安装说明与主包/平台包元数据补足 registry 证据。三类来源分别归档，不虚构官方统一 allowlist。`releases.openai.com` 已由基线覆盖。

选定范围为独立安装器默认源、显式 GitHub、主源失败的 GitHub 回退与官方 npm 安装。Homebrew 全生态、第三方镜像和任意工具依赖不包含在该承诺内。exact 主机会影响其全部 URL 路径，不能只识别 Codex 仓库或 npm 包；不得扩成整个 GitHub、npm 或云厂商后缀。`codex-install` 必须在 policy 声明，缺失时校验失败，不会静默省略这些条目。

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

固定官方事实清单为 **29 项：9 个通配域、20 个 exact**；2026-09-28 后续正文请求曾 HTTP 403，不能称本候选重新取得最新动态清单。上述 3+11 补充与完整基线联合覆盖它们；`js.intercomcdn.com` 已由补充 `.intercomcdn.com` 覆盖。`auth.openai.com`、`chatgpt.com`、`openai.com`、`ws.chatgpt.com` 也在基线内。官方注明 ChatGPT WebSocket 为 `wss://ws.chatgpt.com`、Codex 为 `wss://chatgpt.com/`，消费者还需允许 TCP443 升级及持续连接；匹配成功不证明长连接成功。

已归档原文未列公共 Statsig 家族，仍列 `*.oaistatsig.com`。旧仓库同时有维护者观察记录，不仅是旧网页/社区来源；这些证据可登记待验证候选，不自动变为当前官方必需项。这仅说明固定页面内容，不能写成永久停用；Statsig 供应商当前文档和 SDK 已确认相关候选现行，但不能代替 ChatGPT 使用证据。App Attest 出现在 iOS 排障段，并非主清单强制项，处置见 §4。

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

**2 个已选 optional exact**（源身份仍 optional）：

```text
fonts.googleapis.com
fonts.gstatic.com
```

两项一起选择，为既定 Desktop/Artifacts 字体功能提供产品集合覆盖。先前 CSS/实际字体资源经 Google 规则可达，不是已证实的当前字体故障；现在主动减少对通用 Google 集合的依赖。其余两个 Datadog 主机和 Gerrit regex 保持 optional 且未选，不删除完整基线已有的统计/遥测条目。

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

2026-09-28 基线审阅曾核对以下 IP 规则仓库，不能只按文件名采用：

- SagerNet `sing-geoip` 固定完整 rule-set 树（`7fe82a879ad2666526730c195b55a6d8d9147908`）没有 OpenAI/Anthropic/Claude 专用项。`geoip-ai.srs` 的 `ai` 是安圭拉地区代码，不是人工智能服务；不得把它作为 AI 产品集合。
- KaringX 的 `geo/geoip/openai.srs` 该批样本含 253 个 CIDR，与 Chocolate4U/Iran-sing-box-rules 对应文件字节相同；追溯生成来源最终读取 `chatgpt-user.json`、`searchbot.json`、`gptbot.json`。这是 OpenAI 访问外站的来源集合，不进入本方案客户端目的分流。其文件名不能改变地址方向。
- OpenAI 另有 Realtime SIP 专用媒体目的段：`13.79.45.80/28`、`23.98.140.64/28`、`40.67.149.176/28`、`40.83.204.240/28`。本次未启用 SIP，不混入 ChatGPT Voice 默认补集；以后明确启用时，按该功能当前官方文档单独评估媒体、信令与端口需求，不能把这四段理解为完整 Realtime 网络清单。

## 4. 未加入项的处置

| 项目 | 当前依据和默认处置 | 进入补充层所需依据 |
|---|---|---|
| `register.appattest.apple.com` | Apple 平台验证及网站 Touch ID/Face ID 依赖；不额外纳入产品集合 | 对应产品的真实请求与分流必要性；现有 Apple 前置规则不因加入 AI 被覆盖 |
| `api.statsig.com`、`statsigapi.net`、`events.statsigapi.net`、`featuregates.org`、`prodregistryv2.org`、`featureassets.org` 及旧 `.statsig.com` | 当前 OpenAI 主清单未列；部分主机另有旧仓库维护者观察记录。`events.statsigapi.net`、`statsigapi.net`、`featureassets.org`、`prodregistryv2.org` 已登记 pending；其余三项仅为待审阅发现线索，不在当前17条 registry 中 | 当前官方明确列出，或对应产品自然会话的请求与功能证据；供应商域名文档本身不证明 ChatGPT 使用 |
| `client-api.arkoselabs.com`、`openai-api.arkoselabs.com` | 旧仓库有；rc.1 和新审阅集合均未含，不能称 rc.1→新批次退出 | 当前认证链路的精确主机及功能证据；不扩整个 Arkose |
| `cdn.growthbook.io` | 供应商 SDK 现行端点，当前 Claude 使用仍待证实；已覆盖 `api.anthropic.com` 不证明所有 GrowthBook 用途均不存在 | 对应产品当前使用此外部 CDN 的证据；不能把 GrowthBook 一概视为无用遥测 |
| `cdn.usefathom.com` | 供应商当前统计脚本主机，当前 Claude 使用待证实 | 明确产品用途及保留必要性；仅观察到请求不足以证明功能必需 |
| `o33249.ingest.us.sentry.io` | 旧 OpenAI 候选；不是 `o1158394.ingest.us.sentry.io` | 当前 OpenAI 官方列出或适用的产品证据 |
| `openai-prod.azureedge.net`、`openaicom-api.azureedge.net` | 2026-09-28 两路 DNS 观测均 NXDOMAIN，标记历史候选而非永久退役 | 当前产品用途、恢复解析及受控范围证据 |
| `modelcontextprotocol.io`（后缀） | 文档站可达不等于 Anthropic 客户端运行必需 | 当前产品/功能用途及受控范围证据 |
| `fonts.googleapis.com`、`fonts.gstatic.com` | 已选 optional，纳入本候选 | 来源身份保持；单集与原序消费者验收 |
| Claude 两个 Datadog 主机、Gerrit regex | 官方可选，保持未选 | 显式选择功能/可选项，固定 manifest 并验收；不因此删基线已覆盖内容 |
| Stripe 其他支付主机、Google/Apple/Microsoft IdP、任意插件/MCP | 未完成对应真实链路验收；不等于已证明业务缺陷，也不等于无其他路由 | 具体使用场景的依赖、首次命中、会话与出口证据，优先 exact；可达不单独决定是否收录，需明确该选定功能是否承担独立产品覆盖责任 |

Issue、社区规则及一次抓包用于发现，不直接批准。已对照 blackmatrix7 的 OpenAI/Claude 文件；其 Statsig、Arkose、Fathom 可作候选，不整体并入共享后缀、关键词或 ASN。人工补充禁止 `domain_keyword`、公共后缀、整个云/CDN 父域、默认路由 CIDR、瞬时 DNS 地址和错误方向。官方明确列出的共享通配范围须逐项登记，不类推扩张。

补充类别为 `required`、`feature-required`、`optional`、`compatibility`、`compatibility-critical`。前两类必须覆盖已声明功能；optional 仅按 policy 的原始规范值显式选中；当前选择两条字体。兼容候选状态仅 `pending/approved`，维护 `value/type/product/direction/status/sources/reason/shared_dependency`，功能依赖另列 `features`；兼容项另列 `evidence/first_seen/last_verified/review_after/review_status`。

兼容批准接受有定位信息的真实运行证据；明确维护者确认仅可按固定首次批准锚点用于首次批准。运行证据需日期、环境、版本、方法及结果；确认记录原话、规则、产品、日期来源及已知限制。纯历史收录或一次请求观察不能自动批准。日期为带引号的 UTC `YYYY-MM-DD`；从未验证的 pending 两个复核日期为 null。保留的 approved 满足：

```text
first_seen <= last_verified <= review_as_of < review_after <= last_verified + 30天
```

首次确认锚点在 policy 中固定原 evidence 路径、SHA 和批准日。该条目的首次窗口保留；后续 last_verified 前移必须有新 runtime-validation，包含环境、客户端版本、方法、结果、实际观测及验证日期，不能改原确认日期或新写一份简短陈述续期。元数据验证不能证明证据真实性，维护者仍须审阅。

30 天是项目维护窗口；到期 UTC 当日 00:00 阻断新发布，不能只顺延日期。条目删除/替换须绑定审阅理由及受影响测试；关键兼容项还需替代覆盖或移除后的核心流程证据。不能通过删除、降级或跨产品套用批准消除门槛；旧运行批次不因日历变化自动删除。

<a id="consumer"></a>
## 5. N100 接入与实际分流

### 5.1 保留位置，使用 Release Latest SRS

当前 canonical 单源为系统安装仓库的 `5.sing-box/1.配置文件/config.json` 及配置契约。2026-09-28 系统安装仓库已有后续磁盘文件对齐及只读探测记录，不能继续把原发布批次的“现场仍引用旧仓库”当成当前事实；本次不重新连接实机，也不声明候选已被 N100 加载。仓库 canonical 的 AWS/AWS-CN 等既有修改保留，不从现场回灌，也不把旧审核整份配置覆盖当前文件。

**仓库三端及 iCloud 的两个产品集合统一使用 `type: remote`、`format: binary`，通过 Latest 固定入口加载正式 Release 的同名 SRS。** `v0.1.0` 发布批次曾验证两个入口200且摘要一致；这不代表候选已发布或设备已加载。 不在客户端配置维护内嵌域名/IP 列表。既有 tag 和定义索引 2 / 3 保留，不新增目的 IP 文件、tag 或路由规则。两个定义为：

```json
[
  {
    "tag": "geosite-openai",
    "type": "remote",
    "format": "binary",
    "url": "https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs"
  },
  {
    "tag": "geosite-anthropic",
    "type": "remote",
    "format": "binary",
    "url": "https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs"
  }
]
```

下载继续继承现有 `route.default_http_client: "proxy-http"`。`proxy-http` 是 HTTP client tag，不是出站 tag，不能将它写为 `download_detour`。保持现有 HTTP client、代理、DNS、缓存配置和其他规则来源；`geosite-ai` 不变。恢复原生远程拉取/缓存/周期检查机制，省略默认的 `update_interval`。两个配置 URL 保持不变；以后发布并设为 Latest 的正式 Release 必须同时提供同名 `openai.srs`、`anthropic.srs`，以及可核验的批次 manifest。客户端在后续远程更新时可取得新版，不需要为每个版本修改 URL，也不保证发布后即时更新。两个规则集各自下载/缓存，不构成跨文件原子更新；需要严格固定整批版本的验收或恢复任务仍应另行使用已核对的具体版本地址。

`0.1.0` 历史接入只更改两个下载地址；[发布前核验](evidence/latest-srs/http-results.json)与[发布后核验](evidence/latest-srs/publication-results.json)保留原身份。本次候选改变六个精确主机的产品覆盖，不修改配置，不把旧下载或现场记录作为本候选验收。

**route.rules 与 dns.rules 的对象、内容和顺序均保留。** 四条产品路由继续位于 Google/YouTube 后、通用 `geosite-ai` 前：

```json
[
  {"rule_set": "geosite-openai", "ip_version": 6, "action": "reject", "no_drop": true},
  {"rule_set": "geosite-openai", "outbound": "proxy"},
  {"rule_set": "geosite-anthropic", "ip_version": 6, "action": "reject", "no_drop": true},
  {"rule_set": "geosite-anthropic", "outbound": "proxy"}
]
```

保留现有 QUIC 规则。SRS 只是集合；AAAA 空应答/IPv6 reject 来自消费者规则，受模式、更早命中及内核旁路影响，不代表所有 LAN 请求均由产品规则接管。

**远程启动风险作为部署前置条件保留，不通过改用 inline 消除。** alpha.9 对同 tag 的缓存记录 URLHash；更换 URL 可能使旧缓存不被加载，首次抓取失败可能使启动失败。有效 `initial_path` 能提供种子，但各平台须先实际分发并验证路径、权限、内容与摘要；本轮不向 N100 分发种子，也不添加未经验证的跨平台路径。HTTP 下载和本地配置语法通过不等于目标设备的代理下载链、空缓存启动已经通过。

后续部署前须在授权环境验证实际下载链与文件 SHA、原始配置检查、无旧缓存时的启动及适用的恢复路径；失败不切换生产配置或重启现网。恢复需有可用的原配置及原 SRS 字节，不能仅假定改回旧 URL 就会恢复缓存，因为同 tag 成功下载的新内容可能已覆盖旧内容。以后授权 N100 部署时，仅合入本次获准差异，不能顺带部署其他 canonical 修改。

### 5.2 共有依赖与首次命中

当前配置保持 Google 在产品规则前、OpenAI 在 Anthropic 前、通用 AI/GitHub 在产品规则后。下表是固定集合与配置的预期；候选实际隔离结果见 §7，不把推导代替运行观测。

| 范围 | `0.1.0` → `0.1.1-rc.1` 的预期 | 影响边界 |
|---|---|---|
| `github.com`、`registry.npmjs.org` | 由已存在的 Anthropic 覆盖转为更早 OpenAI 覆盖；仍为产品DNS和IPv6策略 | 当前两产品同一proxy；未来分开出口须重新审阅 |
| `api.github.com`、`release-assets.githubusercontent.com` | 从通用GitHub覆盖进入OpenAI | 可能从通用AAAA/IPv6行为转为产品AAAA空响应和IPv6拒绝；所有该主机请求均受影响 |
| `fonts.googleapis.com`、`fonts.gstatic.com` | 原序仍先命中Google；移除Google覆盖后可由Anthropic独立承接 | 当前首次命中不必变；单集验收必须排除Google及其他兜底 |
| `humb.apple.com`、Apple平台候选 | 保持先于产品的Apple规则 | “产品集合包含某域”不等于全部产品域都禁IPv6或走同一出站 |
| 17条pending及3条未选optional | 不因当前final为proxy而批准 | 以后修改通用集合/final仍可能影响，必须复审相应功能 |

域名SRS不能识别调用它的软件或HTTPS路径，精确共享主机也会影响其他应用。先命中的direct/reject、Direct/Global模式或内核GeoIP-CN旁路仍可能越过产品规则。单集测试仅证明排除代承接后所选范围的规则责任；前置截获应作为可检测反例，不能宣称入SRS后不受任意顺序改动影响。客户端到VPS用IPv4也不证明VPS到服务用IPv4。

旧仓库→rc.2/`0.1.0` 的完整退出记录保存在[迁移清单](../sources/evidence/legacy-to-rc2-coverage.json)与[历史消费者证据](evidence/round3/consumer/README.md)，历史原始字节、投影fixture及首次命中索引不改写。本候选重新选中两字体并增加四个OpenAI安装主机，不能继续套用旧表“字体默认不补、api.github.com不在产品集合”的现状判断。

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

上述流程已实现于 `scripts/common.py`、`sync.py`、`generate.py`、`validate.py`。manifest schema 为 2；记录原始基线与解码语义摘要、完整 provenance、选项、补充证据及工具链。当前目标正式版本为 `0.1.1`；设计修订号不冒充 sing-box 软件升级。

### 6.2 快照与可复现要求

官方快照保留可审阅的网络事实或机器数据及 `url/retrieved_at/method/page_updated/sha256`，并让结构化事实逐项定位原文；原文响应摘要与事实记录文件自身摘要分别登记。正常 HTTP、官方检索正文、维护者保存均可；验证页、空文档、抽取失败必须停止更新。工具抽取文本明确不是原始 HTML。页面只有相对 Updated 时原样记录，绝对日期为 null；不能推算一个精确日期。同一导出时间不自动证明伪造，但不得冒充逐页抓取时间。

`0.1.0` 来源归档批次曾取得 OpenAI 网络页工具正文及 Claude 网络/桌面/IP 页面；后续 Voice JSON 成功取得且字节一致。后续 OpenAI 帮助主页面请求返回403，不把固定归档写成候选期间重新成功取得的动态正文。OpenAI 原文显示 `Updated: last month`；公共 Statsig 未列的描述只对应已归档正文。对外受版本控制输入保存完整网络事实、逐项原文定位、取得时间/方式及原文摘要；完整解释性页面仅留本地审阅，不将未获再分发许可的整篇网页公开复制。Voice 机器数据及上游基线原件归档，公开事实记录不冒称原始 HTML。

manifest 记录 schema、项目版本、source_commit、全部构建输入哈希、基线 repo/ref/path/hash、补充输入及证据、编译器平台与 SHA、固定 Go/sing-box/sing 依赖、features、enabled_optional、review_as_of、build_mode、三个源/二进制摘要与大小、binary_version=2、单 default 结构、验证结果和重建证据。正式批次 `source_commit` 必须指向已提交输入。未提交本地候选的该字段仅为工作树基础提交，实际输入身份由 `inputs` 哈希给出；不得宣称完整提交绑定或发布资格，提交后须重新构建。

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

发布资格分为两层，不能相互代签：

- **静态制品发布**：`release-review.json` 使用 schema 2、`scope: artifact-publication`；绑定本次明确上传授权、目标版本、三个 SRS 摘要，以及有结论和固定依据的 semantic diff 审阅。必须为 release 模式，当前 UTC 日期有效，所有构建输入均匹配已提交 `source_commit`，基线/来源/结构/方向/原生匹配和独立重建通过；pending 未选，无未解决官方冲突。获准后可发布同批制品。
- **消费者运行验收**：独立保留 consumer-integration 门槛。记录平台、版本、环境、方法、地址族、配置摘要、实际出口和结果，并绑定本批次 SRS；声明支持的登录、Challenge、DNS、Voice、Artifacts、插件、启动、重启和消费者组合须有适用证据。未完成时 `validated_consumers: []`、`integration_evidence: []`、`deployment_status: pending`，不能因发布成功改为通过。

当前[发布授权](../sources/evidence/release-v0.1.1-authorization.json)与[静态语义审阅](../sources/evidence/release-v0.1.1-review.json)只批准 `0.1.1` 的三个指定摘要；`release-review.json` 绑定这批记录。旧 `0.1.0` 记录及候选 `publication_approval=null` 保留历史身份。

源提交准备、两次干净构建、隔离回归与静态门槛通过后，归档同批 manifest、校验和与制品。将三个正式 SRS 放入 `dist/`，可复验同批源 JSON、SRS、manifest、cases 与 matches 放入对应版本 `artifacts/<version>/`；构建临时目录不入库。手动建立正文为空的正式 Release，上传三个同名 SRS、manifest、SHA256SUMS 与含来源/许可证的压缩包；先以 draft 上传、核验，再以非 Latest 正式 Release 公开；固定 URL 下载及本机空缓存加载通过后设为 Latest，保持旧 Release 不变。Latest 两条下载入口必须实际返回200并与该批摘要一致。定时 CI 只发现/校验候选，不自动发布。

首次部署前另行确认实际下载链、目标原配置 check、无旧缓存启动、可用原配置及旧 SRS 恢复路径。当前消费者使用 Latest remote URL，发布新 Latest 可能被运行中的服务自动取回，不需要改配置或重启。后续必须区分非 Latest 候选与正式发布；草稿/非 Latest 上传完整资产后核对，再改变入口，测试新旧资产异步组合。Latest 回退也不保证已更新消费者立即回退。本次已授权 GitHub 静态发布；不访问或操作 N100。失败不清空 cache.db、不盲重载、不覆盖上一批准批次。运行验收出现遗漏、实际路径泄漏、非预期出口变化或功能回退时停止该环境部署；本地隔离检查可修复后重测。审阅记录提供可追溯性，不能从记录本身证明其观测真实性。

<a id="execution"></a>
## 7. 当前执行计划与验证层级

### 7.1 已验收输入与正式发布计划

已验收候选为 `0.1.1-rc.1`，本轮以同一规则输入晋升正式 `0.1.1`，固定 `0.1.0` 作为对照。已核对的差异只有 OpenAI exact 20→24、Anthropic exact 12→14；后缀、正则、Voice 目的地址、Anthropic 目的及来源网段全部不变。

| 步骤 | 终点 / 当前状态 |
|---|---|
| 1 来源、规则、policy、文档与版本 | 已完成：四个 Codex 安装 exact，启用已有两字体 optional；17 pending 不选，所有既有来源输入保持 |
| 2 本地候选构建与隔离验收 | 已完成本地范围：46项回归、两批各2,038项原生验证、395请求实际消费者；四场景临时安装、npm离线安装与字体资源链通过。边界见下方 |
| 3 正式输入提交与 release 构建 | 已完成；提交绑定、两次各2,038项原生检查、46项回归；三个SRS及源JSON与候选逐字节一致 |
| 4 手动上传与固定URL验收 | 待执行；draft完整上传并核验摘要，以非Latest公开，再验证真实固定URL及本机空缓存/default HTTP client加载 |
| 5 Latest与交付 | 待执行；步骤4通过后更新Latest并下载比对。在线消费者运行验收保持pending，不操作N100 |

本地结果已归档：[验收汇总](evidence/durability-0.1.1-rc.1/local-results.json)、[证据与复现入口](evidence/durability-0.1.1-rc.1/README.md)、[候选 manifest](../artifacts/v0.1.1-rc.1/manifest.json)、[校验和](../artifacts/v0.1.1-rc.1/SHA256SUMS)。该候选构建时工作树未提交，候选manifest 的 `source_commit` 是基础提交，`inputs` 是当时源码身份；其历史记录不改写为正式提交绑定。

| 本地验收 | 结果与限制 |
|---|---|
| 原生与重建 | 两次 candidate 构建各2,038项零失败；全部3 SRS、3 JSON逐字节一致；完整46项回归通过，无跳过 |
| 单产品独立 | 109请求；排除另一产品、通用集合与代理final；正负例按实际原生消费者判定 |
| 原序与新旧组合 | 240请求，37份完整通用SRS与两产品四种组合；DNS规则全等，route[1:]全等，未投影成见证集合 |
| 对抗与混合DNS | 移除产品/前置direct/reject共36请求；返回IP正反6请求；空AAAA/HTTPS、正常地址、实际出站返回marker均严格断言 |
| 冷启动机制 | 4请求，两个remote SRS经受控HTTP fixture冷缓存加载，default HTTP client路径可观测；非GitHub线上bootstrap验收 |
| 清理 | 共20个sing-box子进程退出，11个回环监听关闭；清理失败会使测试非零退出 |
| 安装与字体 | 固定Codex0.158.0 Mac ARM64真实包摘要核验；四种受控安装来源/回退均运行--version成功；npm11.16.0以验证过的原tarball隔离离线安装成功；公开CSS与实际字体GET200 |

395请求为254 DNS和141 route，其中IPv4/IPv6 TLS各30次。所有业务流量终止于回环观察器，证明实际sing-box选择/拒绝，不证明公网出口。原序测试安全替换了仅ICMP的route[0]为拒绝占位，hosts/mDNS为不命中这些公共见证的空hosts resolver；生产传输、TUN、ICMP bridge、mDNS和公网IPv6不在范围。[fixture转换](evidence/durability-0.1.1-rc.1/consumer/fixture-transform.json)列明全部替换。

**已实测的行为变化**：`api.github.com`、`release-assets.githubusercontent.com` 的AAAA从通用DNS index17有地址变为产品index15空应答；IPv6 TLS从通用route25/proxy变为OpenAI route20/reject，IPv4/域名转route21。`github.com`、npm从Anthropic route23转OpenAI21，AAAA此前已抑制；字体继续先命中Google。这是保持原规则位置后的明确副作用，不称“仅改列表、无行为变化”。索引仅对应本批固定canonical。

| 候选 SRS | 字节数 | SHA-256 |
|---|---:|---|
| `openai.srs` | 775 | `a910767e3f07dfe89e2f72639960612872361d9ae1c8553ddd4a59c8f154778f` |
| `anthropic.srs` | 353 | `864149211a66da97603b62367f19209e5de2e1b52905faee503501fc37a4c08b` |
| `anthropic-ip.srs` | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |

安装来源联网观察、受控故障回退、实际临时安装与候选SRS分流分层记录，没有将它们拼成未经执行的线上端到端登录验收。npm使用已下载的原包离线安装，不声称验证任意用户registry/proxy设置。未做账户登录、真实Artifacts渲染或其他平台安装。来源记录当时的HEAD边界保留，后续实际下载/安装证据另列。

rc.1 本地验收阶段起初缺Go模块缓存，补取锁定依赖时的一次HTTP/2错误通过HTTP/1.1取得同版本解决；没有改go.mod/go.sum或放宽校验，最终两批原生校验离线通过。正式dist、旧批次及仓库客户端配置26份指纹全部不变。candidate和伪改release两种发布尝试均被校验器拒绝；没有实际上传调用。最终候选manifest的消费者与部署声明保持空/pending，独立证据只记录本地隔离层级。

正式重建证据见[0.1.1 构建结果](evidence/release-v0.1.1/build-results.json)与[正式 manifest](../artifacts/v0.1.1/manifest.json)。正式源码提交 `bba3c7c927b4a4bd4a365ca79184e25758c354f3` 绑定全部构建输入；该批已通过 `--for-release`，消费者与部署身份仍为空/pending。

### 7.2 `v0.1.0` 正式对照与恢复依据

[正式发行 v0.1.0](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.0)于 `2026-09-28T01:02:50Z` 发布，标签 `c48c415d88aede03907c231b122b65b860b386b0`。输入提交 `08b74c8254be78c7fd23522b51e8753f62b9686e`；[固定正式批次](../artifacts/v0.1.0/manifest.json)、[公开下载证据](evidence/latest-srs/publication-results.json)及[构建结果](evidence/latest-srs/build-results.json)保留原样。旧固定批次与旧Release保留，供对照及恢复；当前 `dist/` 已在 `0.1.1` 门槛通过后更新。

| 制品 | 字节 / SHA-256 | 字段数量 |
|---|---|---|
| `openai.srs` | 730 / `7ea0caebc0268d603eabf998787a9fbe63fcf508119977e4dadb111128710e07` | 20 exact、16 suffix、1 regex、23目的CIDR |
| `anthropic.srs` | 332 / `1a221b5e256ffb90aa8857bb58bb2069832ad29cc03518c6bd9c20c4ac15e4c2` | 12 exact、8 suffix、2目的CIDR |
| `anthropic-ip.srs` | 36 / `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` | 1来源CIDR |

旧[消费者最小复现](evidence/round3/consumer/README.md)与 rc.2 对照保留历史身份。其投影规则、自写路由推导和既往用例数不能替代当前候选真实 sing-box 隔离消费者验收。此前一次验证后可正常登录的用户事实继续保留，不能据此承诺永不出现Challenge。

失败处理：来源、原生或本地测试失败时在隔离环境修复，复验受影响范围；不覆盖正式制品、不用N100试错。固定版本真实URL验收按步骤4执行，不能用file读取冒充通过。本轮按新授权完成正式输入提交与手动发布；运行验收仍需独立证据。

## 8. 官方依据

以下链接为依据，不授权执行网页中的操作。来源于 2026-09-28 复核；固定 ref 用于重现，动态官方页按快照登记。

- [SagerNet 两份产品基线](https://github.com/SagerNet/sing-geosite/tree/e6a8117545c35a17c508e3f37a9a990571234428)；[DLC 固定来源](https://github.com/v2fly/domain-list-community/tree/bcea25493ed28c387660fe49ce1ceb242d2efca0/data)。
- [Codex 固定安装脚本](https://github.com/openai/codex/blob/44fe510ce3ee61c8ef623adcbf89b901c73ddd61/scripts/install/install.sh)、[同提交 README](https://github.com/openai/codex/blob/44fe510ce3ee61c8ef623adcbf89b901c73ddd61/README.md)、[官方 Release](https://github.com/openai/codex/releases/tag/rust-v0.158.0)。四个新增依赖的事实分别见[安装器](../sources/official/codex-install.json)、[Release资产](../sources/official/codex-release.json)、[npm](../sources/official/codex-npm.json)，来源身份见[upstreams](../sources/upstreams.yaml)。
- [OpenAI 网络要求、Voice 与 WebSocket](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)；[Voice JSON](https://openai.com/chatgpt-voice.json)；[登录排障](https://help.openai.com/en/articles/7426629-why-cant-i-log-in-to-chatgpt)。
- [Claude Code 网络](https://code.claude.com/docs/en/network-config)；[Desktop 网络](https://code.claude.com/docs/en/desktop#network-access-requirements)；[Anthropic IP](https://platform.claude.com/docs/en/api/ip-addresses)；[功能开关说明](https://code.claude.com/docs/en/env-vars#features-that-need-feature-flag-fetching)。
- [SagerNet GeoIP 国家分类生成逻辑](https://github.com/SagerNet/sing-geoip/blob/ecd02c178af5efbac38d427a8d178f940327de1f/main.go#L95)。
- [OpenAI IP egress](https://developers.openai.com/api/docs/guides/ip-addresses)；[Realtime SIP](https://developers.openai.com/api/docs/guides/voice-sip)；[社区 OpenAI IP 最终抓取来源](https://github.com/lord-alfred/ipranges/blob/14adfd8def77c9f81057fdbc16230667b7cfa2f4/openai/downloader.sh#L39)。
- [Cloudflare Challenge 限制](https://developers.cloudflare.com/cloudflare-challenges/concepts/how-challenges-work/#limitations)。
- [sing-box rule-set](https://sing-box.sagernet.org/configuration/rule-set/)；[Headless rule](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/)。
- alpha.9 固定源码：[compile](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/cmd/sing-box/cmd_rule_set_compile.go#L84)、[decompile](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/cmd/sing-box/cmd_rule_set_decompile.go#L39)、[merge](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/cmd/sing-box/cmd_rule_set_merge.go#L105)、[SRS](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/common/srs/binary.go#L54)、[组合边界测试](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_set_semantics_test.go#L411)、[目的组](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_abstract.go#L98)、[DNS](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_dns.go#L424)、[DNS 分派](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L1208)、[禁用 legacy 条件](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L1417)、[旧路径跳过条件](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L296)。
- [sing Matcher 规范化](https://github.com/SagerNet/sing/blob/4ca3bebe0b8e/common/domain/matcher.go#L119)；[固定 testing 对照](https://github.com/SagerNet/sing-box/tree/710d7c715b10cf9fc158b1ab7fd7198754962c59)。
- 社区发现旁证：[blackmatrix OpenAI](https://github.com/blackmatrix7/ios_rule_script/blob/0fa60782abfe70f58da510e90d9086136cf0d855/rule/Clash/OpenAI/OpenAI.list)、[Claude](https://github.com/blackmatrix7/ios_rule_script/blob/0fa60782abfe70f58da510e90d9086136cf0d855/rule/Clash/Claude/Claude.list)。仅用于发现候选，不作为官方批准或新的基础输入。
