# The Passport Page of a Country That Isn't There

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Revaaa28/makefun-passport-20261121/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Revaaa28/makefun-passport-20261121/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

Entry for the [make.fun bounty "The Passport Page of a Country That Isn't There"](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318).

`main.py` (Python 3.13, no network, deterministic) draws one uncaptioned
open passport spread — 1024×1024 PNG — for the invented island republic
of **Solmara** (capital Meridia) and writes it to `/output/entry.png`.

The spread:

- **Data page** — coat of arms, holder Elena Maris Velas (born 14 Mar 1994,
  Meridia), passport No. SM 482 917, issued 12 Feb 2024, expires 11 Feb 2034,
  a code-drawn portrait, a bilingual (English / Solmaran) field column, a
  seafarer endorsement, and a two-line machine-readable zone with ICAO 9303
  check digits.
- **Visa page** — six entry/exit stamps telling one coherent trip
  (Solmara → Dalmara → Ostara → Solmara, 03–25 Mar 2024, every stamp after
  the issue date and before expiry), a Dalmara visitor visa
  ("NOT VALID FOR EMPLOYMENT — FISHING PORTS EXCLUDED", fee 25 DM paid),
  and a circular FEE PAID stamp.

## Run

```sh
python3 main.py
# writes /output/entry.png (or $OUTPUT_PATH when set)
```

## License

MIT — see [LICENSE](LICENSE).
