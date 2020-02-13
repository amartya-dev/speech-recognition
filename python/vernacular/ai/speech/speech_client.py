from vernacular.ai.speech.proto import speech_to_text_pb2 as sppt_pb
from vernacular.ai.speech.proto import speech_to_text_pb2_grpc as sppt_grpc_pb
import grpc


class SpeechClient(object):
    """
    Class that implements Vernacular.ai ASR API
    """

    # STTP_GRPC_HOST = "speechapis.vernacular.ai"
    STTP_GRPC_HOST = "localhost:5021"

    def __init__(self, access_token):
        """Constructor.
        Args:
            access_token: The authorization token to send with the requests.
        """
        self.channel = grpc.insecure_channel(self.STTP_GRPC_HOST)
        self.client = sppt_grpc_pb.SpeechToTextStub(self.channel)
    
    def recognize(self, config, audio, timeout=None):
        """
        Performs synchronous speech recognition: receive results after all audio
        has been sent and processed.
        Example:
            >>> from vernacular.ai import speech
            >>> from vernacular.ai.speech import enums
            >>>
            >>> client = speech.SpeechClient()
            >>>
            >>> encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
            >>> sample_rate_hertz = 16000
            >>> language_code = 'en-IN'
            >>> config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}
            >>> content = open('path/to/audio/file.wav', 'rb').read()
            >>> audio = {'content': content}
            >>>
            >>> response = client.recognize(config, audio)
        Args:
            config (Union[dict, ~vernacular.ai.speech.types.RecognitionConfig]): Required. Provides information to the recognizer that specifies how to
                process the request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~vernacular.ai.speech.types.RecognitionConfig`
            audio (Union[dict, ~vernacular.ai.speech.types.RecognitionAudio]): Required. The audio data to be recognized.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~vernacular.ai.speech.types.RecognitionAudio`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
        Returns:
            A :class:`~vernacular.ai.speech.types.RecognizeResponse` instance.
        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = sppt_pb.RecognizeRequest(
            config=config, audio=audio
        )
        results = self.client.Recognize(request)
        return results
    