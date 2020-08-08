from vernacular.ai import speech
from vernacular.ai.speech import enums, types
import os


def infer_encoding(file_path: str):
    if ".mp3" in file_path:
        return enums.RecognitionConfig.AudioEncoding.MP3
    elif ".wav" in file_path:
        return enums.RecognitionConfig.AudioEncoding.LINEAR16

    return enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED


def sample_recognize(access_token, file_path):
    speech_client = speech.SpeechClient(access_token)

    with open(file_path, "rb") as file:
        audio_content = file.read()

    config = types.RecognitionConfig(
        encoding=infer_encoding(file_path),
        sample_rate_hertz=8000,
        language_code = "en-IN",
        max_alternatives = 1,
    )
    stream_config = types.StreamingRecognitionConfig(
        config=config,
    )

    requests = [stream_config]

    for i in range(0, len(audio_content), 10000):
        requests.append(
            audio_content[i:i+10000]
        )

    response = speech_client.streaming_recognize(requests)

    """for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        print("Confidence: {}".format(alternative.confidence))"""


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--access_token", type=str, default=os.environ.get("AUTH_ACCESS_TOKEN")
    )
    parser.add_argument(
        "--file_path", type=str, default="../resources/hello.wav"
    )
    args = parser.parse_args()

    sample_recognize(args.access_token, args.file_path)


if __name__ == "__main__":
    main()
