import io
from typing import Tuple, List

from ibm_cloud_sdk_core import DetailedResponse
from ibm_watson import SpeechToTextV1

class RecognitionError(Exception): pass

def _parse_recognition_response(response: DetailedResponse) -> List[Tuple[str, float]]:
    """
    Return the transcription result
    """
    if response.status_code != 200:
        raise RecognitionError("There was an error in the recognition service")
    alt_dicts = response.get_result().get('results', [])

    transcripts = [(alt.get('transcript'),
                    alt.get('confidence')) for alt_dict in alt_dicts
                   for alt in alt_dict.get('alternatives')]
    return transcripts


def recognize_audio(stt: SpeechToTextV1,
                    audio_path: str) -> List[Tuple[str, float]]:
    """
    Return a list of (transcript, confidence) tuples.

    :param stt:
    :param audio_path:
    :return:
    """
    with open(audio_path, 'rb') as aud_f:
        audio_data = io.BytesIO(aud_f.read())

    resp = stt.recognize(audio_data)
    return _parse_recognition_response(resp)
