# Independent number check (Tier 1): Section 4.3 prompt-level tests + tab:preds

Recomputed from out/clean11_judgements.jsonl (haiku, opus) and out/clean13_judgements.jsonl (gpt).
0 error rows. In-category cells: haiku 32, opus 32, gpt 30 (8 forks/cell). Wilcoxon = scipy default,
zeros dropped, nan if <5 non-zero; sign test = binomtest(k_higher, n_nonzero, 0.5).

## Part A — every quoted number MATCHES

| # | Paper claim | Paper | Recomputed | Verdict |
|---|---|---|---|---|
| 1 | neutral-rival cell Wilcoxon, all judges | p<3e-4 | 1.35e-6 / 2.44e-4 / 1.46e-6 | MATCH |
| 2 | neutral->rival prompts, haiku | 8 of 8, p=0.008 | 8/0/0, w=0.0078 | MATCH |
| 3 | neutral->rival prompts, gpt | 8 of 8, p=0.008 | 8/0/0, w=0.0078 | MATCH |
| 4 | neutral->rival prompts, opus | 5 of 8, 3 tied, p=0.06 | 5/0/3, w=0.0625 | MATCH |
| 5 | haiku placebo->rival_norep2 cells | 9 of 32 below 8/8, p=0.004 | 9 cells, w=0.00391 | MATCH |
| 6 | haiku placebo->rival_norep2 prompts | 7 of 8, p=0.016 | 7/0/1, w=0.0156 | MATCH |
| 7 | opus placebo->rival_norep2 | 3 of 32 cells; 3 of 8 prompts, sign p=0.25 | 3 cells; 3/0/5, sign=0.25 (Wilcoxon nan, <5 nz) | MATCH |
| 8 | haiku rival_norep2->rival cells | p=2e-6 | 1.72e-6 | MATCH |
| 9 | haiku rival_norep2->rival prompts | 7 higher, 1 lower, p=0.016 | 7/1/0, w=0.0156 | MATCH |
| 10 | opus rival_norep2->rival cells | p=0.01 | 0.00972 | MATCH |
| 11 | opus rival_norep2->rival prompts | 5 higher, 1 lower, 2 tied, p=0.09 | 5/1/2, w=0.0938 | MATCH |
| 12 | gpt neutral->placebo cells | 8 of 30, p=0.008 | 8 cells, w=0.00781 | MATCH |
| 13 | gpt neutral->placebo prompts | 2 of 8, sign p=0.5 | 2/0/6, sign=0.5 (Wilcoxon nan) | MATCH |
| 14 | gpt placebo->rival_norep2 cells | p=8e-5 | 8.02e-5 | MATCH |
| 15 | gpt placebo->rival_norep2 prompts | 7 of 8, p=0.016 | 7/0/1, w=0.0156 | MATCH |
| 16 | gpt rival_norep2->rival cells | p=6e-5 | 5.84e-5 | MATCH |
| 17 | gpt rival_norep2->rival prompts | 7 higher, 1 lower, p=0.023 | 7/1/0, w=0.0234 | MATCH |
| 18 | gpt placebo drop by prompt | city 0.63, fruit 0.71, zero on other six | 0.625, 0.708, 0.000 x6 | MATCH |
| 19 | caption: 32 (Claude) / 30 (GPT) cells, 8 forks | as stated | confirmed | MATCH |

Note (not an error): the "city 0.63 / fruit 0.71" figures are the neutral-minus-placebo drops,
not the placebo levels (placebo levels are 0.35 and 0.292); the text reads correctly as a drop.
Also note prompt-equal-weight means differ trivially from the cell means in tab:frames
(e.g. haiku rival 0.691 by prompt vs 0.684 by cell) — expected, cells are unevenly spread.

## Part B — tab:preds and the exact-arm sentences vs the pilot docs

