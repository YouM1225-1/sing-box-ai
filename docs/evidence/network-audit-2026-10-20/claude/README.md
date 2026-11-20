# Claude / Anthropic 网络覆盖核对（2026-10-20）

截至本次实际抓取，未发现 v0.1.6 对当前官方 Claude Web、Code、Desktop、Artifacts 清单中的已选择用途有域名或 API IP 漏项。44 条去重域名事实中，43 条被最终规则覆盖；唯一未覆盖的是默认未选择的可选 Gerrit 查询 `*-review.googlesource.com`。这不是所有第三方服务、任意 MCP 服务器、云平台部署和爬虫出口的无边界完整性声明。

## 与仓库快照的确切差异

| 来源 | 与 2026-09-27 原始取证记录相比 | 对规则的影响 |
| --- | --- | --- |
| Claude Code 网络清单 | 域名集合无新增、无删除；页面内容及 SHA 已变化 | 不需要新增域名 |
| Claude Desktop 网络清单 | 精简通配符的备选清单删除 `a-cdn.claude.ai`；没有新增域名 | `claude.ai` 根后缀仍覆盖该域名；不据此判定域名停用 |
| Claude API IP 页面 | 原始响应 SHA 完全相同 | 入站两段、出站一段不变 |
| RIPE AS399358 | 当前 3 个公告前缀与仓库 2026-10-15 记录一致 | 全部被现有目的地址 CIDR 覆盖 |

`code.claude.com` 没有出现在 `sources/official/claude-code.json` 的归一化 facts 中，但它已经出现在同日期的原始 `source-records/claude-code.json` 中，并始终被 `claude.com` 后缀覆盖。因此它是 facts 记录可补齐的条目，不能算作新发现的域名或成品规则漏项。

## 必需、功能相关与可选依赖

- Code 的登录、API、MCP 代理、下载、Chrome bridge、Artifacts 一方主机均由现有根后缀覆盖。
- GitHub、npm、Google Storage 和 Homebrew 主机是安装、插件、更新或特定功能相关的共享依赖；现有精确规则已覆盖。它们不应被描述成 Anthropic 独有基础设施。
- Artifacts 的 5 个外部 JavaScript 库主机全部精确匹配；可选的两个 Google Fonts 主机也已覆盖。
- 两个 Datadog 遥测主机由 `domain_keyword: datadog` 覆盖。此关键词不是精准服务边界，可能同时匹配其他厂商域名；它是现有显式策略，不是本次建议扩宽的范围。
- Gerrit 查询仅涉及受信任 `googlesource.com` 工作区的 Desktop Code 会话，可通过关闭非必要流量停用。该可选正则当前未选择；若未来要求覆盖这项功能，应另行选择精确范围，而非加入整个 `googlesource.com`。
- Claude Help Center 当前 HTML 实测出现 4 个 Intercom 主机，均被现有规则覆盖。这里只核对直接 HTML 依赖，没有重放登录态或完整 JS 运行时；旧记录中的 `js.intercomcdn.com` 未在本次 HTML 直接出现，不代表已停用，且仍被后缀覆盖。

## IP 方向与范围

| 事实 | 当前官方值 | v0.1.6 对应规则 | 结论 |
| --- | --- | --- | --- |
| 客户端连接官方 API 的 IPv4 目的地址 | `160.79.104.0/23` | `anthropic.json` 的 `ip_cidr: 160.79.104.0/21` | 包含 |
| 客户端连接官方 API 的 IPv6 目的地址 | `2607:6bc0::/48` | `anthropic.json` 的 `ip_cidr: 2607:6bc0::/32` | 包含 |
| Anthropic 服务对外请求的源地址 | `160.79.104.0/21` | `anthropic-ip.json` 的 `source_ip_cidr: 160.79.104.0/21` | 相同、方向正确 |
| RIPE 另一个可见公告前缀 | `2607:6bc0:11::/48` | `ip_cidr: 2607:6bc0::/32` | 包含；公告本身不证明具体服务用途 |

