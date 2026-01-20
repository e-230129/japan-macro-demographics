#!/usr/bin/env python3
"""
日本財政・インフレ・為替の長期予測（〜2060年）
Comprehensive Japan Fiscal/Inflation/FX Projections to 2060
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
# Historical Data + Projections to 2060
# =============================================================================

# Historical years
hist_years = np.array([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])

# JGB/Fiscal historical data
jgb_outstanding_hist = np.array([166, 225, 368, 527, 637, 807, 945, 1080])  # 兆円
boj_holdings_hist = np.array([25, 38, 55, 90, 75, 282, 500, 576])  # 兆円
boj_share_hist = np.array([15.1, 16.9, 14.9, 17.1, 11.8, 34.9, 52.9, 53.3])  # %
avg_interest_rate_hist = np.array([6.9, 4.8, 2.9, 1.6, 1.3, 1.0, 0.8, 0.9])  # %
tax_revenue_hist = np.array([60.1, 52.1, 50.7, 49.1, 41.5, 56.3, 60.8, 75.2])  # 兆円

# USD/JPY historical (annual average)
usdjpy_hist = np.array([145, 94, 108, 110, 88, 121, 107, 157])  # 円/ドル

# Working-age population ratio (15-64歳比率) - IPSS 2023年推計に基づく
working_age_hist = np.array([69.5, 69.4, 67.9, 65.8, 63.7, 60.6, 59.2, 59.3])  # %

# =============================================================================
# Projection Years (2025-2060)
# =============================================================================
proj_years = np.arange(2025, 2061, 5)  # 5年刻み

# Scenario assumptions for projections:
# - 2% inflation target achieved
# - BOJ gradual normalization
# - Demographic decline continues per IPSS projections

# GDP projection (nominal, assuming 2% inflation + 1% real growth = 3% nominal)
gdp_2025 = 600  # 兆円
gdp_growth_rate = 0.03  # 3% nominal（統合ダッシュボードと統一）
gdp_proj = gdp_2025 * (1 + gdp_growth_rate) ** (proj_years - 2025)

# JGB Outstanding projection (assuming primary deficit continues, slower growth)
jgb_proj = np.array([1080, 1150, 1220, 1280, 1330, 1370, 1400, 1420])  # 兆円

# BOJ Holdings projection (gradual reduction scenario - exit success)
boj_holdings_proj = np.array([576, 500, 400, 320, 260, 220, 200, 180])  # 兆円（他図と統一）
boj_share_proj = boj_holdings_proj / jgb_proj * 100

# Interest rate projection (gradual normalization)
interest_rate_proj = np.array([0.9, 1.5, 2.0, 2.3, 2.5, 2.5, 2.5, 2.5])  # %

# Tax revenue projection (with inflation)
tax_proj = np.array([75.2, 82, 90, 98, 105, 112, 118, 124])  # 兆円

# Working-age population projection (15-64歳比率) - IPSS 2023年推計(出生中位×死亡中位)
working_age_proj = np.array([59.3, 58.5, 56.9, 55.4, 54.1, 53.5, 53.1, 52.8])  # %

# USD/JPY Projection Scenarios
# Base case: gradual weakening due to interest rate differential narrowing
# Scenario A: Inflation success - JPY stabilizes around 130-140
# Scenario B: Stagflation - JPY continues weakening to 180-200
# Scenario C: Crisis - JPY collapse to 200+

usdjpy_base = np.array([157, 150, 145, 140, 138, 135, 133, 130])  # Base (normalization)
usdjpy_weak = np.array([157, 165, 175, 185, 190, 195, 200, 200])  # Weak JPY (stagflation)
usdjpy_crisis = np.array([157, 180, 200, 220, 230, 240, 250, 250])  # Crisis scenario

# =============================================================================
# Combined arrays for plotting
# =============================================================================
all_years = np.concatenate([hist_years[:-1], proj_years])  # Avoid duplicate 2025

# Colors
C = {
    'good': '#27ae60',
    'bad': '#e74c3c',
    'warn': '#f39c12',
    'blue': '#3498db',
    'purple': '#9b59b6',
    'panel': '#16213e',
    'text': 'white',
    'grid': '#333355'
}

# =============================================================================
# GDP projection for Debt/GDP ratio
# =============================================================================
gdp_2025 = 600  # 兆円
gdp_proj_for_debt = gdp_2025 * (1.03) ** (np.arange(8) * 5)  # 名目3%成長（統合ダッシュボードと統一）
debt_gdp = jgb_proj / gdp_proj_for_debt * 100

# =============================================================================
# Figure 1: Comprehensive Dashboard to 2060
# =============================================================================
fig1 = plt.figure(figsize=(22, 20), facecolor='#0f0f23')
fig1.suptitle('日本財政・インフレ・為替の長期予測（〜2060年）\n'
              'Japan Fiscal, Inflation & FX Long-term Projections',
              fontsize=26, fontweight='bold', color='white', y=0.98)

# =============================================================================
# Key Conclusions Box (Top Left) - 結論3行
# =============================================================================
conclusions = """【結論】必要条件は「持続的な名目成長」（賃金追随が前提）
1. 名目成長3%達成なら日銀保有13%へ正常化、利払い35兆円で財政維持可能
2. 為替は正常化で130円、名目成長なしなら250円超と大きく分岐
3. 生産年齢人口(15-64歳)52.8%で高齢化社会へ"""
fig1.text(0.02, 0.93, conclusions, fontsize=13, color='white', va='top',
          bbox=dict(facecolor='#1a3a5c', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#3498db'))

# =============================================================================
# Assumptions & Definitions Box (Top Right) - 前提まとめ
# =============================================================================
assumptions = """【前提・定義】
• 基準年: FY2024決算ベース
• 国債: 普通国債残高（T-Bill除く）
• 人口: 生産年齢15-64歳比率(IPSS 2023推計)
• 利払い: ストレス試算(全残高×同一金利)
• 為替: 金利差・経常収支・財政信認で変動
• 「財政危機」＝利払い/税収30%超"""
fig1.text(0.70, 0.93, assumptions, fontsize=12, color='white', va='top',
          bbox=dict(facecolor='#2d1f3d', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#9b59b6'))

# Panel 1: JGB Outstanding & BOJ Holdings
ax1 = fig1.add_axes([0.05, 0.48, 0.42, 0.32], facecolor=C['panel'])
ax1.set_title('① 国債残高と日銀保有の長期推移', fontsize=17, fontweight='bold', color='white')

# Historical
market_hist = jgb_outstanding_hist - boj_holdings_hist
ax1.bar(hist_years, market_hist, width=4, color=C['blue'], alpha=0.7, label='市場保有')
ax1.bar(hist_years, boj_holdings_hist, width=4, bottom=market_hist, color=C['bad'], alpha=0.7, label='日銀保有')

# Projection
market_proj = jgb_proj - boj_holdings_proj
ax1.bar(proj_years[1:], market_proj[1:], width=4, color=C['blue'], alpha=0.4, hatch='//')
ax1.bar(proj_years[1:], boj_holdings_proj[1:], width=4, bottom=market_proj[1:], color=C['bad'], alpha=0.4, hatch='//')

# Divider line
ax1.axvline(x=2025, color='white', linestyle='--', linewidth=2, alpha=0.7)
ax1.text(2025, 1450, '←実績 | 予測→', ha='center', fontsize=13, color='white')

ax1.set_xlim(1988, 2062)
ax1.set_ylim(0, 1500)
ax1.set_xlabel('年', color='white', fontsize=13)
ax1.set_ylabel('兆円', color='white', fontsize=13)
ax1.tick_params(colors='white', labelsize=12)
ax1.grid(alpha=0.2)
ax1.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=12)

# Add BOJ share labels
for y, total, share in zip([2025, 2040, 2060], [jgb_proj[0], jgb_proj[3], jgb_proj[-1]],
                            [boj_share_proj[0], boj_share_proj[3], boj_share_proj[-1]]):
    ax1.text(y, total + 30, f'日銀{share:.0f}%', ha='center', fontsize=12, color=C['bad'])

# Panel 2: USD/JPY Scenarios
ax2 = fig1.add_axes([0.53, 0.48, 0.42, 0.32], facecolor=C['panel'])
ax2.set_title('② USD/JPY 為替レート予測シナリオ', fontsize=17, fontweight='bold', color='white')

# Historical
ax2.plot(hist_years, usdjpy_hist, 'o-', color='white', linewidth=3, markersize=8, label='実績')

# Projections
ax2.plot(proj_years, usdjpy_base, 's--', color=C['good'], linewidth=2.5, markersize=6,
         label='楽観シナリオ (130円)')
ax2.plot(proj_years, usdjpy_weak, '^--', color=C['warn'], linewidth=2.5, markersize=6,
         label='現状維持シナリオ (200円)')
ax2.plot(proj_years, usdjpy_crisis, 'v--', color=C['bad'], linewidth=2.5, markersize=6,
         label='危機シナリオ (250円)')

ax2.axvline(x=2025, color='white', linestyle='--', linewidth=2, alpha=0.7)
ax2.axhline(y=150, color='gray', linestyle=':', alpha=0.5)
ax2.text(2000, 153, '150円ライン', fontsize=12, color='gray')

ax2.set_xlim(1988, 2062)
ax2.set_ylim(70, 270)
ax2.set_xlabel('年', color='white', fontsize=13)
ax2.set_ylabel('円/ドル', color='white', fontsize=13)
ax2.tick_params(colors='white', labelsize=12)
ax2.grid(alpha=0.2)
ax2.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=12)

# Annotations
ax2.annotate('プラザ合意\n(1985)', xy=(1990, 145), xytext=(1992, 100),
             fontsize=11, color='white', arrowprops=dict(arrowstyle='->', color='white'))
ax2.annotate('異次元緩和\n(2013)', xy=(2015, 121), xytext=(2008, 80),
             fontsize=11, color='white', arrowprops=dict(arrowstyle='->', color='white'))
ax2.annotate('円安加速\n(2022-)', xy=(2025, 157), xytext=(2018, 180),
             fontsize=11, color=C['warn'], arrowprops=dict(arrowstyle='->', color=C['warn']))
# 為替根拠の注記
ax2.text(0.02, 0.02, '※金利差縮小・経常黒字で円高、財政不安・緩和継続で円安',
         transform=ax2.transAxes, fontsize=10, color='gray', va='bottom')

# Panel 3: Interest Rate & Debt Service
ax3 = fig1.add_axes([0.05, 0.08, 0.42, 0.32], facecolor=C['panel'])
ax3.set_title('③ 金利と利払い費の長期予測', fontsize=17, fontweight='bold', color='white')

# Calculate interest payments
interest_payment_hist = jgb_outstanding_hist * avg_interest_rate_hist / 100
interest_payment_proj = jgb_proj * interest_rate_proj / 100

ax3b = ax3.twinx()

# Historical
ax3.bar(hist_years, interest_payment_hist, width=4, color=C['warn'], alpha=0.7, label='利払い費')
ax3b.plot(hist_years, avg_interest_rate_hist, 'o-', color=C['blue'], linewidth=3, markersize=8, label='平均金利')

# Projection
ax3.bar(proj_years[1:], interest_payment_proj[1:], width=4, color=C['warn'], alpha=0.4, hatch='//')
ax3b.plot(proj_years, interest_rate_proj, 's--', color=C['blue'], linewidth=2, markersize=6, alpha=0.7)

ax3.axvline(x=2025, color='white', linestyle='--', linewidth=2, alpha=0.7)

# Danger zone
ax3.axhspan(30, 50, color=C['bad'], alpha=0.1)
ax3.text(2050, 40, '危険ゾーン\n(税収の30%超)', fontsize=12, color=C['bad'], ha='center')

ax3.set_xlim(1988, 2062)
ax3.set_ylim(0, 50)
ax3b.set_ylim(0, 8)
ax3.set_xlabel('年', color='white', fontsize=13)
ax3.set_ylabel('利払い費 (兆円)', color=C['warn'], fontsize=13)
ax3b.set_ylabel('平均金利 (%)', color=C['blue'], fontsize=13)
ax3.tick_params(colors='white', labelsize=12)
ax3b.tick_params(colors='white', labelsize=12)
ax3.grid(alpha=0.2)

lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3b.get_legend_handles_labels()
ax3.legend(lines1+lines2, labels1+labels2, loc='upper right', facecolor=C['panel'], labelcolor='white', fontsize=12)

# Add values
for y, val in [(2040, interest_payment_proj[3]), (2060, interest_payment_proj[-1])]:
    ax3.text(y, val+2, f'{val:.0f}兆円', ha='center', fontsize=12, color=C['warn'])

# Panel 4: Working-age Population & Fiscal Sustainability
ax4 = fig1.add_axes([0.53, 0.08, 0.42, 0.32], facecolor=C['panel'])
ax4.set_title('④ 生産年齢人口比率と財政持続可能性', fontsize=17, fontweight='bold', color='white')

# Working-age population
ax4.fill_between(hist_years, 45, working_age_hist, color=C['bad'], alpha=0.3)
ax4.plot(hist_years, working_age_hist, 'o-', color=C['bad'], linewidth=3, markersize=8, label='生産年齢人口比率')
ax4.fill_between(proj_years, 45, working_age_proj, color=C['bad'], alpha=0.15)
ax4.plot(proj_years, working_age_proj, 's--', color=C['bad'], linewidth=2, markersize=6, alpha=0.7)

ax4.axvline(x=2025, color='white', linestyle='--', linewidth=2, alpha=0.7)
ax4.axhline(y=50, color=C['warn'], linestyle=':', linewidth=2, alpha=0.7)
ax4.text(2000, 51, '50%ライン（2人で1人を支える）', fontsize=12, color=C['warn'])

ax4.set_xlim(1988, 2062)
ax4.set_ylim(45, 72)
ax4.set_xlabel('年', color='white', fontsize=13)
ax4.set_ylabel('生産年齢人口比率 (%)', color='white', fontsize=13)
ax4.tick_params(colors='white', labelsize=12)
ax4.grid(alpha=0.2)
ax4.legend(loc='upper right', facecolor=C['panel'], labelcolor='white', fontsize=12)

# Key annotations
ax4.annotate('1995年\nピーク69.5%', xy=(1995, 69.4), xytext=(2005, 71),
             fontsize=12, color='white', arrowprops=dict(arrowstyle='->', color='white'))
ax4.annotate('2060年\n予測52.8%', xy=(2060, 52.8), xytext=(2050, 57),
             fontsize=12, color=C['bad'], arrowprops=dict(arrowstyle='->', color=C['bad']))

# Summary box
summary = ("【2060年予測】国債残高1,420兆円（普通国債）、日銀保有13%（180兆円）、金利2.5%、利払い35兆円※\n"
           "USD/JPY: 正常化なら130円、停滞なら200円、危機なら250円\n"
           "生産年齢人口(15-64歳)52.8%  ※利払いは全残高に同一金利が乗る仮定（ストレステスト）")
fig1.text(0.5, 0.01, summary, ha='center', fontsize=12, color='#cccccc',
          bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.9))

plt.savefig('japan_2060_comprehensive_v2.png',
            dpi=150, bbox_inches='tight', facecolor=fig1.get_facecolor())
plt.close()

print("Created japan_2060_comprehensive_v2.png")