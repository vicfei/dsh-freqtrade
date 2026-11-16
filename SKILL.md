---
name: dsh-freqtrade
description: GPL-free strategy-bot toolkit for DeepSeek Harness — declarative strategy pack (SMA/RSI/Donchian/MACD) + one deterministic runner with fees and stops; clean-room implementation of the freqtrade concept, live routing via the family ccxt guard.
---

Use this skill to run/compare canned strategies, or as the base for user strategy
files. The runner is deterministic — strategies are declarative YAML.

## Run

```bash
KIT=<this-directory>
python3 $KIT/scripts/bot.py --list
python3 $KIT/scripts/bot.py --all --data <klines.json> --fee_bps 5
python3 $KIT/scripts/bot.py --strategy donchian_breakout --data <klines.json>
```

K-lines JSON: {"SYMBOL": [[date, open, close, high, low, volume], ...]}.

## Discipline

- Results are bar-level (fills and stops judged on close) — label it.
- Never wire this to freqtrade the app; live trading goes through the family's
  guarded ccxt bridge only (M2), behind triple-arm + notional caps.
- Strategy ideas ≠ validated edges; recommend dsh-jesse sweeps before belief.
- Not investment advice.
