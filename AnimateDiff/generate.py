import torch
from diffusers import AnimateDiffPipeline, MotionAdapter
import moviepy as mpy
import time
import numpy as np  # required for np.array conversion

def generate_video(prompt: str):
    print("Loading AnimateDiff pipeline...")

    motion_adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")

    pipe = AnimateDiffPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        motion_adapter=motion_adapter,
        torch_dtype=torch.float32,
    ).to("cpu")

    print(f"Generating video for prompt: {prompt}")

    result = pipe(
        prompt,
        num_inference_steps=5,
        num_frames=10,
        fps=8,
        decode_chunk_size=1,
        height=256,
        width=256,
    )

    video_tensor = result.get("videos", None) or result.get("frames", None)
    if video_tensor is None:
        raise ValueError("No video frames returned by pipeline.")
    video_tensor = video_tensor[0]

    print("Saving video...")

    # Final fix: if frames are PIL images, convert to numpy directly
    if isinstance(video_tensor[0], torch.Tensor):
        video_np = [(frame * 255).permute(1, 2, 0).cpu().numpy().astype("uint8") for frame in video_tensor]
    else:
        video_np = [np.array(frame) for frame in video_tensor]

    clip = mpy.ImageSequenceClip(video_np, fps=8)

    output_path = f"video_{int(time.time())}.mp4"
    clip.write_videofile(output_path, codec="libx264")

    print(f"✅ Video saved to {output_path}")

if __name__ == "__main__":
    start_time = time.time()
    prompt = "A cinematic scene of a robot walking through a neon-lit street in Tokyo"
    generate_video(prompt)
    end_time = time.time()
    print(f"✅ Done in {end_time - start_time:.2f} seconds")



