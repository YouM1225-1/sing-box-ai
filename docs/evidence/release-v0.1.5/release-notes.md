补齐 Net.Coffee Claude 页面各配置格式中除 NTP 外的域名、关键词和目的 IP 范围。覆盖整页并集的 20 项域名／关键词要求与 `160.79.104.0/21`、`2607:6bc0::/32`；当前归档的 AS399358 三个公告前缀均在其中。

- 新增缺失的 Auth0、Ghost、Cloudflare CDN、Statsig、Intercom、Fathom 等域名范围，以及 `datadog`、`sentry`、`sift` 关键词。
- OpenAI 目的规则和 Anthropic 来源规则与 v0.1.4 字节一致。
- 两次正式构建各 2,636 项原生检查通过；64 项回归测试通过，0 失败、0 跳过；正式产品文件与已验收候选字节一致。
- 这是用户指定网页清单的覆盖扩展；关键词也会匹配其他产品使用的第三方域名。静态范围不保证未来 ASN 公告、任意第三方依赖或已登录业务可用。

现有 Latest 订阅地址保持不变。`anthropic-ip.srs` 仍仅匹配来源地址，不应作为客户端目的规则使用。

覆盖清单：[补齐报告](https://github.com/YouM1225-1/sing-box-ai/blob/main/docs/net-coffee-claude-supplement-2026-10-15.md)。发布与公开下载验证：[发布记录](https://github.com/YouM1225-1/sing-box-ai/blob/main/docs/evidence/release-v0.1.5/README.md)。
