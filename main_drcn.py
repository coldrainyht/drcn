from sklearn import preprocessing
from loader import *
from models import *

net_config = {
	'lr': 1e-4,
	'batch_size': 32,
	'nb_epoch': 50,
	'augmentation': True,
	'dropout': 0.5,
	'shuffle': True,
	'dense_dim': 300,
	'loss': 'categorical_crossentropy'
}

ae_config = {
	'lr': 1e-4,
	'batch_size': 32,
	'denoising': 0.4,
	'shuffle': True,
	'loss': 'squared_error',
	'input': 't'
}

src = 'usps'
tgt = 'mnist'

RESFILE = 'results/'+src+'-'+tgt+'_drcn_results_drop%.1f_aug%d_denoise%.1f.pkl.gz' % (net_config['dropout'], net_config['augmentation'], ae_config['denoising'])
PARAMFILE = 'results/'+src+'-'+tgt+'_drcn_weights_drop%.1f_aug%d_denoise%.1f.pkl.gz' % (net_config['dropout'], net_config['augmentation'], ae_config['denoising'])
PREDICTPREFIX = src+'-'+tgt+'_drcn_'
print(PARAMFILE)

# Load data
if src == 'svhn':
	(X_train, Y_train), (X_test, Y_test) = load_svhn()
	(_, _), (_, _), (X_tgt_test, Y_tgt_test) = load_mnist32x32()
elif src == 'mnist':
	if tgt == 'svhn':
		(X_train, Y_train), (_, _), (X_test, Y_test) = load_mnist32x32()
		(_, _), (X_tgt_test, Y_tgt_test) = load_svhn()
	else:
		(X_train, Y_train), (_, _), (X_test, Y_test) = load_mnist()
		(_, _), (X_tgt_test, Y_tgt_test) = load_usps()

elif src == 'usps':
	(X_train, Y_train), (X_test, Y_test) = load_usps()
	(_, _), (_, _), (X_tgt_test, Y_tgt_test) = load_mnist()



print('Preprocess data ...')
# X_train, scaler = remove_mean(X_train)
# X_test, _ = remove_mean(X_test, scaler=scaler)
# X_tgt_test, _ = remove_mean(X_tgt_test, scaler=scaler)

X_train = min_max(X_train)
X_test = min_max(X_test)
X_tgt_test = min_max(X_tgt_test)

[n, c, d1, d2] = X_train.shape


##### CONVEA ####
model = DRCN((c, d1, d2), 10, net_config, ae_config)
# model.create_architecture(input_shape=(c, d1, d2), dout=10, dropout=net_config['dropout'])
# model.compile(lr_net=net_config['lr'], lr_ae=ae_config['lr'])
model.train(X_train, Y_train,
			X_test=X_test, Y_test=Y_test, X_tgt=X_tgt_test, Y_tgt=Y_tgt_test,
			RESFILE=RESFILE, PARAMFILE=PARAMFILE, PREDICTPREFIX=PREDICTPREFIX)