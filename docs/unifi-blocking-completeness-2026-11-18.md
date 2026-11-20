# UniFi 阻断完整性复核

## 追加后的状态

2026 年 11 月 18 日 12:36（北京时间），已向 `AI-DirectBlock-Domains` 追加 `stripe.com` 和 `usefathom.com`。控制器读回和网关 dnsmasq 下发均为 **92 条**，原 90 条保留。按 UniFi 的域名和子域匹配，现覆盖 v0.1.14 可直接导出的 **67／67** 个域名。 [网关读回清单](../build/unifi-domain-roots-2026-11-18.fcl8u07g/domains.txt)

追加后，域名学习集合读回仍为 IPv4 0 条、IPv6 0 条。两条根域已配置覆盖其子域，实际域名阻断取决于网关学到的目的 IP。 [dnsmasq 手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)

13:11 完成受限预解析后，学习集合为 IPv4 40 个地址、IPv6 0 条。 [逐项查询结果](unifi-dns-warmup-2026-11-18.md)

## 为什么双栈学习集合为空

**92 条配置是要学习的域名。** UniFi 的 dnsmasq 必须亲自处理匹配的 DNS 查询，并拿到相应的 A 或 AAAA 地址，才能把结果写进 IPv4 或 IPv6 集合。只保存域名不会自动批量解析。11 月 11 日的受限预解析曾把 IPv4 集合从 6 项增加到 73 项，IPv6 集合保持 3 项，当时已观察到学习机制工作。 [dnsmasq 手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)

**常用的解析路径绕过了网关自己的 DNS 服务。** 主网管理 Mac 当前的 IPv4 DNS 是 `223.5.5.5`，该地址的下一跳是 N100（`192.168.3.2`）。主网下发的 IPv6 DNS 也指向 N100（`fd00:3::2`）。LoT 用 UniFi 作网关，但 DHCP 下发的是外部 DNS `223.5.5.5`。SMB 的 IPv4 DNS 才指向其 UniFi 网关地址。网关转发 DNS 包时，自己的 dnsmasq 不会因此学习地址。

**确认了重载，尚未确认集合何时清空。** 日志显示两次列表更新都伴随 dnsmasq 停止并重新启动，分别是 12:16:55 和 12:36:29。12:48 复核时 dnsmasq 正监听三条 LAN 的双栈 53 端口，两组仍各有 0 个成员。第二次更新前的快照也已经是 0／0。网关未开启逐条 DNS 查询日志，现有记录未能证实是哪一次操作清空了集合，也无法逐条回溯哪些查询曾进入 dnsmasq。

## 让 UniFi 处理匹配查询

可以。只要客户端向 UniFi 的 DNS 服务查询，dnsmasq 就可向上游解析，并按现有 92 条规则，把匹配域名返回的 A 和 AAAA 地址加入相应集合。防火墙域名对象负责匹配学到的 IP，它本身不会接管发给 N100 或外部解析器的查询。 [dnsmasq 手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)

