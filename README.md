# KDT-5_FlaskWebProject
경북대학교 KDT(Korea Digital Training) 웹 활용 프로젝트

## 성경 번역 모델

  
#### DATA
- kaggle
(https://www.kaggle.com/datasets/oswinrh/bible )
  


<br>
<br>
<details>
  <summary>
    이현길 ( 영어 -> 프랑스어 ) 
  </summary>

</details>
  
<details>
  <summary>
    이윤서 ( 영어 -> 한국어 )
  </summary>
  
</details>
  
<details>
  <summary>
    박희진 ( 영어 -> 독일어 )
  </summary>


## (1) 데이터 확인 및 전처리

- 팀 DB에 연결해서 데이터 불러오기
    - SELECT en.text as en, de.text as de FROM language_en en join language_de de on [en.id](http://en.id/) = [de.id](http://de.id/);
    - 쿼리문으로 join해서 DF 생성
- 데이터의 총 개수 : 31102개
- 각 언어의 토큰 갯수 시각화
    
    ![image](https://github.com/KDT5-WebD-4team/KDT-5_FlaskWebProject/assets/155441547/fe3df42c-45a4-48fa-9706-99a135d72ed1)

    
    - 최대 토큰 갯수가 103개여서, 넉넉하게 max_len = 128 지정

## (2) 데이터셋 준비

- 학습용 데이터는 30000개, 검증용 데이터는 나머지로 지정

## (3) 어휘사전 생성

- 토큰화 함수 생성
    - iterator로 구현
- 형태소 분석기로는 okt 사용
- UNK_IDX, PAD_IDX, BOS_IDX, EOS_IDX 지정
    - transformer는 데이터를 한꺼번에 넣기 때문에 문장의 시작과 끝을 지정해줄 인덱스 토큰이 필요
- build_vocab_iterator를 통해 어휘사전 생성
- src_lang(en)과 tat_lang(de)를 pickle 파일로 저장

## (4) Transformer 모델에 필요한 여러 클래스 및 함수 정의

### PositionalEncoding 클래스 정의

- 각도로 포지션 정보 계산
- 짝수는 sin함수 홀수는 cos함수를 사용하여 포지션 인코딩 값 계산
    - 문장에서 토큰의 상대적인 위치 지정
- 입력 텐서와 포지셔널 인코딩 값을 더한 후 드롭아웃 적용
    - dropout =  0.1

### TokenEmbedding 클래스 정의

- 입력 토큰에 대한 임베딩 값 반환

### Seq2SeqTransformer 클래스 정의

- Transformer model
    - 인코더의 레이어 수
    - 디코더의 레이어 수
    - 임베딩 차원의 크기
    - 입력 시퀀스의 최대 길이
    - 멀티 헤드 어텐션의 헤드 수
    - 소스 언어의 어휘 크기
    - 타겟 언어의 어휘 크기
    - 학습 신경망의 은닉층 크기
    - 드롭아웃 비율 ( 기본값 : 0.1 )
- 소스와 타겟 토큰 임베딩 레이어 초기화
- 포지셔널 인코딩 레이어 초기화
- 트랜스포머 모델 초기화
- 출력 레이어 초기화
- 소스와 타겟 시퀀스에 포지셔널 인코딩 적용
- 트랜스포머 모델에 입력 및 마스크 전달하여 출력 계산

### 전처리 함수

- 시작토큰과 끝 토큰 추가 후 텐서 병합

### collator 함수

- 패딩을 적용하여 모든 문장의 길이 통일

### mask 함수

- 0이면 -inf, 1이면 0.0으로 변환
    - 0으로 가중치 부여 → 어텐션 연산 수행 X
    - 1이면 어텐션 연산 수행
    - 1인 값(0.0)만 현재 값 계산에 참고
- 현재 해당하는 위치 이전 값만 참고하여 다음 위치의 토큰을 생성할 수 있도록 하기 위함

## (5) Transformer 모델 학습

```python
model = Seq2SeqTransformer(
    num_encoder_layers=3,
    num_decoder_layers=3,
    emb_size=512,
    max_len=512,
    nhead=8,
    src_vocab_size=len(vocab_transform[SRC_LANGUAGE]),
    tgt_vocab_size=len(vocab_transform[TGT_LANGUAGE]),
    dim_feedforward=512,
)
```

- batch_size = 128
- CrossEntropy 손실함수 이용
    - Cross-entropy 손실 함수는 두 확률 분포 사이의 차이를 측정 → nlp에 적합
- 옵티마이저는 Adam 이용
    - 러닝메이트는 0.01로 지정
- 스케쥴러 이용
    - 학습 함수에 스케쥴러를 이용해 조기 종료 기능 구현
    - Valid Loss가 5번 이상 개선이 안되면 조기 종료
- min_loss 값이 업데이트 될 때마다 모델 저장

## (6) Transformer 모델 평가

![스크린샷 2024-04-26 005903](https://github.com/KDT5-WebD-4team/KDT-5_FlaskWebProject/assets/155441547/2a0cfbcc-2a85-45cc-b850-81b6a0be7966)


> Train Loss : 1.779 
Val Loss : 5.472
> 

## (7) T5 모델 fine tunning

- 허깅페이스의 Reyansh4/NMT_T5_wmt14_en_to_de
- 성경 데이터를 통해 추가 학습

> Eval Loss : 1.0746161937713623
Eval Bleu : 11.00359095017138
> 

## (8) Bart 모델

- facebook/mbart-large-50-many-to-many-mmt
    - en to de
- 따로 fine tunning 하지는 않음

## (8) 예측

### Transformoer 모델

- 원문의 의미를 제대로 전달 못함. 문장 구조와 단어 선택이 무적절해서 의미가 다소 부정확함.

### T5 번역

- 전반적인 의미 전달은 되지만, 일부 부적절한 단어 선택과 성경체 사용이 부족한 편
- "sie" 복수 대명사, 비성경체 동사 활용 등 문제점 존재

### Bart 번역

- 가장 원문 의미에 가깝고 성경체 문체도 상당 부분 살려냄.
- "sie sagt", "gebe ihr", "ich werde...sehen" 등에서 성경체를 사용
- 단어 선택과 문장 구조도 자연스러움 원문을 가장 충실히 반영한 번역

## (9) 한계

- Transformer 모델은 단어 단위로 번역하는 한계를 지니어 T5 모델이나 Bart모델보다 문맥을 잘 학습하지 못한 것 같았다. 그에 반해 T5 모델이나 Bart모델은 앞 뒤 문장의 구조와 문맥을 잘 파악하여 깊이있게 학습되었다. 기본적으로 데이터가 부족했기 때문에 Transformer 모델의 성능이 낮은 걸 수도 있다. 또한 fine tunning한 T5 모델보다 Bart모델의 성능이 더 좋게 나왔는데, 내 생각에 이 또한 학습 데이터셋의 부족의 문제인 것 같다. 또한 제한된 시간 상 Epoch수를 많이 설정하지 못해서 제대로 학습되기 힘들었을 것이다. 그러나 Bart 모델은 디노이징 seq2seq 방식을 채택하여, 노이즈가 있는 입력에서 원본 출력을 재구성함으로써 T5 모델보다 입력과 출력 간의 관계를 보다 깊게 학습하는 것 같았다.
</details>

<details>
  <summary>
    고우석 ( 영어 -> 러시아어 ) 
  </summary>

</details>
