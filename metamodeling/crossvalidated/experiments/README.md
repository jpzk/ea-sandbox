# Crossvalidated constraint SVC metamodel experiments

15+100 EA with tangent constraint on sphere function, best fitness is minimum. A local SVC metamodel is used to approximate the tangent constraint. Before n-fold crossvalidation, training and testing standardscore scaling is applied. N-fold crossvalidation is used on the best fitness feasibles and infeasibles for feature selection and parameter C and gamma adjustment. RBF kernel is used. In the following different approaches have been tested.

## Experiment A

![plot](http://i.imgur.com/g7JVC.png?1)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 10 samples per method. Methods: WithoutMetaModel with Death Penalty; SVCSlidingBestWeighted with window size = 50 and beta = 0.9; SVCCVSlidingBestWeighted with window size = 50, beta = 0.9 and with 5-fold crossvalidation and parameter C and gamma grid search.

## Experiment B

![plot](http://i.imgur.com/2xsjZ.png)
![plot](http://i.imgur.com/fIdYW.png)
![plot](http://i.imgur.com/fFpDF.png)
![plot](http://i.imgur.com/r1Yxe.png)
![plot](http://i.imgur.com/BW0cm.png)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 200 samples per method. Methods: WithoutMetaModel with Death Penalty; SVCSlidingBestWeighted with window size = 50 and beta = 0.9; SVCCVSlidingBestWeighted with window size = 50, beta = 0.9 and with 5-fold crossvalidation and parameter C and gamma grid search; SVCBestWeighted using 10 best feasibles and infeasibles and beta = 0.9.

# Important remark

SVCBestWeighted has most classification error by meta model, but constraint calls are low - theres a mistake in the implementation: when a new generated child is classified infeasible by meta model, a new child has to be generated and tested with against either meta model or constraint function. This is missing therefore there's an unintentional bias, which is emphasized by SVCBestWeighted but is a programming mistake in SVCBestSlidingWeighted and SVCCVSlidingWeighted as well.

