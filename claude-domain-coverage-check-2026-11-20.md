# 用户规则与仓库最新规则对比

对比对象是仓库当前最新版本 `v0.1.15` 的 [`artifacts/v0.1.15/anthropic.json`](artifacts/v0.1.15/anthropic.json)。

## 已覆盖

以下用户规则在最新仓库规则中有等价命中：

- 精确域名：`challenges.cloudflare.com`、`http-intake.logs.us5.datadoghq.com`、`http-intake.us5.datadoghq.com`、`browser-intake-us5-datadoghq.com`、`claude-check.shuita.xyz`
- 后缀：`sentry.io`、`statsigapi.net`、`anthropic.com`、`claude.ai`、`claude.com`、`claude.dev`、`clau.de`、`claudeusercontent.com`、`claudemcpclient.com`、`claudemcpusercontent.com`、`fullstack-anthropic-website-b-cdn.net`
- 关键字：`anthropic`、`claude`
- IP 网段：`160.79.104.0/21`、`153.61.224.0/22`、`2607:6bc0::/32`

其中 Datadog 主机通过 `domain_keyword: datadog` 命中，Claude 和 Anthropic 相关主机通过 `domain_keyword: anthropic` 或 `domain_keyword: claude` 命中。

## 未覆盖

- 精确域名：`api.ipify.org`、`ipify.org`
- 后缀：`featuregates.org`、`ip.sb`
- IP 网段：`153.61.208.0/20`

## 结论

仓库最新 `v0.1.15` 已覆盖你发来的规则中的 21 项，未覆盖 5 项。未覆盖项只有两个 IP 查询域名、两个后缀和一个 IPv4 网段。

本次提交已包含 UniFi 导出、验证和覆盖文档。规则制品版本仍为 `v0.1.15`，本次提交没有新建发布版本。
