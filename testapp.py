from flask import Flask, render_template, request, session, redirect, url_for
import random
from datetime import datetime, timedelta
import os
from pytz import utc

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.secret_key = 'vase_tajne_heslo'
app.permanent_session_lifetime = timedelta(minutes=30)

questions = [
    {
        'id': 1,
        'type': 'multiple_choice',
        'text': 'Jaké jsou hodnoty na výstupech klopných obvodů čítače?',
        'image': 'async_counter_t.png',
        'options': [
            '000, 111, 000, 111',
            '000, 111, 110, 101',
            '000, 001, 010, 011',
            '000, 100, 010, 001',
            '000, 001, 010, 100'
        ],
        'correct_answer': '000, 001, 010, 011'
    },
    {
        'id': 2,
        'type': 'text_input',
        'text': 'Převedte binární hodnoty 0111_0011 z BCD kódu do desítkové soustavy.',
        'correct_answer': '73',
        'strict': True
    },
    {
        'id': 3,
        'type': 'multiple_choice',
        'text': 'Jaký je význam textového souboru ".gitignore" v kořenovém adresáři repozitáře?',
        'options': [
            'ignorování typů souborů, které jsou v něm uvedeny',
            'přidat změněné soubory do stage area',
            'specifikuje licenci s jakou lze data použít',
            'inicializovat nový repozitář',
            'soupis chyb a warningů, které se mají během syntézy ignorovat'
        ],
        'correct_answer': 'ignorování typů souborů, které jsou v něm uvedeny'
    },
    {
        'id': 4,
        'type': 'multiple_choice',
        'text': 'Může se výstup stavového automatu Moorova typu měnit i v době mimo aktivní hranu hodinového signálu "clk"?',
        'options': [
            'ne, toto je vlastnost BCD čítačů',
            'ne, vždy jen synchronně s "clk"',
            'ano, ale pouze obsahuje-li ve zpětné vazbě hradlo XNOR nebo XOR',
            'ano, v závislosti na jiném vstupu do kombinační části ve zpětné vazbě',
            'ano, ale pouze je-li tvořen klopnými obvody typu JK'
        ],
        'correct_answer': 'ne, vždy jen synchronně s "clk"'
    },
    {
        'id': 5,
        'type': 'multiple_choice',
        'text': 'Počet LED diod u 7segmentového dipleje je:',
        'options': [
            '5',
            '6',
            '9',
            '7 nebo 8'
        ],
        'correct_answer': '7 nebo 8'
    },
    {
        'id': 6,
        'type': 'multiple_choice',
        'text': 'Jaký online verzovací systém je používán ve cvičeních na počítači?',
        'options': [
            'Nexys A7-50T',
            'GitHub',
            'Subversion',
            'Bitbucket',
            'Vivado',
            'Xilinx'
        ],
        'correct_answer': 'GitHub'
    },
    {
        'id': 7,
        'type': 'multiple_choice',
        'text': 'Výstupy demultiplexoru 1-to-16 obecně tvoří:',
        'options': [
            'kombinaci 16 datových vstupů',
            'osm 1bitových hodnot',
            'minterny selekčních (adresních) vstupů',
            'maxterny selekčních (adresních) vstupů'
        ],
        'correct_answer': 'minterny selekčních (adresních) vstupů'
    },
    {
        'id': 8,
        'type': 'multiple_choice',
        'text': 'Jaký je význam následující syntaxe ve formátu Markdown? ## Some text',
        'options': [
            'špatná syntaxe',
            'nadpis sekce',
            'podtržený text',
            'tučný text',
            'kurzíva'
        ],
        'correct_answer': 'nadpis sekce'
    },
    {
        'id': 9,
        'type': 'multiple_choice',
        'text': 'Jaký je význam následující syntaxe ve formátu Markdown? **Some text**',
        'options': [
            'špatná syntaxe',
            'tučný text',
            'podtržený text',
            'kurzíva',
            'nadpis sekce'
        ],
        'correct_answer': 'tučný text'
    },
    {
        'id': 10,
        'type': 'multiple_choice',
        'text': 'Nechť je aktuální výstupní hodnota S-R latch (NOR) q=0. Jak se bude v čase měnit "q", je-li vstupní posloupnost "s" a "r" následující: s, r = 1, 0 | 0, 0 | 1, 0 | 0, 1',
        'options': [
            '1 | 0 | 1 | 0',
            '1 | 1 | 1 | 0',
            '0 | 0 | 0 | 1',
            '0 | 1 | 0 | 1',
        ],
        'correct_answer': '1 | 1 | 1 | 0'
    },
    {
        'id': 11,
        'type': 'multiple_choice',
        'text': 'Nechť je aktuální výstupní hodnota klopného obvodu JK řízeného hranou (JK-type flip-flop) q=0. Jak se bude v čase měnit "q", je-li vstupní posloupnost "s" a "r" následující: s, r = 0, 0 | 1, 1 | 1, 1 | 0, 0',
        'options': [
            '0 | 1 | 1 | 1',
            '0 | 0 | 1 | 1',
            '0 | 1 | 0 | 0',
            '1 | 0 | 0 | 1',
        ],
        'correct_answer': '0 | 1 | 0 | 0'
    },
    {
        'id': 12,
        'type': 'text_input',
        'text': 'Jaké mintermy obsahuje kombinační funkce y(c,b,a) = /ca + c/ba? Tj. na kterých pozicích jsou v K-mapě "jedničky"?',
        'correct_answer': '1,3,5',
        'strict': True
    },
    {
        'id': 13,
        'type': 'text_input',
        'text': 'Převedte dekadickou hodnotu 34,5 do binární soustavy. Použijte právě 6 bitů pro celočíselnou část a 2 bity pro desetinnou, tj. např. 101010.11',
        'correct_answer': '100010.10',
        'strict': True
    },
    {
        'id': 14,
        'type': 'text_input',
        'text': 'Kolik řádků a sloupců obsahuje pravdivostní tabulka pro logickou funkci y(c,b,a) = /cba + /b/a? Počítejte pouze vstupní a výstupní hodnoty, tj. nikoliv hlavičku tabulky. Odpovězte ve tvaru počet_řádků x počet_sloupců, např. 5x7 pro 5 řádků a 7 sloupců.',
        'correct_answer': '8 x 4',
        'strict': True
    },
    {
        'id': 15,
        'type': 'text_input',
        'text': 'Napište koncenzus (extra term), který zamaskuje hazard ve funkci y(c,b,a) = (b+a) . (c+/b). V odpovědi nepoužívejte mezery a z logických operací použijte pouze + (plus) a negaci / (lomítko), jako např.: b+/a',
        'correct_answer': 'c+a',
        'strict': True
    },
    {
        'id': 16,
        'type': 'multiple_choice',
        'text': 'Podmínkou vzniku statického hazardu v jedničce jsou: (špatné odpovědi budou penalizovány)',
        'options': [
            'hradlo AND nebo NOR / AND or NOR gate',
            'dvě paralelní větve (x, /x) / two parallel branches (x, /x)',
            'hradlo OR nebo NAND / OR or NAND gate',
            'jedna větev (/x) / one branch (/x)'
        ],
        'correct_answer': ['dvě paralelní větve (x, /x) / two parallel branches (x, /x)', 'hradlo OR nebo NAND / OR or NAND gate'],
        'multi_correct': True  # Indicates multiple correct options
    },
{
        'id': 17,
        'type': 'text_input',
        'text': 'Převedte binární hodnoty 0101_0100 z BCD kódu do desítkové soustavy.',
        'correct_answer': '54',
        'strict': True
    },
    {
        'id': 18,
        'type': 'multiple_choice',
        'text': 'Může se výstup stavového automatu Mealyho typu měnit i v době mimo aktivní hranu hodinového signálu "clk"?',
        'options': [
            'ano, ale pouze při synchronním resetu',
            'ano, v závislosti na jiném vstupu do kombinační části ve zpětné vazbě',
            'ne, toto je možné pouze u Moorova typu',
            'ne, vždy jen synchronně s hodinovým signálem "clk"',
            'ano, je-li tvořen klopnými obvody typu D'
        ],
        'correct_answer': 'ano, v závislosti na jiném vstupu do kombinační části ve zpětné vazbě'
    },
    {
        'id': 19,
        'type': 'multiple_choice',
        'text': 'Pro asynchronní sekvenční systém platí, že:',
        'options': [
            've zpětné vazbě vždy obsahuje hradlo XNOR',
            'neobsahují žádný hodinový signál "clk"',
            'hodinový signál lze šířit z výstupu jednoho klopného obvodu do vstupu druhého',
            'nelze jej sestavit z klopných obvodů T nebo JK',
            'maximální frekvence je vždy stejná jako u synchronních sekvenčních systémů'
        ],
        'correct_answer': 'hodinový signál lze šířit z výstupu jednoho klopného obvodu do vstupu druhého'
    },
    {
        'id': 20,
        'type': 'multiple_choice',
        'text': 'Vstupní signál "en" u Gated latch způsobuje:',
        'options': [
            'synchronizuje obvod na nástupnou hranu clk',
            'zabraňuje vzniku metastability',
            'transparentně přenáší vstup na výstup',
            'povolení činnosti následného SR latche'
        ],
        'correct_answer': 'povolení činnosti následného SR latche'
    },
    {
        'id': 21,
        'type': 'multiple_choice',
        'text': 'Statický hazard v jedničce se může projevit impulzem do úrovně:',
        'options': [
            'zůstane vždy konstantní / it always remains constant',
            'záleží na funkci / depends on the function',
            '0'
        ],
        'correct_answer': '0'
    },
    {
        'id': 22,
        'type': 'multiple_choice',
        'text': 'Jak lze sestavit invertor z hradla NAND?',
        'options': [
            'jeden vstup musí být v 0',
            'vzájemným propojením vstupů',
            'nelze',
            's NAND nelze, musí být hradlo AND'
        ],
        'correct_answer': 'vzájemným propojením vstupů'
    },
    {
        'id': 23,
        'type': 'text_input',
        'text': 'Jaké minterny obsahuje kombinační funkce y(c,b,a) = c/b + b/a? Tj. na kterých pozicích jsou v K-mapě "jedničky"? Indexy minternů oddělujte čárkou a mezerou v vzestupném pořadí např. takto: 1, 2, 3, 7',
        'correct_answer': '2, 4, 5, 6', '2,4,5,6'
        'strict': True
    },
    {
        'id': 24,
        'type': 'text_input',
        'text': 'Převedte binární hodnotu 0b0101_1011 do desítkové soustavy.',
        'correct_answer': '91',
        'strict': True
    },
    {
        'id': 25,
        'type': 'text_input',
        'text': 'Logický výraz s maxtermy y(c,b,a) = M1 . M6 zapíšte pomocí vstupních proměnných. Pro operaci OR použijte + (plus) pro operaci AND . (tečku) a pro negaci / (lomítko). Funkci zapíšte ve tvaru bez mezer např. takto: y(c,b,a)=(/c+/b+/a).(c+b+a)',
        'correct_answer': 'y(c,b,a)=(c+b+/a).(/c+/b+a)',
        'strict': True
    },
    {
        'id': 26,
        'type': 'multiple_choice',
        'text': 'VHDL patří mezi:',
        'options': [
            'hardware description languages',
            'interpretované jazyky',
            'ultra high definition languages',
            'nelze určit',
            'románské jazyky'
        ],
        'correct_answer': 'hardware description languages'
    },
    {
        'id': 27,
        'type': 'multiple_choice',
        'text': 'Jaké jsou hodnoty na výstupech klopných obvodů synchronního čítače z obrázku pro následující 3 periody "clk". Nechť jsou aktuální hodnoty q2q1q0 = 100.',
        'image': 'sync_counter.png',  # Assuming the image is named 'sync_counter.png'
        'options': [
            '100, 101, 110, 111',
            '100, 110, 111, 011',
            '100, 110, 111, 000',
            '100, 011, 010, 001',
            '100, 010, 011, 001'
        ],
        'correct_answer': '100, 110, 111, 011'
    },
    {
        'id': 28,
        'type': 'multiple_choice',
        'text': 'Dvojkový doplněk (two\'s complement) pro vytvoření opačného čísla se vypočte:',
        'options': [
            'negací všech bitů a přičtením hodnoty 1',
            'použitím kaskády 4 plných sčítaček',
            'použitím dvou polovičních sčítaček (half adder)',
            'negací všech bitů a odečtením hodnoty 1'
        ],
        'correct_answer': 'negací všech bitů a přičtením hodnoty 1'
    },
    {
        'id': 29,
        'type': 'multiple_choice',
        'text': 'Statický hazard v nule se může projevit impulzem do úrovně:',
        'options': [
            '0',
            'záleží na funkci / depends on the function',
            'zůstane vždy konstantní / it always remains constant',
            '1'
        ],
        'correct_answer': '1'
    },
    {
        'id': 30,
        'type': 'multiple_choice',
        'text': 'Pro reset klopného obvodu řízeného hranou (flip-flop) NEplatí, že:',
        'options': [
            'vynuluje hlavní výstup obvodu',
            'obvod lze resetovat pouze synchronně',
            'asynchronní reset má větší prioritu než hodinový signál',
            'podle vnitřního provedení, může být synchronní nebo asynchronní'
        ],
        'correct_answer': 'obvod lze resetovat pouze synchronně'
    },
    {
        'id': 31,
        'type': 'multiple_choice',
        'text': 'Jaký je význam příkazu "git pull"?',
        'options': [
            'nahrát veškeré modifikace ze stage area na vzdálený repozitář',
            'inicializovat nový repozitář',
            'přidat změněné soubory do stage area',
            'stáhnout veškeré modifikace ze vzdáleného repozitáře',
            'naklonovat vzdálený repozitář, včetně všech souborů a historie'
        ],
        'correct_answer': 'stáhnout veškeré modifikace ze vzdáleného repozitáře'
    },
    {
        'id': 32,
        'type': 'multiple_choice',
        'text': 'Pomocí jednotlivých hradel je vhodné sestavovat:',
        'options': [
            'pouze logické funkce v úplném součtovém tvaru SoP',
            'pouze logické funkce v úplném součtovém tvaru PoS',
            'pouze jednoduché funkce',
            'mikroprocesory'
        ],
        'correct_answer': 'pouze jednoduché funkce'
    },
    {
        'id': 33,
        'type': 'multiple_choice',
        'text': 'Karnaughova mapa pro kombinační funkci y(c,b,a) = /ca + c/a + cba má rozměry?',
        'options': [
            '4x4',
            '2x4',
            'nelze určit / cannot be determined',
            '2x2'
        ],
        'correct_answer': '2x4'
    },
    {
        'id': 34,
        'type': 'multiple_choice',
        'text': 'Jaké sekvenční prvky nemůže obsahovat asynchronní binární čítač?',
        'options': [
            'JK flip-flop',
            'T flip-flop',
            'D flip-flop',
            'D latch'
        ],
        'correct_answer': 'D latch'
    },
    {
        'id': 35,
        'type': 'multiple_choice',
        'text': 'Pro reset klopného obvodu řízeného hranou (flip-flop) NEplatí, že:',
        'options': [
            'asynchronní reset má větší prioritu než hodinový signál',
            'vynuluje hlavní výstup obvodu',
            'obvod lze resetovat pouze synchronně',
            'podle vnitřního provedení, může být synchronní nebo asynchronní'
        ],
        'correct_answer': 'obvod lze resetovat pouze synchronně'
    },
    {
        'id': 36,
        'type': 'multiple_choice',
        'text': 'Reset v následujícím procesu je:\n\np_reset : process(clk)\nbegin\n    if falling_edge(clk) then\n    if (reset = \'1\') then\n    ...',
        'options': [
            'synchronní, reaguje na vysokou úroveň',
            'asynchronní, reaguje na vysokou úroveň',
            'špatně zapsán',
            'asynchronní, reaguje na nízkou úroveň',
            'synchronní, reaguje na nízkou úroveň'
        ],
        'correct_answer': 'synchronní, reaguje na vysokou úroveň',
        'code_snippet': True  # Flag indicating the question contains code
    },
    {
        'id': 37,
        'type': 'multiple_choice',
        'text': 'Jaké sekvenční prvky nemůže obsahovat asynchronní binární čítač?',
        'options': [
            'JK flip-flop',
            'T flip-flop',
            'D flip-flop',
            'D latch'
        ],
        'correct_answer': 'D latch'
    },
    {
        'id': 38,
        'type': 'multiple_choice',
        'text': 'Podmínkou vzniku statického hazardu v nule jsou: (špatné odpovědi budou penalizovány)',
        'options': [
            'hradlo OR nebo NAND / OR or NAND gate',
            'jedna větev (/x) / one branch (/x)',
            'hradlo AND nebo NOR / AND or NOR gate',
            'dvě paralelní větve (x, /x) / two parallel branches (x, /x)'
        ],
        'correct_answer': ['dvě paralelní větve (x, /x) / two parallel branches (x, /x)', 'hradlo AND nebo NOR / AND or NOR gate'],
        'multi_correct': True
    },
    {
        'id': 39,
        'type': 'multiple_choice',
        'text': 'Výstupy dekodéru 4-to-16 obecně tvoří:',
        'options': [
            'maxtermy vstupních hodnot',
            'mintermy vstupních hodnot',
            'jedinou hodnotu ze 16 datových vstupů',
            'osm 1-bitových hodnot'
        ],
        'correct_answer': 'mintermy vstupních hodnot'
    },
    {
        'id': 40,
        'type': 'multiple_choice',
        'text': 'Označení Common Cathode u 7-segmentového displeje znamená, že segmenty svítí pro vstupní hodnoty:',
        'options': [
            '0',
            '1',
            'nelze určit'
        ],
        'correct_answer': '1'
    },
    {
        'id': 41,
        'type': 'multiple_choice',
        'text': 'Po použití De Morganova pravidla na logickou funkci y(c,b,a) = a/b/c dostaneme:',
        'options': [
            'y(c,b,a) = /(a+b+c)',
            'y(c,b,a) = /(a/bc)',
            'y(c,b,a) = /(a+/b+c)'
        ],
        'correct_answer': 'y(c,b,a) = /(a+b+c)'
    },
    {
        'id': 42,
        'type': 'multiple_choice',
        'text': 'Vnitřní popis modulu se ve VHDL definuje pomocí:',
        'options': [
            'entity',
            'architecture',
            'port',
            'leee',
            'nelze určit'
        ],
        'correct_answer': 'architecture'
    },
    {
        'id': 43,
        'type': 'multiple_choice',
        'text': 'Nechť je aktuální výstupní hodnota klopného obvodu D řízeného hranou (D-type flip-flop) q=0. Jak se bude v čase měnit "q", je-li vstupní posloupnost "d" při náběžných hranách "clk" následující: d = 0 | 1 | 1 | 0',
        'options': [
            '0 | 0 | 1 | 1',
            '1 | 0 | 0 | 1',
            '0 | 1 | 1 | 0',
            '0 | 1 | 1 | 1'
        ],
        'correct_answer': '0 | 1 | 1 | 0'
    },
    {
        'id': 44,
        'type': 'multiple_choice',
        'text': 'Určete zda logická funkce obsahuje statický hazard: y(c,b,a) = c/b + b/a',
        'options': [
            'při změně "b" / when changing "b"',
            'při změně "a" / when changing "a"',
            'při změně "c" / when changing "c"',
            'nelze rozhodnout / cannot be decided'
        ],
        'correct_answer': 'při změně "b" / when changing "b"'
    },
    {
        'id': 45,
        'type': 'multiple_choice',
        'text': 'Jak lze sestavit invertor z hradla NOR?',
        'options': [
            'jeden vstup musí být v 1',
            'nelze',
            's NOR nelze, musí být hradlo OR',
            'vzájemným propojením vstupů'
        ],
        'correct_answer': 'jeden vstup musí být v 1'
    },
    {
        'id': 46,
        'type': 'multiple_choice',
        'text': 'Podmínkou vzniku dynamického hazardu jsou: (špatné odpovědi budou penalizovány)',
        'options': [
            'nepřítomnost statického hazardu / absence of static hazard',
            'tři paralelní větve / three branches',
            'přítomnost statického hazardu / presence of static hazard',
            'dvě paralelní větve (x, /x) / two parallel branches (x, /x)'
        ],
        'correct_answer': ['tři paralelní větve / three branches', 'přítomnost statického hazardu / presence of static hazard'],
        'multi_correct': True
    },
    {
        'id': 47,
        'type': 'multiple_choice',
        'text': 'Vstupní signál "en" u Gated latch způsobuje:',
        'options': [
            'transparentně přenáší vstup na výstup',
            'synchronizuje obvod na nástupnou hranu clk',
            'zabraňuje vzniku metastability',
            'povolení činnosti následného SR latche'
        ],
        'correct_answer': 'povolení činnosti následného SR latche'
    },
    {
        'id': 48,
        'type': 'multiple_choice',
        'text': 'Může se výstup stavového automatu Mealyho typu měnit i v době mimo aktivní hranu hodinového signálu "clk"?',
        'options': [
            'ne, toto je možné pouze u Moorova typu',
            'ano, je-li tvořen klopnými obvody typu D',
            'ano, ale pouze při synchronním resetu',
            'ano, v závislosti na jiném vstupu do kombinační části ve zpětné vazbě',
            'ne, vždy jen synchronně s hodinovým signálem "clk"'
        ],
        'correct_answer': 'ano, v závislosti na jiném vstupu do kombinační části ve zpětné vazbě'
    },
    {
        'id': 49,
        'type': 'multiple_choice',
        'text': 'Jak se jmenují vývojová prostředí, která používáte ve cvičeních na počítači? (Výběr špatné odpovědi je penalizován.)',
        'options': [
            'Vivado',
            'Quartus',
            'VHDL',
            'Xilinx ISE',
            'EDA Playground',
            'Xilinx'
        ],
        'correct_answer': ['Vivado', 'Xilinx ISE'],
        'multi_correct': True
    },
    {
        'id': 50,
        'type': 'multiple_choice',
        'text': 'Vývojová deska, používaná v počítačových cvičení se jmenuje:',
        'options': [
            'Arduino Uno',
            'CoolRunner-II',
            'Nexys A7-50T',
            'Arty A7'
        ],
        'correct_answer': 'Nexys A7-50T'
    },
    {
        'id': 51,
        'type': 'multiple_choice',
        'text': 'Sčítačka tří 1bitových signálů se nazývá:',
        'options': [
            'odčítačka',
            'hradlo AND',
            'poloviční sčítačka / half adder',
            'plná sčítačka / full adder'
        ],
        'correct_answer': 'plná sčítačka / full adder'
    },
    {
        'id': 52,
        'type': 'multiple_choice',
        'text': 'Multiplexor 4-to-1 obsahuje 4 datové vstupy i3, i2, i1, i0 a dva selekční vstupy s1, s0. Jaká rovnice popisuje funkci tohoto multiplexoru?',
        'options': [
            'f = i0s1s0 + i1s1/s0 + i2/s1s0 + i3/s1/s0',
            'jiná funkce',
            'f = i3s1s0 + i2s1/s0 + i1/s1s0 + i0/s1/s0',
            'nelze jej popsat logickou funkcí'
        ],
        'correct_answer': 'f = i3s1s0 + i2s1/s0 + i1/s1s0 + i0/s1/s0'
    },
    {
        'id': 53,
        'type': 'multiple_choice',
        'text': 'Přítomnost výrazu (x+/x).x indikuje:',
        'options': [
            'statický hazard v 0 / static-0 hazard',
            'nepřítomnost hazardu, protože (x+/x).x = x / absence of hazard because (x+/x).x = x',
            'dynamický hazard / dynamic hazard',
            'nelze rozhodnout / cannot be decided'
        ],
        'correct_answer': 'statický hazard v 0 / static-0 hazard'
    },
    {
        'id': 54,
        'type': 'multiple_choice',
        'text': 'Pro klopný obvod řízený hranou vždy platí, že:',
        'options': [
            'může v něm nastat metastabilní stav',
            'obsahuje dvojici sekvenčních obvodů reagující na úroveň',
            'není vždy potřeba hodinový signál',
            'reaguje na vysokou úroveň řídícího signálu'
        ],
        'correct_answer': 'může v něm nastat metastabilní stav'
    },
    {
        'id': 55,
        'type': 'multiple_choice',
        'text': 'Pro synchronní sekvenční systém platí, že:',
        'options': [
            'hodinový signál může být šířen z jednoho klopného obvodu do druhého',
            'nemá hodinový signál "clk"',
            'vždy obsahuje hradlo XOR ve zpětné vazbě',
            'může obsahovat asynchronní nebo synchronní reset',
            'nelze jej sestavit z klopných obvodů typu D ani JK'
        ],
        'correct_answer': 'může obsahovat asynchronní nebo synchronní reset'
    }
]

