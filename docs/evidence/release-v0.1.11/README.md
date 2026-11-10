# v0.1.11 Claude 域名补充与发布记录

日期：2026-11-10。用户指令：添加以上未覆盖的规则 并发布。

当前状态：构建与发布门槛已通过，GitHub 发布及远端下载验收待完成。

## 本次新增

以下 6 项均为 `anthropic.srs` 中的精确目的域名：

- `js.stripe.com`
- `api.stripe.com`
- `checkout.stripe.com`
- `billing.stripe.com`
- `m.stripe.com`
- `api.revenuecat.com`

这些条目按用户指定覆盖登记；Stripe 为共享支付服务，RevenueCat 为可选集成场景，不声称已逐项验证 Claude 真实业务依赖。现有域名、后缀、关键词及网段均保留，没有扩大至整个 `stripe.com` 或 `revenuecat.com` 后缀。

`openai.srs` 与 `anthropic-ip.srs` 均与 v0.1.10 逐字节一致。`js.stripe.com` 现在同时被 OpenAI 和 Anthropic 覆盖；客户端最终使用哪个出站仍由规则顺序决定。

## 验证结果

两次独立正式构建各通过 2,868 项原生检查及发布门槛，9 个批次文件逐字节一致；同提交候选 JSON/SRS 与正式批次一致。完整回归 86 项全部通过，无失败、无跳过。

原 Challenge 及 IPv6 `/48` 兼容条目的日期与证据保持原样。本版授权仅绑定现有基线、6 个新增域名和当前制品摘要，不记为重新完成运行验证。设备刷新及真实登录、支付或 MCP 使用不在本次静态发布验收中。

[构建汇总](build-results.json) · [回归结果](unit-test-results.json) · [语义差异](semantic-diff.json) · [正式 manifest](../../../artifacts/v0.1.11/manifest.json) · [发布授权](../../../sources/evidence/release-v0.1.11-authorization.json) · [保留条目记录](../../../sources/evidence/release-v0.1.11-preserved-entry-exception.json)

## 完整发布规则

### anthropic

```json
{
  "rules": [
    {
      "domain": [
        "api.revenuecat.com",
        "api.stripe.com",
        "billing.stripe.com",
        "cdn.jsdelivr.net",
        "cdn.tailwindcss.com",
        "cdn.usefathom.com",
        "cdnjs.cloudflare.com",
        "challenges.cloudflare.com",
        "checkout.stripe.com",
        "code.jquery.com",
        "fcmtoken.googleapis.com",
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "formulae.brew.sh",
        "github.com",
        "js.stripe.com",
        "m.stripe.com",
        "r.stripe.com",
        "raw.githubusercontent.com",
        "registry.npmjs.org",
        "static.intercomassets.com",
        "storage.googleapis.com",
        "unpkg.com"
      ],
      "domain_keyword": [
        "datadog",
        "sentry",
        "sift"
      ],
      "domain_suffix": [
        "anthropic-com.ghost.io",
        "anthropic.auth0.com",
        "anthropic.com",
        "anthropic.com.cdn.cloudflare.net",
        "clau.de",
        "claude.ai",
        "claude.app",
        "claude.com",
        "claude.dev",
        "claudemcpclient.com",
        "claudemcpcontent.com",
        "claudeusercontent.com",
        "growthbook.io",
        "hcaptcha.com",
        "intercom.io",
        "intercomcdn.com",
        "segment.io",
        "servd-anthropic-website.b-cdn.net",
        "statsigapi.net",
        "stripe.network",
        "stripecdn.com",
        "withpersona.com"
      ],
      "ip_cidr": [
        "160.79.104.0/21",
        "2607:6bc0::/32",
        "34.8.0.0/16"
      ]
    }
  ],
  "version": 2
}
```

### openai

```json
{
  "rules": [
    {
      "domain": [
        "api.github.com",
        "browser-intake-datadoghq.com",
        "cdn.openaimerge.com",
        "cdn.workos.com",
        "challenges.cloudflare.com",
        "forwarder.workos.com",
        "frontend-apps-multi-region.workos.com",
        "github.com",
        "humb.apple.com",
        "images.workoscdn.com",
        "js.stripe.com",
        "o207216.ingest.sentry.io",
        "o33249.ingest.sentry.io",
        "openai.qualtrics.com",
        "openaiapi-site.azureedge.net",
        "openaiassets.blob.core.windows.net",
        "openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net",
        "openaicom.imgix.net",
        "openaicomproductionae4b.blob.core.windows.net",
        "production-openaicom-storage.azureedge.net",
        "registry.npmjs.org",
        "release-assets.githubusercontent.com",
        "rum.browser-intake-datadoghq.com",
        "setup.workos.com",
        "workos.imgix.net"
      ],
      "domain_regex": [
        "^chatgpt-async-webps-prod-\\S+-\\d+\\.webpubsub\\.azure\\.com$"
      ],
      "domain_suffix": [
        ".ct.sendgrid.net",
        ".intercom.io",
        ".intercomcdn.com",
        "chat.com",
        "chatgpt.com",
        "chatgpt.livekit.cloud",
        "chatgpt.site",
        "crixet.com",
        "host.livekit.cloud",
        "oaistatic.com",
        "oaistatsig.com",
        "oaiusercontent.com",
        "openai.com",
        "openai.com.cdn.cloudflare.net",
        "poteto.com",
        "sora.com",
        "turn.livekit.cloud"
      ],
      "ip_cidr": [
        "102.37.57.54/32",
        "13.71.25.29/32",
        "135.220.40.201/32",
        "172.203.39.49/32",
        "172.207.173.200/32",
        "172.214.226.198/32",
        "191.233.251.27/32",
        "20.162.96.163/32",
        "20.168.48.117/32",
        "20.184.36.134/32",
        "20.203.144.245/32",
        "20.74.221.21/32",
        "4.151.200.38/32",
        "4.155.146.196/32",
        "4.197.172.116/32",
        "4.217.235.100/32",
        "4.245.198.13/32",
        "40.118.236.137/32",
        "51.4.112.173/32",
        "52.143.181.161/32",
        "68.155.152.41/32",
        "72.146.20.246/32",
        "74.248.148.7/32"
      ]
    }
  ],
  "version": 2
}
```

### anthropic-ip

```json
{
  "rules": [
    {
      "source_ip_cidr": [
        "160.79.104.0/21"
      ]
    }
  ],
  "version": 2
}
```
