# Claude 截图域名和网段覆盖核对

核对日期：2026-11-08。当前仓库版本：v0.1.9。

**截图中的 14 个域名，12 个已被 `anthropic` 规则集覆盖，2 个未覆盖；另列出的 `34.8.0.0/16` 网段也未覆盖。**

| 截图项目 | 是否覆盖 | 当前命中规则或缺口 |
| --- | --- | --- |
| `claude.ai` | 是 | `domain_suffix: claude.ai` |
| `anthropic.com` | 是 | `domain_suffix: anthropic.com` |
| `claude.com` | 是 | `domain_suffix: claude.com` |
| `claudeusercontent.com` | 是 | `domain_suffix: claudeusercontent.com` |
| `claude.app` | 是 | `domain_suffix: claude.app` |
| `claudemcpcontent.com` | 是 | `domain_suffix: claudemcpcontent.com` |
| `clau.de` | 是 | `domain_suffix: clau.de` |
| `api-iam.intercom.io` | 是 | `domain_suffix: intercom.io` |
| `nexus-websocket-a.intercom.io` | 是 | `domain_suffix: intercom.io` |
| `us5.datadoghq.com` | 是 | `domain_keyword: datadog` |
| `r.stripe.com` | 否 | 无匹配的域名、后缀、关键词或正则规则 |
| `us.sentry.io` | 是 | `domain_keyword: sentry` |
| `siftscience.com` | 是 | `domain_keyword: sift` |
| `fcmtoken.googleapis.com` | 否 | 无匹配的域名、后缀、关键词或正则规则 |
| `34.8.0.0/16` | 否 | 与当前规则集中的 IP 网段均无重叠 |

已有的 `stripe.network`、`stripecdn.com` 后缀不覆盖 `r.stripe.com`；`openai` 规则中的精确域名 `js.stripe.com` 也不覆盖它。已有的 `fonts.googleapis.com` 等精确域名不覆盖 `fcmtoken.googleapis.com`。

已使用仓库内 `.tools/sing-box` 反编译当前 `dist` 中的 `anthropic.srs`、`anthropic-ip.srs` 和 `openai.srs`，确认规则与 v0.1.9 发布 JSON 等价，且这 3 个分发文件分别与对应发布文件字节一致。上述 2 个域名及该网段在另外两个规则集中同样没有匹配项。

核验依据：[Anthropic 发布规则](../artifacts/v0.1.9/anthropic.json)、[Anthropic IP 发布规则](../artifacts/v0.1.9/anthropic-ip.json)、[OpenAI 发布规则](../artifacts/v0.1.9/openai.json)、[逐项匹配结果和文件校验值](evidence/domain-screenshot-coverage-2026-11-08/matches.json)。

本次仅核对规则覆盖，未修改分流规则。客户端实际出口仍由已加载的规则版本、路由顺序及兜底配置决定。
