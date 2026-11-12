# v0.1.13 Claude 六条范围补全与发布记录

日期：2026-11-12（Asia/Shanghai）。本批按用户“完整补全 提交 push 发布”的指令，将上一轮讨论的 6 条部分覆盖表达式全部补齐。**v0.1.13 已提交、推送到 main、正式发布并设为 Latest；全部下载和本机空缓存检查通过。**

## 完整补全范围

| 类型 | 本次新增值 | 新增覆盖 |
| --- | --- | --- |
| `domain_keyword` | `anthropic` | 域名任意位置包含该词 |
| `domain_keyword` | `claude` | 域名任意位置包含该词 |
| `domain_keyword` | `browser-intake` | 不再限于已知 Datadog 主机 |
| `domain_suffix` | `stripe.com` | 根域和全部子域，包括 `hooks.stripe.com`、`js.stripe.com` 子域 |
| `domain_suffix` | `usefathom.com` | 根域和全部子域 |
| `domain_suffix` | `challenges.cloudflare.com` | 根主机和全部子域 |

范围来自 [one-exit 固定提交](https://github.com/wquguru/one-exit/commit/b9d9f8ab6687401f7588dfa7d7023cd58ffb4032)中先前未被完整包含的 6 条域名表达式。它们全部登记为 `user-requested` 共享范围，不标为官方必需或已验证的业务依赖。

这次采用完整范围，不仅限于先前建议的两个 Stripe 子范围。它也会匹配其他应用的 Stripe/Fathom/Challenge 请求，以及任意包含这三个关键词的域名；`notclaude.ai` 这样的边界样例现在也会命中，这是关键词规则的预期结果。

本批只扩大这 6 条表达式，不加入 Google 全域、`modelcontextprotocol` 关键词、进程/ASN 条件或 IPv6 拒绝动作。目的与来源 IP 的方向和范围保持原样。既有关键词仍可能命中含同名词的 NTP 域名；登记中的 `excluded: ntp` 只表示没有新增专门的 NTP 条目，不是关键词匹配中的排除条件。

## 生成结果与旧规则保留

| 制品 | 本批结果 |
| --- | --- |
| `anthropic.srs` | 15 个精确域名、13 个后缀、6 个关键词、4 个目的 CIDR |
| `openai.srs` | 与 v0.1.12 逐字节相同，保留 423 个 Voice /32 |
| `anthropic-ip.srs` | 与 v0.1.12 逐字节相同，仅含 2 条 `source_ip_cidr` |

生成器消除了被宽规则完全包含的重复表达式：8 个精确主机和 12 个旧后缀不再单独出现在最终 JSON，但其覆盖仍在。原始 YAML 条目、官方事实、历史复核日期和 provenance 全部保留。两项过期兼容记录通过绑定本次版本、六项增量与制品摘要的限定记录沿用，不宣称重新完成运行验证。

### 新版完整目的规则

**精确主机，15 项：**

```text
api.revenuecat.com
cdn.jsdelivr.net
cdn.tailwindcss.com
cdnjs.cloudflare.com
code.jquery.com
fcmtoken.googleapis.com
fonts.googleapis.com
fonts.gstatic.com
formulae.brew.sh
github.com
raw.githubusercontent.com
registry.npmjs.org
static.intercomassets.com
storage.googleapis.com
unpkg.com
```

**后缀，13 项，均覆盖根域和子域：**

```text
challenges.cloudflare.com
clau.de
growthbook.io
hcaptcha.com
intercom.io
intercomcdn.com
segment.io
statsigapi.net
stripe.com
stripe.network
stripecdn.com
usefathom.com
withpersona.com
```

**关键词，6 项：**

```text
anthropic
browser-intake
claude
datadog
sentry
sift
```

**目的 CIDR，4 项：**

```text
153.61.224.0/22
160.79.104.0/21
2607:6bc0::/32
34.8.0.0/16
```

独立来源集合仍为 `160.79.104.0/21` 和 `153.61.208.0/20`，使用 `source_ip_cidr`，不并入客户端目的路由。

## 验证与发布范围

源码提交：`4efabd1d38635c32bc433e201b912f77240326ce`。

版本标签提交：`09f79c47b91630b2e54539b5584fcf710b91d0b3`。

GitHub 公开时间：`2026-11-12T10:40:49Z`（UTC）。最终远端回执另行提交至 main；标签和源码 ZIP 固定在制品归档时点。

| 检查 | 结果 |
| --- | --- |
| 完整回归 | 92 项通过，零失败、零跳过 |
| 两次正式构建 | 各 6,156 项原生检查通过，9 个输出文件逐字节一致 |
| 已提交源码的候选复建 | 6,156 项通过；JSON/SRS 与正式批次及回归 fixture 相同 |
| 提交、授权、摘要及日期门槛 | 通过；候选保留未批准身份 |
| 固定版本下载 | 6 个附件全部 HTTP 200，字节数及 SHA-256 一致 |
| Latest 下载 | 6 个附件全部 HTTP 200，字节数及 SHA-256 一致 |
| 固定版本 / Latest 空缓存加载 | 各 732 项请求通过：716 项目的地址/域名匹配请求 + 16 项来源方向检查 |
| 清理 | 两次进程均退出 0，4 个回环监听全部关闭 |
| 历史版本保护 | 14 个旧 Release 与 17 个旧标签引用保持不变 |

已按草稿上传、非 Latest 发布、固定下载及本机空缓存加载、切换 Latest、Latest 下载及空缓存加载的顺序完成验收。三份 SRS 均由原生内核通过远端地址实际下载，空缓存记录包含完整预期字节。旧 Release 比较覆盖发布记录及资产元数据，仅忽略会随下载增长的 `download_count`。

首轮候选检查发现历史测试将已获准扩大范围的 42 个 JSON/SRS 样例固定判为不命中。修正了对应预期并新增新旧范围对照；没有取消边界检查或修改 SRS 匹配引擎。另将 v0.1.12 的历史 IP 增量测试固定到该版 Anthropic 快照，避免后续域名扩展改变历史测试对象。

空缓存探测使用回环 SOCKS 并拒绝全部测试业务连接，只验证远端 SRS 的实际加载、摘要和首个命中规则。它不代表真实 Claude 登录、支付、身份验证、代理出口或设备配置已验收。没有访问或修改 N100、iPhone、UniFi 或系统 DNS/路由设置。

本次在干净检出中完成构建与发布；原工作区尚未提交的 UniFi 生成器、导出和说明保持原样，不混入本批提交或 Release。

## 证据与下载

- [六项增量及规范化差异](semantic-diff.json)
- [发布授权](../../../sources/evidence/release-v0.1.13-authorization.json)
- [保留条目限定记录](../../../sources/evidence/release-v0.1.13-preserved-entry-exception.json)
- [完整用户范围记录](../../../sources/evidence/claude-six-scopes-coverage-request-2026-11-12.json)
- [预编译摘要](preflight-summary.json)
- [92 项回归结果](unit-test-results.json)与[完整日志](unit-tests.log)
- [正式构建与复现结果](build-results.json)
- [正式批次 manifest](../../../artifacts/v0.1.13/manifest.json)
- [发布汇总](publication-results.json)
- [固定版本附件下载核验](fixed-downloads.json)
- [Latest 附件下载核验](latest-downloads.json)
- [固定版本 732 项空缓存检查](remote-fixed/results.json)
- [Latest 732 项空缓存检查](remote-latest/results.json)
- [历史版本保护核验](historical-verification.json)
- [6 个附件摘要](package-assets.json)

## 发布和下载入口

正式版本：[v0.1.13](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.13)。

常用订阅地址保持不变：[Anthropic Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs)、[OpenAI Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs)。实际设备是否已刷新缓存尚未验证。

| 固定版本附件 | 字节数 | SHA-256 |
| --- | ---: | --- |
| [SHA256SUMS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/SHA256SUMS) | 410 | `652be3a42fc059073ae050f6c93b94dbe6fc09daf51b9d928a10e09665a6ca23` |
| [anthropic-ip.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/anthropic-ip.srs) | 47 | `819dcba59e171957aff80c4ddf6c0dd9fd984620e2ee0a7f363deb879828261a` |
| [anthropic.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/anthropic.srs) | 459 | `090329f326922e3d4c1a88f219d71666401c0abc33c098e9c9b233edbc1281c1` |
| [manifest.json](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/manifest.json) | 347066 | `d464dfb9ff833f91dafb04a504d28a39eace085a72a93c61ab0bc36543df7c1d` |
| [openai.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/openai.srs) | 2195 | `926a8e1385b8007855f29413a2bba265e49aa796e5124e6cb3ea80aa964ecb5e` |
| [sing-box-ai-v0.1.13.zip](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/sing-box-ai-v0.1.13.zip) | 3257059 | `62b8007444a0142615bdf9d54f414aa50f8de0117af4a8781a0365ea224a6ae2` |
