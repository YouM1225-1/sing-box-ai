# Claude 截图域名覆盖核对

核对日期为 2026 年 11 月 18 日。

## v0.1.14 发布结果

**v0.1.14 已推送到远端 `main` 并设为 GitHub Latest，截图 17 个域名全部覆盖。** 新增的 `ant.dev` 与 `antspace.dev` 各用一条 `domain_suffix`，匹配根域及全部子域。 [GitHub v0.1.14 发布页](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.14)

本地 92 项回归和两次各 6,184 项原生构建检查全部通过。固定版与 Latest 各通过 6 个附件的摘要核验以及 791 项空缓存加载后的回环请求检查，包含截图域名、子域与边界反例。发布在独立工作树中完成，本机当前主工作区仍检出 v0.1.12。 [远端发布核验记录](https://github.com/YouM1225-1/sing-box-ai/blob/bc37ab108a9801d6002ee3725ab1ede9f63fe4e9/docs/evidence/release-v0.1.14/README.md)

## 增补前的覆盖

增补前 GitHub 最新版 **v0.1.13 覆盖截图中的 15／17 个域名**，未命中的是 **`ant.dev`** 和 **`antspace.dev`**。本地 `main` 的 v0.1.12 制品覆盖 8／17 个。两个版本均覆盖评论可能指的 `datadoghq.com`，该域名另外核对。 [GitHub v0.1.13 发布页](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.13)

## 逐项结果

表中“后缀”表示按该行域名的后缀命中，“关键词”表示主机名包含指定字符串。逐项测试了所列域名、加 `www.` 的子域和加 `audit.deep.` 的多级子域。同一域名的三个测试结果一致。

| 截图域名 | 本地 v0.1.12 | 增补前 v0.1.13 |
| --- | --- | --- |
| `claude.ai` | 后缀 | 关键词 `claude` |
| `ant.dev` | 未命中 | **未命中** |
| `anthropic.com` | 后缀 | 关键词 `anthropic` |
| `anthropic.team` | 未命中 | 关键词 `anthropic` |
| `antspace.dev` | 未命中 | **未命中** |
| `chatbotclaude.com` | 未命中 | 关键词 `claude` |
| `clau.de` | 后缀 | 后缀 |
| `claude.app` | 后缀 | 关键词 `claude` |
| `claude.com` | 后缀 | 关键词 `claude` |
| `claude.dev` | 后缀 | 关键词 `claude` |
| `claude.new` | 未命中 | 关键词 `claude` |
| `claude.site` | 未命中 | 关键词 `claude` |
| `claudeacademy.com` | 未命中 | 关键词 `claude` |
| `claudemcpclient.com` | 后缀 | 关键词 `claude` |
| `claudemcpcontent.com` | 后缀 | 关键词 `claude` |
| `claudepages.dev` | 未命中 | 关键词 `claude` |
| `claudestudio.com` | 未命中 | 关键词 `claude` |

## 评论中的 Datadog

截图写的是 `datadighq`，这里按 Datadog 官方列出的 `datadoghq.com` 另行核对。两个版本均通过 `datadog` 关键词覆盖 `datadoghq.com`。Claude Code 文档里的 `browser-intake-us5-datadoghq.com` 也在两版中命中，v0.1.13 同时匹配 `browser-intake`。按截图原拼法测试的 `datadighq` 和 `datadighq.com` 均未命中。 [Datadog 站点文档](https://docs.datadoghq.com/getting_started/site/) · [Claude Code 网络配置文档](https://code.claude.com/docs/en/network-config)

## 核对依据

- 本地测试使用 [`dist/anthropic.srs`](../dist/anthropic.srs)，与 v0.1.12 归档制品逐字节一致。 [v0.1.12 规则 JSON](../artifacts/v0.1.12/anthropic.json)
- 增补前从 GitHub Latest 下载的 `anthropic.srs` 与当时的 v0.1.13 标签归档和远端 `main` 制品逐字节一致。SHA-256 为 `090329f326922e3d4c1a88f219d71666401c0abc33c098e9c9b233edbc1281c1`。 [v0.1.13 固定版 SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.13/anthropic.srs) · [v0.1.13 规则 JSON](https://github.com/YouM1225-1/sing-box-ai/blob/v0.1.13/artifacts/v0.1.13/anthropic.json)
- 使用仓库内的 sing-box 1.15.0-alpha.9 执行 `rule-set match -f binary`，并反编译二进制确认命中字段。结果适用于规则集本身，设备最终走向取决于实际加载的版本和配置中的规则顺序。
