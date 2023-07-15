import os
import librosa
import numpy as np
from sklearn.svm import SVC

import whisper

model_whisper = whisper.load_model("small")


# ルートディレクトリ
ROOT_PATH = 'SpeakerIdentification/'
WORK_PATH = ROOT_PATH + 'input_split/'
RESULT_FILE = 'Speaker.txt'

# 話者の名前（各話者のデータのディレクトリ名になっている）
speakers = ['ishida', 'hikaru', 'ID02', 'ID03', 'OTHER']

# MFCCを求める関数
def getMfcc(filename):
    y, sr = librosa.load(filename)
    return librosa.feature.mfcc(y=y, sr=sr)

# 話者識別モデルの学習
def trainSpeakerIdentificationModel():
    word_training = []
    speaker_training = []

    for speaker in speakers:
        path = os.path.join(ROOT_PATH + speaker)
        for pathname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.wav'):
                    mfcc = getMfcc(os.path.join(pathname, filename))
                    word_training.append(mfcc.T)
                    label = np.full((mfcc.shape[1],), speakers.index(speaker), dtype=np.int)
                    speaker_training.append(label)

    word_training = np.concatenate(word_training)
    speaker_training = np.concatenate(speaker_training)

    clf = SVC(C=1, gamma=1e-4)
    clf.fit(word_training, speaker_training)
    print('Speaker identification model trained.')
    return clf

# 音声ファイルの識別とテキスト認識
def processAudioFiles():
    clf = trainSpeakerIdentificationModel()
    files = os.listdir(WORK_PATH)

    for filename in files:
            if filename.endswith('.wav'):
                filepath = os.path.join(WORK_PATH, filename)
                mfcc = getMfcc(filepath)
                prediction = clf.predict(mfcc.T)
                result = speakers[np.argmax(np.bincount(prediction))]
                print('Speaker:', result)

                

                # 音声認識
                
                print(filepath)
                result_whisper = model_whisper.transcribe(filepath, verbose=True)
                print(result_whisper["text"])

                # 結果をファイルに追記
                with open(RESULT_FILE, 'a') as f:
                    f.write('Speaker: ' + result + '\n')
                    f.write('Text: ' + result_whisper["text"] + '\n')



processAudioFiles()
