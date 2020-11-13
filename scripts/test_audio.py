import argparse
import os
from typing import List, Tuple, Generator

from watson_stt_tester.recognize import recognize_audio
from watson_stt_tester.utils import load_config, init_stt

from ibm_watson import SpeechToTextV1

import pandas
import configparser

import jiwer

def gather_audio_files():
    """
    Gather audio files to hit the STT instance with.

    :return:
    """

def _str_clean(input_string: str) -> str:
    """
    Use jiwer's
    """
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.SentencesToListOfWords(word_delimiter=" ")
    ])
    return transformation(input_string)

def _gather_sound_files(sound_dir: str,
                        recursive: bool = True) -> Generator[Tuple[str, str], None, None]:
    """
    Search the provided directory for pairs of sound files accompanied
    by '.txt' files providing the transcripts of those files.
    """
    for dirpath, dirnames, filenames in os.walk(sound_dir):

        # Only scan first level if recursive == False
        if not recursive and dirpath != sound_dir:
            break

        # Look for all .mp3 or .wav files accompanied by
        # a .txt file.
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            base, ext = os.path.splitext(fullpath)
            txt_path = f'{base}.txt'

            if ext in ['.wav', '.mp3'] and os.path.exists(txt_path):
                with open(txt_path, 'r') as txt_f:
                    txt = txt_f.read().strip()
                yield (fullpath, txt)


def test_files(sound_dir: str,
               stt: SpeechToTextV1):
    """

    :param csv_path:
    :param stt:
    :return:
    """
    gold_sents = []
    hypo_sents = []

    utt_errors = 0
    utt_compares = 0

    for recording_path, gold_transcript in _gather_sound_files(sound_dir):

        recognized_transcript = recognize_audio(stt, recording_path)[0][0].strip()

        gold_sents.append(gold_transcript)
        hypo_sents.append(recognized_transcript)

        if _str_clean(gold_transcript) != _str_clean(recognized_transcript):
            utt_errors += 1
        utt_compares += 1

    wer = jiwer.wer(gold_sents,
                    hypo_sents,
                    hypothesis_transform=_str_clean,
                    truth_transform=_str_clean)

    print(f'WER: {wer}\nSER: {utt_errors/utt_compares}')



if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--config', default='config.ini', type=load_config)

    args = p.parse_args()

    test_path = args.config[configparser.DEFAULTSECT].get('sound_dir')
    stt = init_stt(args.config)

    test_files(test_path, stt)

