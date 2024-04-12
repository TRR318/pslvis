
data:
    sorted list of unused features
    sorted list of used features
    list of assigned scores
    list of assigned thresholds

- sorting used features, will sort scores and thresholds accordingly
- moving an element from unused to used will trigger retraining with constraints on features, scores and thresholds
- moving feature from used to unused
- re-ordering features


later score changes

later score deletions
- deleting scores will trigger retraining with feature list and partially set scores
- we should also be possible of deleting multiple scores at the same time.

later threshold changes/deletions