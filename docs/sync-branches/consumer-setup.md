# Consumer Repo Setup (rhods-devops-infra)

The **GitHub Actions workflow and config** belong in the infra repo. This repo only provides the Python script and libraries.

## What lives where

| rhods-devops-infra | devops-shared-resources |
|--------------------|-------------------------|
| `.github/workflows/sync-branches.yaml` | `scripts/sync_branches.py` |
| `config/sync-branches.yaml` | `lib/`, `tests/`, docs |

The infra workflow should:

1. Check out the infra repo (for config)
2. Check out `devops-shared-resources` into a subdirectory
3. `pip install -r devops-shared-resources/requirements.txt`
4. Run the script against the infra config

```bash
export SYNC_TOKEN="your-token"

python devops-shared-resources/scripts/sync_branches.py \
  --config config/sync-branches.yaml \
  --only kserve
```

Use `--only` with a comma-separated list of component names, or omit it to run every entry.

## Config format

Use the existing `git:` source map in the infra repo:

```yaml
defaults:
  source-branch: main
  target-branch: stable
  tracking-label: lake-gate

git:
  - name: kserve
    automerge: "yes"
    repo-url: https://github.com/red-hat-data-services/kserve.git
    ignore-files: .tekton/*
  - name: kubeflow
    automerge: "yes"
    repo-url: https://github.com/red-hat-data-services/kubeflow.git
    ignore-files: .tekton/*
  - name: rhoai-additional-images
    automerge: "no"
    repo-url: https://github.com/red-hat-data-services/rhoai-additional-images.git
```

### Field mapping

| Infra config field | Script behavior |
|--------------------|-----------------|
| `name` | Sync entry name; used with `--only` |
| `repo-url` | Source and target repository URL |
| `automerge` | `"yes"` / `"no"` → PR automerge |
| `ignore-files` | Comma- or space-separated glob patterns |
| `defaults.source-branch` | Source branch (default: `main`) |
| `defaults.target-branch` | Target branch (default: `stable`) |
| `defaults.tracking-label` | PR tracking label (default: `lake-gate`) |
| `pr.head-strategy` / `pr-head` | `sync-branch` (default) or `source` (PR directly from source branch) |

Per-entry overrides are also supported: `source-branch`, `target-branch`, `tracking-label`, `sync-type`, `pr-head`.

Use `pr-head: source` when you want `main` → `stable` directly instead of a temporary sync branch. This requires the same repository and cannot be combined with `ignore-files`. Use `pr-head: sync-branch` when you need `ignore-files`.

The native `syncs:` format from `docs/sync-branches/README.md` is still supported.

## Token requirements

Set `GITHUB_TOKEN` or `SYNC_TOKEN` in the environment. The script does not accept tokens on the CLI.

The token needs permission to:

- read and clone target repositories
- push branches
- create and update pull requests and labels

## Local test

```bash
git clone https://github.com/red-hat-data-services/devops-shared-resources.git
export GITHUB_TOKEN="your-token"

python devops-shared-resources/scripts/sync_branches.py \
  --config config/sync-branches.yaml \
  --only kserve \
  --dry-run
```
