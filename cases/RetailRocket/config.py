DATA_PATH = '../data/retailrocket/raw/'
DATA_PATH_PROCESSED = '../data/retailrocket/prepared/'
DATA_FILE = 'events'
SESSION_LENGTH = 30 * 60 #30 minutes

#filtering config (all methods)
MIN_SESSION_LENGTH = 2
MIN_ITEM_SUPPORT = 5

#min date config
MIN_DATE = '2014-04-01'

#days test default config 
DAYS_TEST = 1

#slicing default config
NUM_SLICES = 10
DAYS_OFFSET = 0
DAYS_SHIFT = 5
DAYS_TRAIN = 9
DAYS_TEST = 1

---
type: window # single|window
preprocessor: retailrocket # 
data:
  folder: data/retailrocket/raw/
  prefix: events

filter:
  min_item_support: 5
  min_session_length: 2
  
params:
  days_test: 2
  days_train: 25 #only window
  num_slices: 5 #only window
  days_offset: 0 #only window
  days_shift: 27 #only window

output:
  folder: data/retailrocket/slices/
    
    
---
type: window # single|window, maybe add opt
key: hybrids#added to the csv names
evaluation: evaluation #evaluation|evaluation_last|evaluation_multiple
data:
  name: retailrocket #added in the end of the csv names
  folder: ../../data/retailrocket/slices/
  prefix: events
  slices: 5 #only window
#  skip: [0,3] #only window
  #opts: {sessions_test: 10}

results:
  folder: results/window/

metrics:
- class: accuracy.HitRate
  length: [5,10,15,20]
- class: accuracy.MRR
  length: [5,10,15,20]
- class: coverage.Coverage
  length: [20]
- class: popularity.Popularity
  length: [20]
- class: time_memory_usage.Time_usage_training
- class: time_memory_usage.Time_usage_testing
- class: time_memory_usage.Memory_usage

algorithms:
- class: hybrid.weighted.WeightedHybrid
  params:
    algorithms:
#    - class: baselines.sr.SequentialRules
#      params: { weighting: div }
#      key: sr
#    - class: baselines.ar.AssociationRules
#      key: ar
    - class: filemodel.resultfile.ResultFile
      params: { file: ../../data/retailrocket/slices/recs/sknn }
      key: narm
    - class: filemodel.resultfile.ResultFile
      params: { file: ../../data/aotm/slices/recs/sr }
      key: sr
    fit: True
  params_var:
    weights: [[0.25, 0.75],[0.5, 0.5],[0.75, 0.25],[0.1, 0.9],[0.9, 0.1],[0.2, 0.8],[0.8, 0.2],[0.3, 0.7],[0.7, 0.3],[0.4, 0.6],[0.6, 0.4]] 
  key: weighted
- class: hybrid.weighted.WeightedHybrid
  params:
    algorithms:
#    - class: baselines.sr.SequentialRules
#      params: { weighting: div }
#      key: sr
#    - class: baselines.ar.AssociationRules
#      key: ar
    - class: filemodel.resultfile.ResultFile
      params: { file: ../../data/retailrocket/slices/recs/vsknn }
      key: narm
    - class: filemodel.resultfile.ResultFile
      params: { file: ../../data/aotm/slices/recs/sr }
      key: sr
    fit: True
  params_var:
    weights: [[0.25, 0.75],[0.5, 0.5],[0.75, 0.25],[0.1, 0.9],[0.9, 0.1],[0.2, 0.8],[0.8, 0.2],[0.3, 0.7],[0.7, 0.3],[0.4, 0.6],[0.6, 0.4]] 
  key: weighted
