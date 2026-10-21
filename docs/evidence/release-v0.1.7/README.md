# v0.1.7 发布记录

用户于 2026-10-21 在候选验收及用途说明后明确要求“发布”。当前处于正式输入和发布验证阶段；完成后的 GitHub 地址与结果会在本页更新。

唯一规则增量是 Anthropic 的五个 `domain_suffix`：

| 后缀 | 范围和来源 |
|---|---|
| `growthbook.io` | 根域及全部子域，用户指定覆盖 |
| `hcaptcha.com` | 根域及全部子域，用户指定覆盖 |
| `stripe.network` | 根域及全部子域，用户指定覆盖 |
| `stripecdn.com` | 根域及全部子域，用户指定覆盖 |
| `segment.io` | 根域及全部子域，用户指定覆盖 |

原规则全部保留；OpenAI、Anthropic 来源 IP 两份 SRS 与 v0.1.6 字节一致；IP、关键词和消费者 IPv6 动作不变。来源身份为 `user-requested`，不宣称这些共享后缀都是 Claude 官方必需依赖。具体授权范围见[本次覆盖指令](../../../sources/evidence/one-exit-coverage-request-2026-10-21.json)。

已验收候选为 [v0.1.7-rc.1 manifest](../../../artifacts/v0.1.7-rc.1/manifest.json)，2,720 项原生检查、66 项回归全部通过；正式发布需另行完成已提交输入绑定、两次独立 release 构建、固定下载与空缓存验证，随后设为 Latest。

静态制品发布不等于用户设备已刷新或真实业务验收。不会访问或修改用户设备，manifest 的消费者证据保持为空、部署状态为 pending。
