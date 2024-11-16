from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import time
from open_musiclm.open_musiclm import MusicLM
from open_musiclm.config import create_musiclm_from_config
from open_musiclm.config import load_model_config
from einops import rearrange
#from torch import rearrange

app = FastAPI()
duration = 10  # define the duration in seconds
return_coarse_wave = False  # or True

def model_generate(prompt: str) -> str:

    semantic_path = "checkpoints_new/semantic.transformer.14000.pt"
    coarse_path = "checkpoints_new/coarse.transformer.18000.pt"
    fine_path = "checkpoints_new/fine.transformer.24000.pt"
    rvq_path = 'checkpoints_new/clap.rvq.950_no_fusion.pt'
    kmeans_path = "checkpoints_new/kmeans_10s_no_fusion.joblib"
    model_config = "./configs/model/musiclm_large_small_context.json"
    results_folder = "results"

    device = 'cuda:0'
    model_config = load_model_config(model_config)
    musiclm = create_musiclm_from_config(
            model_config=model_config,
            semantic_path=semantic_path,
            coarse_path=coarse_path,
            fine_path=fine_path,
            rvq_path=rvq_path,
            kmeans_path=kmeans_path,
            device=device)

    generated_wave = musiclm.forward(
                text=prompt,
                output_seconds=duration,
                semantic_window_seconds=model_config.global_cfg.semantic_audio_length_seconds,
                coarse_window_seconds=model_config.global_cfg.coarse_audio_length_seconds,
                fine_window_seconds=model_config.global_cfg.fine_audio_length_seconds,
                semantic_steps_per_second=model_config.hubert_kmeans_cfg.output_hz,
                acoustic_steps_per_second=model_config.encodec_cfg.output_hz,
                return_coarse_generated_wave=return_coarse_wave,
            )
    print(generated_wave.shape)
    generated_wave = rearrange(generated_wave, 'b n -> b 1 n')
    return generated_wave


@app.post("/generation/{prompt}", response_class=FileResponse)
def generation_prompt(prompt: str) -> str:
    
    return model_generate(prompt)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", reload=False)