现有目的地址 `/21` 与 `/32` 比官方 API 入站范围更宽，是仓库已选择的网络覆盖范围。不能借官方出站 `/21` 证明客户端 API 需要整个目的 `/21`，也不能将 AS 公告或地址归属解释成每个地址都运行 Claude 服务。

官方已淘汰的 `34.162.46.92/32`、`34.162.102.82/32`、`34.162.136.91/32`、`34.162.142.92/32`、`34.162.183.95/32` 均未出现在当前源地址或目的地址规则中。

官方页面明确区分 Claude Platform on AWS：其 `aws-external-anthropic.{region}.api.aws` 入站使用 AWS 地址范围，不属于上述 Anthropic API 两段。是否支持 Bedrock、AWS Platform、Google Cloud、Microsoft Foundry、企业网关或用户配置 MCP，应按实际部署单独定义；本次没有将整段 AWS、Google、Azure 共享网络并入 Claude 规则。

官方爬虫 JSON 存在于 `https://claude.com/crawling/bots.json`，当前声明创建时间为 `2026-10-07T00:00:00Z`、包含 38 个 IPv4 前缀。其用途是识别 ClaudeBot、Claude-User、Claude-SearchBot 对网站的请求来源，不能作为客户端目的路由清单；也不等同于 API IP 页面规定的服务出站 `/21`。本次仅记录方向与范围，不将爬虫清单并入现有成品。

## 当前域名事实与匹配依据

下面的计数包含官方同时提供的通配符方案与具体主机备选方案，不能理解为 44 个独立必需服务。`domain_suffix` 的无点根域形式覆盖根域和所有子域；带点的候选表示官方通配符要求。匹配使用仓库 `scripts.common.covered` 的实际语义，原生 SRS 见证由汇总审计统一执行。

| 官方值 / 实测主机 | 用途范围 | 当前覆盖规则 |
| --- | --- | --- |
| `*-review.googlesource.com` | optional | 未选入：可选 Gerrit 查询 |
| `*.frame.claudeusercontent.com` | feature-dependent | domain_suffix `claudeusercontent.com` |
| `api.anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `bridge.claudeusercontent.com` | feature-dependent | domain_suffix `claudeusercontent.com` |
| `browser-intake-us5-datadoghq.com` | optional | domain_keyword `datadog` |
| `claude.ai` | desktop-network-host | domain_suffix `claude.ai` |
| `claude.com` | desktop-network-host | domain_suffix `claude.com` |
| `code.claude.com` | feature-dependent | domain_suffix `claude.com` |
| `downloads.claude.ai` | desktop-network-host | domain_suffix `claude.ai` |
| `formulae.brew.sh` | feature-dependent | domain `formulae.brew.sh` |
| `github.com` | feature-dependent | domain `github.com` |
| `http-intake.logs.us5.datadoghq.com` | optional | domain_keyword `datadog` |
| `mcp-proxy.anthropic.com` | feature-dependent | domain_suffix `anthropic.com` |
| `platform.claude.com` | desktop-network-host | domain_suffix `claude.com` |
| `raw.githubusercontent.com` | feature-dependent | domain `raw.githubusercontent.com` |
| `registry.npmjs.org` | feature-dependent | domain `registry.npmjs.org` |
| `storage.googleapis.com` | feature-dependent | domain `storage.googleapis.com` |
| `*.anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `*.claude.ai` | desktop-network-host | domain_suffix `claude.ai` |
| `*.claude.app` | desktop-network-host | domain_suffix `claude.app` |
| `*.claude.com` | desktop-network-host | domain_suffix `claude.com` |
| `*.claudemcpcontent.com` | desktop-network-host | domain_suffix `claudemcpcontent.com` |
| `*.claudeusercontent.com` | desktop-network-host | domain_suffix `claudeusercontent.com` |
| `*.livepreview.claude.ai` | desktop-network-host | domain_suffix `claude.ai` |
| `*.livepreview.claude.app` | desktop-network-host | domain_suffix `claude.app` |
| `a-api.anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `a-cdn.anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `a.claude.ai` | desktop-network-host | domain_suffix `claude.ai` |
| `anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `assets-proxy.anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `assets.claude.ai` | desktop-network-host | domain_suffix `claude.ai` |
| `claude.app` | desktop-network-host | domain_suffix `claude.app` |
| `s-cdn.anthropic.com` | desktop-network-host | domain_suffix `anthropic.com` |
| `cdnjs.cloudflare.com` | artifact-library | domain `cdnjs.cloudflare.com` |
| `cdn.jsdelivr.net` | artifact-library | domain `cdn.jsdelivr.net` |
| `cdn.tailwindcss.com` | artifact-library | domain `cdn.tailwindcss.com` |
| `code.jquery.com` | artifact-library | domain `code.jquery.com` |
| `unpkg.com` | artifact-library | domain `unpkg.com` |
| `fonts.googleapis.com` | optional-font | domain `fonts.googleapis.com` |
| `fonts.gstatic.com` | optional-font | domain `fonts.gstatic.com` |
| `api-iam.intercom.io` | observed-optional-support-widget | domain_suffix `intercom.io` |
| `downloads.intercomcdn.com` | observed-optional-support-widget | domain_suffix `intercomcdn.com` |
| `static.intercomassets.com` | observed-optional-support-widget | domain `static.intercomassets.com` |
| `widget.intercom.io` | observed-optional-support-widget | domain_suffix `intercom.io` |

