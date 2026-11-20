# one-exit 固定提交在 v0.1.8 中的覆盖情况

核对日期：2026-10-29（Asia/Shanghai）。对照 [one-exit 提交 b9d9f8a](https://github.com/wquguru/one-exit/commit/b9d9f8ab6687401f7588dfa7d7023cd58ffb4032)与当前 [sing-box-ai v0.1.8 正式发布](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.8)。

## 结论

**此前要求补充的 5 个后缀已经发布，当前版本全部保留；该提交的整套规则并未全部照搬。**

三个上游模板在该提交中新增的域名表达式去重后为 17 条。按我们 OpenAI 与 Claude 两份规则的覆盖范围并集核对：**11 条完整覆盖，6 条部分覆盖，没有完全缺少对应服务覆盖的新增项。** “并集”只表示两份规则合计能匹配哪些地址，不代表这些流量会走同一出口。

其中 `stripe.com` 的部分覆盖仅来自 **OpenAI** 中的精确域名 `js.stripe.com`，Claude 规则并未收录它。不能把上述并集结果解释为“Claude 已包含全部”。

## 1. 新增表达式的逐项清单

### 完整覆盖的 11 项

以下都已在 Claude 的 `anthropic.srs` 中覆盖整个上游后缀范围。

| 上游域名后缀 | 当前覆盖方式 | 状态 |
| --- | --- | --- |
| `claudemcpcontent.com` | 同名域名后缀 | 已有 |
| `sentry.io` | `sentry` 关键词 | 已有 |
| `datadoghq.com` | `datadog` 关键词 | 已有 |
| `siftscience.com` | `sift` 关键词 | 已有，包含截图中的 `api3.siftscience.com` |
| `intercom.io` | 同名域名后缀 | 已有 |
| `intercomcdn.com` | 同名域名后缀 | 已有 |
| `growthbook.io` | 同名域名后缀 | v0.1.7 补入，v0.1.8 保留 |
| `hcaptcha.com` | 同名域名后缀 | v0.1.7 补入，v0.1.8 保留 |
| `stripe.network` | 同名域名后缀 | v0.1.7 补入，v0.1.8 保留 |
| `stripecdn.com` | 同名域名后缀 | v0.1.7 补入，v0.1.8 保留 |
| `segment.io` | 同名域名后缀 | v0.1.7 补入，v0.1.8 保留 |

五项补充的历史过程及发布记录见[原补充记录](one-exit-domain-supplement-2026-10-21.md)。

### 部分覆盖的 6 项

| 上游表达式 | 当前实际收录 | 未覆盖的上游范围 |
| --- | --- | --- |
| `DOMAIN-KEYWORD,anthropic` | Claude 中多个对应域名后缀，如 `anthropic.com` | 任意位置含 `anthropic` 的所有域名 |
| `DOMAIN-KEYWORD,claude` | Claude 中多个对应后缀，如 `claude.ai`、`claude.com` | 任意位置含 `claude` 的所有域名 |
| `DOMAIN-KEYWORD,browser-intake` | Claude 的 `datadog` 关键词覆盖相关 Datadog 地址；OpenAI 另有两个精确 intake 主机 | 任意含 `browser-intake` 的域名 |
| `DOMAIN-SUFFIX,challenges.cloudflare.com` | OpenAI、Claude 均精确收录 `challenges.cloudflare.com` | 如 `probe.challenges.cloudflare.com` 的子域 |
| `DOMAIN-SUFFIX,usefathom.com` | Claude 精确收录 `cdn.usefathom.com` | 裸域及其他子域 |
| `DOMAIN-SUFFIX,stripe.com` | **OpenAI** 精确收录 `js.stripe.com`；Claude 无同服务规则 | 裸域及其他子域；Claude 也未收录 `js.stripe.com` |

## 2. 若比较提交后的整个模板

除上述 17 项，模板还有 15 条既有域名表达式。完整清单如下，避免将“本次新增项覆盖”理解成“整套模板一致”。

| 既有表达式 | 当前状态（两份产品规则并集） |
| --- | --- |
| 后缀 `claude.ai`、`claude.com`、`clau.de`、`anthropic.com`、`claudeusercontent.com` | 5 项完整覆盖，均在 Claude 中 |
| 后缀 `googleapis.com` | 部分覆盖：Claude 的 `fonts.googleapis.com`、`storage.googleapis.com` |
| 后缀 `gstatic.com` | 部分覆盖：Claude 的 `fonts.gstatic.com` |
| 后缀 `modelcontextprotocol.io` | 无对应服务覆盖 |
| 关键词 `modelcontextprotocol` | 无对应服务覆盖 |
| 后缀 `google.com`、`gmail.com`、`googleusercontent.com`、`recaptcha.net`、`withpersona.com`、`webshare.io` | 6 项无对应服务覆盖 |

因此全部 **32 条域名表达式 = 16 条完整覆盖、8 条部分覆盖、8 条无对应服务覆盖**。本次计数不把人工构造的“同时包含两个不同关键词”的域名交集算作对应服务覆盖，例如含 `modelcontextprotocol` 和 `sift` 的合成主机不能证明已收录 MCP 服务。

这些是规则范围差异，不能仅凭第三方模板认定它们都是 Claude 或 OpenAI 必需依赖。

## 3. IP 地址与实际策略

| 上游目的地址范围 | 当前 Claude 规则 | 结论 |
| --- | --- | --- |
| `160.79.104.0/21` | 同名目的 `ip_cidr` | 完整包含 |
| `2607:6bc0::/48` | 被目的 `2607:6bc0::/32` 包含 | 完整包含，当前范围更宽 |
| `2607:6bc0:11::/48` | 被目的 `2607:6bc0::/32` 包含 | 完整包含，当前范围更宽 |

上游模板给这两段 IPv6 指定 `REJECT`，给其他多项指定住宅出口。我们的 SRS 只保存匹配条件，不包含这些动作；也未照搬上游的 `IP-ASN,399358` 和三个进程匹配条件。地址被包含不表示 IPv6 会被拒绝，也不表示流量会使用指定住宅出口。

另有 `anthropic-ip.srs` 使用的是**来源** IP 条件，不能与上表的目的地址路由混用。

## 4. 本次验证及证据

- GitHub Latest 查询结果为 v0.1.8。
- 重新下载了固定提交的三个模板，与 10 月 21 日保存的快照逐字节一致；未执行其脚本或加载其配置。
- 重新下载 v0.1.8 的 OpenAI、Claude 两份 SRS，与 GitHub 资产摘要及本地发布归档一致。
- 对照 v0.1.6 可读规则验证语义差异：Claude 仅新增上述 5 个后缀；OpenAI 仅新增 `poteto.com`，不改变本次上游范围结论。
- 针对这些地址、子域边界和 IP 样例执行 **308 项原生二进制规则匹配检查，全部符合预期**。完整范围包含结论同时依据规则语义，不能仅靠样例推导。
- 这些验证不涉及用户设备的实际配置、真实业务请求、最终出口或 IPv4 回退效果。

证据：[下载摘要、32 项分类及 308 项匹配输出](evidence/one-exit-recheck-2026-10-29/comparison.json)。可读发布规则：[Claude](../artifacts/v0.1.8/anthropic.json)、[OpenAI](../artifacts/v0.1.8/openai.json)。

本次仅重新核对并生成报告，没有修改规则、提交代码或发布新版本。
