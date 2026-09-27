# sing-box-ai：OpenAI / Anthropic 规则集正式方案

**主仓库：`YouM1225-1/sing-box-ai`**\
**状态：仓库实现与正式设计基线；新批次消费者验收及正式发布待执行**\
**日期：2026-09-27**\
**文档修订：1.7**

修订 1.7 将方案落到 `sing-box-ai` 0.1.0 仓库，建立维护数据、固定快照、发现分类、SRS 生成和本地验证流程；正式发布与客户端接入仍按验收门槛执行。维护者确认 Claude Challenge 已于旧仓库更新日 2026-09-27 验证，兼容项据此批准；不把这条历史验证改写为本次新制品的现场验收。N100 四条产品路由保留原位置。

本次已拉取 1.15 最新开发分支和最新已发布预览版源码，并取得最新可见 sing-geosite 两个 SRS 及其原始规则。精确版本、实测结果与证据入口见 §4.2、§17。所有“最新”均指 2026-09-27 本次查询时点，不是未来浮动依赖。仓库已由维护者创建；本阶段按用户指令先建立仓库，再处理客户端配置。

阅读入口：仓库消费配置 → §18；生成与验证实现 → §8–§10；真实登录与出口验收 → §11–§12；实施状态 → §15.1。

## 1. 目标与唯一输出

`YouM1225-1/sing-box-ai` 是已建立的唯一主仓库。初始化代码、审核附件与正式发布制品的状态分别记录；没有通过发布门槛的固定制品 URL 不能接入客户端。只发布三个正式 sing-box 二进制规则集：

``` text
dist/openai.srs
dist/anthropic.srs
dist/anthropic-ip.srs
```

规则采用**可信上游的证据驱动并集**：

``` text
官方当前规则
∪ 可信上游有效补集
∪ 已验证本地兼容补集
- 废弃项
- 错误方向项
- 无证据项
- 过宽项
- 明确不启用的可选项（不改变默认功能范围，见 §6）
= canonical rules
```

目标是在可审计证据范围内尽可能完整覆盖 OpenAI/ChatGPT/Codex 与 Anthropic/Claude/Claude Code/Claude Desktop。动态 CDN、用户 MCP、第三方网站和未启用云 provider 不宣称可以用有限静态集合穷举。

不再保留旧仓库迁移叙述、旧文件名 alias、Surge/Clash/Loon/Quantumult X 输出或重复规则源。

## 2. 三个制品的职责

### `openai.srs`

客户端目的规则。覆盖：

-   OpenAI 官方网络 allowlist；
-   ChatGPT Web/Desktop/iOS/Android；
-   Codex 所需 OpenAI/ChatGPT 端点；
-   官方 WebSocket 目标；
-   官方认证、上传、静态资源、WorkOS、Intercom、Sentry、Datadog 等依赖；
-   ChatGPT Voice 当前官方目的 IP 数据（`chatgpt-voice.json`，见 §11）；
-   可信上游经验证的缺失兼容项。

允许：`domain`、`domain_suffix`、经范围审阅的 `domain_regex`，以及官方明确标注为客户端目的地址的 `ip_cidr`。Voice 地址来自官方定期更新的数据快照，不是永久固定网段；不得用一次 DNS 结果替代。

消费者引用本集合时不得设置 `rule_set_ip_cidr_match_source: true`，否则 Voice 目的地址会被改作来源条件。该限制与 `anthropic.srs` 一致。

禁止 `domain_keyword`、一次 DNS 得到的 CDN IP、整个 `amazonaws.com`/`api.aws`/Azure/Cloudflare 公共后缀、OpenAI 爬虫来源 IP 列表（`gptbot.json` 等，见 §3），以及仅因名称类似 OpenAI/ChatGPT 而收录的域名。

### `anthropic.srs`

客户端目的规则。覆盖：

-   Anthropic/Claude 官方网络域名；
-   Claude Code CLI；
-   Claude Desktop / Code tab；
-   Artifact、MCP、live preview、插件与安装流程所需依赖（功能范围与包含策略见 §6、§12）；
-   可信上游经验证的兼容补集；
-   Anthropic 官方稳定 inbound：
    -   `160.79.104.0/23`
    -   `2607:6bc0::/48`

不得把 `160.79.104.0/21` 作为完整目的地址范围加入。消费者路由规则引用 `anthropic.srs` 时**不得**开启 `rule_set_ip_cidr_match_source`（sing-box ≥ 1.10.0；旧拼写 `rule_set_ipcidr_match_source` 已弃用），否则上述 inbound 网段会被当作来源匹配。

### `anthropic-ip.srs`

只用于识别来自 Anthropic 服务的出站请求来源。

唯一网络语义：

``` text
source_ip_cidr: 160.79.104.0/21
```

规则集内直接使用 `source_ip_cidr` 项（headless rule 原生字段，运行时以来源地址匹配），消费者无需也不应再开启 `rule_set_ip_cidr_match_source`。不得含客户端目的 `ip_cidr`。不得包含 Anthropic 已 phased-out 的五个旧 `/32`（值见 §12）。该规则不是身份认证，服务仍需应用层鉴权。

## 3. 上游信任模型

### Tier 0：官方

最高优先级。

OpenAI：

-   OpenAI Network recommendations（帮助中心页面，取得方式见下）；
-   OpenAI 当前产品/企业网络文档；
-   OpenAI 机器可读数据须逐个标明用途与方向：`gptbot.json`、`chatgpt-user.json`、`searchbot.json` 是爬虫/代理请求的来源地址，不进入 `openai.srs`；当前网络文档引用的 `https://openai.com/chatgpt-voice.json` 是 Voice 客户端连接的服务器目的地址，应进入本方案默认 Voice 范围。不能以“OpenAI JSON”这个文件类别判断方向。

Anthropic：

-   Claude Code 官方网络文档（`code.claude.com/docs/en/network-config`）；
-   Claude Desktop 官方网络要求（`code.claude.com/docs/en/desktop#network-access-requirements`）；
-   Anthropic IP addresses（`platform.claude.com/docs/en/api/ip-addresses`）；
-   Claude Platform provider 文档（仅用于 provider 独立 profile，见 §12）。

sing-box：

-   官方 rule-set / Source Format / Headless Rule 文档；
-   SagerNet/sing-box 与 SagerNet/sing 源码用于确认真实匹配和编译语义（固定 commit 记入 manifest）。

**官方页面快照**：允许正常 HTTP 获取、官方页面正文检索或维护者手工保存，不自动解验证码。一次工具返回 403 只描述该次访问，不能写成“任何 HTTP/浏览器都无法取得”。本次通过网页检索工具取得 OpenAI 三篇官方正文；网络页显示 `Updated: last month`，登录页 `5 days ago`，CAPTCHA 页 `2 months ago`，这些相对字符串原样登记，不推算精确修订日期。

实施时将实际采用的正文或经人工核对的结构化网络事实快照存入 `sources/official/`，同时记录 URL、`retrieved_at`（UTC 时间戳）、取得方式、`page_updated` 原文或 null、sha256。正文抽取失败、验证页或空列表必须报错；不得将旧副本自动冒充当前官方基线。离线构建仅使用已审核快照；联网更新先取得新快照再比较，不依赖网页在构建中保持不变。

### Tier 1：可信规则项目

首选：

``` text
v2fly/domain-list-community（data/openai、data/anthropic 文本文件）
```

理由：它提供可定位到原始行的文本数据，便于保留属性和审阅。`SagerNet/sing-geosite` 从 v2fly 的 `dlc.dat` 派生二进制；当前 `rule-set` 提交无父提交、分支会重建。这带来旧对象长期保留不确定性，但不等于固定 SHA 无法下载。本次按完整 SHA 成功取得并反编译两份 SRS。仍优先固定 v2fly 文本作为输入；派生 SRS 用固定 commit、文件哈希与归档副本交叉核对，不依赖可移动 tag。

