# GitHub 上游规则核查：2026-10-20

取得时间：2026-10-20 15:39:56–15:42:55 UTC，即北京时间 23:39:56–23:42:55。比较对象为已发布的 `artifacts/v0.1.6/openai.json` 和 `artifacts/v0.1.6/anthropic.json`。本次只读检查，未修改 sources、artifacts、dist 或发布状态。

## 结论

四个上游的当前产品集合语义一致：OpenAI 24 条，Anthropic 9 条。相对于昨日核查，未发现已合并的 OpenAI/Anthropic 新域名。当前产品文件均不含 IP 规则，因此不能从这些域名集合推断各产品的全部实际 IP。

| 来源 | OpenAI | Anthropic | 相对 v0.1.6 的未覆盖项 |
|---|---:|---:|---|
| v2fly/domain-list-community | 24 条，覆盖 23 条 | 9 条，全覆盖 | `domain_suffix:openai.org` |
| SagerNet/sing-geosite | 24 条，覆盖 23 条 | 9 条，全覆盖 | 同上 |
| MetaCubeX/meta-rules-dat，sing JSON | 24 条，覆盖 23 条 | 9 条，全覆盖 | 同上 |
| Loyalsoldier/v2ray-rules-dat，实际 dat 解码 | 24 条，覆盖 23 条 | 9 条，全覆盖 | 同上 |

`openai.org` 是已经记录的 pending 候选，并非今天首次发现。今日新评论进一步削弱其归属依据，应继续保持未选中。未合并 PR #4057 的 `o33249.ingest.us.sentry.io` 也是仓库已有 pending 候选，不应称作新域名或必需补充项。

## 精确版本及可核验来源

