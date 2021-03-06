from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score

import os
import codecs
import numpy as np
import pickle

basepath = os.path.dirname(os.path.abspath(__file__))+"/../featueExtraction/Output"
model_path = os.path.dirname(os.path.abspath(__file__))+"/TrainedClassifiers"
output_path = os.path.dirname(os.path.abspath(__file__))+"/Output"
eval_path = os.path.dirname(os.path.abspath(__file__))+"/Evaluation"


names = ["NearestNeighbors", "LinearSVM", "RBFSVM", "DecisionTree",
         "RandomForest", "AdaBoost", "QuadraticDiscriminantAnalysis", "LinearDiscriminantAnalysis", "NaiveBayes"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    QuadraticDiscriminantAnalysis(),
    LinearDiscriminantAnalysis(),
    GaussianNB()]

evaluation_names = ["Accuracy","F1 Score","F1_Micro","F1_Macro","F1_Weighted","Log_Loss","Precision","Recall","ROC_AUC"]

def evaluate(y_true,y_pred):
	return [accuracy_score(y_true, y_pred),
	f1_score(y_true, y_pred, average=None),
	f1_score(y_true, y_pred, average='micro'),
	f1_score(y_true, y_pred, average='macro'),
	f1_score(y_true, y_pred, average='weighted'),
	log_loss(y_true,y_pred),
	precision_score(y_true, y_pred, average=None),
	recall_score(y_true, y_pred, average=None),
	roc_auc_score(y_true, y_pred)]



def load_train_dataset(train_path):
    files = os.listdir(train_path)

    X_train = []
    y_train = []

    for filename in files:
        if filename == ".DS_Store":
            continue
        file = codecs.open(train_path+"/"+filename,'r','utf-8')

        for row in file:
            l = row.strip().split(",")
            X_train.append(l[0:11])
            y_train.append(int(l[11]))
        print(filename)
    return X_train,y_train


def load_test_dataset(test_path):
    files = os.listdir(test_path)

    X_test = []
    y_true = []

    for filename in files:
        if filename == ".DS_Store":
            continue
        file = codecs.open(test_path+"/"+filename,'r','utf-8')

        for row in file:
            l = row.strip().split(",")
            X_test.append(l[0:11])
            y_true.append(int(l[11]))
        print(filename)
    return X_test,y_true


def main():

    treshold_dirs = os.listdir(basepath)

    for dir in treshold_dirs:
        if dir == ".DS_Store":
            continue
        print(dir)
        ped_dirs = os.listdir(basepath+"/"+dir)

        for sub_dir in ped_dirs:
            if sub_dir == ".DS_Store":
                continue

            print(dir,sub_dir)

            train_path = basepath+"/"+dir+"/"+sub_dir+"/Train"
            test_path = basepath+"/"+dir+"/"+sub_dir+"/Test"

            write_file = codecs.open(output_path+"/"+dir+"_"+sub_dir+"-output.txt",'w','utf-8')
            eval_file = codecs.open(eval_path+"/"+dir+"_"+sub_dir+"-evaluation_scores.txt",'w','utf-8')

            X_train,y_train = load_train_dataset(train_path)
            X_test,y_true = load_test_dataset(test_path)
            X_train=np.array(X_train).astype(np.float)
            X_test=np.array(X_test).astype(float)
            # print(X_test)
            print(train_path,test_path)

            for algo, clf in zip(names, classifiers):
                try:
                    with open(model_path+"/"+dir+"/"+sub_dir+"/"+algo + '.pkl', 'rb') as f1:
                        clf = pickle.load(f1)
                except:
                    clf.fit(X_train, y_train)
                    with open(model_path+"/"+dir+"/"+sub_dir+"/"+algo + '.pkl', 'wb') as f1:
                        pickle.dump(clf, f1)

                predicted = []
                print(algo+"_fitted")

                for ind in range(0,len(X_test)):
                    vector = np.matrix(X_test[ind])
                    predicted+=[clf.predict(vector)[0]]
                
                print(algo, predicted, file=write_file)
                print(algo+"_Tested")

                scores = evaluate(y_true,predicted)
                print(algo+"\t"+str(scores),file=eval_file)


if __name__ == "__main__":main()
