# OpenAI 域名更新与仓库覆盖核对

核对日期：2026-10-19（北京时间）。仓库：`sing-box-ai`；HEAD：`217e1efb2d93218e155c61b213e138c0a8d95a40`；当前版本：`v0.1.5`。

> 本文保留更新前（v0.1.5）的审计结果。后续更新与发布记录见 [v0.1.6](evidence/release-v0.1.6/README.md)。

## 结论

**有更新，当前仓库尚未完整覆盖最新官方网络清单。确定遗漏 1 个精确域名，另有 1 个 GitHub 上游新增但仍待核实的域名后缀。**

| 检查范围 | 当前结果 | 判断 |
| --- | --- | --- |
| OpenAI 官方网络主清单 | 31 项中覆盖 30 项 | 缺 `frontend-apps-multi-region.workos.com` |
| 官方新增的另一项 | `cdn.platform.openai.com` 已命中 | 现有 `openai.com` 后缀已覆盖，无需重复加规则 |
| v2fly、MetaCubeX、Loyalsoldier 的 OpenAI 集合 | 三者都是 24 条，仓库语义覆盖 23 条 | 差异均为 `openai.org`；其归属与产品必要性仍有疑问 |
| 官方 WebSocket 目标 | 2/2 命中 | `ws.chatgpt.com`、`chatgpt.com` |
| 官方 ChatGPT Voice IP | 23/23 已包含，集合无变化 | 没有发现需要新增或删除的语音 IP |
| 发布 JSON 与 SRS | 语义一致；独立重编译字节一致 | 本次发现属于清单更新滞后 |

