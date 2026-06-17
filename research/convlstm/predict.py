import os
import glob
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from encoder import Encoder
from decoder import Decoder
from model import ED
from net_params import convlstm_encoder_params, convlstm_decoder_params, convgru_encoder_params, convgru_decoder_params
from data.mm import MovingMNIST

# ==================== 参数设置（必须和训练时一致） ====================
frames_input = 10
frames_output = 10
batch_size = 4

# 注意：如果你训练时加了 -clstm 参数，下面两行要改成 convlstm_*
encoder_params = convgru_encoder_params
decoder_params = convgru_decoder_params

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# ==================== 加载测试数据 ====================
testFolder = MovingMNIST(is_train=False,
                         root='data/',
                         n_frames_input=frames_input,
                         n_frames_output=frames_output,
                         num_objects=[3])
testLoader = torch.utils.data.DataLoader(testFolder,
                                         batch_size=batch_size,
                                         shuffle=False)

# ==================== 构建模型 ====================
encoder = Encoder(encoder_params[0], encoder_params[1]).to(device)
decoder = Decoder(decoder_params[0], decoder_params[1]).to(device)
net = ED(encoder, decoder).to(device)

# ==================== 自动查找最佳模型 ====================
save_dir = './save_model/2020-03-09T00-00-00'
checkpoints = glob.glob(os.path.join(save_dir, 'checkpoint_*.pth.tar'))

if not checkpoints:
    print("Error: No checkpoint found!")
    exit(1)

# 按文件名中的 loss 值排序，选最低的
best_ckpt = min(checkpoints, key=lambda x: float(os.path.basename(x).split('_')[-1].replace('.pth.tar','')))
print(f"Loading best model: {os.path.basename(best_ckpt)}")

checkpoint = torch.load(best_ckpt, map_location=device)
net.load_state_dict(checkpoint['state_dict'])
net.eval()

# ==================== 推理与评估 ====================
total_mse = 0
total_mae = 0
num_batches = 0

with torch.no_grad():
    for i, (idx, targetVar, inputVar, _, _) in enumerate(testLoader):
        inputs = inputVar.to(device)      # [B, S, C, H, W]
        labels = targetVar.to(device)     # [B, S, C, H, W]
        
        preds = net(inputs)               # [B, S, C, H, W]
        
        mse = torch.mean((preds - labels) ** 2).item()
        mae = torch.mean(torch.abs(preds - labels)).item()
        
        total_mse += mse
        total_mae += mae
        num_batches += 1
        
        # 只取第一个 batch 做可视化
        if i == 0:
            sample_idx = 0
            input_seq = inputs[sample_idx].cpu().numpy()   # [S, C, H, W]
            true_seq = labels[sample_idx].cpu().numpy()
            pred_seq = preds[sample_idx].cpu().numpy()
            
            n_show = min(5, frames_output)
            fig, axes = plt.subplots(3, n_show, figsize=(3*n_show, 9))
            
            for j in range(n_show):
                # 第1行：输入序列的最后1帧（作为参考）
                axes[0, j].imshow(input_seq[frames_input-1, 0], cmap='gray', vmin=0, vmax=1)
                axes[0, j].set_title('Last Input Frame' if j == 0 else '')
                axes[0, j].axis('off')
                
                # 第2行：真值
                axes[1, j].imshow(true_seq[j, 0], cmap='gray', vmin=0, vmax=1)
                axes[1, j].set_title(f'True t+{j+1}')
                axes[1, j].axis('off')
                
                # 第3行：预测
                axes[2, j].imshow(pred_seq[j, 0], cmap='gray', vmin=0, vmax=1)
                axes[2, j].set_title(f'Pred t+{j+1}')
                axes[2, j].axis('off')
            
            plt.suptitle(f'ConvLSTM Prediction Result\n(MSE: {mse:.6f}, MAE: {mae:.6f})', fontsize=14)
            plt.tight_layout()
            plt.savefig('prediction_comparison.png', dpi=200, bbox_inches='tight')
            print("Visualization saved to: prediction_comparison.png")
            plt.close()

avg_mse = total_mse / num_batches
avg_mae = total_mae / num_batches

print(f"\n{'='*55}")
print(f"  Evaluation Complete")
print(f"  Test batches: {num_batches}")
print(f"  Average MSE : {avg_mse:.6f}")
print(f"  Average MAE : {avg_mae:.6f}")
print(f"{'='*55}")