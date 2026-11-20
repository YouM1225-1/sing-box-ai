# Datadog NTP 与 loc sens 规则覆盖核对

核对日期：2026-11-10。范围：当前仓库 v0.1.10 的 `dist/anthropic.srs`、`dist/openai.srs` 和 `dist/anthropic-ip.srs`，与本次抓取的 [loc-sens-clash 清单](https://gist.githubusercontent.com/janlay/bec3cade3361678d975a8394d54515c6/raw/loc-sens-clash.txt) 对比。

**`*.datadog.pool.ntp.org` 已覆盖；整份清单未全部覆盖。** 清单原有 48 行规则，`DOMAIN-SUFFIX,stripe.com` 重复一次，去重后为 47 条：完整覆盖 15 条、部分覆盖 2 条、未覆盖 30 条。覆盖统计取三个规则集的并集，不意味着只加载其中一个就有相同结果。

## Datadog NTP

`anthropic.srs` 中的 `domain_keyword: datadog` 会匹配所有包含 `datadog` 的域名，因此覆盖 `datadog.pool.ntp.org` 及其全部子域名。原始 Gist 本身也明确列出 `DOMAIN-SUFFIX, datadog.pool.ntp.org`。

已通过 sing-box 实际匹配验证以下域名均命中 `anthropic`：

- `datadog.pool.ntp.org`
- `0.datadog.pool.ntp.org`
- `1.datadog.pool.ntp.org`
- `a.b.datadog.pool.ntp.org`

这几个域名不命中 `openai` 或 `anthropic-ip`。普通的 `pool.ntp.org`、`0.pool.ntp.org`、`time.google.com`、`time.apple.com`、`time.cloudflare.com` 在三个规则集中均未命中。现有规则并没有排除所有 NTP 域名；`datadog` 关键词会覆盖上述特殊 NTP 子域名。

## 完整覆盖的 15 条

| 原始类型 | 内容 | 覆盖规则集及依据 |
| --- | --- | --- |
| `DOMAIN` | `api.segment.io` | `anthropic`：`domain_suffix: segment.io` |
| `DOMAIN` | `fcmtoken.googleapis.com` | `anthropic`：`domain: fcmtoken.googleapis.com` |
| `DOMAIN-SUFFIX` | `datadog.pool.ntp.org` | `anthropic`：`domain_keyword: datadog` |
| `DOMAIN-SUFFIX` | `hcaptcha.com` | `anthropic`：`domain_suffix: hcaptcha.com` |
| `DOMAIN` | `cdn.oaiusercontent.com` | `openai`：`domain_suffix: oaiusercontent.com` |
| `DOMAIN` | `browser-intake-us5-datadoghq.com` | `anthropic`：`domain_keyword: datadog` |
| `DOMAIN-SUFFIX` | `anthropic.com` | `anthropic`：`domain_suffix: anthropic.com` |
| `DOMAIN-SUFFIX` | `chat.com` | `openai`：`domain_suffix: chat.com` |
| `DOMAIN-SUFFIX` | `chatgpt.com` | `openai`：`domain_suffix: chatgpt.com` |
| `DOMAIN-SUFFIX` | `claude.ai` | `anthropic`：`domain_suffix: claude.ai` |
| `DOMAIN-SUFFIX` | `ingest.us.sentry.io` | `anthropic`：`domain_keyword: sentry` |
| `DOMAIN-SUFFIX` | `intercom.io` | `anthropic`：`domain_suffix: intercom.io` |
| `DOMAIN-SUFFIX` | `oaistatic.com` | `openai`：`domain_suffix: oaistatic.com` |
| `DOMAIN-SUFFIX` | `siftscience.com` | `anthropic`：`domain_keyword: sift` |
| `DOMAIN-SUFFIX` | `stripe.network` | `anthropic`：`domain_suffix: stripe.network` |

## 部分覆盖的 2 条

| 原始规则 | 当前覆盖范围 | 未等价覆盖的范围 |
| --- | --- | --- |
| `DOMAIN-SUFFIX,stripe.com` | `anthropic` 精确匹配 `r.stripe.com`；`openai` 精确匹配 `js.stripe.com` | 不覆盖整个 `stripe.com` 后缀，例如根域及 `probe.stripe.com` 均未命中。`stripe.network` 和 `stripecdn.com` 是另外的域名。 |
| `DOMAIN-KEYWORD,openai` | `openai` 包含 `openai.com` 后缀及若干名称含 `openai` 的精确域名 | 没有通用 `openai` 关键词规则，例如 `openai.example.org`、`beforeopenaiafter.example.org` 均未命中。 |

## 未覆盖的 30 条

以下原始规则在当前三个规则集中没有对应的域名或进程匹配覆盖。

| 原始类型 | 内容 |
| --- | --- |
| `DOMAIN` | `ai.google.dev` |
| `DOMAIN` | `aistudio.google.com` |
| `DOMAIN` | `alkalicore-pa.clients6.google.com` |
| `DOMAIN` | `bard.google.com` |
| `DOMAIN` | `gemini.google.com` |
| `DOMAIN` | `generativelanguage.googleapis.com` |
| `DOMAIN` | `proactivebackend-pa.googleapis.com` |
| `DOMAIN` | `phonedeviceverification-pa.googleapis.com` |
| `DOMAIN` | `api.revenuecat.com` |
| `DOMAIN-SUFFIX` | `notebooklm.google` |
| `DOMAIN-SUFFIX` | `deepmind.google` |
| `DOMAIN-SUFFIX` | `geller-pa.googleapis.com` |
| `DOMAIN-SUFFIX` | `generativeai.google` |
| `DOMAIN-SUFFIX` | `makersuite.google.com` |
| `DOMAIN-SUFFIX` | `notebooklm.google.com` |
| `DOMAIN` | `www2.deepl.com` |
| `DOMAIN` | `probe.icloud.com` |
| `DOMAIN` | `mask-api.icloud.com` |
| `DOMAIN` | `apple-relay.apple.com` |
| `DOMAIN` | `configuration.ls.apple.com` |
| `DOMAIN` | `starling.zijieapi.com` |
| `DOMAIN` | `prodregistryv2.org` |
| `DOMAIN` | `integrate.api.nvidia.com` |
| `DOMAIN-SUFFIX` | `ai.com` |
| `DOMAIN-SUFFIX` | `bing.com` |
| `DOMAIN-SUFFIX` | `cursor.sh` |
| `DOMAIN-KEYWORD` | `siri` |
| `PROCESS-NAME` | `Claude` |
| `PROCESS-NAME` | `ChatGPT` |
| `PROCESS-NAME` | `Antigravity` |

`PROCESS-NAME,Claude`、`PROCESS-NAME,ChatGPT` 和 `PROCESS-NAME,Antigravity` 未覆盖，是指没有按进程名匹配全部流量的规则；这些程序访问已覆盖域名时仍可能命中域名规则。

## 验证范围与证据

- 当前三个 `dist/*.srs` 均与 v0.1.10 对应发布文件逐字节一致。
- 反编译后，对单值与数组、重复值、单 IP 与 `/32` 表示作规范化，规则内容与发布 JSON 一致。
- 使用仓库现有 `tests/harness/main.go`，以 sing-box v1.15.0-alpha.9 实际加载当前 SRS：435 个域名匹配检查全部通过，包含原始精确域名、后缀根域和多级子域、边界域名、关键词例子以及 NTP 正反例。
- 完整后缀或关键词覆盖结论由规则语义确定，有限样例用于交叉验证；进程名缺失通过检查反编译规则确认。
- 这里比较的是规则语义覆盖，不是客户端实时出口。未命中域名规则的请求仍可能命中客户端其他规则或解析后的 IP 规则；最终出口取决于客户端加载版本、规则顺序和出站配置。本次未修改或发布规则。

本次原始清单、逐项结果和反编译快照均已保存：

- [原始清单快照](evidence/loc-sens-coverage-2026-11-10/loc-sens-clash.txt)
- [完整逐项匹配及文件校验值](evidence/loc-sens-coverage-2026-11-10/comparison.json)
- [Anthropic 反编译规则](evidence/loc-sens-coverage-2026-11-10/anthropic.json)
- [OpenAI 反编译规则](evidence/loc-sens-coverage-2026-11-10/openai.json)
- [Anthropic IP 反编译规则](evidence/loc-sens-coverage-2026-11-10/anthropic-ip.json)
- [匹配程序汇总](evidence/loc-sens-coverage-2026-11-10/harness-summary.txt)
- [435 项实际匹配结果](evidence/loc-sens-coverage-2026-11-10/harness-results.jsonl)
- [复核脚本](evidence/loc-sens-coverage-2026-11-10/compare.py)
