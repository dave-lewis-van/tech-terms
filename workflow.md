# Tech-terms API workflows 

## Developer Workflow

1. Create a feature branch from `v1.0`
2. Add or modify the endpoint in `main.py`
3. Run `python gen_openapi.py` locally and commit both `main.py` and `reference/openapi.yaml`
4. Push the feature branch — this triggers the CI pipeline
5. CI runs: spec drift check → Spectral lint → Schemathesis contract tests
6. If CI passes, open a PR targeting `v1.0`
7. Done — hand off to the Technical Writer

## Technical Writer Workflow

1. Review the PR, paying attention to spec changes in `reference/openapi.yaml`
2. Test the API endpoints against the live Railway URL
3. Update descriptions, examples, or other doc content in the spec if needed (then push and let CI re-run)
4. Once satisfied, approve and merge the PR into `v1.0`

## On Merge to `v1.0` (Automatic)

1. CI re-runs — final validation gate
2. Railway auto-deploys — live API updated (Railway watches `v1.0`)
3. ReadMe syncs — `reference/openapi.yaml` pushed to ReadMe via GitHub integration

---

**Key design principle:** Nothing reaches `v1.0` until both CI and the Technical Writer have signed off. The developer never touches ReadMe directly.
