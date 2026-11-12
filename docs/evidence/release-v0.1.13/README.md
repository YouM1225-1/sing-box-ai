# v0.1.13 Claude 六条范围补全与发布记录

日期：2026-11-12（Asia/Shanghai）。本批按用户“完整补全 提交 push 发布”的指令，将上一轮讨论的 6 条部分覆盖表达式全部补齐。发布状态将在远端验收完成后更新。

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

正式发布前须完成候选原生匹配、全部回归、两次正式构建、提交绑定和发布门槛。随后按草稿上传、非 Latest 发布、固定下载及本机空缓存加载、切换 Latest、Latest 下载及空缓存加载的顺序验收。

首轮候选检查发现历史测试将已获准扩大范围的 42 个 JSON/SRS 样例固定判为不命中。修正了对应预期并新增新旧范围对照；没有取消边界检查或修改 SRS 匹配引擎。另将 v0.1.12 的历史 IP 增量测试固定到该版 Anthropic 快照，避免后续域名扩展改变历史测试对象。

空缓存探测使用回环 SOCKS 并拒绝全部测试业务连接，只验证远端 SRS 的实际加载、摘要和首个命中规则。它不代表真实 Claude 登录、支付、身份验证、代理出口或设备配置已验收。没有访问或修改 N100、iPhone、UniFi 或系统 DNS/路由设置。

本次在干净检出中准备发布；原工作区尚未提交的 UniFi 生成器、导出和说明保持原样，不混入本批提交或 Release。

## 证据与下载

- [六项增量及规范化差异](semantic-diff.json)
- [发布授权](../../../sources/evidence/release-v0.1.13-authorization.json)
- [保留条目限定记录](../../../sources/evidence/release-v0.1.13-preserved-entry-exception.json)
- [完整用户范围记录](../../../sources/evidence/claude-six-scopes-coverage-request-2026-11-12.json)
- [预编译摘要](preflight-summary.json)

GitHub 目标：[v0.1.13](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.13)。最终发布状态与可用性以完成后的验收回执为准。
