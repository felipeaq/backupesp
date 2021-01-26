import pickle
from collections import deque
import numpy as np
#from sensors import *
from read_routine import *
class KPredictior:
    __instance = None
    PATH="../res/xgb.pkl"
    
    def __new__(cls):
        if KPredictior.__instance is None:
            KPredictior.__instance = object.__new__(cls)
            MAXLEN=100
            with open(KPredictior.PATH, 'rb') as f:
                KPredictior.__instance.model= pickle.load(f)
            KPredictior.__instance.values=deque(maxlen=MAXLEN)
            KPredictior.__instance.MAX=0.35
            KPredictior.__instance.MAXLEN=MAXLEN
            KPredictior.__instance.rm_freqs=[0,60,130]
            KPredictior.__instance.n_neighbors=[0,Sensors.MAX_X//50,Sensors.MAX_X//50]
        return KPredictior.__instance

    def freq_to_index(self,acc_rate,freqs,l,n_neighbors):
        idx=[]
        max_rate=acc_rate/2
        min_rate=acc_rate/l
        for i ,neigh in zip(freqs,n_neighbors):
            val=i/min_rate
            idx+=list(range(int(val-neigh),int(val+neigh+1)))
        return idx

    def get_rm_index(self):
        rm_index=self.freq_to_index(ReadRoutine().sensors.list_s[2].a[2].last_acc_rate,self.rm_freqs,Sensors.MAX_X,self.n_neighbors)
        return rm_index

    def append_predict(self,v):
        
        if  not (v is None):
            rm_index=self.get_rm_index()
            u=np.delete(v,rm_index)
            if len(u)==len(self.model.feature_importances_):
                self.values.append(self.model.predict_proba([u])[0])
            

    def get_prob (self):
        p=[0,0,0]
        N=len(self.values)
        M=0
        if self.values:
            p=[]
            M=len(self.values[0])
        for i in range(M):
            s=0
            for j in range(N):
                s+=self.values[j][i]
            p.append(s/N)
        return p
