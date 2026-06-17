# AutoDL 云服务器运行指南

## 1. 上传文件

通过 FileZilla 上传整个 `LoongClaw` 文件夹到云服务器。

## 2. 安装依赖

```bash
cd LoongClaw
pip install -r requirements.txt
```

## 3. 运行测试

```bash
# 测试模型代码正确性
python tests/test_model.py
```

## 4. 开始训练

```bash
python src/training/train.py
```

## 注意事项

- AutoDL 通常已预装 PyTorch，可跳过 torch 安装
- 如需指定 CUDA 版本：
  ```bash
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
  ```
