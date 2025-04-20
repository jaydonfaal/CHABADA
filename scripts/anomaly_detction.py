from sklearn.svm import OneClassSVM
import numpy as np

# Assume `api_features` is a binary matrix [apps x APIs]
api_features = np.array(your_binary_feature_matrix)

# Train per-cluster OC-SVM model
model = OneClassSVM(kernel='rbf', gamma='auto').fit(api_features)

# Predict anomalies (-1 indicates anomaly)
predictions = model.predict(api_features)

anomalies = np.where(predictions == -1)[0]
print("Anomalous apps indices:", anomalies)
