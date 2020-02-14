# coding=utf-8
"""
脚本用于语料音量缩放调整
"""
import sox

if __name__ == '__main__':
    wav_path1 = r'C:\Users\Administrator\Desktop\9.wav'
    wav_path2 = r'C:\Users\Administrator\Desktop\8.wav'
    tfm = sox.Transformer()
    tfm.stat()
    # create combiner
    cbn = sox.Combiner()
    # pitch shift combined audio up 3 semitones
    cbn.pitch(3.0)
    # convert output to 8000 Hz stereo
    cbn.convert(samplerate=8000, n_channels=2)
    # create the output file
    cbn.build(
        [wav_path1, wav_path2], 'output.wav', 'concatenate'
    )
