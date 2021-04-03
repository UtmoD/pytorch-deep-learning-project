import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams["font.family"] = "serif"

import torch

import numpy as np


from computational_graphs.estimators.problems.multi_obj.nas_gradient_free import NasBench201GradientFree

# init = torch.load('experiments/exp-20210323-1754/checkpoints/[NSGAII] Gen_1.pth.tar')
# last = torch.load('experiments/[NSGAII] Gen_40.pth.tar')
# # f1 = gen1['eval_dict']['f_pop_obj']
# f_last = last['eval_dict']['f_pop_obj']
# current_gen = last['gen']
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter(f_last[:, 0], f_last[:, 1], f_last[:, 2])
# # ax.scatter(f1[:, 0], f1[:, 1], f1[:, 2], color='red')

# ax.set_xlabel('FLOPS')
# ax.set_ylabel('NTK')
# ax.set_zlabel('LR')
# plt.show()
# print('debug')

def get_err(X):
    indices = []
    flops, t_err_X, v_err_X = [], [], []
    for i in range(X.shape[0]):
        x = X[i]
        p_x = problem.decode(x)
        idx_x = problem.api.query_index_by_arch(p_x)
        indices += [idx_x]
    # indices = list(set(indices))
    # for idx_x in indices:
        flop = problem.api.get_cost_info(idx_x, dataset, hp='200')['flops']
        flops += [flop]
        t_err = \
            100 - problem.api.get_more_info(idx_x, dataset, hp='200', is_random=False)['test-accuracy']
        v_err = \
            100 - problem.api.get_more_info(idx_x, dataset, hp='12', is_random=False)['train-accuracy']
        v_err_X += [v_err]
        t_err_X += [t_err]
    # t_err_X = list(set(t_err_X))
    # flops = list(set(flops))
    # v_err_X = list(set(v_err_X))
    return np.array(t_err_X),\
           np.array(v_err_X),\
           np.array(flops),\
           indices

def plot(X, Y, color, linestyle, label):
    ax.plot(X, Y, color=color, linestyle=linestyle, label=label)
def scatter(X, Y, marker, color):
    ax.scatter(X, Y, color=color, marker=marker)

def plot_front(X, 
               Y,
               marker, 
               linestyle, 
               color, 
               label):
    sorted_idx = np.argsort(X)
    plot(X[sorted_idx], Y[sorted_idx], color, linestyle, label)
    scatter(X[sorted_idx], Y[sorted_idx], marker, color)


dataset = 'cifar10'
fig, ax = plt.subplots()

problem = NasBench201GradientFree(dataset, 4, cuda=False)

# A = torch.load('experiments/[NSGAII] Gen_200.pth_11.tar')
A = torch.load('experiments/NSGA_II_flops-val_err-ux-g200/checkpoints/[NSGAII] Gen_200.pth.tar')
B = torch.load('experiments/[NSGAII] Gen_200.pth_12.tar')
# 

# plot_front(B['eval_dict']['f_pop_obj'][:, 0],
#            B['eval_dict']['f_pop_obj'][:, 1],
#            marker='x',
#            linestyle='--',
#            color='blue',
#            label='FLOPS - NTK_LR (200)')

# plot_front(A['eval_dict']['f_pop_obj'][:, 0],
#            A['eval_dict']['f_pop_obj'][:, 1],
#            marker='x',
#            linestyle='--',
#            color='red',
#            label='FLOPS - NTK_LR (40)')

t_err_A, v_err_A, flops_A, indices_A = get_err(A['pop'])
t_err_B, v_err_B, flops_B, indices_B = get_err(B['pop'])


plot_front(flops_B, v_err_B, 
           marker='x', 
           linestyle='--', 
           color='green',
           label='(G:{}) Val Err 12 epochs [NTK-LR]'.format(B['gen']))
plot_front(flops_A, v_err_A, 
           marker='o', 
           linestyle='--', 
           color='blue',
           label='(G:{}) Val Err 12 epochs [FLOPS-VALID_ERR]'.format(A['gen']))

plot_front(flops_B, t_err_B, 
           marker='v', 
           linestyle='--', 
           color='cyan',
           label='(G:{}) Test Err [NTK-LR]'.format(B['gen']))
plot_front(flops_A, t_err_A, 
           marker='^', 
           linestyle='--', 
           color='red',
           label='(G:{}) Test Err [FLOPS-VALID_ERR]'.format(A['gen']))

ax.set_xlabel('FLOPS')
ax.set_ylabel('Error Rate (%)')
# ax.set_ylabel('NTK_LR')
ax.legend(loc='best')
ax.grid(True, linestyle='--')
ax.set_title(dataset.upper() + ' 200 epochs')
plt.show()