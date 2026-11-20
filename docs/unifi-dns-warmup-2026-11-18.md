# UniFi 域名受限预解析结果

2026 年 11 月 18 日 13:11（北京时间），对 UniFi 当前清单的 92 个名称及 `api.openai.com`、`api.anthropic.com` 两个已知子域做 A／AAAA 对照，共 94 个名称、188 个查询项。

**36 个域名的 A 记录通过核对并由 UniFi 本机查询。IPv4 学习集合从 0 增至 40 个地址，IPv6 集合仍为 0。** 40 个地址逐项与本机 DNS 回答一致。举例，`claude.ai`、`api.anthropic.com`、`antspace.dev` 和 `usefathom.com` 的 A 记录已入集合。 [现有防火墙与清单](unifi-blocking-completeness-2026-11-18.md)

## 结果汇总

| 结果 | 查询项数 |
| --- | ---: |
| 预热成功并读回学习集合 | 36 |
| 主网未取得该类型地址 | 84 |
| UniFi 上游地址与主网答案不一致 | 39 |
| 查询超时或失败 | 28 |
| 预热前的上游复查未通过 | 1 |
| 合计 | 188 |

先从管理 Mac 经 N100 查询，并在 UniFi 网关上直查它的四个上游。只选择两边结果一致、地址合法、与目前已知代理出口无重合的查询项。候选在预热前重新比对，再逐项交给 UniFi 本机 dnsmasq。`api.openai.com`、`github.com` 和 `stripe.com` 的 A 记录因答案不一致被跳过。所有 AAAA 项均未通过本轮比对。

复核中，DNS 配置、92 条域名下发、dnsmasq 和 N100 的 sing-box 进程一致。双栈四条相关 DROP 规则与前次网关快照一致。预热前后，正常 OpenAI API 路径均返回 401，百度均返回 200。本次确认预解析与地址入集合，未逐域测试实际直连阻断或重启后的保留情况。

## 逐项结果

