# dsh-freqtrade — a GPL-free strategy-bot toolkit for DeepSeek Harness

**Declarative strategies from a community pack, one deterministic runner, fees
and stops included — every result labeled bar-level. Built as a clean-room
implementation of the strategy-bot concept: zero code from the GPL upstream.**
**声明式策略包 + 统一确定性运行器，含费率与止损——结果随 bar 级执行标注。
策略机器人概念的自研净室实现：与 GPL 上游零代码关系。**

[![DeepSeek Harness](https://img.shields.io/badge/DSH-plugin-4E6DD4)](https://github.com/deepseek-ai) [![License: MIT](https://img.shields.io/badge/license-MIT-3da639)](LICENSE)

> Concept slot of [freqtrade](https://github.com/freqtrade/freqtrade) (57k★) +
> [freqtrade-strategies](https://github.com/freqtrade/freqtrade-strategies) (5.7k★),
> **rebuilt clean-room for DSH** — see the license posture below. Not affiliated.
> Family: [dsh-TradingAgents](https://github.com/vicfei/dsh-TradingAgents) ·
> [dsh-OpenBB](https://github.com/vicfei/dsh-OpenBB) · [dsh-CCXT](https://github.com/vicfei/dsh-CCXT) ·
> [dsh-nautilus_trader](https://github.com/vicfei/dsh-nautilus_trader) · [dsh-jesse](https://github.com/vicfei/dsh-jesse) ·
> [dsh-hummingbot](https://github.com/vicfei/dsh-hummingbot) · [dsh-Kronos](https://github.com/vicfei/dsh-Kronos) ·
> [dsh-quantstats](https://github.com/vicfei/dsh-quantstats) · [dsh-QuantLib](https://github.com/vicfei/dsh-QuantLib) ·
> [dsh-Vibe-Trading](https://github.com/vicfei/dsh-Vibe-Trading) · [dsh-ai-hedge-fund](https://github.com/vicfei/dsh-ai-hedge-fund).

## License posture (upstream is GPL-3.0 — this is a clean-room rebuild)

Upstream is GPL-3.0, which we treat the family way: **no importing, no process
wrapping, no vendoring — not even the "shell out to user-installed GPL app"
workaround.** What's borrowed is the product idea (declarative strategies +
community pack + bot runner); SMA crosses and RSI thresholds are public-domain
common sense. Live execution routes through the family's own guarded ccxt
bridge, never freqtrade itself. The result is a **GPL-free freqtrade concept** —
usable where GPL can't go.

## Quick start

```bash
git clone https://github.com/vicfei/dsh-freqtrade && cd dsh-freqtrade
python3 scripts/bot.py --list                                  # the strategy pack
python3 scripts/bot.py --all --data <klines.json> --fee_bps 5  # run them all
```

Real smoke (binance BTC/USDT 365d, 2026-11-17) — four pack strategies vs a
**−29.9% buy & hold** year:

| strategy | trades | win | return | stops |
|---|---|---|---|---|
| donchian_breakout | 5 | 40% | **+2.6%** | 0 |
| macd_momentum | 8 | 25% | −1.6% | 0 |
| sma_cross | 6 | 33% | −10.5% | 3 |
| rsi_reversion | 6 | 33% | −15.1% | 4 |

Trend/breakout shapes survived the bear year; mean-reversion bled — the pack
teaches regime sensitivity on real data, with bar-level execution labeled.

## Status & roadmap

v0 pack + runner smoke-tested on live data. [ROADMAP](ROADMAP.md): M1 strategy
DSL hardening + trailing stops + dry-run paper loop; M2 live execution behind
the family guard (ccxt bridge — never the GPL app).

## License & disclaimer

MIT (this repo); concept credit to GPL upstreams — zero upstream code used.
**Not investment advice.**
