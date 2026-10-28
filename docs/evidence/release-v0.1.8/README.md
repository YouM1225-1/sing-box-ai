# v0.1.8 发布记录（发布中）

准备发布的唯一规则变更为 OpenAI 新增 `poteto.com` 根域及全部子域。Claude 的两份 SRS 与 v0.1.7 字节一致。

## 已完成

- 新版本候选 [v0.1.8-rc.1](../../../artifacts/v0.1.8-rc.1/manifest.json) 编译及 2,734 项原生匹配检查通过。
- 全部 68 项回归通过，无失败或跳过，见[测试日志](unit-tests.log)。
- [语义差异](semantic-diff.json)确认只增加 `domain_suffix: poteto.com`，没有删除规则。
- GitHub 写入权限已验证，本地与远端 main 的基础提交一致。
- [旧 Release 元数据](release-before.json)和[旧标签引用](tags-before.txt)已留档，供发布后核对。
- 固定版本与 Latest 的[原生空缓存探测脚本](remote-probe.py)已准备，每个入口包含 196 项请求检查，尚未执行远端探测。

## 发布例外与验证边界

当前日期的正式发布校验返回 `Unapproved/expired compatibility: challenges.cloudflare.com`，见[检查记录](preflight.json)。既有 Anthropic 精确规则最后验证日为 2026-09-27，复核截止为 2026-10-27。

[项目发布约定](../../plan.md)明确要求：“到期 UTC 当日 00:00 阻断新发布，不能只顺延日期。”新版本会同时携带三份 SRS，因此字节未变的 Claude 规则也触发该检查。

本次尝试打开 Claude 登录页，页面停在 Cloudflare 安全验证。桌面端仅确认可运行，未取得新的 Challenge 流程验证结果；没有据此续期或声称验证通过。

用户已授权“发布”。用户随后已明确回复“批准本次例外，保留旧日期和证据”，批准以下具体例外：**仅本次 v0.1.8 沿用 v0.1.7 的两份 Claude SRS，保持原字节、原验证日期与原证据，仅更新 OpenAI。** 批准此例外不等于 Claude Challenge 已重新通过验证。例外已通过来源文件和制品摘要固定，仅对授权日的 v0.1.8 生效，见[原文记录](../../../sources/evidence/release-v0.1.8-unchanged-exception.json)。

当前未推送代码、未新建 Release、未改变 Latest；线上仍为 v0.1.7。
