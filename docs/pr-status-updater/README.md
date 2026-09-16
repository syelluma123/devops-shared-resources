# PR status updater (RHOAIENG-93330)

Posts GitHub **commit statuses** on pull request head commits for the Gated Artifacts Promoter (GAP).

## Requirements

- `gh` CLI authenticated (`gh auth login` or `GITHUB_TOKEN`)
- Python 3.10+

## Manual usage

```bash
pip install -r requirements-dev.txt

# Post a green dummy gate on one PR
python scripts/post_pr_status.py \
  --pr-url https://github.com/red-hat-data-services/odh-dashboard/pull/123 \
  --status completed

# Dry-run (runs read-only gh calls for PR head SHA; prints POST commands only)
python scripts/post_pr_status.py \
  --pr-url https://github.com/org/repo/pull/1 \
  --status completed \
  --dry-run

# Discover PRs by label
python scripts/post_pr_status.py \
  --repo red-hat-data-services/odh-dashboard \
  --label gated-artifacts-promoter \
  --status completed
```

Default check context name: `gated artifacts promoter` (override with `--check-name`).

## `--status` values

This tool posts **commit statuses**. The GitHub API `state` is always one of
`success`, `failure`, `pending`, or `error`.

Accept on the CLI (check-oriented names map as shown):

| `--status` | Posted to GitHub as |
|------------|---------------------|
| `completed` | `success` |
| `failure` | `failure` |
| `in_progress` | `pending` |
| `queued` | `pending` |
| `success`, `pending`, `error` | same value |

GAP names (e.g. `merge-failure`) are **not** accepted here; translate them in the
PR monitor workflow ([RHOAIENG-93565](https://redhat.atlassian.net/browse/RHOAIENG-93565))
before invoking this script.

Removing a status entirely is not implemented yet (commit statuses are additive on GitHub).

## Tests

```bash
cd devops-shared-resources   # repo root — required for imports
pip install -r requirements-dev.txt
pytest -v tests/
```