| Item | Paper value | Source (PILOT-14 / PILOT-18) | Verdict |
|---|---|---|---|
| 14.1 pred/refuter | positive every scale, larger at 4B / <=0 at any scale | identical | MATCH |
| 14.1 values, outcome | -0.29,+0.28,+0.31; fired at 1.5B, same amount every question | -0.291,+0.283,+0.311; "refuter fires at 1.5B"; base-rate shift, same on every rung | MATCH |
| 14.2 pred/refuter | |rho| smaller at 4B / rho>=+0.37 p<0.05 | identical | MATCH |
| 14.2 values | +0.16,+0.14,+0.29 | +0.16,+0.14,+0.29 | MATCH |
| 14.2 outcome | failed (grows); refuter not fired; placebo 4B +0.48 | same; +0.48 (p=1.0e-4) | MATCH |
| 14.2 named -0.06; 60 cells | -0.06; n=60 | -0.06; n=60 at 4B | MATCH |
| 14.2 "57 of 60 neutral cells >= 0.9" | quoted | doc: "neutral is >= 0.9 on 57 of 60 in-category cells" | MATCH (stated in doc) |
| 14.2 "every cell below 0.04" at 3B | quoted | doc item 2: "every P(Yes) is below 0.04, sd 0.004" | MATCH (stated in doc) |
| 14.2 "never-sampled makemake" | quoted | doc: "one of them the never-sampled makemake" | MATCH |
| 14.3 | within 0.10 / drop>=0.25; -0.45,-0.19,+0.04; failed 1.5B,3B, placebo raises Yes, not fired | -0.445,-0.187,+0.041; same outcome text | MATCH |
| 14.4 | no prediction; +0.57,+0.19,+0.85; 18 of 18 each scale | +0.569,+0.188,+0.849; 18 of 18 | MATCH |
| 14.5 | >=0.10 at 1.5B, smaller at 4B / refuter none; +0.10,+0.45,+0.26; failed both halves, 0.097 at 1.5B | 0.097,0.445,0.264; doc registers no refuter; same wording | MATCH |
| 18.1 | +-0.10 / >=+0.25 p<0.05; -0.05,0.00,0.00; held, 1.5B sign negative | -0.053 (p=0.002), 0.000, 0.000 | MATCH |
| 18.2 pred/refuter | |rho|<0.3 rival and neutral / rho>=+0.37 p<0.05 either question | doc: refuter registered "under either question" | MATCH |
| 18.2 values | rival -0.47,+0.04,+0.36; neutral -0.66,+0.19,+0.44 (p=0.002) | identical (rival p 0.0007/0.80/0.013) | MATCH |
| 18.2 outcome | failed 1.5B and 4B; rival 0.01 under line; neutral 4B meets refuter as written; 48 cells all 1.000, differ below 0.001; recorded, not acted on | doc: same, "differ below the third decimal" | MATCH |
| 18.3 | >=0.25 every scale / <0.10; +0.39,+0.03,+0.37; fired at 3B, owns nothing under any frame | +0.393,+0.027,+0.368; same | MATCH |
| 18.4 | 0.40-0.60 at 1.5B/3B / >=0.70 with 10 of 12 above 0.5; 0.43-0.59, 0.41-0.58, 0.51-0.54; held | 1.5B 0.430-0.586, 3B 0.409-0.584, 4B 0.510-0.541 | MATCH |
| 18.5 | reported, no prediction; +0.00,0.00,+0.82; 12 of 12 at 4B | +0.002, 0.000, +0.816; 12 of 12, p=0.0005 | MATCH |
| 4.2 forced choice / position bias | 0.43-0.59, 0.41-0.58, 0.51-0.54; 0.47-0.51, 0.82-0.90, 0.03-0.05; 2.8 nats | identical in doc item 4 and log-p paragraph | MATCH |
| 4.2 neutral own vs other | 1.5B 0.156 vs 0.209; 3B 0.000; 4B 1.000 | own 0.156; mean of 0.136/0.268/0.223 = 0.209 | MATCH |
| 4.2 exploratory splits | +0.73 (p=0.007) own twelve; -0.24 (p=0.26) frontier 24 | identical | MATCH |
| 4.2 hedged copy | 1.5 nats less probable; 0.000 against 0.816 | identical | MATCH |
| 4.2 one-word 4B comparison | +0.29 neutral, +0.48 placebo | pilot 14 item 2 | MATCH |

No mismatches found in either part.