def init_session(mode):
    session.clear()
    session['mode'] = mode
    session['current_question'] = 0
    session['score'] = 0
    session['start_time'] = datetime.now(utc)
    session['time_limit'] = 900  # 15 minut
    session['user_answers'] = {}

    if mode == 'test':
        question_ids = random.sample(range(len(questions)), min(8, len(questions)))
    else:
        question_ids = list(range(len(questions)))

    random.shuffle(question_ids)
    session['question_ids'] = question_ids

@app.route('/')
def index():
    return render_template('mode_selection.html')

@app.route('/start/<mode>')
def start(mode):
    if mode not in ['test', 'drill']:
        return redirect(url_for('index'))
    init_session(mode)
    return redirect(url_for('question', qid=0))

@app.route('/question/<int:qid>')
def question(qid):
    if 'question_ids' not in session:
        return redirect(url_for('index'))

    elapsed = datetime.now(utc) - session['start_time']
    if session['mode'] == 'test' and elapsed.total_seconds() > session['time_limit']:
        session['completed'] = True
        return redirect(url_for('results'))

    if qid < 0 or qid >= len(session['question_ids']):
        return redirect(url_for('question', qid=session['current_question']))

    session['current_question'] = qid
    question = questions[session['question_ids'][qid]]
    user_answer = session['user_answers'].get(str(qid), '')

    return render_template('question.html',
                           question=question,
                           qid=qid,
                           total=len(session['question_ids']),
                           mode=session['mode'],
                           time_left=max(0, int(session['time_limit'] - elapsed.total_seconds())),
                           user_answer=user_answer)

