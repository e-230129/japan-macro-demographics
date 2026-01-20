#!/usr/bin/env python3
"""
日本財政・税収・インフレ・為替の統合ダッシュボード（〜2060年）
Integrated Japan Fiscal Dashboard with Tax Revenue Projections
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
# Data
# =============================================================================
hist_years = np.array([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
proj_years = np.arange(2025, 2065, 5)

# JGB & BOJ
jgb_hist = np.array([166, 225, 368, 527, 637, 807, 945, 1080])
boj_hist = np.array([25, 38, 55, 90, 75, 282, 500, 576])
jgb_proj = np.array([1080, 1150, 1220, 1280, 1330, 1370, 1400, 1420])
boj_exit = np.array([576, 500, 400, 320, 260, 220, 200, 180])

# Interest rates
rate_hist = np.array([6.9, 4.8, 2.9, 1.6, 1.3, 1.0, 0.8, 0.9])
rate_proj = np.array([0.9, 1.5, 2.0, 2.3, 2.5, 2.5, 2.5, 2.5])

# Tax Revenue
tax_hist = np.array([60.1, 52.1, 50.7, 49.1, 41.5, 56.3, 60.8, 75.2])
tax_optimistic = np.array([75.2, 87, 100, 115, 130, 145, 160, 175])
tax_baseline = np.array([75.2, 80, 85, 88, 90, 91, 92, 92])
tax_pessimistic = np.array([75.2, 73, 70, 66, 62, 58, 54, 50])

# Expenditure (PB対象歳出 = 決算歳出総額123兆 - 利払費等7.9兆 ≈ 115兆)
social_security_proj = np.array([38.0, 42, 47, 52, 56, 59, 61, 62])
other_exp = np.array([77.0, 75, 73, 71, 69, 67, 64, 62])  # 決算ベースに修正
expenditure_proj = social_security_proj + other_exp  # 2025: 115兆, 2060: 124兆

# Interest payments
interest_hist = jgb_hist * rate_hist / 100
interest_proj = jgb_proj * rate_proj / 100

# USD/JPY
usdjpy_hist = np.array([145, 94, 108, 110, 88, 121, 107, 157])
usdjpy_base = np.array([157, 150, 145, 140, 138, 135, 133, 130])
usdjpy_weak = np.array([157, 165, 175, 185, 195, 200, 200, 200])

# Working-age population (15-64歳比率) - IPSS 2023年推計に基づく
working_age_hist = np.array([69.5, 69.4, 67.9, 65.8, 63.7, 60.6, 59.2, 59.3])
working_age_proj = np.array([59.3, 58.5, 56.9, 55.4, 54.1, 53.5, 53.1, 52.8])

C = {'good': '#27ae60', 'bad': '#e74c3c', 'warn': '#f39c12', 'blue': '#3498db', 
     'purple': '#9b59b6', 'panel': '#16213e'}

# =============================================================================
# GDP projection for Debt/GDP ratio
# =============================================================================
gdp_2025 = 600  # 兆円
gdp_proj_opt = gdp_2025 * (1.03) ** (np.arange(8) * 5)  # 楽観: 名目3%成長
gdp_proj_base = gdp_2025 * (1.01) ** (np.arange(8) * 5)  # 現状維持: 名目1%成長
debt_gdp_opt = jgb_proj / gdp_proj_opt * 100
debt_gdp_base = jgb_proj / gdp_proj_base * 100

# =============================================================================
# Figure 1: 8-Panel Comprehensive Dashboard
# =============================================================================
fig = plt.figure(figsize=(22, 20), facecolor='#0f0f23')
fig.suptitle('日本財政の長期展望 — 統合ダッシュボード（〜2060年）\n'
             '国債・税収・利払い・人口・為替の相互関係',
             fontsize=24, fontweight='bold', color='white', y=0.98)

# =============================================================================
# Key Conclusions Box (Top Left) - 結論3行
# =============================================================================
conclusions = """【結論】デフレ脱却＋名目成長（賃金追随）がないと、利払い/税収が危険域へ
1. 名目成長3%（賃金追随込み）なら税収175兆円、PB黒字+51兆円
2. 名目成長なしなら、PB均衡に33〜74兆円の増税or歳出削減が必要
3. 「財政危機」＝利払い/税収30%超（悲観シナリオで71%到達）"""
fig.text(0.02, 0.94, conclusions, fontsize=12, color='white', va='top',
         bbox=dict(facecolor='#1a3a5c', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#3498db'))

# =============================================================================
# Assumptions & Definitions Box (Top Right) - 前提まとめ
# =============================================================================
assumptions = """【前提・定義】FY2024決算ベース
• 税収75.2兆、歳出(総額)123兆、利払費等7.9兆
• PB対象歳出(利払い除き)115兆＝社会保障38＋その他77
• 国債残高: 外生設定（税収・PBへの感度分析用）
• 利払い: ストレス試算(全残高×2.5%で統一)
  ※金利は全シナリオ固定、税収感度のみ分析
