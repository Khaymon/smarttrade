import argparse
import pandas as pd
from typing import List
from tqdm import tqdm

import torch
from torch.utils.data import Dataset, DataLoader

from transformers import AutoModel, AutoTokenizer


class NewsDataset(Dataset):
    def __init__(self, data: pd.DataFrame, tokenizer, max_length: int):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        article = self.data.iloc[idx]
        text = article["header"] + self.tokenizer.sep_token + article["body"]
        text_tokenized = self.tokenizer(text, 
                                        truncation=True, padding="max_length", 
                                        max_length=self.max_length,
                                        return_tensors="pt")
        
        return {
            "input_ids": text_tokenized["input_ids"].squeeze(),
            "attention_mask": text_tokenized["attention_mask"].squeeze()
        }
        
    
def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="News embeddings",
        description="Collecting of embeddings for news datasets"
    )
    
    parser.add_argument("-m", "--model-name", type=str, dest="model_name", help="Model name from huggingface hub")
    parser.add_argument("-f", "--file", type=str, dest="file", help="News file path")
    parser.add_argument("-l", "--max-lenght", type=int, default=256, dest="max_length",
                        help="Max length of concatenation of header and body")
    parser.add_argument("-b", "--batch-size", type=int, default=8, dest="batch_size", help="DataLoader batch size")
    parser.add_argument("-o", "--output-file", type=str, dest="output_file", help="Embeddings output file")
    
    return parser.parse_args()
    
    
def collect_embeddings(data: pd.DataFrame, model_name: str, max_length: int, batch_size: int) -> List[torch.Tensor]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    
    news_dataset = NewsDataset(data=data, tokenizer=tokenizer, max_length=max_length)
    news_loader = DataLoader(news_dataset, batch_size=batch_size, shuffle=False)
    
    embeddings_list = []
    with torch.no_grad():
        for batch in tqdm(news_loader):
            model_output = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
            embeddings = model_output["last_hidden_state"].cpu()
            
            embeddings_list.append(embeddings[:, 0])
            
    return embeddings_list
    

def main():
    arguments = parse_arguments()
    print(arguments)
    
    news_data = pd.read_csv(arguments.file, parse_dates=["date"], index_col="date")
    embeddings_list = collect_embeddings(data=news_data, model_name=arguments.model_name,
                                    max_length=arguments.max_length, batch_size=arguments.batch_size)

    embeddings = torch.vstack(embeddings_list).numpy()
    embeddings_df = pd.DataFrame(embeddings, index=news_data.index)
    
    embeddings_df.to_csv(arguments.output_file)
    
    
if __name__ == "__main__":
    main()