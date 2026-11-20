# Claude 四个域名的规则覆盖核对

核对日期：2026-11-05。范围：当前工作区的 v0.1.9 规则源文件及发布产物。

**截图中的 4 个域名全部已被 `anthropic` 规则集覆盖，无需重复添加。**

| 截图中的域名 | 是否覆盖 | 发布规则中的命中项 |
| --- | --- | --- |
| `api.anthropic.com` | 是 | `domain_suffix: anthropic.com` |
| `http-intake.logs.us5.datadoghq.com` | 是 | `domain_keyword: datadog` |
| `bridge.claudeusercontent.com` | 是 | `domain_suffix: claudeusercontent.com` |
| `downloads.claude.ai` | 是 | `domain_suffix: claude.ai` |

域名后缀规则覆盖对应父域名下的子域名；关键词规则匹配域名中包含的字符串。因此，发布文件无需逐条列出这 4 个完整域名即可覆盖。

依据为 [v0.1.9 发布规则 JSON](../artifacts/v0.1.9/anthropic.json) 第 22、29、32、38 行。源清单也有完整域名记录：Datadog 地址见 [Anthropic 源清单](../sources/anthropic.yaml) 第 155 行，其余 3 个见 [历史域名输入清单](../sources/upstream/legacy-anthropic-domains.yaml) 第 13、15、22 行。

使用仓库内 `.tools/sing-box` 反编译核验，[当前分发文件](../dist/anthropic.srs) 的 JSON 内容与 v0.1.9 发布规则 JSON 完全一致；它与 [v0.1.9 发布文件](../artifacts/v0.1.9/anthropic.srs) 的 SHA-256 也一致：

```text
13112b79d21073c4478f0e6a902acc7ba6dd7df9efe2c6749d9844afe97256c1
```

以上确认的是仓库内规则覆盖；设备上的实际分流取决于客户端加载的规则版本及路由配置。
