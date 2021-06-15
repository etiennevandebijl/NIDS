from pyod.models.iforest import IForest 
from pyod.models.pca import PCA
      
models = {
          "PCA_0.1":PCA(n_components=0.1, svd_solver="full", random_state = 0)#,
          #"PCA_0.5":PCA(n_components=0.5, svd_solver="full", random_state = 0),
         # "PCA_0.9":PCA(n_components=0.9, svd_solver="full", random_state = 0),
         #"IForest_5": IForest(n_estimators = 5, n_jobs = -1, random_state = 0, verbose = 0)#,
         # "IForest_10": IForest(n_estimators = 10, n_jobs = -1, random_state = 0, verbose = 0)
          }
