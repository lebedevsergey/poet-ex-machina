# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

# Beautiful decorations from original programs comments should be preserved for our descendants // Sergey Lebedev
# ;;───────────────────────────────────────────────────    
# 
# ;───────────┬┬────────────┬───────────────┬─────┬─────────────────┐
# ;───────────┼┴┬─────┬─────┼─────┬─────────┼─────┼──┬───┬──────────┤
# ;───────────┼─┴─┬───┴─┬───┼─────┼───────┬─┼─────┴──┼───┼──────┬───┤
# ;───────────┴───┴─────┼───┼─────┼───────┼─┴────────┴───┼──────┼───┤
# ;─────────────────────┴───┴─────┴───────┴──────────────┴──────┴───┘
#
# ;────────────────────────────────────────────────────


# 
#               \¦/                             \¦/
#       -¬    г¬ -T--=¬ гT===¬ г¬   ¬  \¦/       г==--¬  г--===
#   \¦/ ¦L=¬-=-¦ ¦¦     ¦¦     ¦¦   ¦            ¦    ¦  ¦       \¦/
#       ¦-¬L=¦¬¦ ¦¦     ¦¦ \¦/ L+-==¦     ===    L--==+--+----¬
#       ¦¦L¬г-¦¦ ¦¦     ¦¦          ¦                 ¦  ¦    ¦
#       L- L- L- L- \¦/ L-     L===--    \¦/    ====---  L--==-

englishMsg = '''
Python port of verse making program written in 1996 by Leonid Kaganov 
usage:
 LLEO_DIP.EXE b basename.bsy some.txt
  - create (extend) Words base basename.bsy from text file some.txt
'''

newMsg = '''
Программа-поэт (с) Sergey Lebedev, 2016
написана по мотивам программы Леонида Каганова, 
написанной в 1996 году на x86 Ассемблере     
запустите с ключом --oldschool для вывода оригинального help'а 
       
 Для запуска используйте:
  python lleo_dip.py b basename some.txt
  - создать(дополнить) ассоциативную базу basename, прочтя текст some.txt
  - при расстановке ударений можно нажать ESC, и они будут проставлены сами 
  
 python lleo_dip.py u basename
  - продолжить ручную простановку ударений в базе basename  
 
 python lleo_dip.py p basename
  - сочинять предложения в прозе, используя basename
 
 python lleo_dip.py c basename stih.rtm
  - сочинить стих, используя basename и файл ритма stih.rtm, например:
                       +--+--+--+  A
                       +--+--+     B  
  + - ударный слог, A - код рифмы (заглавная латинская буква).
  
  - программа умеет загружать базу в формате оригинальной программы (.BSY)
  - в этом случае база будет сохранена в новом формате, с тем же именем и расщирением .words,
  - база слогов будет сохранена в новом формате, с тем же именем и расщирением .syll  
'''

oldMsg1 = '''
           Московский Государственный Горный Университет
 Факультет информатики и автоматизации. Кафедра вычислительных машин.
                          ДИПЛОМНЫЙ ПРОЕКТ
 ""Лингвистическое конструирование в системах искусственного интеллекта""
     LLEO_DIP.EXE - программа, сочиняющая стихи с заданным ритмом,
     используя ассоциативную базу, созданную при прочтении текста

 Для запуска используйте:
 LLEO_DIP.EXE b basename.bsy some.txt
  - создать(дополнить) ассоциативную базу basename.bsy, прочтя текст some.txt
    при расстановке ударений можно нажать ESC, и они будут проставлены сами
 
 LLEO_DIP.EXE u basename.bsy
  - продолжить ручную простановку ударений в базе basename.bsy
 
 LLEO_DIP.EXE p basename.bsy
  - сочинять предложения в прозе, используя basename.bsy
 
 LLEO_DIP.EXE c basename.bsy stih.rtm
  - сочинить стих, используя basename.bsy и файл ритма stih.rtm, например:
                       +--+--+--+  A
                       +--+--+     B
                       +--+--+--+  A
                       +--+--+     B
  В этом примере куплеты будут состоять из 4 строк, - - безударный слог,
  + - ударный слог, A - код рифмы (заглавная латинская буква).
 
 ! Все результаты записываются в файл RESULTAT.TXT
'''

oldMsg2 = '''
 А сейчас, пользуясь случаем, хочу выразить благодарность:
 Садретдинову Ринату, Зефирову Сергею и Лемехову Дмитрию за неоценимую помощь и,постоянную консультацию;
 Эльдарову Ильясу за то, что он великий программист и вообще хороший человек,несмотря на то, что любит такую попсу, как WIN95, а не профессиональные,операционные системы как OS/2 WARP;
 Дмитрию Антонову, Алексею Крылову и Сергею Лохову конечно же - что бы я без них делал?;
 Матери, отцу, бабушке, сестре Маргарите, и всем кто за меня волновался;
 Константину Петрову - за мудрые мысли о лингвистике;
 Леониду Гриценко - за то, что не сломал мне компьютер;
 Карине - за то, что она Карина;
 Александру Недоспасову, Даниле Швецу, Шобанову Евгению, Кириллу и Катерине,Сохатовым, Александру Аксельроду и Алексею Линецкому, чтоб он скорее к нам,вернулся из своего мерзкого Нью-Йорка;
 Ольге Лабузовой, Вадиму и Ольге Марковым, Мамаеву Сергею и сестре его Антонине,Вероничке Васильевой, Александре Тертель, Наташке Ярошенко, Ариадне с Костей и  Сороке за то, что они есть на свете;
 Максу Иванову, Артему Полонскому и Борису Савину за материалы, использованные в,пояснительной записке;
 Антону Кротову, Денису Петрову и Jay Way - за мудрость философскую;
'''

oldMsg3 = ''' 
 Алексу Толоку и Леониду Николаеву - за СТЭМ матфака МГПИ;
 Горбатову В.А. и Хомской Е.Д. за вклад в развитие науки;
 Сергею Белоголовцеву, Василию Антонову, Андрею Бочарову,Александру Толоконниковуи Татьяне Лазаревой - за то, что они замечательные люди и не поперли меня с,работы, пока я этот диплом писал. И конечно же Наталье Белоголовцевой;
 Я.Андерсону за ""Jethro Tull"", Д.Моррисону за ""Doors"", И.С.Баху за второй,бранденбургский концерт, и группе ""Барышня и хулиган"" за ""Водопад"", ибо без них я бы конечно ничего не написал;
 Всем тем, кого я обязательно хотел включить в этот список, но в последний моментзабыл, а также всем, кого я в этот список включить не смог;
 Всем участникам эхоконференции FIDO obec.pactet, а также ru.coffee.club,mo.sysoeff и ru.drugs;
 Некоторым участникам ru.duel.rhyme, которые так или иначе убедили меня в том,что моя программа пишет просто замечательные стихи;
 Моему боссу /313 Берковичу Сергею за то, что мой адрес все еще 2:5020/313.8,или, как говорят в Интернете, lleo@p8.f313.n5020.z2.gate.phantom.ru, куда,всячески следует направлять отзывы о данной программе.
 Всему прогрессивному человечеству;
                       Леонид Каганов, 6 июня 1996 6:30
'''

def usageOldMsg():
    print(oldMsg1)
    input("Press Enter to continue...")
    print(oldMsg2)
    input("Press Enter to continue...")
    print(oldMsg3)
    exit()

def usage():    
    print(newMsg)
    exit()
         