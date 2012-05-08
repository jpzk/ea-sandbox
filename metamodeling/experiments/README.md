# SVC metamodel experiments

15+100 EA with tangent constraint on sphere function, best fitness is minimum. A local SVC metamodel is used to approximate the tangent constraint. Before n-fold crossvalidation, training and testing standardscore scaling is applied. N-fold crossvalidation is used on the best fitness feasibles and infeasibles for feature selection and parameter C and gamma adjustment. RBF kernel is used. In the following different approaches have been tested.

## Experiment C

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 200 samples per method. Methods: WithoutMetaModel with Death Penalty; SVCSlidingBestWeighted with Death Penalty window size = 25 and beta = 0.9, append_to_window = 10; SVCCVSlidingBestWeighted with Death Penalty window size = 25, beta = 0.9 and with 5-fold crossvalidation and parameter C and gamma grid search and standard score scaling; SVCBestWeighted using amount_metamodel = 50 best feasibles and infeasibles and beta = 0.9. Termination on 10^-2 accuracy on 0.0.

### Constraint calls
![](http://i.imgur.com/vtOFj.png)
### Wrong classification by meta model
![](http://i.imgur.com/YHrni.png)
### Generations
![](http://i.imgur.com/Ik2xD.png)

