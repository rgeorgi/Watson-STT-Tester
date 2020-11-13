#!/usr/bin/env python3
"""
Script
"""
import argparse

from cvs_ia_tools.recognize import recognize_audio
from cvs_ia_tools.utils import load_config, init_stt

def gather_audio_files():
    """
    Gather audio files to hit the STT instance with.

    :return:
    """


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--config', default='config.ini', type=load_config)
    p.add_argument('-i', '--input', required=True, help='Sound input file')

    args = p.parse_args()

    stt = init_stt(args.config)
    print(recognize_audio(stt, args.input))

