# GTA 6 meme on X — make.fun bounty entry

[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/aliceskyfahriz-cyber/makefun-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/aliceskyfahriz-cyber/makefun-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

Entry for the [make.fun bounty "Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01) ($500, 50 places).

## The meme

A Wanted-star parody with a Vice City sunset: the make.fun ghost is the
fugitive, front and centre under five gold wanted stars, over a giant
slatted sunset sun. The picture is built programmatically by
`make_meme.py` (Python + Pillow) from the real ghost logo at
https://make.fun/press/ — `meme.png`, 1024x1024. The post itself is the
entry: it goes out from a public X account with the picture attached,
its text carrying make.fun and the entrant's play code.

## What the program does

`main.ts` (Node 22, standard library only, no network) carries the X
post's address from the repository into the grader's output directory:
it reads `POST.json` next to it, checks it parses as JSON holding a
`url` string, and writes the same bytes to
`$MAKEFUN_OUTPUT_DIR/POST.json`. Any failure prints an error and exits
non-zero. `POST.json` holds the post's address once the post is live;
until then it carries a placeholder URL.

## Run it locally

```sh
./run.sh
# mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is byte-identical to `POST.json`.

## Files

- `main.ts` — the entry program (Node 22, stdlib only)
- `POST.json` — the X post's address (placeholder until the post is live)
- `meme.png` — the meme picture, 1024x1024
- `make_meme.py` — the Pillow script that draws the meme

Optional: earn referral rewards — [join make.fun with my link](https://make.fun/r/qxc8rweq).
