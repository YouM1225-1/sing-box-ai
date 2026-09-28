# 0.1.1-rc.1 本地候选验收

修订：1.1；日期：2026-09-28。用途：步骤1、2的来源、候选构建与隔离验收证据；不代表发布、部署或N100会话验收。

- [正式方案与当前状态](../../plan.md#execution)
- [机器汇总](local-results.json)、[语义差异](semantic-delta.json)、[构建尝试与最终结果](build-results.json)、[46项回归](unit-tests.log)
- [候选完整批次](../../../artifacts/v0.1.1-rc.1/manifest.json)、[同批校验和](../../../artifacts/v0.1.1-rc.1/SHA256SUMS)
- [395请求消费者](consumer/results.json)、[隔离转换](consumer/fixture-transform.json)、[37个完整外部集合身份](consumer/external-inputs.json)；原始集合在 `consumer/fixtures/`，无投影缩减。
- [公开资源链](function/network-results.json)、[四种临时安装](function/installer-results.json)、[npm原包完整性与wrapper](function/npm-results.json)、[真实npm离线安装](function/npm-cli-results.json)

消费者采用[同批测试脚本](../../../tests/consumer_durability.py)，只创建回环端口、进程、缓存和配置副本。可在规则仓库根目录运行下列命令，`--config` 输入对应待审核canonical路径；必须选择不存在的新输出目录，并具备锁定的 `.tools/sing-box`。输入配置只读，不会启动其TUN或生产出站。

```text
python3 tests/consumer_durability.py --candidate artifacts/v0.1.1-rc.1 --baseline artifacts/v0.1.0 --config <只读canonical.json路径> --output <新的本机测试目录> --fixture-cache docs/evidence/durability-0.1.1-rc.1/consumer/fixtures
```

上面的尖括号是必须填写的输入，不是可直接粘贴的shell执行块。缓存文件的URL与摘要仍需匹配当前输入；本批canonical摘要与所有SRS摘要见机器汇总。结果只证明这份固定配置的相关DNS/路由选择，不声称其他配置同样通过。

原始安装探测助手、上游脚本和下载主体留在本机忽略目录 `build/durability-0.1.1-rc.1/function-probes/`，其 `RESULTS.md` 与 `SHA256SUMS` 提供本地复现入口。这里仅归档网络事实/元数据、结果与小型日志，不复制265MB软件主体、字体文件或完整上游README。结果JSON中的当时路径、目录或响应摘要属于观测记录，不表示每个原始大文件在本目录都有副本。后续联网复算需从固定官方地址取得并核对同一摘要；旧source-record的HEAD证据不因后续安装而改写。

边界：IPv6仅真实本机`::1`入站与受控IPv6目的元数据；原序测试保留DNS全序和route[1:]，但ICMP bridge、hosts/mDNS、生产出站等作隔离替换。安装器只改两个测试目录，回退故障经loopback fixture注入；npm安装使用原始已验证tarball并关闭lifecycle/audit。没有登录、真实Artifacts渲染、N100访问或网络设置变更。

未执行：提交、推送、候选上传、Latest更新；真实候选URL冷启动留待步骤3。当前候选仍会被正式发布门槛拒绝。正式 `v0.1.0` 和旧审阅记录保留原样。
