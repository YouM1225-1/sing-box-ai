# alpha.9 消费者与启动机制证据

核验日期：2026-09-28。固定实现：sing-box `1.15.0-alpha.9` / `132b38e9caaba1a1959354d518e54d2d08419afe`。

这些脚本仅使用 Python 标准库及指定 sing-box 二进制。监听地址全部为 `127.0.0.1` 的临时高端口，DNS/HTTP 上游也全部是本机合成响应器；不读取生产凭据、设置系统代理、创建 TUN 或连接 N100。`--output` 必须指向尚不存在的新目录，避免旧缓存影响案例；只终止脚本自己启动的子进程。

从规则仓库根目录运行（替换证据目录实际位置）：

```bash
python3 docs/evidence/round3/consumer/remote_startup.py --binary .tools/sing-box --output build/repro-round3-startup
python3 docs/evidence/round3/consumer/dns_non_address.py --binary .tools/sing-box --output build/repro-round3-dns
```

## 结果与复现层级

- `observed-22-rule-non-address-results.json`：保留原 N100 2026-09-28 保存的 22 条 DNS 规则对象/顺序，使用固定旧 SRS 与审阅合成 SRS/inline，测得 126 次查询，modern 84 次、明确构造 legacy 对照 42 次。modern 产品 TXT/SVCB/MX/CNAME 首命中索引 16；HTTPS 为 0、AAAA 为 15。无关域名到 19。该运行使用历史本地外部规则集输入，结果是历史观测，并不声称能从附带最小 fixture 重建完整 N100 消费者。
- `dns_non_address.py` 与 `fixtures/` 是相同机制的最小可复现五规则 fixture：126 次查询；modern 对应索引变为 2（产品非地址）、0（HTTPS）、1（AAAA）、3（无关域名）。记录为 `minimal-non-address-results.json`，不计作新增生产覆盖。old/fixture 的 SRS 与 inline 在这一矩阵完全相同；仅两个 legacy 子进程设置 `ENABLE_DEPRECATED_LEGACY_DNS_ADDRESS_FILTER=true`。
- `remote_startup.py` 完全自包含，生成 synthetic old/new/wrong 三份 SRS：11 个启动案例、7 成功、4 预期失败；21 次 DNS 验证确认已载入内容；remote `rules` 字段被解析器拒绝。初次观测与可复现重跑分别存 `observed-remote-startup-results.json`、`minimal-remote-startup-results.json`，是同一案例重复，不双计覆盖。
- `exit-consumer-results.json` 是补齐退出全集的历史观测：27 个见证 × old/rc1/candidate × A/AAAA =162 次查询，837 次原生 SRS 会员断言均通过。包含每个输入 SHA、首命中索引、实际响应和条件路由表。candidate 为构建前 source/SRS fixture，是否等于正式构建以最终同步摘要为准。正则仅两个见证，suffix 为 apex 与一个子域见证；完整语言退出范围由同批退出 ledger 给出。

域名会员和 DNS 查询阶段不等于实际业务流量；路由表仅为 Rule 模式普通 TCP443、有域名元数据、无更早 private/IP/ASN/协议/内核旁路的条件推导。缓存关闭；合成 A/AAAA 响应不能证明生产 DNS、登录、Challenge、出口、IPv6 或手机/TV 已验收。

## 关键发现

同 tag 改 remote URL 会使 URLHash 不同的旧缓存失效并要求启动抓取。成功拉新后缓存按 tag 覆盖，回旧 URL 不恢复旧缓存；HTTP503 时启动失败。initial_path 缺失/坏 SRS 无法兜底，但格式有效、内容错误的 SRS 被接受，运行时不核对预期发布摘要。

当前配置的 query_type/evaluate/match_response 等条件禁用 legacy；非地址查询会走 modern 的 Match，并非旧 matchDNS 的 WithAddressLimit skip。固定源码：[模式判定](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L1417)、[Exchange 分派](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L1208)、[modern 规则遍历](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L648)、[legacy skip](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/dns/router.go#L296)、[remote 启动](https://github.com/SagerNet/sing-box/blob/132b38e9caaba1a1959354d518e54d2d08419afe/route/rule/rule_set_remote.go#L104)。
