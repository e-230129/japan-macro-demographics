#!/usr/bin/env python3
"""
日銀の国債保有と財政持続可能性（〜2060年）+ USD/JPY
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
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
# Historical Data (1990-2025)
# =============================================================================
hist_years = np.array([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
jgb_hist = np.array([166, 225, 368, 527, 637, 807, 945, 1080])  # 兆円
boj_hist = np.array([25, 38, 55, 90, 75, 282, 500, 576])  # 兆円
rate_hist = np.array([6.9, 4.8, 2.9, 1.6, 1.3, 1.0, 0.8, 0.9])  # %
tax_hist = np.array([60.1, 52.1, 50.7, 49.1, 41.5, 56.3, 60.8, 75.2])  # 兆円
usdjpy_hist = np.array([145, 94, 108, 110, 88, 121, 107, 157])  # 円/ドル

# =============================================================================
# Projections (2025-2060)
# =============================================================================
proj_years = np.arange(2025, 2065, 5)

# JGB projections
jgb_proj = np.array([1080, 1150, 1220, 1280, 1330, 1370, 1400, 1420])

# BOJ Holdings - 3 scenarios
boj_exit = np.array([576, 500, 400, 320, 260, 220, 200, 180])  # 正常化
boj_hold = np.array([576, 600, 620, 640, 660, 680, 700, 720])  # 現状維持
boj_expand = np.array([576, 650, 750, 850, 950, 1050, 1100, 1150])  # 拡大

# Interest rate scenarios
rate_normal = np.array([0.9, 1.5, 2.0, 2.3, 2.5, 2.5, 2.5, 2.5])  # 正常化
rate_low = np.array([0.9, 1.0, 1.2, 1.3, 1.5, 1.5, 1.5, 1.5])  # 低金利継続

# Tax revenue projection
tax_proj = np.array([75.2, 82, 90, 98, 105, 112, 118, 124])

# USD/JPY scenarios
usdjpy_strong = np.array([157, 145, 135, 130, 125, 120, 118, 115])  # 円高
usdjpy_base = np.array([157, 150, 145, 140, 138, 135, 133, 130])  # 正常化
usdjpy_weak = np.array([157, 165, 175, 185, 195, 200, 200, 200])  # 円安継続
usdjpy_crisis = np.array([157, 180, 200, 220, 240, 250, 250, 250])  # 危機

C = {'good': '#27ae60', 'bad': '#e74c3c', 'warn': '#f39c12', 'blue': '#3498db', 
     'purple': '#9b59b6', 'panel': '#16213e'}

# =============================================================================
# GDP projection for Debt/GDP ratio
# =============================================================================
gdp_2025 = 600  # 兆円
gdp_proj = gdp_2025 * (1.03) ** (np.arange(8) * 5)  # 名目3%成長（統合ダッシュボードと統一）
debt_gdp = jgb_proj / gdp_proj * 100

# =============================================================================
# Figure: 6-Panel Dashboard
# =============================================================================
fig = plt.figure(figsize=(20, 18), facecolor='#0f0f23')
fig.suptitle('日銀の国債買い支えと「出口戦略」シナリオ（〜2060年）\n'
             '+ USD/JPY為替予測',
             fontsize=22, fontweight='bold', color='white', y=0.98)

# =============================================================================
# Key Conclusions Box (Top Left) - 結論3行
# =============================================================================
conclusions = """【結論】デフレ脱却＋名目成長（賃金追随込み）が日銀出口の条件
1. 名目成長3%（賃金追随込み）なら日銀保有13%へ正常化、財政健全化へ
2. 中央（現状維持1%）なら日銀保有51%で金融政策の自由度が低下
3. 悲観（デフレ回帰）・拡大継続なら日銀保有81%、円安250円超、財政危機"""
fig.text(0.02, 0.93, conclusions, fontsize=12, color='white', va='top',
         bbox=dict(facecolor='#1a3a5c', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#3498db'))

# =============================================================================
# Assumptions & Definitions Box (Top Right) - 前提まとめ
# =============================================================================
assumptions = """【前提・定義】FY2024決算ベース
• 税収75.2兆、歳出(総額)123兆、利払費等7.9兆
• PB対象歳出(利払い除き)115兆＝社会保障38＋その他77
• 国債残高: 外生設定（日銀出口シナリオ分析用）
• 利払い: ストレス試算(全残高×金利2.5%/1.5%)
• 為替: 日銀出口成功で円高、失敗で円安
• 「財政危機」＝利払い/税収30%超"""
fig.text(0.68, 0.93, assumptions, fontsize=10, color='white', va='top',
         bbox=dict(facecolor='#2d1f3d', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#9b59b6'))

# =============================================================================
# Panel 1: JGB Outstanding & BOJ Holdings
# =============================================================================
ax1 = fig.add_axes([0.05, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax1.set_title('① 国債残高と日銀保有', color='white', fontsize=15, fontweight='bold')

# Historical
market_hist = jgb_hist - boj_hist
ax1.bar(hist_years, market_hist, width=4, color=C['blue'], alpha=0.7, label='市場保有')
ax1.bar(hist_years, boj_hist, width=4, bottom=market_hist, color=C['bad'], alpha=0.7, label='日銀保有')

# Projection (exit scenario)
market_proj = jgb_proj - boj_exit
ax1.bar(proj_years[1:], market_proj[1:], width=4, color=C['blue'], alpha=0.4, hatch='//')
ax1.bar(proj_years[1:], boj_exit[1:], width=4, bottom=market_proj[1:], color=C['bad'], alpha=0.4, hatch='//')

ax1.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)
ax1.text(2025, 1450, '実績|予測', ha='center', fontsize=12, color='white')

# BOJ share labels
for y, jgb, boj in [(2025, jgb_proj[0], boj_exit[0]), (2040, jgb_proj[3], boj_exit[3]), (2060, jgb_proj[-1], boj_exit[-1])]:
    share = boj / jgb * 100
    ax1.text(y, jgb + 30, f'{share:.0f}%', ha='center', fontsize=12, color=C['bad'])

ax1.set_xlim(1988, 2062); ax1.set_ylim(0, 1550)
ax1.set_xlabel('年', color='white', fontsize=12); ax1.set_ylabel('兆円', color='white', fontsize=12)
ax1.tick_params(colors='white', labelsize=11); ax1.grid(alpha=0.2)
ax1.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)

# =============================================================================
# Panel 2: BOJ Holdings Scenarios
# =============================================================================
ax2 = fig.add_axes([0.37, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax2.set_title('② 日銀保有 シナリオ比較', color='white', fontsize=15, fontweight='bold')

ax2.plot(hist_years, boj_hist, 'o-', color='white', lw=3, markersize=6, label='実績')
ax2.plot(proj_years, boj_exit, 's--', color=C['good'], lw=2.5, markersize=5, label='楽観（出口成功）')
ax2.plot(proj_years, boj_hold, '^--', color=C['warn'], lw=2.5, markersize=5, label='現状維持')
ax2.plot(proj_years, boj_expand, 'v--', color=C['bad'], lw=2.5, markersize=5, label='危機（拡大継続）')

ax2.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)

ax2.set_xlim(1988, 2062); ax2.set_ylim(0, 1250)
ax2.set_xlabel('年', color='white', fontsize=12); ax2.set_ylabel('兆円', color='white', fontsize=12)
ax2.tick_params(colors='white', labelsize=11); ax2.grid(alpha=0.2)
ax2.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)

ax2.text(2058, boj_exit[-1]+40, f'{boj_exit[-1]}兆', color=C['good'], fontsize=12, ha='center')
ax2.text(2058, boj_expand[-1]+40, f'{boj_expand[-1]}兆', color=C['bad'], fontsize=12, ha='center')

# =============================================================================
# Panel 3: USD/JPY Scenarios
# =============================================================================
ax3 = fig.add_axes([0.69, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax3.set_title('③ USD/JPY 為替シナリオ', color='white', fontsize=15, fontweight='bold')

ax3.plot(hist_years, usdjpy_hist, 'o-', color='white', lw=3, markersize=6, label='実績')
ax3.plot(proj_years, usdjpy_strong, 's--', color=C['good'], lw=2.5, markersize=5, label='楽観 (115円)')
ax3.plot(proj_years, usdjpy_base, '^--', color=C['blue'], lw=2.5, markersize=5, label='正常化 (130円)')
ax3.plot(proj_years, usdjpy_weak, 'D--', color=C['warn'], lw=2.5, markersize=5, label='現状維持 (200円)')
ax3.plot(proj_years, usdjpy_crisis, 'v--', color=C['bad'], lw=2.5, markersize=5, label='危機 (250円)')

ax3.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)
ax3.axhline(y=150, color='gray', ls=':', alpha=0.5)

ax3.set_xlim(1988, 2062); ax3.set_ylim(70, 270)
ax3.set_xlabel('年', color='white', fontsize=12); ax3.set_ylabel('円/ドル', color='white', fontsize=12)
ax3.tick_params(colors='white', labelsize=11); ax3.grid(alpha=0.2)
ax3.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=10)
# 為替根拠の注記
ax3.text(0.02, 0.02, '※金利差縮小・出口成功で円高\n  財政不安・出口失敗で円安',
         transform=ax3.transAxes, fontsize=9, color='gray', va='bottom')

# =============================================================================
# Panel 4: Interest Payment Scenarios
# =============================================================================
ax4 = fig.add_axes([0.05, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax4.set_title('④ 利払い費シナリオ', color='white', fontsize=15, fontweight='bold')

# Calculate interest payments
int_hist = jgb_hist * rate_hist / 100
int_normal = jgb_proj * rate_normal / 100
int_low = jgb_proj * rate_low / 100

ax4.bar(hist_years, int_hist, width=4, color=C['warn'], alpha=0.7, label='実績')
ax4.bar(proj_years[1:], int_normal[1:], width=4, color=C['bad'], alpha=0.4, hatch='//', label='正常化(2.5%)')
ax4.plot(proj_years, int_low, 's--', color=C['good'], lw=2.5, markersize=5, label='低金利継続(1.5%)')

ax4.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)

# Danger zone
ax4.axhspan(tax_proj[-1]*0.3, 50, color=C['bad'], alpha=0.1)
ax4.text(2050, 42, '税収の30%超\n(危険ゾーン)', fontsize=11, color=C['bad'], ha='center')

ax4.set_xlim(1988, 2062); ax4.set_ylim(0, 50)
ax4.set_xlabel('年', color='white', fontsize=12); ax4.set_ylabel('利払い費 (兆円)', color='white', fontsize=12)
ax4.tick_params(colors='white', labelsize=11); ax4.grid(alpha=0.2)
ax4.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)

ax4.text(2058, int_normal[-1]+2, f'{int_normal[-1]:.0f}兆', color=C['bad'], fontsize=12, ha='center')
ax4.text(2058, int_low[-1]+2, f'{int_low[-1]:.0f}兆', color=C['good'], fontsize=12, ha='center')

# =============================================================================
# Panel 5: Interest Payment as % of Tax Revenue
# =============================================================================
ax5 = fig.add_axes([0.37, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax5.set_title('⑤ 利払い費 / 税収 比率', color='white', fontsize=15, fontweight='bold')

int_tax_hist = int_hist / tax_hist * 100
int_tax_normal = int_normal / tax_proj * 100
int_tax_low = int_low / tax_proj * 100

ax5.plot(hist_years, int_tax_hist, 'o-', color='white', lw=3, markersize=6, label='実績')
ax5.plot(proj_years, int_tax_normal, 's--', color=C['bad'], lw=2.5, markersize=5, label='正常化シナリオ')
ax5.plot(proj_years, int_tax_low, '^--', color=C['good'], lw=2.5, markersize=5, label='低金利継続')

ax5.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)
ax5.axhline(y=20, color=C['warn'], ls=':', lw=2, alpha=0.7)
ax5.axhline(y=30, color=C['bad'], ls=':', lw=2, alpha=0.7)
ax5.text(2000, 21, '警戒ライン 20%', fontsize=11, color=C['warn'])
ax5.text(2000, 31, '危機ライン 30%', fontsize=11, color=C['bad'])

ax5.set_xlim(1988, 2062); ax5.set_ylim(0, 35)
ax5.set_xlabel('年', color='white', fontsize=12); ax5.set_ylabel('利払い費/税収 (%)', color='white', fontsize=12)
ax5.tick_params(colors='white', labelsize=11); ax5.grid(alpha=0.2)
ax5.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=11)

ax5.text(2058, int_tax_normal[-1]+1.5, f'{int_tax_normal[-1]:.0f}%', color=C['bad'], fontsize=12, ha='center')
ax5.text(2058, int_tax_low[-1]+1.5, f'{int_tax_low[-1]:.0f}%', color=C['good'], fontsize=12, ha='center')

# =============================================================================
# Panel 6: Summary & Scenarios with Debt/GDP
# =============================================================================
ax6 = fig.add_axes([0.69, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax6.set_title('⑥ 2060年シナリオまとめ', color='white', fontsize=15, fontweight='bold')
ax6.axis('off')
ax6.set_xlim(0, 10); ax6.set_ylim(0, 10)

scenarios = [
    ('【楽観シナリオ】', C['good'], [
        '条件: 名目成長3%(賃金追随)',
        '日銀保有: 180兆円 (13%)',
        f'債務/GDP: {debt_gdp[-1]:.0f}%、USD/JPY: 115-130円',
    ]),
    ('【現状維持】', C['warn'], [
        '日銀保有: 720兆円 (51%)',
        '利払い: 21兆円、USD/JPY: 180-200円',
    ]),
    ('【危機シナリオ】', C['bad'], [
        '条件: 名目成長なし',
        '日銀保有: 1150兆円 (81%)',
        'USD/JPY: 250円超、財政危機リスク大',
    ]),
]

y = 9.5
for title, color, items in scenarios:
    ax6.text(0.3, y, title, fontsize=12, color=color, fontweight='bold')
    y -= 0.5
    for item in items:
        ax6.text(0.5, y, item, fontsize=10, color='white')
        y -= 0.5
    y -= 0.2

# Key insight
ax6.text(5, 0.8, '鍵: 名目成長3%達成 → 日銀出口 → 円安是正', ha='center', fontsize=12,
         color='white', bbox=dict(facecolor=C['blue'], alpha=0.5, boxstyle='round'))

# Footer
footer = ("【結論】名目成長3%（賃金追随）達成なら日銀出口成功→財政正常化・円高へ。"
          "名目成長なしなら日銀保有拡大・円安加速・財政危機リスク上昇。")
fig.text(0.5, 0.01, footer, ha='center', fontsize=12, color='#cccccc', style='italic')

plt.savefig('boj_fiscal_2060_v2.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Created boj_fiscal_2060_v2.png")
