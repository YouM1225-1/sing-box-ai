# v0.1.1 手动正式发布证据

修订：1.0；日期：2026-09-28。用途：绑定手动构建、GitHub 上传、公开下载与本机空缓存加载结果；不代表 N100 或账户会话验收。

- [正式方案](../../plan.md#execution)、[发布汇总](publication-results.json)、[构建结果](build-results.json)、[46项回归](unit-tests.log)
- [正式批次](../../../artifacts/v0.1.1/manifest.json)、[固定版本6项下载](fixed-downloads.json)、[Latest四项下载](latest-downloads.json)
- [原生远程冷启动结果](remote-results.json)、[实际执行的探测源码](remote-probe.py)、[原文件保留核对](preservation.json)
- [GitHub Release](https://github.com/YouM1225-1/sing-box-ai/releases/tag/v0.1.1)

两次 release 构建各2,038项原生检查通过，三个SRS与源JSON均与已验收候选逐字节一致。新批次发布批准绑定已提交输入；395请求的原消费者证据因此按字节身份关联，未重标为实机验收。

远程测试使用固定GitHub地址、alpha.9、空初始缓存与默认HTTP client。两个产品正例及一个负例实际进入受控reject，子进程退出、回环监听关闭。原始运行日志只保留本机忽略目录，其摘要记录于结果；此处公开原始结果与实际执行源码。

复现远程探测时，在规则仓库根目录将 `remote-probe.py` 复制到 `build/release-v0.1.1-remote/probe.py` 后运行该副本，并传入一个尚不存在的输出子目录名。脚本按该目录层级定位锁定的 `.tools/sing-box`；不能直接从归档目录启动。复现仅请求固定公开资产并创建本机回环测试进程，不改系统网络或N100。联网条件不满足时保留失败结果并停止，不将历史通过状态代入新环境。

发布包固定于制品标签提交，之后的发布证据和当前文档保存在 main；不替换已上传资产来补记后验状态。Latest可能被在线消费者自动获取，即使没有配置写入或服务重启。消费者与部署身份保持空/pending。
