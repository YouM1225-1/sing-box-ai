# v0.1.7 发布记录

用户于 2026-10-21 在候选验收及用途说明后明确要求“发布”。两次正式构建、发布门槛和完整回归已通过，当前准备 GitHub 上传与下载验证；完成后的地址与结果会在本页更新。

唯一规则增量是 Anthropic 的五个 `domain_suffix`：

| 后缀 | 范围和来源 |
|---|---|
| `growthbook.io` | 根域及全部子域，用户指定覆盖 |
| `hcaptcha.com` | 根域及全部子域，用户指定覆盖 |
| `stripe.network` | 根域及全部子域，用户指定覆盖 |
| `stripecdn.com` | 根域及全部子域，用户指定覆盖 |
| `segment.io` | 根域及全部子域，用户指定覆盖 |

原规则全部保留；OpenAI、Anthropic 来源 IP 两份 SRS 与 v0.1.6 字节一致；IP、关键词和消费者 IPv6 动作不变。来源身份为 `user-requested`，不宣称这些共享后缀都是 Claude 官方必需依赖。具体授权范围见[本次覆盖指令](../../../sources/evidence/one-exit-coverage-request-2026-10-21.json)。

已验收候选为 [v0.1.7-rc.1 manifest](../../../artifacts/v0.1.7-rc.1/manifest.json)。已提交输入经两次独立 release 构建，每次 2,720 项原生检查与 `--for-release` 门槛通过；同输入 candidate fixture 的 66 项回归全部通过。两次正式 manifest 字节相同，三份 SRS 与三份 JSON 均与已验收候选字节一致。

正式规则：[Anthropic JSON](../../../artifacts/v0.1.7/anthropic.json) · [OpenAI JSON](../../../artifacts/v0.1.7/openai.json) · [独立来源 IP JSON](../../../artifacts/v0.1.7/anthropic-ip.json)。Anthropic 为 15 个精确域名、21 个后缀、3 个关键词和 2 个目的 CIDR；OpenAI 为 25 个精确域名、16 个后缀、1 个正则和 23 个 Voice 目的 `/32`；独立来源集合只有 `160.79.104.0/21`。

| 正式 SRS | 字节数 | SHA-256 |
|---|---:|---|
| `anthropic.srs` | 529 | `38aeb4b09903bb238df6f33b476a247830719d7246950edc024660dd6e112ab4` |
| `openai.srs` | 800 | `196619631ab33a362794ef826b9bd5b8779d08c315f46a335443f3321d4dd48c` |
| `anthropic-ip.srs` | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |

构建证据：[构建汇总](build-results.json) · [第一次正式验证](release-validate.log) · [第二次正式验证](release-rebuild-validate.log) · [66 项回归](unit-tests.log) · [差异清单](semantic-diff.json) · [独立审阅](independent-review.json) · [正式 manifest](../../../artifacts/v0.1.7/manifest.json)。

静态制品发布不等于用户设备已刷新或真实业务验收。不会访问或修改用户设备，manifest 的消费者证据保持为空、部署状态为 pending。
