# sing-box-ai

OpenAI / ChatGPT / Codex 与 Anthropic / Claude 的 sing-box 规则源、生成器及验证工具。

项目版本 **0.1.0**，正式设计修订 **1.8**。已手动发布 [v0.1.0-rc.1 预发布验收批次](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.0-rc.1)；当前尚无已批准的 `dist/` 正式批次。

Claude 的 `challenges.cloudflare.com` 精确兼容规则已按维护者确认批准，验证日期为 **2026-09-27**（旧仓库更新日期），下次复核日期为 **2026-10-27**。原客户端和环境未提供，记录不冒充本次现场测试：[确认依据](sources/evidence/claude-challenge-confirmation.json)。

## 输出与方向

| 制品 | 用途 |
|---|---|
| `openai.srs` | OpenAI 客户端目的域名及官方 Voice 目的 IP |
| `anthropic.srs` | Claude 客户端目的域名及 Anthropic inbound IP |
| `anthropic-ip.srs` | Anthropic 服务主动发出请求的**来源 IP**；不用于客户端目的分流 |

每个 SRS 恰好一条 default rule，source / binary version 均为 2。固定编译器为 `1.15.0-alpha.9`，源码 commit、sing module、二进制与归档 SHA256 见 [tools.lock.json](tools.lock.json)。格式最低读取版本 1.10.0 不等于已验证消费者版本。

规则只负责匹配；不能保证不出现厂商正常安全验证。同一 Challenge 域名会被多个网站共用，SRS 不识别浏览器标签页归属。运行约束与验收见 [正式方案](docs/plan.md)。

## 文件入口

