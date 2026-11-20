# 用户规则与仓库最新规则对比

对比对象是仓库新发布的 `v0.1.16` 制品 [`artifacts/v0.1.16/anthropic.json`](artifacts/v0.1.16/anthropic.json)。

## 结果

你提供的 26 项规则现已全部覆盖：

- 精确域名：`challenges.cloudflare.com`、`http-intake.logs.us5.datadoghq.com`、`http-intake.us5.datadoghq.com`、`browser-intake-us5-datadoghq.com`、`claude-check.shuita.xyz`、`api.ipify.org`、`ipify.org`
- 后缀：`sentry.io`、`statsigapi.net`、`featuregates.org`、`anthropic.com`、`claude.ai`、`claude.com`、`claude.dev`、`clau.de`、`claudeusercontent.com`、`claudemcpclient.com`、`claudemcpusercontent.com`、`fullstack-anthropic-website-b-cdn.net`、`ip.sb`
- 关键字：`anthropic`、`claude`
- IP 网段：`160.79.104.0/21`、`153.61.208.0/20`、`153.61.224.0/22`、`2607:6bc0::/32`

其中 Datadog 主机通过 `domain_keyword: datadog` 或 `domain_suffix: datadoghq.com` 命中，Claude 和 Anthropic 相关主机通过对应关键字或后缀命中。

## 发布状态

`v0.1.16` 已在 `main` 上生成并完成正式发布校验。OpenAI 与 Anthropic 来源 IP 制品保持原摘要，Anthropic 目的制品新增 5 项此前缺失的规则。

- 原生发布校验：6,332 项，失败 0
- 完整回归：100 项通过，6 项按仓库条件跳过
- UniFi 派生清单已按 `v0.1.16` 重新生成
