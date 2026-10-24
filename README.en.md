# GitHub Open Source Prep

English · [简体中文](README.md)

A Codex skill for organizing local projects, maintaining Chinese and English documentation, automatically creating private GitHub repositories, and syncing changes in preparation for open source publication.

Supports code, Codex skills, design assets, product images, and mixed projects. An agent follows its instructions; it is not a background sync service or a standalone Git client.

## Capabilities

- Identify project types, organize files moderately, and repair references affected by moves or renames.
- Create Chinese `README.md` and English `README.en.md`, then update affected sections incrementally.
- Use an available GitHub connector, CLI, or controllable signed-in browser to create a repository with a name and Chinese description.
- Review upload scope, configuration, and large files before committing and pushing. Newly created repositories are private by default.
- Review licensing, asset sources, and usage instructions. Make a repository public only when explicitly requested.

## Installation

Place the entire project directory at `$CODEX_HOME/skills/github-open-source-prep`, or `~/.codex/skills/github-open-source-prep` when `CODEX_HOME` is unset. Preserve the relative locations of `SKILL.md`, `agents/`, `references/`, and `scripts/`.

Invoke `$github-open-source-prep` in the next conversation turn. Windows + Codex is the primary environment. The inspector requires Python 3.9+ and only its standard library. Git operations require Git; remote operations require an authorized GitHub connection, authenticated CLI, or controllable signed-in browser. Local push authentication is checked separately from browser sign-in.

## Usage

Prepare without uploading:

```text
Use $github-open-source-prep to organize this project and write both READMEs. Do not push yet.
```

Create a private repository and sync:

```text
Use $github-open-source-prep to sync this project to GitHub.
```

Update an existing project:

```text
Use $github-open-source-prep to review these changes, update both READMEs, and sync to GitHub.
```

A request to sync authorizes inspection, necessary organization, committing, and pushing. Unclear target accounts, conflicts, or missing permissions require clarification. Preparation does not automatically make a repository public. To review readiness, ask: “Prepare this project for open source, keeping it private.”

## Default scope

Editable design sources, original images, and work-in-progress assets stay local by default; upload required files and selected examples. Sources that are essential to the project are assessed individually. Excluding a file does not delete the original. Preserve established structure and manual documentation; discuss major source restructuring first.

The user chooses a license before it is generated; mixed projects may use separate licenses. The skill includes its author's Chinese-first and private-first preferences. Other users can adjust them in `SKILL.md`.

## Inspector

Run from the repository root, replacing the path with your project:

```shell
python scripts/inspect_project.py /path/to/project
python scripts/inspect_project.py /path/to/project --max-files 20000 --large-mib 20
python scripts/check_inspector.py
```

On Windows, use your actual project path in quotes. The inspector returns JSON containing file locations and finding categories, never matched credential values.

**Scope limits:** it does not audit Git history or honor gitignore rules. It detects selected credential patterns, reads content only from files up to 1 MiB, and skips dependency directories, links, and nested repositories. The agent must separately review tracked content and outgoing history. No findings do not prove safety.

## Structure

```text
SKILL.md                    Workflow and default preferences
agents/openai.yaml          Codex display metadata
references/project-types.md Guidance by project type
references/readme-guide.md  Bilingual documentation guidance
scripts/inspect_project.py  Read-only initial file inspection
scripts/check_inspector.py  Isolated tests
```

## Validation and limitations

Skill format validation and isolated checks for mixed project detection, credential redaction, directory exclusions, file limits, and read-only behavior have passed on Windows. macOS/Linux have not been tested on actual machines. Repository creation and pushing depend on tools and authentication available in the execution environment.

The inspector does not replace a full credential scan or asset rights review. If networking, authentication, or remote conflicts block progress, the agent retains local work and reports the precise state.

## Contributing and licensing

Issues and pull requests with reproducible problems and improvements are welcome. Maintain both READMEs when changing behavior, and run the isolated tests after changing the inspector.

This project is licensed under the [MIT License](LICENSE), copyright mobaibumo. Use, modification, distribution, and commercial use are permitted provided the copyright and permission notice are retained. The software is provided as is, without warranty.
