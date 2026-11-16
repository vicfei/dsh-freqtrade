# ROADMAP — dsh-freqtrade

北极星：十二仓家族的策略机器人位，吃 freqtrade 57k★+strategies 5.7k★ 流量，
30 天 100–300★。命名全表面：GitHub=npm=dsh-freqtrade（镜像上游小写仓名）。

## 许可红线（GPL-3.0 上游，owner 铁律执行）

零 import / 零进程包装 / 不 vendored，连"用户自装上游我们包壳"的隔离变通
也不做。借鉴=产品思路（声明式策略+策略集+运行器）；实盘执行接家族 ccxt
护栏桥。差异化卖点=**GPL-free 的 freqtrade 概念**（企业可用的那一份）。

## 里程碑

### M0 ✅（2026-11-17）
策略包 4 策略（SMA 交叉/RSI 回归/唐奇安突破/MACD 动量，声明式 YAML+
止损）+ 统一运行器（含费/止损/bar 级标注/交易日志）。真实冒烟：BTC 365d
熊年四策略对比——突破 +2.6% 领先、均值回归 -15.1% 垫底（风格敏感性教学）。

### M0.5 · 发布包
- [ ] README 打磨 + 四策略对比表截图 + npm 0.0.1 占位（owner 手动）
- [ ] 公开仓 topics + 家族互链 + marketplace + 渠道（GPL-free 卖点单列）

### M1 · DSL 与纸面循环（第 2-3 周）
- [ ] 规则 DSL 加固（trailing stop/多条件/仓位比例）+ 策略校验器
- [ ] dry-run 纸面循环（实时数据定时跑，虚拟仓位——freqtrade dry-run 思想）
- [ ] 策略包扩充（社区贡献通道——freqtrade-strategies 的自研版）

### M2 · 实盘（第 4-6 周）
- [ ] 经家族 ccxt 护栏桥的受护栏实盘（三重解锁+名义额+白名单+
      近期纸面/回测通过为前置）——永不接 freqtrade 本体

### M3 · 生态（第 2 月起）
- [ ] 策略跑分榜（家族栈流水线：bot → jesse 调参 → quantstats 成绩单）
- [ ] 策略格式标准（STRATEGY-PACK，家族格式第七件）

## 纪律（不可让步）

- GPL 红线（零上游代码关系）；bar 级标注随结果；
- 策略≠已验证的 edge（推荐 jesse 调参+quantstats 报告再信）；不做投资建议。