## 证据、时间与限制

| 来源 | 实际抓取时间（UTC） | 状态 | 本地证据 |
| --- | --- | --- | --- |
| [Claude Code 网络配置](https://code.claude.com/docs/en/network-config.md) | 2026-10-20T15:41:50.663548+00:00 | HTTP 200 | [network-config.json](network-config.json) |
| [Claude Desktop 网络要求](https://code.claude.com/docs/en/desktop.md) | 2026-10-20T15:41:50.663875+00:00 | HTTP 200 | [desktop.json](desktop.json) |
| [Claude API IP](https://platform.claude.com/docs/en/api/ip-addresses.md) | 2026-10-20T15:41:50.664039+00:00 | HTTP 200 | [ip-addresses.json](ip-addresses.json) |
| [RIPE AS399358 公告](https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS399358) | 2026-10-20T15:41:50.664146+00:00 | HTTP 200 | [announced-prefixes.json](announced-prefixes.json) |
| [Claude Help Center 页面依赖](https://support.claude.com/en/) | 2026-10-20T15:41:50.664244+00:00 | HTTP 200 | [support.json](support.json) |
| [官方爬虫说明](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) | 2026-10-20T15:42:53.696433+00:00 | HTTP 200 | [crawler-doc.json](crawler-doc.json) |
| [官方爬虫 JSON](https://claude.com/crawling/bots.json) | 2026-10-20T15:42:53.696113+00:00 | HTTP 200 | [crawler-json.json](crawler-json.json) |

[coverage.json](coverage.json) 保存逐条覆盖结果、CIDR 包含关系和最终产物 SHA；[native-domain-targets.txt](native-domain-targets.txt) 供成品 SRS 匹配见证使用。45 个见证目标中，`audit-review.googlesource.com` 是预期不匹配的可选 Gerrit 反例，其余预期匹配。

页面没有可验证的绝对更新时间，因此“本次抓取内容”与“官方在某日更新”分开表述。网络清单与已有原始事实做集合比较；页面总 SHA 变化只能证明页面内容变化，不能单独证明域名变化。RIPE 记录最新数据时间为 `2026-10-20T08:00:00`，是该观测窗口的路由视图，无法保证所有观察点及未来地址完整性。本次没有做所有地区、账号功能、登录流程及用户连接器的运行时抓包。

本次仅写入本证据目录，没有修改 `sources/`、`artifacts/`、`dist/` 或发布。原始文档正文没有随证据再分发；保留 HTTP 元数据、响应摘要、互操作所需域名/IP 事实和定位信息。

Graft：本子任务 1 次调用，工具报告节省 29,391 tokens；不将其他任务的节省量合并，不折算金额。
