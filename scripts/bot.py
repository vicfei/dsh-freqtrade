#!/usr/bin/env python3
"""策略机器人统一运行器（freqtrade 概念位的自研替代，M0 零依赖）

许可姿势（GPL 边界，owner 铁律）：上游 freqtrade/freqtrade-strategies 均为
GPL-3.0——本插件**零代码依赖、零进程包装、不 vendored**，借鉴的只有
"声明式策略 + 策略集合 + 机器人运行器"的产品思路（SMA 交叉等策略本身是
公共领域常识）。实盘执行接家族自己的 ccxt 护栏桥，不接 freqtrade 本体。

策略包（strategies/*.yaml）：声明式——指标（kind+params）+ 进出场规则
（简单表达式）+ 止损百分比。运行器统一执行：指标计算（纯 python）、
bar 级规则触发、含费成交、止损、交易日志与汇总。

用法：
  python3 scripts/bot.py --list
  python3 scripts/bot.py --strategy sma_cross --data /tmp/btc_365.json --fee_bps 5
  python3 scripts/bot.py --all --data /tmp/btc_365.json        # 全策略对比
"""
import argparse, datetime as dt, glob as _glob, json, math, os, sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_yaml(path):
    """极简 YAML 读取（策略文件是受控格式，免依赖）。"""
    out = {}
    stack = [(-1, out)]
    for line in open(path):
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, val = line.strip().partition(":")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        val = val.strip()
        if val == "":
            d = {}
            parent[key] = d
            stack.append((indent, d))
        else:
            if val.startswith("{") and val.endswith("}"):
                d = {}
                for part in val[1:-1].split(","):
                    k2, _, v2 = part.partition(":")
                    v2 = v2.strip().strip('"')
                    try:
                        d[k2.strip()] = int(v2) if v2.isdigit() else float(v2)
                    except ValueError:
                        d[k2.strip()] = v2
                parent[key] = d
            elif val.startswith('"') and val.endswith('"'):
                parent[key] = val[1:-1]
            else:
                try:
                    parent[key] = int(val) if val.isdigit() else float(val)
                except ValueError:
                    parent[key] = val
    return out


def sma(xs, n):
    out, s = [], 0.0
    for i, x in enumerate(xs):
        s += x
        if i >= n: s -= xs[i - n]
        out.append(s / n if i >= n - 1 else None)
    return out


def ema(xs, n):
    k, out, e = 2 / (n + 1), [], None
    for x in xs:
        e = x if e is None else x * k + e * (1 - k)
        out.append(e)
    return out


def rsi(xs, n=14):
    out, g, l = [None], 0.0, 0.0
    for i in range(1, len(xs)):
        ch = xs[i] - xs[i - 1]
        g = (g * (n - 1) + max(ch, 0)) / n
        l = (l * (n - 1) + max(-ch, 0)) / n
        out.append(100 - 100 / (1 + g / (l + 1e-12)) if i >= n else None)
    return out


def compute_indicators(bars, cfg):
    closes = [b[2] for b in bars]
    highs = [b[3] for b in bars]
    lows = [b[4] for b in bars]
    out = {}
    for name, ic in cfg.items():
        kind, p = ic["kind"], ic
        if kind == "sma":
            out[name] = sma(closes, int(p["period"]))
        elif kind == "rsi":
            out[name] = rsi(closes, int(p.get("period", 14)))
        elif kind == "ema":
            out[name] = ema(closes, int(p["period"]))
        elif kind == "macd":
            out[name] = [ (f - s) if (f is not None and s is not None) else None
                          for f, s in zip(ema(closes, int(p["fast"])), ema(closes, int(p["slow"]))) ]
        elif kind == "donchian_high":
            n = int(p["period"]); out[name] = [max(highs[max(0, i - n):i]) if i >= n else None for i in range(len(bars))]
        elif kind == "donchian_low":
            n = int(p["period"]); out[name] = [min(lows[max(0, i - n):i]) if i >= n else None for i in range(len(bars))]
    out["close"] = closes
    return out


def eval_rule(rule, ind, i):
    env = {k: (v[i - 1] if k.endswith("_prev") else v[i]) for k, v in ind.items()
           if v[i] is not None and (not k.endswith("_prev") or v[i - 1] is not None)}
    if not env or len(env) < len({t.split("_prev")[0] for t in rule.split()} & set(env)):
        return False
    try:
        return eval(rule, {"__builtins__": {}}, env)  # 规则来自受控策略包
    except NameError:
        return False


def run_strategy(bars, strat, fee_bps, initial=100000.0):
    ind = compute_indicators(bars, strat["indicators"])
    for k in list(ind):
        ind[k + "_prev"] = ind[k]
    fee = fee_bps / 10000
    sl = strat.get("stop_loss_pct", 0.08)
    pos, entry, entry_i, cash, trades = 0, None, None, initial, []
    for i in range(2, len(bars)):
        c = bars[i][2]
        if pos == 1:
            if c < entry * (1 - sl):
                cash += c * (1 - fee); trades.append({"entry_bar": entry_i, "exit_bar": i, "entry": round(entry, 2), "exit": round(c, 2), "pnl_pct": round(c / entry - 1, 4), "reason": "stop"}); pos = 0
            elif eval_rule(strat["exit"], ind, i):
                cash += c * (1 - fee); trades.append({"entry_bar": entry_i, "exit_bar": i, "entry": round(entry, 2), "exit": round(c, 2), "pnl_pct": round(c / entry - 1, 4), "reason": "rule"}); pos = 0
        if pos == 0 and eval_rule(strat["entry"], ind, i):
            pos, entry, entry_i = 1, c * (1 + fee), i
            cash -= entry
    final = cash + (bars[-1][2] * (1 - fee) if pos == 1 else 0)
    ret = final / initial - 1
    wins = sum(1 for t in trades if t["pnl_pct"] > 0)
    return {"strategy": strat["name"], "bars": len(bars), "trades": len(trades),
            "win_rate": wins / len(trades) if trades else None,
            "return": round(ret, 4), "final": round(final, 2),
            "stops": sum(1 for t in trades if t["reason"] == "stop"),
            "trade_log": trades}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--strategy")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--data", required=False)
    ap.add_argument("--fee_bps", type=float, default=5.0)
    args = ap.parse_args()
    packs = sorted(_glob.glob(os.path.join(KIT, "strategies", "*.yaml")))
    if args.list:
        for p in packs:
            s = load_yaml(p)
            print(f"{s['name']:<20} {s.get('description', '')[:56]}\n  entry: {s['entry']} | exit: {s['exit']} | stop {s.get('stop_loss_pct')}")
        return
    if not (args.strategy or args.all) or not args.data:
        print(__doc__); sys.exit(2)
    data = json.load(open(args.data))
    symbol, bars = next(iter(data.items()))
    sel = packs if args.all else [os.path.join(KIT, "strategies", args.strategy + ".yaml")]
    results = []
    for p in sel:
        strat = load_yaml(p)
        r = run_strategy(bars, strat, args.fee_bps)
        r["symbol"] = symbol
        results.append(r)
        print(f"· {r['strategy']}: {r['trades']} trades · win {r['win_rate']} · return {r['return']:+.2%} · stops {r['stops']}")
    if args.all:
        bh = bars[-1][2] / bars[0][2] - 1
        print(f"\n基准 buy&hold: {bh:+.2%} · fee {args.fee_bps}bps · bar 级执行（假设随结果）")
        print(json.dumps({"ran_at": dt.datetime.now().isoformat(timespec="seconds"),
                          "assumptions": "bar 级成交+止损按 bar 收盘判定；非投资建议"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
