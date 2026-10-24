# GitHub 开源项目整理

[English](README.en.md) · 简体中文

一个 Codex Skill，帮助整理本地项目、维护中英文说明、自动创建私有 GitHub 仓库并同步更新，为后续开源做好准备。

适用于代码、Codex Skills、设计素材、产品图片及混合项目。它由代理按指引执行，不是后台同步服务，也不是独立的 Git 客户端。

## 能做什么

- 识别项目类型，适度整理文件，并修复移动或重命名涉及的引用。
- 生成中文 `README.md` 与英文 `README.en.md`，后续按变更增量维护。
- 根据实际可用工具，通过 GitHub 连接、CLI 或已登录浏览器自动创建仓库、填写名称和中文描述。
- 检查上传范围、配置与大文件，提交并推送；首次创建的仓库默认私有。
- 协助检查许可证、素材来源和使用步骤；只有明确要求时才公开仓库。

## 安装

将整个项目目录放到 `$CODEX_HOME/skills/github-open-source-prep`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills/github-open-source-prep`。保持 `SKILL.md`、`agents/`、`references/` 和 `scripts/` 的相对位置。

下一轮对话中通过 `$github-open-source-prep` 调用。以 Windows + Codex 为主要环境；检查脚本仅依赖 Python 3.9+ 标准库。Git 操作需要可用的 Git，远端操作需要具备相应权限的 GitHub 连接、已认证 CLI 或可控制的已登录浏览器。本地推送认证与浏览器登录分别检查。

## 使用示例

先整理，不上传：

```text
使用 $github-open-source-prep 整理当前项目，补齐中英文 README，先不要推送。
```

创建私有仓库并同步：

```text
使用 $github-open-source-prep 将当前项目同步到 GitHub。
```

后续更新：

```text
使用 $github-open-source-prep 检查这次变更，更新双语说明并同步到 GitHub。
```

“同步到 GitHub”授权检查、必要整理、提交和推送；目标账号不明、冲突或缺少权限时会询问。不会因为准备完成就自动公开。只检查开源准备时可以说“准备开源这个项目，先保持私有”。

## 默认整理范围

设计源文件、原始图片和过程稿默认留在本地，只上传使用必需文件和精选示例；项目价值依赖源文件时单独判断。排除上传不删除原件。已有项目结构和手工文档优先保留，源码结构大调整先讨论。

许可证由用户确认后生成，混合项目可分别授权。此 Skill 包含作者的中文首页、私有优先等工作偏好，其他使用者可在 `SKILL.md` 中调整。

## 检查脚本

在仓库根目录运行，将路径替换为目标项目：

```shell
python scripts/inspect_project.py /path/to/project
python scripts/inspect_project.py /path/to/project --max-files 20000 --large-mib 20
python scripts/check_inspector.py
```

Windows 可使用引号包住的实际项目路径。检查器输出 JSON，仅包含文件位置与风险类别，不输出匹配到的凭据值。

**检查边界：**它不审计 Git 历史、不读取 gitignore 规则，只检测部分凭据模式，内容读取限于不超过 1 MiB 的文件，并跳过依赖目录、链接和嵌套仓库。代理仍需检查已跟踪内容及待推送历史。没有发现不能视为安全证明。

## 项目结构

```text
SKILL.md                   工作流程与默认偏好
agents/openai.yaml         Codex 显示信息
references/project-types.md 按项目类型整理的指引
references/readme-guide.md  双语文档指引
scripts/inspect_project.py  只读文件初筛
scripts/check_inspector.py  隔离测试
```

## 验证与限制

已在 Windows 上通过 Skill 格式校验，以及混合类型识别、敏感值不回显、跳过目录、扫描数量限制和只读行为测试。macOS/Linux 尚未实机验证。自动建仓与推送依赖运行环境实际开放的工具和认证能力。

检查脚本不能代替完整凭据扫描或素材授权核查。无网络、认证失效或远端冲突时，代理保留本地结果并报告具体状态。

## 贡献与许可

欢迎通过 Issue 或 Pull Request 提供可复现的问题和改进。修改流程时同时维护双语说明；修改检查器后运行上述隔离测试。

许可证尚未确定，目前不声明开放源代码许可；公开发布前由作者选择并补充 LICENSE。
