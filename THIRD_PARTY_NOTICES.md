# 来源与许可证

- `sources/upstream/dlc-*.txt`：v2fly/domain-list-community，固定提交见 `sources/upstreams.yaml`。保留上游 MIT 许可证 `sources/upstream/dlc-LICENSE`。
- `sources/upstream/geosite-*.srs`：SagerNet/sing-geosite 的派生交叉核对输入；来源、提交和哈希见 upstream registry。它们不是本项目发布输出。
- `sources/upstream/public_suffix_list.dat`：Mozilla Public Suffix List；原始文件内保留 MPL 2.0 声明及来源。用于公共边界检查。
- `sources/upstream/legacy-anthropic-domains.yaml`：维护者旧仓库的固定规则快照，仅用于历史依据及发现分类。
- `sources/official/*.json`：官方网络事实的结构化记录及 OpenAI Voice 原始 JSON。每份事实保留直接来源、观察时间和取得方式；不包含厂商页面全文。
- sing-box 编译器在准备阶段下载到忽略目录 `.tools/`；源码与许可证见 https://github.com/SagerNet/sing-box/tree/132b38e9caaba1a1959354d518e54d2d08419afe 。Go harness 的依赖按 `go.mod` / `go.sum` 获取，遵循各模块许可证；不将依赖许可证重标为本项目许可证。

本仓库未替维护者选择整体开源许可证。第三方数据与工具各自的许可证不因此改变。