@app.route('/check', methods=['POST'])
def check():
    if 'question_ids' not in session:
        return redirect(url_for('index'))

    qid = session['current_question']
    question = questions[session['question_ids'][qid]]
    
    if question.get('multi_correct', False):
        user_answer = ';'.join(request.form.getlist('answer'))
    else:
        user_answer = request.form.get('answer', '').strip()
    
    session['user_answers'][str(qid)] = user_answer

    if question['type'] == 'multiple_choice':
        if question.get('multi_correct', False):
            user_answers = set(user_answer.split(';')) if user_answer else set()
            correct_answers = set(question['correct_answer'])
            is_correct = user_answers == correct_answers
        else:
            is_correct = (user_answer == question['correct_answer'])
    elif question['type'] == 'text_input':
        correct = question['correct_answer']
        is_correct = user_answer == correct if question.get('strict', False) else user_answer.lower() == correct.lower()
    else:
        is_correct = False

    if is_correct and session['mode'] == 'test':
        session['score'] += 1

    if session['mode'] == 'drill' and not is_correct:
        return render_template('question.html',
                           question=question,
                           qid=qid,
                           total=len(session['question_ids']),
                           mode=session['mode'],
                           show_feedback=True,
                           is_correct=is_correct,
                           correct_answer=question['correct_answer'],
                           user_answer=user_answer)
    else:
        next_qid = qid + 1
        if next_qid >= len(session['question_ids']):
            session['completed'] = True
            return redirect(url_for('results'))
        return redirect(url_for('question', qid=next_qid))

