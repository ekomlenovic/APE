"""
Load a saved model and test it on a dataset ('text_a','text_b','labels') .
"""

from simpletransformers.classification import ClassificationModel
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

def load_data(file_path) -> pd.DataFrame:
    """
    Load the data from the csv file and prepare it for testing.
    """
    df = pd.read_csv(file_path)
    
    # only take text_a,text_b,labels
    df = df[['text_a','text_b','labels']]
    print(df.head())
    
    print(f"Df shape: {df.shape}")
    # value counts
    print(df['labels'].value_counts())

    # check is there any null values or nan values

    print(df.isnull().sum())

    print("any nan values: ",df.isna().any())

    
    return df

def load_model(model_path : str) -> ClassificationModel:
    """
    Load the saved model.
    """
    model = ClassificationModel(
        'distilbert',
        model_path,
        use_cuda=True,  # Set to False if you're not using a GPU
        cuda_device=0
    )
    return model

def test_model(model : ClassificationModel, test_df : pd.DataFrame) -> None:
    """
    Test the model on the given dataset and print metrics.
    """
    texts_a = test_df['text_a'].tolist()
    texts_b = test_df['text_b'].tolist()
    labels = test_df['labels'].tolist()

    # Prepare input for the model
    to_predict = list(zip(texts_a, texts_b))
    print(f"to predict shape: {len(to_predict)}")
    # Predict using the model
    predictions, raw_outputs = model.predict(to_predict)
    
    # Calculate metrics
    accuracy = accuracy_score(labels, predictions)
    # Print metrics
    print(f"Accuracy: {accuracy}")


if __name__ == "__main__":
    # Path to your saved model
    model_path = "../../outputs/best_model"
    
    # Path to your test CSV file
    test_csv_path = "../../data/distance2.csv"
    
    # Load the model
    model = load_model(model_path)
    
    # Load the test data
    test_df = load_data(test_csv_path)
    
    # Test the model
    test_model(model, test_df)