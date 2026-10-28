# v0.1.8 发布记录

已发布 [v0.1.8](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.8) 并设为 [Latest](https://github.com/YouM1225-1/sing-box-ai/releases/latest)。发布时间：北京时间 **2026-10-28 12:45:09**。原有 Latest 订阅地址继续可用；消费者成功刷新后取得本版，本次未确认用户设备已刷新。

## 变更与批准范围

唯一规则增量为 OpenAI 的 `domain_suffix: poteto.com`，覆盖根域及全部子域；`notpoteto.com` 和 `poteto.com.invalid` 不匹配。原规则全部保留，两份 Anthropic SRS 与 v0.1.7 字节一致。见[语义差异](semantic-diff.json)、[OpenAI JSON](../../../artifacts/v0.1.8/openai.json)及[用户域名指令](../../../sources/evidence/poteto-coverage-request-2026-10-28.json)。

用户授权“发布”，并明确批准“批准本次例外，保留旧日期和证据”。Claude `challenges.cloudflare.com` 的 `last_verified=2026-09-27`、`review_after=2026-10-27` 和原证据原样保留。此次是对 v0.1.8 的静态发布例外，不是 Challenge 重新通过验证。例外限定授权日、版本、原始条目、来源摘要及两份原始 SRS 摘要；错误日期、版本、来源变化、制品变化和运行验证声明均有拒绝测试。

[发布授权](../../../sources/evidence/release-v0.1.8-authorization.json) · [例外原文及约束](../../../sources/evidence/release-v0.1.8-unchanged-exception.json) · [语义审阅](../../../sources/evidence/release-v0.1.8-review.json)。

## 验证结果

| 检查 | 结果 |
|---|---|
| 两次正式构建 | 各 2,734 项原生检查与 `--for-release` 门禁通过 |
| 完整回归 | 73 项全部通过，无跳过 |
| 重建一致性 | 两次正式 manifest 相同；3 SRS、3 JSON 与候选一致 |
| 固定与 Latest 下载 | 各 6 个资产，合计 12 次，HTTP 200 且字节/摘要一致 |
| 固定与 Latest 空缓存加载 | 各 196 项请求检查，共 392 项；三份 SRS 均被原生内核下载并缓存 |
| 探测清理 | 两个进程均退出 0，4 个回环监听全部关闭 |
| 历史保留 | 9 个既有 Release 和 12 个旧标签引用保持不变 |

原生消费者测试在回环 SOCKS 入口匹配后拒绝业务目的请求，不代表真实登录、验证码、实际出口或生产设备验收。manifest 继续为 `validated_consumers=[]`、`integration_evidence=[]`、`deployment_status=pending`。

[构建汇总](build-results.json) · [正式 manifest](../../../artifacts/v0.1.8/manifest.json) · [73 项回归](unit-tests-final.log) · [固定下载](fixed-downloads.json) · [Latest 下载](latest-downloads.json) · [固定原生结果](remote-fixed/results.json) · [Latest 原生结果](remote-latest/results.json) · [探测脚本](remote-probe.py) · [历史核对](historical-releases-verification.json)。

## 下载入口与完整资产

- [OpenAI Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs) · [固定 v0.1.8 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.8/openai.srs)
- [Anthropic Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs)
- [Anthropic 来源 IP Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic-ip.srs)
- [正式 manifest](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.8/manifest.json)
- [SHA256SUMS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.8/SHA256SUMS)
- [包含源码、来源与许可证的 ZIP](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.8/sing-box-ai-v0.1.8.zip)

| SRS | 字节数 | SHA-256 |
|---|---:|---|
| `openai.srs` | 802 | `5068d4d1a9c4550b803a887f03e7e91e647299007d02840fa8a4c38f5aa39c55` |
| `anthropic.srs` | 529 | `38aeb4b09903bb238df6f33b476a247830719d7246950edc024660dd6e112ab4` |
| `anthropic-ip.srs` | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |

六个资产的完整摘要见[资产清单](local-assets.json)。

## 发布身份

Release ID：`426270523`。输入提交：`b041dc5ad626967c5e115710bf8aee6fb96cd272`。标签提交：`e8b43a0397f8e6a5df835ab7068693822cfd7c65`。Release 正文按现有约定留空。源码 ZIP 固定在标签提交，因此其中的发布文档保留上传前状态；最终回执另行提交 main，不移动版本标签。

[发布汇总](publication-results.json) · [Latest API 回执](release-final-status.json) · [上传回执](release-asset-upload-receipts.json)。初次过期门禁拦截的[记录](preflight.json)保留历史身份，不改写成验证通过。