其他上游只有满足以下条件才能登记：公开源码、持续维护、可固定 commit、可追踪原始规则、许可证适用、不要求执行其远程代码。

Tier 1 只用于发现官方基线的**补集**，不能覆盖官方事实。带 `@ads` 等属性的条目（如 `browser-intake-datadoghq.com`、`o33249.ingest.sentry.io`、`openai.qualtrics.com`）按遥测 / 共享依赖处置，只有官方 allowlist 同时列出时才可为 `required`。

### Tier 2：本地兼容证据

兼容项分为普通 `compatibility` 与关键 `compatibility-critical`。后者表示缺失时可能影响登录、挑战验证或核心交互的精确规则，不允许使用宽泛共享服务后缀。关键程度不代表证据已合格；两类采用相同证据和复核要求，不因 `critical` 获得豁免。

兼容候选必须具备以下字段；发布资格由下述 `review_status` 和日期判据共同决定：

``` text
value
type
product
reason
review_status
evidence
first_seen
last_verified
review_after
```

`review_status` 仅允许 `pending`、`approved`。历史收录、一次抓包或 DNS 观察只支持登记候选，不能单独证明当前产品需要该规则；`approved` 必须有对应产品的有效性验证证据。证据至少记录种类、可定位的 `reference`、观测日期和它能支持的结论；运行证据还记录环境、产品/客户端版本、验证方法及结果。不得用 OpenAI 的官方依赖证明 Claude 的当前需求，也不得把读取历史文件的日期写成现场验证日期。

维护者在审阅中明确确认已完成验证时，可登记 `user-confirmation` 作为兼容项批准依据。记录原话、对应精确规则、验证日期的来源和适用范围；未提供的客户端版本、环境保持 null，不编造。该确认支持兼容项的有效性复核，不自动成为新制品/新配置的逐平台集成验收。自动 validator 核对记录的完整性及日期，证据真实性由维护者审阅负责。

日期统一为带引号的 UTC 日历日期 `YYYY-MM-DD`。`first_seen` 是本项目首次有据登记该候选的日期，不宣称是域名或上游规则的最早出现时间；`last_verified` 是最近一次完成本条目有效性复核的日期。从未完成有效性复核时 `review_status: pending`，`last_verified` 与 `review_after` 均为 `null`；已复核过但需重验的条目保留真实旧日期与证据。`pending` 无论日期是否为空均不能发布。

批准项必须满足 `first_seen <= last_verified <= review_as_of < review_after <= last_verified + 30天`。30 个日历日是本项目的维护窗口，不是厂商要求；可设置更早的复核日期。到达 `review_after` 当日 UTC 00:00 即到期，无宽限期；即使文件仍写着 `approved`，也不能继续发布。复核不能只改日期，必须有对应的新增验证记录或明确的证据重验记录。

`review_as_of` 是本次构建固定的复核基准日期，写入 manifest，供相同输入重建；发布前还必须以实际当前 UTC 日期再检查一次，不能用旧基准日期绕过到期门槛。候选、到期项及批准/删除处置按 §8、§9、§15 执行。

### Tier 3：发现源

Issue、论坛、个人规则库、历史仓库、一次抓包、DNS 观察等只能产生候选，不能直接进入正式 SRS。

## 4. 合并与冲突规则

优先级：

``` text
同用途、同方向、适用当前版本的官方文档与机器数据/源码（冲突时暂停审阅，不机械互相覆盖）
> Tier 1 可信上游
> Tier 2 本地实测
> Tier 3 发现源
```

第三方新增条目必须先判断：

1.  是否已被官方 suffix 覆盖；
2.  是否属于实际 OpenAI/Claude 产品链路；
3.  是否为共享 CDN/遥测/云基础设施；
4.  是否能缩小为精确主机；
5.  是否只是一次 DNS/IP 观察；
6.  是否会扩大到无关服务。

冲突官方、明显过宽或用途不明的条目不得进入 canonical。

先按制品及 `product` 核验来源、兼容复核状态与适用范围，再在同一制品内按 `(type, normalized_value, direction)` 去重；某一产品的批准不能跨制品继承。但 provenance 必须保留多个来源。最终 binary 可去掉被父规则完全覆盖的冗余精确域名，canonical 数据不能丢失来源关系。

Wildcard 必须保留原语义；`*.example.com` 不得未经判断就转换成同时覆盖 apex 的规则。转换按 §4.1 执行。

### 4.1 记法映射（规范）

sing-box 的 `domain_suffix` 语义（SagerNet/sing `common/domain/matcher.go`，`NewMatcher` / `has`）：

| 规则 | 命中 `example.com` | 命中 `a.example.com`、`b.a.example.com` | 命中 `notexample.com` |
|---|---|---|---|
| `domain: "example.com"` | 是 | 否 | 否 |
| `domain_suffix: ".example.com"` | **否** | 是 | 否 |
| `domain_suffix: "example.com"` | 是 | 是 | 否（按 `.` 边界） |

官方与上游记法转换：

| 来源记法 | 转换 | 说明 |
|---|---|---|
| 官方 `*.x`（例如 `*.oaistatic.com`） | `domain_suffix: ".x"`（例：`.oaistatic.com`） | 通配域逐一映射，保留各自域名；不自动加入 apex |
| 来源写作 `.x` | 先核对该来源的记法定义，确认表示仅子域后才转换为 `.x` | 当前 OpenAI 页面是 `*.x`；旧副本记法不能覆盖当前事实 |
| Anthropic `anthropic.com` + `*.anthropic.com` 成对出现 | `domain_suffix: "anthropic.com"` | 官方已分别列出 apex 与子域，可合并为无前导点后缀 |
| 官方精确主机、v2fly `full:` | `domain` | |
| v2fly `domain:openai.com` 或无前缀 `openai.com` | `domain_suffix: "openai.com"` | v2fly 根域语义 = apex + 子域；sing-geosite 的 `domain` + `domain_suffix: ".x"` 组合与此等价 |
| v2fly `regexp:` | `domain_regex`，须通过 §10 判据 | |
| v2fly `keyword:`、Surge/Clash `DOMAIN-KEYWORD` | 拒绝（`TOO_BROAD`） | |
| v2fly `include:list @a @-b` | 递归展开并按“有 a 且无 b”过滤，再转换 | 固定整个依赖闭包的 commit/哈希；检测循环、缺文件和未知语法 |
| v2fly `@attr` / `&list` | 属性保留为元数据；affiliation 按上游语义导入被指向列表 | 本次两份文本无 include/affiliation；实现未支持时遇到必须失败，不可悄悄忽略 |

三份产品规则 YAML 的 `type` 只允许 `domain`、`domain_suffix`、`domain_regex`、`ip_cidr`、`source_ip_cidr`；`domain_suffix` 的 `value` 是否带前导点即为语义本身，规范化不得增删前导点。精确/后缀域名统一小写、IDNA ASCII，删除输入末尾 DNS 根点前须记录规范化；运行时收到带根点/非 ASCII 域名不能假定匹配器会自动作同样转换，须在实际消费者路径验收。regex 保留原表达式，只允许经验证的 Go RE2 语法，不做可能改变语义的字符串“规范化”。

## 4.2 sing-box 1.15 精确匹配与 SRS 契约

| 用途 | 本次固定版本 |
|---|---|
| 最新已发布 1.15 预览版、隔离运行测试 | `v1.15.0-alpha.9`，commit `132b38e9caaba1a1959354d518e54d2d08419afe`，2026-09-26 发布 |
| 本次最新 testing 源码分析/交叉测试 | `af60b5e60525ff003940a7816a5302d58ad550fa`，2026-09-27T10:40:50Z；不能标成 alpha.9 发布二进制 |
| 发布版所依赖 sing | `v0.9.6-0.20260922013359-4ca3bebe0b8e` |
| testing 所依赖 sing | `v0.9.6-0.20260927091435-fcc22e2b9f96` |
| 本次可见 stable（仅版本查询） | `v1.14.2`；未做该版本运行测试 |