以上数量只描述本次核对的清单，不能解释为所有 OpenAI 产品、插件、外部网站和所有网络环境的全量可用性保证。官方来源：[网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)、[Voice IP 数据](https://openai.com/chatgpt-voice.json)。上游差异：[v2fly #4149](https://github.com/v2fly/domain-list-community/pull/4149)。

导航：[新增项与建议](#新增项与建议) · [官方完整清单](#官方完整清单) · [GitHub 对照](#github-对照) · [旧规则差异清单](#旧规则差异清单) · [本地实测](#本地实测) · [当前规则完整内容](#当前规则完整内容)

## 新增项与建议

### 应补入：frontend-apps-multi-region.workos.com

当前英文官方网络文档明确列出了该地址，仓库保存的 2026-09-27 主清单没有它。当前 SRS 仅包含 `cdn.workos.com`、`forwarder.workos.com`、`setup.workos.com` 等精确地址，不包含整个 `workos.com` 后缀，因此不会覆盖该地址。原生匹配也证实未命中。[官方清单](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)

建议的最小变更是增加 `domain: frontend-apps-multi-region.workos.com`，沿用现有 WorkOS 条目的共享依赖标记与来源记录方式。应同时更新官方事实快照与来源记录，再按仓库已有流程生成并验证新批次。没有依据把范围扩大为整个 `workos.com`。

### 已覆盖：cdn.platform.openai.com

这也是相对仓库 2026-09-27 快照新增的官方清单条目；当前 `domain_suffix: openai.com` 已覆盖它。需要刷新来源证据，不需要增加重复域名规则。[官方清单](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)

官方页面本次抓取显示 `Updated: 3 days ago`。这是页面的相对更新时间，不能据此认定这两个域名恰好在某一天新增；可确认的是“本地旧快照没有，当前英文页面有”。旧快照主清单为 29 项，现为 31 项，未发现删除项。

### 待核候选：openai.org

v2fly 在 **2026-10-17 12:58:53 UTC（北京时间 20:58:53）** 合并新增 `openai.org`，提交为 `5b1678867da0afc35854f481c1749a39048952df`。MetaCubeX 和 Loyalsoldier 的本次最新构建也已包含它。当前仓库对 `openai.org` 及其子域均不匹配。[提交记录](https://github.com/v2fly/domain-list-community/commit/5b1678867da0afc35854f481c1749a39048952df)

但该 PR 中，Loyalsoldier 明确询问归属证据；合并者仅引用 WHOIS、证书记录，并推测它可能是内部域名。本次没有从官方网络文档确认其产品用途；尝试打开主页也未取得可核实的页面。这不证明它不属于 OpenAI，但不足以把它认定为 ChatGPT 必需连接。建议先列为发现候选，补充官方用途或实际请求证据后再决定是否纳入。[PR 讨论](https://github.com/v2fly/domain-list-community/pull/4149)

本次完成的是联网审计与报告，未更改规则源、发布产物、订阅或运行中的网络配置。

## 官方完整清单

依据当前英文[官方网络文档](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)的 31 项主清单逐项核对。表中 `domain` 为精确匹配；`domain_suffix` 为后缀规则。带前导点的后缀只覆盖子域，例如 `.intercom.io` 不匹配根域 `intercom.io`，但足以覆盖官方要求的 `*.intercom.io`。

| 官方条目 | 仓库覆盖依据 | 相对 2026-09-27 快照 |
| --- | --- | --- |
| `*.auth.openai.com` | `domain_suffix: openai.com` | 已有 |
| `*.chatgpt.com` | `domain_suffix: chatgpt.com` | 已有 |
| `*.ct.sendgrid.net` | `domain_suffix: .ct.sendgrid.net` | 已有 |
| `*.intercom.io` | `domain_suffix: .intercom.io` | 已有 |
| `*.intercomcdn.com` | `domain_suffix: .intercomcdn.com` | 已有 |
| `*.oaistatic.com` | `domain_suffix: oaistatic.com` | 已有 |
| `*.oaiusercontent.com` | `domain_suffix: oaiusercontent.com` | 已有 |
| `*.openai.com` | `domain_suffix: openai.com` | 已有 |
| `*.oaistatsig.com` | `domain_suffix: oaistatsig.com` | 已有 |
| `android.chat.openai.com` | `domain_suffix: openai.com` | 已有 |
| `auth0.openai.com` | `domain_suffix: openai.com` | 已有 |
| `cdn.openaimerge.com` | `domain: cdn.openaimerge.com` | 已有 |
| `cdn.platform.openai.com` | `domain_suffix: openai.com` | 新增 |
| `cdn.workos.com` | `domain: cdn.workos.com` | 已有 |
| `challenges.cloudflare.com` | `domain: challenges.cloudflare.com` | 已有 |
| `chat.openai.com` | `domain_suffix: openai.com` | 已有 |
| `desktop.chat.openai.com` | `domain_suffix: openai.com` | 已有 |
| `forwarder.workos.com` | `domain: forwarder.workos.com` | 已有 |
| `frontend-apps-multi-region.workos.com` | **未覆盖** | 新增 |
| `humb.apple.com` | `domain: humb.apple.com` | 已有 |
| `images.workoscdn.com` | `domain: images.workoscdn.com` | 已有 |
| `ios.chat.openai.com` | `domain_suffix: openai.com` | 已有 |
| `js.intercomcdn.com` | `domain_suffix: .intercomcdn.com` | 已有 |
| `js.stripe.com` | `domain: js.stripe.com` | 已有 |
| `o207216.ingest.sentry.io` | `domain: o207216.ingest.sentry.io` | 已有 |
| `o33249.ingest.sentry.io` | `domain: o33249.ingest.sentry.io` | 已有 |
| `rum.browser-intake-datadoghq.com` | `domain: rum.browser-intake-datadoghq.com` | 已有 |
| `setup.auth.openai.com` | `domain_suffix: openai.com` | 已有 |
| `setup.workos.com` | `domain: setup.workos.com` | 已有 |
| `tcr9i.chat.openai.com` | `domain_suffix: openai.com` | 已有 |
| `workos.imgix.net` | `domain: workos.imgix.net` | 已有 |

官方 WebSocket 目标 `wss://ws.chatgpt.com` 和 `wss://chatgpt.com/` 均由 `chatgpt.com` 后缀覆盖。官方要求 TCP 443 并允许 WebSocket Upgrade；这类协议与连接超时要求不是增加域名条目就能解决的。[WebSocket 要求](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)

官方[登录排障页](https://help.openai.com/en/articles/7426629-why-cant-i-log-in-to-chatgpt)中涉及的 `chatgpt.com`、`openai.com`、`auth.openai.com`、`help.openai.com` 均已覆盖。`register.appattest.apple.com` 在网络文档中是 iOS 排障访问地址，并非主清单中的强制代理条目；当前未覆盖不计为本次确定遗漏。

## GitHub 对照

本次直接读取公开源文件、GitHub 提交与发行元数据；Loyalsoldier 的 `geosite.dat` 已实际下载、验证 SHA-256 并提取 OPENAI 集合。

| 规则源 | 核对版本或时间 | 结果 |
| --- | --- | --- |
| [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community/blob/5b1678867da0afc35854f481c1749a39048952df/data/openai) | OpenAI 文件最近修改：2026-10-17；`5b167886…` | 24 条，覆盖 23 条，差 `openai.org` |
| [MetaCubeX/meta-rules-dat，sing JSON](https://github.com/MetaCubeX/meta-rules-dat/blob/47fe33701f64a9a4e02b9c3a4237e0223b763196/geo/geosite/openai.json) | 2026-10-19 00:21:17 UTC；`47fe3370…` | 同一 24 条；覆盖情况相同 |
| [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat/releases/tag/202610182205) | 发行 `202610182205`，2026-10-18 22:06:25 UTC 发布 | 解码后同一 24 条；覆盖情况相同 |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script/blob/0fa60782abfe70f58da510e90d9086136cf0d855/rule/Clash/OpenAI/OpenAI.list) | OpenAI 文件最近提交：2025-06-17；文件头 UPDATED：2025-06-06 | 35 条，包含较宽共享域名、关键词、旧 IP 和 ASN，需另作解释 |

三个较新的规则源存在上游继承关系，其集合一致不能当成三份独立的域名归属证据。MetaCubeX 的 `.list` 版本只有 23 条，无法表达该正则；本次比较使用保留正则的 sing JSON，避免把格式限制误判为域名删除。

近期历史补充：`oaistatsig.com` 于 [2026-06-06 的 PR #3690](https://github.com/v2fly/domain-list-community/pull/3690) 加入；`openai.qualtrics.com` 与 `openaiassets.blob.core.windows.net` 于 [2026-07-02 的 PR #3798](https://github.com/v2fly/domain-list-community/pull/3798) 加入；`chatgpt.site` 于 [2026-07-13 的 PR #3842](https://github.com/v2fly/domain-list-community/pull/3842) 加入。这些条目当前仓库均已覆盖。

以下是三者一致的 24 条集合，按规则语义比较：

| 类型 | 值 | 当前仓库 |
| --- | --- | --- |
| suffix | `chat.com` | 已覆盖 |
| suffix | `chatgpt.com` | 已覆盖 |
| suffix | `chatgpt.site` | 已覆盖 |
| suffix | `crixet.com` | 已覆盖 |
| suffix | `oaistatic.com` | 已覆盖 |
| suffix | `oaistatsig.com` | 已覆盖 |
| suffix | `oaiusercontent.com` | 已覆盖 |
| suffix | `openai.com` | 已覆盖 |
| suffix | `openai.org` | 未覆盖；待核候选 |
| suffix | `sora.com` | 已覆盖 |
| suffix | `openai.com.cdn.cloudflare.net` | 已覆盖 |
| exact | `openaiapi-site.azureedge.net` | 已覆盖 |
| exact | `openaiassets.blob.core.windows.net` | 已覆盖 |
| exact | `openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net` | 已覆盖 |
| exact | `openaicom.imgix.net` | 已覆盖 |
| exact | `openaicomproductionae4b.blob.core.windows.net` | 已覆盖 |
| exact | `production-openaicom-storage.azureedge.net` | 已覆盖 |
| regex | `^chatgpt-async-webps-prod-\S+-\d+\.webpubsub\.azure\.com$` | 已覆盖 |
| exact | `browser-intake-datadoghq.com` | 已覆盖 |
| exact | `o33249.ingest.sentry.io` | 已覆盖 |
| exact | `openai.qualtrics.com` | 已覆盖 |
| suffix | `chatgpt.livekit.cloud` | 已覆盖 |
| suffix | `host.livekit.cloud` | 已覆盖 |
| suffix | `turn.livekit.cloud` | 已覆盖 |

## 旧规则差异清单

[blackmatrix7 的 OpenAI 清单](https://github.com/blackmatrix7/ios_rule_script/blob/0fa60782abfe70f58da510e90d9086136cf0d855/rule/Clash/OpenAI/OpenAI.list)有 35 条，其中当前仓库完整覆盖 12 条、完全未覆盖 13 条、覆盖范围较窄 6 条，另有 4 条关键词/IP/ASN 规则没有采用。**这些差异不等同于 23 个已确认的功能缺陷**：该文件较旧，且混合共享服务与粗粒度匹配。本次未找到将以下全部条目认定为当前必需依赖的官方证据。

### 完全未覆盖的 13 条

| 类型 | 值 | 审计判断 |
| --- | --- | --- |
| exact | `openai-api.arkoselabs.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| exact | `static.cloudflareinsights.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `ai.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `algolia.net` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `api.statsig.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `auth0.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `client-api.arkoselabs.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `events.statsigapi.net` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `featuregates.org` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `identrust.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `launchdarkly.com` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `observeit.net` | 旧源候选，当前必要性待核，不建议直接整批补入 |
| suffix | `segment.io` | 旧源候选，当前必要性待核，不建议直接整批补入 |

### 当前覆盖范围较窄的 6 条

| 旧源范围 | 当前仓库覆盖 | 差异含义 |
| --- | --- | --- |
| `intercom.io` 后缀 | `.intercom.io` | 子域已覆盖，根域未覆盖；符合官方通配符范围 |
| `intercomcdn.com` 后缀 | `.intercomcdn.com` | 子域已覆盖，根域未覆盖；符合官方通配符范围 |
| `openaiapi-site.azureedge.net` 后缀 | 同名精确域名 | 根地址已覆盖，不扩展未知子域 |
| `openaicom.imgix.net` 后缀 | 同名精确域名 | 根地址已覆盖，不扩展未知子域 |
| `sentry.io` 后缀 | `o207216.ingest.sentry.io`、`o33249.ingest.sentry.io` | 覆盖官方列出的租户，不扩展整个服务商 |
| `stripe.com` 后缀 | `js.stripe.com` | 覆盖官方列出的端点，不扩展整个服务商 |

### 没有采用的另外 4 条

- `DOMAIN-KEYWORD,openai`
- `IP-CIDR,24.199.123.28/32`
- `IP-CIDR,64.23.132.171/32`
- `IP-ASN,20473`

关键词可能匹配无关域名，整个 ASN 的范围也显著大于已确认的 OpenAI 端点；两个旧 IP 不在本次抓取的官方 Voice 列表中。没有新的产品用途证据时，不应仅为与旧清单逐字一致而扩大规则范围。

## 本地实测

审计使用当前工作区的 [v0.1.5 JSON](../artifacts/v0.1.5/openai.json) 与 [dist/openai.srs](../dist/openai.srs)，并检查 [补充规则源](../sources/openai.yaml)、[策略文件](../sources/policy.yaml)、[旧官方快照](evidence/release-v0.1.6/before/openai-network.json)、[旧来源记录](evidence/release-v0.1.6/before/openai-network-source-record.json)。

验证包含 JSON 语义比较、sing-box 原生 `rule-set match`、SRS 反编译与临时目录中的独立重编译。通配符使用子域见证；上游后缀检查根域与子域；正则使用符合其表达式的见证。有限见证用于验证实际二进制行为，完整范围判定仍依据规则语义。

| 原生匹配对象 | 结果 |
| --- | --- |
| 官方 31 项主清单 | 30 项命中，WorkOS 新地址未命中 |
| 两个官方 WebSocket 域名 | 2 项命中 |
| v2fly 24 条规则的 38 个见证 | 36 个命中；`openai.org` 根域与子域未命中 |
| `cdn.platform.openai.com` | 命中 |
| `frontend-apps-multi-region.workos.com` | 未命中 |
| `openai.org`、`www.openai.org`、`a.b.openai.org` | 未命中 |
| `cdn.workos.com` | 命中 |
| `workos.com`、`a.cdn.workos.com` | 未命中，精确域名没有被误当作后缀 |
| `intercom.io` / `a.intercom.io` | 根域未命中 / 子域命中 |

原生 `rule-set match` 对未命中也可能返回退出码 0，因此本次依据实际 `match rules.[0]` 输出判断，没有把退出码 0 当作命中证据。

SRS 反编译可能把 `/32` 写作单 IP、把单个正则数组写作字符串；归一化这些表示差异后与 JSON 语义一致。独立重新编译同一 JSON 后，得到的 SRS 与当前 dist 字节完全一致。

- `dist/openai.srs` SHA-256：`a910767e3f07dfe89e2f72639960612872361d9ae1c8553ddd4a59c8f154778f`
- `artifacts/v0.1.5/openai.json` SHA-256：`8f1efe104bb5dd78fc1af9cf94e2ba2b6a7984667f4e9d6686d73c5e6dcd9c5f`
- Loyalsoldier `geosite.dat` SHA-256：`3691de3874692fc8709686998c7627d030df3910d21f3d68232aaa0f1249dd2d`
- 当前官方 Voice JSON SHA-256：`8f03f3c594165eeff009915c7e2beb4bdfb9d429fb1955c205e3b33ec781899a`

本次未执行路由器部署、账户登录、真实语音会话或消费者配置的端到端验证。规则命中并不证明它在某台设备上最终优先于其他路由规则。

### 语音范围

官方 [chatgpt-voice.json](https://openai.com/chatgpt-voice.json) 本次直接下载成功，`creationTime` 为 `2026-03-26T20:12:45.451356+00:00`；23 个 IPv4 /32 与当前产物集合一致。该时间是数据源提供的生成时间，不是本次抓取时间。官方建议 UDP 3478，并提供 TCP 443 回退；本次只确认地址集合覆盖，没有据此声称 UDP 路径已实测可用。

### 证据时效

- 当前官方网络页通过联网检索工具成功打开并读取完整英文正文；普通 HTTP 客户端获取 HTML 返回 403，未把错误页当作来源内容。
- 本地官方网络事实快照采集于 2026-09-27；DLC/Sager 固定基线最后校验于 2026-10-03。仓库版本更新至 2026-10-15 不代表所有 OpenAI 资料均在当天重新抓取。
- `sources/openai.yaml` 最后改动于 2026-09-28；v0.1.1 到 v0.1.5 的 OpenAI JSON/SRS 字节相同，最近发布并没有刷新这部分规则。
- GitHub 文件采用提交/发行时间；页面相对更新时间仅保留原始表述，不推算域名上线日期。
- 域名归属、被规则库收录、产品当前实际依赖，是不同层次的证据。本报告分别列明。

## 当前规则完整内容

以下内嵌当前 OpenAI 产物的全部规则，便于在单文件预览中核对：24 个精确域名、16 个后缀、1 个正则、23 个语音 IP。此处为审计时的原状，**不含上述建议新增项**。

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

## 最小后续处理清单

1. 为 `frontend-apps-multi-region.workos.com` 增加精确规则，并更新官方来源快照、来源哈希与审阅日期。
2. 将 `cdn.platform.openai.com` 记录为新增官方事实，但复用 `openai.com` 后缀覆盖。
3. 把 `openai.org` 单独登记为上游发现候选，补齐用途证据；不与确定的官方遗漏合并判断。
4. 生成新批次并验证新增命中、精确域名边界、历史覆盖以及 JSON/SRS 一致性，再按需要进行消费者配置验证。

当前不需要因本次审计调整语音 IP，也没有证据要求批量导入 blackmatrix7 的宽泛共享域名、关键词或 ASN。
