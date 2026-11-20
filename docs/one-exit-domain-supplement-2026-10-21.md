# one-exit 域名补充记录

2026-10-21，按用户在[完整对比](one-exit-b9d9f8a-comparison-2026-10-21.md)后提出的“补充”，已将上一轮列出的五个未覆盖后缀加入 Anthropic 规则，并生成、验证 **v0.1.7-rc.1 候选**。

候选补充阶段只完成了本地规则与候选产物，当时尚未提交、推送或发布，`dist/` 仍为 v0.1.6。下文候选验证结果保留该阶段的事实。

**后续发布更新：** 用户随后明确要求“发布”，`v0.1.7` 已于北京时间 **2026-10-21 14:37:32** 发布并设为 Latest，`dist/` 已更新。五个后缀现已进入正式版，三份 SRS 与本候选字节一致；现有 Latest 订阅地址继续可用，设备成功刷新后取得本版。两组下载和合计 380 项空缓存请求检查均通过，未确认实际用户设备已刷新。完整结果见[正式发布记录](evidence/release-v0.1.7/README.md)。

## 补入清单

| 域名后缀 | 本次匹配范围 | 收录身份 |
|---|---|---|
| `growthbook.io` | 根域及全部子域，包括 `cdn.growthbook.io` | 用户指定的共享服务覆盖 |
| `hcaptcha.com` | 根域及全部子域 | 用户指定的共享服务覆盖 |
| `stripe.network` | 根域及全部子域 | 用户指定的共享服务覆盖 |
| `stripecdn.com` | 根域及全部子域 | 用户指定的共享服务覆盖 |
| `segment.io` | 根域及全部子域 | 用户指定的共享服务覆盖 |

五条均使用 `domain_suffix`、目的方向、`status: user-requested`、`product: claude-website-coverage`、`shared_dependency: true`。它们会扩大这些共享服务的匹配范围，不限于 Claude 的请求；最终出站由消费者配置决定。

