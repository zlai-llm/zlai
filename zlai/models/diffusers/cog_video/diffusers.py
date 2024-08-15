import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video


__all__ = [

]


def load_cog_video():
    """"""
    return None


prompt = "A panda, dressed in a small, red jacket and a tiny hat, sits on a wooden stool in a serene bamboo forest. The panda's fluffy paws strum a miniature acoustic guitar, producing soft, melodic tunes. Nearby, a few other pandas gather, watching curiously and some clapping in rhythm. Sunlight filters through the tall bamboo, casting a gentle glow on the scene. The panda's face is expressive, showing concentration and joy as it plays. The background includes a small, flowing stream and vibrant green foliage, enhancing the peaceful and magical atmosphere of this unique musical performance."

pipe = CogVideoXPipeline.from_pretrained(
    "THUDM/CogVideoX-2b",
    torch_dtype=torch.float16
)

pipe.enable_model_cpu_offload()

prompt_embeds, _ = pipe.encode_prompt(
    prompt=prompt,
    do_classifier_free_guidance=True,
    num_videos_per_prompt=1,
    max_sequence_length=226,
    device="cuda",
    dtype=torch.float16,
)

video = pipe(
    num_inference_steps=50,
    guidance_scale=6,
    prompt_embeds=prompt_embeds,
).frames[0]

export_to_video(video, "output.mp4", fps=8)