| 域名 | A（IPv4） | AAAA（IPv6） |
| --- | --- | --- |
| `ant.dev` | 主网未取得该类型地址 | 主网未取得该类型地址 |
| `anthropic-com.ghost.io` | 上游地址不一致 | 查询超时或失败 |
| `anthropic.auth0.com` | 已入集合 `104.18.37.18`、`172.64.150.238` | 查询超时或失败 |
| `anthropic.com` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `anthropic.com.cdn.cloudflare.net` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `anthropic.team` | 主网未取得该类型地址 | 查询超时或失败 |
| `antspace.dev` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `api.anthropic.com` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `api.github.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `api.openai.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `api.revenuecat.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `api.stripe.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `billing.stripe.com` | 查询超时或失败 | 主网未取得该类型地址 |
| `browser-intake-datadoghq.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `cdn.jsdelivr.net` | 上游地址不一致 | 主网未取得该类型地址 |
| `cdn.openaimerge.com` | 已入集合 `104.18.2.136`、`104.18.3.136` | 主网未取得该类型地址 |
| `cdn.tailwindcss.com` | 已入集合 `104.26.2.143`、`104.26.3.143`、`172.67.68.11` | 主网未取得该类型地址 |
| `cdn.usefathom.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `cdn.workos.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `cdnjs.cloudflare.com` | 已入集合 `104.17.24.14`、`104.17.25.14` | 主网未取得该类型地址 |
| `challenges.cloudflare.com` | 已入集合 `104.18.94.41`、`104.18.95.41` | 主网未取得该类型地址 |
| `chat.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `chatbotclaude.com` | 查询超时或失败 | 主网未取得该类型地址 |
| `chatgpt.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `chatgpt.livekit.cloud` | 查询超时或失败 | 查询超时或失败 |
| `chatgpt.site` | 已入集合 `104.18.22.186`、`104.18.23.186` | 主网未取得该类型地址 |
| `checkout.stripe.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `clau.de` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claude.ai` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claude.app` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claude.com` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claude.dev` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claude.new` | 已入集合 `160.79.104.10` | 查询超时或失败 |
| `claude.site` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claudeacademy.com` | 查询超时或失败 | 查询超时或失败 |
| `claudemcpclient.com` | 主网未取得该类型地址 | 主网未取得该类型地址 |
| `claudemcpcontent.com` | 主网未取得该类型地址 | 主网未取得该类型地址 |
| `claudepages.dev` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claudestudio.com` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `claudeusercontent.com` | 已入集合 `160.79.104.10` | 主网未取得该类型地址 |
| `code.jquery.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `crixet.com` | 查询超时或失败 | 主网未取得该类型地址 |
| `ct.sendgrid.net` | 查询超时或失败 | 查询超时或失败 |
| `fcmtoken.googleapis.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `fonts.googleapis.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `fonts.gstatic.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `formulae.brew.sh` | 上游地址不一致 | 主网未取得该类型地址 |
| `forwarder.workos.com` | 已入集合 `104.18.41.116`、`172.64.146.140` | 主网未取得该类型地址 |
| `frontend-apps-multi-region.workos.com` | 查询超时或失败 | 主网未取得该类型地址 |
| `github.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `growthbook.io` | 上游地址不一致 | 查询超时或失败 |
| `hcaptcha.com` | 已入集合 `104.19.229.21`、`104.19.230.21` | 主网未取得该类型地址 |
| `host.livekit.cloud` | 查询超时或失败 | 主网未取得该类型地址 |
| `humb.apple.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `images.workoscdn.com` | 查询超时或失败 | 主网未取得该类型地址 |
| `intercom.io` | 上游地址不一致 | 查询超时或失败 |
| `intercomcdn.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `js.stripe.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `m.stripe.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `o207216.ingest.sentry.io` | 已入集合 `34.160.81.0` | 主网未取得该类型地址 |
| `o33249.ingest.sentry.io` | 已入集合 `34.160.81.0` | 主网未取得该类型地址 |
| `oaistatic.com` | 已入集合 `104.18.41.158`、`172.64.146.98` | 主网未取得该类型地址 |
| `oaistatsig.com` | 已入集合 `104.18.42.153`、`172.64.145.103` | 主网未取得该类型地址 |
| `oaiusercontent.com` | 主网未取得该类型地址 | 查询超时或失败 |
| `openai.com` | 已入集合 `104.18.33.45`、`172.64.154.211` | 主网未取得该类型地址 |
| `openai.com.cdn.cloudflare.net` | 已入集合 `104.18.33.45`、`172.64.154.211` | 主网未取得该类型地址 |
| `openai.qualtrics.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `openaiapi-site.azureedge.net` | 上游地址不一致 | 主网未取得该类型地址 |
| `openaiassets.blob.core.windows.net` | 已入集合 `20.150.95.164` | 主网未取得该类型地址 |
| `openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net` | 上游地址不一致 | 主网未取得该类型地址 |
| `openaicom.imgix.net` | 上游地址不一致 | 查询超时或失败 |
| `openaicomproductionae4b.blob.core.windows.net` | 查询超时或失败 | 查询超时或失败 |
| `poteto.com` | 查询超时或失败 | 主网未取得该类型地址 |
| `production-openaicom-storage.azureedge.net` | 查询超时或失败 | 主网未取得该类型地址 |
| `r.stripe.com` | 已入集合 `54.186.23.98`、`54.187.119.242`、`54.187.159.182` | 主网未取得该类型地址 |
| `raw.githubusercontent.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `registry.npmjs.org` | 上游地址不一致 | 主网未取得该类型地址 |
| `release-assets.githubusercontent.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `rum.browser-intake-datadoghq.com` | 预热前复查未通过 | 主网未取得该类型地址 |
| `segment.io` | 已入集合 `100.23.45.24`、`32.186.247.208`、`44.228.166.142` | 主网未取得该类型地址 |
| `servd-anthropic-website.b-cdn.net` | 查询超时或失败 | 查询超时或失败 |
| `setup.workos.com` | 已入集合 `104.18.35.233`、`172.64.152.23` | 主网未取得该类型地址 |
| `sora.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `static.intercomassets.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `statsigapi.net` | 已入集合 `34.128.128.0` | 主网未取得该类型地址 |
| `storage.googleapis.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `stripe.com` | 上游地址不一致 | 主网未取得该类型地址 |
| `stripe.network` | 上游地址不一致 | 主网未取得该类型地址 |
| `stripecdn.com` | 上游地址不一致 | 查询超时或失败 |
| `turn.livekit.cloud` | 上游地址不一致 | 查询超时或失败 |
| `unpkg.com` | 已入集合 `104.18.0.22`、`104.18.1.22` | 主网未取得该类型地址 |
| `usefathom.com` | 已入集合 `216.150.1.1` | 主网未取得该类型地址 |
| `withpersona.com` | 已入集合 `162.159.141.40`、`172.66.1.36` | 主网未取得该类型地址 |
| `workos.imgix.net` | 上游地址不一致 | 主网未取得该类型地址 |