| 来源 | 固定版本 | 时间（UTC） | 链接 |
|---|---|---|---|
| v2fly OpenAI 文件最后变更 | `5b1678867da0afc35854f481c1749a39048952df` | 2026-10-17 12:58:53 | [OpenAI 固定版本](https://github.com/v2fly/domain-list-community/blob/5b1678867da0afc35854f481c1749a39048952df/data/openai) |
| v2fly Anthropic 文件最后变更 | `2c892a618f4e23c549d28edd0f3f75407521b1aa` | 2026-10-02 05:00:05 | [Anthropic 固定版本](https://github.com/v2fly/domain-list-community/blob/2c892a618f4e23c549d28edd0f3f75407521b1aa/data/anthropic) |
| SagerNet rule-set 当前构建 | `a3795b85be650b16ffa9770a836d90afc391baaf` | 2026-10-20 04:10:04 | [OpenAI SRS](https://raw.githubusercontent.com/SagerNet/sing-geosite/a3795b85be650b16ffa9770a836d90afc391baaf/geosite-openai.srs)；[Anthropic SRS](https://raw.githubusercontent.com/SagerNet/sing-geosite/a3795b85be650b16ffa9770a836d90afc391baaf/geosite-anthropic.srs) |
| MetaCubeX sing 当前构建 | `cce4c2ff6a45b76149e9740ece0942a8df9723f7` | 2026-10-20 01:10:47 | [OpenAI JSON](https://github.com/MetaCubeX/meta-rules-dat/blob/cce4c2ff6a45b76149e9740ece0942a8df9723f7/geo/geosite/openai.json)；[Anthropic JSON](https://github.com/MetaCubeX/meta-rules-dat/blob/cce4c2ff6a45b76149e9740ece0942a8df9723f7/geo/geosite/anthropic.json) |
| Loyalsoldier 最新 release | `202610192206` | 2026-10-19 22:07:38 | [Release](https://github.com/Loyalsoldier/v2ray-rules-dat/releases/tag/202610192206) |

构建时间不等于域名新增时间。SagerNet、MetaCubeX 和 Loyalsoldier 的集合属于同源派生结果，不能把四源一致当作四份独立官方背书。

Loyalsoldier 的实际 `geosite.dat` 已下载，SHA256 与发布的校验文件一致：`bf40e80d6a91f7759a6810d792639facd89faf27895dea5264f14bc15ec3639d`。随后解码 OPENAI、ANTHROPIC 项进行比较。SagerNet SRS 使用本仓库固定的 sing-box 工具解编译后比较。

当前 v2fly OpenAI 文本与 10 月 19 日抓取内容逐字节一致；MetaCubeX OpenAI JSON 的 SHA256 也与昨日一致。SagerNet Anthropic SRS 与仓库 10 月 3 日固定输入逐字节一致，SHA256 为 `4c58ec54eed852bddc07d434d42b1b97c4c22ebc52aa3b393221b607c3d56f6f`。

## 新评论与未合并候选

### openai.org：新评论承认未充分验证所有权

[PR #4149](https://github.com/v2fly/domain-list-community/pull/4149) 已于 10 月 17 日合并。之前已有维护者质疑归属，另一个回复只引用 WHOIS、crt.sh 并推测可能是内部域名。

2026-10-19 16:09:40 UTC，即北京时间 **10 月 20 日 00:09:40**，提交者新增[这条评论](https://github.com/v2fly/domain-list-community/pull/4149#issuecomment-6271665917)：

> I added the domain without sufficiently verifying its ownership, and I understand the concern. ... If needed, I'm happy to help correct the entry.

该评论不是 OpenAI 官方归属确认，也没有提供产品使用或必要性证据。本仓库已有 `openai:domain_suffix:openai.org` pending 记录，`selected_pending` 仍为空；继续排除符合现有证据。

### o33249.ingest.us.sentry.io：已有 pending，PR 仍在索要来源

[PR #4057](https://github.com/v2fly/domain-list-community/pull/4057) 创建于 **2026-09-14 02:16:30 UTC**，提议新增：

```text
full:o33249.ingest.us.sentry.io @ads
```

PR 描述仅称其为 ChatGPT app tracking API。2026-10-19 04:04:29 UTC 的[唯一评论](https://github.com/v2fly/domain-list-community/pull/4057#issuecomment-6259393105) 是维护者询问 `Source?`；截至本次抓取仍未合并、未见来源回复。

仓库已有此域的 pending 记录，`first_seen` 为 2026-09-27，依据为历史 SRS。v0.1.6 的 OpenAI 规则未匹配该域；这属于已知遥测候选，不能证明核心功能缺失，也不支持扩大到整个 `sentry.io`。

## 搜索范围与限制

查询了四仓库中包含 OpenAI、Anthropic、Claude，且在 2026-10-19 之后更新的 PR；GitHub 搜索均返回 `incomplete_results:false`。实际相关结果为 #4149、#4057。两个 Claude 关键词命中与产品规则无关：v2fly #4168 只修改三家中国运营商域名文件；Loyalsoldier #530 只修改 workflow 和 README，已检查文件清单排除。

上述搜索不等于互联网全部相关资料。四个域名集合不包含 IP，不能代替 OpenAI Voice、Anthropic 官方 IP 文档或 ASN 路由公告核查；也不应把共享云或 CDN 的全部地址归为产品必需 IP。

## 本地完整证据

- [完整规则类型与条目](normalized.json)
- [与 v0.1.6 的逐源语义比较](comparison-v0.1.6.json)
- [本地制品 SHA256、已有 pending 与选中状态](local-comparison-context.json)
- [首轮来源 URL、取得时间、SHA256](fetch-index.json)
- [固定构建与二进制抓取记录](fetch-artifacts-index.json)
- [v2fly 当前 OpenAI 原文](v2fly-openai.txt)、[Anthropic 原文](v2fly-anthropic.txt)
- [SagerNet OpenAI 解编译](sager-openai.json)、[Anthropic 解编译](sager-anthropic.json)
- [MetaCubeX OpenAI](meta-openai.json)、[Anthropic](meta-anthropic.json)
- [Loyalsoldier 解码结果](loyalsoldier-decoded.json)
- [#4149 全部评论原文](v2fly-pr4149-comments.json)
- [#4057 详情](v2fly-pr4057.json)、[补丁](v2fly-pr4057-files.json)、[评论](v2fly-pr4057-comments.json)
- [v2fly PR 搜索记录](search-index.json)、[派生仓库 PR 搜索记录](search-downstream-index.json)
- [补充提交及无关 PR 文件清单](commit-extra-index.json)

本子任务 graft：1 次调用，估算节约 21,258 tokens。
