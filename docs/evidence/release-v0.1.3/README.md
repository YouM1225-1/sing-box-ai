# v0.1.3 正式构建与发布记录

日期：2026-10-09（Asia/Shanghai）。本快照记录正式制品完成构建、等待上传的阶段；最终发布状态将在主分支本文件更新。

依据用户提供的 DMIT 隔离消费者验证，正式版本沿用已补齐的 7 个精确主机：

- `http-intake.logs.us5.datadoghq.com`
- `browser-intake-us5-datadoghq.com`
- `api-iam.intercom.io`
- `widget.intercom.io`
- `js.intercomcdn.com`
- `downloads.intercomcdn.com`
- `static.intercomassets.com`

没有新增未经用途证明的 Auth0、Ghost、Fathom、Sentry/Statsig 整后缀、关键词或 ASN；IPv4 `/21` 保持来源地址，目的范围仍为 IPv4 `/23` 与 IPv6 `/48`。

## 已完成的验证

| 层级 | 结果 |
|---|---|
| 用户验证包摘要 | 顶层 64 项全部匹配；嵌套清单仅核验各自随包的 4 项，不把未附带的 7 项输入计为本轮实物复验。 |
| VPS 消费者 | 459/459；DNS 240、route 219，6 组通过。 |
| 正式独立重建 | 两次均 2,164 项原生校验通过，并通过 `--for-release`。 |
| 与受测候选对比 | 三 SRS、三 JSON 在两次正式批次、测试 fixture 及 rc.1 间逐字节一致。 |
| 完整回归 | 47 项通过，0 失败、0 跳过；使用同正式输入的 candidate fixture。 |
| 输入提交 | `e8e65920c84efaf99d9b631712f461694926db60`；manifest 输入及语义证据均受提交绑定。 |

## 证据入口

- [消费者证据核对](consumer-review.json)：原始 ZIP / raw results 摘要、计数、范围和局限。
- [公开测试观察](consumer-observations.json)：459 行测试字段投影；不是原始完整结果文件。
- [两次构建结果](build-results.json)、[完整测试日志](unit-tests.log)。
- [正式 manifest](../../../artifacts/v0.1.3/manifest.json)、[正式文件摘要](../../../artifacts/v0.1.3/SHA256SUMS)。
- [本次发布授权](../../../sources/evidence/release-v0.1.3-authorization.json)、[静态语义审阅](../../../sources/evidence/release-v0.1.3-review.json)。
- [候选补齐分析](../../claude-rule-supplement-2026-10-09.md)、[公开下载空缓存核验脚本](remote-probe.py)。

## 验证边界

VPS 结果是实际 sing-box 加载合成参考策略、使用回环观察器的证据。它没有证明生产完整配置顺序、真实 Claude 登录、公网代理、外部 IPv6 或真实 Anthropic 来源入站。原始压缩包及生产/SSH 元数据保留本地，只公开必要摘要和测试观察。

正式 manifest 的 `validated_consumers`、`integration_evidence` 保持空，`deployment_status` 保持 `pending`；本轮授权发布静态制品，不授权修改或重启生产服务。旧正式批次与候选身份均保留。

发布顺序为：提交正式制品、推送 main/tag → 草稿完整上传与摘要核验 → 非 Latest 发布 → 固定 URL 下载及本机空缓存加载 → 设为 Latest → Latest 下载核验。
