# poteto.com 加入 OpenAI 规则

日期：2026-10-28

已将图片中的 `poteto.com` 加入本地 OpenAI 源规则，覆盖根域名及其子域名。`notpoteto.com`、`poteto.com.invalid` 不匹配。

```json
{"domain_suffix": ["poteto.com"]}
```

来源为本次用户指令，使用 `user-requested` 分类；[源规则](../sources/openai.yaml)与[指令记录](../sources/evidence/poteto-coverage-request-2026-10-28.json)已保存。规则字段写法已核对 [sing-box 官方文档](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/#domain_suffix)。

## 验证结果

- 使用仓库锁定的 sing-box `1.15.0-alpha.9` 编译，2,734 个原生匹配用例全部通过，包含 14 个新域名相关用例。
- JSON 与 SRS 语义一致、重复编译字节一致，`sing-box check` 通过。
- 相对 `v0.1.7`，唯一规则变化为 OpenAI 新增 `domain_suffix: poteto.com`；Anthropic 和 Anthropic IP 的 SRS 字节不变。
- 完整回归首次执行 68 项：67 项通过，1 项发布测试被既有过期记录提前拦截。调整该单元测试的隔离方式后，相关 6 项全部通过；生产校验器的有效期检查保持不变。
- 历史日期测试使用已发布 `v0.1.7` 的 OpenAI 输入，当前新增规则另有范围及错误分类测试。

## 文件与生效状态

- [本地候选 OpenAI SRS](../build/poteto-2026-10-28-validated/openai.srs)
- [可读 JSON](../build/poteto-2026-10-28-validated/openai.json)
- [构建与验证清单](../build/poteto-2026-10-28-validated/manifest.json)
- [完整回归初次日志](../build/poteto-tests-2026-10-28.log)与[相关测试复验日志](../build/poteto-artifact-tests-2026-10-28.log)

用户随后授权发布，并明确批准 v0.1.8 沿用两份未变的 Anthropic 制品，保留原复核日期和证据；没有声称 Challenge 已重新验证。最终状态与下载入口以[本次发布记录](evidence/release-v0.1.8/README.md)为准。
