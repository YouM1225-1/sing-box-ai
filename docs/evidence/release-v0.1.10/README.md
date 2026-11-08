# v0.1.10 截图规则补充与发布记录

日期：2026-11-08。用户指令：补充并发布。

规则已补齐并完成本地验证，正式发布进行中。

| 新增项目 | 匹配方式 |
| --- | --- |
| `r.stripe.com` | 精确域名 |
| `fcmtoken.googleapis.com` | 精确域名 |
| `34.8.0.0/16` | 目的 IPv4 网段 |

仅 Anthropic 目的规则增加这三项。两域名未扩大为父域或子域，网段未加入来源 IP 规则。它们按用户指定范围登记，不标为官方依赖或 Claude 专用地址。OpenAI 与 Anthropic 来源 IP 两份 SRS 保持 v0.1.9 字节不变。

两次独立正式构建各通过 2,784 项原生检查及发布门槛，9 个批次文件逐字节一致；同一提交的候选 JSON/SRS 与正式批次一致。84 项回归全部通过、无跳过；中断后按同一输入保存并续跑测试。另有 62 项原生截图覆盖、精确域名边界及相邻网段检查通过。

[构建汇总](build-results.json) · [回归结果](unit-test-results.json) · [原生覆盖结果](screenshot-native-matches.json) · [语义差异](semantic-diff.json) · [正式 manifest](../../../artifacts/v0.1.10/manifest.json)。

原 Challenge 条目仍保留 `last_verified: 2026-09-27`、`review_after: 2026-10-27`；原 IPv6 `/48` 条目仍保留 `last_verified: 2026-10-09`、`review_after: 2026-11-08`。本次限定发布记录绑定原条目、日期、版本、三个新增条目及制品摘要，不将其记为重新完成运行验证。首次正式预检暴露的 IPv6 到期问题与处理结果均保留。

[发布授权](../../../sources/evidence/release-v0.1.10-authorization.json) · [保留条目限定记录](../../../sources/evidence/release-v0.1.10-preserved-entry-exception.json)。设备实际规则刷新及业务运行验收未包含在本次静态发布中。

## 本批完整规则

### anthropic.srs

```json
{
  "rules": [
    {
      "domain": [
        "cdn.jsdelivr.net",
        "cdn.tailwindcss.com",
        "cdn.usefathom.com",
        "cdnjs.cloudflare.com",
        "challenges.cloudflare.com",
        "code.jquery.com",
        "fcmtoken.googleapis.com",
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "formulae.brew.sh",
        "github.com",
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

### anthropic-ip.srs

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

### openai.srs

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
