from sklearn import preprocessing
from loader import *
from models import *

net_config = {
	'lr': 1e-4,
	'batch_size': 128,
	'nb_epoch': 50,
	'augmentation': False,
	'dropout': 0.5,
	'shuffle': False,
	'dense_dim': 300,
	'loss': 'categorical_crossentropy'
}

ae_config = {
	'lr': 1e-4,
	'batch_size': 128,
	'denoising': 0.5,
	'shuffle': False,
	'loss': 'squared_error'
}

src = 'svhn'
tgt = 'mnist'
model ='drcn-fixed'

RESFILE = 'results/'+src+'-'+tgt+'_'+model+'_results_drop%.1f_aug%d_denoise%.1f.pkl.gz' % (net_config['dropout'], net_config['augmentation'], ae_config['denoising'])
PARAMFILE = 'results/'+src+'-'+tgt+'_'+model+'_weights_drop%.1f_aug%d_denoise%.1f.pkl.gz' % (net_config['dropout'], net_config['augmentation'], ae_config['denoising'])
PREDICTPREFIX = src+'-'+tgt+'_'+model+'_'
print(PARAMFILE)


# Load data
if src == 'svhn':
	(X_train, Y_train), (X_test, Y_test) = load_svhn()
	(_, _), (_, _), (X_tgt_test, Y_tgt_test) = load_mnist32x32()
elif src == 'mnist':
	(X_train, Y_train), (_, _), (X_test, Y_test) = load_mnist32x32()
	(_, _), (X_tgt_test, Y_tgt_test) = load_svhn()


print('Preprocess data ...')
# X_train, scaler = remove_mean(X_train)
# X_test, _ = remove_mean(X_test, scaler=scaler)
# X_tgt_test, _ = remove_mean(X_tgt_test, scaler=scaler)

X_train = min_max(X_train)
X_test = min_max(X_test)
X_tgt_test = min_max(X_tgt_test)

[n, c, d1, d2] = X_train.shape


print('Load convnet weights')
PARAMFILE_NET = 'results/'+src+'-'+tgt+'_convnet_weights_drop0.5_aug0_h300.pkl.gz'
params_net = pickle.load(gzip.open(PARAMFILE_NET, 'rb'))


# ##### DRCN ####
print('Train DRCN...')
model = DRCN((c, d1, d2), 10, net_config, ae_config, enc_weights=params_net)
model.train(X_train, Y_train,
			X_test=X_test, Y_test=Y_test, X_tgt=X_tgt_test, Y_tgt=Y_tgt_test,
			RESFILE=RESFILE, PARAMFILE=PARAMFILE, PREDICTPREFIX=PREDICTPREFIX)