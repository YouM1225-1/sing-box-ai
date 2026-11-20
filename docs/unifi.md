# UniFi 域名与目的 IP 列表

> 2026-11-18，网关的 `AI-DirectBlock-Domains` 在原 81 条基线上分批追加截图域名和共享依赖。最近一次追加 7 条 Datadog 与 Sentry 规则后，控制器读回和网关下发均为 101 条。本文下方的导出文件与条目数记录 2026-11-11 的原始批次。 [域名增量](unifi-claude-domain-review-2026-11-18.md) · [当前域名表与遥测域名核对](claude-datadog-unifi-coverage-2026-11-18.md)

文档修订：1.2；日期：2026-11-11。目标：UniFi Network 11.0.99 / UniFi OS 6.0.17。源规则：sing-box-ai v0.1.12；导出格式版本：1。

## 当前交付与发布状态

用户要求先验证 UniFi 访问 GitHub，不能访问时不发布、直接导入 UniFi。当前网关自身下载本仓库 GitHub Raw `VERSION` 发生连接超时；UniFi 原生外部列表预览则能取得 GitHub Raw 公共域名样本（24 条、未截断）。两条路径的结果不同，尚未证明网关定时下载可用，因此本批 **不提交、不推送、不发布 GitHub**，采用本地静态文件导入。

文件保存在本地工作树 [dist/unifi](../dist/unifi/manifest.json)，不是已上线的订阅地址。现有 v0.1.12 Release、Latest、三个 SRS 和历史归档保持原样。新增导出代码属于下一次构建输入；不得重写旧 manifest 冒充当时已经构建过这些文本。

| 文件 | 条目数 | UniFi 列表类型 | 已保存的对象名 |
|---|---:|---|---|
| [domains.txt](../dist/unifi/domains.txt) | 81 | Domain / 静态 | `AI-DirectBlock-Domains` |
| [ipv4.txt](../dist/unifi/ipv4.txt) | 426 | IPv4 Address / 静态 | `AI-DirectBlock-IPv4` |
| [ipv6.txt](../dist/unifi/ipv6.txt) | 1 | IPv6 Address / 静态 | `AI-DirectBlock-IPv6` |

[导出 manifest](../dist/unifi/manifest.json) 记录源 JSON/SRS 摘要、每份文本摘要、条目数、域名转换和全部未导出规则。三份静态列表已保存并完整读回一致。用户 2026-11-11 要求配置，并明确来源为「所有 Internal 内网」；现已创建并启用三条 Internal → External 阻断策略，原有 72 条策略和 3 个列表内容未改变。IPv4/IPv6 内核地址集合已逐项核对；域名策略采用 UniFi 原生 DNS 学习机制，配置读回通过，但不能据此宣称所有客户端缓存与外部 DNS 路径都已被阻断。用户随后明确只在 UniFi 阻断这三份清单、其他直连继续可用；N100 在线时的 sing-box 故障已有其 nftables 保护，本批不扩展全网断网或修改 N100。

## 生成范围与限制

唯一输入是同批 `openai.json` 与 `anthropic.json` 的目的规则，逐项核对源 JSON 和 SRS 与该批 manifest 的摘要；不读取 `anthropic-ip` 来源规则来生成目的列表。

