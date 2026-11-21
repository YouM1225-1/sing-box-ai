# v0.1.17 共享服务补充规则发布

2026 年 11 月 21 日，`v0.1.17` 完成正式构建并发布。Anthropic 目的规则新增 `sift.com`、`siftscience.com`、`statsig.com` 和 `prodregistryv2.org` 四个共享服务根域，规则登记为用户明确要求的覆盖范围，不宣称官方 Claude 依赖或消费者运行验收。

## 验证结果

- release 模式原生校验通过 6,420 项，失败 0。
- 所有 SRS 完成独立重建，重建字节一致；构建工具链为 `go1.27.1`。
- UniFi 派生域名、IPv4、IPv6 清单从同批制品生成并通过同步校验，分别为 73、427、1 项。
- OpenAI 与 Anthropic 源地址制品摘要与 `v0.1.16` 保持一致。
- 完整 Python 回归通过 101 项，6 项按仓库条件跳过。

## 制品摘要

| 文件 | SHA-256 |
| --- | --- |
| `anthropic-ip.srs` | `819dcba59e171957aff80c4ddf6c0dd9fd984620e2ee0a7f363deb879828261a` |
| `anthropic.srs` | `12ecdd3dfa38a841be8d0f76d0d74b84446ef5ec124ebced5b29ef88a82ef9e4` |
| `openai.srs` | `926a8e1385b8007855f29413a2bba265e49aa796e5124e6cb3ea80aa964ecb5e` |

- [Anthropic SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.17/anthropic.srs)
- [Anthropic source-IP SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.17/anthropic-ip.srs)
- [OpenAI SRS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.17/openai.srs)
- [GitHub Release v0.1.17](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.17)

本次发布保持 `validated_consumers=[]`、`integration_evidence=[]` 和 `deployment_status=pending`。这些字段只表示静态制品发布门禁通过，消费者运行验收仍单独记录。

同批完整可复验文件位于 `artifacts/v0.1.17/`，当前派生清单位于 `dist/`。发布门禁绑定已提交源 `83b1eaf4ee302377b34b2fef9fe7925e07f93248`、四项新增规则的用户指令、保留旧兼容条目的版本绑定例外，以及本批三个 SRS 摘要。
