#!/usr/bin/env python


def main():
    # import src.application as app
    import src.udp_echo as udp
    udp.main()


def clear_log():
    import logging
    import os
    import tensorflow as tf

    logger = logging.getLogger('chardet')
    logger.setLevel(logging.CRITICAL)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)


if __name__ == '__main__':
    print('AI is awakening now...')
    print('Provided Feature : 날씨, 뉴스, 달력, 맛집, 미세먼지, 명언, 번역, 시간, 위키, 음악, 이슈, 인물', end='\n\n')
    clear_log()
    main()
