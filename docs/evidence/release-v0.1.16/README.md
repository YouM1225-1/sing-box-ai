# v0.1.16 完整覆盖规则发布

2026 年 11 月 20 日，v0.1.16 已推送到 `main`，创建 GitHub Release 并设为 Latest。此次补入用户提供规则中此前缺失的 `api.ipify.org`、`ipify.org`、`featuregates.org`、`ip.sb` 和 `153.61.208.0/20`。

## 验证结果

- 发布模式原生校验通过 6,332 项，失败 0。
- 完整 Python 回归通过 100 项，6 项按仓库条件跳过。
- UniFi 派生域名、IPv4、IPv6 清单已从同批制品重新生成并通过同步校验。
- OpenAI 与 Anthropic 来源 IP 制品摘要保持 v0.1.15 不变。
- 完整 Anthropic 规则覆盖用户提供的 26 项。
- GitHub Latest 为 `v0.1.16`，6 个发布资产均已上传。
- 固定下载的三个 SRS 与本地摘要一致。

## 制品摘要

| 文件 | SHA-256 |
| --- | --- |
| `anthropic-ip.srs` | `819dcba59e171957aff80c4ddf6c0dd9fd984620e2ee0a7f363deb879828261a` |
| `anthropic.srs` | `d62a03c44427400c4533f87aa76bbc0b3fcc18e034890e9f2ae724316323e2cc` |
| `openai.srs` | `926a8e1385b8007855f29413a2bba265e49aa796e5124e6cb3ea80aa964ecb5e` |

- [Anthropic SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.16/anthropic.srs)
- [Anthropic source-IP SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.16/anthropic-ip.srs)
- [OpenAI SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.16/openai.srs)
- [GitHub Release v0.1.16](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.16)

本次发布保持 `validated_consumers=[]`、`integration_evidence=[]` 和 `deployment_status=pending`，这些字段只表示静态制品发布门禁通过。
