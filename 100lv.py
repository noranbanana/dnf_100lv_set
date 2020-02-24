# -*- coding: utf-8 -*-
import requests
from urllib import parse
import json
import time
import os
import datetime
import itertools
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
import tkinter.ttk
import copy

set_list = {'천상의 무희 세트': {'setItemId': '72b9d0625ac8f77c16e4fb3a329235a5', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '3872c16434aed8e7bbb010280ede0850', 'itemName': '낭만적인 선율의 왈츠', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'b4545fc902750d51102a091319bbfc83', 'itemName': '우아한 선율의 왈츠', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '386d0e43da5233fab6028804a34f2932', 'itemName': '격렬한 스텝의 자이브', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '0be4773fe978dbdd803d06e4bc2d9776', 'itemName': '즉흥적인 감각의 탱고', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'f4c81d9caef284d06ff9ea02ccb1b044', 'itemName': '매혹적인 리듬의 룸바', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '998592e472485393d29420e7a739f029', 'itemName': '정열적인 흐름의 삼바', 'itemRarity': '에픽'}]}, '고대 제사장의 신성한 의식 세트': {'setItemId': '266097499b3bdfd1b2427649856f9b42', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '081d9219035a3fe5912c4e3735508142', 'itemName': '대제사장의 예복', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '34797b92fcbc66fcb86d490934ae1303', 'itemName': '고대 제사장의 로브', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '7fd3263d52d0e24576d981ebdc47add1', 'itemName': '고대 제사장의 치마', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': 'c5c83d9c4b552d6208245cefc58cd67e', 'itemName': '고대 제사장의 견대', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': 'a62e4f4e87bc0fc5b6a02e5d0822285c', 'itemName': '고대 제사장의 띠', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '8e69862ea23bbb7c99b4692973e19b10', 'itemName': '고대 제사장의 샌들', 'itemRarity': '에픽'}]}, '잊혀진 마법사의 유산 세트': {'setItemId': 'a91423120c0d260dad4b879165d5c234', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'a114f11a376f8def22de8cd8d4397f7c', 'itemName': '대 마법사 [???]의 로브', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '9354e9b70817f5315f0d42501b463f60', 'itemName': '마법사 [???]의 로브', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': 'e3fa3afc77a4da47f3dcf871a4c6464d', 'itemName': '마법사 [???]의 부츠', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '2dd9acb683a62d1443ef92ccb1a99c34', 'itemName': '마법사 [???]의 망토', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'bd6e6a67fbfeb18320bf8093f06cc3c7', 'itemName': '마법사 [???]의 하의', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '8c74c821255d86f66a42e993e77abbd3', 'itemName': '마법사 [???]의 허리띠', 'itemRarity': '에픽'}]}, '죽음을 자아내는 그림자 세트': {'setItemId': '070e8126fc113f9a7a148d3a9ceb3ea0', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '22a5933a2736a711c2bfcad7322a623e', 'itemName': '죽음을 덮치는 그림자 재킷', 'itemRarity': '에픽'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '3d3161f248ef5e6ed2d1eeb9b5446d28', 'itemName': '생사를 다스리는 그림자의 재킷', 'itemRarity': '신화'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '797fa631b20018166886706cb86648f6', 'itemName': '죽음을 덮치는 그림자 부츠', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '10dbd9f4b8f332664c33b76a13305d10', 'itemName': '죽음을 덮치는 그림자 견갑', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'ff7f1b74c167fc8aaeeede3ed2f1c77a', 'itemName': '죽음을 덮치는 그림자 바지', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '83c3c5c3f16c0f10b45d788c60d5f618', 'itemName': '죽음을 덮치는 그림자 벨트', 'itemRarity': '에픽'}]}, '황실 직속 집행자의 선고 세트': {'setItemId': 'a9ea5e000a2942e188126d02be966b84', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'f496b895505ea6302d990a9869530103', 'itemName': '수석 집행관의 코트', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '78026473046b75847c008c2faa740cb9', 'itemName': '고귀한 집행자의 제복 자켓', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '2f6fe603453f4066b1c24e9a54bd2f7d', 'itemName': '고귀한 집행자의 제복 바지', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '75e5260fda66742c0f05fb41ffa03d68', 'itemName': '고귀한 집행자의 제복 견장', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '7e693cdea438a54291f5cf494b5f09fd', 'itemName': '고귀한 집행자의 가죽 벨트', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': 'f0e4e08cd5e895c74ec1906a4dc236cb', 'itemName': '고귀한 집행자의 구두', 'itemRarity': '에픽'}]}, '베테랑 군인의 정복 세트': {'setItemId': 'c5947b6928696a5bf182c6acf348ca28', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'c40d2977d03a7656fe858579c2530a04', 'itemName': '최후의 전술', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'ea7619426683f2edbcc6b2651d438d79', 'itemName': '전장의 매', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '786acb2ca6431f1fbd29ce33c0f7843f', 'itemName': '데파르망', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '7e1ede6e49d2715c67bc4a5a8b96e15f', 'itemName': '퀘이크 프론', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '63e54c65377fd7b2c660a726e9e3ab80', 'itemName': '오퍼레이션 델타', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '2d8ef3cf0c87e8a2bed6ed59848cb2e3', 'itemName': '전쟁의 시작', 'itemRarity': '에픽'}]}, '메마른 사막의 유산 세트': {'setItemId': '3fddf4524b6aa73652e0cdfbc2306137', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'efed1b3100d2abda90b26119acba1b84', 'itemName': '타오르는 열기의 용기', 'itemRarity': '에픽'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'ec3983c86e084fd38f7551153450dfbf', 'itemName': '작열하는 대지의 용맹', 'itemRarity': '신화'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '892598da1a3ae04c12702c189fb5baec', 'itemName': '얼어붙는 밤의 인내', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '991913dfae244337b3ff06cabfef0eee', 'itemName': '바라는 삶의 투지', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'ae42ac7d0cb2aad8b83bf58bcb499b56', 'itemName': '몰아치는 바람의 의지', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': 'ee80dc4be059e87c19732be146aa957d', 'itemName': '수호하는 전사의 고난', 'itemRarity': '에픽'}]}, '열대의 트로피카 세트': {'setItemId': '504960c246d867f262a4bdfb174d9ecb', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'a4610bc3ab02d64af5f38b7d7dd45e0b', 'itemName': '트로피카 : 드레이크', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '3761008a46d01e9d6dbd5d77b6c3e165', 'itemName': '트로피카 : 용과', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': 'db5f7f878090c2bc0de7fa91a32ec104', 'itemName': '트로피카 : 파파야', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': 'fa24d6a3e1261dd29216bc9dd9107098', 'itemName': '트로피카 : 두리안', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'e33a7a9aebdf187907d0a0977cb87b23', 'itemName': '트로피카 : 리치', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '13309a3bc5672bb4f540da64ef795079', 'itemName': '트로피카 : 망고스틴', 'itemRarity': '에픽'}]}, 'A.D. P 슈트 세트': {'setItemId': '3a441737656962d57d3f506bc3ed68e0', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '2f5acdd7a1496c8f96e29293280962ed', 'itemName': '웨어러블 아크 팩', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'a57ee196541e0db113f6f3e48caa739b', 'itemName': '웨어러블 파워 슈트', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '15060608692b95e2b335c54762cd67be', 'itemName': '인듀어런스 파워 레그', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '125230e058bbe65ad25b10ff0a6f071d', 'itemName': '에큐레이트 파워 숄더', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': 'a634272704be22125066dfb6930e15fd', 'itemName': '모빌리티 파워 벨트', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': 'a611f2774742a8b1a2a213aaaf066f0f', 'itemName': '벨로시티 파워 부츠', 'itemRarity': '에픽'}]}, '개악 : 지옥의 길 세트': {'setItemId': '3c5b33d2817bfeb33fb9d64a84a64ef8', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'e6c950d0d494055b207c1eed7593b51e', 'itemName': '사탄 : 분노의 군주', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '0e935269970e86d144bdaf0389aadcd4', 'itemName': '사탄 : 들끓는 분노', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '21bd802c865a732105c1883c4c6988aa', 'itemName': '바알 : 영혼의 타락', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '06f0de644f29119cb7aec3b216326dad', 'itemName': '벨리알 : 멸망의 씨앗', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'ef296147598c75779f1153669ac36edc', 'itemName': '아몬 : 거짓된 힘', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': 'b225e8ce16097be6a82952b565ca7672', 'itemName': '아바돈 : 절망의 나락', 'itemRarity': '에픽'}]}, '전설의 대장장이 - 역작 세트': {'setItemId': '00d09213980eb1bb66389ad61576703b', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '3c894436df9672f92477f3de78ae9cbc', 'itemName': '천상의 날개', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'bb68345a23460443a05f3761f903a52d', 'itemName': '페어리의 몸짓', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'ec31fa66cb12e360def2a4513126d6d2', 'itemName': '사악한 형상의 뿔', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '392d70ee822c5637f8ecb9e0d423dd49', 'itemName': '무한한 마나의 심장', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '5f700cfedb4c3002177839a3bf127692', 'itemName': '강철을 뜯는 이빨', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': 'e15183e68084333b390b5eb616cc0699', 'itemName': '융합된 자연의 핵', 'itemRarity': '에픽'}]}, '구속의 가시덩굴 세트': {'setItemId': '8cf8910dcbabacf11907f98db19de767', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'e4df5f151f39112fbf6b9d816c642f2f', 'itemName': '결속의 체인 플레이트', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'b8bb021cdee7340946495f2e7c9a4126', 'itemName': '구속의 체인 메일', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '553f31379c7f665d97e60e629a13bd86', 'itemName': '구속의 체인 그리브', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '8c07fa07397d14e513a80fb154f1f633', 'itemName': '구속의 폴드런', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '12074c5cadd3387f79def00bdfb7404c', 'itemName': '구속의 퀴스', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '5db568449d3e2cfaed39832080e7528d', 'itemName': '구속의 체인 벨트', 'itemRarity': '에픽'}]}, '대자연의 숨결 세트': {'setItemId': 'f1076d938f10a593c757c377bc84af03', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'baf124579507400a603b2a4c746482b5', 'itemName': '원시 태동의 대지', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '2ba3e0c8bb4662c3a383b841a0aae316', 'itemName': '포용의 굳건한 대지', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '831fef9bc88638e7df5575883ed32a82', 'itemName': '휘감는 햇살의 바람', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '8e1379998738521c445da694877fc88b', 'itemName': '맹렬히 타오르는 화염', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'beda39d809a0df2a6e314481590180e3', 'itemName': '잠식된 신록의 숨결', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '97fdbc3d22c2b983a3a69ccfc9edc2bb', 'itemName': '잔잔한 청록의 물결', 'itemRarity': '에픽'}]}, '선택의 기로 세트': {'setItemId': '861e52afdbbcbcc015188a5d77f30dc1', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'b281ed888094e708d5cbf30f71a34c74', 'itemName': '선택이익', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'ccc01f949b9be7732ebf90401e9d6dd4', 'itemName': '무의식적 선택', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '0074f1dee0de62f1ea4bbe183a23d049', 'itemName': '임의 선택', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '4677045206fb6ccd0ba55fc2eac65241', 'itemName': '선택의 역설', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': 'ec5ce2a1f589de2f91640253e72aea41', 'itemName': '합리적 선택', 'itemRarity': '에픽'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '8a712d558498c23a9aa1ea0517391f32', 'itemName': '탈리스만 선택', 'itemRarity': '에픽'}]}, '영원한 흐름의 길 세트': {'setItemId': 'd69db0f43a2c9250ee020e5cd38a18f6', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '79a0fda77889debf6d6f5ce2274f2c7f', 'itemName': '지체없는 흐름의 한뉘', 'itemRarity': '에픽'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '882e8164dd6711c1895526d030200250', 'itemName': '영명한 세상의 순환', 'itemRarity': '신화'}, {'slotId': 'SHOES', 'slotName': '신발', 'itemId': '62d62b7531e09610bee17e45df2f74c9', 'itemName': '지체없는 흐름의 미리내', 'itemRarity': '에픽'}, {'slotId': 'SHOULDER', 'slotName': '머리어깨', 'itemId': '91ae40407418fe3682d39d8f3034fedb', 'itemName': '지체없는 흐름의 마루', 'itemRarity': '에픽'}, {'slotId': 'PANTS', 'slotName': '하의', 'itemId': '38fd6a778be23237a414d5115062252a', 'itemName': '지체없는 흐름의 가람', 'itemRarity': '에픽'}, {'slotId': 'WAIST', 'slotName': '허리', 'itemId': '349af6128d7d88fc5d1356aca5bbf2e8', 'itemName': '지체없는 흐름의 바람', 'itemRarity': '에픽'}]}, '심연을 엿보는 자 세트': {'setItemId': 'd675cb6e153e02388e2e0a7ab188acde', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '0b5668da99c6dd6207887f336e523e71', 'itemName': '고대 심연의 로브', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '81a49b255427241e432b4f8bc8e79430', 'itemName': '심연에 빠진 검은 셔츠', 'itemRarity': '에픽'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': 'faac667b094734568db66d4c0af663f4', 'itemName': '타락한 세계수의 생명', 'itemRarity': '에픽'}, {'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': 'cd5895092f186bc87dbb8b540271c9d3', 'itemName': '암흑술사가 직접 저술한 고서', 'itemRarity': '에픽'}]}, '황혼의 여행자 세트': {'setItemId': 'b5bb71953bc709c84137b0cad5d14e4e', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '4e28aa6397e262a21b385e4e17eb0863', 'itemName': '길 방랑자의 물소 코트', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': 'bc7c4e3a0050ef4aea85988a83642634', 'itemName': '길 안내자의 물소 코트', 'itemRarity': '에픽'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': '89a0e7652c40aaacb3f13c810097dd9e', 'itemName': '길 안내자의 계절', 'itemRarity': '에픽'}, {'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': 'c4c2cf7f1ee32babea0679124c4b654c', 'itemName': '길 안내자의 여행서', 'itemRarity': '에픽'}]}, '삼켜진 분노 세트': {'setItemId': 'ae4e5f8c339b667f2af12db2505f6ece', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '8f833c773b16a1236d31a0c6a3f09cff', 'itemName': '세상을 삼키는 분노', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '2f15190f0615de75cf4cdae922e70bc9', 'itemName': '피를 머금은 한', 'itemRarity': '에픽'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': '880219804acccc7d1deff35843742c31', 'itemName': '과격한 분노의 격앙', 'itemRarity': '에픽'}, {'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': 'd5aa285ea041ca244da5c0d6103ac8f8', 'itemName': '통제할 수 없는 화', 'itemRarity': '에픽'}]}, '기구한 운명 세트': {'setItemId': '33348fff4c17d204c4655ee50e2c6bdc', 'setItems': [{'slotId': 'JACKET', 'slotName': '상의', 'itemId': '26cd8c6f3296bb4335604c1ea02582cd', 'itemName': '종말의 역전', 'itemRarity': '신화'}, {'slotId': 'JACKET', 'slotName': '상의', 'itemId': '8510a6b8ef21003c625d1ef0931e8a40', 'itemName': '나락의 끝자락', 'itemRarity': '에픽'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': 'da5e4132290136b6bae3d1d8e2692446', 'itemName': '비통한 자의 목걸이', 'itemRarity': '에픽'}, {'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': '33727ea5e4d52bf641bd15ba2556bc75', 'itemName': '비운의 유물', 'itemRarity': '에픽'}]}, '흑마술의 탐구자 세트': {'setItemId': '1d4ed1e13b380593c889feef9ec2f62d', 'setItems': [{'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'd56008e8c9fc2208dc933e4735200cdc', 'itemName': '어둠을 파헤치는 바지', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '96f8258abe5a61b45cd95aeb75e7296b', 'itemName': '영원히 끝나지 않는 탐구', 'itemRarity': '신화'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': 'b5f385f622665794605cd7fa94a67bb9', 'itemName': '지독한 집념의 탐구', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': '44becbbee44c861cdf8df571d4fd2aed', 'itemName': '암흑술사의 정수', 'itemRarity': '에픽'}]}, '시간의 여행자 세트': {'setItemId': '2faa0b8988b5baa7216f0330b2a9e1ae', 'setItems': [{'slotId': 'PANTS', 'slotName': '하의', 'itemId': 'bf0bcb8aa7ae39381730dab959f73bfc', 'itemName': '시간에 휩쓸린 물소 각반', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '2663b5e40549791e69a2a8a024943efb', 'itemName': '시간을 거스르는 자침', 'itemRarity': '신화'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '19f152ef5b53761c5ac058d735e9aace', 'itemName': '시간을 가리키는 지침', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': '74a1e80dc0d3302523f0ead3824f6fa0', 'itemName': '시간에 갇혀버린 모래', 'itemRarity': '에픽'}]}, '운명을 가르는 함성 세트': {'setItemId': '5bc36d6fb20ea5007422608f9a18e586', 'setItems': [{'slotId': 'PANTS', 'slotName': '하의', 'itemId': '2e08623069832fc50c9dcfad3a7476c6', 'itemName': '본능적인 외침', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': 'dd8fb29cc2d99113e208efc67474b52e', 'itemName': '천지에 울려퍼지는 포효', 'itemRarity': '신화'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '4ec68a286d263752266de671d1a5ec4a', 'itemName': '전장을 지배하는 함성', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': '4b897931e2f8da03285e51849f0164d1', 'itemName': '적막이 흐르는 아우성', 'itemRarity': '에픽'}]}, '광란의 추종자 세트': {'setItemId': '4409ac3fd335adeea84fe227fcbe0fa9', 'setItems': [{'slotId': 'PANTS', 'slotName': '하의', 'itemId': '4f9b33ab2503c2625772b22fb3cbac7b', 'itemName': '따르는 광기의 기운', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '2b0d249f743023bebc653fd5b7bcac8e', 'itemName': '광란을 품은 자', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '486f00eae262f4afc4a47d8187e368c2', 'itemName': '숙명을 뒤엎는 광란', 'itemRarity': '신화'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': '147e35acab785cc70a363286d38689c0', 'itemName': '폭주하는 광란의 힘', 'itemRarity': '에픽'}]}, '나락의 구도자 세트': {'setItemId': 'f51b430435a8383b3cf6d34407c4a553', 'setItems': [{'slotId': 'SHOES', 'slotName': '신발', 'itemId': '8147eaaaac72c2d533421dc5460dbf11', 'itemName': '나락으로 빠진 발', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': 'b89ed6af0153823f530f9a07e4225d46', 'itemName': '어둠을 지배하는 고리', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'dca766f2875f2ca7df989f32394679c1', 'itemName': '영원한 나락의 다크버스', 'itemRarity': '신화'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '825c40401d213613835587dc8f721376', 'itemName': '끝없는 나락의 다크버스', 'itemRarity': '에픽'}]}, '차원의 여행자 세트': {'setItemId': 'bcd72f6c009738cb256b13403fc84b8c', 'setItems': [{'slotId': 'SHOES', 'slotName': '신발', 'itemId': '34ee102e1e23475196f6947c79b2739e', 'itemName': '차원을 걷는 물소 부츠', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': 'e79a8bcf880c6467f10b4f3530f64f4a', 'itemName': '차원을 지나는 자의 인장', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '5d1784fa174f6ccd6bc21a0f85a8d74a', 'itemName': '차원을 관통하는 초신성', 'itemRarity': '신화'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'ecfc048f1bcb1b9aa4156126cd1a3448', 'itemName': '차원을 맴도는 혜성', 'itemRarity': '에픽'}]}, '운명의 주사위 세트': {'setItemId': '5742ec75674086d001067005f43f0da4', 'setItems': [{'slotId': 'SHOES', 'slotName': '신발', 'itemId': '88a33fb3d366f187e85e43a381275952', 'itemName': '희비교차', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': '631feec15f8c5c24ea2357d4f1207678', 'itemName': '운명의 장난', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '88186ce9a9fc02dfb274f225acd406b4', 'itemName': '운명을 거스르는 자', 'itemRarity': '신화'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '1c93cac5af6dbd1212e646f87c558ed3', 'itemName': '운명을 마주하는 자', 'itemRarity': '에픽'}]}, '아린 비극의 잔해 세트': {'setItemId': 'bf7f99836f89770380231245c6048dfe', 'setItems': [{'slotId': 'SHOES', 'slotName': '신발', 'itemId': 'f658400818fa831bf451e4ef2dbc55f4', 'itemName': '무너진 세상의 슬픔', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': '4a64c839121cc75e1fe33dbcc2aa3351', 'itemName': '광란을 품은 자의 종막', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '830fc9494e0d30f05c49355b272d03de', 'itemName': '슬픔을 담은 운명', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'c549adc567f46e47f536a1e26e7f9d0b', 'itemName': '아린 고통의 비극', 'itemRarity': '신화'}]}, '고대의 술식 세트': {'setItemId': 'f19e9a71b2cd4f077998309cea838b93', 'setItems': [{'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': '777cc0388e21e1fc87355568d309d934', 'itemName': '케나즈 : 정신을 밝히는 불', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': '301bd15b827ffe3ab72a6181d33f21ae', 'itemName': '게보 : 완벽한 균형', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '83a90f63e8753b409ea7059d35099816', 'itemName': '라이도 : 이동의 규율', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '677f0a5c7d742933ddff42b935377705', 'itemName': '라이도 : 질서의 창조자', 'itemRarity': '신화'}]}, '먼동 틀 무렵 세트': {'setItemId': '2d228dcdcab18d2ab425dae8a2781df9', 'setItems': [{'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': 'f765a2c6d5a352eea26c930b4ac002dc', 'itemName': '새벽을 녹이는 따스함', 'itemRarity': '신화'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': 'd6f33782f34039670394faf46429bc12', 'itemName': '달빛을 가두는 여명', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': '836c39afd1d4c97c0c0e08a4516e58f7', 'itemName': '고요를 머금은 이슬', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '3adaa72c296d7c05b63111d2183d25be', 'itemName': '새벽을 감싸는 따스함', 'itemRarity': '에픽'}]}, '행운의 트라이앵글 세트': {'setItemId': '9b2a1398222c5ead60edc99cf959338a', 'setItems': [{'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '488b6c2c54f029ff2fd88d875c0bf2e8', 'itemName': '가네샤의 영원한 가호', 'itemRarity': '신화'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '6466876944e1fdef5098d13f8d65f0d1', 'itemName': '하얀 코끼리의 가호', 'itemRarity': '에픽'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': 'c54888203ba8125d7d1079df893041c2', 'itemName': '네잎 클로버의 초심', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': 'ba6884c830f3ee2865e21a688c6f21ec', 'itemName': '붉은 토끼의 축복', 'itemRarity': '에픽'}]}, '정령사의 장신구 세트': {'setItemId': 'f999962c227725c02d4b8626f46f58c7', 'setItems': [{'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '2478dbd8b9d68e651df67bc9a1f3c8fa', 'itemName': '지고의 화염 - 이프리트', 'itemRarity': '신화'}, {'slotId': 'AMULET', 'slotName': '목걸이', 'itemId': '13d4c8409741f7cb4b273640969ae237', 'itemName': '냉염의 빙설 - 운디네', 'itemRarity': '에픽'}, {'slotId': 'RING', 'slotName': '반지', 'itemId': '339a2c347e8c4c69bb6a77f4e0d968b8', 'itemName': '축복의 바람 - 실프', 'itemRarity': '에픽'}, {'slotId': 'WRIST', 'slotName': '팔찌', 'itemId': '476fde8df4c575bb07ed65dfa8e354c8', 'itemName': '화마의 불꽃 - 샐러맨더', 'itemRarity': '에픽'}]}, '군신의 숨겨진 유산 세트': {'setItemId': '0d7fa7e5f82d8ec524d1b8202b31497f', 'setItems': [{'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': 'd1a84411f3f90550dd898ce9747b1056', 'itemName': '군신의 유언장', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': 'aa441e3ae68e73d464f10f6e11e89098', 'itemName': '군신의 가호가 담긴 보석', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'e98db581d86ffc2098c66049b019cf83', 'itemName': '군신의 마지막 갈망', 'itemRarity': '신화'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'e8339821b962569895a1dcd569ef1ed8', 'itemName': '군신의 수상한 귀걸이', 'itemRarity': '에픽'}]}, '시간전쟁의 잔해 세트': {'setItemId': '0cd4fb46aa92d65d242ca44d34a3f27a', 'setItems': [{'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '28532be7516724b79a6825aaf0a03235', 'itemName': '또다른 시간의 흐름', 'itemRarity': '신화'}, {'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': '8d962518bb1a88346c95f3cf061e8a97', 'itemName': '종말의 시간', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': '00fc487d65673903cabda8b21a2ceb38', 'itemName': '시간의 소용돌이', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'dca32f90a9a9fb049709bdd18622791b', 'itemName': '시간의 모순', 'itemRarity': '에픽'}]}, '노멀라이즈 싱크로 세트': {'setItemId': 'cff2e64e3f4fb0669d77b11743d0cc6b', 'setItems': [{'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': '28c58ddd69572e8407996b1792ee323a', 'itemName': '제어 회로 모듈', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': 'd563a033184eca2823192ead5e8da912', 'itemName': '에너지 분배 제어기', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '237b18584ee0ec4ae16b27acc091e326', 'itemName': '전자기 진공관', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': '297a7f90713900aeb6804f39b4df02ef', 'itemName': '플라즈마 초 진공관', 'itemRarity': '신화'}]}, '영보 : 세상의 진리 세트': {'setItemId': '236b7169ff3612b54fb09f9753c138c1', 'setItems': [{'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'a540a3704f3015701c046575f21950d1', 'itemName': '영원을 새긴 바다', 'itemRarity': '신화'}, {'slotId': 'SUPPORT', 'slotName': '보조장비', 'itemId': '370c0d826b0cee4c22e70cadbe39254e', 'itemName': '뜻을 품은 하늘', 'itemRarity': '에픽'}, {'slotId': 'MAGIC_STON', 'slotName': '마법석', 'itemId': '0a417fc8f0588e579377be78298dbb7d', 'itemName': '지혜를 담은 대지', 'itemRarity': '에픽'}, {'slotId': 'EARRING', 'slotName': '귀걸이', 'itemId': 'd3f1be6b88482b833ff69c3134cffbf1', 'itemName': '마음을 새긴 바다', 'itemRarity': '에픽'}]}}
option_dict = {'고대 제사장의 로브': [0, 0, 0, 0, 12.0, 10, 10, 0, 0.0, 0.0, 0], '대제사장의 예복': [0, 0, 10, 0, 12.0, 21, 20, 0, 0.0, 0.0, 0], '마법사 [???]의 로브': [0, 0, 0, 0, 12.0, 10, 5, 0, 0.0, 4.5, 0], '대 마법사 [???]의 로브': [11, 0, 0, 0, 12.0, 10, 17, 0, 0.0, 9.0, 0], '우아한 선율의 왈츠': [17, 14, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '낭만적인 선율의 왈츠': [25, 14, 0, 0, 10.0, 3, 0, 0, 0.0, 0.0, 24], '심연에 빠진 검은 셔츠': [0, 0, 0, 0, 35.0, 0, 0, 0, 0.0, 0.0, 0], '고대 심연의 로브': [0, 0, 0, 0, 35.0, 7, 0, 0, 0.0, 18.0, 0], '고대 제사장의 견대': [0, 0, 0, 0, 0.0, 10, 10, 0, 12.0, 0.0, 0], '마법사 [???]의 망토': [0, 0, 0, 0, 0.0, 10, 5, 0, 13.0, 0.0, 0], '즉흥적인 감각의 탱고': [0, 0, 17, 0, 0.0, 0, 0, 0, 14.0, 0.0, 0], '고대 제사장의 치마': [12, 0, 0, 0, 0.0, 10, 10, 0, 0.0, 0.0, 0], '마법사 [???]의 하의': [12, 0, 0, 0, 0.0, 10, 5, 0, 0.0, 0.0, 18], '매혹적인 리듬의 룸바': [0, 0, 0, 0, 17.0, 0, 14, 0, 0.0, 0.0, 0], '어둠을 파헤치는 바지': [35, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '고대 제사장의 샌들': [0, 0, 12, 0, 0.0, 10, 10, 0, 0.0, 0.0, 0], '마법사 [???]의 부츠': [0, 16, 0, 0, 0.0, 10, 5, 0, 0.0, 0.0, 0], '격렬한 스텝의 자이브': [0, 0, 14, 0, 0.0, 17, 0, 0, 0.0, 0.0, 0], '나락으로 빠진 발': [0, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 18.0, 70], '고대 제사장의 띠': [0, 12, 0, 0, 0.0, 10, 10, 0, 0.0, 0.0, 0], '마법사 [???]의 허리띠': [0, 0, 14, 0, 0.0, 10, 5, 0, 0.0, 0.0, 0], '정열적인 흐름의 삼바': [0, 0, 0, 0, 14.0, 0, 17, 0, 0.0, 0.0, 0], '길 안내자의 물소 코트': [0, 0, 0, 0, 0.0, 12, 20, 0, 0.0, 0.0, 0], '길 방랑자의 물소 코트': [10, 0, 10, 0, 0.0, 12, 20, 0, 0.0, 0.0, 40], '죽음을 덮치는 그림자 재킷': [18, 10, 0, 0, 0.0, 4, 0, 0, 0.0, 0.0, 0], '생사를 다스리는 그림자의 재킷': [18, 20, 0, 0, 0.0, 4, 10, 0, 0.0, 0.0, 0], '고귀한 집행자의 제복 자켓': [19, 14, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '수석 집행관의 코트': [5, 21, 6, 0, 5.0, 19, 0, 0, 0.0, 0.0, 0], '전장의 매': [0, 0, 0, 0, 0.0, 35, 0, 0, 0.0, 0.0, 0], '최후의 전술': [4, 10, 0, 0, 0.0, 38, 8, 0, 0.0, 0.0, 0], '죽음을 덮치는 그림자 견갑': [0, 18, 0, 0, 0.0, 4, 0, 0, 10.0, 0.0, 0], '고귀한 집행자의 제복 견장': [0, 12, 0, 0, 0.0, 0, 0, 0, 20.0, 0.0, 0], '퀘이크 프론': [0, 0, 0, 0, 0.0, 0, 0, 0, 35.0, 0.0, 0], '시간에 휩쓸린 물소 각반': [0, 0, 0, 0, 32.0, 0, 0, 0, 0.0, 0.0, 0], '죽음을 덮치는 그림자 바지': [18, 10, 0, 0, 0.0, 4, 0, 0, 0.0, 0.0, 0], '고귀한 집행자의 제복 바지': [0, 0, 0, 0, 17.0, 0, 16, 0, 0.0, 0.0, 0], '데파르망': [0, 35, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '차원을 걷는 물소 부츠': [19, 0, 0, 0, 0.0, 10, 0, 0, 0.0, 4.5, 0], '죽음을 덮치는 그림자 부츠': [0, 10, 18, 0, 0.0, 4, 0, 0, 0.0, 0.0, 0], '고귀한 집행자의 구두': [0, 0, 0, 0, 21.0, 0, 11, 0, 0.0, 0.0, 0], '전쟁의 시작': [0, 0, 0, 0, 0.0, 0, 35, 0, 0.0, 0.0, 0], '죽음을 덮치는 그림자 벨트': [0, 10, 18, 0, 0.0, 4, 0, 0, 0.0, 0.0, 0], '고귀한 집행자의 가죽 벨트': [18, 15, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '오퍼레이션 델타': [0, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 18.0, 72], '나락의 끝자락': [0, 0, 0, 0, 0.0, 35, 0, 0, 0.0, 0.0, 0], '종말의 역전': [0, 0, 20, 0, 5.0, -20, 0, 0, 35.0, 2.0454545454545454, 0], '타오르는 열기의 용기': [6, 28, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '작열하는 대지의 용맹': [6, 43, 0, 0, 0.0, 8, 8, 0, 0.0, 0.0, 0], '트로피카 : 용과': [0, 15, 0, 0, 0.0, 0, 16, 0, 0.0, 0.0, 0], '트로피카 : 드레이크': [4, 23, 0, 0, 10.0, 16, 3, 0, 0.0, 0.0, 0], '웨어러블 파워 슈트': [34, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.8181818181818182, 0], '웨어러블 아크 팩': [43, 7, 0, 0, 4.0, 0, 0, 0, 4.0, 0.8181818181818182, 0], '바라는 삶의 투지': [6, 0, 16, 0, 0.0, 0, 0, 0, 10.0, 0.0, 0], '트로피카 : 두리안': [0, 0, 0, 0, 0.0, 0, 0, 0, 33.0, 0.0, 0], '에큐레이트 파워 숄더': [0, 0, 0, 0, 0.0, 0, 0, 0, 34.0, 0.8181818181818182, 0], '본능적인 외침': [0, 0, 17, 0, 0.0, 0, 14, 0, 0.0, 0.0, 0], '몰아치는 바람의 의지': [6, 16, 10, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '트로피카 : 리치': [0, 0, 0, 0, 0.0, 0, 33, 0, 0.0, 0.0, 0], '인듀어런스 파워 레그': [0, 34, 0, 0, 0.0, 0, 0, 0, 0.0, 0.8181818181818182, 0], '희비교차': [0, 0, 0, 0, 0.0, 29, 0, 0, 0.0, 0.0, 20], '얼어붙는 밤의 인내': [6, 0, 0, 0, 0.0, 0, 28, 0, 0.0, 0.0, 0], '트로피카 : 파파야': [30, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '벨로시티 파워 부츠': [0, 0, 0, 0, 34.0, 0, 0, 0, 0.0, 0.8181818181818182, 0], '수호하는 전사의 고난': [6, 0, 10, 0, 0.0, 0, 16, 0, 0.0, 0.0, 0], '트로피카 : 망고스틴': [0, 0, 0, 0, 0.0, 16, 0, 0, 0.0, 0.0, 60], '모빌리티 파워 벨트': [0, 0, 0, 0, 0.0, 0, 34, 0, 0.0, 0.8181818181818182, 0], '피를 머금은 한': [0, 0, 23, 0, 0.0, 0, 0, 10, 0.0, 0.0, 0], '세상을 삼키는 분노': [0, 0, 23, 0, 4.0, 13, 4, 10, 5.0, 0.0, 0], '사탄 : 들끓는 분노': [16, 16, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '사탄 : 분노의 군주': [25, 23, 4, 0, 0.0, 0, 0, 5, 0.0, 0.0, 0], '페어리의 몸짓': [0, 0, 0, 0, 34.0, 0, 0, 0, 0.0, 0.0, 0], '천상의 날개': [0, 0, 9, 0, 38.0, 7, 4, 0, 0.0, 0.0, 0], '구속의 체인 메일': [35, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '결속의 체인 플레이트': [35, 10, 10, 0, 0.0, 10, 0, 0, 0.0, 0.0, 0], '벨리알 : 멸망의 씨앗': [16, 0, 0, 0, 0.0, 0, 0, 0, 16.0, 0.0, 0], '무한한 마나의 심장': [0, 0, 0, 0, 12.0, 0, 0, 0, 20.0, 0.0, 0], '구속의 폴드런': [0, 0, 0, 0, 0.0, 0, 0, 0, 34.0, 0.0, 0], '따르는 광기의 기운': [0, 22, 0, 0, 0.0, 10, 0, 0, 0.0, 0.0, 0], '아몬 : 거짓된 힘': [0, 0, 0, 0, 16.0, 0, 16, 0, 0.0, 0.0, 0], '사악한 형상의 뿔': [0, 0, 34, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '구속의 퀴스': [0, 0, 0, 0, 0.0, 35, 0, 0, 0.0, 0.0, 0], '무너진 세상의 슬픔': [0, 0, 10, 0, 0.0, 0, 17, 0, 0.0, 0.0, 0], '바알 : 영혼의 타락': [16, 0, 0, 0, 0.0, 0, 16, 0, 0.0, 0.0, 0], '융합된 자연의 핵': [0, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 13.0, 70], '구속의 체인 그리브': [0, 0, 0, 0, 35.0, 0, 0, 0, 0.0, 0.0, 0], '아바돈 : 절망의 나락': [0, 16, 0, 0, 0.0, 0, 16, 0, 0.0, 0.0, 0], '강철을 뜯는 이빨': [34, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '구속의 체인 벨트': [0, 0, 0, 0, 0.0, 0, 35, 0, 0.0, 0.0, 0], '지체없는 흐름의 한뉘': [30, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '영명한 세상의 순환': [30, 0, 5, 0, 6.0, 0, 8, 0, 0.0, 2.0454545454545454, 0], '무의식적 선택': [21, 0, 0, 0, 0.0, 11, 0, 0, 0.0, 0.0, 0], '선택이익': [5, 7, 5, 0, 6.0, 11, 21, 0, 0.0, 0.0, 0], '포용의 굳건한 대지': [0, 0, 0, 0, 0.0, 0, 28, 0, 0.0, 0.0, 24], '원시 태동의 대지': [9, 0, 0, 0, 9.0, 0, 40, 0, 0.0, 0.0, 24], '지체없는 흐름의 마루': [0, 0, 0, 0, 0.0, 10, 0, 0, 20.0, 0.0, 0], '선택의 역설': [0, 0, 0, 0, 0.0, 0, 0, 0, 34.0, 0.0, 0], '맹렬히 타오르는 화염': [0, 0, 0, 0, 0.0, 0, 0, 0, 32.0, 0.0, 0], '지체없는 흐름의 가람': [0, 31, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '임의 선택': [7, 7, 7, 0, 7.0, 7, 0, 0, 0.0, 0.0, 0], '잠식된 신록의 숨결': [0, 0, 0, 0, 32.0, 0, 0, 0, 0.0, 0.0, 0], '지체없는 흐름의 미리내': [0, 0, 28, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '탈리스만 선택': [0, 0, 17, 0, 0.0, 0, 0, 0, 7.0, 0.0, 0], '휘감는 햇살의 바람': [0, 32, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '지체없는 흐름의 바람': [0, 0, 0, 0, 0.0, 32, 0, 0, 0.0, 0.0, 0], '합리적 선택': [0, 0, 0, 0, 0.0, 20, 0, 0, 10.0, 0.0, 0], '잔잔한 청록의 물결': [32, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 24], '케나즈 : 정신을 밝히는 불': [0, 0, 12, 0, 0.0, 20, 0, 0, 0.0, 0.0, 25], '달빛을 가두는 여명': [0, 0, 0, 0, 0.0, 6, 14, 0, 0.0, 1.2272727272727273, 28], '네잎 클로버의 초심': [7, 7, 0, 0, 7.0, 7, 7, 0, 0.0, 0.0, 0], '냉염의 빙설 - 운디네': [0, 0, 0, 0, 0.0, 27, 0, 0, 0.0, 0.0, 38], '타락한 세계수의 생명': [0, 0, 0, 0, 0.0, 0, 40, 0, 0.0, 0.0, 0], '길 안내자의 계절': [0, 0, 35, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '비통한 자의 목걸이': [0, 0, 0, 0, 28.0, 10, 0, 0, 0.0, 0.0, 0], '과격한 분노의 격앙': [0, 0, 0, 0, 0.0, 30, 0, 10, 0.0, 0.0, 0], '게보 : 완벽한 균형': [0, 0, 12, 0, 0.0, 0, 20, 0, 0.0, 0.0, 25], '고요를 머금은 이슬': [14, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 1.6363636363636365, 30], '붉은 토끼의 축복': [7, 7, 0, 0, 7.0, 7, 7, 0, 0.0, 0.0, 0], '축복의 바람 - 실프': [0, 0, 0, 0, 27.0, 0, 0, 0, 0.0, 0.0, 38], '어둠을 지배하는 고리': [0, 40, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '차원을 지나는 자의 인장': [0, 0, 0, 0, 0.0, 0, 14, 0, 18.0, 2.0454545454545454, 0], '운명의 장난': [10, 0, 0, 0, 6.0, 0, 0, 0, 19.0, 0.0, 0], '광란을 품은 자의 종막': [0, 27, 10, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '라이도 : 이동의 규율': [0, 0, 12, 0, 0.0, 0, 0, 0, 20.0, 0.0, 25], '라이도 : 질서의 창조자': [0, 9, 12, 0, 0.0, 3, 6, 0, 27.200000000000003, 0.0, 25], '새벽을 감싸는 따스함': [0, 0, 0, 0, 6.0, 0, 0, 0, 14.0, 4.909090909090909, 28], '새벽을 녹이는 따스함': [11, 10, 0, 0, 6.0, 0, 0, 0, 14.0, 4.909090909090909, 28], '하얀 코끼리의 가호': [7, 7, 7, 0, 0.0, 0, 7, 0, 7.0, 0.0, 0], '가네샤의 영원한 가호': [10, 11, 7, 0, 0.0, 8, 17, 0, 7.0, 0.0, 0], '화마의 불꽃 - 샐러맨더': [0, 0, 30, 0, 0.0, 0, 0, 0, 0.0, 0.0, 38], '지고의 화염 - 이프리트': [0, 0, 30, 0, 12.0, 12, 0, 0, 0.0, 0.0, 38], '지독한 집념의 탐구': [0, 0, 0, 0, 28.0, 0, 0, 0, 0.0, 0.0, 40], '영원히 끝나지 않는 탐구': [0, 0, 7, 0, 28.0, 12, 0, 0, 0.0, 0.0, 40], '시간을 가리키는 지침': [0, 0, 0, 0, 0.0, 0, 20, 0, 14.0, 0.0, 0], '시간을 거스르는 자침': [0, 0, 0, 0, 8.0, 0, 24, 0, 14.0, 0.0, 20], '전장을 지배하는 함성': [12, 0, 0, 0, 23.0, 0, 0, 0, 0.0, 0.0, 0], '천지에 울려퍼지는 포효': [12, 0, 4, 0, 23.0, 12, 7, 0, 3.0, 0.0, 0], '광란을 품은 자': [0, 0, 0, 0, 0.0, 0, 30, 0, 11.0, 0.0, 0], '숙명을 뒤엎는 광란': [10, 12, 0, 0, 0.0, 0, 30, 0, 11.0, 0.0, 32], '군신의 유언장': [25, 0, 14, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '뜻을 품은 하늘': [0, 0, 0, 0, 12.0, 0, 0, 0, 12.0, 0.0, 40], '종말의 시간': [0, 0, 0, 0, 0.0, 0, 15, 0, 12.0, 0.0, 0], '제어 회로 모듈': [20, 0, 0, 0, 0.0, 0, 16, 0, 0.0, 0.0, 0], '암흑술사가 직접 저술한 고서': [0, 0, 0, 0, 0.0, 42, 0, 0, 0.0, 0.0, 0], '길 안내자의 여행서': [0, 22, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 64], '비운의 유물': [11, 0, 0, 0, 0.0, 10, 16, 0, 0.0, 0.0, 0], '통제할 수 없는 화': [0, 0, 0, 0, 30.0, 0, 0, 10, 0.0, 0.0, 0], '군신의 가호가 담긴 보석': [0, 21, 0, 0, 0.0, 0, 0, 0, 17.0, 0.0, 0], '지혜를 담은 대지': [0, 0, 0, 0, 12.0, 0, 12, 0, 0.0, 0.0, 40], '시간의 소용돌이': [0, 0, 0, 0, 15.0, 24, 0, 0, 0.0, 0.0, 0], '에너지 분배 제어기': [0, 0, 0, 0, 13.0, 0, 0, 0, 24.0, 0.0, 0], '암흑술사의 정수': [0, 35, 0, 0, 0.0, 0, 0, 0, 7.0, 0.0, 0], '시간에 갇혀버린 모래': [0, 0, 0, 0, 0.0, 0, 17, 0, 0.0, 0.0, 80], '적막이 흐르는 아우성': [0, 23, 0, 0, 0.0, 0, 0, 0, 13.0, 0.0, 0], '폭주하는 광란의 힘': [20, 0, 0, 0, 0.0, 20, 0, 0, 0.0, 0.0, 0], '군신의 수상한 귀걸이': [0, 0, 0, 0, 17.0, 15, 10, 0, 0.0, 0.0, 0], '군신의 마지막 갈망': [0, 0, 4, 0, 24.0, 24, 0, 0, 14.4, 0.0, 0], '마음을 새긴 바다': [16, 0, 10, 0, 0.0, 0, 0, 0, 0.0, 0.0, 40], '영원을 새긴 바다': [20, 0, 10, 0, 8.0, 0, 5, 0, 0.0, 0.0, 80], '시간의 모순': [15, 24, 0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '또다른 시간의 흐름': [15, 24, 8, 0, 0.0, 6, 5, 0, 4.0, 0.0, 0], '전자기 진공관': [0, 0, 10, 0, 0.0, 12, 10, 0, 0.0, 0.0, 40], '플라즈마 초 진공관': [12, 0, 22, 0, 0.0, 12, 10, 0, 0.0, 0.0, 40], '끝없는 나락의 다크버스': [0, 0, 0, 0, 42.0, 0, 0, 0, 0.0, 0.0, 0], '영원한 나락의 다크버스': [0, 0, 9, 0, 54.0, 0, 0, 0, 0.0, 0.0, 40], '차원을 맴도는 혜성': [0, 10, 0, 0, 19.0, 0, 0, 0, 0.0, 1.2272727272727273, 0], '차원을 관통하는 초신성': [0, 21, 0, 0, 19.0, 0, 0, 0, 0.0, 4.909090909090909, 0], '운명을 마주하는 자': [0, 22, 0, 0, 5.0, 0, 10, 0, 0.0, 0.0, 0], '운명을 거스르는 자': [2, 22, 7, 0, 6.0, 0, 15, 0, 0.0, 2.0454545454545454, 0], '슬픔을 담은 운명': [15, 10, 10, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0], '아린 고통의 비극': [15, 18, 11, 0, 0.0, 0, 0, 10, 0.0, 0.0, 16], '(무기)흑천의 주인': [0, 0, 0, 0, 32.0, 0, 0, 0, 55.0, 0.0, 0], '(무기)별의 바다 : 바드나후': [26, 0, 0, 20, 0.0, 0, 0, 0, 22.0, 0.0, 25], '(무기)적광검 루이너스': [0, 0, 0, 0, 22.0, 20, 17, 0, 33.0, 0.0, 31], '(무기)전장의 열정 : 앵거바딜': [0, 30, 34, 0, 0.0, 0, 0, 0, 40.0, 0.0, 0], '(무기)신념의 징표 : 칼리번': [22, 0, 0, 0, 0.0, 22, 26, 0, 30.0, 0.0, 0], '(무기)판데모니엄 플레임': [0, 0, 32, 0, 0.0, 20, 0, 0, 36.0, 0.0, 55], '(무기)히티 - 달을 탐하는 자': [16, 41, 12, 0, 0.0, 0, 0, 0, 32.0, 0.0, 0], '(무기)태극천제검(음)': [0, 0, 0, 0, 21.0, 40, 10, 0, 30.0, 0.0, 0], '(무기)태극천제검(양)': [0, 0, 0, 0, 0.0, 40, 10, 0, 59.9, 0.0, 0], '(무기)아방가르드': [14, 26, 0, 0, 0.0, 0, 25, 0, 35.0, 0.0, 0], '(무기)데우스 이미저리': [35, 0, 0, 0, 0.0, 0, 0, 0, 24.0, 37.0, 50], '(무기)카심의 대검': [0, 0, 20, 0, 43.0, 0, 0, 0, 30.0, 0.0, 0], '(무기)백호의 울음소리': [0, 0, 0, 0, 0.0, 0, 50, 0, 40.0, 0.0, 56], '(무기)청명한 의지': [11, 0, 0, 15, 20.0, 0, 0, 0, 15.0, 37.0, 0], '(무기)청사곤': [0, 40, 34, 0, 0.0, 0, 0, 0, 30.0, 0.0, 0], '(무기)어그레시브 카이트': [30, 0, 0, 0, 0.0, 40, 0, 0, 34.0, 0.0, 0], '(무기)매드 싸이클론(명왕)': [47, 0, 0, 0, 0.0, 0, 16, 10, 22.0, 0.0, 0], '(무기)로드 오브 더 페인': [0, 17, 50, 0, 0.0, 0, 0, 0, 40.0, 0.0, 0], '(무기)태음신 : 영귀': [0, 25, 0, 0, 26.0, 0, 14, 0, 35.0, 0.0, 0], '(무기)디스트로이 프레셔': [0, 40, 34, 0, 0.0, 0, 0, 0, 30.0, 0.0, 0], '(무기)블레이즈 헌터': [24, 0, 0, 0, 12.0, 35, 0, 0, 30.0, 0.0, 0], '(무기)일렉트로 부스터': [0, 0, 35, 0, 0.0, 0, 20, 10, 26.0, 0.0, 35], '(무기)팔로우 더 스타티스': [0, 0, 0, 0, 0.0, 35, 35, 0, 34.0, 0.0, 0], '(무기)메가쇼크 런처': [0, 0, 29, 0, 22.0, 0, 0, 0, 38.0, 0.0, 40], '(무기)커스텀 라이져 보우': [0, 0, 35, 0, 0.0, 36, 0, 0, 30.0, 0.0, 0], '(무기)음유시인의 만돌린': [0, 34, 0, 0, 40.0, 0, 0, 0, 30.0, 0.0, 0], '(무기)미드나잇 러시안 룰렛': [0, 54, 0, 0, 0.0, 18, 0, 0, 35.0, 0.0, 0], '(무기)블러드 샷 부스터': [40, 0, 32, 0, 0.0, 0, 0, 0, 32.0, 0.0, 0], '(무기)터뷸런스': [0, 23, 23, 0, 0.0, 23, 0, 0, 31.0, 0.0, 0], '(무기)스트라이커-X': [20, 20, 0, 0, 0.0, 0, 27, 0, 30.0, 0.0, 0], '(무기)레볼루션 차지': [32, 16, 20, 0, 0.0, 0, 0, 0, 30.0, 0.0, 0], '(무기)오버스펙 라이즈': [0, 0, 0, 0, 0.0, 16, 32, 0, 30.0, 8.0, 40], '(무기)세계수의 뿌리': [0, 0, 10, 0, 0.0, 20, 24, 0, 32.0, 0.0, 0], '(무기)루나 베네딕티오': [13, 13, 0, 0, 25.0, 0, 0, 0, 36.0, 8.0, 0], '(무기)플레임 헬': [0, 0, 0, 15, 34.0, 0, 0, 0, 33.0, 0.0, 0], '(무기)마력의 샘 : 카스탈리아': [0, 0, 0, 0, 21.0, 21, 21, 0, 38.0, 0.0, 0], '(무기)우디 부기': [0, 0, 15, 0, 21.0, 26, 0, 0, 33.0, 0.0, 0], '(무기)카오스 시드': [0, 0, 35, 0, 0.0, 0, 35, 0, 35.0, 0.0, 0], '(무기)어나이얼레이터': [0, 0, 0, 15, 33.0, 0, 0, 0, 35.0, 0.0, 0], '(무기)영창 : 불멸의 혼': [25, 25, 0, 0, 0.0, 15, 0, 0, 35.0, 0.0, 0], '(무기)세계수의 요정': [0, 0, 0, 15, 26.0, 0, 0, 0, 26.0, 8.0, 0], '(무기)순백의 기도': [15, 15, 0, 0, 0.0, 15, 15, 0, 30.0, 0.0, 26], '(무기)포 더 세크리드': [0, 0, 0, 0, 0.0, 36, 36, 0, 31.0, 0.0, 0], '(무기)눈부신 영광': [30, 30, 0, 0, 0.0, 0, 0, 0, 32.0, 0.0, 40], '(무기)윤회의 고리 : 환룡': [20, 0, 0, 0, 0.0, 0, 34, 0, 34.0, 3.0, 0], '(무기)고대 신수의 기억': [0, 36, 0, 0, 0.0, 0, 33, 0, 35.0, 0.0, 0], '(무기)라스트 인파이팅': [12, 16, 38, 0, 0.0, 0, 0, 0, 36.0, 0.0, 0], '(무기)개척자의 길': [0, 10, 0, 0, 0.0, 24, 31, 0, 36.0, 0.0, 0], '(무기)불카누스의 두번째 흔적': [0, 0, 41, 0, 17.0, 0, 0, 10, 28.0, 4.0, 0], '(무기)신념의 무게': [0, 12, 0, 0, 55.0, 0, 0, 0, 40.0, 0.0, 0], '(무기)루즈 리즌': [0, 0, 18, 0, 18.0, 28, 0, 0, 38.0, 0.0, 0], '(무기)이교도 교주의 심판': [20, 24, 25, 0, 0.0, 0, 0, 0, 31.0, 0.0, 0], '(무기)샤프 쉐도어': [0, 0, 0, 18, 26.0, 0, 0, 0, 34.0, 0.0, 0], '(무기)암살단장의 옥장도': [0, 0, 0, 0, 22.0, 22, 22, 0, 35.0, 0.0, 0], '(무기)화려한 눈속임': [0, 0, 0, 0, 32.0, 32, 0, 0, 32.0, 0.0, 0], '(무기)핏빛 무도회': [0, 20, 21, 0, 20.0, 0, 0, 0, 39.2, 0.0, 0], '(무기)푸른 생명의 이면': [0, 0, 19, 0, 23.3, 0, 19, 0, 40.0, 0.0, 0], '(무기)고결한 정령의 유물': [13, 27, 0, 0, 0.0, 27, 0, 0, 35.0, 0.0, 0], '(무기)블러드 루비아이': [30, 20, 0, 0, 0.0, 0, 0, 0, 35.0, 20.0, 40], '(무기)도화선': [0, 0, 13, 0, 0.0, 45, 0, 0, 28.0, 18.0, 0], '(무기)끊임없는 환영': [0, 40, 12, 0, 12.0, 0, 0, 0, 28.0, 0.0, 0], '(무기)전장의 선봉장': [24, 0, 0, 0, 0.0, 13, 26, 0, 38.0, 0.0, 0], '(무기)통곡의 수문장': [0, 0, 0, 14, 29.0, 0, 0, 0, 16.0, 0.0, 0], '(무기)사암주극': [30, 0, 0, 0, 24.0, 0, 0, 0, 16.0, 23.0, 0], '(무기)일렉트로전': [0, 0, 32, 0, 0.0, 16, 18, 0, 35.0, 0.0, 0], '(무기)천장군 : 전승의 빛': [10, 34, 0, 0, 20.0, 0, 0, 0, 38.0, 0.0, 0], '(무기)사일런트 베놈': [0, 0, 0, 0, 40.0, 0, 24, 0, 30.0, 2.0, 0], '(무기)기가 드릴러': [26, 35, 0, 0, 0.0, 0, 0, 0, 38.0, 0.0, 0], '(무기)금강비장도': [10, 10, 0, 0, 0.0, 10, 10, 0, 28.0, 16.0, 50], '(무기)야천도': [0, 0, 0, 14, 29.0, 0, 0, 0, 16.0, 2.0, 0], '(무기)차갑게 굳어버린 홍염': [21, 0, 0, 0, 30.0, 0, 11, 0, 40.0, 0.0, 0], '(무기)다크 플레임 리퍼': [0, 30, 14, 0, 0.0, 23, 0, 0, 35.0, 0.0, 0], '(무기)아토믹 파일': [0, 55, 0, 0, 0.0, 0, 15, 0, 30.0, 0.0, 22], '(무기)홍염폭검': [0, 0, 17, 20, 15.0, 0, 0, 0, 28.0, 0.0, 0], '(무기)베투스 코르': [0, 0, 24, 0, 20.0, 0, 23, 0, 33.0, 0.0, 0], '(무기)프로젝트 : 오버코어': [0, 20, 0, 0, 20.0, 22, 0, 0, 35.00000000000001, 0.0, 0]}
set_option_dict = {'고대 제사장의 신성한 의식 세트2': [21.0, 0, 0, 0, 0, 0, 8.0, 0, 0, 0.0, 0], '고대 제사장의 신성한 의식 세트3': [21.0, 0, 21.0, 0, 0, 8.0, 8.0, 0, 0, 0.0, 0], '고대 제사장의 신성한 의식 세트5': [21.0, 21.0, 21.0, 0, 0, 8.0, 8.0, 0, 25.0, 0.0, 0], '잊혀진 마법사의 유산 세트2': [0, 0, 0, 0, 14.0, 0, 0, 0, 14.0, 0.0, 0], '잊혀진 마법사의 유산 세트3': [22.0, 10.0, 0, 0, 14.0, 0, 0, 0, 14.0, 0.0, 0], '잊혀진 마법사의 유산 세트5': [22.0, 10.0, 0, 0, 14.0, 0, 13.0, 0, 14.0, 24, 0], '천상의 무희 세트2': [0, 17.0, 0, 0, 10.0, 0, 0, 0, 0, 0.0, 0], '천상의 무희 세트3': [16.0, 17.0, 0, 0, 10.0, 0, 11.0, 0, 0, 0.0, 0], '천상의 무희 세트5': [16.0, 17.0, 0, 0, 10.0, 12.0, 11.0, 0, 20.0, 0.0, 0], '심연을 엿보는 자 세트2': [9.0, 0, 0, 0, 0, 0, 0, 0, 0, 9.818181818181818, 0], '심연을 엿보는 자 세트3': [9.0, 0, 0, 0, 0, 0, 0, 0, 13.0, 15.136363636363637, 0], '흑마술의 탐구자 세트2': [12.0, 0, 0, 0, 0, 0, 0, 0, 10.0, 0.0, 0], '흑마술의 탐구자 세트3': [12.0, 0, 0, 13.0, 0, 0, 0, 0, 10.0, 0.0, 0], '나락의 구도자 세트2': [0, 0, 10.0, 0, 10.0, 0, 0, 0, 0, 0.0, 0], '나락의 구도자 세트3': [0, 0, 10.0, 0, 10.0, 0, 0, 0, 16.0, 0.0, 40.0], '황혼의 여행자 세트2': [0, 11.0, 10.0, 0, 0, 0, 0, 0, 0, 0.0, 0], '황혼의 여행자 세트3': [0, 11.0, 10.0, 0, 0, 5.0, 0, 0, 12.0, 0.0, 32.0], '죽음을 자아내는 그림자 세트2': [0, 0, 0, 0, 0, 0, 14.0, 0, 0, 0.0, 55.0], '죽음을 자아내는 그림자 세트3': [0, 0, 0, 0, 14.0, 0, 14.0, 0, 16.0, 0.0, 55.0], '죽음을 자아내는 그림자 세트5': [0, 0, 0, 0, 14.0, 0, 14.0, 0, 69.12800000000001, 0.0, 55.0], '황실 직속 집행자의 선고 세트2': [16.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 52.0], '황실 직속 집행자의 선고 세트3': [16.0, 0, 0, 0, 0, 0, 15.0, 0, 0, 0.0, 114.0], '황실 직속 집행자의 선고 세트5': [16.0, 0, 0, 20.0, 0, 0, 15.0, 0, 0, 0.0, 114.0], '베테랑 군인의 정복 세트2': [0, 0, 0, 0, 0, 0, 23.0, 0, 0, 0.0, 0], '베테랑 군인의 정복 세트3': [0, 24.0, 0, 0, 0, 0, 23.0, 0, 0, 0.0, 24.0], '베테랑 군인의 정복 세트5': [0, 24.0, 41.0, 0, 0, 0, 23.0, 0, 0, 0.0, 24.0], '시간의 여행자 세트2': [0, 0, 0, 0, 10.0, 10.0, 0, 0, 0, 0.0, 0], '시간의 여행자 세트3': [0, 17.0, 0, 0, 10.0, 10.0, 0, 0, 13.0, 0.0, 0], '차원의 여행자 세트2': [0, 0, 22.0, 0, 0, 0, 0, 0, 0, 0.0, 0], '차원의 여행자 세트3': [0, 10.0, 22.0, 0, 0, 0, 0, 0, 18.0, 0.0, 0], '메마른 사막의 유산 세트2': [0, 0, 0, 0, 0, 22.0, 0, 0, 6.0, 0.0, 0], '메마른 사막의 유산 세트3': [0, 0, 0, 0, 0, 22.0, 0, 0, 21.899999999999984, 0.0, 60.0], '메마른 사막의 유산 세트5': [0, 0, 0, 0, 0, 22.0, 0, 0, 73.09799999999997, 0.0, 60.0], '열대의 트로피카 세트2': [0, 18.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 40.0], '열대의 트로피카 세트3': [0, 18.0, 10.0, 0, 0, 0, 0, 0, 20.0, 0.0, 40.0], '열대의 트로피카 세트5': [0, 18.0, 10.0, 0, 22.0, 0, 0, 0, 20.0, 0.0, 40.0], 'A.D. P 슈트 세트2': [14.0, 14.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0], 'A.D. P 슈트 세트3': [14.0, 14.0, 0, 0, 0, 32.0, 0, 0, 0, 0.0, 0], 'A.D. P 슈트 세트5': [14.0, 14.0, 0, 12.0, 0, 32.0, 0, 0, 2.5, 0.0, 0], '운명을 가르는 함성 세트2': [0, 0, 0, 0, 0, 23.0, 0, 0, 0, 0.0, 0], '운명을 가르는 함성 세트3': [0, 0, 0, 0, 0, 23.0, 14.0, 0, 16.0, 0.0, 0], '운명의 주사위 세트2': [7.0, 0, 8.0, 0, 0, 0, 0, 0, 5.0, 0.0, 0], '운명의 주사위 세트3': [7.0, 0, 18.0, 0, 0, 0, 11.666666666666668, 0, 12.35, 0.0, 0], '기구한 운명 세트2': [14.0, 0, 0, 0, 0, 0, 0, 0, 9.0, 0.0, 0], '기구한 운명 세트3': [14.0, 20.0, 0, 0, 0, 0, 0, 0, 19.9, 0.0, 0], '삼켜진 분노 세트2': [10.0, 11.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0], '삼켜진 분노 세트3': [10.0, 11.0, 0, 0, 0, 0, 30.0, 0, 0, 0.0, 0], '개악 : 지옥의 길 세트2': [0, 0, 0, 0, 6.0, 16.0, 0, 0, 6.0, 0.0, 0], '개악 : 지옥의 길 세트3': [0, 0, 0, 0, 6.0, 16.0, 0, 0, 6.0, 8.181818181818182, 66.0], '개악 : 지옥의 길 세트5': [0, 0, 0, 0, 6.0, 16.0, 0, 0, 54.760000000000005, 8.181818181818182, 66.0], '전설의 대장장이 - 역작 세트2': [0, 0, 0, 0, 14.0, 0, 14.0, 0, 0, 0.0, 0], '전설의 대장장이 - 역작 세트3': [0, 0, 0, 0, 14.0, 21.0, 14.0, 0, 0, 0.0, 0], '전설의 대장장이 - 역작 세트5': [0, 0, 27.0, 0, 14.0, 21.0, 14.0, 0, 0, 0.0, 0], '구속의 가시덩굴 세트2': [12.0, 11.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0], '구속의 가시덩굴 세트3': [12.0, 11.0, 25.0, 0, 0, 0, 0, 0, 0, 0.0, 0], '구속의 가시덩굴 세트5': [22.0, 11.0, 25.0, 0, 0, 0, 0, 0, 28.0, 0.0, 0], '광란의 추종자 세트2': [0, 0, 0, 0, 0, 0, 18.0, 0, 0, 0.0, 25.0], '광란의 추종자 세트3': [0, 16.0, 0, 0, 0, 0, 18.0, 0, 15.0, 0.0, 25.0], '아린 비극의 잔해 세트2': [0, 0, 0, 0, 23.0, 0, 0, 0, 0, 0.0, 0], '아린 비극의 잔해 세트3': [0, 0, 0, 0, 23.0, 29.0, 0, 0, 0, 0.0, 0], '영원한 흐름의 길 세트2': [0, 0, 0, 0, 0, 0, 32.0, 0, 0, 0.0, 0], '영원한 흐름의 길 세트3': [0, 0, 0, 0, 32.0, 0, 32.0, 0, 0, 0.0, 0], '영원한 흐름의 길 세트5': [20.0, 0, 0, 0, 32.0, 23.0, 32.0, 0, 0, 0.0, 0], '선택의 기로 세트2': [15.0, 0, 13.0, 0, 0, 0, 0, 0, 0, 0.0, 0], '선택의 기로 세트3': [27.0, 17.0, 13.0, 0, 0, 0, 0, 0, 0, 0.0, 0], '선택의 기로 세트5': [27.0, 28.0, 13.0, 0, 30.0, 0, 0, 0, 0, 0.0, 0], '대자연의 숨결 세트2': [0, 15.0, 0, 0, 0, 0, 16.0, 0, 0, 0.0, 0], '대자연의 숨결 세트3': [15.0, 15.0, 0, 0, 0, 0, 16.0, 0, 13.0, 0.0, 0], '대자연의 숨결 세트5': [15.0, 15.0, 0, 0, 11.0, 0, 16.0, 0, 24.3, 0.0, 64.0], '고대의 술식 세트2': [0, 0, 0, 0, 0, 14.0, 10.0, 0, 0, 0.0, 0], '고대의 술식 세트3': [0, 20.0, 0, 0, 0, 14.0, 10.0, 0, 0, 0.0, 0], '먼동 틀 무렵 세트2': [0, 0, 0, 0, 10.0, 10.0, 0, 0, 0, 0.0, 0], '먼동 틀 무렵 세트3': [0, 0, 0, 10.0, 10.0, 10.0, 0, 0, 0, 0.4090909090909091, 0], '행운의 트라이앵글 세트2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 77.0], '행운의 트라이앵글 세트3': [0, 0, 0, 0, 0, 0, 0, 0, 29.15, 0.0, 77.0], '정령사의 장신구 세트2': [0, 10.0, 0, 0, 0, 0, 0, 0, 12.0, 0.0, 0], '정령사의 장신구 세트3': [0, 10.0, 0, 0, 0, 0, 10.0, 0, 12.0, 0.0, 0], '군신의 숨겨진 유산 세트2': [0, 5.0, 0, 0, 8.0, 10.0, 0, 0, 0, 0.0, 0], '군신의 숨겨진 유산 세트3': [0, 5.0, 0, 0, 8.0, 10.0, 10.0, 0, 10.0, 0.0, 0], '영보 : 세상의 진리 세트2': [0, 0, 15.0, 0, 0, 0, 0, 0, 7.0, 0.0, 0], '영보 : 세상의 진리 세트3': [0, 12.0, 15.0, 0, 0, 0, 0, 0, 7.0, 8.181818181818182, 0], '시간전쟁의 잔해 세트2': [0, 11.0, 0, 0, 0, 11.0, 0, 0, 0, 0.0, 0], '시간전쟁의 잔해 세트3': [0, 11.0, 0, 0, 0, 11.0, 10.0, 0, 10.0, 0.0, 0], '노멀라이즈 싱크로 세트2': [12.0, 0, 0, 0, 0, 12.0, 0, 0, 0, 0.0, 0], '노멀라이즈 싱크로 세트3': [12.0, 0, 10.0, 0, 0, 12.0, 0, 0, 8.0, 0.0, 0], '붉게 일렁이는 혈광갑주 세트3': [0, 0, 10.0, 0, 0, 5.0, 0, 0, 0, 0.0, 20.0], '붉게 일렁이는 혈광갑주 세트5': [0, 0, 10.0, 0, 0, 15.0, 10.0, 0, 0, 0.0, 50.0], '타락한 어둠의 힘 세트3': [10.0, 10.0, 0, 0, 0, 5.0, 0, 0, 0, 0.0, 0], '타락한 어둠의 힘 세트5': [10.0, 10.0, 20.0, 0, 12.0, 5.0, 0, 0, 0, 0.0, 0], '디멘션 크래쉬 세트3': [0, 0, 8.0, 0, 0, 0, 8.0, 0, 8.0, 0.0, 0], '어둠의 침식 세트3': [0, 10.0, 0, 0, 0, 0, 5.0, 0, 15.0, 0.0, 0], '엠피리언 컴벳 유니폼 세트3': [0, 0, 0, 0, 0, 0, 25.0, 0, 0, 0.0, 0], '엠피리언 퍼스트 컴벳 세트3': [0, 0, 0, 0, 0, 0, 0, 0, 10.0, 0.0, 0], '엠피리언 세컨드 컴벳 세트3': [0, 0, 0, 0, 0, 0, 0, 0, 12.0, 0.0, 0]}
server_value = ["카인", "디레지에", "시로코", "프레이", "카시야스", "힐더", "안톤", "바칼"]

equipped_weapon = ''
server_name = ''

window = tk.Tk()
window.title("서버 닉네임 무기")

tk.Label(window, text="서버").grid(row=0)
tk.Label(window, text="").grid(row=1)
tk.Label(window, text="닉네임").grid(row=2)
tk.Label(window, text="").grid(row=3)
tk.Label(window, text="무기").grid(row=4)

combobox_value = []
for items in option_dict:
    if items.find('(무기)') > -1:
        combobox_value.append(items[4:])

server_combobox = tkinter.ttk.Combobox(window, height=30, values=server_value)
server_combobox.set('카인')
server_combobox.grid(row=0, column=1)



ch_name = tk.Entry(window)
ch_name.grid(row=2, column=1)

weapon_combobox = tkinter.ttk.Combobox(window, height=30, values=combobox_value)
weapon_combobox.set('흑천의 주인')
weapon_combobox.grid(row=4, column=1)
char_name = ''


def callback():
    global server_name
    global equipped_weapon
    global char_name
    server_name = server_combobox.get()
    equipped_weapon = weapon_combobox.get()
    char_name = ch_name.get()

    window.destroy()

b = tk.Button(window, text="입력", command=callback)
b.grid(row=2, column=2)
window.mainloop()


server_url = "https://api.neople.co.kr/df/servers?apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH"
response = requests.get(server_url)
server_info = json.loads(response.text)
for server in server_info['rows']:
    for id, name in server.items():
        if name.find(server_name) > -1:
            server_name = server['serverId']
            break

url = "https://api.neople.co.kr/df/servers/" + server_name + "/characters?characterName=" + parse.quote(char_name) + "&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH"
response = requests.get(url)
result = json.loads(response.text)

char_id = result['rows'][0]['characterId']

timeline_code = ['504', '505', '506', '507', '508', '511', '513', '514']
item_list = []

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y%m%d')
for cd in timeline_code:
    dungeon_url = "https://api.neople.co.kr/df/servers/" + server_name + "/characters/" + char_id + "/timeline?limit=100&code=" + cd + "&startDate=20200101T0000&endDate=" + nowDatetime + "&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH"
    dungeon_response = requests.get(dungeon_url)
    dungeon_result = json.loads(dungeon_response.text)
    for epic_drop in dungeon_result['timeline']['rows']:
        item_list.append(epic_drop['data']['itemName'])
    if dungeon_result['timeline']['next']:
        while True:
            dungeon_url = "https://api.neople.co.kr/df/servers/" + server_name + "/characters/" + char_id + "/timeline?" + "next=" + \
                          dungeon_result['timeline']['next'] + "&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH"
            dungeon_response = requests.get(dungeon_url)
            dungeon_result = json.loads(dungeon_response.text)
            for epic_drop in dungeon_result['timeline']['rows']:
                item_list.append(epic_drop['data']['itemName'])
            if not dungeon_result['timeline']['next']:
                break

timeline_list = item_list[:]

path = os.getcwd()
path += "\\"

set_dict = {}
code_dict = {}
mythcal_list = []
for set_name, data in set_list.items():
    tmp_dict = {}
    for part in data['setItems']:
        code_dict[part['itemName']] = part['itemId']
        if part['itemRarity'] == '신화':
            mythcal_list.append(part['itemName'])
            if not part['slotName'] in tmp_dict:
                if part['itemName'] in item_list:
                    tmp_dict[part['slotName']+'[신화]'] = part['itemName']
        else:
            if not part['slotName'] in tmp_dict:
                if part['itemName'] in item_list:
                    tmp_dict[part['slotName']] = part['itemName']
    if bool(tmp_dict):
        set_dict[set_name] = tmp_dict

timeline_set = copy.deepcopy(set_dict)

# for set, parts in set_dict.items():
#    print('\t'+set)
#    print(parts)

def set_finder(part_name):
    for set_name, set_parts in set_dict.items():
        for part, item_name in set_parts.items():
            if part_name == item_name:
                return set_name


parts = ['상의[신화]', '상의', '하의', '머리어깨', '허리', '신발', '팔찌[신화]', '팔찌', '목걸이', '반지', '보조장비', '마법석', '귀걸이[신화]', '귀걸이']


while True:
    checkbox = tk.Tk()
    checkbox.title("타임라인에 기록되지 않는 아이템 추가")
    checkbox.geometry("+1+1")
    checkbox.attributes("-topmost", True)
    button_dict = {}
    var_dict = {}
    img_dict = {}
    for set_name, data in set_list.items():

        button_list = []
        for part in data['setItems']:
            var_dict[part['itemName']] = tk.IntVar()
            if not os.path.isdir(path+'images\\'):
                os.mkdir(path+'images\\')
                response = requests.get('https://img-api.neople.co.kr/df/items/' + code_dict[part['itemName']])
                img = Image.open(BytesIO(response.content))
                img.save(path + 'images\\' + part['itemId'] + '.png')
            else:
                img = Image.open(path + 'images\\' + part['itemId'] + '.png')
            img_dict[part['itemName']] = ImageTk.PhotoImage(img)
            if part['itemRarity'] == '신화':
                checkbutton = tk.Checkbutton(checkbox, text=part['slotName'] + '[신화]', image=img_dict[part['itemName']],
                                             height=20, variable=var_dict[part['itemName']])
            else:
                checkbutton = tk.Checkbutton(checkbox, text=part['slotName'], image=img_dict[part['itemName']],
                                             height=20, variable=var_dict[part['itemName']])
            if part['itemName'] in item_list:
                checkbutton.select()
            button_list.append(checkbutton)
        button_dict[set_name] = button_list

    button_row = 0
    accessory = 0
    add_list = []
    sub_list = []
    for set_name, buttons in button_dict.items():
        button_parts = ['상의[신화]', '상의', '하의', '머리어깨', '허리', '신발', '세트명', '팔찌[신화]', '팔찌', '목걸이', '반지', '보조장비', '마법석',
                        '귀걸이[신화]', '귀걸이']
        label = tk.Label(checkbox, text=set_name)
        if accessory == 0:
            label.grid(row=button_row, column=0)
        if accessory == 1:
            label.grid(row=button_row, column=7)
        for button in buttons:
            button_col = button_parts.index(button.cget("text")) + 1
            button.grid(row=button_row, column=button_col)
            button_col += 1
        button_row += 1
        if set_name == '아린 비극의 잔해 세트':
            button_row = 0
            accessory = 1
    def checkbox_check():
        for key, value in var_dict.items():
            if value.get() == 1 and key not in item_list:
                for set_name, data in set_list.items():
                    for part in data['setItems']:
                        if part['itemName'] == key:
                            if key in mythcal_list:
                                add_elem = [set_name, part['slotName']+'[신화]', part['itemName'], part['itemId']]
                            else:
                                add_elem = [set_name, part['slotName'], part['itemName'], part['itemId']]
                            add_list.append(add_elem)
            if value.get() == 0 and key in item_list:
                for set_name, data in set_list.items():
                    for part in data['setItems']:
                        if part['itemName'] == key:
                            sub_list.append(key)

        checkbox.destroy()


    submit_button = tk.Button(checkbox, text="완료", command=checkbox_check)
    submit_button.grid(row=10, column=17, rowspan=10)

    reset_flag = False
    def item_list_reset():
        global item_list
        global timeline_list
        global reset_flag
        global set_dict
        global timeline_set
        item_list = timeline_list[:]
        set_dict = copy.deepcopy(timeline_set)
        checkbox.destroy()
        reset_flag = True


    submit_button = tk.Button(checkbox, text="초기화", command=item_list_reset)
    submit_button.grid(row=9, column=17, rowspan=10)

    checkbox.mainloop()

    if reset_flag == True:
        continue

    for item in sub_list:

        deleting_set = set_finder(item)
        if len(set_dict[deleting_set]) == 1:
            del set_dict[deleting_set]
        else:
            deleting_part = ''
            for sub_part, sub_name in set_dict[deleting_set].items():
                if sub_name == item:
                    deleting_part = sub_part
            del set_dict[deleting_set][deleting_part]
        item_list.remove(item)

    for item in add_list:
        if not item[0] in set_dict:
            set_dict[item[0]] = {}
        set_dict[item[0]][item[1]] = item[2]
        item_list.append(item[2])


    best_score = 0.0
    candidate = {}

    for set_name, set_part in set_dict.items():
        candidate[set_name] = []
        not_mythcal = ['상의', '하의', '머리어깨', '허리', '신발', '팔찌', '목걸이', '반지', '보조장비', '마법석', '귀걸이']
        candi_temp = {}
        for non_myth in not_mythcal:
            if non_myth in set_part.keys():
                candi_temp[non_myth] = set_part[non_myth]
        if len(candi_temp) == 2:
            candidate[set_name].append(candi_temp)
        if len(candi_temp) == 3:
            candidate[set_name].append(candi_temp)
            two_set_keys = list(itertools.combinations(candi_temp, 2))
            for key_list in two_set_keys:
                temp_two = {}
                for keys in key_list:
                    temp_two[keys] = candi_temp[keys]
                candidate[set_name].append(temp_two)
        if len(candi_temp) == 4:
            two_set_keys = list(itertools.combinations(candi_temp, 2))
            for key_list in two_set_keys:
                temp_two = {}
                for keys in key_list:
                    temp_two[keys] = candi_temp[keys]
                candidate[set_name].append(temp_two)

            three_set_keys = list(itertools.combinations(candi_temp, 3))
            for key_list in three_set_keys:
                temp_three = {}
                for keys in key_list:
                    temp_three[keys] = candi_temp[keys]
                candidate[set_name].append(temp_three)
        if len(candi_temp) == 5:
            candidate[set_name].append(candi_temp)
            two_set_keys = list(itertools.combinations(candi_temp, 2))
            for key_list in two_set_keys:
                temp_two = {}
                for keys in key_list:
                    temp_two[keys] = candi_temp[keys]
                candidate[set_name].append(temp_two)

            three_set_keys = list(itertools.combinations(candi_temp, 3))
            for key_list in three_set_keys:
                temp_three = {}
                for keys in key_list:
                    temp_three[keys] = candi_temp[keys]
                candidate[set_name].append(temp_three)
        if not candi_temp.keys() == set_part.keys():    #신화있음
            myth_key = ''
            for x in set_part.keys():
                if x.find('신화') > -1:
                    myth_key = x

            if myth_key[:len(myth_key)-4] in candi_temp.keys():  #같은부위 일반템 있음
                myth_temp = copy.deepcopy(candidate[set_name])
                for duplicates in myth_temp:
                    if myth_key[:len(myth_key)-4] in duplicates.keys():
                        del duplicates[myth_key[:len(myth_key)-4]]
                    duplicates[myth_key] = set_part[myth_key]
                    candidate[set_name].append(duplicates)
            else:
                myth_temp = copy.deepcopy(candidate[set_name])
                for duplicates in myth_temp:
                    duplicates[myth_key] = set_part[myth_key]
                    candidate[set_name].append(duplicates)
            candidate[set_name].append({myth_key: set_part[myth_key]})

    candi_keys = list(candidate.keys())

    def equip_checker(set_a, set_b):
        A_list = [*set_a]
        for a in A_list:
            if a == '상의' or a == '팔찌' or a == '귀걸이':
                if not set_b[a] == '':
                    return False
                if not set_b[a+'[신화]'] == '':
                    return False
            else:
                if a == '상의[신화]' or a == '팔찌[신화]' or a == '귀걸이[신화]':
                    if not set_b[a] == '':
                        return False
                    if not set_b[a[:len(a)-4]] == '':
                        return False
                else:
                    if not set_b[a] == '':
                        return False
        return True
    best_sets = []
    secondary = []
    sets_list = []
    for candi_level in candi_keys:
        if not sets_list:
            for items in candidate[candi_level]:
                tmp = {}
                for part in parts:
                    tmp[part] = ''

                if len(items) == 2:
                    tmp['score'] = 2.0
                if len(items) == 3:
                    #if len(set_list[candi_level]['setItems']) == 3:
                    #    tmp['score'] = 5.0
                    #else:
                    #    tmp['score'] = 4.0
                    tmp['score'] = 5.0
                if len(items) == 5:
                    tmp['score'] = 7.0
                else:
                    tmp['score'] = 0.0
                for key, value in items.items():
                    tmp[key] = value
                sets_list.append(tmp)

            tmp = {}
            for part in parts:
                tmp[part] = ''
            tmp['score'] = 0.0
            sets_list.append(tmp)
        else:
            for cur_list in range(0, len(sets_list)):
                for items in candidate[candi_level]:
                    if equip_checker(items, sets_list[cur_list]):
                        tmp = sets_list[cur_list].copy()
                        if len(items) == 2:
                            tmp['score'] += 2.0
                        if len(items) == 3:
                            #if len(set_list[candi_level]['setItems']) == 3:
                            #    tmp['score'] += 5.0
                            #else:
                            #    tmp['score'] += 4.0
                            tmp['score'] += 5.0
                        if len(items) == 5:
                            tmp['score'] += 7.0
                        for key, value in items.items():
                            tmp[key] = value

                        sets_list.append(tmp)
    for complete_lists in sets_list:
        sinhwa = 0
        for key, value in complete_lists.items():
            if not key == 'score':
                if value in mythcal_list:
                    if sinhwa > 0:
                        complete_lists['score'] = -1
                        break
                    sinhwa = 2.0
        if not complete_lists['score'] == -1:
            complete_lists['score'] += sinhwa
    for complete_lists in sets_list:
        if complete_lists['score'] > best_score:
            best_score = complete_lists['score']
            secondary = best_sets[:]
            best_sets = [complete_lists]
        if complete_lists['score'] == best_score:
            if not complete_lists in best_sets:
                best_sets.append(complete_lists)

    # print("먹은 에픽 개수: " + str(len(item_list)))
    # print("가장 많은 세트 효과를 가진 조합," + str(best_score) + '점')


    # for BS in best_sets:
    #    for part, name in BS.items():
    #        print('\t\t' + part)
    #        print('%-20s(%s)' % (str(name), str(set_finder(name))))
    #    print("==========================================================\n\n")

    row = 0
    window = tk.Tk()
    window.title("Best Sets")
    window.geometry("+1+1")
    window.attributes("-topmost", True)
    label_dict = []
    label_image_list = []


    if len(best_sets) + len(secondary) < 30:
        best_sets = best_sets + secondary
    mythcal_part = ['상의', '팔찌', '귀걸이']
    for bs in best_sets:
        for x in mythcal_part:
            bs[x] = bs[x]+bs[x+'[신화]']
            del bs[x+'[신화]']
    for BS in best_sets:
        col = 0
        label_list = []
        image_inner_list = []
        default = [0.0, 18.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 181.0]
        #기본속강 181 크증크리쳐 18프로 추뎀칭호 10프로
        equipped_set = {}
        for part, name in BS.items():
            if not name == '' and not isinstance(name, float):
                if not set_finder(name) in equipped_set.keys():
                    equipped_set[set_finder(name)] = 1
                else:
                    equipped_set[set_finder(name)] += 1
                for i in range(0, 11):
                    if i == 8:
                        default[i] *= (option_dict[name][i] + 100.0) / 100.0
                    else:
                        default[i] += option_dict[name][i]

            label_list.append(name)

            col += 1
        final_score = 100.0
        for ES, num in equipped_set.items():
            if num == 1: continue
            for i in range(0, 11):
                if i == 8:
                    default[i] *= (set_option_dict[ES+str(num)][i] + 100.0) / 100.0
                else:
                    default[i] += set_option_dict[ES+str(num)][i]

        for i in range(0, 11):
            if i == 8:
                default[i] *= (option_dict['(무기)'+equipped_weapon][i] + 100.0) / 100.0
            else:
                default[i] += option_dict['(무기)'+equipped_weapon][i]

        elemental = (1.05 + (default[10]*0.0045))
        add_dmg = default[2]/100.0 + default[3]*elemental/100.0 + 1
        final_score *= elemental * add_dmg * (default[8]/100.0)
        for i in range(0, 10):
            if i in [0, 1, 4, 5, 6, 7, 9]:
                final_score *= (default[i]+100.0)/100.0



        label_list.append(round(final_score))

        if len(label_dict) == 0:
            label_dict.append(label_list)
        else:
            inserted = False
            for index in range(len(label_dict)):
                tmp = label_dict[index][12]
                if int(tmp) < final_score:
                    label_dict.insert(index, label_list)
                    inserted = True
                    break
            if inserted == False:
                label_dict.append(label_list)
        row += 1
    row = 0
    images = []
    for labels in label_dict:
        if row > 12:
            break
        col = 0
        for name in labels:
            if name == '':
                img = Image.new('RGB', (28, 28))
            else:
                if isinstance(name, float):
                    continue
                if isinstance(name, int):
                    label = tk.Label(window, text=str(name), fg="red", relief="solid")
                    label_list.append(label)
                    label.grid(row=row, column=col)
                    col += 1
                    break
                img = Image.open(path + 'images\\' + code_dict[name] + '.png')

            img2 = ImageTk.PhotoImage(img)
            images.append(img2)
            label = tk.Label(window, width=28, height=56, image=images[len(images)-1])
            label.grid(row=row, column=col)
            col += 1
        row += 1
    go_back_flag = False

    def go_back():
        global go_back_flag
        window.destroy()
        go_back_flag = True

    b = tk.Button(window, text="뒤로가기", command=go_back)
    b.grid(row=0, column=16)
    window.mainloop()

    if go_back_flag == True:
        continue

    break

# set_list = ['72b9d0625ac8f77c16e4fb3a329235a5', 'd675cb6e153e02388e2e0a7ab188acde', '266097499b3bdfd1b2427649856f9b42', 'a91423120c0d260dad4b879165d5c234', 'b5bb71953bc709c84137b0cad5d14e4e', '070e8126fc113f9a7a148d3a9ceb3ea0', 'a9ea5e000a2942e188126d02be966b84', 'c5947b6928696a5bf182c6acf348ca28', '33348fff4c17d204c4655ee50e2c6bdc', '3fddf4524b6aa73652e0cdfbc2306137', '504960c246d867f262a4bdfb174d9ecb', '3a441737656962d57d3f506bc3ed68e0', 'ae4e5f8c339b667f2af12db2505f6ece', '3c5b33d2817bfeb33fb9d64a84a64ef8', '00d09213980eb1bb66389ad61576703b', '8cf8910dcbabacf11907f98db19de767', 'f1076d938f10a593c757c377bc84af03', '861e52afdbbcbcc015188a5d77f30dc1', 'd69db0f43a2c9250ee020e5cd38a18f6', '1d4ed1e13b380593c889feef9ec2f62d', '2faa0b8988b5baa7216f0330b2a9e1ae', '5bc36d6fb20ea5007422608f9a18e586', '4409ac3fd335adeea84fe227fcbe0fa9', 'f51b430435a8383b3cf6d34407c4a553', 'bcd72f6c009738cb256b13403fc84b8c', '5742ec75674086d001067005f43f0da4', 'bf7f99836f89770380231245c6048dfe', 'f19e9a71b2cd4f077998309cea838b93', '2d228dcdcab18d2ab425dae8a2781df9', '9b2a1398222c5ead60edc99cf959338a', 'f999962c227725c02d4b8626f46f58c7', '0d7fa7e5f82d8ec524d1b8202b31497f', '0cd4fb46aa92d65d242ca44d34a3f27a', 'cff2e64e3f4fb0669d77b11743d0cc6b', '236b7169ff3612b54fb09f9753c138c1']
# for set_code in set_list:
#     set_url = "https://api.neople.co.kr/df/setitems/"+ set_code +"?apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH"
#
#     set_response = requests.get(set_url)
#     set_result = json.loads(set_response.text)
#     #while True:
#     #    try:
#     #        set_code = set_result['rows'][0]['setItemId']
#     #    except:
#     #        time.sleep(5)
#     #        set_response = requests.get(set_url)
#     #        set_result = json.loads(set_response.text)
#     #        continue
#     #    break
#     while True:
#         if not 'error' in set_result:
#             break
#         time.sleep(5)
#         set_response = requests.get(set_url)
#         set_result = json.loads(set_response.text)
#     print(set_result)