• 人口: 生産年齢15-64歳比率(IPSS 2023推計)
• 「財政危機」＝利払い/税収30%超"""
fig.text(0.75, 0.94, assumptions, fontsize=10, color='white', va='top',
         bbox=dict(facecolor='#2d1f3d', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#9b59b6'))

# Panel positions (4x2 grid) - adjusted for conclusion/assumption boxes
panels = [
    [0.05, 0.62, 0.21, 0.18],  # 1
    [0.29, 0.62, 0.21, 0.18],  # 2
    [0.53, 0.62, 0.21, 0.18],  # 3
    [0.77, 0.62, 0.21, 0.18],  # 4
    [0.05, 0.34, 0.21, 0.22],  # 5
    [0.29, 0.34, 0.21, 0.22],  # 6
    [0.53, 0.34, 0.21, 0.22],  # 7
    [0.77, 0.34, 0.21, 0.22],  # 8
]

# =============================================================================
# Panel 1: 国債残高
# =============================================================================
ax1 = fig.add_axes(panels[0], facecolor=C['panel'])
ax1.set_title('① 国債残高', color='white', fontsize=14, fontweight='bold')

market_hist = jgb_hist - boj_hist
market_proj = jgb_proj - boj_exit
ax1.bar(hist_years, market_hist, width=4, color=C['blue'], alpha=0.7)
ax1.bar(hist_years, boj_hist, width=4, bottom=market_hist, color=C['bad'], alpha=0.7)
ax1.bar(proj_years[1:], market_proj[1:], width=4, color=C['blue'], alpha=0.4, hatch='//')
ax1.bar(proj_years[1:], boj_exit[1:], width=4, bottom=market_proj[1:], color=C['bad'], alpha=0.4, hatch='//')

ax1.axvline(x=2025, color='white', ls='--', lw=1.5, alpha=0.7)
ax1.set_xlim(1988, 2062); ax1.set_ylim(0, 1500)
ax1.set_ylabel('兆円', color='white', fontsize=12)
ax1.tick_params(colors='white', labelsize=11); ax1.grid(alpha=0.2)
ax1.text(2060, jgb_proj[-1]+50, f'{jgb_proj[-1]}兆', color='white', fontsize=11, ha='center')

# =============================================================================
# Panel 2: 税収予測シナリオ
# =============================================================================
ax2 = fig.add_axes(panels[1], facecolor=C['panel'])
ax2.set_title('② 税収予測シナリオ', color='white', fontsize=14, fontweight='bold')

ax2.plot(hist_years, tax_hist, 'o-', color='white', lw=2, markersize=4)
ax2.plot(proj_years, tax_optimistic, 's--', color=C['good'], lw=2, markersize=3, label='楽観')
ax2.plot(proj_years, tax_baseline, '^--', color=C['warn'], lw=2, markersize=3, label='現状維持')
ax2.plot(proj_years, tax_pessimistic, 'v--', color=C['bad'], lw=2, markersize=3, label='悲観')
ax2.fill_between(proj_years, tax_pessimistic, tax_optimistic, color='gray', alpha=0.2)

ax2.axvline(x=2025, color='white', ls='--', lw=1.5, alpha=0.7)
ax2.set_xlim(1988, 2062); ax2.set_ylim(30, 190)
ax2.set_ylabel('兆円', color='white', fontsize=12)
ax2.tick_params(colors='white', labelsize=11); ax2.grid(alpha=0.2)
ax2.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=10)

ax2.text(2058, tax_optimistic[-1]+8, f'{tax_optimistic[-1]}兆', color=C['good'], fontsize=11)
ax2.text(2058, tax_pessimistic[-1]-12, f'{tax_pessimistic[-1]}兆', color=C['bad'], fontsize=11)

# =============================================================================
# Panel 3: USD/JPY 為替
# =============================================================================
ax3 = fig.add_axes(panels[2], facecolor=C['panel'])
ax3.set_title('③ USD/JPY 為替予測', color='white', fontsize=14, fontweight='bold')

ax3.plot(hist_years, usdjpy_hist, 'o-', color='white', lw=2, markersize=4)
ax3.plot(proj_years, usdjpy_base, 's--', color=C['good'], lw=2, markersize=3, label='正常化')
ax3.plot(proj_years, usdjpy_weak, 'v--', color=C['bad'], lw=2, markersize=3, label='円安継続')

ax3.axvline(x=2025, color='white', ls='--', lw=1.5, alpha=0.7)
ax3.axhline(y=150, color='gray', ls=':', alpha=0.5)
ax3.set_xlim(1988, 2062); ax3.set_ylim(70, 220)
ax3.set_ylabel('円/ドル', color='white', fontsize=12)
ax3.tick_params(colors='white', labelsize=11); ax3.grid(alpha=0.2)
ax3.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=10)

ax3.text(2058, usdjpy_base[-1]-10, f'{usdjpy_base[-1]}円', color=C['good'], fontsize=11)
ax3.text(2058, usdjpy_weak[-1]+5, f'{usdjpy_weak[-1]}円', color=C['bad'], fontsize=11)
# 為替根拠の注記
ax3.text(0.02, 0.02, '※金利差縮小・経常黒字で円高\n  財政不安・金利差拡大で円安',
         transform=ax3.transAxes, fontsize=9, color='gray', va='bottom')

# =============================================================================
# Panel 4: 生産年齢人口
# =============================================================================
ax4 = fig.add_axes(panels[3], facecolor=C['panel'])
ax4.set_title('④ 生産年齢人口比率', color='white', fontsize=14, fontweight='bold')

ax4.fill_between(hist_years, 45, working_age_hist, color=C['bad'], alpha=0.3)
ax4.plot(hist_years, working_age_hist, 'o-', color=C['bad'], lw=2, markersize=4)
ax4.fill_between(proj_years, 45, working_age_proj, color=C['bad'], alpha=0.15)
ax4.plot(proj_years, working_age_proj, 's--', color=C['bad'], lw=2, markersize=3, alpha=0.7)

ax4.axvline(x=2025, color='white', ls='--', lw=1.5, alpha=0.7)
ax4.axhline(y=50, color=C['warn'], ls=':', lw=1.5, alpha=0.7)
ax4.set_xlim(1988, 2062); ax4.set_ylim(45, 72)
ax4.set_ylabel('%', color='white', fontsize=12)
ax4.tick_params(colors='white', labelsize=11); ax4.grid(alpha=0.2)

ax4.text(1995, 71, '69.5%', color='white', fontsize=11)
ax4.text(2058, working_age_proj[-1]+2, f'{working_age_proj[-1]}%', color=C['bad'], fontsize=11)

# =============================================================================
# Panel 5: 税収 vs 歳出（利払い除き＝PBベース）
# =============================================================================
ax5 = fig.add_axes(panels[4], facecolor=C['panel'])
ax5.set_title('⑤ 税収 vs PB対象歳出（利払い除き）', color='white', fontsize=14, fontweight='bold')

# Historical comparison with expenditure data (利払い除き・PB対象)
expenditure_hist = np.array([69.3, 75.9, 89.3, 82.2, 92.3, 96.3, 147.6, 115.0])  # 2025: 決算ベース

ax5.fill_between(hist_years, 0, tax_hist, color=C['good'], alpha=0.4, label='税収')
ax5.fill_between(hist_years, 0, expenditure_hist, color=C['bad'], alpha=0.2, label='歳出')
ax5.plot(hist_years, tax_hist, 'o-', color=C['good'], lw=2, markersize=4)
ax5.plot(hist_years, expenditure_hist, 's-', color=C['bad'], lw=2, markersize=4)

# Projections
ax5.plot(proj_years, tax_optimistic, '^--', color=C['good'], lw=2, markersize=3, alpha=0.7)
ax5.plot(proj_years, expenditure_proj, 'v--', color=C['bad'], lw=2, markersize=3, alpha=0.7)

ax5.axvline(x=2025, color='white', ls='--', lw=1.5, alpha=0.7)
ax5.set_xlim(1988, 2062); ax5.set_ylim(0, 180)
ax5.set_xlabel('年', color='white', fontsize=12)
ax5.set_ylabel('兆円', color='white', fontsize=12)
ax5.tick_params(colors='white', labelsize=11); ax5.grid(alpha=0.2)
ax5.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=10)

# Gap annotation
ax5.annotate('', xy=(2060, tax_optimistic[-1]), xytext=(2060, expenditure_proj[-1]),
             arrowprops=dict(arrowstyle='<->', color=C['good'], lw=1.5))
gap = tax_optimistic[-1] - expenditure_proj[-1]
ax5.text(2055, (tax_optimistic[-1]+expenditure_proj[-1])/2, f'+{gap:.0f}兆\n黒字',
         fontsize=11, color=C['good'], ha='right')

# =============================================================================
# Panel 6: 利払い費と税収比率
# =============================================================================
ax6 = fig.add_axes(panels[5], facecolor=C['panel'])
ax6.set_title('⑥ 利払い費 / 税収 比率', color='white', fontsize=14, fontweight='bold')

int_tax_hist = interest_hist / tax_hist * 100
int_tax_opt = interest_proj / tax_optimistic * 100
int_tax_base = interest_proj / tax_baseline * 100
int_tax_pess = interest_proj / tax_pessimistic * 100

ax6.plot(hist_years, int_tax_hist, 'o-', color='white', lw=2, markersize=4, label='実績')
ax6.plot(proj_years, int_tax_opt, 's--', color=C['good'], lw=2, markersize=3, label='楽観')
ax6.plot(proj_years, int_tax_base, '^--', color=C['warn'], lw=2, markersize=3, label='現状維持')
ax6.plot(proj_years, int_tax_pess, 'v--', color=C['bad'], lw=2, markersize=3, label='悲観')

ax6.axvline(x=2025, color='white', ls='--', lw=1.5, alpha=0.7)
ax6.axhline(y=20, color=C['warn'], ls=':', lw=1.5, alpha=0.7)
ax6.axhline(y=30, color=C['bad'], ls=':', lw=1.5, alpha=0.7)
ax6.fill_between([2025, 2060], 30, 80, color=C['bad'], alpha=0.1)

ax6.set_xlim(1988, 2062); ax6.set_ylim(0, 80)
ax6.set_xlabel('年', color='white', fontsize=12)
ax6.set_ylabel('%', color='white', fontsize=12)
ax6.tick_params(colors='white', labelsize=11); ax6.grid(alpha=0.2)
ax6.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=10)

ax6.text(2045, 22, '警戒20%', color=C['warn'], fontsize=10)
ax6.text(2045, 32, '危機30%', color=C['bad'], fontsize=10)
ax6.text(2058, int_tax_pess[-1]+3, f'{int_tax_pess[-1]:.0f}%', color=C['bad'], fontsize=11)

# =============================================================================
# Panel 7: 基礎的財政収支（PB）予測
# =============================================================================
ax7 = fig.add_axes(panels[6], facecolor=C['panel'])
ax7.set_title('⑦ 基礎的財政収支（PB）', color='white', fontsize=14, fontweight='bold')

fb_opt = tax_optimistic - expenditure_proj
fb_base = tax_baseline - expenditure_proj
fb_pess = tax_pessimistic - expenditure_proj

ax7.axhline(0, color='white', ls='-', lw=1, alpha=0.5)
ax7.fill_between(proj_years, 0, fb_opt, where=fb_opt>0, color=C['good'], alpha=0.3)
ax7.fill_between(proj_years, fb_pess, 0, color=C['bad'], alpha=0.3)

ax7.plot(proj_years, fb_opt, 's-', color=C['good'], lw=2.5, markersize=4, label='楽観')
ax7.plot(proj_years, fb_base, '^-', color=C['warn'], lw=2.5, markersize=4, label='現状維持')
ax7.plot(proj_years, fb_pess, 'v-', color=C['bad'], lw=2.5, markersize=4, label='悲観')

ax7.set_xlim(2023, 2062); ax7.set_ylim(-80, 70)
ax7.set_xlabel('年', color='white', fontsize=12)
ax7.set_ylabel('兆円', color='white', fontsize=12)
ax7.tick_params(colors='white', labelsize=11); ax7.grid(alpha=0.2)
ax7.legend(loc='lower left', facecolor=C['panel'], labelcolor='white', fontsize=10)

ax7.text(0.95, 0.95, '黒字', transform=ax7.transAxes, fontsize=12, color=C['good'], ha='right')
ax7.text(0.95, 0.05, '赤字', transform=ax7.transAxes, fontsize=12, color=C['bad'], ha='right')
ax7.text(2058, fb_opt[-1]+5, f'+{fb_opt[-1]:.0f}兆', color=C['good'], fontsize=11)
ax7.text(2058, fb_pess[-1]-8, f'{fb_pess[-1]:.0f}兆', color=C['bad'], fontsize=11)

# =============================================================================
# Panel 8: Summary with Debt/GDP
# =============================================================================
ax8 = fig.add_axes(panels[7], facecolor=C['panel'])
ax8.set_title('⑧ 2060年シナリオまとめ', color='white', fontsize=14, fontweight='bold')
ax8.axis('off')
ax8.set_xlim(0, 10); ax8.set_ylim(0, 10)

summary = [
    ('【楽観】名目成長3%', C['good'], [
        f'税収175兆、PB黒字+51兆',
        f'利払い/税収20%、円高130円',
    ]),
    ('【中央】現状維持1%', C['warn'], [
        '税収92兆、PB赤字-32兆',
        '利払い/税収39%、円安継続',
    ]),
    ('【悲観】デフレ回帰', C['bad'], [
        '税収50兆、PB赤字-74兆',
        '利払い/税収71%、円安200円',
    ]),
]

y = 9.5
for title, color, items in summary:
    ax8.text(0.3, y, title, fontsize=11, color=color, fontweight='bold')
    y -= 0.5
    for item in items:
        ax8.text(0.5, y, item, fontsize=9, color='white')
        y -= 0.4
    y -= 0.2

ax8.text(5, 0.8, '鍵: 名目成長(賃金追随込み)\n→ 税収増 → PB黒字化', ha='center', fontsize=11,
         color='white', bbox=dict(facecolor=C['blue'], alpha=0.5, boxstyle='round'))

# =============================================================================
# Bottom Summary Box
# =============================================================================
summary_box = fig.add_axes([0.05, 0.05, 0.90, 0.28], facecolor='#1a1a2e')
summary_box.axis('off')
summary_box.set_xlim(0, 100); summary_box.set_ylim(0, 10)

# Title
summary_box.text(50, 9.2, '【因果関係の全体像】名目成長（賃金追随込み） → 税収増 → PB黒字化',
                 ha='center', fontsize=16, fontweight='bold', color='white')

# Flow diagram
flow_items = [
    (8, 6.5, '名目成長3%\n(賃金追随込み)', C['blue']),
    (25, 6.5, '税収増加\n175兆円', C['good']),
    (42, 6.5, 'PB黒字化\n+51兆円', C['good']),
    (59, 6.5, '日銀出口\n正常化', C['good']),
    (76, 6.5, '金利正常化\n円高130円', C['good']),
    (92, 6.5, '財政持続\n可能に', C['good']),
]

for x, y, text, color in flow_items:
    summary_box.text(x, y, text, ha='center', va='center', fontsize=11, color='white',
                     bbox=dict(facecolor=color, alpha=0.6, boxstyle='round,pad=0.4'))

# Arrows
for i in range(len(flow_items)-1):
    x1 = flow_items[i][0] + 6
    x2 = flow_items[i+1][0] - 6
    summary_box.annotate('', xy=(x2, 6.5), xytext=(x1, 6.5),
                         arrowprops=dict(arrowstyle='->', color='white', lw=2))

# Counter scenario
summary_box.text(50, 3.5, '【逆シナリオ】名目成長なし → 税収停滞 → PB赤字74兆 → 日銀依存継続 → 円安200円',
                 ha='center', fontsize=12, color=C['bad'],
                 bbox=dict(facecolor='#2a1a1e', alpha=0.8, boxstyle='round'))

# Key numbers
numbers = [
    ('税収予測', '50〜175兆円', '（3.5倍の差）'),
    ('PB収支', '-74〜+51兆円', '（125兆円の差）'),
    ('利払い/税収', '20〜71%', '（3.5倍の差）'),
    ('USD/JPY', '130〜200円', '（70円の差）'),
]

summary_box.text(12, 1.5, '【2060年 楽観vs悲観の差】', fontsize=12, fontweight='bold', color='white')
for i, (label, value, note) in enumerate(numbers):
    x = 35 + i * 18
    summary_box.text(x, 1.5, f'{label}: {value}', ha='center', fontsize=11, color='white')
    summary_box.text(x, 0.7, note, ha='center', fontsize=10, color='gray')

plt.savefig('japan_integrated_dashboard_2060_v2.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Created japan_integrated_dashboard_2060_v2.png")
