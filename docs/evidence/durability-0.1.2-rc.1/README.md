# 0.1.2-rc.1 候选证据与复现入口

核验日期：2026-10-03。这里归档本地候选 `0.1.2-rc.1` 的原始证据，正式目标为 `0.1.2`。候选 manifest 的 `source_commit=9f33df7464d134cb347301ca1fbafde0e1f5fc8a` 仅是当时工作树基础提交，`inputs` 哈希才完整描述实际未提交输入；不将其改写为正式提交或发布批准。正式构建须在本轮输入提交后重新执行。

## 结果与原始证据

- [候选 manifest](../../../artifacts/v0.1.2-rc.1/manifest.json) 与[候选校验和](../../../artifacts/v0.1.2-rc.1/SHA256SUMS)：candidate 身份，发布批准为 null，消费者声明为空，部署 pending。
- [构建汇总](build/build-summary.json)、[两批与 v0.1.1 对比](build/byte-comparison.json)、[单元回归日志](build/unittest.log)：两次各 2,066 项原生验证零失败，46 项回归通过，无跳过；三 SRS 与三 JSON 两批一致。
- [原生 sync 前](build/sync-before.json)与[原生 sync 后](build/sync-after.json)：保留基线、补充和来源元数据差异；唯一规则语义新增是 Anthropic root suffix `claude.dev`。
- [上游语义差异](domain/geosite-semantic-diff.json)、[固定来源下载记录](domain/fetch-baselines.json)、[独立复核](domain/candidate-independent/review.json)：完整 SRS 基线与 DLC 对应字段一致，新增条目属于社区基线，不冒称官方最小网络白名单。
- [消费者结果](consumer/results.json)：560 个合成请求，392 DNS、168 route；8 个 sing-box 进程全部退出 0、12 个监听关闭，受控 HTTP 空缓存下载一次且摘要匹配。
- [用户截图九项覆盖](screenshot-domain-coverage.json)：8 个 root suffix 与 1 个 exact 全部在新候选中，旧 v0.1.1 仅缺 `claude.dev`。
- [OpenAI 来源复核及局限](domain/openai/review-result.json)：Voice 字节和地址不变；成功取得的 Codex 来源未发现主机增量。OpenAI 网络和登录页面均 HTTP 403，最新正文未核实，不据此声称官方清单完整无变更。
- [候选发布门禁预期拒绝](build/publication-gate-rejected.json)：本候选不能直接晋升为正式发布；正式输入、构建模式和摘要批准须重新绑定。

`consumer/` 中的配置、日志、数据库和命令记录来自合成回环实验；其中绝对缓存路径只定位当时环境，不能直接作为当前运行路径。真实登录、账户、Challenge、公网出口、生产 DNS、TUN、目标设备及重启持久化不在本批验收范围。

## 手动复现

从仓库根目录执行现有脚本，使用 `tools.lock.json` 的 sing-box `1.15.0-alpha.9`、Go `1.27.1` 与经 `--require-hashes` 安装的 PyYAML `6.0.3`。工具和依赖先按哈希核验；离线阶段使用已准备的模块缓存，设置 `GOTOOLCHAIN=local`、`GOPROXY=off`、`GOSUMDB=off`、`GOWORK=off`，全部缓存及 `TMPDIR` 指向会话私有目录。

以下为复现顺序说明，输出目录须选择尚不存在的会话缓存路径：

1. 用 `python scripts/generate.py --mode candidate --output <新目录>` 生成候选，再用 `python scripts/validate.py <新目录>` 验证。当前工作树已面向正式 `0.1.2` 准备，重新生成的 manifest 不会等同历史 `0.1.2-rc.1` manifest；规则 JSON/SRS 应按摘要逐字节核对。
2. 设置 `SINGBOX_TEST_BATCH=<已验证目录>` 后运行 `python -m unittest discover -s tests -v`，必须全量 46 项通过且无跳过。
3. 运行 `python tests/claude_dev_consumer.py --candidate <已验证目录> --baseline artifacts/v0.1.1 --output <新证据目录>`；它只使用合成回环配置，结果与清理断言均须通过。
4. 正式发布按[正式方案的执行计划](../../plan.md#execution)进行，使用 release 模式和 `--for-release`，不得把本候选的 null 批准修改为通过。

本仓库的 `Validate rules` workflow 已在 main `ed69b36617f7afa0c1244e724c4a4d54f303587c` 删除，当前没有对应定时或推送 CI；上述复现和本轮发布均为手动过程。
