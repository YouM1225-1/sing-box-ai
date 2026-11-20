# Claude 五个域名的规则覆盖核对

核对日期：2026-11-07。当前工作区版本：v0.1.9。

**新截图中的 5 个域名全部已被 `anthropic` 规则集覆盖，无需补充规则。** 新增核对的 `platform.claude.com` 由 `claude.com` 后缀规则覆盖。

| 域名 | 是否覆盖 | 命中规则 |
| --- | --- | --- |
| `api.anthropic.com` | 是 | `domain_suffix: anthropic.com` |
| `downloads.claude.ai` | 是 | `domain_suffix: claude.ai` |
| `http-intake.logs.us5.datadoghq.com` | 是 | `domain_keyword: datadog` |
| `bridge.claudeusercontent.com` | 是 | `domain_suffix: claudeusercontent.com` |
| `platform.claude.com` | 是 | `domain_suffix: claude.com` |

依据：[v0.1.9 发布规则 JSON](../artifacts/v0.1.9/anthropic.json)。其中 `claude.com` 位于第 34 行，覆盖其子域名 `platform.claude.com`。

[当前分发的 anthropic.srs](../dist/anthropic.srs) 与 [v0.1.9 发布的 anthropic.srs](../artifacts/v0.1.9/anthropic.srs) 字节完全一致；使用仓库内 `.tools/sing-box` 反编译后，JSON 内容与发布规则完全一致，确认编译产物也包含 `claude.com` 后缀规则。前 4 个域名的详细核验见 [此前核对记录](claude-four-domain-coverage-2026-11-05.md)。

本结论确认仓库规则覆盖；截图中的流量统计本身不能证明客户端命中了哪条规则或采用哪个出口。
