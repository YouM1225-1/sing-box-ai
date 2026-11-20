# Sift 域名覆盖核对

核对日期：2026-10-29（Asia/Shanghai）。范围：用户截图中的 `SiftScience` / `api3.siftscience.com`。

## 结论

**已包含，无需补加或重新发布。** 已发布的 v0.1.8 Claude / Anthropic 域名规则集 `anthropic.srs` 包含 `domain_keyword: sift`，因此截图中的 `api3.siftscience.com` 会命中。

该条目属于域名关键词匹配，并非仅收录某个完整域名：域名任意位置含连续的 `sift` 都会覆盖，范围比 `sift.com` 或 `siftscience.com` 后缀规则更广。

## 证据与实测

- [源规则](../sources/anthropic.yaml) 中的 `sift` 条目标记为 `user-requested`，来源为已有的站点覆盖要求；它不是“Claude 官方声明必需”的标记。
- [v0.1.8 归档 JSON](../artifacts/v0.1.8/anthropic.json) 的 `domain_keyword` 列表为 `datadog`、`sentry`、`sift`。
- 本次重新下载了 [GitHub v0.1.8 发布的 anthropic.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.8/anthropic.srs)，与本地发布归档逐字节一致。SHA-256：`38aeb4b09903bb238df6f33b476a247830719d7246950edc024660dd6e112ab4`。
- 使用项目自带 sing-box 的原生 `rule-set match --format binary` 检查下载文件，结果如下。判定依据是实际匹配输出，不能仅凭退出码判断，因为未命中也返回 0。

| 域名 | 实测结果 |
| --- | --- |
| `api3.siftscience.com` | 命中 |
| `api.sift.com` | 命中 |
| `cdn.sift.com` | 命中 |
| `beforeSIFTAFTER.example.org`（合成测试域名） | 命中，验证大小写及子串匹配 |
| `si-ft.example.org`（合成测试域名） | 未命中 |

原始证据：[匹配输出及下载校验记录](evidence/sift-coverage-2026-10-29/match-results.json)、[实际测试的 SRS 文件](evidence/sift-coverage-2026-10-29/anthropic.srs)。这些是本地规则匹配测试，不代表访问了这些域名或验证了用户设备的实时流量。

## 截图中的 Sift 和 BLOCKED

Sift 提供反欺诈及风险识别服务。其[官方 SDK 文档](https://developers.sift.com/docs/curl/api-overview)直接列出 `api3.siftscience.com` 作为移动端事件上传端点，说明该域名确实用于 Sift 服务；这些资料不能单独证明 Claude 当前哪些功能必须依赖它。

截图中的 **BLOCKED** 是截图所用工具显示的拦截状态，不能据此推断本项目规则漏收。`anthropic.srs` 本身提供匹配条件；实际走哪个代理、直连还是被拦截，取决于使用它的客户端配置、规则顺序及其他拦截层。本次没有检查用户设备的实际配置或连接日志。

本次仅核对覆盖情况并保存证据，没有修改规则或发布新版本。
