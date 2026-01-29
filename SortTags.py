import os, sys
import traceback
import sqlite3
from rich import print as rpn

__author__ = 't.me/dokin_sergey'
__version__ = '1.5.-2'
__verdate__ = '2025-08-02 14:03'
########################################################################################################################
if (debug := bool(sys.argv[1]) if len(sys.argv) > 1  else False):
    rpn(f'debug is [orange_red1]{debug}')
SQLiteBase:str = f"{os.environ['APPDATA']}\\foobar2000-v2\\configuration\\foo_sqlite.user.db"
# r"C:/Users/dokin/AppData/Roaming/foobar2000/configuration/foo_sqlite.user.db"
#pylint: disable-msg=W0602
ListTrack:dict[int,int] = {}
rpn(f'База {SQLiteBase}')
#######################################################################################################################
def SQLiteRead() ->bool:
    global ListTrack
    _res = False
    try:
        with sqlite3.connect(SQLiteBase) as _conn:
            _cursor = _conn.cursor() # основной и 1-го курсор
            _SQLTxt = "Select Id_DP, NewTrack from CurPlaylist;"
            _cursor.execute(_SQLTxt)
            _crsr = _cursor.fetchall()
            for itm in _crsr:
                ListTrack[int(itm[0])] = int(itm[1])
    except sqlite3.Warning as Warn:
        rpn(f'\t[red1]{Warn}')
    except sqlite3.Error as DErr:
        rpn(f'\t[red1]{DErr}')
    else:
        _res = True
    finally:
        _conn.close()
    return _res
#######################################################################################################################
def SQLiteUpdate(IdTrack: int, NewNumTrakc: int) ->None:
    try:
        with sqlite3.connect(SQLiteBase) as conn:
        # conn = sqlite3.connect( SQLiteBase )
            conn.execute("Update CurPlaylist Set NewTrack = ? Where Id_DP = ? ;", (NewNumTrakc, IdTrack))
            conn.commit()
    except sqlite3.Warning as Warn:
        rpn(f'\t[red1]{Warn}')
    except sqlite3.Error as DErr:
        rpn(f'\t[red1]{DErr}')
#######################################################################################################################
def NewStep (IdTrack: int, OldStp: int, ArtStp: int, GrStp: int,dbg:bool = False) ->int:
    res = 0
    # rpn(f'{IdTrack = } {CurTrk =} {OldStp = } {ArtStp = } {GrStp = }')
    try: # парт намба 1. Начинаем с предыдушего, если занято шагаем по GrStep
        if not (CurTrk := OldStp + ArtStp * GrStp): CurTrk = 1
        # rpn(f'{IdTrack  = :4} {CurTrk    = :4} {OldStp  = :4} {ArtStp    = :4} {GrStp = :4}\n')
        while CurTrk <= AllCount : # первое условие, вмещаемся, проверяем на занятость
            if ListTrack[CurTrk] == 0:
                ListTrack[CurTrk] = IdTrack
                res = CurTrk
                break
            CurTrk += GrStp
            rpn(f'\t {CurTrk    = :4} {OldStp  = :4} {ArtStp    = :4} {GrStp = :4}')
        # else:
            # for ns in range(ArtStp + 1, 1,-1): # пытаемся впихнуть деля шаг пополам от текущего значения
                # CurTrk = OldStp + GrStp * ns //2   # С нормальным шагом не нашли, нужно уменьшить шаг
                # # rpn(f'Не нашли Но пробуем {CurTrk = } {ns = } {ListTrack[CurTrk] =}')
                # while CurTrk <= AllCount :
                    # if ListTrack[CurTrk] == 0:
                        # ListTrack[CurTrk] = IdTrack
                        # res = CurTrk
                        # break
                    # CurTrk += GrStp * ns //2
                # if res: break
    except Exception as ErrMs:
        rpn ('except:', str(ErrMs), IdTrack, CurTrk )
        rpn(traceback.format_exc())
    if dbg:rpn(f'\t\t[khaki1]{IdTrack = } {OldStp = } {ArtStp = } {GrStp = } {res = }')
    return res
#######################################################################################################################
def FirstFreeList(FF:int, FFStp:int,dbg:bool = False) ->int:
    res = 0
    fi = len(ListTrack) + 1
    try:
        while FFStp:
            if dbg:rpn(f'[yellow1]{fi = } {FFStp = }')
            for k in range(FF, fi, FFStp):
                if dbg:rpn(f'[orange1]{k = } {ListTrack[k] = }')
                if ListTrack[k] == 0:
                    res = k
                    break
            else:
                FFStp = int(FFStp/2)
            if res:break
    except Exception as ErrMs:
        rpn(f'except:{ErrMs}')
        rpn(f'[cyan3]\t {FF = } {FFStp = } {fi = }')
        if k:rpn(f'[cyan3]\t {k = } {ListTrack[k] = }')
        rpn(traceback.format_exc())
        input(':-)> ')
    return res
