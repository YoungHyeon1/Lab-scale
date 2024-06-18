import os
import torch
import torch.nn as nn
import json
import pickle

class TabTransformer(nn.Module):
    def __init__(self, num_categories, embed_dim, num_heads, num_layers, dropout_rate):
        super(TabTransformer, self).__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate
        self.embeddings = nn.ModuleList([nn.Embedding(num_categories[i], embed_dim) for i in range(len(num_categories))])
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dropout=dropout_rate)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        # 수정 필요 코드
        # self.regressor = nn.Linear(embed_dim * len(num_categories) + len(numeric_columns), 1)
        
        self._init_weights()

    def _init_weights(self):
        nn.init.kaiming_uniform_(self.regressor.weight, mode='fan_in', nonlinearity='relu')
        for embedding in self.embeddings:
            nn.init.kaiming_uniform_(embedding.weight, mode='fan_in', nonlinearity='relu')


    def forward(self, x_cat, x_num):
        x = [self.embeddings[i](x_cat[:, i]) for i in range(len(self.embeddings))]
        x = torch.stack(x, dim=1)
        x = self.transformer_encoder(x).view(x.size(0), -1)
        x = torch.cat((x, x_num), dim=1)
        output = self.regressor(x).squeeze()
        return output

def model_fn(model_dir):
    # pkl 파일 디렉토리
    pkl_files = [os.path.join(model_dir, f'category_info_{i}.pkl') for i in range(1, 12)]
    
    num_categories = []
    
    # 각 pkl 파일 읽기
    for pkl_path in pkl_files:
        with open(pkl_path, 'rb') as f:
            category_info = pickle.load(f)
            # category_info가 리스트 또는 딕셔너리라고 가정하고, 각 변수의 고유 개수를 num_categories에 추가
            if isinstance(category_info, dict):
                num_categories.extend([len(categories) for categories in category_info.values()])
            elif isinstance(category_info, list):
                num_categories.extend([len(categories) for categories in category_info])

    # 모델 초기화
    model = TabTransformer(num_categories=num_categories, embed_dim=32, num_heads=4, num_layers=6, dropout_rate=0.2)
    model_path = os.path.join(model_dir, 'TabTransformer_model.pth')
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def input_fn(request_body, request_content_type):
    return torch.tensor(json.loads(request_body), dtype=torch.float32)

def predict_fn(input_data, model):
    with torch.no_grad():
        return model(input_data).numpy()

def output_fn(prediction, content_type):
    return json.dumps(prediction.tolist())
