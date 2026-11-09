# v0.1.10 截图规则补充与发布记录

发布日期：2026-11-08；最终记录整理：2026-11-09。用户指令：补充并发布。

**v0.1.10 已发布并设为 Latest，截图中的 14 个域名及 `34.8.0.0/16` 网段已全部覆盖。** [GitHub 发布页面](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.10) 于北京时间 2026-11-08 23:40:43 公开，Release ID 为 `438340281`。固定版本与 Latest 均完成下载及空缓存验收。

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

## 发布与下载验收

固定版本和 Latest 各 6 个附件均返回 HTTP 200，大小及 SHA-256 与本地发布包一致。两个入口各完成 230 个主请求和 10 个来源方向请求，共 480 项空缓存请求检查；三份远程 SRS 均由原生 sing-box 实际加载，新缓存含完整对应字节。两个隔离进程均退出 0，4 个回环监听全部关闭。

11 个历史 Release 的 ID、tag、目标提交及已记录附件信息保持一致，14 个历史 tag 引用未变。正式输入提交为 `c084a053bae204c2ddbb93ea8927bced269fc384`；版本标签及源码 ZIP 固定在 `d43bdac649a3b6f9b5aa017cd59c016d25291833`。ZIP 内全部 manifest 输入与正式 dist 已核对；最终回执另外提交到 main。

[发布汇总](publication-results.json) · [上传回执](release-asset-upload-receipts.json) · [固定下载](fixed-downloads.json) · [Latest 下载](latest-downloads.json) · [固定空缓存](remote-fixed/results.json) · [Latest 空缓存](remote-latest/results.json) · [历史保持检查](historical-releases-verification.json)。

现有 Latest 订阅地址无需更换；在客户端刷新规则即可取得新版。这里确认发布与隔离验证通过，未确认具体设备已经刷新。

[Latest Anthropic](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [Latest OpenAI](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs) · [Latest Anthropic 来源 IP](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic-ip.srs)。

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| [SHA256SUMS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.10/SHA256SUMS) | 410 | `80c25dda4ea7d097e9c7ecdecaed8752d3d44619814a5a1e02edf9df175828f7` |
| [anthropic-ip.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.10/anthropic-ip.srs) | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |
| [anthropic.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.10/anthropic.srs) | 561 | `e12a2a365d9ccd7092e5ed08e529402585091c0c4aad20a17e91281971f551f0` |
| [manifest.json](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.10/manifest.json) | 114229 | `819b907dd6a0d67c297afe81fe17673bbf8a8efe782ce31fbbbc4cba5ef25324` |
| [openai.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.10/openai.srs) | 802 | `5068d4d1a9c4550b803a887f03e7e91e647299007d02840fa8a4c38f5aa39c55` |
| [sing-box-ai-v0.1.10.zip](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.10/sing-box-ai-v0.1.10.zip) | 2616284 | `b40ff855d22a55cbd14870e7552d89f7ed8ae71b93bc2cdacefffe0764f4df13` |

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
