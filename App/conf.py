import torch



DEVICE = ('cuda' if torch.cuda.is_available() else 'cpu')
REC_MODEL = 'vgg_seq2seq'