源码已经下载，关键依据：[alpha.9](https://github.com/SagerNet/sing-box/tree/132b38e9caaba1a1959354d518e54d2d08419afe)、[testing](https://github.com/SagerNet/sing-box/tree/af60b5e60525ff003940a7816a5302d58ad550fa)。两份快照的 `cmd_rule_set_match.go`、`cmd_rule_set_compile.go`、`common/srs/binary.go`、`route/rule/rule_headless.go` 与 `rule_item_cidr.go` 本次对比一致；依赖 sing 不同，因此分别测试。

1. `route/rule/rule_item_domain.go` 优先取 `metadata.Domain`，没有时取 `Destination.Fqdn`，转小写后调用 sing matcher。输入缺失目的域名时域名规则不能凭空命中；透明代理的嗅探、DNS/FakeIP 映射需在消费者配置验收。IP 命中与 DNS 响应匹配还受上下文影响，本方案默认用于 route，不据此宣称所有 DNS rule 场景已验证。
2. `rule_abstract.go`：default rule 内同一组为 OR，不同组为 AND。`domain/domain_suffix/domain_regex/ip_cidr` 属于目的地址组；`source_ip_cidr` 属于来源组。故同一 default 的 domain + ip_cidr 是“域名或目的 IP”，source_ip_cidr + ip_cidr 是“来源且目的”。SRS 多条顶层规则按 OR；logical 的 and/or 与 invert 不可在生成时随意扁平化。
3. `rule_item_rule_set.go:mergeableRuleIn/matchWithOuterGroups`：单条、非 invert 的 default SRS 会与外层同组条件合并；多条或 logical SRS 不走该合并路径。上游 `TestRuleSetShapeBoundary` 明确覆盖了同一集合拆成两条后与外层 domain 条件组合产生不同结果。本次上游测试已通过，不能以孤立集合等价推导消费者组合等价。
4. **生成结构固定**：本项目每个 SRS 恰好一条 default，目的制品只放目的域名/IP 字段，来源制品只放 source_ip_cidr；不生成空 default、invert 或 logical。改变这个结构属于行为变更，必须重验消费者组合，不能当作压缩优化。
5. **消费者引用固定**：推荐路由 leaf 只写 `rule_set` 引用；额外 inbound/来源/端口/网络限制需要逻辑 AND 时，放在不同 logical-and 子规则，动作放在最外层。不要把外层 domain/CIDR 写在 rule_set 同一 default 中期待 AND；也不要通过给三个 SRS 设置来源改写开关切换含义。无附加限制时两个目的集合可同一 rule_set 列表引用（OR），共享 Challenge 走统一出口。来源集合单独引用。
6. 格式最大版本由 `constant/rule.go` 确认为 **5**；官方映射是 v1→1.8、v2→1.10、v3→1.11、v4→1.13、v5→1.14。1.15 没有因此变成 SRS v15。本项目只用基础域名/IP 字段，source v2 即足够；用 v5 输入同样降为 binary v2，已实测。
7. `common/srs/binary.go` 的分发格式是 `SRS` + 一字节版本 + zlib。`common/srs/mmap.go` 的 `SRSM` 是内部 mmap 存储格式，不能替代分发 `.srs`。只检查 magic 不够，必须用上游完整解析器读取所有规则，并禁止项目白名单以外结构。

本仓库的具体配置片段统一见 §18，复用实际的 `proxy`、`dns_proxy`、`proxy-http` 和两个 `geosite-*` tag；不再使用虚构的 `ai-session-in` / `ai-stable-egress` 标签。

## 5. 最小仓库结构

```text
sing-box-ai/
├── README.md
├── sources/
│   ├── openai.yaml
│   ├── anthropic.yaml
│   ├── anthropic-ip.yaml
│   ├── upstreams.yaml
│   └── official/
├── scripts/                 # bootstrap.py、common.py、sync.py、generate.py、validate.py
├── tests/                   # fixtures、固定 module 的 Go harness、语义与元数据回归
├── build/manifest.json
└── dist/                    # openai.srs、anthropic.srs、anthropic-ip.srs
```

三份 YAML 是唯一人工维护数据，保留已批准条目及明确纳入本次发布范围的待核验候选；构建所用 canonical 是其中符合证据契约的集合。仅发现、尚未决定纳入的条目留在同步结果，不自动成为发布阻断项。已登记的必验候选/到期项不能被生成器静默过滤。`upstreams.yaml` 登记上游、固定对象、哈希与归档位置。

构建输入快照与必要依赖必须能从归档恢复，完整 SHA 不保证远端对象永久可取。可保存在受控仓库或制品存储，manifest 记录定位方式与 sha256；干净重建禁止依赖未登记本机缓存。第三方同步只读数据，不执行其脚本。构建/测试使用固定官方 sing-box、固定 module 和工具链。

## 6. canonical 条目

示例：

``` yaml
- value: api.anthropic.com
  type: domain
  product: [claude-api, claude-code]
  direction: destination
  status: required
  shared_dependency: false
  sources:
    - kind: official
      upstream: anthropic
      reference: claude-code-network
  reason: Claude API endpoint
```

`status` 取值：

| 值 | 含义 | 进入制品 |
|---|---|---|
| `required` | 官方当前明确要求 | 是 |
| `feature-required` | 官方明确某已支持功能使用的依赖，例如 Artifact 库 CDN、插件下载、Voice | 默认功能范围启用时必须纳入，记录 `features` |
| `optional` | 官方允许关闭且有降级路径或不影响已声明功能，例如字体、非必要遥测 | 默认不额外纳入；显式 opt-in 时写入 manifest 并验收 |
| `compatibility` | 本地兼容项 | 满足 §3 时是 |
| `compatibility-critical` | 关键兼容项 | 满足 §3 时是 |

默认功能范围固定为 ChatGPT Web/客户端/Codex/Voice，以及 Claude Web/API/Code/Desktop、Artifact、官方文档所列安装与插件路径。关闭上述功能必须修改支持范围、semantic diff 和对应测试，不能把依赖悄悄标成 optional。默认 `enabled_optional: []`；有选择时固定排序写入 manifest，同一批次不发布多个同名不同内容制品。可选规则即使不单独纳入，若被某条有依据的必需 suffix 覆盖，仍可能命中；省略可选项不等于阻断它。

所有条目要求 `value/type/product/direction/status/sources/reason/shared_dependency`（后者布尔值），功能依赖另有 `features`。`shared_dependency: true` 表示该 host 同时服务其他软件或网站（GitHub、npm、Google Storage、`challenges.cloudflare.com` 等），按域名分流会影响其他访问；README 必须列出全部 `shared_dependency` 条目。

`compatibility` 与 `compatibility-critical` 均遵循 §3 的全部字段、证据等级和日期判据，包括 `review_status`、`first_seen`。维护数据可保存待核验状态，正式构建不能接受该状态；完整待核验示例见 §12.1。

`anthropic-ip.yaml` 必须使用：

``` yaml
- value: 160.79.104.0/21
  type: source_ip_cidr
  product: [anthropic-service-egress]
  direction: source
  status: required
  shared_dependency: false
  reason: Official Anthropic service outbound source range
  sources:
    - kind: official
      upstream: anthropic
      reference: ip-addresses
```

## 7. upstream 固定

截至本次查询，锁定以下数据对象：

| 数据 | 固定对象 | 角色 |
|---|---|---|
| v2fly/domain-list-community | `bcea25493ed28c387660fe49ce1ceb242d2efca0`；`data/openai`、`data/anthropic` | 文本发现源；固定闭包与原始哈希 |
| SagerNet/sing-geosite | `e6a8117545c35a17c508e3f37a9a990571234428`；`geosite-openai.srs`、`geosite-anthropic.srs` | 派生交叉核对，不直接充当正式规则 |
| OpenAI Voice | `https://openai.com/chatgpt-voice.json` 的归档字节 | 官方目的地址快照；sha256 `8f03f3c594165eeff009915c7e2beb4bdfb9d429fb1955c205e3b33ec781899a` |

生产构建禁止读取浮动分支、`latest` 或仅凭 tag 定位；更新流程可以发现最新对象，但必须先锁定、归档、比较再构建。官方动态 JSON 没有 Git commit 时以原始字节 sha256 固定，记录获取时间和原文 `creationTime`，二者不得混淆。

本次 sing-geosite 两文件头均为 `SRS` + 版本 `1`，不是“最新规则一定是 SRS v5”。alpha.9 可读取；反编译后与固定 DLC 文本一致：OpenAI 为 9 个 exact + 13 个 root suffix + 1 个 regex，Anthropic 为 1 个 exact + 7 个 root suffix。此比较证明两份数据内容对应，不证明社区新增域名均应批准。

版本 1 输入可用于交叉核对；本项目自己的输出统一版本 2。更新 ref、官方快照、include/affiliation 依赖或上游删除均生成 semantic diff。许可证与来源关系随归档保留。

## 8. 同步、生成、发布

`sync.py`：

1.  获取固定 commit 的文本数据与本地官方快照；
2.  校验哈希、格式、大小以及官方 JSON 的字段/方向；空数据、验证页和未知语法必须失败；
3.  按 §4.1 转换为内部候选结构；
4.  与官方/canonical 比较；
5.  输出：
    -   `ADD_CANDIDATE`
    -   `ALREADY_COVERED`
    -   `CONFLICT_OFFICIAL`
    -   `TOO_BROAD`
    -   `INVALID`
    -   `REMOVED_UPSTREAM`
    -   `OPTIONAL_OFFICIAL`（确为可选、默认不额外纳入）；`FEATURE_REQUIRED`（已声明功能必需，必须纳入）
6.  不直接写 `dist/`。

候选构建与正式构建必须分开。下列接口已在仓库实现；输出目录及运行前置条件见 README。候选构建与 release 模式生成都先写隔离目录，不直接改写 dist：

- **候选构建**：在当前正式规则基线（首次发布时为已核对的官方基线）上加入本次明确选定的候选及其依赖，生成三个候选制品供组合测试；允许兼容状态为 `pending` 或已到期，仍必须通过格式、方向、范围及来源检查。输出到独立临时目录，manifest 标明 `build_mode: candidate`，不得写 `dist/` 或触发发布。候选制品用于取得 §11.3、§12.1 的集成证据，验证未通过时保留问题与证据，不能把候选视为正式规则。
- **正式构建**：固定 `review_as_of`，按 §3 先检查所有兼容项，再生成正式候选批次，manifest 标明 `build_mode: release`。任何 `pending`、到期或证据缺失项均阻断整批三个制品的发布。批准前的验收记录绑定候选规则输入、制品哈希与消费者配置；批准后若仅更改元数据，须确认正式 SRS 与受测候选 SRS 字节一致，否则重验受影响项。

正式构建接口：

``` bash
python3 scripts/generate.py --mode release --output build/release
python3 scripts/validate.py build/release
python3 scripts/validate.py build/release --for-release
```

`generate.py` 必须规范化域名、IDNA、CIDR（regex 仅校验与范围审阅，不改写），检查方向，语义去重，生成临时 sing-box source JSON，并调用固定 sing-box：

``` bash
sing-box rule-set compile --output <tmp>.srs <tmp>.json
```

版本约定：

- source JSON 固定 `"version": 2`（sing-box 1.10.0 引入，优化 `domain_suffix` 存储）。三个制品只含域名 / IP 项，不需要更高版本的规则项。
- `sing-box rule-set compile` 对源版本 2–5 会按实际特性降级（5 → 4 → 3 → 2）；源版本 1 保持 1，不能概括为所有输入都不低于 2；`.srs` 头为 `SRS` 三字节 + 1 字节二进制版本 + zlib 流。manifest 的 `binary_version` 直接读取该字节，回归断言三制品均为 `2`。
- 格式理论最低读取版本是 sing-box 1.10.0；这不代表其路由组合语义已经验收。本次已验证运行时为 `1.15.0-alpha.9`，最新开发 commit 用于交叉回归。1.10.x、1.14.2 及其他消费者须自行完成加载/匹配/集成矩阵后才能列为受支持版本。1.15 是预览系列，本方案不据此要求现网升级。
- 编译器版本、平台、下载来源和 SHA256 固定；测试 harness 使用的 sing-box / sing Go module 版本同样固定并记入 manifest。

上述验证按 manifest 的 `review_as_of` 检查，允许历史输入离线重建；这不等于取得当前发布资格。发布任务最后还须以实际当前 UTC 日期重新执行 §3 的有效期和证据检查，并拒绝 `build_mode: candidate`。只有两层校验及 §14 全部成功，才同一提交发布三个 `dist/*.srs`；未通过时不覆盖上一批准批次。

## 9. validator 必须验证语义

禁止仅做 manifest SHA256 比较。

必须拒绝：

-   空 manifest / 空规则维护数据 / 任一目标制品规则集合为空 / 缺 artifact；
-   非法 YAML、域名、CIDR、regex；
-   未知 type / direction / status；
-   无来源条目；
-   `compatibility` 或 `compatibility-critical` 不满足 §3：字段缺失、未知复核状态、证据不支持该产品、日期非法/矛盾；正式模式还拒绝 `pending`、空复核日期和到期项；
-   普通文本伪装 SRS（magic 不是 `SRS` 或 zlib 解压失败）；
-   二进制版本不为 2；
-   source 与 binary 语义不一致（用固定解析器读取，反编译后作有边界的结构等价比较，并在两者上运行同一正反例）；
-   source/destination 方向错误；
-   未授权的大范围匹配；
-   `status: optional` 条目被显式纳入却不在 `enabled_optional`，或共享项未标记、缺单独验收；已启用功能缺失 `feature-required` 项。

三个 SRS 必须真实解析。

候选模式仅豁免正式批准与未到期要求，不豁免字段存在、已知 `review_status`、来源和合法日期形态；它要求证据如实支持所声明的历史收录/观察结论，不要求待验证结论事先成立。`null` 只适用于从未完成有效性复核的 `pending`。正式模式按固定 `review_as_of` 判定，发布门槛按当前 UTC 日期重判，不能相互替代。回归必须覆盖：普通/关键兼容使用同一判据、纯历史证据不能获批、缺字段、`pending`、未来验证日期、到期前一天/当日/后一天、超过 30 天窗口，以及旧基准日期可重建但当前已过期不能发布。证据、复核状态和日期变动均进入 semantic diff。

### 匹配测试工具

- `sing-box rule-set match -f binary <file>.srs <domain|ip>` 只把参数写入 `Destination`（IP）或 `Domain`（域名），**不设置来源地址**，因此只能用于 destination / domain 正反例；`-f` 默认值为 `source`，测试 `.srs` 必须显式传 `-f binary`。命中时向 **stderr** 打印 `match rules.[i]: ...`，不命中不打印，两种情况都正常退出 0。必须先检查退出码，再在 stderr 中判定命中；不能只看退出码或 stdout。
- 来源方向、`source_ip_cidr` 与 `ip_cidr` 同时存在的组合，由 `tests/harness/` 用固定 sing-box Go module 执行：加载 `.srs`（`srs.Read`），`rule.NewHeadlessRule` 构造规则，分别以 `adapter.InboundContext{Source: ...}` 与 `{Destination: ...}` 断言。每个测试、每个 OR 分支使用全新或按上游规范重置的 metadata，避免缓存污染。Go harness 必须使用最终目标版本的 sing-box 与其 go.mod 锁定的 sing；不能只在更新的 sing 依赖上测试旧发布版。另须按 §4.2 测试外层消费者组合，不能以孤立 headless MATCH 代替。

### Anthropic IP 方向测试

每条测试清空 Domain/FQDN 等其他匹配条件，只设置所写的 Source 或 Destination；不得因同一 metadata 留有域名命中而误判 IP 方向。来源与目的分别测试，不将两者都填写后推断方向。

``` text
destination 160.79.104.10 -> anthropic.srs 命中
destination 160.79.106.1  -> anthropic.srs 不因 Anthropic IP 命中（/21 内、/23 外）
source      160.79.106.1  -> anthropic-ip.srs 命中
destination 160.79.106.1  -> anthropic-ip.srs 不命中
source      160.79.112.1  -> anthropic-ip.srs 不命中（/21 外）
source / destination 34.162.46.92、34.162.102.82、34.162.136.91、34.162.142.92、34.162.183.95
                          -> 三个制品均不命中
```

每个 suffix 测试以下边界；regex 按它自身经审阅的语言生成正反例，不套用“任何子域都命中”的 suffix 模板：

``` text
apex          domain_suffix ".x" -> NO MATCH；domain_suffix "x" -> MATCH
一层子域      MATCH
多层子域      MATCH
lookalike     notx.tld、x.tld.example.org -> NO MATCH
错误父域      NO MATCH
```

## 10. 范围扩大保护

每次上游更新必须输出：

``` text
added/removed domain
added/removed domain_suffix
added/removed regex
added/removed CIDR
新出现的父规则覆盖关系
source/destination 变化
provenance 变化
official snapshot 变化
```

以下是项目硬拒绝项，不设普通人工批准旁路：`domain_keyword`、公共后缀、整个公共云/CDN 父域、`0.0.0.0/0`、`::/0`、错误方向、伪 SRS、无来源数据。厂商明确列出的共享范围（如 `*.intercom.io`）须以逐条官方例外登记，不能类推到其他公共后缀。

其余扩大范围、source/destination 转换、feature/optional 状态变更及新 CIDR 均暂停到审阅完成；严重缩小范围也需审阅。优先 exact，其次有明确域边界的 suffix。regex 使用 Go RE2；必须每条分支都限定在经证据允许的域内，不能仅检查字符串有 `^`、`$` 和一个域名字面量。

反例 `^(?:allowed\.example\.com|.*)$` 满足 v1.3 的表面判据却命中任意域名，本次已复现。采用小型已批准表达式清单及其测试，不声称靠几个正则检查即可证明任意 regex 安全。社区 `^chatgpt-async-webps-prod-\S+-\d+\.webpubsub\.azure\.com$` 仅登记候选；先核实需求，再审阅 `\S+` 可跨点号的问题。缩窄表达式也会改变覆盖范围，必须写 diff，不能自动替换后仍称“与上游等价”。

源 JSON 与反编译 JSON 不要求文本逐字相等：排序、listable 单值/数组、exact + 点后缀与 root suffix、冗余覆盖及 CIDR 合并可能不同。只为已准许字段实现可证明的等价规范化，保留前导点与方向；regex 默认只能同表达式比较。未知结构、logical/invert、额外字段出现即阻断人工审阅。有限测试补充等价检查，不能单独证明任意规则全集相等。

## 11. OpenAI 基线策略

当前官方网络页的 29 项按下表分别登记，避免 v1.3 把 `*.oaistatic.com` 错映射为 `.openai.com`。来源 [O1]；额外 apex 依据登录排障 [O2] 与 WebSocket 说明。

| 类型 | 值 |
|---|---|
| 仅子域 suffix（均保留前导点） | `.auth.openai.com`、`.chatgpt.com`、`.ct.sendgrid.net`、`.intercom.io`、`.intercomcdn.com`、`.oaistatic.com`、`.oaiusercontent.com`、`.openai.com`、`.oaistatsig.com` |
| exact | `android.chat.openai.com`、`auth0.openai.com`、`cdn.openaimerge.com`、`cdn.workos.com`、`challenges.cloudflare.com`、`chat.openai.com`、`desktop.chat.openai.com`、`forwarder.workos.com`、`humb.apple.com`、`images.workoscdn.com`、`ios.chat.openai.com`、`js.intercomcdn.com`、`js.stripe.com`、`o207216.ingest.sentry.io`、`o33249.ingest.sentry.io`、`rum.browser-intake-datadoghq.com`、`setup.auth.openai.com`、`setup.workos.com`、`tcr9i.chat.openai.com`、`workos.imgix.net` |
| 额外保留的 exact/provenance | `auth.openai.com`、`chatgpt.com`、`openai.com`、`ws.chatgpt.com`；可在制品中覆盖消重，canonical 保留依据 |

WebSocket 还需消费者允许 TCP 443 协议升级和持续连接；仅 SRS MATCH 不能证明代理支持该协议。官方列出的共享域名不得因“像遥测”而删去；全部标注影响其他软件访问的范围。

**Voice**：当前 [O1] 指向 [O4] 的服务器 IP，优先 UDP 3478，受限时使用 TCP 443。本次 JSON 的 `creationTime` 是 `2026-03-26T20:12:45.451356+00:00`，包含 23 个 IPv4 `/32`。默认 Voice 范围将这些固定快照前缀按 `ip_cidr`、`direction: destination`、`status: feature-required`、`features: [chatgpt-voice]` 纳入 `openai.srs`。IPv6 前缀如后续出现，按字段和方向审阅再纳入。拒绝空前缀表、非法 CIDR、未知前缀字段；任何变化先归档、diff 和验收，不在生成时临时联网拼入。

SRS 的 `ip_cidr` 不限制端口：它会匹配该地址的其他端口流量，消费者需知晓这个范围。网络放行规则另按官方端口配置，不能误将目的域与目的 IP 写在同一默认规则中期待 AND，也不能给整个 OpenAI 集合只加 UDP 3478 限制。

当前官方页面不再以 LiveKit 说明 Voice。社区的 `chatgpt.livekit.cloud`、`host.livekit.cloud`、`turn.livekit.cloud` 留作历史兼容候选，不因 2024 年副本直接进入正式集。其他 Tier 1 差集如 `chat.com`、`sora.com`、`crixet.com`、`chatgpt.site`、Azure/imgix 主机、遥测与 regex，同样逐条核验产品归属、用途及范围；社区存在不等于官方批准。

## 11.1 OpenAI 登录与 Cloudflare 验证保护

适用于 ChatGPT Web、客户端的浏览器登录，以及 Codex 使用的 OpenAI 登录链路。目标是避免规则遗漏、共享域名分流冲突或会话中出口变化造成的验证失败、反复验证和登录循环；不承诺消除厂商正常安全验证。规则命中不能证明客户端 Cookies、JavaScript、扩展或服务端风控正常。

2026-09-27 用户提供的 `截屏2026-09-27 20.41.52.png` 显示 `auth.openai.com` 的 Cloudflare 安全验证。该截图只证明出现验证页面；未提供路由日志、实际出口 IP、客户端版本和完整验证结果，不能据此认定 IPv6、漏规则或出口变化是本次原因。

`openai.srs` 必须满足以下增补要求，依据见 §11.4：

- `challenges.cloudflare.com` 是 OpenAI 官方 allowlist 条目（本次当前官方正文已核实），使用精确 `domain`、`status: required`，并标记 `shared_dependency`；不得降为无官方依据的社区兼容项，也不得扩大为 Cloudflare 公共后缀。
- `auth.openai.com`、`chatgpt.com`、`openai.com` 作为明确的 apex 保留在 canonical：通配符转换不能隐含 apex；按 [O2] 的本站登录/Cookies 范围补充 exact，保留独立依据。若最终制品做覆盖消重，必须保留来源并验证这三个主机仍命中。
- 认证、WorkOS、静态资源和 WebSocket 依赖继续按 §11 官方基线纳入；第三方登录 provider 按实际启用方式验收，不因此扩大为整个 Google、Microsoft 或 Apple 地址空间。

## 11.2 两个产品共用的 Challenge 与出口契约

本节是 OpenAI 与 Claude 的共享运行时契约，§12.1 引用本节。它属于本项目的兼容性设计；厂商没有承诺使用同一代理即可免除验证。

`challenges.cloudflare.com` 同时进入 `openai.srs` 与 `anthropic.srs`；OpenAI 侧有官方依据，Claude 侧由维护者确认的历史验证批准，详见 §12.1。新批次的整体发布资格仍须通过 §14。该域名也服务于其他使用 Turnstile 的网站（Cloudflare Turnstile CSP 要求 `script-src` 与 `frame-src` 放行 `https://challenges.cloudflare.com`；pre-clearance 还会请求站点自身的 `/cdn-cgi/` 路径，该 CSP 资料本身只证明资源加载要求，不直接证明所有 Turnstile 模式都有同一源 IP 的约束）。精确域名规则仍无法辨认它属于哪个浏览器标签页；`product` 和 `shared_dependency` 元数据不会给 SRS 增加网页归属判断能力。

同一客户端同时启用两个集合时，本项目默认将两产品的主站、认证链路和共享 Challenge 路由到同一固定实际出口，作为降低冲突的保守运行契约，不宣称这是所有 Turnstile 模式的官方强制要求。若必须让 OpenAI 与 Claude 使用不同出口，须使用能保持会话归属的独立浏览器环境和入站等隔离方式，并分别验收；仅调整两个 SRS 的顺序，或按同一个浏览器进程匹配，不能解决标签页间的共享域名冲突。其他网站访问该共享 host 也会受到所选路由影响，消费者必须知晓这一范围。

验收区分以下三层，不得相互替代：

1. **匹配层**：主站、认证和 Challenge 的 IPv4/IPv6 流量均进入预期策略；存在 AAAA 时不得从客户端绕过该策略。使用域名规则必须有实际可用的目的域名信息，不能把离线域名 MATCH 当作透明代理现场已经可识别。
2. **出口层**：记录最终实际 outbound、地址族和实际对外源 IP。固定策略名、节点名、地区或 ASN 均不能证明源 IP 稳定；URLTest（默认 `interval 3m`、`tolerance 50`，`interrupt_exist_connections` 只作用于入站连接）、故障切换和多地址 NAT 可能改变实际出口。挑战开始到完成期间保持实际出口稳定，不能只验相同 policy。若出口失效，停止当前认证并在出口稳定后重新开始，不把旧会话的验证状态视为仍有效。
3. **会话层**：验证正常登录及返回业务页面；若自然出现 Challenge，由用户完成正常验证并记录是否循环。Cloudflare 明确限制 Managed Challenge 的签发与解答使用不同 IP（"the solve is not valid and you may encounter a Challenge loop"）；这不等于已证明所有 OpenAI/Claude 验证或双栈问题均由 IP 差异造成。

可以让代理内部为相关认证会话使用稳定 IPv4 出口，但这是需验收的局部兼容选择；不要求全局关闭 IPv6。双栈下无法取得实际出口或会话证据时标为未验证，不能宣告出口一致性通过。

## 11.3 强制回归与失败分支

每次生成对实际 `openai.srs` 验证下列域名，不能只验证生成前的 YAML：

```text
auth.openai.com                       MATCH
setup.auth.openai.com                 MATCH
chatgpt.com                           MATCH
ws.chatgpt.com                        MATCH
openai.com                            MATCH
api.openai.com                        MATCH
challenges.cloudflare.com             MATCH
www.challenges.cloudflare.com         NO MATCH
cloudflare.com                        NO MATCH
www.cloudflare.com                    NO MATCH
example.cloudflare.com                NO MATCH
notopenai.com                         NO MATCH
auth.openai.com.example.org           NO MATCH
challenges.cloudflare.com.example.org NO MATCH
```

发布还须执行两个 SRS 同时加载的集成测试：使用最终消费者规则顺序，核查 OpenAI 主站、`auth.openai.com`、Claude 主站及共享 Challenge 的实际 outbound。故意给两产品设置不同出口且未隔离的配置必须被报告为冲突、禁止作为受支持配置发布；不能因两个集合各自通过 MATCH 测试而放行。

固定目标 sing-box 版本、消费者配置摘要和制品哈希，在 IPv4、IPv6、双栈环境分别记录匹配、实际出口和登录结果；不存在的地址族或未覆盖的客户端标为未验证。无 Challenge 的一次成功登录只证明该次登录成功，不证明 Challenge 路径已经通过。正式发布需有目标支持环境的有效集成记录，未测试的环境不纳入已验证范围；策略、出口或相关规则变化后重验受影响项。

异常按证据分支处理：

- 有漏匹配、非预期直连、共享域名冲突或会话中出口变化：停止新批次发布，保留上一批准批次；修正后重跑受影响验收。
- 路由与出口检查通过，但页面仍循环：转入 OpenAI 官方登录排障；官方建议包括停用 VPN/代理作对照、检查本站 Cookies/JavaScript、扩展和网络过滤。本方案的代理出口稳定契约不是 OpenAI 官方免验证建议；在符合访问条件的网络按官方路径排查（Cloudflare 同时说明修改 User-Agent 或 Canvas/WebGL 等 Web API 的浏览器扩展不受支持）；在符合访问条件的网络做对照，不通过添加无证据域名或轮换出口求解。
- 出现正常人机验证：交由用户完成，不自动点击或解题。若持续失败，保留日期、环境、请求 ID、脱敏日志与结果，标记会话验收未通过；先确认原因，不自动反复登录。普通验证提示本身不作为规则集失败判据。

## 11.4 官方依据索引

核对日期均为 2026-09-27；页面事实通过正常网页正文工具核对，GitHub/JSON 由 HTTPS 获取；没有手工登录或解决验证页。当前页面不是不可变历史来源，实施入库时依 §3 保存实际输入及哈希。以下链接也是恢复依据，不依赖旧审计报告。

| 编号 | 直接来源 | 用途 |
|---|---|---|
| O1 | [OpenAI Network recommendations](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps) | 当前 allowlist、WebSocket、Voice |
| O2 | [OpenAI 登录排障](https://help.openai.com/en/articles/7426629-why-cant-i-log-in-to-chatgpt) | 登录与验证循环、Cookies/JavaScript |
| O3 | [CAPTCHAs in ChatGPT](https://help.openai.com/en/articles/8184038-captchas-in-chatgpt) | 正常验证与持续出现时的排查 |
| O4 | [Voice JSON](https://openai.com/chatgpt-voice.json) | Voice 客户端服务器目的 IP |
| A1 | [Anthropic IP addresses](https://platform.claude.com/docs/en/api/ip-addresses) | inbound/outbound/phased-out；AWS 区分 |
| A2 | [Claude Code network config](https://code.claude.com/docs/en/network-config) | 核心、安装、Artifact、可选依赖 |
| A3 | [Claude Desktop 网络要求](https://code.claude.com/docs/en/desktop#network-access-requirements) | Desktop 域名、字体与库 CDN |
| C1 | [Cloudflare Challenge 限制](https://developers.cloudflare.com/cloudflare-challenges/concepts/how-challenges-work/#limitations) | Managed Challenge 不同 IP 签发/解答限制 |
| C2 | [Turnstile CSP](https://developers.cloudflare.com/turnstile/reference/content-security-policy/) | 共享脚本/iframe 和 pre-clearance 路径 |
| S1 | [Source Format](https://sing-box.sagernet.org/configuration/rule-set/source-format/)、[Headless Rule](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/)、[Route Rule](https://sing-box.sagernet.org/configuration/route/rule/) | 格式版本、字段与外层语义；精确实现以 §4.2 为准 |
| S2 | [URLTest](https://sing-box.sagernet.org/configuration/outbound/urltest/) | 自动节点选择及连接切换 |
| D1 | [DLC 固定 openai](https://github.com/v2fly/domain-list-community/blob/bcea25493ed28c387660fe49ce1ceb242d2efca0/data/openai)、[anthropic](https://github.com/v2fly/domain-list-community/blob/bcea25493ed28c387660fe49ce1ceb242d2efca0/data/anthropic) | 社区发现源 |
| D2 | [sing-geosite 固定规则提交](https://github.com/SagerNet/sing-geosite/tree/e6a8117545c35a17c508e3f37a9a990571234428) | 最新可见派生 SRS 交叉核对 |

## 12. Anthropic 基线策略

`anthropic.srs` 以 Claude Code、Claude Desktop 和 Anthropic 官方网络资料为最低集合，并合并经验证的可信上游差集。

官方条目处置（2026-09-27 核对）：

| 官方条目 | 来源 | 处置 |
|---|---|---|
| `anthropic.com` + `*.anthropic.com`、`claude.ai` + `*.claude.ai`、`claude.com` + `*.claude.com`、`claude.app` + `*.claude.app` | Desktop | `domain_suffix` 无前导点，`required` |
| `*.claudeusercontent.com`、`*.claudemcpcontent.com` | Desktop | `domain_suffix: ".x"`；apex 是否需要按 §4.1 登记 |
| `api.anthropic.com`、`platform.claude.com`、`mcp-proxy.anthropic.com`、`downloads.claude.ai`、`bridge.claudeusercontent.com`、`*.frame.claudeusercontent.com`、`code.claude.com` | Claude Code | 已被上行后缀覆盖，provenance 保留精确来源 |
| `github.com`、`raw.githubusercontent.com`、`registry.npmjs.org`、`storage.googleapis.com`、`formulae.brew.sh` | Claude Code 安装/插件/变更说明/Homebrew 路径 | 默认声明支持这些路径：`feature-required` + `shared_dependency: true`；不声称每次模型调用均依赖它们 |
| `cdnjs.cloudflare.com`、`cdn.jsdelivr.net`、`cdn.tailwindcss.com`、`code.jquery.com`、`unpkg.com` | Claude Code / Desktop：依赖库的 Artifact 无加载回退 | `feature-required` + `shared_dependency: true`，默认纳入；不能与有字体回退的项目一律删除 |
| `*-review.googlesource.com`、`http-intake.logs.us5.datadoghq.com`、`browser-intake-us5-datadoghq.com`、`fonts.googleapis.com`、`fonts.gstatic.com` | Gerrit 非必要发现、可关闭遥测、字体有回退 | `optional`，默认不额外纳入；如启用 Gerrit 通配符须保持单个 label 内 `*-review` 的语义，不能扩成 `.googlesource.com` |
| Tier 1 差集：`clau.de`、`claudemcpclient.com`、`full:servd-anthropic-website.b-cdn.net` | v2fly | 按 §4 六项判断后登记为候选或 `ALREADY_COVERED` |

共享依赖如 GitHub、npm、Google Storage 必须标记 `shared_dependency`，因为按域名分流会同时覆盖其他软件访问。

Provider（AWS/Bedrock、Google Cloud、Microsoft 等）不默认并入 Claude 主集合。只有用户实际启用相应 provider 时才建立独立 profile；不得把整个 AWS/Google/Azure 地址空间纳入 `anthropic.srs`。官方 IP 页面说明 Claude Platform on AWS 的 inbound 端点 `aws-external-anthropic.{region}.api.aws` 解析到 AWS 地址段，属于 provider profile 范围。

Anthropic 官方当前稳定 IP：

``` text
Inbound:
160.79.104.0/23
2607:6bc0::/48

Outbound source:
160.79.104.0/21
```

已 phased-out 的五个旧 `/32` 必须进入负例：

``` text
34.162.46.92/32
34.162.102.82/32
34.162.136.91/32
34.162.142.92/32
34.162.183.95/32
```

## 12.1 Claude Cloudflare Challenge 与双栈出口一致性

`challenges.cloudflare.com` 作为精确 `domain`、`compatibility-critical`、`shared_dependency: true` 纳入 Claude 维护数据。

历史依据：旧仓库提交 `8a516762efb09332f4fcdd2aecccdfcf6916ecfd` 的 `domains.yaml` 已收录该精确规则。本次维护者明确确认此前已验证，并指定旧仓库更新日期就是验证日期。最近更新提交为 [`1f6e61caa9f8c157771e2e48a9084ded3cb4caa2`](https://github.com/YouM1225-1/anthropic-claude-surge-rules-set/commit/1f6e61caa9f8c157771e2e48a9084ded3cb4caa2)，提交时间为 `2026-09-27T09:55:30Z`（北京时间 17:55:30）。提交时间用于定位维护者指定的日期，提交本身不证明运行结果。

批准记录见 [`sources/evidence/claude-challenge-confirmation.json`](../sources/evidence/claude-challenge-confirmation.json)，状态为 `approved`，`first_seen` / `last_verified` 均为 `2026-09-27`，`review_after` 为 `2026-10-27`。精确客户端、版本与环境未提供，保持 null；不能据此宣称所有平台、新批次 SRS、IPv4/IPv6 出口均已验收。

旧仓库中的 `cdn.growthbook.io`、`cdn.usefathom.com` 与 `clau.de` 继续作为发现输入，sync 明确分类；本次确认只批准 Challenge 精确规则，不扩展到其他历史条目或整个 Cloudflare 后缀。官方单列的 `cdnjs.cloudflare.com` 继续作为 Artifact 功能必需 exact。

共享出口与双栈验收按 §11.2–§11.3。两个目的集合必须验证以下关键反例与正例：

```text
challenges.cloudflare.com              MATCH
www.challenges.cloudflare.com          NO MATCH
cloudflare.com                         NO MATCH
www.cloudflare.com                     NO MATCH
example.cloudflare.com                 NO MATCH
challenges.cloudflare.com.example.org  NO MATCH
claude.ai                              MATCH（anthropic）
claude.app                             MATCH（anthropic）
notclaude.ai                           NO MATCH
cdnjs.cloudflare.com                   MATCH（anthropic，Artifact）
```

确认规则有效，不等于确认旧问题必然由 IPv6 或出口变化造成。现网根因仍由流量、实际出口与会话证据判断；正常验证由用户完成，不自动解题或重复登录。

## 13. manifest

每个隔离批次包含 `manifest.json`，记录 schema、项目版本、build_mode、review_as_of、source_commit、全部 sources/scripts/tests 输入哈希、固定 upstream 快照、compiler 版本/平台/哈希、features、enabled_optional、source/binary version、单条 default 结构、规范化记录，以及三个 artifact 的路径、源 JSON 哈希、二进制哈希、大小和方向。

validator 追加源/二进制匹配用例数、结果哈希、重建一致性、固定 Go/sing-box/sing 依赖及 harness 摘要。`validated_consumers` 只有通过指定批次的集成证据检查才填写；本地 check 不会自动填充。发布审阅记录由 `sources/release-review.json` 引用，维护者的 Challenge 确认与新批次集成记录分别保留。

正式发布时将同批次三个 `dist/*.srs` 和 manifest 放入同一 Git 提交。source_commit 指生成输入的提交，不试图在 manifest 内自引用尚未产生的发布提交。manifest 不是可信身份；真实性仍依赖固定 commit、代码审阅和发布权限。

## 14. 发布门槛

发布必须同时满足：

1.  Tier 0 官方基线完整，`required` 与已启用的 `feature-required` 均指向已登记快照；
2.  Tier 1 补集全部经过分类；
3.  无 unresolved official conflict；
4.  无未知 provenance；
5.  三个 SRS 可真实解析，二进制版本为 2；
6.  source 与 binary 语义一致（受限结构等价 + 两侧实际匹配，见 §10）；
7.  Anthropic inbound/outbound 方向正确（harness 断言，含五个 phased-out 负例）；
8.  正反例全部通过（含 §4.1 apex/子域期望）；
9.  两次 clean build 字节一致；
10. semantic diff 已审阅；
11. 三个 artifact 和 manifest 同一 commit；
12. 固定目标 sing-box 运行时完成加载测试。
13. §11.3 与 §12.1 的回归通过；跨制品共享域名冲突已处理，声明支持的目标环境具有匹配、实际出口和会话验收记录。
14. 所有兼容项符合 §3；`build_mode` 为 `release`，发布前以实际当前 UTC 日期复查，无待核验、到期或证据不足项。历史重建通过不能代替此项。
15. `features` 与 `enabled_optional` 固定且与实际制品一致；可选项被显式纳入时有单独验收，共享项如实标记。继承自已批准 suffix 的覆盖关系单独报告，不把 optional 未纳入解释为已阻断。
16. §4.2 的单条 default 结构及消费者组合契约通过目标版本验证；作用于两个目的集合的来源改写开关均为 false；Voice、Artifact、插件等声明支持功能有对应端到端结果。

任何一项失败，不覆盖上一批已批准制品。

## 15. 更新策略

更新触发：

-   OpenAI/Anthropic 官方网络资料变化（以快照 diff 为准）；
-   Tier 1 上游固定 commit 更新；
-   实际故障或抓包发现缺失端点；
-   sing-box rule-set 格式变化（新的 Source Format 版本或 `compile` 降级规则变化）；
-   共享依赖、消费者路由顺序或认证会话出口策略变化；按 §11.3 重验受影响环境；
-   任一兼容项到达 `review_after`，或发现证据失效、适用产品变化；两种兼容类别均进入复核。

流程：

``` text
refresh and archive official snapshots (record actual method)
→ fetch fixed upstream
→ normalize (§4.1)
→ compare official baseline
→ generate candidate diff
→ review additions/removals
→ generate
→ semantic validation (source/binary + consumer composition + metadata)
→ clean rebuild
→ publish one commit
```

GitHub Actions 每天 02:17 UTC 检查复核到期情况，每次正式发布前 validator 再按实际 UTC 日期检查；工作流只有读取和上传候选附件权限，不自动修改规则、发布或部署。`pending`、到期或失去依据的条目阻断新批次，不能自动重用旧批准结果。上一批准批次不会因日期变化被自动撤销、删除或重写，但也不能将继续运行解释为重新通过复核。

复核只有两条完成路径：补充有效证据并按 §3 重新批准；或者经审阅决定删除/替换。删除/替换说明须记录原条目标识、前一批准版本或本次候选、证据、理由、受影响产品及回归结果，绑定到同次 semantic diff 的提交/PR 审阅记录；§14 的审阅门槛拒绝没有对应处置说明的删除，不能只删条目来消除到期报错。仍在列表中的到期项不能靠处置说明放行；继续保留就必须重新批准。

"复核后无法继续建立有效依据"是允许删除普通兼容项的明确理由，不必等到发生故障。`compatibility-critical` 不能仅凭无证据直接从正式集合删除：须先有替代规则覆盖或受影响核心流程在移除后的验收证据；没有证据则保留待核验并停止新批次。修改 §12.1 必测域名还必须同步其回归预期与依据，不能静默跳过测试。目标是持续完善，不能通过仅顺延日期、降级关键类别或跨产品继承批准来积累无依据规则。

## 15.1 当前执行计划

目标：项目 0.1.0、设计修订 1.7。实现与现场验收分别记状态。

| 步骤 | 成功终点 | 当前状态 |
|---|---|---|
| 既有审计与 1.15 精确版本核验 | 16 项核验与历史证据可定位 | 已完成；历史验证见 §17，不作为新批次自动验收 |
| 建立规则仓库 | 三份维护数据、官方/社区归档、锁文件、来源许可、构建与验证代码 | 已实现；版本及当前检查状态以 README 为准 |
| Claude Challenge 兼容批准 | 保留维护者确认及原验证日期 | 已批准；见 §12.1，复核截止 2026-10-27 |
| 本地与 CI 验证 | 元数据反例、真实 SRS 匹配、来源方向及重建一致性通过 | 执行结果记录在 README / 工作流附件；不代表现场流量 |
| 新批次发布审阅 | 语义差异与三制品哈希、消费者配置及集成证据绑定 | 待执行；`sources/release-review.json` 仍 pending |
| 正式制品与配置接入 | 同一提交发布三个 SRS，取得实际版本后再合并客户端 | 待发布门槛；N100 保留原有四条产品路由位置 |
| 设备验收与恢复 | 加载、DNS/TUN、出口、登录、功能与重启持久化 | 待目标设备执行；失败保留/恢复上一批准批次 |

本地检查失败可修复后重测；正式发布门槛失败则不发布。仓库初始化不推定生产配置已经部署。

## 16. 正式结论

`YouM1225-1/sing-box-ai` 作为唯一规则仓库，只承担三个清晰职责：

``` text
openai.srs       = OpenAI / ChatGPT / Codex 客户端目的规则
anthropic.srs    = Claude / Anthropic 客户端目的规则 + 官方 inbound IP
anthropic-ip.srs = Anthropic outbound source IP
```

规则数据采用"官方基线 + 可信上游补集 + 已验证兼容补集"的合并模型。官方事实优先，第三方只补缺；不执行第三方代码，不在正式构建时读取浮动 ref；固定对象及输入字节同时归档，不把动态 CDN 的瞬时 IP 固化为永久规则，不通过过宽后缀追求表面上的"全覆盖"。

最终验收标准不是规则数量，而是：**覆盖充分、方向正确、来源可追踪、构建可复现、语义可测试、更新可审计。**

## 17. 历史审计与当前验证

2026-09-27 的前期审计已固定 alpha.9 与 testing commit，验证两个源码/依赖组合的 720 次 source/binary 断言，并运行 220 个上游测试/子测试 pass 事件。这些属于原审计环境的历史证据；当前仓库每次构建均重新执行自己的校验，不把历史计数冒充当前通过数量。

当前 validator 使用正式固定编译器解析三个真实 SRS，分别在 source 与 binary 上测试域名边界及来源/目的 IP，执行独立重编译与隔离运行时构造检查。当前结果位于对应批次 manifest、matches.jsonl 和 GitHub Actions 的 candidate 附件。`check` 不等于 TUN/nft、DNS 实际报文、最终源 IP、登录、Voice/Artifact/插件或重启验收。

## 18. 客户端接入契约

本阶段先建立并验证规则仓库。正式批次发布、固定 commit 与 SHA256 确定后，才处理真实客户端配置；本仓库不保存含节点凭据的 N100/iOS/TV 配置。

- 保留消费 tag `geosite-openai`、`geosite-anthropic`，只将它们的两个来源 URL 指向同一正式发布提交下的 `dist/openai.srs`、`dist/anthropic.srs`；下载继续复用实际 `proxy-http`。通用 `geosite-ai` 保留原来源。
- **保留原来的 route.rules 顺序与对象**。OpenAI IPv6 reject → OpenAI proxy → Anthropic IPv6 reject → Anthropic proxy 继续在 Google/YouTube 之后、通用 geosite-ai 之前；保留原 QUIC 规则，不新增 AI 专用 QUIC reject。没有实际重叠证据时不整体前移。
- DNS 审核方案保留两条 AI 规则的前移：AAAA predefined 空 NOERROR，然后 dns_proxy；实际实施时按原对象内容和业务规则锚点移动，避免重复。Direct/Global、私网与端侧例外保持各自契约。
- N100 的内核 geoip-cn 旁路发生在用户态规则之前，调整路由顺序不能收回旁路流量。客户端到 VPS 使用 IPv4 也不证明 VPS 连接业务目标使用 IPv4；两者分别验收。
- `anthropic-ip.srs` 使用 source_ip_cidr，只用于确有此需求的服务端来源识别；不加入客户端或当前 Hysteria2 入站白名单，不打开来源改写开关。
- 客户端同步须同一次处理公共规则、三端差异、派生配置、安装摘要与原机 check；只有本地 JSON 通过不足以部署。macOS 无法替 N100 验证 Linux auto_redirect。
- 首次切换前保存原配置与原 SRS 字节/哈希；下载完整 SRS、校验同批次哈希并确认实际加载。缓存存在不代表已使用新规则，不清空整个 cache.db。

本仓库提供设计与规则制品。生产部署以目标环境的配置契约、现场证据及用户授权为准。