- `sources/openai.yaml`、`sources/anthropic.yaml`、`sources/anthropic-ip.yaml`：唯一人工维护规则源。
- `sources/policy.yaml`：功能范围、可选项、复核基准日期与逐条范围例外。
- `sources/official/`：从官方页面核对的结构化事实与 Voice 原始 JSON；不把摘要伪装为原网页。
- `sources/upstream/`：固定 DLC、派生 SRS、历史规则与 PSL 归档；URL、commit 和 SHA256 由 `sources/upstreams.yaml` 锁定。
- `scripts/bootstrap.py`：按哈希获取官方编译器；`sync.py`：只输出发现/差异；`generate.py`：生成隔离批次；`validate.py`：解析与匹配验证。
- `tests/test_pipeline.py`：元数据、复核期限、范围和输入篡改反例；`tests/harness/`：固定依赖的上游真实匹配器。
- `sources/release-review.json`：正式发布审阅与新批次集成证据状态。
- [执行计划](#执行计划)、[来源及许可证](THIRD_PARTY_NOTICES.md)。

## 本地生成与验证

运行端：macOS arm64 或 Linux amd64；普通用户；仓库根目录。需要 Python 3.9+ 和 **Go 1.27.1**。命令失败即先修复对应错误，不继续生成正式制品。仅以下准备阶段联网；不执行第三方同步源中的脚本。

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
python scripts/bootstrap.py
(cd tests/harness && GOTOOLCHAIN=local go mod download)
```

准备后，输入检查、编译和匹配验证使用本地快照与 Go module 缓存；validator 强制 `GOPROXY=off`、`GOTOOLCHAIN=local`。新机器先完成上述准备，不把开发机已有缓存当作依赖已经安装。Go module 的版本与校验和已锁定；若需独立于 Go proxy 的灾难恢复，另归档准备后的依赖缓存，当前未将整个依赖树 vendor 到仓库。

```sh
python -m unittest discover -s tests -v
python scripts/sync.py
python scripts/generate.py --mode candidate --output build/candidate
python scripts/validate.py build/candidate
SINGBOX_TEST_BATCH=build/candidate python -m unittest discover -s tests -p test_artifacts.py -v
```

成功判定：最后输出 `failures: 0`；三个 `.srs`、对应源 JSON、manifest、匹配结果位于 `build/candidate/`。生成器拒绝覆盖已有目录；再次运行时使用新的目录，例如 `build/candidate-2`。指定 `--go /absolute/path/to/go` 可使用隔离工具链，不需要修改全局 Go。

验证会检查整个归档哈希、官方基线完整性、元数据、单条 default 结构、反编译语义等价、源/二进制真实匹配、IP 来源方向、suffix 边界、已退役地址，以及第二次独立编译的字节一致性。隔离 `sing-box check` 不等于 N100 TUN、DNS 流量、实际出口或登录验收。

GitHub Actions 在 push、PR、手动触发及每天 02:17 UTC 检查。Actions 使用固定 commit 和只读权限；只上传标明 candidate 的审核附件，不改写规则、`dist/`、客户端配置或自动提交。兼容项到期会使日期检查失败。

## 手动预发布

2026-09-27 发布的 `v0.1.0-rc.1` 指向构建输入提交 `83b0049c0ce6ec3957af40b4ebb282c55e505db3`，manifest 保持 `build_mode: candidate`。本次重新执行 22 项对抗性测试与 1,330 个匹配用例，全部通过；三个 SRS 与此前审核包字节一致。发布操作在本地完成；[此前 Actions 运行](https://github.com/YouM1225-1/sing-box-ai/actions/runs/36328568237) 因账号账单问题未启动，不记为 CI 通过。

| 下载 | 内容 |
|---|---|
| [openai.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.0-rc.1/openai.srs) | OpenAI 客户端目的规则 |
| [anthropic.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.0-rc.1/anthropic.srs) | Claude 客户端目的规则 |
| [anthropic-ip.srs](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.0-rc.1/anthropic-ip.srs) | 服务请求来源 IP，不能加入客户端目的分流 |
| [manifest.json](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.0-rc.1/manifest.json) | 输入、编译器、三个制品及验证结果的哈希 |
| [完整验收包](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.0-rc.1/sing-box-ai-v0.1.0-rc.1.zip) | SRS、源 JSON、匹配结果、发现报告、测试日志及来源许可 |
| [SHA256SUMS](https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.0-rc.1/SHA256SUMS) | 上述五个附件的校验值 |

下载全部附件到同一目录后执行 `shasum -a 256 -c SHA256SUMS`，五项均应为 `OK`。使用固定版本下载地址，同时核对 manifest 的 source commit 和制品 SHA256；tag 与 Release 附件不视作不可变存储。六个公开附件已回下载并逐一比对本地字节。

预发布供受控的消费者集成验收，不写入 `dist/`，不将 `sources/release-review.json` 改为 approved。目标配置、实际出口、登录及功能验收仍待完成；本次未修改或部署 N100。临时验收使用独立配置并保留原配置与原 SRS；失败恢复原配置。满足下节全部门槛后另建正式批次，不将旧 candidate manifest 直接改名冒充正式结果。

## 更新与发布

1. 更新前固定并归档新的上游字节，审阅 `sources/upstreams.yaml` 的 SHA256 与来源。`sync.py --fetch` 仅恢复**已锁定且缺失**的归档；原始字节变化会失败，不自动追踪浮动分支。
2. `python scripts/sync.py --previous build/previous-sync.json --output build/new-sync.json` 比较发现、移除、canonical 元数据与归档哈希。新增社区条目先是 `ADD_CANDIDATE`，不会自动进入规则源。DLC include/affiliation 当前遇到即报错，必须先实现并归档闭包。
3. 修改维护数据、官方事实或兼容证据。兼容项需 `approved` 且满足复核日期关系；维护者确认可以作为有效性证据，但不能冒充自动测试或指定新批次的现场验收。`optional` 默认不纳入；默认支持 Voice、Artifact、安装和插件路径，不将其必要依赖降为可选。
4. 先生成、验证隔离候选，保留记录。生成之后输入文件发生变化时必须重建；validator 不接受旧 manifest。准备正式候选时运行：

```sh
python scripts/generate.py --mode release --output build/release
python scripts/validate.py build/release
python scripts/validate.py build/release --for-release
```

5. 最后一条另按**实际当前 UTC 日期**检查，核对所有构建输入都属于 manifest 记录的 source commit，并要求 `sources/release-review.json` 已批准、语义差异已审阅、现场证据绑定同一批次的三个制品哈希和消费者配置哈希。当前记录 pending，所以正式发布检查会停止；这不撤销已确认的 Claude Challenge 兼容规则。
6. 发布门槛全部通过后，维护者将三个 SRS 与 manifest 作为同一个 Git 提交发布，才填写客户端的固定 commit URL。仓库当前没有自动写入远端、发布或部署脚本。

首次发布之前没有上一正式批次；候选失败时保留现有客户端配置。后续更新失败时保留上一已批准提交。恢复按同一提交取回两个目的 SRS 和对应客户端配置，不能混用不同批次。

N100 接入时保留原来的四条 OpenAI/Anthropic route 规则位置与先后顺序，也不新增 AI 专用 QUIC 拒绝。完整含凭据客户端配置不存入本仓库。只有正式制品地址确定后再处理配置接入。

## 共享依赖

这些域名也服务其他应用；按域名分流会影响它们。`optional` 未单独纳入不等于被阻断，仍可能被其他已批准 suffix 覆盖。

| 制品 | 域名 / 范围 | 状态 |
|---|---|---|
| `openai` | `.ct.sendgrid.net` | `required` |
| `openai` | `.intercom.io` | `required` |
| `openai` | `.intercomcdn.com` | `required` |
| `openai` | `cdn.workos.com` | `required` |
| `openai` | `challenges.cloudflare.com` | `required` |
| `openai` | `forwarder.workos.com` | `required` |
| `openai` | `humb.apple.com` | `required` |
| `openai` | `images.workoscdn.com` | `required` |
| `openai` | `js.intercomcdn.com` | `required` |
| `openai` | `js.stripe.com` | `required` |
| `openai` | `o207216.ingest.sentry.io` | `required` |
| `openai` | `o33249.ingest.sentry.io` | `required` |
| `openai` | `rum.browser-intake-datadoghq.com` | `required` |
| `openai` | `setup.workos.com` | `required` |
| `openai` | `workos.imgix.net` | `required` |
| `anthropic` | `github.com` | `feature-required` |
| `anthropic` | `raw.githubusercontent.com` | `feature-required` |
| `anthropic` | `registry.npmjs.org` | `feature-required` |
| `anthropic` | `storage.googleapis.com` | `feature-required` |
| `anthropic` | `formulae.brew.sh` | `feature-required` |
| `anthropic` | `cdnjs.cloudflare.com` | `feature-required` |
| `anthropic` | `cdn.jsdelivr.net` | `feature-required` |
| `anthropic` | `cdn.tailwindcss.com` | `feature-required` |
| `anthropic` | `code.jquery.com` | `feature-required` |
| `anthropic` | `unpkg.com` | `feature-required` |
| `anthropic` | `http-intake.logs.us5.datadoghq.com` | `optional` |
| `anthropic` | `browser-intake-us5-datadoghq.com` | `optional` |
| `anthropic` | `fonts.googleapis.com` | `optional` |
| `anthropic` | `fonts.gstatic.com` | `optional` |
| `anthropic` | `^[^.]+-review\.googlesource\.com$` | `optional` |
| `anthropic` | `challenges.cloudflare.com` | `compatibility-critical` |

PSL 的 private 段也包含 Claude 自有产品边界。`claude.app`、`.claudeusercontent.com`、`.frame.claudeusercontent.com` 根据官方明确范围逐条登记例外；ICANN 公共后缀、整个通用公共云/CDN 父域仍拒绝。不能用任意 regex 或自报来源扩大范围。

## 执行计划

| 项目 | 状态 / 完成依据 |
|---|---|
| 三份维护数据、固定官方与社区快照、用户验证记录 | 已建立 |
| 生成器、分类器、验证器、哈希锁、CI | 已实现；本地及远端检查结果在交付时记录 |
| 本地对抗性检查 | 19 个策略测试、3 个伪造/损坏制品反例通过；1,330 个真实 source/binary 用例零失败，重建一致，上游交叉核对通过 |
| 手动预发布 | `v0.1.0-rc.1` 已发布；6 个公开附件回下载校验通过，未变更现场配置 |
| 正式发布审阅与新批次消费者集成 | 待执行；具体门槛见 `sources/release-review.json` 与正式方案 |
| `dist/` 正式批次与客户端接入 | 待上一步通过；N100 保留原路由位置 |
