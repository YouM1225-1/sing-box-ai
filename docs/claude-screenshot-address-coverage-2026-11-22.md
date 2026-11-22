# 图片地址与仓库规则覆盖核对

核对日期为 2026-11-22。核对对象是仓库当前 `VERSION`（v0.1.18）及其 [`artifacts/v0.1.18/anthropic.srs`](../artifacts/v0.1.18/anthropic.srs)。本地 [`dist/anthropic.srs`](../dist/anthropic.srs) 与该制品的 SHA-256 相同。

## 结论

图片列出的 42 项中，当前规则直接命中 42 项。

- 已覆盖 32 个域名中的 32 个
- 已覆盖 4 个 IP 网段中的 4 个
- 已覆盖 6 个验证或统计域名中的 6 个
- `intercomassets.com` 已按后缀覆盖根域及其子域

## 逐项核对

### 图片第一组域名

| 地址 | 结果 | 当前匹配方式 |
| --- | --- | --- |
| `claude.ai` | 已覆盖 | `domain_keyword: claude` |
| `anthropic.com` | 已覆盖 | `domain_keyword: anthropic` |
| `claude.com` | 已覆盖 | `domain_keyword: claude` |
| `claudeusercontent.com` | 已覆盖 | `domain_keyword: claude` |
| `claude.app` | 已覆盖 | `domain_keyword: claude` |
| `claudemcpcontent.com` | 已覆盖 | `domain_keyword: claude` |
| `clau.de` | 已覆盖 | `domain_suffix: clau.de` |
| `intercom.io` | 已覆盖 | `domain_suffix: intercom.io` |
| `intercomcdn.com` | 已覆盖 | `domain_suffix: intercomcdn.com` |
| `intercomassets.com` | 已覆盖 | `domain_suffix: intercomassets.com` |
| `intercom-messenger.com` | 已覆盖 | `domain_suffix: intercom-messenger.com` |
| `us5.datadoghq.com` | 已覆盖 | `domain_keyword: datadog` |
| `browser-intake-us5-datadoghq.com` | 已覆盖 | `domain_keyword: browser-intake`、`datadog` |
| `r.stripe.com` | 已覆盖 | `domain_suffix: stripe.com` |
| `us.sentry.io` | 已覆盖 | `domain_keyword: sentry` |
| `siftscience.com` | 已覆盖 | `domain_keyword: sift` |
| `fcmtoken.googleapis.com` | 已覆盖 | 精确 `domain` |
| `claudemcpclient.com` | 已覆盖 | `domain_keyword: claude` |
| `servd-anthropic-website.b-cdn.net` | 已覆盖 | `domain_keyword: anthropic` |
| `anthropic.auth0.com` | 已覆盖 | `domain_keyword: anthropic` |
| `anthropic-com.ghost.io` | 已覆盖 | `domain_keyword: anthropic` |
| `anthropic.com.cdn.cloudflare.net` | 已覆盖 | `domain_keyword: anthropic` |
| `claude.dev` | 已覆盖 | `domain_keyword: claude` |
| `claude.site` | 已覆盖 | `domain_keyword: claude` |
| `claudeacademy.com` | 已覆盖 | `domain_keyword: claude` |
| `claude.new` | 已覆盖 | `domain_keyword: claude` |
| `ant.dev` | 已覆盖 | `domain_suffix: ant.dev` |
| `anthropic.team` | 已覆盖 | `domain_keyword: anthropic` |
| `antspace.dev` | 已覆盖 | `domain_suffix: antspace.dev` |
| `chatbotclaude.com` | 已覆盖 | `domain_keyword: claude` |
| `claudepages.dev` | 已覆盖 | `domain_keyword: claude` |
| `claudestudio.com` | 已覆盖 | `domain_keyword: claude` |

### 图片中的 IP 网段

| 网段 | 结果 | 当前匹配方式 |
| --- | --- | --- |
| `34.8.0.0/16` | 已覆盖 | `ip_cidr` |
| `160.79.104.0/21` | 已覆盖 | `ip_cidr` |
| `153.61.208.0/20` | 已覆盖 | `ip_cidr` |
| `153.61.224.0/22` | 已覆盖 | `ip_cidr` |

### 验证、KYC 与统计域名

| 地址 | 结果 | 当前匹配方式 |
| --- | --- | --- |
| `hcaptcha.com` | 已覆盖 | `domain_suffix: hcaptcha.com` |
| `challenges.cloudflare.com` | 已覆盖 | `domain_suffix: challenges.cloudflare.com` |
| `withpersona.com` | 已覆盖 | `domain_suffix: withpersona.com` |
| `yoti.com` | 已覆盖 | `domain_suffix: yoti.com` |
| `statsigapi.net` | 已覆盖 | `domain_suffix: statsigapi.net` |
| `usefathom.com` | 已覆盖 | `domain_suffix: usefathom.com` |

## 核对依据

- 规则源为 [`sources/anthropic.yaml`](../sources/anthropic.yaml)
- 目的地址制品为 [`artifacts/v0.1.18/anthropic.json`](../artifacts/v0.1.18/anthropic.json)
- 本地网关域名导出为 [`artifacts/v0.1.18/unifi/domains.txt`](../artifacts/v0.1.18/unifi/domains.txt)
- 逐项使用仓库内 [`sing-box`](../.tools/sing-box) 执行 `rule-set match -f binary`

这里的结果说明规则集本身是否命中。实际客户端还需要加载 v0.1.18 的 `anthropic.srs`，并由客户端路由决定命中后的出口。
