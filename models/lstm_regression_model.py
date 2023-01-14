from .stocks_model import StocksModel
from targets.task import Task

import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchmetrics import MeanAbsolutePercentageError

import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping

import numpy as np
from typing import List


class LSTMLightningModel(pl.LightningModule):
    def __init__(self, 
                 input_size: int,
                 hidden_size: int = 256, 
                 num_layers: int = 2, 
                 batch_first: bool = True,
                 dropout: float = 0.2,
                 bidirectional: bool = True,
                 learning_rate: float = 1e-4):
        
        super().__init__()
        
        self.lstm = nn.LSTM(input_size=input_size, 
                            hidden_size=hidden_size, 
                            num_layers=num_layers, 
                            batch_first=batch_first, 
                            dropout=dropout, 
                            bidirectional=bidirectional)
        
        final_states_output_dim = num_layers
        if bidirectional:
            final_states_output_dim *= 2
            
        self.linear = nn.Linear(in_features=hidden_size * final_states_output_dim, out_features=1)
        self.loss = nn.MSELoss()
        
        self.train_mape = MeanAbsolutePercentageError()
        self.val_mape = MeanAbsolutePercentageError()
        
        self.learning_rate = learning_rate
        
    
    def forward(self, batch):
        batch_size = len(batch["inputs"])
        
        _, (model_output, _) = self.lstm(batch["inputs"])
        model_output = model_output.transpose(0, 1)
        model_output = model_output.reshape(batch_size, -1)
        
        predictions = self.linear(model_output).squeeze()
        return predictions


    def training_step(self, batch, _):
        predictions = self.forward(batch)
        
        loss = self.loss(predictions, batch["labels"])
        self.train_mape(predictions, batch["labels"])
        
        return loss
    
    def training_epoch_end(self, _) -> None:
        self.log("train_epoch_mape", self.train_mape, prog_bar=True)
        
    
    def validation_step(self, batch, _):
        predictions = self.forward(batch)
        
        loss = self.loss(predictions, batch["labels"])
        self.val_mape(predictions, batch["labels"])
        
        return loss
    
    
    def validation_epoch_end(self, _):
        self.log("val_epoch_mape", self.val_mape, prog_bar=True)
        
    
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.learning_rate)
        
        return optimizer
    
    
class SequenceDataset(Dataset):
    def __init__(self, data_sequences: List[torch.Tensor], target_sequences: List[torch.Tensor] = None):
        self.data_sequences = torch.nn.utils.rnn.pad_sequence(data_sequences, batch_first=True)
        self.target_sequence = target_sequences


    def __len__(self):
        return len(self.data_sequences)    


    def __getitem__(self, idx):
        input = self.data_sequences[idx]
        if self.target_sequence is not None:
            label = self.target_sequence[idx]
            
            return {
                "inputs": input.float(),
                "labels": label[-1].float()
            }
        
        return {
            "inputs": input.float()
        }
    

class LSTMRegressionModel(StocksModel):
    def __init__(self, num_features: int, batch_size: int = 64, **kwargs):
        self.task = Task.REGRESSION
        
        self.batch_size = batch_size
        self.model = LSTMLightningModel(input_size=num_features, **kwargs)
        
        
    def fit(self, 
            train_inputs: List[np.ndarray], 
            train_targets: List[np.ndarray],
            val_inputs: List[np.ndarray] = None, 
            val_targets: List[np.ndarray] = None,
            max_epochs: int = 100):
        
        train_dataset = SequenceDataset(train_inputs, train_targets)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size)
        
        if val_inputs is not None and val_targets is not None:
            val_dataset = SequenceDataset(val_inputs, val_targets)
            val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)

            early_stopping_callback = EarlyStopping(
                monitor="val_epoch_mape",
                patience=2,
                min_delta=1e-3
            )    
            
            trainer = pl.Trainer(
                accelerator="gpu",
                devices=1,
                max_epochs=max_epochs,
                callbacks=early_stopping_callback
            )
            
            trainer.fit(self.model, train_loader, val_loader)
        
        else:
            early_stopping_callback = EarlyStopping(
                monitor="train_epoch_mape",
                patience=2,
                min_delta=1e-3
            )    
            
            trainer = pl.Trainer(
                accelerator="gpu",
                devices=1,
                max_epochs=max_epochs,
                callbacks=early_stopping_callback
            )
            
            trainer.fit(self.model, train_loader)
            
    
    def predict(self, test_inputs: List[np.ndarray]):
        test_dataset = SequenceDataset(test_inputs)
        test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)
        
        predictions = []
        with torch.no_grad():
            for batch in test_loader:
                predictions.append(self.model(batch["inputs"])).cpu()
                
        predictions = torch.vstack(predictions)
        return predictions
