# Claude 身份验证网络错误与分流规则的关系

核对日期：2026-10-30。对象：用户截图中的 Government ID 页面及“网络问题，请重试”提示；当前 sing-box-ai v0.1.8 发布规则。

**结论：存在与身份验证相关的明确域名覆盖缺口，值得优先排查，但尚未证实它导致本次错误。** 当前 Claude 规则覆盖 `anthropic.com`，没有覆盖 Persona 的 `withpersona.com`。验证请求若因此落入直连、其他代理或拦截规则，可能出现主页面已打开、验证步骤却报网络错误的情况。如果其余规则已把 Persona 正确送往可用出口，这个缺口也可能完全不影响访问。

## 1. 为什么 Persona 与这张截图有关

Claude 官方明确说明其身份验证合作方是 Persona，证件及自拍由 Persona 收集和保存。因此，核查验证流程不能只看 Anthropic 自有域名，还应检查 Persona 的网络依赖。官方资料确认的是服务关系；截图没有请求日志，不能确定当时失败的具体主机或接口。[Claude 身份验证说明](https://support.claude.com/en/articles/14328960-identity-verification-on-claude)

Persona 官方网络放行清单包括下表中的 11 个域名，以及客户自定义的 `withpersona.com` 子域。它是通用清单，并不表示每次 Claude 验证都会请求其中每一项。[Persona 网络放行清单](https://docs.withpersona.com/security)

截图地址栏左侧被截断。本次使用 `portal.anthropic.com` 作为候选主机进行匹配检查，不把它当作已从浏览器日志确认的完整地址。凡真正属于 `anthropic.com` 的子域，现有同名后缀规则均已覆盖。

## 2. 当前发布规则的实际检查结果

本次在线查询 GitHub Latest 为 **v0.1.8**，重新下载该版本的 `anthropic.srs`，与本地发布归档逐字节一致。使用本地 sing-box **1.15.0-alpha.9** 原生二进制匹配器，对 Claude、OpenAI 两份规则各测试 15 个域名，共 **30 次检查**。此版本是测试工具版本，不能据此推断 iPhone 或路由器正在使用的内核版本。

| 域名 | Claude 规则 | OpenAI 规则 |
| --- | --- | --- |
| `withpersona.com` | 未命中 | 未命中 |
| `app.withpersona.com` | 未命中 | 未命中 |
| `cdn.withpersona.com` | 未命中 | 未命中 |
| `docs.withpersona.com` | 未命中 | 未命中 |
| `inquiry.withpersona.com` | 未命中 | 未命中 |
| `miniapp.withpersona.com` | 未命中 | 未命中 |
| `sdk.withpersona.com` | 未命中 | 未命中 |
| `status.withpersona.com` | 未命中 | 未命中 |
| `t.withpersona.com` | 未命中 | 未命中 |
| `webrtc-consumer.withpersona.com` | 未命中 | 未命中 |
| `webrtc-stun.withpersona.com` | 未命中 | 未命中 |

Claude 规则的对照项 `portal.anthropic.com`、`api.anthropic.com`、`claude.ai`、`api3.siftscience.com` 全部命中。Sift 已由 `sift` 关键词覆盖，补加同一 Sift 域名不会解决 Persona 未覆盖的问题。

这些是**仅输入域名的匹配检查**，没有解析 DNS、测试目的 IP 条件，也没有测试完整消费者配置。SRS 存放匹配条件，不决定流量被代理、直连还是拒绝；未命中某一规则集不等于最终一定直连。

Claude SRS 的 SHA-256：`38aeb4b09903bb238df6f33b476a247830719d7246950edc024660dd6e112ab4`。

证据：[原始匹配输出、版本及下载校验](evidence/claude-verification-2026-10-30/match-results.json)、[本次下载的 Claude SRS](evidence/claude-verification-2026-10-30/anthropic.srs)、[Claude 可读发布规则](../artifacts/v0.1.8/anthropic.json)、[OpenAI 可读发布规则](../artifacts/v0.1.8/openai.json)。[10 月 29 日的覆盖报告](one-exit-coverage-2026-10-29.md)此前也记录了 `withpersona.com` 未覆盖。

## 3. 哪些情况下会与规则有关

| 实际情况 | 对本次错误的意义 |
| --- | --- |
| Anthropic 命中专用出口，Persona 落入直连或另一出口，且该路径连接失败 | 能解释“页面可见、验证请求失败”，需要日志确认 |
| Persona 被更靠前的拒绝规则、DNS 过滤或浏览器内容拦截器阻断 | 也可能导致流程出错；只补代理匹配不一定解除其他层的拦截 |
| Persona 的 DNS 解析超时、返回异常或连接到的地址不可达 | 需要结合 DNS 与连接错误排查；当前没有这方面实测证据 |
| Persona 已走相同可用出口，请求仍返回服务端错误或会话错误 | 域名漏收可能不是本次根因，应继续查接口状态及验证会话 |

Persona 官方也说明网络问题、广告拦截器或隐私工具可能让验证流程停住，但该说明不能证明用户启用了这些功能。[Persona 加载故障排查](https://help.withpersona.com/articles/86qHcxc3sUmu3beI1hMpHB/)

不能仅凭通用 network issues 提示认定证件被拒、账号被封，或认定“不同出口必然触发风控”。

## 4. 用户补充：两条路径均报错

用户确认：经 Wi-Fi/N100 和使用 iPhone 本机代理两种方式，都会出现同样的错误。这是用户报告的复现结果，本次未现场抓包验证。

这降低了“只由 N100 特有配置导致”的优先级，但不能直接排除分流规则。需要区分两边是否共用本项目规则、同一出口节点、DNS 或其他过滤设置；若共用，Persona 未覆盖造成的路径问题可能在两边重复出现。若手机本机代理仍通过同一 Wi-Fi 上网，两次测试也不能直接视作完全独立的网络对照。

同时，两种方式可能仍共用同一 Safari、内容拦截器及验证会话，因此浏览器侧拦截、会话失效和服务端错误仍需保留为候选原因。相同提示不能证明两次失败的是同一请求，也不能证明 Persona 漏收已经构成本次根因。

最有区分度的对照仍是：固定当前网络、节点及浏览器设置，只临时补充 Persona 域名的路由与适用 DNS 策略，并用连接日志确认它实际使用的出口，再观察原来失败的步骤。若请求已走预期出口且正常连通，但页面仍报错，应转查验证会话及具体接口响应；若客户端日志只有连接信息，不能用它代替 HTTP 响应证据。

## 5. 最有区分度的检查方法

1. **核对两条链路的共同项。** 已知 Wi-Fi/N100 与 iPhone 本机代理均能复现；继续确认客户端、内核版本、实际加载的规则及模式、出口节点，以及手机代理测试时是否仍在相同 Wi-Fi 下。当前仓库和设备实际生效配置可能不同。
2. **记录一次复现的连接信息。** 查看 Anthropic 与 `withpersona.com` 相关请求各自命中的规则、出口及错误；同时检查 DNS 或拦截日志。保留域名、时间、错误和规则即可，分享时去掉验证令牌、Cookie 和证件内容。
3. **做局部对照。** 保持网络及 Claude 使用的节点不变，临时让 `withpersona.com` 根域和子域使用同一固定出口，核对适用的 DNS 策略，并检查是否仍被更早的规则拦截。重新进入验证页面观察原网络错误是否消失，无需为测试反复提交证件。
4. **按结果归因。** 若日志显示 Persona 路径修正后请求恢复且同一步错误消失，才能较有把握归因于分流或相关过滤。单次成功仍可能受服务瞬时恢复影响。若完全无变化，应查看实际失败请求，再查会话或服务端问题。

从规则覆盖角度，候选补充是 `domain_suffix: withpersona.com`。它覆盖 Persona 的根域及子域，也会影响其他网站使用 Persona 的流量；它不是仅限 Claude 的服务。具体路由与 DNS 写法应依据实际客户端配置，不宜凭当前截图指定规则标签或顺序。[sing-box 匹配字段文档](https://sing-box.sagernet.org/configuration/rule-set/headless-rule/)

本次完成了发布规则、官方依赖和原生匹配核查；没有取得出错设备的实时配置或请求日志，没有修改分流规则或发布新版本。
