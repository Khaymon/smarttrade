from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

METRICS = {
    "MAPE": mean_absolute_percentage_error,
    "MAE": mean_absolute_error,
    "MSE": mean_squared_error
}