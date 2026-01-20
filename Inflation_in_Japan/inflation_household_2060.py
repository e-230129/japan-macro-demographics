#!/usr/bin/env python3
"""
年2%インフレが年収500万円の人に与える影響（〜2060年版）+ USD/JPY
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

# Data - Extended to 2060
start_year = 2026
years = np.arange(0, 35)  # 0-34年 (2026-2060)
inflation = 0.02

# 物価水準（2026年=100）
price = 100 * (1 + inflation) ** years

# 名目年収
initial_income = 500  # 万円
income_up = initial_income * (1 + inflation) ** years  # 賃金連動
income_flat = np.full(35, float(initial_income))  # 賃金据置

# 実質購買力（2026年=100として正規化）
real_up = (income_up / price) / (initial_income / 100) * 100
real_flat = (income_flat / price) / (initial_income / 100) * 100

# USD/JPY projection (base case: gradual normalization from 157 to 130)
usdjpy_2026 = 157
usdjpy_2060_base = 130
usdjpy_base = usdjpy_2026 - (usdjpy_2026 - usdjpy_2060_base) * (years / 34)

usdjpy_2060_weak = 200
usdjpy_weak = usdjpy_2026 + (usdjpy_2060_weak - usdjpy_2026) * (years / 34)

# Dollar-denominated income (万ドル)
income_usd_up = income_up / usdjpy_base * 100  # Index (2026=100)
income_usd_flat = income_flat / usdjpy_base * 100
income_usd_weak_up = income_up / usdjpy_weak * 100
income_usd_weak_flat = income_flat / usdjpy_weak * 100

C = {'good': '#27ae60', 'bad': '#e74c3c', 'warn': '#f39c12', 'blue': '#3498db', 'panel': '#16213e'}

# =============================================================================
# Create figure - 6 panels
# =============================================================================
fig = plt.figure(figsize=(20, 18), facecolor='#0f0f23')
fig.suptitle('年2%インフレが「年収500万円」の生活に与える影響（2026年→2060年）\n'
             '+ USD/JPY為替の影響',
             fontsize=22, fontweight='bold', color='white', y=0.98)

# =============================================================================
# Key Conclusions Box (Top Left) - 結論3行
# =============================================================================
conclusions = """【結論】鍵は「賃金追随」- インフレ下での生活防衛
1. 34年後に物価は約2倍：賃金追随なしだと実質購買力は51%に低下
2. 賃金追随+円高シナリオならドル建て所得は159%に上昇
3. 賃金停滞+円安シナリオならドル建て所得は40%に激減（60%減）"""
fig.text(0.02, 0.93, conclusions, fontsize=12, color='white', va='top',
         bbox=dict(facecolor='#1a3a5c', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#3498db'))

# =============================================================================
# Assumptions & Definitions Box (Top Right) - 前提まとめ
# =============================================================================
assumptions = """【前提・定義】
• インフレ: 年率2%で継続
• 賃金連動: 賃金もインフレ率と同率で上昇
• 賃金据置: 名目賃金が固定（実質減少）
• 為替: 楽観130円/危機200円（シナリオ仮置き）
• ※金利差縮小・経常黒字で円高、
  財政不安・金融緩和継続で円安"""
fig.text(0.70, 0.93, assumptions, fontsize=11, color='white', va='top',
         bbox=dict(facecolor='#2d1f3d', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#9b59b6'))

# Panel 1: 物価と名目年収
ax1 = fig.add_axes([0.05, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax1.set_title('① 物価と名目年収', color='white', fontsize=15, fontweight='bold')
ax1.fill_between(start_year + years, 0, price, color=C['bad'], alpha=0.2)
ax1.plot(start_year + years, price, color=C['bad'], lw=2, label='物価水準')
ax1.plot(start_year + years, income_up/5, 'o-', color=C['good'], lw=2, markersize=3, label='賃金連動', markevery=5)
ax1.plot(start_year + years, income_flat/5, 's--', color=C['bad'], lw=2, markersize=3, label='賃金据置', markevery=5)
ax1.set_xlim(2026, 2060); ax1.set_ylim(0, 210)
ax1.set_xlabel('年', color='white', fontsize=12); ax1.set_ylabel('指数 (2026=100)', color='white', fontsize=12)
ax1.tick_params(colors='white', labelsize=11); ax1.grid(alpha=0.2)
ax1.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)
ax1.text(2058, 200, '物価\n1.97倍', color=C['bad'], fontsize=12, ha='center')

# Panel 2: 実質購買力
ax2 = fig.add_axes([0.37, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax2.set_title('② 実質購買力（円建て）', color='white', fontsize=15, fontweight='bold')
ax2.fill_between(start_year + years, 40, real_flat, color=C['bad'], alpha=0.2)
ax2.plot(start_year + years, real_flat, '-', color=C['bad'], linewidth=3, label='賃金据置→低下')
ax2.plot(start_year + years[::5], real_flat[::5], 's', color=C['bad'], markersize=8)
ax2.plot(start_year + years, real_up, '-', color=C['good'], linewidth=3, label='賃金連動→維持')
ax2.plot(start_year + years[::5], real_up[::5], 'o', color=C['good'], markersize=8)
ax2.axhline(100, color='white', ls='--', alpha=0.5, lw=1.5)

for m in [10, 20, 34]:
    y_val = real_flat[m]
    ax2.plot(start_year+m, y_val, 'o', color='white', markersize=12)
    ax2.plot(start_year+m, y_val, 'o', color=C['bad'], markersize=8)
    ax2.text(start_year+m, y_val-6, f'{y_val:.0f}%', ha='center', color='white', fontsize=12, fontweight='bold')

ax2.set_xlim(2026, 2060); ax2.set_ylim(40, 115)
ax2.set_xlabel('年', color='white', fontsize=12); ax2.set_ylabel('実質購買力 (%)', color='white', fontsize=12)
ax2.tick_params(colors='white', labelsize=11); ax2.grid(alpha=0.2)
ax2.legend(loc='lower left', facecolor=C['panel'], labelcolor='white', fontsize=11)
ax2.text(0.97, 0.95, '34年後\n購買力51%', transform=ax2.transAxes, va='top', ha='right',
         color='white', fontsize=12, bbox=dict(facecolor=C['bad'], alpha=0.4, boxstyle='round'))

# Panel 3: USD/JPY予測
ax3 = fig.add_axes([0.69, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax3.set_title('③ USD/JPY 為替レート予測', color='white', fontsize=15, fontweight='bold')
ax3.plot(start_year + years, usdjpy_base, 'o-', color=C['good'], linewidth=3, markersize=4,
         label='楽観シナリオ', markevery=5)
ax3.plot(start_year + years, usdjpy_weak, 's-', color=C['bad'], linewidth=3, markersize=4,
         label='危機シナリオ', markevery=5)
ax3.axhline(150, color='white', ls=':', alpha=0.5)
ax3.text(2030, 153, '150円ライン', color='white', fontsize=11, alpha=0.7)

ax3.set_xlim(2026, 2060); ax3.set_ylim(100, 220)
ax3.set_xlabel('年', color='white', fontsize=12); ax3.set_ylabel('円/ドル', color='white', fontsize=12)
ax3.tick_params(colors='white', labelsize=11); ax3.grid(alpha=0.2)
ax3.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)

ax3.text(2058, usdjpy_base[-1]+5, f'{usdjpy_base[-1]:.0f}円', color=C['good'], fontsize=12, ha='center')
ax3.text(2058, usdjpy_weak[-1]+5, f'{usdjpy_weak[-1]:.0f}円', color=C['bad'], fontsize=12, ha='center')

# Panel 4: ドル建て所得（楽観シナリオ）
ax4 = fig.add_axes([0.05, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax4.set_title('④ ドル建て所得（楽観シナリオ）', color='white', fontsize=15, fontweight='bold')

# Calculate actual USD values
income_usd_up_actual = income_up / usdjpy_base  # 万ドル
income_usd_flat_actual = income_flat / usdjpy_base

# Index (2026=100)
income_usd_up_idx = income_usd_up_actual / income_usd_up_actual[0] * 100
income_usd_flat_idx = income_usd_flat_actual / income_usd_flat_actual[0] * 100

ax4.plot(start_year + years, income_usd_up_idx, 'o-', color=C['good'], linewidth=3, markersize=4,
         label='賃金連動', markevery=5)
ax4.plot(start_year + years, income_usd_flat_idx, 's-', color=C['warn'], linewidth=3, markersize=4,
         label='賃金据置', markevery=5)
ax4.axhline(100, color='white', ls='--', alpha=0.5)

ax4.set_xlim(2026, 2060); ax4.set_ylim(60, 180)
ax4.set_xlabel('年', color='white', fontsize=12); ax4.set_ylabel('ドル建て所得指数 (2026=100)', color='white', fontsize=12)
ax4.tick_params(colors='white', labelsize=11); ax4.grid(alpha=0.2)
ax4.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)

ax4.text(0.97, 0.95, '円高で\nドル建て所得↑', transform=ax4.transAxes, va='top', ha='right',
         color='white', fontsize=12, bbox=dict(facecolor=C['good'], alpha=0.4, boxstyle='round'))

# Panel 5: ドル建て所得（危機シナリオ）
ax5 = fig.add_axes([0.37, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax5.set_title('⑤ ドル建て所得（危機シナリオ）', color='white', fontsize=15, fontweight='bold')

income_usd_weak_up_actual = income_up / usdjpy_weak
income_usd_weak_flat_actual = income_flat / usdjpy_weak

income_usd_weak_up_idx = income_usd_weak_up_actual / income_usd_weak_up_actual[0] * 100
income_usd_weak_flat_idx = income_usd_weak_flat_actual / income_usd_weak_flat_actual[0] * 100

ax5.fill_between(start_year + years, 40, income_usd_weak_flat_idx, color=C['bad'], alpha=0.2)
ax5.plot(start_year + years, income_usd_weak_up_idx, 'o-', color=C['warn'], linewidth=3, markersize=4,
         label='賃金連動', markevery=5)
ax5.plot(start_year + years, income_usd_weak_flat_idx, 's-', color=C['bad'], linewidth=3, markersize=4,
         label='賃金据置', markevery=5)
ax5.axhline(100, color='white', ls='--', alpha=0.5)

for m in [17, 34]:  # 10年後、34年後
    y_val = income_usd_weak_flat_idx[m]
    ax5.plot(start_year+m, y_val, 'o', color='white', markersize=10)
    ax5.plot(start_year+m, y_val, 'o', color=C['bad'], markersize=7)
    ax5.text(start_year+m, y_val-5, f'{y_val:.0f}%', ha='center', color='white', fontsize=12, fontweight='bold')

ax5.set_xlim(2026, 2060); ax5.set_ylim(30, 120)
ax5.set_xlabel('年', color='white', fontsize=12); ax5.set_ylabel('ドル建て所得指数 (2026=100)', color='white', fontsize=12)
ax5.tick_params(colors='white', labelsize=11); ax5.grid(alpha=0.2)
ax5.legend(loc='lower left', facecolor=C['panel'], labelcolor='white', fontsize=11)

ax5.text(0.97, 0.95, '円安+賃金停滞で\nドル建て所得激減', transform=ax5.transAxes, va='top', ha='right',
         color='white', fontsize=12, bbox=dict(facecolor=C['bad'], alpha=0.5, boxstyle='round'))

# Panel 6: Summary Table
ax6 = fig.add_axes([0.69, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax6.set_title('⑥ 2060年時点のまとめ', color='white', fontsize=15, fontweight='bold')
ax6.axis('off')
ax6.set_xlim(0, 10); ax6.set_ylim(0, 10)

# Summary data
summary_data = [
    ('物価水準', '197 (約2倍)', C['bad']),
    ('', '', 'white'),
    ('【賃金連動の場合】', '', C['good']),
    ('名目年収', '985万円', C['good']),
    ('円建て購買力', '100%維持', C['good']),
    ('ドル建て(楽観)', '159%', C['good']),
    ('ドル建て(危機)', '78%', C['warn']),
    ('', '', 'white'),
    ('【賃金据置の場合】', '', C['bad']),
    ('名目年収', '500万円', C['bad']),
    ('円建て購買力', '51%に低下', C['bad']),
    ('ドル建て(楽観)', '122%', C['warn']),
    ('ドル建て(危機)', '40%', C['bad']),
]

y = 9.5
for label, value, color in summary_data:
    if label:
        ax6.text(0.5, y, label, fontsize=12, color=color, fontweight='bold' if '【' in label else 'normal')
        if value:
            ax6.text(6.5, y, value, fontsize=12, color=color, ha='left')
    y -= 0.7

# Key message
ax6.text(5, 0.8, '最悪シナリオ:\n賃金据置×円安でドル建て所得60%減', ha='center', fontsize=12,
         color='white', bbox=dict(facecolor=C['bad'], alpha=0.5, boxstyle='round'))

# Footer
footer = ("【結論】2060年までに物価は約2倍。賃金追随なしだと円建てで購買力半減、円安も進めばドル建てで60%減。\n"
          "インフレと円安の「ダブルパンチ」を避けるには、名目成長に連動した賃金上昇が不可欠。")
fig.text(0.5, 0.01, footer, ha='center', fontsize=12, color='#cccccc', style='italic')

plt.savefig('inflation_household_2060_v2.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Created inflation_household_2060_v2.png")
