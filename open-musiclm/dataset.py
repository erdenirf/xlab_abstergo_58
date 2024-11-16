from torch.utils.data import Dataset, DataLoader

class MusicDataset(Dataset):
    def __init__(self, yandex_path, download_dir, vocal_transform=None):
        self.yandex_path = yandex_path
        self.download_dir = download_dir
        self.transform = transform
        self.yandex = pd.read_csv("dataset.csv")

    def __len__(self):
        return len(self.yandex)

    def __getitem__(self, idx):
        cleaned_text = "".join([c if c in symbols else " " for c in self.yandex.iloc[:, 7][0]])
        input_tensor = torch.LongTensor([symbols.index(c) for c in cleaned_text]).unsqueeze(0).to(device)

        audio, sr = librosa.load("data/vocals/" + self.yandex['title'][idx] + "_vocals.mp3", sr=None)
        input_tensor = torch.tensor(audio, dtype=torch.float32)
        input_tensor = input_tensor.unsqueeze(0)