- IP 保留目的集合原有范围；单地址去掉 `/32` 或 `/128`，其他 CIDR 原样保留，按地址族分开、消重、稳定排序。UTF-8、无 BOM、LF、每行一项、无注释或标题。
- 域名合并 `domain` 和 `domain_suffix`；后缀的一个前导点去掉。实机下发为 dnsmasq 的 `ipset=/domain/...`，依 DNS 查询结果学习地址；[dnsmasq 官方手册](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html) 说明它同时匹配域名与子域。因此不能视为 sing-box 精确域名的等价转换，`.ct.sendgrid.net` 去点后也扩大到 apex。未逐个域名验证实际业务。
- OpenAI 的 1 条正则及 Anthropic 的 3 个关键词（`datadog`、`sentry`、`sift`）不能无损转成有限域名表，完整原值在 manifest 的 `omitted` 中，绝不宣称全部规则已等价导出。
- 保留已批准目的宽网段 `160.79.104.0/21`、`2607:6bc0::/32`、`34.8.0.0/16`，以及 GitHub、npm、Cloudflare Challenge、Google Storage、Stripe 等共享依赖。阻断可能影响非 AI 业务，须按客户端范围审阅；不能把此表解释为官方最窄 IP 集合。
- 来源专用 `153.61.208.0/20` 不导出；`160.79.104.0/21` 出现在 IPv4 表是因为它本来也是目的规则。
- 官方覆盖核验时点为 2026-11-11：OpenAI [Voice JSON](https://openai.com/chatgpt-voice.json) 的 423 个 IPv4 全部包含、无 IPv6；它只代表 Voice。Anthropic [IP 文档](https://platform.claude.com/docs/en/api/ip-addresses) 的 inbound `160.79.104.0/23`、`153.61.224.0/22`、`2607:6bc0::/48` 全部被覆盖；不代表所有云平台或所有服务 IP。

## UniFi 导入与配置方案

在策略对象的列表页面分别创建 Domain、IPv4、IPv6 **静态**列表，将对应文本逐行导入，保存后核对上述条目数及完整集合。实际 11.0.99 前端支持三种类型；IPv4/IPv6 不要混放。控制器对地址族不符的外部预览可能返回 HTTP 200 但空列表，因此必须核对条目数、集合和截断标志，不能只看 HTTP 状态。

本次配置为以下三条独立策略，来源均为所有 Internal，目的区域 External；动作 Block、所有端口/协议、所有连接状态、始终生效。原生排序索引 10000–10002，均在系统规则之前。Internal 当前包含默认网络、LoT 和 SMB；SMB 原有外网隔离保留。规则不会自动把流量改为代理，也不覆盖 Gateway 自身发出的流量。

| 策略 | 地址族 | 当前状态 | 原生策略 ID |
|---|---|---|---|
| AI-阻断直连-IPv4 | IPv4 | 已启用；集合与 426 项源表一致 | `8e31c400-290b-4724-9f71-a9bd122470c4` |
| AI-阻断直连-IPv6 | IPv6 | 已启用；集合与 1 项源表一致 | `a445defb-5c7f-44e9-9a0c-d00b21f24451` |
| AI-阻断直连-域名 | 两个地址族 | 已启用；域名运行覆盖未验收 | `bcfbbc3e-b745-47c9-928a-74145e9667aa` |

域名策略依 UniFi DNS 查询学习目的 IP：初始 IPv4/IPv6 集合均空。对同一测试域名，UniFi DNS 返回的地址与正常 N100 路径使用的地址不同；一次 UniFi DNS 探测向其动态集合加入了 1 个 IPv4 与 1 个 IPv6。当前证据不能确定差异根因，但足以说明不能证明实际访问路径被覆盖，且共享地址存在误拦风险。未更改 DNS、DHCP、N100 或全网路由。

用户 2026-11-11 澄清用途为 N100 整机重启时的 UniFi 清单阻断，并要求不过度设计、其他直连继续可用。最终保留上表三条原生防火墙策略，不调整 N100 的 DNS / nftables，不改 DHCP / RA / DNS 上游。静态 IP 阻断只覆盖本表目的集合，域名仍受 UniFi DNS 学习机制限制。

尝试用原生 Content Filtering 单独承载 81 项域名时，Network 11.0.99 对 `categories: []` 返回 HTTP 400（`categories must not be empty`），读回列表仍空。它要求附带分类过滤，不符合本批仅清单范围，因此没有创建内容过滤策略，也没有启用广告、安全搜索或额外分类。

控制器读回、底层 DROP 和地址集合核对不代替真实直连命中测试。现有 N100 路径访问 OpenAI API 返回 401，只证明该访问样本仍可达；尚未完成绕过透明代理的受控直连、IPv6 端到端、QUIC、既有连接和重启持久化验收。

若需撤销本批，只处理上表精确 ID 并核对名称、Internal → External 方向及描述中的 `sing-box-ai v0.1.12`；在 UniFi 策略页面停用后保存，读回确认，并检查网关对应 DROP 已撤除。三个列表可保留用于后续审阅；不要修改原有策略。原生 ID 不得用于 Integration API。

## 与 SRS 同步更新

`scripts/generate.py` 在每个新批次内同时生成 `unifi/` 四个文件；`scripts/validate.py` 从同批 JSON 独立重算并逐字节校验，漏更新、额外文件或篡改都会失败。原三个 SRS 的输出和发布授权契约保持不变。

从已经验收归档的正式批次补导出时，在仓库根的 Bash 运行以下本地命令。它先验证候选与 VERSION、正式归档、dist SRS 一致，再替换本地 `dist/unifi`；不连接 UniFi、不提交或发布。旧归档和三份 `dist/*.srs` 必须已与 `VERSION` 一致。生成失败停止，检查通过后再按用户授权导入现场。不得并发运行本块；进程被 SIGKILL 或断电时 trap 无法执行，先检查打印的工作目录：存在 `previous` 时保留它并恢复到 `dist/unifi`，不能直接删除工作目录后重跑。

```bash
set -eu
mkdir -p build
unifi_work=$(mktemp -d build/unifi-export.XXXXXX)
printf 'UniFi 临时目录：%s\n' "$unifi_work"
unifi_committed=0
unifi_installed=0
unifi_cleanup() {
  if [ "$unifi_committed" = 0 ]; then
    if [ "$unifi_installed" = 1 ]; then rm -rf dist/unifi; fi
    if [ -d "${unifi_work}/previous" ]; then
      mv "${unifi_work}/previous" dist/unifi || return 1
    fi
  fi
  rm -rf "$unifi_work"
}
trap unifi_cleanup EXIT
trap 'exit 1' HUP INT TERM
unifi_version=$(cat VERSION)
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_unifi.py \
  --batch "artifacts/v${unifi_version}" --output "${unifi_work}/unifi"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_unifi.py \
  --check-current --output "${unifi_work}/unifi"
if [ -e dist/unifi ]; then mv dist/unifi "${unifi_work}/previous"; fi
unifi_installed=1
mv "${unifi_work}/unifi" dist/unifi
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_unifi.py --check-current
unifi_committed=1
```

每次规则变更同批更新源制品、四份派生文件、本文条目数/版本和验证状态；运行 `tests/test_unifi.py`，同时用新生成且已验证的 candidate fixture 跑完整回归。`--check-current` 比对当前 VERSION、正式归档、dist SRS 和文本，可发现更新 SRS 后漏同步文本。静态列表没有自动订阅，UniFi 现场仍需按授权手动替换三份内容并读回比较；本地检查不能替代现场同步。

若今后改为外部订阅，先从网关验证目标 HTTPS 下载，再验证原生预览、非空完整集合、真实保存/引用、初次加载、定时刷新及失效行为。11.0.99 前端提供 24/48/72 小时刷新选项，默认 24 小时；本次未验证调度刷新。通过这些检查并获得该批发布授权后，才发布稳定 URL；当前不提供尚不存在的地址。

## 验证记录

导出代码完整回归 96 项（含专项 8 项）、同批候选 6,084 项原生检查曾通过；本次源文件未改，重新执行 `--check-current` 通过。前一轮兼容性测试对象已清理。本轮另创建上表三条正式策略，控制器完整读回、官方顺序查询、底层 DROP 及 IPv4/IPv6 地址集合核对通过；原有 72 条策略配置与顺序保持不变。8 个隔离事务故障场景覆盖失联回读、未知结果、顺序错误和回滚边界；不是实机故障注入。运行覆盖边界见上节。

测试发现并修正了接口差异：Integration API 的区域 ID 不能直接用于管理界面的原生 API，应在同一接口按 `zone_key` 读取；原生 Domain 对象引用读回补入空 `web_domains` 与 `web_matching_type: CUSTOM`，仅精确默认值可归一化，区域/类型/组 ID/非空条件仍须严格核对；原生 DELETE 的 204 是成功返回，之后仍须读取确认消失。Integration API 对本次原生 Domain 对象仅返回空 `domains`，不能单独据此证明引用或运行覆盖，须同时核对原生组 ID 与网关下发配置。
