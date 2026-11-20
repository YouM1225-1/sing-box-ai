# one-exit b9d9f8a 域名范围独立复核

比较固定提交 `b9d9f8ab6687401f7588dfa7d7023cd58ffb4032` 与本仓库 v0.1.6 最终规则。仅只读检查本地固定证据，不重新联网，不修改规则。原生 SRS 见证由主任务统一执行。

## 计数先校正

提交 diff 中，Clash Party 与 Shadowrocket 各新增 **17** 条域名规则，FlClash 新增 **15** 条。三份新增行的去重并集是 **17** 条：14 条后缀、3 条关键词。`anthropic`、`claude` 关键词此前已在 FlClash；按所有模板旧规则并集计算，真正此前从未出现的域名语句是 **15** 条。`modelcontextprotocol.io` 后缀及 FlClash 的 `modelcontextprotocol` 关键词都在提交前已存在。不能写成 16 条新增。

## 比较语义

“完整”指整个新增规则范围均被包含；“部分”指已配置的相关子范围或官方/已知主机命中，但有明确反例；“无同服务覆盖”指没有该服务的同域规则或已知目标覆盖。后一项不等于数学上所有构造的主机都不命中：现有 `sentry` 关键词会命中 `sentry.hcaptcha.com`，`openai.com` 后缀会命中 `anthropic.openai.com`；这类构造不证明 hCaptcha 或 Anthropic 功能已覆盖。

后缀 `example.com` 包含根域及子域；后缀 `.example.com` 只含子域；精确 `js.stripe.com` 只匹配本身。关键词规则匹配任何位置的字面字符串。规则并集的命中不证明最终配置会把流量送往同一个出口。

| 新增语句 | anthropic | openai | 两者并集 | 判断依据 |
| --- | --- | --- | --- | --- |
| `DOMAIN-KEYWORD,anthropic` | 部分 | 无同服务覆盖 | 部分 | Anthropic first-party suffixes cover documented hosts; no keyword anthropic rule. |
| `DOMAIN-KEYWORD,browser-intake` | 部分 | 部分 | 部分 | Anthropic datadog keyword covers documented Datadog intake names; OpenAI has two exact intake names; neither implements generic browser-intake substring. |
| `DOMAIN-KEYWORD,claude` | 部分 | 无同服务覆盖 | 部分 | Selected claude.ai/.app/.com/.dev and content suffixes do not cover all hostnames containing claude. |
| `DOMAIN-SUFFIX,challenges.cloudflare.com` | 部分 | 部分 | 部分 | Both artifacts have this exact host; neither has suffix challenges.cloudflare.com. |
| `DOMAIN-SUFFIX,claudemcpcontent.com` | 完整 | 无同服务覆盖 | 完整 | Anthropic root suffix covers apex and every subdomain. |
| `DOMAIN-SUFFIX,datadoghq.com` | 完整 | 无同服务覆盖 | 完整 | Anthropic datadog keyword includes entire suffix; OpenAI browser-intake-datadoghq.com and rum child are not under datadoghq.com. |
| `DOMAIN-SUFFIX,growthbook.io` | 无同服务覆盖 | 无同服务覆盖 | 无同服务覆盖 | No direct suffix or exact GrowthBook rule in either artifact. |
| `DOMAIN-SUFFIX,hcaptcha.com` | 无同服务覆盖 | 无同服务覆盖 | 无同服务覆盖 | No same-domain selected coverage. |
| `DOMAIN-SUFFIX,intercom.io` | 完整 | 部分 | 完整 | Anthropic root suffix includes apex and children; OpenAI dotted .intercom.io includes children only. |
| `DOMAIN-SUFFIX,intercomcdn.com` | 完整 | 部分 | 完整 | Anthropic root suffix includes apex and children; OpenAI dotted .intercomcdn.com includes children only. |
| `DOMAIN-SUFFIX,segment.io` | 无同服务覆盖 | 无同服务覆盖 | 无同服务覆盖 | No same-domain selected coverage. |
| `DOMAIN-SUFFIX,sentry.io` | 完整 | 部分 | 完整 | Anthropic sentry keyword contains entire suffix scope; OpenAI only exact o207216 and o33249 ingest hosts. |
| `DOMAIN-SUFFIX,siftscience.com` | 完整 | 无同服务覆盖 | 完整 | Anthropic sift keyword covers apex and every subdomain; OpenAI has no same-domain selected rule. |
| `DOMAIN-SUFFIX,stripe.com` | 无同服务覆盖 | 部分 | 部分 | OpenAI has exact js.stripe.com only; Anthropic has no same-domain selected rule. |
| `DOMAIN-SUFFIX,stripe.network` | 无同服务覆盖 | 无同服务覆盖 | 无同服务覆盖 | No same-domain selected coverage. |
| `DOMAIN-SUFFIX,stripecdn.com` | 无同服务覆盖 | 无同服务覆盖 | 无同服务覆盖 | No same-domain selected coverage. |
| `DOMAIN-SUFFIX,usefathom.com` | 部分 | 无同服务覆盖 | 部分 | Anthropic contains only exact cdn.usefathom.com; apex and other subdomains are outside that rule. |

