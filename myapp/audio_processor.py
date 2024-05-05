import os
import glob
import numpy as np
from scipy.spatial.distance import cdist
from pyannote.audio import Model, Inference
import torch


def process_audio(single_audio_path, folder_paths):
    # print("Processing single audio path:", single_audio_path)
    # print("Processing folder paths:", folder_paths)

    access_token = "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"
    model = Model.from_pretrained("pyannote/embedding", use_auth_token=access_token)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inference = Inference(model, window="whole", device=device)
    embedding_single = inference(single_audio_path)
    embedding_single = embedding_single[np.newaxis, :]
    threshold = 0.5
    results = []

    for audio_path in folder_paths:
        try:
            embedding_other = inference(audio_path)
            embedding_other = embedding_other[np.newaxis, :]
            distance = cdist(embedding_single, embedding_other, metric="cosine")[0, 0]
            if distance < threshold:
                result = f"Audio {os.path.basename(single_audio_path)} is similar to {os.path.basename(audio_path)}: {distance}"
                results.append(result)
        except RuntimeError as e:
            error_msg = f"Skipping {os.path.basename(audio_path)} due to error: {e}"
            results.append(error_msg)

    return results
