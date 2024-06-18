import sagemaker
from sagemaker.pytorch import PyTorchModel

# SageMaker 세션 설정
sagemaker_session = sagemaker.Session()
role = '추론 시 추가 예정'
model_path = '추론 시 추가 예정/TabTransformer_model.pth'

# PyTorch 모델 설정
pytorch_model = PyTorchModel(model_data=model_path,
                             role=role,
                             entry_point='inference.py',  # 추론 스크립트
                             framework_version='2.1.0',  # 사용한 PyTorch 버전
                             py_version='py3')

# 엔드포인트 이름
endpoint_name = 'Win-rate-TF'

# 엔드포인트 배포
predictor = pytorch_model.deploy(initial_instance_count=1,
                                 instance_type='ml.t3.medium',
                                 endpoint_name=endpoint_name)

# 엔드포인트 이름 출력 (엔드포인트 요청에 필요)
print(predictor.endpoint_name)