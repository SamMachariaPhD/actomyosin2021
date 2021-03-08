# Plot lifetime histogram from bindingLifetime.py
# Regards, Sam Macharia

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

m1r_lyf0 = pd.read_csv('lyf8_active_label_life.csv')
m2r_lyf0 = pd.read_csv('lyf10_defective_label_life.csv')

# Make lifetime histogram.
fig, ax = plt.subplots(1,2, sharex=False, sharey=False, figsize=(10,8))
#fig.add_subplot(231, frameon=False)
bins = np.arange(0.0,0.51,0.01)

ax[0].hist(0.01*m1r_lyf0['life'], bins=bins, color = 'green', ec='black', alpha=1, label='Active') # , hatch='/'
#ax[0].set_xticks(np.arange(0.0,0.51,0.1))
#ax[0].set_yticks(np.arange(0,15001,2500))
ax[0].tick_params(labelsize=14)
#ax[0].set_xlabel('Lifetime (sec)', fontsize=16)
#ax[0].set_ylabel('Number of occurrences', fontsize=16)
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)
ax[0].spines['bottom'].set_bounds(0,0.5)
#ax[0].spines['left'].set_bounds(0,12500)
#ax[0].legend(loc='upper left')
mlyf = round(np.mean(0.01*m1r_lyf0['life']), 2)
ax[0].set_title('Active | $\mu$ = %s'%mlyf, fontsize=16)

#fig.add_subplot(232, frameon=False)
bins = np.arange(0.0,5.1,0.01)
ax[1].hist(0.01*m2r_lyf0['life'], bins=bins, color = 'blue', ec='black', alpha=1, label='Defective')
#ax[1].set_xticks(np.arange(0.0,2.1,0.4))
#ax[1].set_yticks(np.arange(0,1801,300))
ax[1].tick_params(labelsize=14, labelleft=True) # False -- if y scale is the same
#ax[1].set_xlabel('Lifetime (sec)', fontsize=16)
#ax[1].set_ylabel('Number of occurrences', fontsize=16)
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[1].spines['bottom'].set_bounds(0,2.0)
#ax[1].spines['left'].set_bounds(0,12500)
#ax[1].legend(loc='upper left')
mlyf = round(np.mean(0.01*m2r_lyf0['life']), 2)
ax[1].set_title('Defective | $\mu$ = %s'%mlyf, fontsize=16)

fig.text(0.5,0.04, 'Lifetime (sec)', fontsize=16, va='center', ha='center')
fig.text(0.03,0.5, 'Occurrences', fontsize=16, va='center', ha='center', rotation='vertical')

plt.subplots_adjust(hspace=0.3)

plt.savefig('A_Defe_ctiveLifetime.svg', fmt='.svg', dpi=1200, bbox_inches='tight')
plt.savefig('A_Defe_ctiveLifetime.png', fmt='.png', dpi=1200, bbox_inches='tight')

plt.show()