# Claude 规则补齐结果

> 本文保留候选完成时的分析记录。该候选已依据后续 VPS 验证于 2026-10-09 晋升为正式 `v0.1.3` 并发布为 Latest，见[最终发布报告](evidence/release-v0.1.3/README.md)。

日期：2026-10-09（Asia/Shanghai）

采用口径：用户已选择 **“核验用途后补齐”**。

修改前基线：`v0.1.2`；新工作树与候选：`v0.1.3-rc.1`。

**已补入 7 个有用途证据的精确主机：2 个 Claude Code 可选遥测主机、5 个帮助中心/客服主机。** 新规则已编译并通过 **2,164 项原生匹配校验、47 项完整回归测试**。Claude 产物由 14 个增至 **21 个精确域名**，另保留 9 个域名后缀、2 个目的 IP 前缀。

本次完成的是仓库规则源和本地候选批次。新候选在 [artifacts/v0.1.3-rc.1](../artifacts/v0.1.3-rc.1/manifest.json)，`publication_approval` 为空；正式 `dist/` 仍对应既有 `v0.1.2`。没有提交、推送、发布或修改实际客户端配置。

导航：[新增清单](#added) · [原始规则逐项结论](#comparison) · [IP 取舍](#ip) · [实现与验证](#verification) · [文件入口与复现](#files)

<a id="added"></a>
## 新增清单及用途

| 精确主机 | 本次处理 | 证据和用途 |
|---|---|---|
| `http-intake.logs.us5.datadoghq.com` | 启用已有 optional | Claude Code 官方网络表中的可选运行遥测入口。 |
| `browser-intake-us5-datadoghq.com` | 启用已有 optional | 同一官方表中的可选错误报告入口；是否发送仍取决于客户端设置与服务端条件。 |
| `api-iam.intercom.io` | 新增并启用 optional | 官方帮助首页 messenger 配置的 `app.apiBase`。 |
| `widget.intercom.io` | 新增并启用 optional | 同页 `app.messengerUrl` 指向 Anthropic 对应的 widget loader。 |
| `js.intercomcdn.com` | 新增并启用 optional | 上述 loader 用此地址作为动态脚本加载前缀。 |
| `downloads.intercomcdn.com` | 新增并启用 optional | 官方帮助页 logo 与栏目图片的实际 `img src` 主机。 |
| `static.intercomassets.com` | 新增并启用 optional | 官方帮助页 JS/CSS 的实际 `script src`、`link href` 主机。 |

两个遥测主机由当前[Claude Code 官方网络要求](https://code.claude.com/docs/en/network-config#network-access-requirements)明确列出。本次只是选择已有 optional 规则，不会更改客户端的遥测开关；也不将遥测写成登录或推理的必需条件。

五个客服主机来自[Claude 官方帮助首页](https://support.claude.com/en/)及其链接的[Intercom widget loader](https://widget.intercom.io/widget/lupk8zyo)。这是第一方页面及其依赖脚本的静态证据，不是登录后抓包或真实客服会话成功证明。它们标注为 `claude-support`，`optional` 表示仓库选择覆盖帮助中心/客服功能，不表示厂商发布过对应强制网络白名单。

以上全部使用 `domain` 精确匹配。没有扩展为 `datadog` 关键词、`intercom.io` 或 `intercomcdn.com` 整后缀。域名规则不能区分请求来自哪个应用，因此其他软件访问相同共享主机时也可能命中该规则集，实际出口仍由消费者路由决定。

<a id="comparison"></a>
## 对原始域名规则的逐项结论

下面以新候选 `anthropic.srs` 为口径。“部分”表示只收录了已核验的具体主机，故意不复刻更大的后缀/关键词范围。

| 原始要求 | 新候选结果 | 分析与处理 |
|---|---|---|
| 后缀 `anthropic.com` | 完整覆盖 | 原有核心后缀保留。 |
| 后缀 `claude.ai` | 完整覆盖 | 原有核心后缀保留。 |
| 后缀 `claude.com` | 完整覆盖 | 原有核心后缀保留。 |
| 后缀 `clau.de` | 完整覆盖 | 原有核心后缀保留。 |
| 后缀 `claudemcpclient.com` | 完整覆盖 | 原有核心后缀保留。 |
| 后缀 `claudeusercontent.com` | 完整覆盖 | 原有核心后缀保留。 |
| 精确 `servd-anthropic-website.b-cdn.net` | 完整覆盖 | 原有 CDN 精确规则保留。 |
| 精确 `anthropic.com.cdn.cloudflare.net` | 未加入 | 本次未取得当前客户端依赖证据；不能按名称或可能的历史 CNAME 推断。 |
| 精确 `anthropic.auth0.com` | 未加入 | 当前官方认证表列出 `claude.ai`、`claude.com`、`platform.claude.com`；没有证实这个第三方旧主机仍需访问。 |
| 精确 `anthropic-com.ghost.io` | 未加入 | 未取得当前客户端依赖证据。 |
| 后缀 `sentry.io` | 未加入 | 厂商关联本身不足以确定 Claude 客户端的具体入口，更不能支持整个共享后缀。 |
| 后缀 `statsigapi.net` | 未加入 | 供应商文档和历史规则不能证明当前 Claude 使用；自有 `statsig.anthropic.com` 已由核心后缀覆盖。 |
| 精确 `browser-intake-us5-datadoghq.com` | **本轮补齐** | 当前官方文档明确列出，已启用。 |
| 关键词 `datadog` | **部分，按具体主机补齐** | 已纳入上述两个已证实入口，不匹配任意含此字符串的主机。 |
| 关键词 `sift` | 未加入 | 未取得当前客户端依赖证据，也没有确定的具体目标主机。 |
| 后缀 `intercom.io` | **部分，按客服主机补齐** | 仅 `api-iam.intercom.io`、`widget.intercom.io`。 |
| 后缀 `intercomcdn.com` | **部分，按客服主机补齐** | 仅 `js.intercomcdn.com`、`downloads.intercomcdn.com`；另补入已观察到的 `static.intercomassets.com`。 |
| 精确 `cdn.usefathom.com` | 继续候选、未启用 | 只有历史/社区与供应商通用用途线索；现有 pending 记录保留。 |

按原始 18 条规则的完整范围计算，新候选为 **8 条完整、3 条部分、7 条未加入**。这与用户选择的用途核验口径一致，不能描述成“原配置逐条完全等价”。

本次公开资料研究中，匿名访问 `claude.ai` 返回 403，因此没有检查其登录后页面。“未取得证据”不等于证明已停用。没有将候选改标为已验证，也没有将修改授权写成运行验证记录。

<a id="ip"></a>
## IP 与 ASN 的取舍

2026-10-09 重新取得的[官方 IP 地址文档](https://platform.claude.com/docs/en/api/ip-addresses)仍区分：

| 用途 | 正确保留的范围 | 对用户原配置的处理 |
|---|---|---|
| 客户端访问 Anthropic 的目的 IPv4 | `160.79.104.0/23` | 不扩大为目的 `/21`。 |
| 客户端访问 Anthropic 的目的 IPv6 | `2607:6bc0::/48` | 不扩大为目的 `/32`。 |
| Anthropic 发出请求时的来源 IPv4 | `160.79.104.0/21` | 继续放在独立 `anthropic-ip.srs` 的 `source_ip_cidr`。 |
| `AS399358` 全量兜底 | 未新增 | 官方列出的目的前缀不能证明整个 ASN 都应该作为客户端目的范围。 |

按保留的较小范围，`160.79.106.1`、`2607:6bc0:1::1` 不会被这两条 Claude 目的 IP 规则命中；IPv4 `/21` 的来源语义保留。边界测试检查较大目的前缀没有被引入。两个目的 CIDR 已在 `anthropic.srs` 内，不另造重复目的 IP 文件。

原配置中的 `bypass-system`、私网/本地 `skip-proxy`、`CLAUDE0409 = direct` 和 `no-resolve` 属于消费者设置，本次产品规则补充不对这些行为作等价声明。

<a id="verification"></a>
## 实现与验证

实现复用现有生成与校验链路，没有修改生成器或校验器：

- `VERSION` 更新为 `0.1.3-rc.1`。
- `sources/policy.yaml` 启用 7 个新选项，加上原有两个字体主机，共 9 个 optional exact；pending 仍为空。
- `sources/anthropic.yaml` 新增 5 条客服精确规则，两个 Datadog 源项沿用原登记。
- 新增 `claude-support` 的官方页面事实与来源记录，并在上游登记中绑定 SHA-256。
- 新增本轮分析证据、范围边界回归，更新正式方案的工作树/已发布版本区分。

| 验证 | 结果 |
|---|---|
| 原生 source JSON / SRS 匹配测试 | **2,164 项，0 失败**。 |
| 完整单元与对抗回归 | **47 项通过，0 失败、0 跳过**。 |
| 原生反编译与独立重新编译 | 语义一致，重新编译字节一致。 |
| sing-box 隔离配置加载 | 通过，不创建业务监听或部署。 |
| 增量检查 | 只新增 7 个 Claude exact，无域名删除，后缀与 IP 不变。 |
| 范围边界 | 新增主机命中；其子域、伪后缀、Intercom 根/兄弟域不扩入，宽泛关键词不启用。 |
| 其他产品 | OpenAI 与独立 Anthropic 来源 JSON/SRS 均与 `v0.1.2` 逐字节一致。 |
| 输入身份 | 新候选 manifest 的输入哈希与当前工作树一致；它记录的是未提交工作树输入，不宣称完整提交绑定。 |
| 独立复审 | 来源、分类、哈希和精确匹配范围未发现实质问题。 |

运行校验时先修正了 Go 可执行文件的相对路径，再显式使用仓库现有的固定版本模块缓存；最终离线校验通过。没有更换依赖版本或放宽校验。初始调用错误与最终结果均保存在证据目录。

**验证层级是本地静态制品、原生匹配和隔离加载。** 没有证明登录、聊天、客服、客户端出口或现网部署成功。候选仍为 `publication_approval: null`、`validated_consumers: []`、`integration_evidence: []`、`deployment_status: pending`。

<a id="files"></a>
## 文件入口与复现

| 文件 | 用途 |
|---|---|
| [候选 Claude JSON](../artifacts/v0.1.3-rc.1/anthropic.json) | 查看完整域名与 IP 列表。 |
| [候选 Claude SRS](../artifacts/v0.1.3-rc.1/anthropic.srs) | 新编译的二进制规则，尚未正式发布。 |
| [候选 manifest](../artifacts/v0.1.3-rc.1/manifest.json) | 输入身份、来源、编译器与验证结果。 |
| [SHA256SUMS](../artifacts/v0.1.3-rc.1/SHA256SUMS) | 整批文件摘要。 |
| [本轮规则分析证据](../sources/evidence/claude-rule-review-2026-10-09.json) | 取得时间、来源、新增及未采用范围。 |
| [客服原始来源事实](../sources/official/source-records/claude-support.json) | HTML/JSON/脚本定位和原始响应摘要。 |
| [验证结果](evidence/claude-rule-review-2026-10-09/results.json) | 增量、产物摘要、测试与身份检查。 |
| [完整测试日志](evidence/claude-rule-review-2026-10-09/unit-tests.log) | 47 项完整回归结果。 |
| [原生校验日志](evidence/claude-rule-review-2026-10-09/validate.log) | 2,164 项匹配结果摘要。 |
| [修改前检查报告](claude-rule-coverage-2026-10-09.md) | `v0.1.2` 的原始差异基线。 |

新 `anthropic.srs`：**462 字节**，SHA-256：

```text
a34483911551a44160e394555d2a62a199e423d16e7ae544da7a0ef1dc57946e
```

在仓库根目录、已有固定工具与模块缓存的环境中，可用尚不存在的新目录复现：

```sh
export PATH="$PWD/.tools/go1.27.1-restored/go/bin:$PATH"
export GOMODCACHE="$PWD/.tools/gomodcache"
export GOCACHE="$PWD/.tools/gocache"
python3 scripts/generate.py --mode candidate --review-as-of 2026-10-09 --output build/claude-review-rebuild
python3 scripts/validate.py build/claude-review-rebuild --go "$(command -v go)"
SINGBOX_TEST_BATCH=build/claude-review-rebuild python3 -m unittest discover -s tests -v
```

本文件提供工作区原生预览入口；未将其上传或公开发布。
