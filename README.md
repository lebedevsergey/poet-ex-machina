# Poet Ex Machina #

#### see English description below ####

### Что это? ###
* Python-программа, сочиняющая стихи на русском языке
* Основана на алгоритме программы [lleo_dip.exe](https://lleo.me/soft/lleo_dip.htm) написанной Леонидой Кагановым

### Как пользоваться? ###

Используя базу слов от оригинальной программы:
`python lleo_dip.py c ./words/GS.BSY  ./steps/CHASTU.RTM`
####или:####
1. Создать базу слов из текстового файла, например:
`python lleo_dip.py b ./words/tolstoy.words ./examples/texts/tolstoy.txt`
2. После предыдущего шага ударения в словах будут расставлены автоматически, но далеко не всегда корректно. Если хотите расставить в словах ударения вручную, то запускаете программу с ключом `u`:
`python lleo_dip.py u ./words/tolstoy.words ./syll/$$$$SLOG.BSY`
3. Запустить генерацию стихов, указав программе файл с ритмом стихов:
`python lleo_dip.py c ./words/tolstoy.words ./steps/CHASTU.RTM`
4. Ура, теперь вы -- СамСебеПоэт!

### Что еще скажете? ###
* Программа написана под Python 3, для работы ей необходим Python-модуль [click](http://click.pocoo.org)
* Оригинальная программа написана Леонидом Кагановым в  1996 году на x86 Ассемблере, как дипломная работа.
* Алгоритм основан на марковских цепях, стихотворные строфы составляются путем подбора слов с учетом рифм в конце строк, ритма стихов, и предыдущего слова строфы
* В репозиторий включены от оригинальной программы: база слов (words/BS.BSY), база слогов и ударений (syll/$$$$SLOG.BSY), и файлы ритмов стихов (steps/*.RTM). Новая программа умеет загружать базы в оригинальном формате, сохраняя их в новом формате (сериализируя данные через Python pickle)

### Автора!!! ###
* (c) Сергей Лебедев, 2016, программа распространяется на условиях лицензии Apache 2.0
* Cвязаться cо мною можно через:
    * https://habrahabr.ru/users/sunman/
    * http://stackoverflow.com/users/7135046/sergeylebedev
    * https://www.facebook.com/sergei.lebedev.5891 

## English description ##
### What is it? ###
* Python program that composes verses in Russian language
* Based on original [lleo_dip.exe](https://lleo.me/soft/lleo_dip.htm) program by Leonid Kaganov with some additions and improvements

### How to use it? ###
Using original program's words database:
`python lleo_dip.py c ./words/GS.BSY  ./steps/CHASTU.RTM`
####or####
1. Generate words base from text file, like so:
`python lleo_dip.py b ./words/tolstoy.words ./examples/texts/tolstoy.txt`
2. If would like, you can mark words accents manually:
`python lleo_dip.py u ./words/tolstoy.words ./syll/$$$$SLOG.BSY`
3. Generate verses:
`python lleo_dip.py c ./words/tolstoy.words ./steps/CHASTU.RTM`
4. Enjoy!

### What else? ###
* Program requires Python 3.* and Python module [click](http://click.pocoo.org)
* Original program was written in 1996 by Leonid Kaganov in x86 Assembly
* Algorithm composes verses taking in account words rhymes, rhytms and their neighbouring words in texts
* Repository includes files from original program: word database (words/BS.BSY), syllables database (syll/$$$$SLOG.BSY), and verse rhytms files (steps/*.RTM). The program can load old databases, but saves them in new format by serializing data with Python pickle

### Who wrote this? ###
* (c) 2016 Sergey Lebedev, licensed under the Apache License, Version 2.0
* Feel free to contact me at:
    * https://habrahabr.ru/users/sunman/
    * http://stackoverflow.com/users/7135046/sergeylebedev
    * https://www.facebook.com/sergei.lebedev.5891
