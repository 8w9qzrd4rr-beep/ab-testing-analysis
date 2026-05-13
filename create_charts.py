import matplotlib.pyplot as plt
import numpy as np
from run_tests import control_converted, treatment_converted

# Calculate conversion rates
control_rate = sum(control_converted) / len(control_converted) * 100
treatment_rate = sum(treatment_converted) / len(treatment_converted) * 100

# Plot
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(['Control', 'Treatment'], [control_rate, treatment_rate], 
               color=['#4C72B0', '#DD8452'], width=0.5, edgecolor='white')

# Add value labels on bars
for bar, rate in zip(bars, [control_rate, treatment_rate]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold')

ax.set_title('Conversion Rate: Control vs Treatment')
ax.set_ylabel('Conversion Rate (%)')
ax.set_ylim(0, max(control_rate, treatment_rate) * 1.3)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('charts/conversion_rates.png', dpi=150)

# Calculate counts
control_not = control_converted.count(0)
control_yes = control_converted.count(1)
treatment_not = treatment_converted.count(0)
treatment_yes = treatment_converted.count(1)

x = np.arange(2)
width = 0.35

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(x - width/2, [control_not, control_yes], width, label='Control', color='#4C72B0', edgecolor='white')
ax.bar(x + width/2, [treatment_not, treatment_yes], width, label='Treatment', color='#DD8452', edgecolor='white')

ax.set_xticks(x)
ax.set_xticklabels(['Not Converted', 'Converted'])
ax.set_title('Conversion Distribution: Control vs Treatment')
ax.set_ylabel('Count')
ax.legend()
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('charts/distribution_plot.png', dpi=150)

from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

effect_size = abs(sum(treatment_converted)/len(treatment_converted) - 
                  sum(control_converted)/len(control_converted))

sample_sizes = np.arange(100, 50000, 500)
power_values = [analysis.solve_power(effect_size=effect_size, 
                                      nobs1=n, 
                                      alpha=0.05) for n in sample_sizes]

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(sample_sizes, power_values, color='#4C72B0', lw=2)
ax.axhline(y=0.8, color='red', linestyle='--', label='Power = 0.8 threshold')
ax.axvline(x=len(control_converted), color='green', linestyle='--', 
           label=f'Your sample size = {len(control_converted)}')

ax.set_title('Power Analysis: Sample Size vs Statistical Power')
ax.set_xlabel('Sample Size')
ax.set_ylabel('Statistical Power')
ax.legend()
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('charts/power_analysis.png', dpi=150)
