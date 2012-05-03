# Crossvalidated constraint SVC metamodel experiments

15+100 EA with tangent constraint on sphere function, best fitness is minimum. A local SVC metamodel is used to approximate the tangent constraint. Before n-fold crossvalidation, training and testing standardscore scaling is applied. N-fold crossvalidation is used on the best fitness feasibles and infeasibles for feature selection and parameter C and gamma adjustment. RBF kernel is used. In the following different approaches have been tested.

## Experiment A

![plot](http://i.imgur.com/g7JVC.png?1)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 10 samples per method. Methods: WithoutMetaModel with Death Penalty; SVCSlidingBestWeighted with window size = 50 and beta = 0.9; SVCCVSlidingBestWeighted with window size = 50, beta = 0.9 and with 5-fold crossvalidation and parameter C and gamma grid search.

