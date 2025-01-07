from simpletransformers.classification import ClassificationModel
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import datetime
import torch

train_args = {
    "output_dir": "outputs/",
    "cache_dir": "cache/",
    "fp16": True,
    "fp16_opt_level": "O1",
    "max_seq_length": 256,
    "train_batch_size": 32,
    "eval_batch_size": 32,
    "gradient_accumulation_steps": 1,
    "num_train_epochs": 5,
    "weight_decay": 0,
    "learning_rate": 4e-5,
    "adam_epsilon": 1e-8,
    "warmup_ratio": 0.06,
    "warmup_steps": 0,
    "max_grad_norm": 1.0,
    "do_lower_case": True,
    "logging_steps": 50,
    "evaluate_during_training": True,  # Enable evaluation during training
    "evaluate_during_training_steps": 2000,
    "evaluate_during_training_verbose": False,
    "use_cached_eval_features": False,
    "save_eval_checkpoints": False,
    "save_steps": 2000,
    "no_cache": False,
    "save_model_every_epoch": True,
    "tensorboard_dir": None,
    "overwrite_output_dir": True,
    "reprocess_input_data": True,
    "n_gpu": 1,
    "silent": False,
    "use_multiprocessing": True,
    "wandb_project": None,
    "wandb_kwargs": {},
    "use_early_stopping": True,
    "early_stopping_patience": 3,
    "early_stopping_delta": 0,
}


def load_data(file_path: str = 'data/kialoPairsEnglist.csv'):
    """
    Load the data from the csv file and return the train, validation, and test datasets.
    """
    df = pd.read_csv(file_path, index_col=0)

    # Rename 'relation' column to 'labels' and convert to numeric labels
    df = df.rename(columns={'relation': 'labels'})
    df['labels'] = df['labels'].map({'attack': 0, 'support': 1})
    
    # Drop the 'topic' column
    df = df.drop(columns=['topic'])
    df = df.rename(columns={'argSrc': 'text_a', 'argTrg': 'text_b'})
    
    # Split the data into train and test sets
    train_df, test_df = train_test_split(df, test_size=0.1, random_state=200)
    
    # Further split train_df into actual train and validation sets
    train_df, valid_df = train_test_split(train_df, test_size=0.1, random_state=200)
    
    train_labels = train_df['labels'].tolist()
    valid_labels = valid_df['labels'].tolist()
    test_labels = test_df['labels'].tolist()

    return train_df, valid_df, test_df, valid_labels, test_labels


if __name__ == "__main__":
    # Create classification model
    model = ClassificationModel(
        'distilbert',
        'distilbert-base-uncased',
        num_labels=2,
        use_cuda=True,
        cuda_device=0,
        args=train_args
    )

    # Load data with train, validation, and test sets
    train_df, valid_df, test_df, valid_labels, test_labels = load_data()

    print(datetime.datetime.now())
    
    # Train the model with validation data
    model.train_model(train_df, eval_df=valid_df)

    print(datetime.datetime.now())

    # Evaluate on test set
    result, model_outputs, wrong_predictions = model.eval_model(test_df, acc=sklearn.metrics.accuracy_score)
    print(result)

    # Predictions and calculate scores
    preds = [pred.tolist().index(max(pred.tolist())) for pred in model_outputs]

    print('Test F1-macro score:', f1_score(test_labels, preds, average='macro'))
    print('Test precision score:', precision_score(test_labels, preds, average='macro'))
    print('Test recall score:', recall_score(test_labels, preds, average='macro'))
