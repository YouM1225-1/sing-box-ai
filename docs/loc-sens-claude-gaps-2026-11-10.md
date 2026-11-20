# loc sens 清单中与 Claude 相关的域名缺口

核对日期：2026-11-10。范围限定为上一轮 loc-sens 清单及当前仓库 v0.1.10；不是对 Claude 全部网络依赖的重新审计。

**有明确 Claude 订阅和支付关联、但尚未完整覆盖的是 `stripe.com` 后缀。** 完全未覆盖的条目中，`api.revenuecat.com` 有可选 MCP 集成场景的关联，但不能算作已证实的 Claude 核心依赖。

## Stripe 的部分覆盖

Stripe 官方客户案例确认 Anthropic 使用 Stripe 处理 Claude 的订阅、支付与结账，并使用 Elements、Link 等产品，因此 Stripe 与 Claude 的关系有直接依据。[Stripe 的 Anthropic 客户案例](https://stripe.com/customers/anthropic)

当前 `anthropic` 规则只精确收录 `r.stripe.com`，没有收录整个 `stripe.com` 后缀。以下是该后缀中值得核对的具体例子：

| 域名 | anthropic 规则 | openai 规则 | 说明 |
| --- | --- | --- | --- |
| `js.stripe.com` | 未覆盖 | 已覆盖 | 仅加载 Claude 规则时，不会因 OpenAI 中有此条而获得覆盖。 |
| `api.stripe.com` | 未覆盖 | 未覆盖 | Stripe 官方清单列出的域名。 |
| `checkout.stripe.com` | 未覆盖 | 未覆盖 | Stripe 官方清单列出的域名。 |
| `billing.stripe.com` | 未覆盖 | 未覆盖 | Stripe 官方清单列出的域名。 |
| `m.stripe.com` | 未覆盖 | 未覆盖 | Stripe 官方清单列出的域名。 |
| `stripe.com` | 未覆盖 | 未覆盖 | 原始后缀规则也覆盖根域。 |
| `r.stripe.com` | 已覆盖 | 未覆盖 | v0.1.10 已精确收录，不是缺口。 |

这些域名均见于 [Stripe 官方域名清单](https://docs.stripe.com/ips#stripe-domains)。**服务层面的关联已经确认，但没有逐个抓包证明上表所有域名都会被你的 Claude 客户端访问。** 因此，上表是共享支付依赖的候选缺口，不是“Claude 每次聊天都必须访问”的清单；也不是整个 `stripe.com` 后缀缺口的穷举。

已有的 `stripe.network` 和 `stripecdn.com` 后缀不能覆盖 `stripe.com`。

## RevenueCat 的条件性关联

`api.revenuecat.com` 在当前 `anthropic`、`openai` 规则中都未覆盖。

RevenueCat 官方文档提供 Claude 和 Claude Code 的 MCP 接入方式，其官方仓库中的集成问题记录明确出现 `api.revenuecat.com/oauth2/authorize`。因此，如果使用 RevenueCat MCP 或插件，这个域名与该功能有关。[官方 MCP 配置文档](https://www.revenuecat.com/docs/tools/mcp/setup)、[官方仓库中的 OAuth 集成记录](https://github.com/RevenueCat/ai-toolkit/issues/58)

这些证据不证明 Claude 自身的订阅、普通聊天或默认客户端使用 RevenueCat。未使用该集成时，不能仅凭它出现在 loc-sens 清单中，就把它列为 Claude 必需补项。

## 其余条目如何理解

- `prodregistryv2.org`：本仓库将其保存在 OpenAI 历史候选项中；目前没有足够依据把它认定为 Claude 的实际依赖。参见 [候选规则记录](../sources/discovery/pending.yaml)。
- 原清单里其他未覆盖的 Google、Apple、DeepL、NVIDIA、Cursor 等域名：本次没有确认其为 Claude 自身依赖；通过 Claude 访问第三方服务不等于它们都是 Claude 的固定依赖。
- `PROCESS-NAME,Claude`：确实未覆盖，但它是进程规则，不是域名。Claude 访问已收录的域名时仍会命中域名规则。
- `*.datadog.pool.ntp.org`、`fcmtoken.googleapis.com`、`api.segment.io`、`hcaptcha.com`、`intercom.io`、`ingest.us.sentry.io`、`siftscience.com` 和 `r.stripe.com`：已被当前 `anthropic` 覆盖，不在本次缺口中。

本次只整理覆盖与关联依据，没有修改规则。覆盖依据为 [v0.1.10 Anthropic 规则](../artifacts/v0.1.10/anthropic.json)、[v0.1.10 OpenAI 规则](../artifacts/v0.1.10/openai.json) 及上一轮 [完整覆盖核对](loc-sens-coverage-2026-11-10.md)。
