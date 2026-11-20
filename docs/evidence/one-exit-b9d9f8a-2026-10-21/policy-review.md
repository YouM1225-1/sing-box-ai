# one-exit b9d9f8a：分流行为与证据边界

审阅对象：[固定提交 b9d9f8ab6687401f7588dfa7d7023cd58ffb4032](https://github.com/wquguru/one-exit/commit/b9d9f8ab6687401f7588dfa7d7023cd58ffb4032)，提交时间 2026-10-21 01:35:18 UTC。根据已保存的提交、前后文件与当前 Mihomo 规则文档进行静态分析；未执行下载的脚本、未加载三客户端配置、未进行住宅代理或 502 实测。

## 提交实际改变什么

这是三种客户端的出站策略调整，不是 OpenAI/Anthropic 官方域名或 IP 公告。提交共改 5 个文件，增加 64 行、删除 4 行。

1. 三模板把 `2607:6bc0::/48` 从住宅代理改为 `REJECT`，并新增拒绝 `2607:6bc0:11::/48`；两条放在各自新增规则列表最前面，均带 `no-resolve`。
2. 增加 `claudemcpcontent.com`；补充支付、验证码、客服与遥测供应商的后缀规则，指向 `SG_Residential`：`sentry.io`、`datadoghq.com`、`growthbook.io`、`usefathom.com`、`hcaptcha.com`、`stripe.com`、`stripe.network`、`stripecdn.com`、`intercom.io`、`intercomcdn.com`、`challenges.cloudflare.com`、`siftscience.com`、`segment.io`，另加 `browser-intake` 域名关键词。
3. Clash Party、Shadowrocket 新增 `anthropic`、`claude` 关键词；FlClash 原来已有。Shadowrocket 此次才补上 `IP-ASN,399358`，另外两模板已有。
4. 调整静态检查器，允许 IPv6 规则使用 `REJECT`，而非要求所有规则都指向住宅代理。

Google、Gmail、Persona、Webshare 等规则原来已存在；此次没有新增 OpenAI 专用规则。

完整增删和三端规则列表见 [template-rule-diff.json](template-rule-diff.json)。这是静态解析结果，不执行 JavaScript。

## 三客户端不是同一份实现

| 项目 | Clash Party | FlClash | Shadowrocket |
|---|---|---|---|
| 配置方式 | `proxies+`、`proxy-groups+`、`+rules` 覆写 | JS 增加代理/组，`pin.concat(config.rules || [])` 把规则放在原规则前 | 仅 `[Rule]` 模块；住宅节点与「代理通过」由用户在客户端设置 |
| 前后规则数 | 17 → 35 | 18 → 34 | 16 → 35 |
| 提交后域名/IP规则关系 | 与 Shadowrocket 完整列表相同 | 用关键词替代部分显式后缀，并保留额外进程匹配 | 与 Clash Party 完整列表相同 |
| 中转与住宅代理 | HTTP 住宅节点经 `Dialer-Res` url-test 组拨号 | 同左 | 模块本身不创建住宅节点或中转链；须人工配置 |
| 进程规则 | 无 | Claude、Google Play、Google Wallet 的 Android 包名 | 无 |

FlClash 独有 `DOMAIN-KEYWORD,modelcontextprotocol`，而另外两端只对 `modelcontextprotocol.io` 使用后缀匹配。FlClash 没有另外两端的显式 `anthropic.com`、`claude.ai`、`claude.com`、`claudeusercontent.com` 后缀，但其 `anthropic`、`claude` 关键词会覆盖这些域，并扩展到任何含对应字符串的其他域。

FlClash 的三个 `PROCESS-NAME` 是 `com.anthropic.claude`、`com.android.vending`、`com.google.android.apps.walletnfcrel`，本次提交前已经存在。Mihomo 文档说明 Android 可用该类型匹配包名。它依赖客户端能够识别进程/包名并捕获该连接；匹配成功时影响该应用的其他目的请求，不限于前面的已列域名，也不会覆盖更早已命中的拒绝规则。不能把 Android 进程规则解释成另外两端同样具有的能力。

来源：[Clash Party 模板](after/clash-party/override.yaml)、[FlClash 脚本文本](after/flclash/claude-google.js)、[Shadowrocket 模块](after/shadowrocket/one-exit.module)。

## 固定住宅出口能保证到哪一步

模板把匹配的流量送到同一个名为 `SG_Residential` 的 HTTP 代理，再通过 `Dialer-Res` 选择中转。中转变动与最后一跳住宅出口是两个不同层次；如住宅服务实际提供固定出口，换中转不必然改变最后出口。

但配置只包含 `<HOST>`、端口 `0`、用户名/密码占位符，无法证明真实服务供应商始终提供同一公网 IP。`url-test` 通过候选中转访问 `www.gstatic.com/generate_204`，没有验证「候选中转 → 指定住宅代理 → 每项业务目的」的整条链路。

README 的 `ipv4.webshare.io` 检查最多验证该次 Webshare 请求的 IPv4 出口；它本身已被专门规则固定，不能由这一结果推出所有 Claude、Stripe、验证或后台流量都走相同出口。规则遗漏的域、未捕获的连接、客户端未启用规则模式或不同模块优先级，仍可能走其他路径。相同出口也不能单独证明登录、付款、验证码或账户风险判断会成功。

## IPv6 REJECT 与 no-resolve 的关键限制

**拒绝两段已知 IPv6 目的，不等于关闭 Anthropic 全部 IPv6，也不等于强制应用使用 IPv4。**

- 范围仅是 `2607:6bc0::/48` 和 `2607:6bc0:11::/48`，不是整个 `2607:6bc0::/32`。其它 IPv6 地址可能落到后面的域名或 ASN 规则，继续送往住宅代理。
- `no-resolve` 的含义是：不要为了匹配目的 IP 规则主动发起 DNS 解析。Mihomo 文档明确说明，若之前已经解析出了目的 IP，带该参数的 IP 规则仍可命中。它不是「禁用 AAAA」、不是「只用 IPv4」，也不是「禁止 DNS」。
- 如果连接以域名交给本地代理，而路由阶段尚没有可匹配的真实目的 IP，首两条 IP 拒绝可能不命中，后续域名规则即可选中住宅代理。住宅 HTTP 代理收到带主机名的 CONNECT 后如何解析、是否选择 IPv6，不由这两个本地 `no-resolve` 规则保证。
- 应用拿到 IPv6 失败后，只有在有 IPv4 候选并实施重试/Happy Eyeballs 等机制时才可能改走 IPv4；IPv6 字面地址、仅 AAAA 的目标或不重试的客户端可能直接失败。`REJECT` 自身不合成 IPv4 地址，也不触发一个通用的「重写到 IPv4」流程。
- 规则靠前使其在已知目的 IP 命中时优先于后续住宅规则；但只覆盖进入该规则引擎、符合这些目的条件的连接。无法追回旁路流量或阻止远端代理内部随后选择 IPv6。

规则语义依据：[Mihomo 官方规则说明](https://wiki.metacubex.one/config/rules/#no-resolve)，本次取得的[文本](mihomo-rule-docs.txt)及[抓取记录](mihomo-rule-docs-fetch.json)。Shadowrocket 的具体 DNS/进程/模块合并行为没有在本次运行验证，不能仅因规则字符串相似就声称三端执行细节完全相同。

## 关键词、ASN 与共享后缀的范围

| 规则 | 实际范围 | 不应推导出的结论 |
|---|---|---|
| `DOMAIN-KEYWORD,claude` / `anthropic` / `browser-intake` | 域名中出现字符串即可；例如 `myclaude.example.org` 也可能命中 | 不是域名所有权验证，也不是官方完整清单 |
| `DOMAIN-SUFFIX,sentry.io`、Stripe 等共享供应商后缀 | 根域及全部子域，影响其他应用访问同供应商的连接 | 不代表全部租户都是 Claude 依赖或功能必需 |
| `DOMAIN-SUFFIX,challenges.cloudflare.com` | 该主机及其子域 | 不是整个 Cloudflare，也不是全部验证码服务 |
| `IP-ASN,399358,...,no-resolve` | 由客户端使用的 IP→ASN 数据分类目的地址；有可用目的 IP 时可匹配 | 不是来源 IP 白名单，不等同实时 BGP 查询，也不证明每个地址承载 Claude 必需服务 |
| `IP-CIDR,160.79.104.0/21,...` | 匹配客户端请求的目的地址 | 不能因为官方某列表称其为服务 outbound 地址，就当成客户端目的必需范围 |

规则本身没有证明供应商后缀、ASN、IPv6 地址完整或永不变化。共享服务范围扩大后，可以减少一部分流量换出口，但也会把其他软件的同类流量送入该住宅代理，影响带宽、延迟与可用性。

## 作者的 502 主张与能验证的事实

能验证的是：提交说明、README 和注释都称该作者的住宅代理访问 `2607:6bc0` 会返回 502；代码确实采用两段 IPv6 拒绝来绕开这种路径。

这 5 个变更文件未提供原始请求、代理响应、时间、住宅节点配置、DNS/AAAA、IPv4 对照或原生客户端测试记录。因此不能据此认定所有住宅代理或 Anthropic IPv6 全部存在同样问题，也不能确定 502 根因或本修复必然恢复业务。作者注释中的「让客户端改走 IPv4」应理解为意图，不能当作已验证结果。

检查器的能力也有限：[check_templates.py](after/scripts/check_templates.py) 第 77–89 行只要求所有遇到的 `IP-CIDR6` 规则目标为 `REJECT`；没有断言两条指定 CIDR 必须存在、必须靠前或必须带 `no-resolve`。而 `check_flclash()` 第 99–110 行只检查中转及 filter 文本，没有遍历 `pin` 中的 IPv6、域名或进程规则。不能把 `templates ok` 解释为三端 IPv4 回退、IPv6 防绕过或出口一致性的原生验收。

## 与本仓库设计的关系

本仓库 [docs/plan.md](../../plan.md) 第 273–284 行把目的匹配集合与消费者动作分开；第 323–329 行记录，现有 Anthropic 的目的 `/21`、IPv6 `/32` 及部分关键词来自 10 月 15 日用户明确授权的网页覆盖，并不是官方逐项必要性声明。

因此可借鉴这次提交对「业务和共享认证链路保持出口一致」「按具体代理能力处理 IPv6」的思路，但不能把 `REJECT`、`SG_Residential`、ASN 或进程规则当成应直接加入产品 SRS 的新域名/IP。是否拒绝 IPv6、使用什么出站、如何保证回退，属于消费者配置和实际运行验收；当前产品 SRS 保留目的范围并不等于承诺必须通过 IPv6 连接。

本次只新增本证据摘要和静态规则差异文件，未修改 sources、artifacts、dist。graft 1 次，估算节约 10,861 tokens。
