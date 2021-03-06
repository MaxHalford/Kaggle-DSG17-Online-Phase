from collections import Counter

import numpy as np
import pandas as pd
import xam


features = pd.read_csv('data/features.csv')
train_idxs = features['is_listened'].notnull()
train = features[train_idxs].copy()
test = features[~train_idxs].copy()

ewb = xam.preprocessing.EqualFrequencyBinner(n_bins=20)
ewb.fit(test[['user_listen_count']])
train['bin'] = ewb.transform(train[['user_listen_count']])
bin_counts = Counter(train['bin'])
train['weight'] = train['bin'].apply(lambda x: 1 / bin_counts[x])
train2 = train.sample(1300000, weights='weight').drop(['bin', 'weight'], axis='columns')

train_sample = train2.sample(50000)

y_cols = ['is_listened', 'sample_id']
X_train = train2.drop(y_cols, axis='columns').copy()
y_train = train2[y_cols].copy()

X_train_sample = train_sample.drop(y_cols, axis='columns').copy()
y_train_sample = train_sample[y_cols].copy()
X_test = test.drop(y_cols, axis='columns').copy()
y_test = test[y_cols].copy()

X_train.to_csv('data/X_train.csv', index=False)
y_train['is_listened'] = y_train['is_listened'].astype(int)
y_train.to_csv('data/y_train.csv', index=False)

X_train_sample.to_csv('data/X_train_sample.csv', index=False)
y_train_sample['is_listened'] = y_train['is_listened'].astype(int)
y_train_sample.to_csv('data/y_train_sample.csv', index=False)

X_test.to_csv('data/X_test.csv', index=False)
y_test['sample_id'] = y_test['sample_id'].astype(int)
y_test.to_csv('data/y_test.csv', index=False)
