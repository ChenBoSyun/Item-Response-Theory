# Item-Response-Theory #
* <font size=5>introduce :</font> <br> It is machine learning model to implement the **computerized adaptive test** . <br>
We use MLE(maximum likelihood estimation) to estimate the question's parameter according to user's answer record(training data).

* <font size=5>usage :</font> <br> import : `import pretrained_model` <br> initialize with training data input: `model = pretrained_model.Model(trainind_data)` <br>
your training data need to be a metrix like this [[0,1,0,1,0],[1,1,1,1,1]]. 1 means the user answer is correct 0 means error. each row is each user's answer record.<br>
train model : `model.train(epochs = epochs , init_size = init_size)` <br>
epoch is the training time , default is 10 . init_size is the grid search's size ,default is 331. <br>
save the model :  `model.save()` <br> it will save the model into .pickle