@app.route('/review')
def review():
    if 'question_ids' not in session or not session.get('completed', False):
        return redirect(url_for('index'))

    questions_with_answers = []
    for i, qid in enumerate(session['question_ids']):
        q = questions[qid]
        user_ans = session['user_answers'].get(str(i), '')
        correct = q['correct_answer']
        
        if q.get('multi_correct', False):
            user_answers = set(user_ans.split(';')) if user_ans else set()
            correct_answers = set(correct)
            is_correct = user_answers == correct_answers
        elif q.get('strict', False):
            is_correct = user_ans == correct
        else:
            is_correct = user_ans.lower() == correct.lower() if isinstance(correct, str) else user_ans == correct
        
        questions_with_answers.append({
            'question': q,
            'user_answer': user_ans,
            'is_correct': is_correct
        })

    elapsed = datetime.now(utc) - session['start_time']
    minutes, seconds = divmod(int(elapsed.total_seconds()), 60)

    return render_template('review.html',
                           questions=questions_with_answers,
                           score=session['score'],
                           total=len(session['question_ids']),
                           time_spent=f"{minutes} min. {seconds} sek.")

@app.route('/results')
def results():
    if 'question_ids' not in session or session['mode'] != 'test':
        return redirect(url_for('index'))

    elapsed = datetime.now(utc) - session['start_time']
    minutes, seconds = divmod(int(elapsed.total_seconds()), 60)

    return render_template('results.html',
                           score=session['score'],
                           total=len(session['question_ids']),
                           time_spent=f"{minutes} min. {seconds} sek.")

@app.route('/end_session')
def end_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)