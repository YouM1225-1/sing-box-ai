# v0.1.7 发布记录

**已发布 [v0.1.7](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.7)，并设为 [Latest](https://github.com/YouM1225-1/sing-box-ai/releases/latest)。** 发布时间为北京时间 **2026-10-21 14:37:32**。现有 Latest 订阅地址可继续使用，消费者成功刷新后取得本版；本次未确认实际用户设备已刷新。

用户在候选验收及用途说明后明确要求“发布”。已完成输入提交、两次正式构建、发布门槛、完整回归、GitHub 上传、固定下载和 Latest 下载核验，以及两个入口的原生空缓存加载。既有 8 个 Release 和 11 个标签引用均保持不变。

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

## 下载入口

- [Claude / Anthropic Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic.srs) · [固定 v0.1.7 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.7/anthropic.srs)
- [OpenAI Latest SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/openai.srs) · [独立 Anthropic 来源 IP SRS](https://github.com/YouM1225-1/sing-box-ai/releases/latest/download/anthropic-ip.srs)
- [正式 manifest](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.7/manifest.json) · [校验和](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.7/SHA256SUMS) · [包含源码、来源与许可证的 ZIP](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.7/sing-box-ai-v0.1.7.zip)

固定版本和 Latest 两组各 6 个资产均实际下载，全部返回 HTTP 200，与本地资产字节及 SHA-256 一致。全部资产大小和摘要见[资产清单](local-assets.json)。

## 发布与下载验收

| 检查 | 结果 |
|---|---|
| 两次正式构建 | 每次 2,720 项原生检查通过，均通过 `--for-release` |
| 完整回归 | 同输入 candidate fixture 的 66 项通过，无跳过 |
| 重建一致性 | 两次正式 manifest 相同；3 SRS、3 JSON 与验收候选一致 |
| 固定 / Latest 公开下载 | 各 6 个资产，合计 12 次，均为 200 且字节一致 |
| 固定入口空缓存加载 | 190 项请求检查通过，三份远程 SRS 实际下载、缓存字节正确 |
| Latest 入口空缓存加载 | 独立空缓存的 190 项请求检查通过，三份远程 SRS 实际下载、缓存字节正确 |
| 探测进程与监听 | 两次进程均退出 0，共 4 个回环监听全部关闭 |
| 历史保留 | 8 个既有 Release 的元数据与资产身份/摘要不变；11 个历史标签引用不变 |

两个入口合计 **380 项请求检查**。每个入口包含 184 项主监听请求和 6 项来源方向请求；五个新增后缀各检查根域、一层/多层子域，以及近似前缀和错误父域。业务目标在回环探测中被拒绝，没有向这些服务发起登录、支付或验证码业务请求。

## 发布身份与证据

Release ID：`419231418`；输入提交：`b7b7c53ed4124bfa2abea9e79c771c8dfda728da`；版本标签提交：`a15a40e3a97d42a17f101a5af5a41ab2c6663a5b`。Release 正文按仓库约定留空。源码 ZIP 固定在标签提交，内部报告保留上传前状态；最终发布回执另行提交至 main，不移动版本标签。

- [发布汇总](publication-results.json) · [Latest API 回执](release-final-status.json) · [历史发行核对](historical-releases-verification.json)
- [固定下载结果](fixed-downloads.json) · [Latest 下载结果](latest-downloads.json)
- [固定入口原生结果](remote-fixed/results.json) · [固定入口运行日志](remote-fixed/runtime.log)
- [Latest 原生结果](remote-latest/results.json) · [Latest 运行日志](remote-latest/runtime.log) · [探测脚本](remote-probe.py)
- [本版发布授权](../../../sources/evidence/release-v0.1.7-authorization.json) · [语义批准](../../../sources/evidence/release-v0.1.7-review.json)

静态制品发布与本机隔离检查不等于用户设备已刷新或真实业务验收。本次没有访问或修改用户设备；manifest 保持 `validated_consumers=[]`、`integration_evidence=[]`、`deployment_status=pending`。
