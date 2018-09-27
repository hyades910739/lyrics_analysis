'''
This is a tf_idf based document classifier, with KNN as classifier.

Reference : 
1. MUSIC EMOTION CLASSIFICATION OF CHINESE SONGS BASED ON LYRICS USING TF*IDF AND RHYME
2. AUTOMATIC MOOD CLASSIFICATIONUSING TF*IDF BASED ON LYRICS
'''
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.neighbors import KNeighborsClassifier
except:
    print("tfidf_classifier need to install sklearn,numpy,pandas.")
    exit()

'''
train_x : pd.DataFrame with wordcount.
train_y : pd.Series with wordcount.
the index of train_x,train_y should be matched.
n : knn parameter.
'''
def tfidf_classifier(train_x,train_y,test_x,test_y,n=3):
    label_set = set(train_y.values)
    tfidf_dict = {}
    for i in label_set:
        sel = train_y.index[train_y==i]
        tfidf_dict[i] = train_x.loc[sel,:].sum(0)
    emotion_tf = pd.DataFrame(tfidf_dict).transpose()
    transformer = TfidfTransformer()
    emotion_tfidf = transformer.fit_transform(emotion_tf)
    emotion_tfidf = pd.DataFrame(emotion_tfidf.toarray(),index=emotion_tf.index,columns=emotion_tf.columns)
    # get train feature:
    train_feature = pd.DataFrame(index=train_x.index,columns=emotion_tf.index)
    for title in train_x.index:
        train_feature.loc[title,:] = ((train_x.loc[title,:]>0)*emotion_tfidf).sum(1)

    # get test feature:
    test_feature = pd.DataFrame(index=test_x.index,columns=emotion_tf.index)
    for title in test_x.index:
        test_feature.loc[title,:] = ((test_x.loc[title,:]>0)*emotion_tfidf).sum(1)    
    
    #fit model
    neigh = KNeighborsClassifier(n_neighbors=n)
    neigh.fit(train_feature, train_y)

    #acc
    train_acc = np.mean(neigh.predict(train_feature)== train_y)
    test_acc = np.mean(neigh.predict(test_feature)== test_y)
    return(neigh,train_acc,test_acc)


def main():
    #load feature:
    vsm = pd.read_csv("vsm.csv",encoding="utf-8",index_col=0)
    #load label:
    df_label = pd.read_csv("label.csv",encoding = "utf-16",index_col=0)
    emotion = df_label.arousal.astype("str") + df_label.valence.astype("str").values
    df_label['emotion'] = pd.Categorical(emotion,categories=["00","01","10","11"])
    label_set = set(df_label.emotion.values)

    #split train and test set:
    # randomly select 4 item in each label as test set.
    test_sel = []
    np.random.seed(689)
    for i in label_set:    
        candidate = np.where(df_label.emotion==i)[0]
        test_sel = test_sel + np.random.choice(candidate,4,replace=False).tolist()

    train_sel = set(range(len(vsm))) - set(test_sel)
    train_sel = list(train_sel)    
        
    test_index = df_label.index[test_sel]    
    train_index = df_label.index[train_sel]
    train_x = vsm.loc[train_index,:]
    train_y = df_label.emotion.loc[train_index]
    test_x = vsm.loc[test_index,:]
    test_y = df_label.emotion.loc[test_index]

    #fit model
    model,train_acc,test_acc = tfidf_classifier(train_x,train_y,test_x,test_y,n=5)
    print("---  Result  ---")
    print("Train Acc : {}".format(train_acc))
    print("Test Acc : {}".format(test_acc))
    return 0

if __name__ == '__main__':
    main()