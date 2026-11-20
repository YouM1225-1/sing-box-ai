# one-exit 提交与本仓库 v0.1.6 域名 / IP 规则对比

核对对象：[wquguru/one-exit 提交 `b9d9f8ab6687401f7588dfa7d7023cd58ffb4032`](https://github.com/wquguru/one-exit/commit/b9d9f8ab6687401f7588dfa7d7023cd58ffb4032)，提交时间为北京时间 **2026-10-21 09:35:18**。本地基线是 HEAD `ad7c86f9e36c4be232a1523b030e6de46efba191`、VERSION `0.1.6`，实际检查 [v0.1.6 本地归档](../artifacts/v0.1.6/)与 `dist/`；本次没有重新下载 GitHub Release 制品。

**结论：该提交主要改变“流量怎么分流”，没有提供新的 OpenAI/Anthropic 官方清单证据。** 它拒绝两段 Anthropic IPv6 前缀，并把支付、验证码、遥测等共享服务送入住宅代理。本仓库的 Anthropic 目的 IP 已包含这些 IPv6 和 IPv4 范围；新增域名表达式则有完整、部分和未对应覆盖的情况，不能称为与对方模板完全一致，也不能据此认定本仓库遗漏了必需依赖。

本仓库这三份 SRS 保存匹配条件，不包含 `REJECT` 或住宅出站动作，也没有对方的 ASN、进程匹配条件。两者需要分别比较地址范围、域名范围和消费端行为。

文内导航：[提交变化](#change) · [IP 对照](#ip) · [32 条域名对照](#domains) · [本仓库基线与反向差异](#repo) · [处理建议](#recommendation) · [验证证据](#verify)

<a id="change"></a>

## 1. 提交改了什么

提交修改 5 个文件，共 **64 行新增、4 行删除**：

- Clash Party、FlClash、Shadowrocket 三个模板都新增最前面的 `IP-CIDR6,2607:6bc0::/48,REJECT,no-resolve` 和 `IP-CIDR6,2607:6bc0:11::/48,REJECT,no-resolve`。
- 原先把 `2607:6bc0::/48` 送往住宅代理的规则被移除；`160.79.104.0/21` 仍送往住宅代理，并保留/补充 `IP-ASN,399358` 的目的地址分流。
- 三模板新增域名表达式并集为 **17 条：14 条后缀、3 条关键词**。其中 `anthropic`、`claude` 关键词本来已存在于 FlClash；`modelcontextprotocol.io` 及 FlClash 的 `modelcontextprotocol` 也不是本提交新增。
- 新增后缀/关键词的逐项差异见[结构化独立复核](evidence/one-exit-b9d9f8a-2026-10-21/independent-domain-review.md)和[模板前后规则差异](evidence/one-exit-b9d9f8a-2026-10-21/template-rule-diff.json)。

完整模板的去重并集是 **39 条表达式：32 条域名、3 条 CIDR、1 条 ASN、3 条进程规则**。其中 17 条域名表达式在至少一个模板中新增；按三个旧模板的并集计算，首次出现的只有 15 条。

| 模板 | 提交前规则数 | 提交后规则数 | 本次新增域名表达式数 |
|---|---:|---:|---:|
| Clash Party | 17 | 35 | 17 |
| FlClash | 18 | 34 | 15 |
| Shadowrocket | 16 | 35 | 17 |

三端行为不完全相同：FlClash 用 `pin.concat(config.rules || [])` 把 pin 规则放到原配置前；Clash Party 和 Shadowrocket 的提交后规则列表相同。FlClash 还保留以下三个既有 `PROCESS-NAME`，均送到 `SG_Residential`：

| 进程/Android 包名 | 作用对象 | 本仓库对照 |
|---|---|---|
| `com.anthropic.claude` | Claude 应用 | 三份产品 SRS 均无该进程条件 |
| `com.android.vending` | Google Play | 同上 |
| `com.google.android.apps.walletnfcrel` | Google Wallet | 同上 |

进程匹配依赖客户端捕获连接并识别包名，范围不限于已列域名；这不表示 sing-box 不支持进程规则。提交中的检查器只检查部分静态格式，新增 IPv6 断言没有检查 FlClash 的 pin 列表，也没有验证真实出口、IPv4 回退、代理链或 502。

<a id="ip"></a>

## 2. IP 规则对比

| 地址/范围 | one-exit 提交 | 本仓库 v0.1.6 | 对比结论 |
|---|---|---|---|
| `160.79.104.0/21` IPv4 | `IP-CIDR` 目的地址 → `SG_Residential` | `anthropic.srs` 目的 `ip_cidr` | **目的范围相同，本仓库不指定出站动作**；另有独立 `anthropic-ip.srs` 的 `source_ip_cidr`，方向不是目的路由 |
| `2607:6bc0::/48` | 目的地址 → `REJECT` | 被目的 `2607:6bc0::/32` 包含 | **本仓库匹配范围更宽，但不规定拒绝** |
| `2607:6bc0:11::/48` | 新增目的 `REJECT` | 同样被 `2607:6bc0::/32` 包含 | **已覆盖地址范围；拒绝行为只在对方消费者模板中存在** |
| `IP-ASN,399358` | 目的地址按客户端 ASN 数据 → `SG_Residential` | 没有 ASN 规则，使用显式 CIDR | **语义不同**；ASN 可能覆盖该 ASN 的其他地址，不能当作固定 CIDR 等价物 |
| OpenAI Voice 23 个 `/32` | 未出现 | `openai.srs` 已包含 23 个 `/32` | 对方提交不涉及 OpenAI Voice IP |
| OpenAI 其他 IP / 官方出站 feed | 未出现 | 本仓库也不把服务端出站 feed 当客户端目的规则 | 无新增可合并项 |

当前 RIPE AS399358 观测到的 `160.79.104.0/23`、`2607:6bc0::/48`、`2607:6bc0:11::/48` 均被本仓库现有规则包含；证据见 [RIPE 快照](evidence/one-exit-b9d9f8a-2026-10-21/ripe-as399358.json)，抓取于北京时间 2026-10-21 13:22，数据最新时间为当日 08:00。ASN 匹配依赖客户端的 IP→ASN 数据，不是实时 BGP 查询；当前包含不保证未来仍然完整。AS 公告本身也不证明每个地址都承载 Claude，或住宅代理必须拒绝 IPv6。

**重要边界：** `no-resolve` 不是禁用 AAAA 或强制 IPv4；它只阻止规则为匹配主动解析。HTTP 代理收到域名 CONNECT 后，远端如何解析 IPv6 可能不经过本地 IP 规则。`REJECT` 也不自动触发应用 IPv4 重试。作者声称“住宅代理访问 `2607:6bc0` 会 502”可以从提交说明中确认，但该提交没有提供请求日志、代理响应、DNS、IPv4 对照或客户端复现证据。

<a id="domains"></a>

## 3. 域名规则逐项对比

“完整”表示待比较规则的整个域名范围被本仓库同类规则覆盖；“部分”表示只有具体主机/子范围覆盖；“无同服务覆盖”表示没有可直接对应的同服务规则。关键词偶然命中其他域名不算功能覆盖证明。

以下“无”均为“无同服务覆盖”的缩写；“两者并集”只用于比较匹配范围，不代表两个产品规则在实际配置中使用同一出口。

### 3.1 本次新增行的并集：17 条

| one-exit 新增表达式 | Anthropic SRS | OpenAI SRS | 两者并集 | 说明 |
|---|---|---|---|---|
| `DOMAIN-KEYWORD,anthropic` | 部分 | 无 | 部分 | Anthropic 有一方域名后缀，没有任意位置匹配 `anthropic` 的关键词 |
| `DOMAIN-KEYWORD,browser-intake` | 部分 | 部分 | 部分 | Anthropic 以 `datadog` 关键词覆盖相关主机；OpenAI 有两个精确 intake 主机，均未覆盖任意 `browser-intake` |
| `DOMAIN-KEYWORD,claude` | 部分 | 无 | 部分 | 已有 Claude 一方后缀，但不匹配所有含 `claude` 的域名 |
| `DOMAIN-SUFFIX,challenges.cloudflare.com` | 部分 | 部分 | 部分 | 两者仅精确匹配该主机，没有扩展其全部子域 |
| `DOMAIN-SUFFIX,claudemcpcontent.com` | 完整 | 无 | 完整 | Anthropic 已有根后缀，包含根域及全部子域 |
| `DOMAIN-SUFFIX,datadoghq.com` | 完整 | 无 | 完整 | Anthropic 的 `datadog` 关键词包含整个范围；OpenAI 的 intake 域不是该后缀的子域 |
| `DOMAIN-SUFFIX,growthbook.io` | 无 | 无 | 无 | 两者均无已选入的 GrowthBook 同域规则 |
| `DOMAIN-SUFFIX,hcaptcha.com` | 无 | 无 | 无 | 两者均无对应同域规则 |
| `DOMAIN-SUFFIX,intercom.io` | 完整 | 部分 | 完整 | Anthropic 包含根域及子域；OpenAI 的 `.intercom.io` 只含子域 |
| `DOMAIN-SUFFIX,intercomcdn.com` | 完整 | 部分 | 完整 | Anthropic 包含根域及子域；OpenAI 的 `.intercomcdn.com` 只含子域 |
| `DOMAIN-SUFFIX,segment.io` | 无 | 无 | 无 | 两者均无对应同域规则 |
| `DOMAIN-SUFFIX,sentry.io` | 完整 | 部分 | 完整 | Anthropic 有 `sentry` 关键词；OpenAI 仅有 `o207216`、`o33249` 两个精确 ingest 主机 |
| `DOMAIN-SUFFIX,siftscience.com` | 完整 | 无 | 完整 | Anthropic 的 `sift` 关键词包含根域及全部子域 |
| `DOMAIN-SUFFIX,stripe.com` | 无 | 部分 | 部分 | OpenAI 仅有精确 `js.stripe.com`；Anthropic 无对应同域规则 |
| `DOMAIN-SUFFIX,stripe.network` | 无 | 无 | 无 | 两者均无对应同域规则 |
| `DOMAIN-SUFFIX,stripecdn.com` | 无 | 无 | 无 | 两者均无对应同域规则 |
| `DOMAIN-SUFFIX,usefathom.com` | 部分 | 无 | 部分 | Anthropic 仅有精确 `cdn.usefathom.com`，不包含根域与其他子域 |

因此，17 条新增表达式在本仓库两份产品规则并集中的结果是：**完整 6 条、部分 6 条、无同服务覆盖 5 条**。这不是“官方依赖缺失 5 条”的结论。

关键例子：

- `claudemcpcontent.com`：Anthropic 已有根后缀，完整覆盖。
- `sentry.io`、`datadoghq.com`、`siftscience.com`：Anthropic 现有 `sentry`、`datadog`、`sift` 关键词可覆盖这些范围，但这些关键词来自已有明确策略，不等于所有供应商流量都是 Claude 必需。
- `stripe.com`：OpenAI 只有精确 `js.stripe.com`，不能扩展为整个 Stripe；Anthropic 没有同域规则。
- `usefathom.com`：Anthropic 只有精确 `cdn.usefathom.com`，不是整个后缀。
- `intercom.io` 和 `intercomcdn.com`：Anthropic 的无前导点后缀覆盖根域和子域；OpenAI 的带前导点后缀只覆盖子域，不覆盖裸域。
- `growthbook.io`、`hcaptcha.com`、`stripe.network`、`stripecdn.com`、`segment.io`：当前两份产品 SRS 没有对应同服务规则；其中精确主机 `cdn.growthbook.io` 已在本仓库 pending（待核实）清单，不能据此认定整个 `growthbook.io` 后缀已有依赖证据。
- `modelcontextprotocol.io`：对方在本提交前已经存在；本仓库同名项仍是未选 pending，不能把它算成此次新增或已发布规则。

### 3.2 其余既有域名表达式：15 条

这 15 条不在上面的新增行并集中，但仍是提交后完整模板的一部分。`anthropic`、`claude` 虽在 FlClash 中原已存在，为避免重复已计入上表。

| one-exit 既有表达式 | Anthropic SRS | OpenAI SRS | 依据 |
|---|---|---|---|
| `DOMAIN-SUFFIX,claude.ai` | 完整 | 无 | Anthropic 有相同后缀 |
| `DOMAIN-SUFFIX,claude.com` | 完整 | 无 | Anthropic 有相同后缀 |
| `DOMAIN-SUFFIX,clau.de` | 完整 | 无 | Anthropic 有相同后缀 |
| `DOMAIN-SUFFIX,anthropic.com` | 完整 | 无 | Anthropic 有相同后缀 |
| `DOMAIN-SUFFIX,claudeusercontent.com` | 完整 | 无 | Anthropic 有相同后缀 |
| `DOMAIN-SUFFIX,modelcontextprotocol.io` | 无 | 无 | 本仓库为未选待核实候选；文档站不等于通用 MCP 服务端点 |
| `DOMAIN-KEYWORD,modelcontextprotocol` | 无 | 无 | 仅 FlClash 有此更宽关键词；本仓库无同名关键词或同服务规则 |
| `DOMAIN-SUFFIX,google.com` | 无 | 无 | 两份产品 SRS 均无 Google 全域规则 |
| `DOMAIN-SUFFIX,googleapis.com` | 部分 | 无 | Anthropic 精确覆盖 `fonts.googleapis.com`、`storage.googleapis.com` |
| `DOMAIN-SUFFIX,gstatic.com` | 部分 | 无 | Anthropic 精确覆盖 `fonts.gstatic.com` |
| `DOMAIN-SUFFIX,gmail.com` | 无 | 无 | 无对应同域规则 |
| `DOMAIN-SUFFIX,googleusercontent.com` | 无 | 无 | 无对应同域规则 |
| `DOMAIN-SUFFIX,recaptcha.net` | 无 | 无 | 无对应同域规则 |
| `DOMAIN-SUFFIX,withpersona.com` | 无 | 无 | 无对应同域规则；对方将 Persona 固定到住宅出口 |
| `DOMAIN-SUFFIX,webshare.io` | 无 | 无 | 无对应同域规则；对方用于 Webshare 相关访问及出口检查 |

这 15 条在两份产品 SRS 并集中为完整 5、部分 2、无同服务覆盖 8；连同上表，全部 **32 条 = 完整 11、部分 8、无同服务覆盖 13**。Google、Gmail、Wallet、Persona 和 Webshare 反映对方“统一住宅出口”的应用场景，不能全部当成 OpenAI/Claude 产品规则的缺项。

<a id="repo"></a>

## 4. 本仓库当前规则基线

| 制品 | 当前结构 |
|---|---|
| `openai.srs` | 25 个精确域名、16 个后缀、1 个正则、23 个目的 IPv4 `/32` |
| `anthropic.srs` | 15 个精确域名、16 个后缀、3 个关键词、目的 `160.79.104.0/21` 与 `2607:6bc0::/32` |
| `anthropic-ip.srs` | 独立来源 `source_ip_cidr: 160.79.104.0/21` |

完整本地规则见 [OpenAI JSON](../artifacts/v0.1.6/openai.json)、[Anthropic JSON](../artifacts/v0.1.6/anthropic.json) 和 [Anthropic 来源 IP JSON](../artifacts/v0.1.6/anthropic-ip.json)。

反向比较，本仓库也有对方显式域名规则未覆盖的重要范围：

| 本仓库范围示例 | one-exit 完整模板中的对应情况 |
|---|---|
| OpenAI 的 `openai.com`、`chatgpt.com`、`sora.com`、`oaistatic.com`、`oaiusercontent.com` 及 Voice/LiveKit | 没有对应专用域名规则，也未列出本仓库的 23 个 Voice `/32` |
| Anthropic 的 `statsigapi.net` 后缀 | 没有对应后缀或关键词 |
| `cdn.jsdelivr.net`、`cdn.tailwindcss.com`、`cdnjs.cloudflare.com`、`code.jquery.com`、`unpkg.com` | 没有对应显式域名规则 |
| `github.com`、`raw.githubusercontent.com`、`registry.npmjs.org`、`formulae.brew.sh` | 没有对应显式域名规则；这些精确主机见本仓库 Anthropic 规则 |
| `static.intercomassets.com` | 不属于 `intercom.io` 或 `intercomcdn.com`，未被对方相应后缀覆盖 |
| 本仓库 `sentry`、`datadog`、`sift` 关键词 | 对方对应供应商后缀和 `browser-intake` 关键词不能包含这三个任意位置关键词的完整范围 |

这里比较显式域名条件；不能由此断言其实际流量一定直连，FlClash 的进程条件、原订阅规则或消费者兜底仍可能命中。反过来，`claude.app`、`claude.dev`、`claudemcpclient.com`、`anthropic.auth0.com` 虽未逐一出现在对方后缀列表，却能被其 `claude` / `anthropic` 关键词覆盖，不能算缺失。

两边的域名范围互不包含：one-exit 更强调多个共享服务和 Google/身份验证流量统一出口，本仓库额外覆盖 OpenAI 主体及 Claude 的库、安装和客服依赖。本仓库规则集只负责产品/依赖范围匹配；最终出站、IPv6 拒绝与规则优先级需要在消费者配置中单独验收。直接加入 one-exit 的宽后缀或关键词，会扩大其他软件的匹配范围，且缺少相同的来源和功能证据。

<a id="recommendation"></a>

## 5. 是否需要据此补规则

| 项目 | 本次判断 |
|---|---|
| Anthropic 目的 CIDR | 无需因这次提交补地址：提交列出的 IPv4、两段 IPv6 都已包含 |
| 新增 17 条域名表达式中的完整 6 条 | 无需重复添加 |
| 部分 6 条：`anthropic`、`claude`、`browser-intake`、`challenges.cloudflare.com`、`stripe.com`、`usefathom.com` | 先区分具体已用主机与宽泛范围；本次提交不足以证明应扩成整个关键词或后缀 |
| 无同服务覆盖 5 条：`growthbook.io`、`hcaptcha.com`、`stripe.network`、`stripecdn.com`、`segment.io` | 可作为后续核实候选；需要官方资料或实际业务请求证据后，再决定产品归属及精确范围 |
| `modelcontextprotocol.io`、Google/Persona/Webshare 等既有规则 | 属于额外场景对比，不计作此次新增 OpenAI/Claude 依赖 |
| IPv6 `REJECT`、固定住宅出口、ASN、进程匹配 | 属于消费端策略设计；应按实际代理能力、DNS 解析位置及 IPv4 重试结果配置 |

因此建议保留当前产品规则的范围，先核实候选依赖；仅凭该提交不足以支持扩表或重新发布。本次按要求完成分析，没有修改规则或发布版本。

<a id="verify"></a>

## 6. 验证与证据

- 固定提交 API、前后 5 个文件均已按固定 SHA 抓取并保存；文件哈希见[file-fetches.json](evidence/one-exit-b9d9f8a-2026-10-21/file-fetches.json)。
- `artifacts/v0.1.6/` 的三份本地归档 SRS 已原生解编译，与 `dist/` 对应文件字节一致、与归档 JSON 语义一致；见[本地基线](evidence/one-exit-b9d9f8a-2026-10-21/local-baseline.json)。这不是重新下载并校验远端 Release 的结论。
- 使用当前 `sing-box 1.15.0-alpha.9` 对对比主机、边界和 IP 端点执行 **306 项原生匹配检查，全部通过**；见[comparison.json](evidence/one-exit-b9d9f8a-2026-10-21/comparison.json)。这些检查验证规则匹配，不验证代理出口、真实业务或作者的 502 复现。
- [分流行为审阅](evidence/one-exit-b9d9f8a-2026-10-21/policy-review.md)记录 `no-resolve`、REJECT、ASN、进程匹配和三端差异的限制。

原生检查共 **145 个域名 × 2 份产品 SRS + 8 项 IP 地址样例 × 2 份产品 SRS = 306 项**。IP 样例去重后为 7 个地址，其中一个地址因不同范围验证重复检查；完整范围包含关系同时依据静态规则语义判断，不能仅靠几个正例证明。没有执行下载的上游脚本，也没有加载对方模板进行业务实测。

本次仅新增分析证据和报告，未修改 `sources/`、`artifacts/`、`dist/`，未提交、推送或发布版本。

审计时间：2026-10-21T05:28:48.107527+00:00。
