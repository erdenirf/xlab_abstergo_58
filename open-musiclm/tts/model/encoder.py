import torch
from config import TTS_DEVICE

class SileroTTSEncoder:
    def __init__(self):
        torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
                                       'latest_silero_models.yml',
                                       progress=False)
        language = 'ru'
        speaker = 'kseniya_16khz'
        silero_tts = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language=language,
            speaker=speaker)

        self.model, self.symbols, self.sample_rate, example_text, self.apply_tts = silero_tts
        self.model.eval()
        self.model = self.model.to(TTS_DEVICE)

        self.embeder = self.model.tacotron.embedding.to(TTS_DEVICE)
        self.encoder = self.model.tacotron.encoder.to(TTS_DEVICE)
        self.decoder = self.model.tacotron.decoder.to(TTS_DEVICE)

    def encode_to_mel(self, text) -> torch.Tensor:
        cleaned_example_text = "".join([c if c in self.symbols else " " for c in text])

        sequence = torch.LongTensor(self.symbols.index(c) for c in cleaned_example_text).unsqueeze(0).to(TTS_DEVICE)
        embedded_inputs = self.embeder(sequence).transpose(1, 2)
        encoder_outputs = self.encoder(embedded_inputs)
        mel_outputs, gate_outputs, alignments, mel_lengths = self.decoder(encoder_outputs)
        return mel_outputs