# coding=utf-8
"""
脚本用于语料音量缩放调整， sox测试
"""
import sox


def adjust_voice(transformer, wav_path, dst_path):
    v_adjustment = float(transformer.stat(wav_path).get('Volume adjustment')) or 1.0
    print(v_adjustment)
    transformer.vol(v_adjustment)
    transformer.build(wav_path, dst_path)
    transformer.clear_effects()


if __name__ == '__main__':
    # 放大音量
    wav_path1 = r'C:\Users\Administrator\Desktop\9.wav'
    wav_path2 = r'C:\Users\Administrator\Desktop\8.wav'
    tfm = sox.Transformer()
    adjust_voice(tfm, wav_path1, 'output1.wav')
    adjust_voice(tfm, wav_path2, 'output2.wav')
    # # create combiner
    # cbn = sox.Combiner()
    # # pitch shift combined audio up 3 semitones
    # cbn.pitch(3.0)
    # # convert output to 8000 Hz stereo
    # cbn.convert(samplerate=8000, n_channels=2)
    # # create the output file
    # cbn.build(
    #     [wav_path1, wav_path2], 'output.wav', 'concatenate'
    # )
