from distutils.core import setup

setup(
    name="Watson Speech to Text Tester",
    version='0.1',
    packages=[
        'watson_stt_tester'
    ],
    install_requires=[
        'ibm-watson>=4.7.1',
        'ibm_cloud_sdk_core',
        'pandas',
        'jiwer'
    ]
)