"""경로 설정.

REPO : 저장소 폴더(번역·도구·문서)
BASE : 원본 ISO·글꼴·작업 폴더(work/)·결과 ISO가 있는 폴더.
       환경변수 JAKX_BASE 로 지정하거나, 없으면 저장소 폴더 → 그 상위 폴더 순서로
       원본 ISO가 있는 곳을 찾는다.
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISO_NAME = 'Jak X - Combat Racing (USA) (En,Fr,De,Es,It,Pt,Ru) (v2.00).iso'
OUT_NAME = 'Jak X - Combat Racing (USA) (Korean).iso'

def _base():
    env = os.environ.get('JAKX_BASE')
    if env:
        return os.path.abspath(env)
    for cand in (REPO, os.path.dirname(REPO)):
        if os.path.exists(os.path.join(cand, ISO_NAME)):
            return cand
    return os.path.dirname(REPO)

BASE = _base()
ISO = os.environ.get('JAKX_ISO', os.path.join(BASE, ISO_NAME))
OUT = os.environ.get('JAKX_OUT', os.path.join(BASE, OUT_NAME))
WORK = os.path.join(BASE, 'work')
ORIG = os.path.join(WORK, 'orig')
TR = os.path.join(REPO, 'translation')
FONTS = os.environ.get('JAKX_FONTS', BASE)
FONTFILE = os.path.join(FONTS, 'NanumSquareNeo-eHv.ttf')
EMU = os.environ.get('JAKX_PCSX2', os.path.join(BASE, 'emu', 'pcsx2'))