来源为 [one-exit 固定提交](https://github.com/wquguru/one-exit/commit/b9d9f8ab6687401f7588dfa7d7023cd58ffb4032)的差异及本次用户指令，不标为官方必需依赖，也不声称已经验证真实业务。原话“补充”与五项范围解释分别保存在[指令证据](../sources/evidence/one-exit-coverage-request-2026-10-21.json)，由[来源登记表](../sources/upstreams.yaml)固定 SHA-256。

历史 `cdn.growthbook.io` pending 记录保留且未选；现在它被新后缀覆盖，发现报告会显示 `ALREADY_COVERED`，不代表其历史证据已升级为官方或运行验证。

<a id="roles"></a>

## 五个后缀分别做什么

以下根据 2026-10-21 读取的供应商官方文档解释服务用途，不代表已证实 Claude 当前依赖这些服务。

| 后缀 | 已核实的用途 | 对使用这些服务的网站可能有什么影响 |
|---|---|---|
| `growthbook.io` | GrowthBook 提供功能开关、灰度配置和 A/B 测试；官方 JavaScript 示例从 `cdn.growthbook.io` 下载功能与实验配置 | 配置拉取失败可能影响功能开关或实验分组；是否使用缓存或默认值取决于集成方式 |
| `hcaptcha.com` | hCaptcha 提供人机验证及自动化滥用防护；官方示例加载 `js.hcaptcha.com`，服务端使用 `api.hcaptcha.com/siteverify` 校验令牌 | 如果页面实际采用 hCaptcha，资源或验证请求失败可能阻断登录、注册等受保护操作；服务端校验请求不一定经过用户设备 |
| `stripe.network` | Stripe 集成使用的配套网络域名；官方明确列出 `m.stripe.network` | 可能涉及网站的 Stripe 支付集成；官方清单未披露该子域的具体职责，不能直接认定是支付 API 或反欺诈接口 |
| `stripecdn.com` | Stripe 集成使用的配套域名；官方列出 `a`、`b`、`c`、`f.stripecdn.com` | 属于 Stripe 集成的网络访问范围；本次官方资料未逐域说明所提供的资源，不能仅凭名称断言具体用途 |
| `segment.io` | Segment 收集用户与产品事件，例如 Identify、Track、Page；官方 HTTP API 使用 `api.segment.io/v1/` | 主要影响事件上报及后续分析/数据分发；是否影响网站其他功能取决于其集成方式 |

本仓库添加这些后缀的作用是扩大 Anthropic 规则的**域名匹配范围**。例如 `growthbook.io` 与 `cdn.growthbook.io` 都会命中，`notgrowthbook.io` 和 `growthbook.io.example.org` 不会命中。命中后使用哪条出站取决于消费者配置；这些服务被其他网站使用时，同样可能匹配。规则不会自动安装 SDK、启用验证码或执行付款。

两个 Stripe 后缀需要特别保留证据边界：官方域名清单确认其与 Stripe 集成有关，但官方高级反欺诈页明确列出的风险数据地址是 `m.stripe.com`，不能把它与 `m.stripe.network` 混为一谈。官方列出几个具体子域，也不等于要求覆盖整个后缀。

官方参考：[GrowthBook JavaScript SDK](https://docs.growthbook.io/lib/js) · [hCaptcha 开发指南](https://docs.hcaptcha.com/) · [Stripe 网络域名](https://docs.stripe.com/ips#stripe-domains) · [Stripe 高级反欺诈](https://docs.stripe.com/disputes/prevention/advanced-fraud-detection) · [Segment HTTP API](https://www.twilio.com/docs/segment/connections/sources/catalog/libraries/server/http-api)。

## 与 v0.1.6 的差异

| 制品 | 变化 |
|---|---|
| Anthropic | 仅新增上述五个后缀；后缀数 **16 → 21**；精确域名 15、关键词 3、目的 CIDR 2 均不变 |
| OpenAI | 规则与 SRS 字节均不变；保留 23 个 Voice `/32` |
| Anthropic 来源 IP | 规则与 SRS 字节均不变；仍仅为来源 `160.79.104.0/21` |

原有规则完整保留。未扩大上一轮“部分覆盖”的六项，没有引入通用 `claude` / `anthropic` / `browser-intake` 关键词，也没有加入 Google、Persona、Webshare、ASN、进程或 IPv6 拒绝动作。

上一轮新增表达式并集的 17 项，在候选的两份产品规则并集中由“完整 6、部分 6、无同服务覆盖 5”变成“**完整 11、部分 6、无同服务覆盖 0**”。这是指定范围的变化，不表示 one-exit 的整个分流策略已被复制。

## 验证结果

- **2,720 项原生检查全部通过**：包含新后缀的根域、多级子域、近似域与错误父域边界，既有域名、关键词、正则和来源/目的 IP 方向检查。
- **66 项回归全部通过，无跳过**。新增独立回归对照 v0.1.6，约束“只加五个后缀”，防止旧规则丢失或另外两份产品发生变化。
- 原生反编译语义一致，独立重编译字节一致，三个本地 SRS 的 sing-box 配置加载检查通过。
- 候选阶段的旧 v0.1.6 归档与 `dist/` 保持原样；OpenAI 和 Anthropic 来源 IP 两份候选与 v0.1.6 逐字节一致。后续正式发布已更新 `dist/`，旧归档仍保留。
- 已独立复核新指令来源、登记摘要和 manifest 输入摘要。测试中的当前日期更新为 10 月 21 日，未来日期反例改为 22 日；历史日期与到期门槛保留。

机器结果见[验证摘要](evidence/one-exit-supplement-2026-10-21/validation-summary.json)，完整原生结果见[匹配记录](../artifacts/v0.1.7-rc.1/matches.jsonl)。上述检查验证静态规则与本地加载，不代表登录、支付、验证码或最终代理出口已实测。

## 候选文件

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| [anthropic.srs](../artifacts/v0.1.7-rc.1/anthropic.srs) | 529 | `38aeb4b09903bb238df6f33b476a247830719d7246950edc024660dd6e112ab4` |
| [openai.srs](../artifacts/v0.1.7-rc.1/openai.srs) | 800 | `196619631ab33a362794ef826b9bd5b8779d08c315f46a335443f3321d4dd48c` |
| [anthropic-ip.srs](../artifacts/v0.1.7-rc.1/anthropic-ip.srs) | 36 | `9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c` |

可读规则：[Anthropic JSON](../artifacts/v0.1.7-rc.1/anthropic.json) · [OpenAI JSON](../artifacts/v0.1.7-rc.1/openai.json) · [来源 IP JSON](../artifacts/v0.1.7-rc.1/anthropic-ip.json)。批次信息：[manifest](../artifacts/v0.1.7-rc.1/manifest.json) · [摘要清单](../artifacts/v0.1.7-rc.1/SHA256SUMS)。

候选 `build_mode=candidate`、`publication_approval=null`、`validated_consumers=[]`、`deployment_status=pending`。manifest 的 `source_commit` 标识工作树基础提交，实际候选输入由 `inputs` 摘要固定，不冒称已提交的正式发行。
