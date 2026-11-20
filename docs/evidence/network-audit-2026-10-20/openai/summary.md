# OpenAI 官方网络资料复核（2026-10-20）

相对已发布 v0.1.6，本次没有发现应补入当前 ChatGPT/Codex 客户端规则的新增官方域名或 Voice IP。官方网络主清单 31 项、2 个 WebSocket 主机均被规则语义覆盖；23 个 Voice /32 与既有归档字节一致。

本目录只保存本次审计证据；未修改 sources、artifacts 或 dist。完整事实及覆盖标记见 [official-facts.json](official-facts.json)，真实抓取时间、响应哈希和 URL 见 [fetch-manifest.json](fetch-manifest.json)。正文完整响应仅保存在临时审阅缓存；此处保留功能性端点事实。

## 官方主清单完整列表

来源：[OpenAI 网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)。页面原文更新时间为 `23 hours ago`；不将相对时间推算为域名上线日期。与 2026-10-19 来源记录对比：新增 0，移除 0。

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

WebSocket：`wss://ws.chatgpt.com`、`wss://chatgpt.com/`，TCP 443；两者均覆盖。`register.appattest.apple.com` 仍仅出现在 iOS 诊断步骤，不在 31 项主清单。

## ChatGPT Voice 完整 IP 列表

来源：[官方 Voice JSON](https://openai.com/chatgpt-voice.json)，本次原始响应见 [voice.json](voice.json)。`creationTime` 为 `2026-03-26T20:12:45.451356+00:00`，本次下载成功，895 字节，SHA-256 `8f03f3c594165eeff009915c7e2beb4bdfb9d429fb1955c205e3b33ec781899a`。23 个 IPv4 /32，无 IPv6；相对既有归档和 v0.1.6 新增 0、移除 0、缺漏 0。

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

推荐 UDP 3478、可回退 TCP 443；本次未执行语音会话。

## Codex 网络与安装

[官方 CLI 文档](https://learn.chatgpt.com/docs/codex/cli)的安装入口实际重定向到 `releases.openai.com`。当前公开安装脚本哈希与仓库旧来源记录完全一致；官方发布频道、GitHub Release、npm 最新稳定版均指向 `0.163.0`。只读取脚本和元数据，并用 HEAD 检查一个 GitHub 发行资产重定向；未执行安装脚本。

以下本次确认的目的主机全部已覆盖：

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

`codex-cloud-environments.chatgpt.com` 来自 [self-hosted executor 网络要求](https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted)，通过现有 `chatgpt.com` 后缀覆盖。当前资料确认主机用途，但没有足够历史资料将该主机称为最近新增。

## 另两份官方 IP feed：服务端出站源地址

[官方 IP egress 文档](https://developers.openai.com/api/docs/guides/ip-addresses)区分以下用途；这些地址用于客户服务识别来自 OpenAI 的请求，并非 ChatGPT 客户端的目的地址。

| Feed | 数量 | creationTime | 本地完整原始数据 |
| --- | ---: | --- | --- |
| ChatGPT integrations: plugins, connectors, GPT Actions and agentic commerce | 283（全为 IPv4） | `2026-10-06T23:18:01.923622` | [connectors.json](connectors.json) |
| Codex cloud connections to external services such as GitHub | 1758（全为 IPv4） | `2026-10-16T17:33:26.060036` | [agents.json](agents.json) |


仓库 upstream registry 未追踪这两份 feed 的历史基线，因此不声称本次新增、移除或遗漏；本次仅建立审计观察记录。

## Realtime SIP：范围外复核

[当前官方 SIP 文档](https://developers.openai.com/api/docs/guides/voice-sip?voice-api=realtime)仍列出以下 4 段，与此前列出的集合完全一致：

```text
13.79.45.80/28
23.98.140.64/28
40.67.149.176/28
40.83.204.240/28
```

用于双向 UDP SRTP 媒体，端口由 SDP 协商；`sip.api.openai.com`、`sip-eu.api.openai.com` 的信令要求为 TCP/TLS 5061，域名已有后缀覆盖。4 段媒体 IP 当前未纳入 v0.1.6，这是未选择的 Realtime API SIP 功能范围，不应混入 ChatGPT Voice 的 23 个 /32。

## 验证边界

本文件的覆盖结论来自 v0.1.6 JSON 规则语义与官方原始 feed 的完整集合比较；主审计另行记录重新下载的发布 SRS 原生命中见证。本次未证明实际设备 DNS/路由优先级、身份验证、语音质量或任意插件/包管理器的全部第三方依赖。

本轮 graft 节省约 23,631 tokens（1 次查询）。