#**************************************************************************************************************************
if __name__ == '__main__':
    debug = False
    rpn(f'[cyan1]Сортировка Музыкальных сборников ver.[green1]{__version__} SQL Lite [green1]{sqlite3.sqlite_version}')
    if debug:rpn(f'[orchid]Режим отладки {debug}')
    try:
        if not SQLiteRead():raise OSError
        # rpn(ListTrack.items())
        # input(' :-)> ')
        with sqlite3.connect(SQLiteBase) as MusBase:
            cursor1 = MusBase.cursor() # основной и 1-го курсор
            SQLTxt = "SELECT distinct AllCount, EnRuCount FROM CurPlaylist order by Locale"
            cursor1.execute(SQLTxt)
            crsr = cursor1.fetchall()
        AllCount = crsr[0][0]   # общее количество треков
        # ListTrack = dict((x,0) for x in range(1, AllCount + 1)) # Список для проверки трек занят/свободен
        EnCount = crsr[0][1]    # En количество треков
        RuCount = crsr[1][1]    # Ru количество треков
                            # шаг групп треков = 4?
        GroupStep = int(round(EnCount/RuCount,0)) + 1 if EnCount/RuCount > 1 else int(round(RuCount/EnCount,0)) + 1
        GroupCount = int(round(AllCount/GroupStep,0))# количество групп треков
        FirsTrack  = GroupStep # Текущий новый номер трека, начальное значение AND Artist = 'Fancy'
        rpn(f'{EnCount =} {EnCount = } {RuCount =} {GroupCount =} {GroupStep  =} {AllCount = }')
        SQLTxt = "SELECT Distinct ArtSort, ArtCount FROM CurPlaylist Where Locale = 'En' ORDER BY ArtCount Desc;"
        CounTrc = 0
        NewTtack = 0
        CurrenTrack = 0
