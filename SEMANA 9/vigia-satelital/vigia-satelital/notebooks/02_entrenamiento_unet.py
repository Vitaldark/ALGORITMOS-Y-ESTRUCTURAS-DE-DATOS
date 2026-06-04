# VIGIA SATELITAL — Notebook 2: Entrenamiento U-Net
# Ejecutar en Google Colab con GPU T4

# CELDA 1: Instalar
# !pip install segmentation-models-pytorch albumentations rasterio

# CELDA 2: Imports
import torch
import numpy as np
import rasterio
from torch.utils.data import Dataset, DataLoader
import segmentation_models_pytorch as smp
import albumentations as A
from albumentations.pytorch import ToTensorV2
from pathlib import Path

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Dispositivo: {DEVICE}")

# CELDA 3: Dataset
class MiningDataset(Dataset):
    def __init__(self, img_dir, mask_dir, transform=None):
        self.imgs      = sorted(Path(img_dir).glob('*.npy'))
        self.masks     = sorted(Path(mask_dir).glob('*.npy'))
        self.transform = transform

    def __len__(self): return len(self.imgs)

    def __getitem__(self, idx):
        img  = np.load(self.imgs[idx]).astype(np.float32) / 10000.0
        mask = np.load(self.masks[idx]).astype(np.float32)
        img  = np.transpose(img, (1, 2, 0))  # (4,H,W) -> (H,W,4)
        if self.transform:
            out = self.transform(image=img, mask=mask)
            img, mask = out['image'], out['mask']
        return img, mask.unsqueeze(0)

# CELDA 4: Augmentacion
train_tf = A.Compose([
    A.RandomRotate90(p=0.5), A.HorizontalFlip(p=0.5), A.VerticalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3), ToTensorV2(),
])
val_tf = A.Compose([ToTensorV2()])

# CELDA 5: Modelo U-Net + ResNet50
model = smp.Unet(
    encoder_name="resnet50", encoder_weights="imagenet",
    in_channels=4, classes=1, activation='sigmoid'
).to(DEVICE)
print(f"Parametros totales: {sum(p.numel() for p in model.parameters()):,}")

# CELDA 6: Loss + optimizer
criterion  = smp.losses.DiceLoss(mode='binary') + smp.losses.SoftBCEWithLogitsLoss()
optimizer  = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-5)
scheduler  = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)

def run_epoch(loader, train=True):
    model.train() if train else model.eval()
    loss_sum, iou_sum = 0, 0
    ctx = torch.enable_grad() if train else torch.no_grad()
    with ctx:
        for imgs, masks in loader:
            imgs, masks = imgs.to(DEVICE), masks.to(DEVICE)
            if train: optimizer.zero_grad()
            preds = model(imgs)
            loss  = criterion(preds, masks)
            if train: loss.backward(); optimizer.step()
            iou = smp.metrics.iou_score((preds>0.5).long(), masks.long(), reduction='micro')
            loss_sum += loss.item(); iou_sum += iou.item()
    return loss_sum/len(loader), iou_sum/len(loader)

# CELDA 7: Entrenar (descomentar cuando tengas los datos listos)
# train_ds = MiningDataset('datasets/processed/train/imgs', 'datasets/processed/train/masks', train_tf)
# val_ds   = MiningDataset('datasets/processed/val/imgs', 'datasets/processed/val/masks', val_tf)
# train_loader = DataLoader(train_ds, batch_size=8, shuffle=True, num_workers=2)
# val_loader   = DataLoader(val_ds, batch_size=4, shuffle=False, num_workers=2)
# best_iou = 0
# for epoch in range(1, 51):
#     tl, ti = run_epoch(train_loader, train=True)
#     vl, vi = run_epoch(val_loader,   train=False)
#     scheduler.step()
#     print(f"Ep{epoch:02d} | Loss={tl:.4f} mIoU={ti:.4f} | Val Loss={vl:.4f} mIoU={vi:.4f}")
#     if vi > best_iou:
#         best_iou = vi
#         torch.save(model.state_dict(), 'models/unet_resnet50_best.pth')
#         print(f"  Mejor modelo guardado mIoU={best_iou:.4f}")
