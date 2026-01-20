#!/usr/bin/env python3
"""
日本の税収予測と財政バランス（〜2060年）
Japan Tax Revenue Projections & Fiscal Balance to 2060
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

# Tax Revenue (一般会計税収) - 兆円
# 2025(FY2024)は令和6年度決算概要に基づく
tax_hist = np.array([60.1, 52.1, 50.7, 49.1, 41.5, 56.3, 60.8, 75.2])

# Tax breakdown - 2025(FY2024)は令和6年度決算の公式値
# 消費税25.0/所得税21.2/法人税17.9/その他11.0(兆円)
income_tax_hist = np.array([26.0, 19.5, 18.8, 15.6, 12.8, 16.4, 19.2, 21.2])  # 所得税
corp_tax_hist = np.array([18.4, 13.7, 11.7, 13.3, 9.0, 11.0, 11.2, 17.9])    # 法人税
consumption_tax_hist = np.array([4.6, 5.8, 9.8, 10.6, 10.0, 17.4, 21.0, 25.0])  # 消費税
other_tax_hist = tax_hist - income_tax_hist - corp_tax_hist - consumption_tax_hist  # その他

# Expenditure (一般会計歳出) - 兆円
# 2025(FY2024)は令和6年度決算の支出済歳出額123.0兆円
expenditure_hist = np.array([69.3, 75.9, 89.3, 82.2, 92.3, 96.3, 147.6, 123.0])

# Social Security (社会保障関係費) - 兆円
social_security_hist = np.array([11.6, 14.5, 16.8, 20.4, 27.3, 31.5, 35.9, 38.0])

# JGB data
jgb_hist = np.array([166, 225, 368, 527, 637, 807, 945, 1080])  # 兆円
interest_rate_hist = np.array([6.9, 4.8, 2.9, 1.6, 1.3, 1.0, 0.8, 0.9])  # %
interest_payment_hist = jgb_hist * interest_rate_hist / 100

# =============================================================================
# Projections (2025-2060) - 3 Scenarios
# =============================================================================
proj_years = np.arange(2025, 2065, 5)

# Working-age population ratio (affects tax base)
working_age_proj = np.array([58.5, 57.0, 55.2, 53.5, 52.0, 50.8, 49.8, 49.0])  # %
working_age_decline = working_age_proj / working_age_proj[0]  # Relative to 2025

# Scenario 1: Optimistic (インフレ達成 + 成長)
# - 2% inflation + 1% real growth = 3% nominal growth
# - Tax revenue grows with nominal GDP
tax_optimistic = np.array([75.2, 87, 100, 115, 130, 145, 160, 175])
consumption_tax_opt = np.array([23.5, 28, 33, 38, 43, 48, 53, 58])  # 消費税増収
income_tax_opt = np.array([22.5, 26, 30, 35, 40, 45, 50, 55])
corp_tax_opt = np.array([15.0, 17, 19, 21, 23, 25, 27, 29])
other_tax_opt = tax_optimistic - consumption_tax_opt - income_tax_opt - corp_tax_opt

# Scenario 2: Baseline (現状継続)
# - 1% nominal growth (low inflation)
# - Demographic headwind
tax_baseline = np.array([75.2, 80, 85, 88, 90, 91, 92, 92])
consumption_tax_base = np.array([23.5, 26, 28, 30, 31, 32, 32, 32])
income_tax_base = np.array([22.5, 23, 24, 24, 24, 24, 24, 24])
corp_tax_base = np.array([15.0, 15, 15, 15, 15, 15, 15, 15])
other_tax_base = tax_baseline - consumption_tax_base - income_tax_base - corp_tax_base

# Scenario 3: Pessimistic (デフレ回帰 + 人口減加速)
# - 0% nominal growth
# - Tax base shrinks with working-age population
tax_pessimistic = np.array([75.2, 73, 70, 66, 62, 58, 54, 50])

# Expenditure projections
social_security_proj = np.array([38.0, 42, 47, 52, 56, 59, 61, 62])  # 高齢化で増加
other_expenditure = np.array([74.0, 72, 70, 68, 66, 64, 62, 60])  # その他は抑制
expenditure_proj = social_security_proj + other_expenditure

# Interest rate scenarios
rate_normal = np.array([0.9, 1.5, 2.0, 2.3, 2.5, 2.5, 2.5, 2.5])
rate_low = np.array([0.9, 1.0, 1.2, 1.3, 1.5, 1.5, 1.5, 1.5])

# JGB projection
jgb_proj = np.array([1080, 1150, 1220, 1280, 1330, 1370, 1400, 1420])

# Interest payments
interest_normal = jgb_proj * rate_normal / 100
interest_low = jgb_proj * rate_low / 100

# Primary balance (税収 - 歳出 + 利払い)
pb_optimistic = tax_optimistic - (expenditure_proj - interest_normal)
pb_baseline = tax_baseline - (expenditure_proj - interest_normal)
pb_pessimistic = tax_pessimistic - (expenditure_proj - interest_normal)

# Fiscal balance (税収 - 歳出)
fb_optimistic = tax_optimistic - expenditure_proj
fb_baseline = tax_baseline - expenditure_proj
fb_pessimistic = tax_pessimistic - expenditure_proj

C = {'good': '#27ae60', 'bad': '#e74c3c', 'warn': '#f39c12', 'blue': '#3498db', 
     'purple': '#9b59b6', 'panel': '#16213e', 'income': '#3498db', 
     'corp': '#9b59b6', 'consumption': '#e74c3c', 'other': '#95a5a6'}

# =============================================================================
# Figure 1: Tax Revenue Dashboard (6 panels)
# =============================================================================
fig = plt.figure(figsize=(20, 18), facecolor='#0f0f23')
fig.suptitle('日本の税収予測と財政バランス（〜2060年）\n'
             'Japan Tax Revenue & Fiscal Balance Projections',
             fontsize=22, fontweight='bold', color='white', y=0.98)

# =============================================================================
# Key Conclusions Box (Top Left) - 結論3行
# =============================================================================
conclusions = """【結論】必要条件は「持続的な名目成長」（賃金追随が前提）
1. 名目成長3%で税収175兆円、PB黒字化+53兆円
2. 名目成長なしならPB均衡に30〜72兆円の増税or歳出削減が必要
3. 「財政危機」＝利払い/税収30%超（悲観シナリオで71%到達）"""
fig.text(0.02, 0.93, conclusions, fontsize=11, color='white', va='top',
         bbox=dict(facecolor='#1a3a5c', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#3498db'))

# =============================================================================
# Assumptions & Definitions Box (Top Right) - 前提まとめ
# =============================================================================
assumptions = """【前提・定義】
• 基準年: FY2024決算(税収75.2兆/歳出123.0兆)
• 税目内訳: 令和6年度決算の公式値
• 楽観: 名目3%成長/現状維持: 1%/悲観: 0%
• 歳出: 利払い除きのPBベース
• 利払い: ストレス試算(全残高×同一金利)"""
fig.text(0.72, 0.93, assumptions, fontsize=10, color='white', va='top',
         bbox=dict(facecolor='#2d1f3d', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#9b59b6'))

# =============================================================================
# Panel 1: Historical Tax Revenue Breakdown
# =============================================================================
ax1 = fig.add_axes([0.05, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax1.set_title('① 税収の内訳推移（実績）', color='white', fontsize=13, fontweight='bold')

ax1.bar(hist_years, income_tax_hist, width=4, color=C['income'], alpha=0.8, label='所得税')
ax1.bar(hist_years, corp_tax_hist, width=4, bottom=income_tax_hist, color=C['corp'], alpha=0.8, label='法人税')
ax1.bar(hist_years, consumption_tax_hist, width=4, bottom=income_tax_hist+corp_tax_hist, 
        color=C['consumption'], alpha=0.8, label='消費税')
ax1.bar(hist_years, other_tax_hist, width=4, bottom=income_tax_hist+corp_tax_hist+consumption_tax_hist,
        color=C['other'], alpha=0.8, label='その他')

ax1.plot(hist_years, tax_hist, 'o-', color='white', lw=2, markersize=6, label='合計')

# Add labels
for y, total in zip([1990, 2010, 2025], [tax_hist[0], tax_hist[4], tax_hist[-1]]):
    idx = list(hist_years).index(y)
    ax1.text(y, total + 3, f'{total:.1f}兆', ha='center', fontsize=9, color='white')

ax1.set_xlim(1988, 2027); ax1.set_ylim(0, 85)
ax1.set_xlabel('年度', color='white'); ax1.set_ylabel('税収 (兆円)', color='white')
ax1.tick_params(colors='white'); ax1.grid(alpha=0.2)
ax1.legend(loc='upper right', facecolor=C['panel'], labelcolor='white', fontsize=8, ncol=2)

# Annotation
ax1.annotate('バブル崩壊', xy=(1995, 52), xytext=(1998, 65),
             fontsize=8, color=C['warn'], arrowprops=dict(arrowstyle='->', color=C['warn']))
ax1.annotate('リーマン\nショック', xy=(2010, 41.5), xytext=(2003, 35),
             fontsize=8, color=C['bad'], arrowprops=dict(arrowstyle='->', color=C['bad']))

# =============================================================================
# Panel 2: Tax Revenue Scenarios to 2060
# =============================================================================
ax2 = fig.add_axes([0.37, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax2.set_title('② 税収予測シナリオ（〜2060年）', color='white', fontsize=13, fontweight='bold')

ax2.plot(hist_years, tax_hist, 'o-', color='white', lw=3, markersize=6, label='実績')
ax2.plot(proj_years, tax_optimistic, 's--', color=C['good'], lw=2.5, markersize=5, 
         label='楽観 (インフレ2%+成長)')
ax2.plot(proj_years, tax_baseline, '^--', color=C['warn'], lw=2.5, markersize=5, 
         label='現状維持')
ax2.plot(proj_years, tax_pessimistic, 'v--', color=C['bad'], lw=2.5, markersize=5, 
         label='悲観 (デフレ回帰)')

ax2.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)
ax2.fill_between(proj_years, tax_pessimistic, tax_optimistic, color='gray', alpha=0.2)

ax2.set_xlim(1988, 2062); ax2.set_ylim(30, 190)
ax2.set_xlabel('年度', color='white'); ax2.set_ylabel('税収 (兆円)', color='white')
ax2.tick_params(colors='white'); ax2.grid(alpha=0.2)
ax2.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=8)

# End values
ax2.text(2058, tax_optimistic[-1]+5, f'{tax_optimistic[-1]}兆', color=C['good'], fontsize=9, ha='center')
ax2.text(2058, tax_baseline[-1]+5, f'{tax_baseline[-1]}兆', color=C['warn'], fontsize=9, ha='center')
ax2.text(2058, tax_pessimistic[-1]-8, f'{tax_pessimistic[-1]}兆', color=C['bad'], fontsize=9, ha='center')

# =============================================================================
# Panel 3: Tax Revenue vs Expenditure
# =============================================================================
ax3 = fig.add_axes([0.69, 0.48, 0.28, 0.32], facecolor=C['panel'])
ax3.set_title('③ 税収 vs 歳出（財政ギャップ）', color='white', fontsize=13, fontweight='bold')

# Historical
ax3.fill_between(hist_years, 0, tax_hist, color=C['good'], alpha=0.3, label='税収')
ax3.fill_between(hist_years, 0, expenditure_hist, color=C['bad'], alpha=0.3, label='歳出')
ax3.plot(hist_years, tax_hist, 'o-', color=C['good'], lw=2, markersize=5)
ax3.plot(hist_years, expenditure_hist, 's-', color=C['bad'], lw=2, markersize=5)

# Projection (baseline)
ax3.plot(proj_years, tax_baseline, '^--', color=C['good'], lw=2, markersize=4, alpha=0.7)
ax3.plot(proj_years, expenditure_proj, 'v--', color=C['bad'], lw=2, markersize=4, alpha=0.7)

# Gap annotation
ax3.annotate('', xy=(2025, tax_hist[-1]), xytext=(2025, expenditure_hist[-1]),
             arrowprops=dict(arrowstyle='<->', color=C['warn'], lw=2))
gap_2025 = expenditure_hist[-1] - tax_hist[-1]
ax3.text(2027, (tax_hist[-1] + expenditure_hist[-1])/2, f'ギャップ\n{gap_2025:.0f}兆円', 
         fontsize=9, color=C['warn'])

ax3.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)

ax3.set_xlim(1988, 2062); ax3.set_ylim(0, 160)
ax3.set_xlabel('年度', color='white'); ax3.set_ylabel('兆円', color='white')
ax3.tick_params(colors='white'); ax3.grid(alpha=0.2)
ax3.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=9)

# =============================================================================
# Panel 4: Primary Balance & Fiscal Balance
# =============================================================================
ax4 = fig.add_axes([0.05, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax4.set_title('④ 財政収支（税収−歳出）', color='white', fontsize=13, fontweight='bold')

ax4.axhline(0, color='white', ls='-', lw=1, alpha=0.5)

ax4.plot(proj_years, fb_optimistic, 's-', color=C['good'], lw=3, markersize=6, label='楽観シナリオ')
ax4.plot(proj_years, fb_baseline, '^-', color=C['warn'], lw=3, markersize=6, label='現状維持')
ax4.plot(proj_years, fb_pessimistic, 'v-', color=C['bad'], lw=3, markersize=6, label='悲観シナリオ')

ax4.fill_between(proj_years, 0, fb_optimistic, where=fb_optimistic>0, color=C['good'], alpha=0.3)
ax4.fill_between(proj_years, fb_pessimistic, 0, color=C['bad'], alpha=0.3)

ax4.set_xlim(2023, 2062); ax4.set_ylim(-80, 80)
ax4.set_xlabel('年度', color='white'); ax4.set_ylabel('財政収支 (兆円)', color='white')
ax4.tick_params(colors='white'); ax4.grid(alpha=0.2)
ax4.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=9)

# Labels
ax4.text(2058, fb_optimistic[-1]+5, f'{fb_optimistic[-1]:+.0f}兆', color=C['good'], fontsize=9, ha='center')
ax4.text(2058, fb_baseline[-1]-10, f'{fb_baseline[-1]:.0f}兆', color=C['warn'], fontsize=9, ha='center')
ax4.text(2058, fb_pessimistic[-1]-10, f'{fb_pessimistic[-1]:.0f}兆', color=C['bad'], fontsize=9, ha='center')

ax4.text(0.5, 0.95, '黒字', transform=ax4.transAxes, fontsize=10, color=C['good'], ha='center')
ax4.text(0.5, 0.05, '赤字', transform=ax4.transAxes, fontsize=10, color=C['bad'], ha='center')

# =============================================================================
# Panel 5: Tax Revenue vs Interest Payment
# =============================================================================
ax5 = fig.add_axes([0.37, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax5.set_title('⑤ 税収に占める利払い費の割合', color='white', fontsize=13, fontweight='bold')

# Historical
int_tax_hist = interest_payment_hist / tax_hist * 100

# Projections
int_tax_opt_normal = interest_normal / tax_optimistic * 100
int_tax_base_normal = interest_normal / tax_baseline * 100
int_tax_pess_normal = interest_normal / tax_pessimistic * 100

ax5.plot(hist_years, int_tax_hist, 'o-', color='white', lw=3, markersize=6, label='実績')
ax5.plot(proj_years, int_tax_opt_normal, 's--', color=C['good'], lw=2.5, markersize=5, label='楽観+金利正常化')
ax5.plot(proj_years, int_tax_base_normal, '^--', color=C['warn'], lw=2.5, markersize=5, label='現状維持+金利正常化')
ax5.plot(proj_years, int_tax_pess_normal, 'v--', color=C['bad'], lw=2.5, markersize=5, label='悲観+金利正常化')

ax5.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)
ax5.axhline(y=20, color=C['warn'], ls=':', lw=2, alpha=0.7)
ax5.axhline(y=30, color=C['bad'], ls=':', lw=2, alpha=0.7)
ax5.text(1995, 21, '警戒ライン 20%', fontsize=8, color=C['warn'])
ax5.text(1995, 31, '危機ライン 30%', fontsize=8, color=C['bad'])

# Danger zone
ax5.fill_between([2025, 2060], 30, 80, color=C['bad'], alpha=0.1)

ax5.set_xlim(1988, 2062); ax5.set_ylim(0, 80)
ax5.set_xlabel('年度', color='white'); ax5.set_ylabel('利払い費/税収 (%)', color='white')
ax5.tick_params(colors='white'); ax5.grid(alpha=0.2)
ax5.legend(loc='upper left', facecolor=C['panel'], labelcolor='white', fontsize=7)

# End labels
ax5.text(2058, int_tax_opt_normal[-1]+3, f'{int_tax_opt_normal[-1]:.0f}%', color=C['good'], fontsize=9)
ax5.text(2058, int_tax_pess_normal[-1]+3, f'{int_tax_pess_normal[-1]:.0f}%', color=C['bad'], fontsize=9)

# =============================================================================
# Panel 6: Summary Table
# =============================================================================
ax6 = fig.add_axes([0.69, 0.08, 0.28, 0.32], facecolor=C['panel'])
ax6.set_title('⑥ 2060年 財政シナリオまとめ', color='white', fontsize=13, fontweight='bold')
ax6.axis('off')
ax6.set_xlim(0, 10); ax6.set_ylim(0, 10)

scenarios = [
    ('【楽観シナリオ】', C['good'], [
        f'税収: {tax_optimistic[-1]}兆円 (+{tax_optimistic[-1]-tax_hist[-1]:.0f}兆)',
        f'財政収支: {fb_optimistic[-1]:+.0f}兆円 (黒字化)',
        f'利払い/税収: {int_tax_opt_normal[-1]:.0f}%',
    ]),
    ('【現状維持】', C['warn'], [
        f'税収: {tax_baseline[-1]}兆円 (+{tax_baseline[-1]-tax_hist[-1]:.0f}兆)',
        f'財政収支: {fb_baseline[-1]:.0f}兆円 (赤字継続)',
        f'利払い/税収: {int_tax_base_normal[-1]:.0f}%',
    ]),
    ('【危機シナリオ】', C['bad'], [
        f'税収: {tax_pessimistic[-1]}兆円 ({tax_pessimistic[-1]-tax_hist[-1]:.0f}兆)',
        f'財政収支: {fb_pessimistic[-1]:.0f}兆円 (大幅赤字)',
        f'利払い/税収: {int_tax_pess_normal[-1]:.0f}%',
    ]),
]

y = 9.5
for title, color, items in scenarios:
    ax6.text(0.3, y, title, fontsize=10, color=color, fontweight='bold')
    y -= 0.5
    for item in items:
        ax6.text(0.5, y, item, fontsize=8, color='white')
        y -= 0.5
    y -= 0.2

# Key insight
ax6.text(5, 0.5, '鍵: インフレ達成で税収増 → 財政黒字化が可能', ha='center', fontsize=10,
         color='white', bbox=dict(facecolor=C['blue'], alpha=0.5, boxstyle='round'))

# Footer
footer = ("【結論】税収予測は楽観175兆〜悲観50兆円と大きく分岐。インフレ2%達成なら財政黒字化の可能性あり。"
          "デフレ継続なら税収減+利払い増で財政危機リスク上昇。")
fig.text(0.5, 0.01, footer, ha='center', fontsize=10, color='#cccccc', style='italic')

plt.savefig('tax_revenue_2060_v2.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

# =============================================================================
# Figure 2: Tax Revenue Detailed Breakdown (Optimistic Scenario)
# =============================================================================
fig2 = plt.figure(figsize=(16, 10), facecolor='#0f0f23')
fig2.suptitle('楽観シナリオにおける税収内訳予測（〜2060年）', 
              fontsize=16, fontweight='bold', color='white', y=0.97)

# Combined years
all_years = np.concatenate([hist_years, proj_years[1:]])
income_all = np.concatenate([income_tax_hist, income_tax_opt[1:]])
corp_all = np.concatenate([corp_tax_hist, corp_tax_opt[1:]])
consumption_all = np.concatenate([consumption_tax_hist, consumption_tax_opt[1:]])
other_all = np.concatenate([other_tax_hist, other_tax_opt[1:]])
tax_all = np.concatenate([tax_hist, tax_optimistic[1:]])

ax = fig2.add_axes([0.08, 0.12, 0.85, 0.75], facecolor=C['panel'])

# Stacked area
ax.stackplot(all_years, income_all, corp_all, consumption_all, other_all,
             labels=['所得税', '法人税', '消費税', 'その他'],
             colors=[C['income'], C['corp'], C['consumption'], C['other']], alpha=0.8)

ax.plot(all_years, tax_all, 'o-', color='white', lw=2, markersize=5, label='合計')

ax.axvline(x=2025, color='white', ls='--', lw=2, alpha=0.7)
ax.text(2025, 180, '←実績 | 予測→', ha='center', fontsize=11, color='white')

# Labels for breakdown
for y_pos, (label, val, color) in [
    (2060, ('消費税', consumption_tax_opt[-1], C['consumption'])),
    (2060, ('所得税', income_tax_opt[-1], C['income'])),
    (2060, ('法人税', corp_tax_opt[-1], C['corp'])),
]:
    pass  # Skip individual labels, use legend

ax.set_xlim(1988, 2062); ax.set_ylim(0, 190)
ax.set_xlabel('年度', fontsize=12, color='white')
ax.set_ylabel('税収 (兆円)', fontsize=12, color='white')
ax.tick_params(colors='white')
ax.grid(alpha=0.2)
# 凡例を右下に移動（税の変化ボックスと重ならないように）
ax.legend(loc='lower right', facecolor=C['panel'], labelcolor='white', fontsize=10)

# Annotations
ax.annotate(f'2025年: {tax_hist[-1]:.1f}兆円', xy=(2025, tax_hist[-1]), xytext=(2008, 55),
            fontsize=10, color='white', arrowprops=dict(arrowstyle='->', color='white'))
ax.annotate(f'2060年: {tax_optimistic[-1]}兆円 (+{tax_optimistic[-1]-tax_hist[-1]:.0f}兆)',
            xy=(2060, tax_optimistic[-1]), xytext=(2040, 185),
            fontsize=10, color=C['good'], arrowprops=dict(arrowstyle='->', color=C['good']))

# Key changes box - 左上に配置
changes = f"""【2025年→2060年の変化（楽観シナリオ）】
消費税: {consumption_tax_hist[-1]:.1f}兆 → {consumption_tax_opt[-1]}兆 (+{consumption_tax_opt[-1]-consumption_tax_hist[-1]:.1f}兆)
所得税: {income_tax_hist[-1]:.1f}兆 → {income_tax_opt[-1]}兆 (+{income_tax_opt[-1]-income_tax_hist[-1]:.1f}兆)
法人税: {corp_tax_hist[-1]:.1f}兆 → {corp_tax_opt[-1]}兆 (+{corp_tax_opt[-1]-corp_tax_hist[-1]:.1f}兆)
合計:   {tax_hist[-1]:.1f}兆 → {tax_optimistic[-1]}兆 (+{tax_optimistic[-1]-tax_hist[-1]:.1f}兆)"""

ax.text(0.02, 0.98, changes, transform=ax.transAxes, fontsize=9, color='white',
        verticalalignment='top', bbox=dict(facecolor='#1a1a2e', alpha=0.9, boxstyle='round'))

footer2 = "インフレ2%+実質1%成長で名目3%成長を達成すれば、税収は35年で2.3倍（75兆→175兆円）に増加可能"
fig2.text(0.5, 0.02, footer2, ha='center', fontsize=11, color='#cccccc', style='italic')

plt.savefig('tax_revenue_breakdown_2060_v2.png',
            dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()

print("Created tax_revenue_2060_v2.png")
print("Created tax_revenue_breakdown_2060_v2.png")
