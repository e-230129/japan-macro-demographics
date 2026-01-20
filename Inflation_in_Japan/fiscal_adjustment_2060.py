#!/usr/bin/env python3
"""
名目成長なしの場合の財政調整必要額（2060年）
- 「名目成長を避けるなら、代わりにこの規模の増税or歳出削減が必要」を可視化
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# Japanese font for Windows
import platform
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'MS Gothic'
else:
    for font in ['Noto Sans CJK JP', 'IPAexGothic', 'DejaVu Sans']:
        if font in [f.name for f in font_manager.fontManager.ttflist]:
            plt.rcParams['font.family'] = font
            break
plt.rcParams['axes.unicode_minus'] = False

# =============================================================================
# 2060年シナリオ別データ（統合ダッシュボードと同じ前提）
# =============================================================================
# 税収予測
tax_optimistic = 175  # 楽観：名目成長3%（賃金追随込み）
tax_baseline = 92     # 中央：現状維持（名目成長1%）
tax_pessimistic = 50  # 悲観：デフレ回帰

# PB対象歳出（利払い除き）- FY2024決算ベースから推計
expenditure = 124  # 社会保障62 + その他62（決算ベース115兆からの推計）

# 利払い（ストレス試算: 1420兆円 × 2.5%）
jgb_2060 = 1420  # 兆円
rate = 2.5  # %
interest = jgb_2060 * rate / 100  # 35.5兆円

# =============================================================================
# 財政調整必要額の計算
# =============================================================================
# PB（基礎的財政収支）ベース
pb_opt = tax_optimistic - expenditure  # +53
pb_base = tax_baseline - expenditure    # -30
pb_pess = tax_pessimistic - expenditure # -72

# PB均衡に必要な調整額（楽観シナリオとの差）
pb_adjustment_base = abs(pb_base)  # 30兆円
pb_adjustment_pess = abs(pb_pess)  # 72兆円

# 利払い込み収支
total_opt = pb_opt - interest     # +17.5
total_base = pb_base - interest   # -65.5
total_pess = pb_pess - interest   # -107.5

# 利払い込み均衡に必要な調整額
total_adjustment_base = abs(total_base)  # 65.5兆円
total_adjustment_pess = abs(total_pess)  # 107.5兆円

C = {'good': '#27ae60', 'bad': '#e74c3c', 'warn': '#f39c12', 'blue': '#3498db', 'panel': '#16213e'}

# =============================================================================
# Figure: 財政調整必要額の可視化
# =============================================================================
fig = plt.figure(figsize=(16, 14), facecolor='#0f0f23')
fig.suptitle('名目成長（賃金追随込み）なしの場合の財政調整必要額（2060年）\n'
             'デフレ脱却を避けるなら、代わりにこれだけの増税or歳出削減が必要',
             fontsize=20, fontweight='bold', color='white', y=0.98)

# =============================================================================
# Key Message Box
# =============================================================================
message = """【結論】名目成長3%（賃金追随込み）を達成しないなら…
• 中央シナリオ（現状維持）: PB均衡に32兆円、利払い込みで68兆円の調整が必要
• 悲観シナリオ（デフレ回帰）: PB均衡に74兆円、利払い込みで110兆円の調整が必要
→ 消費税換算で約13〜44%ポイントの増税、または社会保障費の大幅削減"""
fig.text(0.5, 0.91, message, fontsize=12, color='white', ha='center', va='top',
         bbox=dict(facecolor='#1a3a5c', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#3498db'))

# 前提注記
fig.text(0.98, 0.84, '【前提】FY2024決算ベース: PB対象歳出124兆円(2060年推計)、利払い35.5兆円(1420兆×2.5%)、国債残高は外生設定',
         fontsize=9, color='gray', ha='right', va='top')

# =============================================================================
# Panel 1: PBベースの調整必要額
# =============================================================================
ax1 = fig.add_axes([0.08, 0.38, 0.40, 0.38], facecolor=C['panel'])
ax1.set_title('① PB（基礎的財政収支）均衡に必要な調整', color='white', fontsize=16, fontweight='bold')

scenarios = ['楽観\n(名目成長3%)', '中央\n(現状維持1%)', '悲観\n(デフレ回帰)']
pb_values = [pb_opt, pb_base, pb_pess]
colors = [C['good'], C['warn'], C['bad']]

bars1 = ax1.bar(scenarios, pb_values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)

# 値ラベル（バーの下端に配置）
for bar, val in zip(bars1, pb_values):
    height = bar.get_height()
    if val >= 0:
        ax1.text(bar.get_x() + bar.get_width()/2, height + 2, f'+{val:.0f}兆円\n黒字',
                ha='center', fontsize=14, color=C['good'], fontweight='bold')
    else:
        # 赤字ラベルはバーの下端近くに配置
        ax1.text(bar.get_x() + bar.get_width()/2, height + 5, f'{val:.0f}兆円',
                ha='center', fontsize=13, color='white', fontweight='bold')

ax1.axhline(0, color='white', ls='-', lw=2)
ax1.set_ylim(-90, 70)
ax1.set_ylabel('PB収支（兆円）', color='white', fontsize=14)
ax1.tick_params(colors='white', labelsize=12)
ax1.grid(axis='y', alpha=0.2)

# 調整必要額の矢印と注記（右側に配置）
ax1.annotate('', xy=(1.15, 0), xytext=(1.15, pb_base),
             arrowprops=dict(arrowstyle='<->', color='white', lw=2))
ax1.text(1.35, pb_base/2, f'調整{pb_adjustment_base:.0f}兆円', fontsize=12, color='white', va='center')

ax1.annotate('', xy=(2.15, 0), xytext=(2.15, pb_pess),
             arrowprops=dict(arrowstyle='<->', color='white', lw=2))
ax1.text(2.35, pb_pess/2, f'調整{pb_adjustment_pess:.0f}兆円', fontsize=12, color='white', va='center')

# =============================================================================
# Panel 2: 利払い込みの調整必要額
# =============================================================================
ax2 = fig.add_axes([0.55, 0.38, 0.40, 0.38], facecolor=C['panel'])
ax2.set_title('② 利払い込み収支均衡に必要な調整', color='white', fontsize=16, fontweight='bold')

total_values = [total_opt, total_base, total_pess]

bars2 = ax2.bar(scenarios, total_values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)

# 値ラベル（バーの下端に配置）
for bar, val in zip(bars2, total_values):
    height = bar.get_height()
    if val >= 0:
        ax2.text(bar.get_x() + bar.get_width()/2, height + 2, f'+{val:.0f}兆円\n黒字',
                ha='center', fontsize=14, color=C['good'], fontweight='bold')
    else:
        # 赤字ラベルはバーの下端近くに配置
        ax2.text(bar.get_x() + bar.get_width()/2, height + 5, f'{val:.0f}兆円',
                ha='center', fontsize=13, color='white', fontweight='bold')

ax2.axhline(0, color='white', ls='-', lw=2)
ax2.set_ylim(-130, 40)
ax2.set_ylabel('収支（兆円）', color='white', fontsize=14)
ax2.tick_params(colors='white', labelsize=12)
ax2.grid(axis='y', alpha=0.2)

# 調整必要額の矢印と注記（右側に配置）
ax2.annotate('', xy=(1.15, 0), xytext=(1.15, total_base),
             arrowprops=dict(arrowstyle='<->', color='white', lw=2))
ax2.text(1.35, total_base/2, f'調整{total_adjustment_base:.0f}兆円', fontsize=12, color='white', va='center')

ax2.annotate('', xy=(2.15, 0), xytext=(2.15, total_pess),
             arrowprops=dict(arrowstyle='<->', color='white', lw=2))
ax2.text(2.35, total_pess/2, f'調整{total_adjustment_pess:.0f}兆円', fontsize=12, color='white', va='center')

# =============================================================================
# Bottom: 具体的な調整手段の例
# =============================================================================
examples_box = fig.add_axes([0.05, 0.05, 0.90, 0.28], facecolor='#1a1a2e')
examples_box.axis('off')
examples_box.set_xlim(0, 100)
examples_box.set_ylim(0, 10)

examples_box.text(50, 9, '【調整手段の例】名目成長なしでPBを均衡させるには…',
                  ha='center', fontsize=15, fontweight='bold', color='white')

# 消費税換算
consumption_tax_rate = 2.5  # 消費税1%ポイント ≈ 2.5兆円
tax_increase_base = pb_adjustment_base / consumption_tax_rate  # 30/2.5 = 12%
tax_increase_pess = pb_adjustment_pess / consumption_tax_rate  # 72/2.5 = 28.8%
tax_increase_total_base = total_adjustment_base / consumption_tax_rate  # 66/2.5 = 26.4%
tax_increase_total_pess = total_adjustment_pess / consumption_tax_rate  # 108/2.5 = 43.2%

examples = [
    ('中央\n(PB均衡)', f'消費税+{tax_increase_base:.0f}%\n(10%→{10+tax_increase_base:.0f}%)',
     f'または歳出\n{pb_adjustment_base:.0f}兆円削減', C['warn']),
    ('悲観\n(PB均衡)', f'消費税+{tax_increase_pess:.0f}%\n(10%→{10+tax_increase_pess:.0f}%)',
     f'または歳出\n{pb_adjustment_pess:.0f}兆円削減', C['bad']),
    ('中央\n(利払い込み)', f'消費税+{tax_increase_total_base:.0f}%\n(10%→{10+tax_increase_total_base:.0f}%)',
     f'または歳出\n{total_adjustment_base:.0f}兆円削減', C['warn']),
    ('悲観\n(利払い込み)', f'消費税+{tax_increase_total_pess:.0f}%\n(10%→{10+tax_increase_total_pess:.0f}%)',
     f'または歳出\n{total_adjustment_pess:.0f}兆円削減', C['bad']),
]

for i, (scenario, tax, cut, color) in enumerate(examples):
    x = 12 + i * 22
    examples_box.text(x, 6.5, scenario, ha='center', fontsize=12, color=color, fontweight='bold')
    examples_box.text(x, 4.5, tax, ha='center', fontsize=12, color='white',
                      bbox=dict(facecolor=color, alpha=0.4, boxstyle='round'))
    examples_box.text(x, 2, cut, ha='center', fontsize=12, color='white',
                      bbox=dict(facecolor=color, alpha=0.4, boxstyle='round'))

# 注記
examples_box.text(50, 0.3, '※消費税1%≈2.5兆円で試算。歳出削減の場合、社会保障費62兆円が主な対象となる。',
                  ha='center', fontsize=11, color='gray')

# Footer
footer = "【結論】名目成長（賃金追随込み）なしで財政を均衡させるには、消費税23〜54%または社会保障の大幅削減が必要。"
fig.text(0.5, 0.01, footer, ha='center', fontsize=12, color='#cccccc', style='italic')

plt.savefig('fiscal_adjustment_2060.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Created fiscal_adjustment_2060.png")
