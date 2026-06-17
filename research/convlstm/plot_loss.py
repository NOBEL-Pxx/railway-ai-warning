import matplotlib.pyplot as plt

with open('avg_train_losses.txt', 'r') as f:
    train_loss = [float(line.strip()) for line in f.readlines()]

with open('avg_valid_losses.txt', 'r') as f:
    valid_loss = [float(line.strip()) for line in f.readlines()]

plt.figure(figsize=(10, 6))
plt.plot(train_loss, label='Train Loss', linewidth=1.5)
plt.plot(valid_loss, label='Valid Loss', linewidth=1.5)
plt.xlabel('Epoch')
plt.ylabel('MSE Loss')
plt.legend()
plt.title('ConvLSTM Training Curve (Moving-MNIST)')
plt.grid(True, alpha=0.3)
plt.savefig('loss_curve.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Total epochs: {len(train_loss)}")
print(f"Best valid loss: {min(valid_loss):.6f} at epoch {valid_loss.index(min(valid_loss))}")