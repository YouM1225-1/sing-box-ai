# v0.1.9 Persona 补充与发布准备

日期：2026-10-30。用户指令：**“联网搜索相关信息 添加并发布”**。

当前状态：Persona 补充已完成。初次预检因 Challenge 复核过期受阻，用户随后明确要求“先继续添加 发布”“继续 完成发布”；本次按限定的旧条目保留例外准备静态发布。真实 Challenge 复验仍未完成，不更新原复核日期。正式发布及下载结果将在完成后记录于此。

## 已核实的依据与唯一规则增量

- [Claude 身份验证说明](https://support.claude.com/en/articles/14328960-identity-verification-on-claude)确认验证服务商为 Persona。
- [Persona Security](https://docs.withpersona.com/security)列出 `withpersona.com` 根域及标准子域。
- [Persona WebView 网络要求](https://docs.withpersona.com/hosted-flow-webview-considerations)明确要求允许 `*.withpersona.com/*` 的外部网络请求。

因此在 Anthropic 规则中新增 **`domain_suffix: withpersona.com`**，覆盖根域及全部子域。标记为 `claude-identity-verification` 功能所需的共享依赖；它也会覆盖其他网站使用 Persona 的请求，不代表仅属于 Claude，也不代表已经证实截图中的错误得到修复。无需将 Persona 的邮件发送域名或服务器回调来源 IP 加入客户端目的规则。

三个官方页面均以普通 HTTPS 取得 HTTP 200，保存取得时间、响应摘要及事实定位；完整网页只保留于本地忽略目录，公开来源记录不复制整篇网页。[抓取记录](official-fetches.json) · [结构化事实](../../../sources/official/claude-identity.json) · [来源记录](../../../sources/official/source-records/claude-identity.json)。

| 制品 | 相对 v0.1.8 的变化 |
| --- | --- |
| `anthropic.srs` | 仅新增 `withpersona.com` 后缀 |
| `openai.srs` | 无规则变化 |
| `anthropic-ip.srs` | 无规则变化 |

完整证据：[语义差异](semantic-diff.json)、[候选可读规则](../../../artifacts/v0.1.9-rc.1/anthropic.json)、[候选 manifest](../../../artifacts/v0.1.9-rc.1/manifest.json)。

## 验证

- 候选构建通过；2,748 项原生匹配、源与二进制一致性、独立重建及隔离配置检查全部通过。[验证日志](candidate-validation.log)
- 第二次独立候选构建同样通过 2,748 项检查；三份 SRS、三份 JSON 和 manifest 均与第一次逐字节一致。[重建日志](rebuild-validation.log) · [构建汇总及制品摘要](build-results.json)
- 21 项专门检查通过：包括官方 11 个 Persona 域名、API/文件主机、多级子域、原有 Anthropic/Sift 对照及 3 个相似域名反例。[原始输出](persona-matches.json)
- 最终 79 项完整回归全部通过，无跳过，见[测试日志](unit-tests-final.log)。新增 5 项检查验证旧条目保留例外的日期、版本、输入与制品边界；最终候选另通过 2,748 项原生检查，见[日志](final-candidate-validation.log)。历史 v0.1.7/v0.1.8 差异与例外测试使用固定的 v0.1.8 Anthropic 源输入，避免把新功能误当成旧版本差异；新增单独测试核对当前版本只增加 Persona 及域名边界。原有发布校验断言未放宽。

## 正式构建

输入提交为 `92822cf877ba3c011d65fb7397d43169d8d868dc`。两次独立 release 构建分别通过 2,748 项原生检查与 `--for-release` 发布门槛，全部 9 个批次文件逐字节一致。同一提交生成的 candidate 再通过 2,748 项检查和 79 项完整回归；三份 SRS、三份 JSON 与正式批次一致。首次校验的 Go 相对路径调用失败已改用绝对路径重跑通过，没有修改校验逻辑。

[正式校验](release-validate.log) · [独立重建](release-rebuild-validate.log) · [同提交回归](unit-tests-release-fixture.log) · [构建汇总](build-results.json) · [完整正式批次](../../../artifacts/v0.1.9/manifest.json) · [批次校验和](../../../artifacts/v0.1.9/SHA256SUMS)。

## Challenge 记录与本次发布授权

发布预检实际返回：`Unapproved/expired compatibility: challenges.cloudflare.com`。[预检结果](release-preflight.json)

现有 Challenge 条目仍保留 `last_verified: 2026-09-27` 和 `review_after: 2026-10-27`。已有 v0.1.8 例外限定当日、版本、源文件及两份 Anthropic 制品全部不变；本次新增 Persona 后 Anthropic 制品发生变化，因此旧例外不能沿用。具体约束见[复核检查](../../../scripts/common.py)、[发布检查](../../../scripts/validate.py)与[v0.1.8 原例外](../../../sources/evidence/release-v0.1.8-unchanged-exception.json)。

联网确认 Persona 依赖不能冒充旧 Challenge 条目的新运行验证。随后检查到桌面端能进入现有会话，但没有出现可见 Challenge；浏览器控制不可用，用户选择稍后复验，再明确要求继续发布。见[初步观察](challenge-observation.json)。

本次新增的[限定例外](../../../sources/evidence/release-v0.1.9-preserved-entry-exception.json)只允许 2026-10-30 的 v0.1.9 发布，绑定 v0.1.8 源输入、原 Challenge 条目完整内容、唯一 Persona 增量及本批全部制品摘要；其他版本、日期、源变更或制品变化不能借用它。旧例外与旧运行证据保持原样。[本次发布授权](../../../sources/evidence/release-v0.1.9-authorization.json) · [语义审阅](../../../sources/evidence/release-v0.1.9-review.json)。

本批授权与语义审阅绑定、输入提交、两次正式构建及发布检查已完成。接下来完成草稿资产核对、非 Latest 公开后的固定下载与空缓存验证，随后切换 Latest 并复核。静态发布与真实设备上的验证成功分开记录。