如果接受让测试设备的常规 DNS 都由 UniFi 解析，最小试点是一台已使用 UniFi 作默认网关的 LoT 设备，将测试设备的 DNS 指向 LoT 网关 `192.168.4.1`。双栈试点还要核对设备实际使用的 IPv6 DNS。确认相同查询答案进入集合后，再核对实际直连命中及普通网站的对照结果。 [UniFi DHCP DNS 说明](https://help.ui.com/hc/en-us/articles/15179064940439-UniFi-DNS-Records-and-Local-Hostnames)

如果只想让清单内的查询交给 UniFi，当前收到查询的解析器需要按域名转发。让 N100 做这一步只能覆盖 N100 在线的时段。N100 整机重启时要靠 UniFi 继续阻断，客户端必须能独立使用 UniFi 的 DNS，且直连数据包实际走 UniFi。主网当前默认网关指向 N100，单独调整 DNS 不会让默认网关自动切换。 [UniFi DNS 转发说明](https://help.ui.com/hc/en-us/articles/12568927589143-Content-and-Domain-Filtering-in-UniFi)

## 追加前的复核

2026 年 11 月 18 日，UniFi Network 11.0.99。追加两个根域前，从控制器和网关读取了配置、内核规则及集合，并与 sing-box-ai v0.1.14 和 11 月 11 日的实际流量记录对照。

**结论。静态 IP 阻断已完整同步 v0.1.14，截图 17 个域名也全部下发，但当前 UniFi 对域名直连的阻断仍不完整。** 两次只读采样均看到域名规则的 IPv4、IPv6 学习集合为 **0／0**。这时，目的 IP 若也不在静态集合里，就不会命中这三条 AI 阻断规则。 [域名增量及回读清单](unifi-claude-domain-review-2026-11-18.md) · [v0.1.14 发布页](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.14)

### 现场核对结果

| 层级 | 当前证据 | 完整性判断 |
| --- | --- | --- |
| 策略 | 三条 Internal → External 的 Block 规则均已启用，索引为 10000–10002。控制器排序符合预期，双栈目标 DROP 都在该链中的 ACCEPT 之前 | 预定范围的规则已加载 |
| 静态 IPv4 | 426 项，包含 423 个 Voice 地址和 3 个 Anthropic 目的网段。控制器、内核集合及 v0.1.14 一致 | 对 v0.1.14 的静态目的 IPv4 清单完整 |
| 静态 IPv6 | `2607:6bc0::/32`。控制器、内核集合及 v0.1.14 一致，采样时其 DROP 计数为 973 个数据包 | 对 v0.1.14 的静态目的 IPv6 清单完整 |
| 静态域名表 | 90 条均已写入 dnsmasq 的双栈学习配置，包含新增 9 项和截图全部 17 项 | 截图清单完整 |
| 动态域名地址 | IPv4 与 IPv6 集合两次读回均为空，域名 DROP 计数为 0 | 采样时域名规则没有可供匹配的目的 IP |

静态目的 IPv4 的 3 个网段为 `34.8.0.0/16`、`153.61.224.0/22` 和 `160.79.104.0/21`。独立的 Anthropic 来源集合不计入目的清单。`160.79.104.0/21` 在目的规则中也有独立定义，因此 UniFi 静态 IPv4 表包含这一段。 [当前 UniFi 配置说明](unifi.md) · [v0.1.14 目的规则](https://github.com/YouM1225-1/sing-box-ai/blob/v0.1.14/artifacts/v0.1.14/anthropic.json)

### 清单相对 v0.1.14 的差异

将两份目的规则中的精确域名和后缀去重后，可直接导出 67 个域名。现有 UniFi 表按根域和子域匹配覆盖 **65／67**。缺少 `stripe.com` 与 `usefathom.com` 的整域后缀，现有表保留了部分 Stripe 主机和 `cdn.usefathom.com`。补整域会扩大到这些服务的其他用途。

有限静态域名表也无法等价复刻 Anthropic 的 6 个关键词 `anthropic`、`claude`、`browser-intake`、`datadog`、`sentry`、`sift`，以及 OpenAI 的 1 条 Azure Web PubSub 主机名正则。补入截图 9 项后，其他仅靠这些表达式命中的主机仍可能不在 UniFi 域名范围内。`github.com`、`api.github.com` 和 `raw.githubusercontent.com` 在当前静态表里。 [导出逻辑](../scripts/export_unifi.py) · [v0.1.14 OpenAI 规则](https://github.com/YouM1225-1/sing-box-ai/blob/v0.1.14/artifacts/v0.1.14/openai.json)

### 运行时缺口

- **域名下发只建立学习规则。** dnsmasq 在处理匹配域名或子域的查询时，把解析到的地址加入集合。设备持有缓存 IP、由 N100 处理 DNS 或直接使用外部 DNS 时，UniFi 可能没有学到设备实际使用的地址。防火墙在这里按目的 IP 检查。 [dnsmasq 手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)
- **当前网络下发确实存在两条不同的 DNS 路径。** 主网 DHCP 仍将 N100 下发为 IPv4 默认网关，IPv6 DNS 也指向 N100。LoT 的 IPv4 DHCP 将 UniFi 下发为默认网关，DNS 指向外部解析器。因此，网络包经 UniFi 转发时，网关的 dnsmasq 仍可能没有处理对应查询。N100 整机停机后，各客户端是否回退到 UniFi 取决于当时的网关与路由状态。
- **已有实际漏拦样本。** 11 月 11 日的 33 个无应用数据 TCP 探针中，已学习地址和静态地址样本命中 DROP。N100 DNS 当时返回的两个 `api.openai.com` 地址和一个 `github.com` 地址则从 WAN 发出 SYN 并收到 SYN-ACK。这三个历史地址在本次读取的静态及动态集合中仍无匹配。本次未重发探针，历史地址也不能代表这两个域名现在的全部地址。
- **预解析只能提供当时的地址覆盖。** 11 月 11 日受限预解析后，动态集合曾有 73 个 IPv4 和 3 个 IPv6 成员。本次两次读回均为 0／0，现有证据无法判断清空原因或时间。加入 9 个名称不会让旧解析结果自动进入集合。

### 验收判断

如果目标是让 UniFi 在 N100 离线时继续阻断 **已知静态地址和网关已学到的域名地址**，三条规则已下发，静态 IP 覆盖与发布版一致。如果目标是 **清单域名在所有解析路径和回退情况下都无法直连**，目前未达到。主要差距是 UniFi 学习到的地址与客户端真正连接的地址可能不同，继续只补域名无法消除这个差距。 [UniFi 区域防火墙说明](https://help.ui.com/hc/en-us/articles/115003173168-Zone-Based-Firewalls-in-UniFi)

本次验证使用控制器读回、网关只读快照及历史流量样本。整机离线、现有连接的后续行为和重启后的学习持久性仍缺少本次流量证据。
