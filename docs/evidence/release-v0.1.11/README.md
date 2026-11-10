# v0.1.11 Claude 域名补充与发布记录

日期：2026-11-10。用户指令：添加以上未覆盖的规则 并发布。

**v0.1.11 已发布并设为 Latest，固定版本和 Latest 的下载及空缓存验证均通过。** [GitHub 发布页面](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.11)。现有 Latest 订阅地址无需修改，客户端刷新规则即可取得新版。

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

## 发布与下载验收

发布时间：2026-11-10 14:58:58（Asia/Shanghai）。固定版本和 Latest 各 6 个附件均返回 HTTP 200，大小及 SHA-256 与本地发布包一致。两个入口各完成 262 项主请求及 10 项来源方向检查，合计 544 项；三份远程 SRS 均由原生 sing-box 实际加载且完整写入新缓存。两个隔离进程正常退出，监听均已关闭。

12 个历史 Release 及其附件身份、摘要等记录保持不变，15 个历史标签引用保持不变。未访问或修改客户端设备，不将静态发布及本机隔离验证记为设备已刷新或真实业务已成功。

正式输入提交：`23a5994e96cee3b5ba4c21bcea13b7f3db33743f`；版本标签及源码 ZIP 固定于 `c9c513eef033311453f33499eb15af0bba15ca65`。ZIP 中全部 manifest 输入与正式 dist 已逐项校验。

首次固定版本验收已完成全部请求，但脚本末尾仍保留上版总数断言，因而失败；将主请求和域名请求计数修正为 262 和 241 后，使用全新缓存重新完成固定及 Latest 验收。初次结果保留于 [首次验收记录](remote-fixed-first-attempt/results.json) 和 [错误日志](remote-fixed-first-attempt.log)。修正后的验收脚本及最终回执提交至 main；已发布的 SRS、manifest、ZIP 和标签均未替换。

[发布汇总与全部附件校验值](publication-results.json) · [上传回执](release-asset-upload-receipts.json) · [固定下载](fixed-downloads.json) · [Latest 下载](latest-downloads.json) · [固定空缓存](remote-fixed/results.json) · [Latest 空缓存](remote-latest/results.json) · [历史保持核验](historical-releases-verification.json)。

[Latest Anthropic](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [Latest OpenAI](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs) · [Latest Anthropic 来源 IP](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic-ip.srs)。

Anthropic SRS 为 598 字节，SHA-256 为 `53793df8d575abf1892ca3e700b4d54ea4bbea67bfdad0e5bc87f3b9bc6e10ae`。

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
