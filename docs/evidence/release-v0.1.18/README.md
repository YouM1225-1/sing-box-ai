# v0.1.18 Claude 地址后缀补充发布

2026 年 11 月 22 日，`v0.1.18` 完成正式构建。Anthropic 目的规则新增三个用户指定的完整域名后缀。

- `intercomassets.com`
- `intercom-messenger.com`
- `yoti.com`

## 检查结果

- release 模式原生检查通过 6,462 项，失败 0
- 三个 SRS 均完成独立重建，重建字节一致
- UniFi 派生域名、IPv4、IPv6 清单由同批制品生成
- OpenAI 与 Anthropic source-IP 制品保持与 v0.1.17 一致
- Python 回归测试通过 101 项，6 项因本机环境条件跳过
- 发布门禁保持 `validated_consumers=[]`、`integration_evidence=[]` 和 `deployment_status=pending`

## 制品摘要

| 文件 | SHA-256 |
| --- | --- |
| `anthropic.srs` | `f49fda58dd9d5f240dc7d332bf093d9aa07966e15fbb881b08ffd760742ee345` |
| `anthropic-ip.srs` | `819dcba59e171957aff80c4ddf6c0dd9fd984620e2ee0a7f363deb879828261a` |
| `openai.srs` | `926a8e1385b8007855f29413a2bba265e49aa796e5124e6cb3ea80aa964ecb5e` |

完整可复验文件位于 [`artifacts/v0.1.18/`](../../../artifacts/v0.1.18/)，当前派生清单位于 [`dist/`](../../../dist/)。逐项地址核对见 [`claude-screenshot-address-coverage-2026-11-22.md`](../../claude-screenshot-address-coverage-2026-11-22.md)。
