# v0.1.2 正式发布证据

核验日期：2026-10-03（Asia/Shanghai）。[正式 Release](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.2) 已发布并设为 Latest；发布时间 `2026-10-03T14:06:35Z`，Release ID `402537457`。

## 身份与验收

- 正式输入提交：`d965fa091f4c57961cf5a172968840175d90d2a8`；标签提交：`79bc9a084cc095f4a5879843e27d6f9d9cd8f37f`。
- [发布结果](publication-results.json)：固定 URL 下载、Latest 下载、本机空缓存加载和旧 Release 保持检查均为通过。该记录描述实际发布验收，不改写此前构建记录的时点状态。
- [固定版本下载](fixed-downloads.json)、[Latest 下载](latest-downloads.json)、[实际空缓存加载](remote/results.json)及[原生日志](remote/runtime.log)：下载摘要一致，10 个回环请求的产品命中与后缀负例通过，进程和监听端口已结束。
- [上传中断](upload-interruption.json)：首次按标签查询草稿返回 404，尚无资产上传；修正为按创建响应 ID 定位，用户回复“继续”后完成本次发布。
- [正式 manifest](../../../artifacts/v0.1.2/manifest.json)与[正式校验和](../../../artifacts/v0.1.2/SHA256SUMS)：release 模式、输入提交绑定、静态 artifact-publication 批准。消费者声明仍为空，部署 pending。
- [构建结果](build-results.json)、[第一次正式校验](release-1-validate.log)与[第二次正式校验](release-2-validate.log)：两次正式构建各 2,066 项原生检查及 `--for-release` 门禁通过；三 SRS 和三 JSON 两批及相对已验收候选逐字节一致。
- [46 项回归](unit-tests.log)与[同输入 candidate fixture 校验](test-candidate-validate.log)：对抗回归依照测试入口使用 candidate fixture，其 63 份输入与正式构建相同、三 SRS 和三 JSON 与正式批次相同；全量通过且无跳过。
- [首次 release fixture 失败日志](unit-tests-release-fixture.log)：三项篡改制品测试被更前的发布摘要门禁拒绝，预期消息不匹配。仅纠正测试调用为 candidate fixture，没有改源码、断言或正式门禁；不称 release fixture 直接通过 46 项回归。
- [候选证据与复现入口](../durability-0.1.2-rc.1/README.md)：社区基线唯一新增 `claude.dev` root suffix、独立复核、截图九项覆盖及 560 个隔离消费者请求，均保持原始证据身份。
- [本轮授权](../../../sources/evidence/release-v0.1.2-authorization.json)与[静态语义审阅](../../../sources/evidence/release-v0.1.2-review.json)：绑定本轮三个制品摘要；OpenAI 网络和登录页面 HTTP 403 的未核实局限明确保留。

本轮只完成静态制品发布和本机验收。未访问或写入 N100，未改客户端配置、DNS、路由或防火墙，未重启或重载服务；真实登录、公网出口及目标设备重启持久化未验收。Latest 订阅者可能自行取回新规则，不等于这些消费者已完成运行验收。

`manifest`、`build-results.json`、候选记录及历史版本均保留原有身份和时点状态；不因发布完成将其消费者声明或历史待执行描述改成运行验收通过。`Validate rules` workflow 的既有删除继续保留，本轮为手动构建与发布。