# ***************** первый шаг по автору en ********************************************
        for row in cursor1.execute(SQLTxt):
            Artist = row[0]
            # ArtStep = AllCount/(GroupStep * ArtCount)
            ArtStep = int(round(AllCount/(GroupStep * row[1]),0))
            SQLTxt2 = "SELECT Id_DP, Title, ArtCount  FROM CurPlaylist Where (Locale = 'En') AND (ArtSort = '" + Artist + "') ORDER by Id_DP"
            cursor2 = MusBase.cursor()
            cursor2.execute(SQLTxt2)
            one_res = cursor2.fetchone()
            Id_DP = one_res[0] #ID трека
            # rpn(f'{Id_DP = } {ListTrack[Id_DP] = }')
            # if ListTrack[Id_DP]  :
                # rpn('пропуск')
                # continue
            Title = one_res[1] # Название трека
            ArtCount = one_res[2] #Количество трэк/артист
            FirsTrack = FirstFreeList(FirsTrack, GroupStep )
            rpn(f'E1:{Id_DP = } {FirsTrack = } ArtStep = 0 {GroupStep = }')
            NewTtack = NewStep(Id_DP, FirsTrack, 0, GroupStep)
            rpn(f'1:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = :20}:{Title = }')
            if NewTtack:
                SQLiteUpdate(Id_DP,NewTtack)
                CounTrc += 1
            else:
                rpn(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                # rpn('Ай, ай, авария 1')
                # sys.exit(1)
                raise OSError(('Ай, ай, авария 1'))
 # **************************************************** шаги по кругу по автору en ****************************
            for row2 in cursor2:
                Id_DP = row2[0] #ID трека
                Title = row2[1] # Название трека
                ArtCount = row2[2] # Шаг номера трека в группах ( *4)
                # rpn(f'E2:{Id_DP = :4} {NewTtack = :4} {ArtStep = :4} {GroupStep = :4}')
                if (NewTtack := NewStep(Id_DP, NewTtack, ArtStep, GroupStep)): # шаги от последнего значения
                    rpn(f'2:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                    SQLiteUpdate(Id_DP,NewTtack)
                    CounTrc += 1
                else:
                    if (FirsTrack := FirstFreeList(int(FirsTrack), GroupStep,)):
                        # rpn(f'E3:{Id_DP = :4} {FirsTrack = :4} {ArtStep = :4} {GroupStep = :4}')
                        if (NewTtack := NewStep(Id_DP, FirsTrack, ArtStep, GroupStep)): # повторим тоже самое от первого значения
                            rpn(f'3:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                            SQLiteUpdate(Id_DP,NewTtack)
                            CounTrc += 1
                    else:
                        # rpn()
                        rpn(str(Id_DP).rjust(5),' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                        # rpn('Ай, ай, авария 2')
                        # sys.exit(1)
                        raise OSError(('Ай, ай, авария 2'))
# ****************************************************************************************************
        #raise ('отладка')
        SQLTxt = "SELECT Distinct ArtSort, ArtCount FROM CurPlaylist Where Locale = 'Ru' ORDER BY ArtCount Desc;"
        NewTtack = 0
        CurrenTrack = 1
        FirsTrack = 1
        for row in cursor1.execute(SQLTxt):
            Artist = row[0]
            ArtStep = int(round(AllCount/(GroupStep * row[1]),0))# Шаг номера автора в ГРУППАХ
            if debug:rpn(f'[khaki1]{AllCount = } {GroupStep = } {row[1] = } {ArtStep = }')
            # if debug:rpn(f'{ArtStep = }')
            SQLTxt2 = "SELECT Id_DP, Title, ArtCount  FROM CurPlaylist Where (Locale = 'Ru') and (ArtSort = '" + Artist + "') "
            cursor2 = MusBase.cursor()
            cursor2.execute(SQLTxt2)
            one_res = cursor2.fetchone()
            Id_DP = one_res[0] #ID трека
            Title = one_res[1] # Название трека
            ArtCount = one_res[2] # Шаг номера трека в группах ( *4) нет такого
            FirsTrack = FirstFreeList(FirsTrack, 1) # Текущий новый номер трека, начальное значение
            # rpn(f'E4:{Id_DP = } {FirsTrack = } ArtStep = 0 GroupStep = 1')
            NewTtack = NewStep(Id_DP, FirsTrack, 0, 1,debug)
            rpn(f'4:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
            if NewTtack:
                SQLiteUpdate(Id_DP,NewTtack)
                CounTrc += 1
            else:
                FirsTrack = FirstFreeList(FirsTrack,1)
                # rpn(f'E5:{Id_DP = :4} {FirsTrack = :4} {ArtStep = :4} GroupStep = 1')
                NewTtack = NewStep(Id_DP, FirsTrack, ArtStep,1,debug)
                rpn('Ай, ай, авария 3')
                rpn(f'5:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                rpn(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                rpn('FirsTrack = ',FirsTrack,'CurrenTrack = ',CurrenTrack,'NewTtack = ', NewTtack )
                for i,j in ListTrack.items():
                    rpn(str(i).rjust(4),str(j).rjust(4))
                sys.exit(1)
            for row2 in cursor2:
                Id_DP = row2[0] #ID трека
                Title = row2[1] # Название трека
                ArtCount = row2[2] # Шаг номера трека в группах ( *4)
                # rpn(f'E6:{Id_DP = } {NewTtack = } {ArtStep = } {GroupStep = }')
                NewTtack = NewStep(Id_DP, NewTtack, ArtStep, GroupStep,debug)
                # rpn(f'6:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                if  NewTtack:
                    SQLiteUpdate(Id_DP,NewTtack)
                    CounTrc += 1
                else:
                    FirsTrack = FirstFreeList(FirsTrack, 1)
                    NewTtack = NewStep(Id_DP, FirsTrack, ArtStep, GroupStep) # повторим тоже самое от первого значения
                    # rpn(f'7:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                    if NewTtack:
                        SQLiteUpdate(Id_DP,NewTtack)
                        CounTrc += 1
                    else:
                        NewStep(Id_DP, FirsTrack, ArtStep, GroupStep)
                        NewTtack = NewStep(Id_DP, FirsTrack, 0, 0)
                        # rpn(f'8:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                        if NewTtack:
                            SQLiteUpdate(Id_DP,NewTtack)
                            break
                        rpn(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                        rpn('FirsTrack = ',FirsTrack,'CurrenTrack = ',CurrenTrack,'NewTtack = ', NewTtack )
                        rpn('Ай, ай, авария 4')
                        for i,j in ListTrack.items():
                            rpn(str(i).rjust(4),str(j).rjust(4))
                        break
    except sqlite3.Warning as Warn:
        rpn(f'\t[khaki1]{Warn}')
    except sqlite3.Error as DErr:
        rpn(f'\t[red1]{DErr}')
        rpn(f'\t[red1]{traceback.format_exc()}')
    except Exception as ErrMs:
        rpn(f'\t[orange_red1]{NewTtack}')
        rpn(f'\t[orange_red1]EO:{GroupStep * ArtStep:5}')
        rpn(f'\t[orange_red1]EO:{Artist = }')
        rpn(f'\t[orange_red1]EO:{Title = }')
        rpn(f'\t[orange_red1]EO:{str(ErrMs)}')
        rpn(f'\t[orange_red1]{traceback.format_exc()}')
    finally:
        MusBase.commit()
        MusBase.close()
    rpn()
#-----------------------------------------------------------------
    input('Выход:-> ')
    os._exit(0)
