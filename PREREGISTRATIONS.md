# Pre-registration commit hashes

The pilot write-ups in `docs/` pre-register each stage's hypotheses, arms and
refuters in a commit made *before* the rows for that stage were collected, and
then cite that commit by its short hash. Those hashes were minted in the
private working repository this repository was extracted from.

This repository's history was produced by path-filtering that working
repository with `git filter-repo`, keeping only the files belonging to the
ownership work and dropping an unrelated earlier study carried out on a private
chat corpus. Rewriting a commit's tree changes its hash, so every hash in the
history is new. Nothing else about the history changed: commit order, author
and committer dates, messages, and the contents of every kept file are exactly
as they were. A pre-registration commit therefore still sits, in this history,
strictly before the commit that added the rows it registers, which is the
property the pre-registration claim rests on.

The table maps every hash cited in the kept documents to its counterpart here.

| Cited (original) | This repository | Date | Commit | Cited in |
| --- | --- | --- | --- | --- |
| `0af65c8` | `587943e` | 2026-09-04 | Paper: GPT stage E row from the finished clean13 refill; pilot 19 GPT stage E figures | docs/REVIEW-hostile-paper-2026-09-04.md |
| `0bc6cb6` | `9c50ca7` | 2026-09-04 | Answer the hostile review, tier 2 and the rest | docs/REVIEW-hostile-paper-2026-09-04-pass2.md |
| `1c766bf` | `aea5bb8` | 2026-09-04 | Answer the hostile review, tier 1 | docs/REVIEW-hostile-paper-2026-09-04-pass2.md |
| `6cb67e6` | `7f92c0a` | 2026-09-04 | Paper: pass-2 revision, title to 'Ownership by label' | docs/REVIEW-hostile-paper-2026-09-04-pass2.md |
| `aab4d66` | `cc36ded` | 2026-09-03 | Pilot 13b results; pre-register 13c | docs/PILOT-13-ownership-gpt.md |
| `d6f2c55` | `7f067a0` | 2026-09-04 | Gitignore the 28 MB fork index; the audit script rebuilds it | docs/REVIEW-hostile-paper-2026-09-04-pass2.md |
| `ef1f6dd` | `f0cae51` | 2026-09-04 | Harness context leak fix; 17c and 15b pre-registered | docs/PILOT-13-ownership-gpt.md, docs/PILOT-19-leak-check.md, docs/PLAN-bulletproof.md |

Full new hashes:

```
0af65c8  ->  587943edeee3a27b2ca3316f19c9b1cd2b9e8e30
0bc6cb6  ->  9c50ca7fbe479168a9708c2486db451a25764da5
1c766bf  ->  aea5bb838f141e83668002bb3466a7e2d89fd425
6cb67e6  ->  7f92c0a85a7d13ad7fb53ef091450213a43ca606
aab4d66  ->  cc36ded3ebda149f1ee600966182047b50921054
d6f2c55  ->  7f067a0e87f2b6c44984a734baec5cff803d1fd1
ef1f6dd  ->  f0cae51489337d34b0071dfe9e22c9809c2afbf8
```

The complete old-to-new mapping for all 107 commits was produced by
`git filter-repo` and is not reproduced here; the seven hashes above are every
hash cited in the kept text.

