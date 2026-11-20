# OpenAI 与 Claude 域名 / IP 联网核查

核查日期：**2026-10-20**；汇总于北京时间 **23:48**。比较对象：[已发布 v0.1.6](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.6)，联网确认当前仍为 Latest。

**结论：在本次检查的官方资料和 GitHub 上游中，未发现需要为仓库当前已选客户端功能新增的域名或 IP，本轮无需重新发布。** OpenAI 昨天补齐的 WorkOS 主机仍在官方清单中；Claude 的域名与 IP 需求也已被现有规则覆盖。`openai.org` 仍有归属疑问，今天凌晨的新评论进一步支持保持待核。

本次只新增审计报告和证据，规则源、制品、版本与 GitHub Release 均未修改。

导航：[结果概览](#result) · [新证据与待核项](#changes) · [OpenAI 完整核对清单](#openai) · [Claude 完整核对清单](#claude) · [IP 方向与范围](#ip) · [验证与来源](#evidence)

<a id="result"></a>
## 结果概览

| 范围 | 当前结果 | 相对仓库记录的变化 |
|---|---|---|
| OpenAI 官方网络主清单 | **31/31 覆盖** | 相对 10 月 19 日记录，新增 0、删除 0 |
| ChatGPT / Codex WebSocket | **2/2 覆盖** | 目标主机未变 |
| ChatGPT Voice 目的 IP | **23/23 覆盖** | 原始 JSON 字节及 IP 集合均未变 |
| 本次核查的 Codex 网络 / 安装主机 | **8/8 覆盖** | 安装脚本哈希未变；新查到的主机已有后缀覆盖 |
| Claude Code 网络要求 | 已覆盖已选功能 | 相对仓库原始记录，域名无新增、无删除 |
| Claude Desktop / Artifacts / 客服依赖 | 合并 Code 后，44 项事实中 43 项覆盖 | 仅可选 Gerrit 未启用；Desktop 备选列表少了 `a-cdn.claude.ai` |
| Anthropic API IP | 官方两段目的 IP、一段出站源 IP均覆盖 | 官方文档响应与旧快照完全相同 |
| AS399358 路由公告 | **3/3 网段覆盖** | 与 10 月 15 日记录相同 |
| 4 个 GitHub 上游 | 每源 OpenAI 24 条、Anthropic 9 条 | 无昨日之后已合并的新域名；OpenAI 唯一未选差异仍是 `openai.org` |

主清单来源：[OpenAI 网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)、[Claude Code 网络配置](https://code.claude.com/docs/en/network-config)、[Claude Desktop 网络要求](https://code.claude.com/docs/en/desktop)。44 项 Claude 事实包含通配符方案、具体主机备选方案、可选功能及客服页面实测依赖，不表示 44 个独立必需服务。

<a id="changes"></a>
## 新证据、清单变化与待核项

| 项目 | 本次证据 | 处理结论 |
|---|---|---|
| `openai.org` | 北京时间 **10 月 20 日 00:09:40**，社区提交者承认加入时未充分核实所有权 | 继续待核，不纳入 OpenAI 规则；这不是今天新发现的域名 |
| `o33249.ingest.us.sentry.io` | PR #4057 仍未合并，维护者仍在索要来源；PR 创建于 9 月 14 日，仓库 9 月 27 日已登记 pending | 既有遥测候选，不能认定为新增必需依赖；OpenAI SRS 当前不匹配 |
| `a-cdn.claude.ai` | 当前 Desktop 的具体主机备选清单相对本地 9 月 27 日记录少了此项 | 没有新增；现有 `claude.ai` 后缀仍覆盖，不能仅凭清单删除认定停用 |
| `code.claude.com` | 旧归一化 facts 未列，但同日原始来源记录已列；当前文档仍列 | 来源 facts 可补充记录，成品已由 `claude.com` 覆盖，不是新域名或规则缺口 |
| `codex-cloud-environments.chatgpt.com` | 当前 self-hosted executor 文档确认其命令/结果 WebSocket 用途 | 已由 `chatgpt.com` 覆盖；没有充分历史基线判定上线时间 |

关键证据：[openai.org 新评论](https://github.com/v2fly/domain-list-community/pull/4149#issuecomment-6271665917)、[遥测候选 PR #4057](https://github.com/v2fly/domain-list-community/pull/4057)、[self-hosted executor 网络要求](https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted)。

OpenAI 的 `o33249.ingest.us.sentry.io` 与主清单中的 `o33249.ingest.sentry.io` 是不同主机。前者没有进入 OpenAI 规则；仓库 Claude 集合现有的 `sentry` 关键词可匹配该共享遥测主机，这不构成 OpenAI 必需性证据，也不能据此推断真实设备的最终路由。

<a id="openai"></a>
## OpenAI 完整核对清单

以下 31 项来自本次实际打开的官方英文网络页，均已覆盖，且与 10 月 19 日来源记录一致。页面显示的相对更新时间不用于推断域名上线日期。

```text
*.auth.openai.com
*.chatgpt.com
*.ct.sendgrid.net
*.intercom.io
*.intercomcdn.com
*.oaistatic.com
*.oaiusercontent.com
*.openai.com
*.oaistatsig.com
android.chat.openai.com
auth0.openai.com
cdn.openaimerge.com
cdn.platform.openai.com
cdn.workos.com
challenges.cloudflare.com
chat.openai.com
desktop.chat.openai.com
forwarder.workos.com
frontend-apps-multi-region.workos.com
humb.apple.com
images.workoscdn.com
ios.chat.openai.com
js.intercomcdn.com
js.stripe.com
o207216.ingest.sentry.io
o33249.ingest.sentry.io
rum.browser-intake-datadoghq.com
setup.auth.openai.com
setup.workos.com
tcr9i.chat.openai.com
workos.imgix.net
```

WebSocket 两个主机：`ws.chatgpt.com`、`chatgpt.com`，均覆盖。`register.appattest.apple.com` 仍出现在 iOS 诊断步骤，不属于上述主清单，也没有被当成本次新增必需项。

本次确认的 8 个 Codex 主机均已覆盖：

```text
chatgpt.com
releases.openai.com
api.github.com
github.com
release-assets.githubusercontent.com
registry.npmjs.org
api.openai.com
codex-cloud-environments.chatgpt.com
```

公开安装脚本内容哈希与仓库原始记录相同；只读取文档、脚本和元数据，未执行安装。来源、定位及逐项标记见 [OpenAI 官方事实](evidence/network-audit-2026-10-20/openai/official-facts.json)。

ChatGPT Voice 当前完整目的 IP 列表如下，23 个 IPv4 `/32`，无 IPv6；原始 [Voice JSON](https://openai.com/chatgpt-voice.json) 的 `creationTime` 仍为 `2026-03-26T20:12:45.451356+00:00`。

```text
102.37.57.54/32
13.71.25.29/32
135.220.40.201/32
172.203.39.49/32
172.207.173.200/32
172.214.226.198/32
191.233.251.27/32
20.162.96.163/32
20.168.48.117/32
20.184.36.134/32
20.203.144.245/32
20.74.221.21/32
4.151.200.38/32
4.155.146.196/32
4.197.172.116/32
4.217.235.100/32
4.245.198.13/32
40.118.236.137/32
51.4.112.173/32
52.143.181.161/32
68.155.152.41/32
72.146.20.246/32
74.248.148.7/32
```

本次下载的 Voice JSON 与既有归档字节一致，SHA-256 为 `8f03f3c594165eeff009915c7e2beb4bdfb9d429fb1955c205e3b33ec781899a`。

<a id="claude"></a>
## Claude 完整核对清单

以下 44 项为本次文档和客服页面中提取的去重事实。43 项已覆盖，唯一例外是当前未启用的可选 Gerrit 查询，属于既有范围选择。`domain` 是精确主机，`domain_suffix` 是后缀，`domain_keyword` 是字符串包含；共享依赖和关键词可能同时匹配其他应用请求。

| # | 官方条目 / 页面实测主机 | 用途 | v0.1.6 覆盖依据 |
|---|---|---|---|
| 1 | `*-review.googlesource.com` | 可选 | 未选用的可选 Gerrit 功能 |
| 2 | `*.frame.claudeusercontent.com` | 功能依赖 | `domain_suffix: claudeusercontent.com` |
| 3 | `api.anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 4 | `bridge.claudeusercontent.com` | 功能依赖 | `domain_suffix: claudeusercontent.com` |
| 5 | `browser-intake-us5-datadoghq.com` | 可选 | `domain_keyword: datadog` |
| 6 | `claude.ai` | Desktop 网络要求 | `domain_suffix: claude.ai` |
| 7 | `claude.com` | Desktop 网络要求 | `domain_suffix: claude.com` |
| 8 | `code.claude.com` | 功能依赖 | `domain_suffix: claude.com` |
| 9 | `downloads.claude.ai` | Desktop 网络要求 | `domain_suffix: claude.ai` |
| 10 | `formulae.brew.sh` | 功能依赖 | `domain: formulae.brew.sh` |
| 11 | `github.com` | 功能依赖 | `domain: github.com` |
| 12 | `http-intake.logs.us5.datadoghq.com` | 可选 | `domain_keyword: datadog` |
| 13 | `mcp-proxy.anthropic.com` | 功能依赖 | `domain_suffix: anthropic.com` |
| 14 | `platform.claude.com` | Desktop 网络要求 | `domain_suffix: claude.com` |
| 15 | `raw.githubusercontent.com` | 功能依赖 | `domain: raw.githubusercontent.com` |
| 16 | `registry.npmjs.org` | 功能依赖 | `domain: registry.npmjs.org` |
| 17 | `storage.googleapis.com` | 功能依赖 | `domain: storage.googleapis.com` |
| 18 | `*.anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 19 | `*.claude.ai` | Desktop 网络要求 | `domain_suffix: claude.ai` |
| 20 | `*.claude.app` | Desktop 网络要求 | `domain_suffix: claude.app` |
| 21 | `*.claude.com` | Desktop 网络要求 | `domain_suffix: claude.com` |
| 22 | `*.claudemcpcontent.com` | Desktop 网络要求 | `domain_suffix: claudemcpcontent.com` |
| 23 | `*.claudeusercontent.com` | Desktop 网络要求 | `domain_suffix: claudeusercontent.com` |
| 24 | `*.livepreview.claude.ai` | Desktop 网络要求 | `domain_suffix: claude.ai` |
| 25 | `*.livepreview.claude.app` | Desktop 网络要求 | `domain_suffix: claude.app` |
| 26 | `a-api.anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 27 | `a-cdn.anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 28 | `a.claude.ai` | Desktop 网络要求 | `domain_suffix: claude.ai` |
| 29 | `anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 30 | `assets-proxy.anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 31 | `assets.claude.ai` | Desktop 网络要求 | `domain_suffix: claude.ai` |
| 32 | `claude.app` | Desktop 网络要求 | `domain_suffix: claude.app` |
| 33 | `s-cdn.anthropic.com` | Desktop 网络要求 | `domain_suffix: anthropic.com` |
| 34 | `cdnjs.cloudflare.com` | Artifacts 外部库 | `domain: cdnjs.cloudflare.com` |
| 35 | `cdn.jsdelivr.net` | Artifacts 外部库 | `domain: cdn.jsdelivr.net` |
| 36 | `cdn.tailwindcss.com` | Artifacts 外部库 | `domain: cdn.tailwindcss.com` |
| 37 | `code.jquery.com` | Artifacts 外部库 | `domain: code.jquery.com` |
| 38 | `unpkg.com` | Artifacts 外部库 | `domain: unpkg.com` |
| 39 | `fonts.googleapis.com` | 可选字体 | `domain: fonts.googleapis.com` |
| 40 | `fonts.gstatic.com` | 可选字体 | `domain: fonts.gstatic.com` |
| 41 | `api-iam.intercom.io` | 客服页面实测依赖 | `domain_suffix: intercom.io` |
| 42 | `downloads.intercomcdn.com` | 客服页面实测依赖 | `domain_suffix: intercomcdn.com` |
| 43 | `static.intercomassets.com` | 客服页面实测依赖 | `domain: static.intercomassets.com` |
| 44 | `widget.intercom.io` | 客服页面实测依赖 | `domain_suffix: intercom.io` |

客服四项来自 [Claude Help Center](https://support.claude.com/en/) 的直接 HTML 依赖观测，没有重放完整登录态或 JavaScript 运行过程。旧记录的 `js.intercomcdn.com` 本次没有直接出现在 HTML 中，不能据此判定停用；现有后缀仍覆盖。完整来源与差集见 [Claude 专项核对](evidence/network-audit-2026-10-20/claude/README.md)。

<a id="ip"></a>
## IP 方向与范围

| 用途 | 当前值 | 仓库处理 |
|---|---|---|
| Anthropic API IPv4 目的 | `160.79.104.0/23` | 被现有目的 `160.79.104.0/21` 包含 |
| Anthropic API IPv6 目的 | `2607:6bc0::/48` | 被现有目的 `2607:6bc0::/32` 包含 |
| Anthropic 服务出站源地址 | `160.79.104.0/21` | 独立 `anthropic-ip.srs` 的 `source_ip_cidr` 相同 |
| AS399358 另一个已知公告段 | `2607:6bc0:11::/48` | 被目的 `2607:6bc0::/32` 包含 |

[Anthropic 官方 IP 文档](https://platform.claude.com/docs/en/api/ip-addresses)当前响应 SHA 与仓库 9 月 27 日记录完全一致。[RIPE AS399358](https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS399358)本次视图的最新数据时间为 **2026-10-20 08:00 UTC**，可见的三个公告段是 `160.79.104.0/23`、`2607:6bc0::/48`、`2607:6bc0:11::/48`，与 10 月 15 日记录相同。公告归属本身不能证明每个地址的具体产品用途。

官方已淘汰的五个 IPv4 地址仍不在当前规则中：`34.162.46.92`、`34.162.102.82`、`34.162.136.91`、`34.162.142.92`、`34.162.183.95`。

以下资料也已查看，但属于不同方向或未选功能，不作为客户端规则漏项：

| 项目 | 本次事实 | 边界 |
|---|---|---|
| OpenAI Realtime SIP 媒体 | `13.79.45.80/28`、`23.98.140.64/28`、`40.67.149.176/28`、`40.83.204.240/28`，四段未变 | 仓库未启用的独立 SIP 功能；不与 ChatGPT Voice 混合 |
| OpenAI integrations 出站源地址 | 当前 feed 283 个前缀，创建时间 2026-10-06 | 服务端访问客户服务的来源；仓库无历史 feed 基线，不能称本次新增 |
| Codex cloud 出站源地址 | 当前 feed 1,758 个前缀，创建时间 2026-10-16 | 同上，不是用户访问 ChatGPT 的目的 IP |
| Claude 爬虫源地址 | 当前 feed 38 个 IPv4 前缀，创建时间 2026-10-07 | 网站识别爬虫流量所用；没有纳入客户端目的或 API 来源制品 |

方向依据：[OpenAI IP egress](https://developers.openai.com/api/docs/guides/ip-addresses)、[Realtime SIP](https://developers.openai.com/api/docs/guides/voice-sip?voice-api=realtime)、[Claude 爬虫数据](https://claude.com/crawling/bots.json)。这些 feed 自报创建时间不是“本次发现新增地址”的证据。AWS、Bedrock、其他云平台、企业 SSO 和任意 MCP / 插件依赖按实际功能另行定义，没有并入整段共享云地址。

<a id="evidence"></a>
## 验证、GitHub 版本与证据

重新下载了当前 v0.1.6 的三份 SRS，均 HTTP 200，字节、SHA-256 与本地制品及 GitHub digest 一致。原生解编译后，经单值/数组与 CIDR 表示规范化，语义与归档 JSON 一致。使用固定 sing-box `1.15.0-alpha.9` 对实际下载的 SRS 执行 **164 项原生匹配见证**，全部符合预期：

| 组别 | 数量 | 结果 |
|---|---:|---|
| OpenAI 官方主清单、WebSocket、Voice 及边界/待核项 | 67 | 全部符合预期 |
| Codex 本次核对的主机 | 8 | 全部命中 |
| Claude 文档、历史删除项、公告段端点及旧 IP 负例 | 56 | 全部符合预期 |
| GitHub 上游当前 OpenAI / Anthropic 规则见证 | 33 | 仅已知 `openai.org` 预期未覆盖，其余命中 |

这是静态匹配与下载核验；来源 CIDR 另按解编译结果验证方向和完整包含关系。没有进行真实登录、所有地区/账号功能抓包或目标设备配置测试，不把集合覆盖等同于业务一定成功。

四个上游是 v2fly、SagerNet、MetaCubeX、Loyalsoldier；后面三个是同源派生，四源一致不等于四份独立官方背书。v2fly 的 OpenAI 文件最后域名变更为 10 月 17 日的 `openai.org`，Anthropic 为 10 月 2 日的 `claude.dev`；SagerNet / MetaCubeX 的 10 月 20 日构建没有带来更多域名。Loyalsoldier 最新实际 dat 已下载并验证校验和后解码。四组产品文件都不包含 IP 规则。完整固定 SHA、URL、时间与 PR 搜索记录见 [GitHub 专项核查](evidence/network-audit-2026-10-20/github/summary.md)。

- [机器可读汇总](evidence/network-audit-2026-10-20/audit-results.json) · [Latest 身份](evidence/network-audit-2026-10-20/baseline.json) · [发布资产实际下载与解编译](evidence/network-audit-2026-10-20/released-assets-verification.json)
- [OpenAI 专项报告](evidence/network-audit-2026-10-20/openai/summary.md) · [Claude 专项报告](evidence/network-audit-2026-10-20/claude/README.md) · [GitHub 专项报告](evidence/network-audit-2026-10-20/github/summary.md)
- [OpenAI 原生命中](evidence/network-audit-2026-10-20/openai-native-matches.json) · [Codex 原生命中](evidence/network-audit-2026-10-20/codex-native-matches.json) · [Claude 原生命中](evidence/network-audit-2026-10-20/claude-native-matches.json) · [GitHub 原生命中](evidence/network-audit-2026-10-20/github-native-matches.json)
- [上一轮 v0.1.6 发布报告与 OpenAI 完整规则](evidence/release-v0.1.6/README.md) · [当前 Claude 完整规则](../artifacts/v0.1.6/anthropic.json) · [当前 Anthropic 来源规则](../artifacts/v0.1.6/anthropic-ip.json)

建议保持 v0.1.6。后续只有在确认新的功能依赖或地址集合变化后，才需要修改规则并发布新批次。
