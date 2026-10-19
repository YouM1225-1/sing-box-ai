# v0.1.6 发布结果与完整 OpenAI 清单

**已发布 [v0.1.6](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.6)，并设为 [Latest](https://github.com/YouM1225-1/sing-box-ai/releases/latest)。** 发布时间：2026-10-19 13:57:26（北京时间）。原 Latest 订阅地址继续有效，客户端成功刷新规则后可取得新版。

本次补入精确域名 `frontend-apps-multi-region.workos.com`，**2026-10-19 核对的 OpenAI 官方网络主清单现已覆盖 31/31 项**，WebSocket 目标覆盖 2/2。新出现于官方证据中的 `cdn.platform.openai.com` 已由 `openai.com` 后缀覆盖，无需重复规则。官方 Voice 的 23 个 IP 没有变化，Anthropic 两份 SRS 与 v0.1.5 字节一致。

GitHub 社区新增的 `openai.org` 已登记为未选中的待核候选；官方网络清单未列出该项，现有资料不足以确认产品依赖，因此本版未将其纳入规则。上述完整覆盖仅指本次核对的官方清单及仓库已选功能，不代表所有产品、插件、外部网站或真实设备业务均已验收。

导航：[下载与摘要](#downloads) · [官方 31 项清单](#official) · [当前完整规则](#rules) · [验证结果](#verification) · [来源与发布身份](#evidence)

<a id="downloads"></a>
## 下载与摘要

- [OpenAI Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs) · [固定 v0.1.6 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.6/openai.srs)
- [Claude Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [独立 Anthropic 来源 IP SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic-ip.srs)
- [正式 manifest](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.6/manifest.json) · [发布校验和](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.6/SHA256SUMS) · [含来源与许可证的 ZIP](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.6/sing-box-ai-v0.1.6.zip)

固定版本和 Latest 两组下载共 12 次均返回 HTTP 200，下载内容与本地资产逐字节一致。

| 资产 | 字节数 | SHA-256 |
|---|---:|---|
| `anthropic.srs` | 488 | `0d8e26718c663ffdb03d0d32a2cf42bf61be540787c46fa7684bf1a70a23c5f1` |
| `openai.srs` | 800 | `196619631ab33a362794ef826b9bd5b8779d08c315f46a335443f3321d4dd48c` |
| `anthropic-ip.srs` | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |
| `manifest.json` | 102,612 | `6c1a4d1a2c79ad966cb5481290932b243462453f57f35a3fc33d2e7eeb1865d7` |
| `sing-box-ai-v0.1.6.zip` | 1,907,832 | `a97547769effd8abeb9f1c6d123bd1f441d97e86dffee1bdb4497b29419f7876` |
| `SHA256SUMS` | 409 | `4a35e08d57211c579f603984ae58975399049a5527b794069fc6412c4fa263c5` |

<a id="official"></a>
## 官方主清单完整核对

以下逐项对应本次归档的[官方网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)。`*.x` 使用子域见证配合原生后缀边界验证；完整逐项结果见[来源覆盖回执](source-coverage.json)。

| # | 官方要求 | v0.1.6 覆盖方式 | 结果 |
|---|---|---|---|
| 1 | `*.auth.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 2 | `*.chatgpt.com` | 后缀 `chatgpt.com` | 已覆盖 |
| 3 | `*.ct.sendgrid.net` | 后缀 `.ct.sendgrid.net` | 已覆盖 |
| 4 | `*.intercom.io` | 后缀 `.intercom.io` | 已覆盖 |
| 5 | `*.intercomcdn.com` | 后缀 `.intercomcdn.com` | 已覆盖 |
| 6 | `*.oaistatic.com` | 后缀 `oaistatic.com` | 已覆盖 |
| 7 | `*.oaiusercontent.com` | 后缀 `oaiusercontent.com` | 已覆盖 |
| 8 | `*.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 9 | `*.oaistatsig.com` | 后缀 `oaistatsig.com` | 已覆盖 |
| 10 | `android.chat.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 11 | `auth0.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 12 | `cdn.openaimerge.com` | 精确域名 | 已覆盖 |
| 13 | `cdn.platform.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 14 | `cdn.workos.com` | 精确域名 | 已覆盖 |
| 15 | `challenges.cloudflare.com` | 精确域名 | 已覆盖 |
| 16 | `chat.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 17 | `desktop.chat.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 18 | `forwarder.workos.com` | 精确域名 | 已覆盖 |
| 19 | `frontend-apps-multi-region.workos.com` | 新增精确域名 | 已覆盖 |
| 20 | `humb.apple.com` | 精确域名 | 已覆盖 |
| 21 | `images.workoscdn.com` | 精确域名 | 已覆盖 |
| 22 | `ios.chat.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 23 | `js.intercomcdn.com` | 后缀 `.intercomcdn.com` | 已覆盖 |
| 24 | `js.stripe.com` | 精确域名 | 已覆盖 |
| 25 | `o207216.ingest.sentry.io` | 精确域名 | 已覆盖 |
| 26 | `o33249.ingest.sentry.io` | 精确域名 | 已覆盖 |
| 27 | `rum.browser-intake-datadoghq.com` | 精确域名 | 已覆盖 |
| 28 | `setup.auth.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 29 | `setup.workos.com` | 精确域名 | 已覆盖 |
| 30 | `tcr9i.chat.openai.com` | 后缀 `openai.com` | 已覆盖 |
| 31 | `workos.imgix.net` | 精确域名 | 已覆盖 |

正文另列的 WebSocket 目标 `ws.chatgpt.com` 和 `chatgpt.com` 均由 `chatgpt.com` 后缀覆盖。Voice [官方地址数据](https://openai.com/chatgpt-voice.json)重新取得成功，23 个 IPv4 `/32` 与发布规则完全一致，无新增或删除；数据内 `creationTime` 为 `2026-03-26T20:12:45.451356+00:00`。

<a id="rules"></a>
## 当前 OpenAI 完整规则

以下内容与 [v0.1.6 的 openai.json](../../../artifacts/v0.1.6/openai.json) 完全一致，含 **25 个精确域名、16 个后缀、1 个正则和 23 个目的 IP**。其中包含完整社区基线及已选 Codex 安装依赖；并非每项都来自官方网络主清单，逐项来源见 [manifest](../../../artifacts/v0.1.6/manifest.json)。

`domain` 仅匹配精确主机；无前导点的 `domain_suffix` 匹配裸域及各级子域，有前导点的仅匹配子域。新增 WorkOS 项不会扩大到整个 `workos.com` 或该主机的子域。

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

<a id="verification"></a>
## 验证结果

| 检查 | 结果 |
|---|---|
| 候选原生匹配 | 2,650 项通过，0 失败。 |
| 两次正式构建与发布门槛 | 每次 **2,650 项通过，0 失败**，均通过 `--for-release`。 |
| 完整回归 | **65 项通过，0 失败、0 跳过**；使用同一已提交输入生成的 candidate fixture。 |
| 可重复构建 | 两次正式构建的 3 SRS、3 JSON 和 manifest 字节一致；六份产品文件与已复核候选一致。 |
| 官方清单与范围见证 | **42 项通过**：31 项主清单、2 项 WebSocket、9 项精确范围及待核排除见证。 |
| 固定版本 / Latest 下载 | 各 **6 个资产**返回 200，与本地字节及 SHA-256 一致。 |
| 原生空缓存加载 | 三份公开远程 SRS 实际下载并进入缓存；**165 项请求检查通过**。 |
| 测试进程清理 | 进程退出 0，两个回环监听均关闭。 |
| 历史发行保留 | 既有 **7 个 Release** 的元数据、资产身份、大小和摘要保持不变。 |
| 独立复核 | 已通过，无未解决冲突；本版唯一产品规则增量为新 WorkOS 精确主机。 |

空缓存测试使用固定 sing-box `1.15.0-alpha.9` 与 v0.1.6 固定下载地址，包括 159 项主入口请求和 6 项来源方向请求。新 WorkOS 主机命中；相似域、错误后缀、子域及未选 `openai.org` 均按预期排除，原有 OpenAI/Claude 规则行为保留。业务目标在本机回环测试中拒绝，未向这些目标发起登录或业务连接。

本次完成 GitHub 静态发布及本机隔离验证。现网客户端是否已刷新未作确认；manifest 继续保持 `validated_consumers=[]`、`integration_evidence=[]`、`deployment_status=pending`。

<a id="evidence"></a>
## 来源、发布身份与证据

官方证据已刷新为本次完整英文正文，主清单相对旧来源快照由 29 项增加至 31 项；旧规则已覆盖其中 30 项，本次补齐最后一项。原始联网审计中的更新前结果保留为[历史对照](../../openai-domain-coverage-2026-10-19.md)。GitHub 差异及未选理由见 [v2fly #4149](https://github.com/v2fly/domain-list-community/pull/4149) 和[候选发现记录](../../../sources/discovery/openai-org-2026-10-19.json)。

发布时间：`2026-10-19T05:57:26Z`；发布者：`YouM1225-1`；Release ID：`416949195`。Release 正文按仓库约定留空，详情保存在本文。

输入提交：`d586a7a559ca1ea70186f04218b1ad8e703fd5ef`。版本标签提交：`39abd161bd5c05b769dbddf5fef916d4d7662ec4`。最终下载与发布回执另行提交到 main，不移动 `v0.1.6` 标签。源码 ZIP 固定于标签提交，其中报告保留上传前状态；独立候选审阅记录也保留当时状态，后续发布结果由本页及对应回执证明。

准备阶段两次验证失败日志保留在本目录：首次为 Go 路径调用错误，另一次为输入准备期间变动；已由提交输入后的成功正式验证和完整回归替代，没有将失败步骤计为通过。

- [发布汇总](publication-results.json) · [Latest API 回执](release-final-status.json) · [资产身份与摘要](local-assets.json)
- [固定下载核验](fixed-downloads.json) · [Latest 下载核验](latest-downloads.json) · [历史发行核验](historical-releases-verification.json)
- [原生空缓存结果](remote/results.json) · [运行日志](remote/runtime.log) · [探测脚本](remote-probe.py)
- [构建结果](build-results.json) · [正式门槛日志](release-validate.log) · [第二次构建门槛](release-rebuild-validate.log) · [完整回归日志](unit-tests.log)
- [官方覆盖与 Voice 核对](source-coverage.json) · [语义差异](semantic-diff.json) · [独立复核](independent-review.json)
- [正式 OpenAI JSON](../../../artifacts/v0.1.6/openai.json) · [正式 manifest](../../../artifacts/v0.1.6/manifest.json) · [批次校验和](../../../artifacts/v0.1.6/SHA256SUMS)
- [发布授权](../../../sources/evidence/release-v0.1.6-authorization.json) · [语义审批](../../../sources/evidence/release-v0.1.6-review.json)
