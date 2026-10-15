# v0.1.5：补齐 Claude 网站清单（排除 NTP）

2026-10-15。**正式制品已完成本地验证，尚待上传及公开下载验收。** 最终发布回执将在主分支更新，标签内保留本上传前记录。

本版按用户要求覆盖 Net.Coffee 网页各配置格式的并集：20 项域名／关键词要求、两个目的 CIDR（`160.79.104.0/21`、`2607:6bc0::/32`），排除 NTP。完整清单见[补齐报告](../../net-coffee-claude-supplement-2026-10-15.md)。OpenAI 和 Anthropic 来源规则与 v0.1.4 字节一致。

两次正式构建各 **2,636 项原生检查通过**；完整回归 **64 项通过，0 失败、0 跳过**。两次构建的三份 SRS、三份 JSON 和 manifest 逐字节一致；六份产品文件与候选一致。

输入提交：`66f228557a5ee0e82d34a1be25331d7eccd3bf89`。本次授权仅发布静态发行，未改变现网客户端；manifest 继续保持 `validated_consumers=[]`、`integration_evidence=[]`、`deployment_status=pending`。

- [正式 manifest](../../../artifacts/v0.1.5/manifest.json) · [批次摘要](../../../artifacts/v0.1.5/SHA256SUMS)
- [构建结果](build-results.json) · [完整回归](unit-tests.log) · [语义差异](semantic-diff.json) · [独立审阅](independent-review.json)
- [发布授权](../../../sources/evidence/release-v0.1.5-authorization.json) · [语义审批](../../../sources/evidence/release-v0.1.5-review.json)
- [空缓存探测脚本](remote-probe.py)

`anthropic.srs` SHA-256：

```text
0d8e26718c663ffdb03d0d32a2cf42bf61be540787c46fa7684bf1a70a23c5f1
```
