# v0.1.9 Persona 补充与最终发布记录

日期：2026-10-30。用户指令：**“联网搜索相关信息 添加并发布”**。

**已发布并设为 Latest。** [GitHub v0.1.9](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.9) 于 `2026-10-30T05:57:52Z` 公开，Release ID 为 `428698657`。规则仅新增 `withpersona.com`；固定及 Latest 各 6 个资产下载、各 214 项空缓存请求检查全部通过。

用户后续明确要求“先继续添加 发布”“继续 完成发布”，本次按限定旧条目保留例外完成静态发布。真实 Challenge 复验仍未完成，原复核日期及证据保持不变。未确认截图中的错误已经解决。

## 已核实的依据与唯一规则增量

- [Claude 身份验证说明](https://support.claude.com/en/articles/14328960-identity-verification-on-claude)确认验证服务商为 Persona。
- [Persona Security](https://docs.withpersona.com/security)列出 `withpersona.com` 根域及标准子域。
- [Persona WebView 网络要求](https://docs.withpersona.com/hosted-flow-webview-considerations)明确要求允许 `*.withpersona.com/*` 的外部网络请求。

因此在 Anthropic 规则中新增 **`domain_suffix: withpersona.com`**，覆盖根域及全部子域。标记为 `claude-identity-verification` 功能所需的共享依赖；它也会覆盖其他网站使用 Persona 的请求，不代表仅属于 Claude，也不代表已经证实截图中的错误得到修复。无需将 Persona 的邮件发送域名或服务器回调来源 IP 加入客户端目的规则。

三个官方页面均以普通 HTTPS 取得 HTTP 200，保存取得时间、响应摘要及事实定位；完整网页只保留于本地忽略目录，公开来源记录不复制整篇网页。[抓取记录](official-fetches.json) · [结构化事实](../../../sources/official/claude-identity.json) · [来源记录](../../../sources/official/source-records/claude-identity.json)。

| 制品 | 相对 v0.1.8 的变化 |
| --- | --- |
| `anthropic.srs` | 仅新增 `withpersona.com` 后缀 |
| `openai.srs` | 无规则变化 |
| `anthropic-ip.srs` | 无规则变化 |

完整证据：[语义差异](semantic-diff.json)、[候选可读规则](../../../artifacts/v0.1.9-rc.1/anthropic.json)、[候选 manifest](../../../artifacts/v0.1.9-rc.1/manifest.json)。

## 验证

- 候选构建通过；2,748 项原生匹配、源与二进制一致性、独立重建及隔离配置检查全部通过。[验证日志](candidate-validation.log)
- 第二次独立候选构建同样通过 2,748 项检查；三份 SRS、三份 JSON 和 manifest 均与第一次逐字节一致。[重建日志](rebuild-validation.log) · [构建汇总及制品摘要](build-results.json)
- 21 项专门检查通过：包括官方 11 个 Persona 域名、API/文件主机、多级子域、原有 Anthropic/Sift 对照及 3 个相似域名反例。[原始输出](persona-matches.json)
- 最终 79 项完整回归全部通过，无跳过，见[测试日志](unit-tests-final.log)。新增 5 项检查验证旧条目保留例外的日期、版本、输入与制品边界；最终候选另通过 2,748 项原生检查，见[日志](final-candidate-validation.log)。历史 v0.1.7/v0.1.8 差异与例外测试使用固定的 v0.1.8 Anthropic 源输入，避免把新功能误当成旧版本差异；新增单独测试核对当前版本只增加 Persona 及域名边界。原有发布校验断言未放宽。

## 正式构建

输入提交为 `92822cf877ba3c011d65fb7397d43169d8d868dc`。两次独立 release 构建分别通过 2,748 项原生检查与 `--for-release` 发布门槛，全部 9 个批次文件逐字节一致。同一提交生成的 candidate 再通过 2,748 项检查和 79 项完整回归；三份 SRS、三份 JSON 与正式批次一致。首次校验的 Go 相对路径调用失败已改用绝对路径重跑通过，没有修改校验逻辑。

[正式校验](release-validate.log) · [独立重建](release-rebuild-validate.log) · [同提交回归](unit-tests-release-fixture.log) · [构建汇总](build-results.json) · [完整正式批次](../../../artifacts/v0.1.9/manifest.json) · [批次校验和](../../../artifacts/v0.1.9/SHA256SUMS)。

## Challenge 记录与本次发布授权

发布预检实际返回：`Unapproved/expired compatibility: challenges.cloudflare.com`。[预检结果](release-preflight.json)

现有 Challenge 条目仍保留 `last_verified: 2026-09-27` 和 `review_after: 2026-10-27`。已有 v0.1.8 例外限定当日、版本、源文件及两份 Anthropic 制品全部不变；本次新增 Persona 后 Anthropic 制品发生变化，因此旧例外不能沿用。具体约束见[复核检查](../../../scripts/common.py)、[发布检查](../../../scripts/validate.py)与[v0.1.8 原例外](../../../sources/evidence/release-v0.1.8-unchanged-exception.json)。

联网确认 Persona 依赖不能冒充旧 Challenge 条目的新运行验证。随后检查到桌面端能进入现有会话，但没有出现可见 Challenge；浏览器控制不可用，用户选择稍后复验，再明确要求继续发布。见[初步观察](challenge-observation.json)。

本次新增的[限定例外](../../../sources/evidence/release-v0.1.9-preserved-entry-exception.json)只允许 2026-10-30 的 v0.1.9 发布，绑定 v0.1.8 源输入、原 Challenge 条目完整内容、唯一 Persona 增量及本批全部制品摘要；其他版本、日期、源变更或制品变化不能借用它。旧例外与旧运行证据保持原样。[本次发布授权](../../../sources/evidence/release-v0.1.9-authorization.json) · [语义审阅](../../../sources/evidence/release-v0.1.9-review.json)。

本批授权与语义审阅绑定、输入提交、两次正式构建及发布检查、草稿资产核对、非 Latest 固定下载与空缓存验证、Latest 切换及复核均已完成。静态发布与真实设备上的验证成功分开记录。


## 发布与下载验收

- 正式输入提交：`92822cf877ba3c011d65fb7397d43169d8d868dc`。
- 版本标签及源码 ZIP 固定提交：`c9da2d3e6081deb811f647387c0e8100e2cc3ad0`。源码 ZIP 中全部 manifest 输入与正式批次 `dist` 均已逐项核对。
- 草稿上传 6 个资产，API 返回的 SHA-256、大小、名称全部一致；正文保持为空。随后非 Latest 公开，经固定地址验收后切换 Latest。
- 固定版本及 Latest 各 6 个下载全部 HTTP 200，字节数和 SHA-256 与本地发布包一致。
- 固定版本及 Latest 各通过 208 个主请求与 6 个来源方向请求，共 428 项；三份远端 SRS 均由原生 sing-box 实际下载到全新缓存。两个进程均退出 0，4 个回环监听全部关闭。
- 10 个历史 Release 的 ID、tag、目标提交及已记录资产 ID/名称/大小/摘要保持一致；10 个旧标签引用保持一致。
- 最终回执另行提交至 main；版本标签和源码 ZIP 保持固定时点内容。

[机器汇总](publication-results.json) · [上传回执](release-asset-upload-receipts.json) · [固定下载](fixed-downloads.json) · [Latest 下载](latest-downloads.json) · [固定空缓存](remote-fixed/results.json) · [Latest 空缓存](remote-latest/results.json) · [历史保持检查](historical-releases-verification.json)。

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| [SHA256SUMS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.9/SHA256SUMS) | 409 | `b39133b8b9ff906e4e9bdf04804b0db780e25a392aebe68a42203326bd4d3aaf` |
| [anthropic-ip.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.9/anthropic-ip.srs) | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |
| [anthropic.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.9/anthropic.srs) | 535 | `13112b79d21073c4478f0e6a902acc7ba6dd7df9efe2c6749d9844afe97256c1` |
| [manifest.json](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.9/manifest.json) | 111139 | `4c6a7a14789eadab9d6e2741e3e46ea757084c32b83818a31d7f9aaf4aa9bea2` |
| [openai.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.9/openai.srs) | 802 | `5068d4d1a9c4550b803a887f03e7e91e647299007d02840fa8a4c38f5aa39c55` |
| [sing-box-ai-v0.1.9.zip](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.9/sing-box-ai-v0.1.9.zip) | 2476187 | `5adc92e42ea7bd617669b7393ae1b78032631a1c32134ad0158dafb6a5ea3a01` |

现有 Latest 订阅地址继续可用，客户端后续更新可取得新版；未确认实际设备已刷新。可以在客户端更新规则后重新尝试身份验证。

[Latest OpenAI](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs) · [Latest Anthropic](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [Latest Anthropic 来源 IP](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic-ip.srs)。

## 验证边界

未修改 N100、iPhone、生产代理配置、系统 DNS、路由或防火墙，未重启现有服务。空缓存检查在 Mac 隔离进程内进行，业务目标请求均由回环 SOCKS 测试规则拒绝；它证明规则下载、缓存和匹配，不证明真实登录、上传证件、Challenge 或账户验证成功。正式 manifest 仍为 `validated_consumers: []`、无消费者集成证据、`deployment_status: pending`。

## 本批完整规则清单

以下为正式 SRS 对应的完整源 JSON，便于在单个文档中核对所有域名和 IP。

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
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "formulae.brew.sh",
        "github.com",
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
        "2607:6bc0::/32"
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