17 条新增语句的并集结论：**6 条完整、6 条部分、5 条无同服务覆盖**。Anthropic 单独为 6/5/6，OpenAI 单独为 0/6/11（顺序均为完整/部分/无同服务覆盖）。这些是规则范围计数，不是官方依赖缺失计数。

## 重点事实与证据级别

- `growthbook.io`：无同服务覆盖。`cdn.growthbook.io` 自 2026-09-27 已在 [pending](../../../sources/discovery/pending.yaml)，只支持历史发现，不支持当前强制运行依赖；更不能扩为全域已获官方证明。
- `usefathom.com`：只有 Anthropic 的精确 `cdn.usefathom.com`，根域、其他子域、`audit.cdn.usefathom.com` 都不由它覆盖。旧 pending 仍保留，但当前精确主机另按 [用户要求](../../../sources/anthropic.yaml) 已选入；不能因为它仍在 pending 就说最终制品未覆盖。
- `hcaptcha.com`、`stripe.network`、`stripecdn.com`、`segment.io`：本次检查的官方快照和 pending 没有同名依赖事实，模板作者把它们固定出口不等同于 Claude 官方必需。
- `stripe.com`：仅 OpenAI 的 `js.stripe.com` 是已有 [官方事实](../../../sources/official/openai-network.json)。不能从这项推导全部 Stripe 域名必需，也不能直接移植为 Claude 必需。
- `modelcontextprotocol.io`：既有 pending 文档域名，两个模板用后缀，FlClash 用更宽的关键词；两者都不是本提交新增。协议文档站不等同于每次 MCP 请求都会连接的固定服务器。
- `browser-intake`：Anthropic 现有 `datadog` 关键词包含两个官方可选 Datadog 主机；OpenAI 是精确主机。`browser-intake.example.net` 两者均不匹配，因此都未完整实现通用 `browser-intake` 关键词。
- `datadoghq.com`：OpenAI 的 `browser-intake-datadoghq.com` 是另一个注册域，不是 `datadoghq.com` 的子域。Anthropic `datadog` 关键词则覆盖整个目标范围。
- `anthropic`、`claude`：当前一方后缀覆盖官方主机，但不能代替任意位置的关键词。`unrelated-anthropic.example.net` 和 `unrelated-claude.example.net` 不命中。这两个关键词对 Clash Party/Shadowrocket 是新行，对 FlClash 已存在。
- `intercom.io`、`intercomcdn.com`：Anthropic 为无前导点根后缀，全范围覆盖；OpenAI 为带点后缀，缺根域，只能判部分。既有官方通配符与客服可选主机不代表任何 App 都需要整个客服平台。
- `challenges.cloudflare.com`：两个产物都只精确覆盖该主机，子域并未被完整覆盖。OpenAI 有官方清单依据；Anthropic 精确项是维护者确认过的 compatibility-critical 记录，不能写成官方要求其全部子域。
- `sentry.io`、`datadoghq.com`、`siftscience.com`：Anthropic 的 `sentry`、`datadog`、`sift` 关键词分别完整包含这些后缀，且范围更宽。这些关键词的依据是明确用户要求，而非整个平台都是 Claude 官方依赖。

## 复查入口

- [固定提交数据](commit.json)
- [逐项结构化结果和正反主机](independent-domain-review.json)
- [Anthropic v0.1.6 规则](../../../artifacts/v0.1.6/anthropic.json)
- [OpenAI v0.1.6 规则](../../../artifacts/v0.1.6/openai.json)
- [Claude Code 官方事实](../../../sources/official/claude-code.json) · [Desktop 官方事实](../../../sources/official/claude-desktop.json) · [客服实测事实](../../../sources/official/claude-support.json)

本轮 graft 1 次，工具报告节省约 26,577 tokens。
