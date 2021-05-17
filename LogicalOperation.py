from sys import exit
ERROR_MESSAGE = ['間違った倫理式', '"）" か "（" が足りない']
LOGICAL_SYMBOL = ['&&', '||', '->', '==']
TRUE_VALUE = ['t', 'true']
FALSE_VALUE = ['f', 'false']
HELP_MESSAGE = '''-------------------------------------
命令と論理式を入力してください
このプログラミングで論理演算子"¬, ∧, ∨, →, ≡"を"!, &&, ||, ->, =="で取り扱う
0がfalseで，0以外の数字はTrueとする
基本命題はアルファベットと数のみ許される
命令は以下となる
exit()                  終了する

ope [exps]              論理式を計算する
istauto [flag] [exps]   トートロジー判定

        flag:
                -all    真理分析表をすべて表示
                -f      falseとなる場合のみ'''


# 入力エラーを弾く
def error_exit(code):
    print('error：', ERROR_MESSAGE[code])
    exit(1)


# 倫理式を倫理記号と括弧で区切って，その要素をリストに入れる
def format_exps(exps):
    # 論理演算子が空の場合はエラー
    if exps == '':
        print('error：間違った倫理式')
        exit(1)

    formatted = []  # returnするリスト
    symbl_index = []  # 括弧と倫理記号のindex
    exps = str(exps).lower().replace(' ', '')  # 全部小文字に，スベースを除去
    le = len(exps)
    # 倫理記号のindexを探す
    for i in range(le):
        if exps[i:i + 2] in LOGICAL_SYMBOL:
            # 論理演算子の前か後ろに命題をがない場合，エラー
            if i == 0 or i == le - 2:
                error_exit(0)
            elif (exps[i + 2] == '!' and
                  (exps[i + 3] == '!' or exps[i + 3:i + 5] in LOGICAL_SYMBOL)
                  ) or exps[i + 2:i + 4] in LOGICAL_SYMBOL:
                error_exit(0)

            symbl_index.append(i)
        elif exps[i] == '(' or exps[i] == ')':
            symbl_index.append(i)

    # print(symbl_index)
    # 倫理記号と括弧を区切りに要素をリストに入れる
    start_index = 0
    for end_index in symbl_index:
        if exps[end_index] == '(':
            formatted.append(exps[end_index])
            start_index = end_index + 1
        elif exps[end_index] == ')':
            if start_index != end_index:
                formatted.append(exps[start_index:end_index])
            formatted.append(exps[end_index])
            start_index = end_index + 1
        elif start_index == end_index:
            start_index = end_index + 2
            formatted.append(exps[end_index:start_index])
        else:
            formatted.append(exps[start_index:end_index])
            start_index = end_index + 2
            formatted.append(exps[end_index:start_index])
    else:
        if start_index < le:
            formatted.append(exps[start_index:])

    # 個々の基本命題はアルファベットと数字以外で構成している場合，エラー
    for i in formatted:
        if i[0] == '!':
            i = i[1:]
        if not i.isalnum:
            error_exit(0)

    return formatted


# 文字列を真理値に変える
def str_to_bool(exps):
    # notがついているかどうかを判定
    flag = False
    if exps[0] == '!':
        exps = exps[1:]
        flag = True

    if exps in FALSE_VALUE or exps == '0':
        return_exps = False
    elif exps in TRUE_VALUE or exps != '0':
        return_exps = True

    if flag:
        return not return_exps
    else:
        return return_exps


# ならばの計算
def implication(a, b):
    if a and not b:
        return False
    else:
        return True


# 小倫理式の計算
def min_operate(a, b, symbl):
    if symbl == '&&':
        return a and b
    elif symbl == '||':
        return a or b
    elif symbl == '->':
        return implication(a, b)
    elif symbl == '==':
        return a == b


# 括弧なし論理式の計算
def operate(formatted_exps):
    le = len(formatted_exps)
    if le == 1:
        return str_to_bool(formatted_exps[0])

    t = min_operate(str_to_bool(formatted_exps[0]),
                    str_to_bool(formatted_exps[2]), formatted_exps[1])
    # print('1', t)
    for i in range(3, le - 1, 2):
        # print(t, str_to_bool(formatted_exps[i + 1]), formatted_exps[i])
        t = min_operate(t, str_to_bool(formatted_exps[i + 1]),
                        formatted_exps[i])
        # print(t)

    return t


# 括弧がつく論理式の計算
def operate_with_brackets(formatted_exps):
    while True:
        open_brackets = -1
        close_brackets = -1
        le = len(formatted_exps)
        # 最初の")"を探して，その前にある一番近い"("とカップリングする
        for i in range(le):
            if formatted_exps[i] == '(':
                open_brackets = i
            elif formatted_exps[i] == ')':
                close_brackets = i
                if open_brackets == -1:  # ")"の前に"("がないとき，エラー
                    error_exit(1)
                # 二つの括弧の間の内容を計算する
                t = operate(formatted_exps[open_brackets + 1:close_brackets])
                formatted_exps = formatted_exps[:open_brackets] + [
                    str(t).lower()
                ] + formatted_exps[close_brackets + 1:]
                break

        if open_brackets != -1 and close_brackets == -1:
            # "("の後ろに")"がないとき，エラー
            error_exit(1)
        elif open_brackets == -1 and close_brackets == -1:
            # 括弧がなくなるまで繰り返す
            return operate(formatted_exps)


# 取りうる値をすべてリストアップ
def exhaustion(amount, max):
    t = '0' * amount
    output = [t]
    max = str(max)
    endloop = max * amount

    while t != endloop:
        index = 0
        # max進数が1ずつ増えていくと同じ原理
        # 最初の桁がmaxではないならそれを1増やす
        if t[index] != max:
            t = str(int(t[index]) + 1) + t[index + 1:]
        else:
            # 最初の桁がmaxなら，次のmaxではない数を探しそれを1増やしてその前のすべての桁を0にする(1桁繰り上がる)
            while t[index] == max:
                index += 1
            t = '0' * index + str(int(t[index]) + 1) + t[index + 1:]
        output.append(t)

    return output


# トートロジーがどうかを判定
def is_tautology(formatted_exps, flag):
    formatted_exps = tuple(formatted_exps)
    atomic_proposition = []  # 基本命題の名前を保存
    atomic_proposition_value = {}  # 基本命題の真理値を保存
    maxlen = 0  # 一番長い基本命題の長さ，outputのとき，formatに使う

    # 基本命題を取り出す，値を0にする
    for i in formatted_exps:
        if i not in LOGICAL_SYMBOL and i != '(' and i != ')':
            if i[0] == '!':
                i = i[1:]

            # 数字のみの値は除外
            if i not in atomic_proposition_value and not i.isnumeric():
                atomic_proposition.append(i)
                atomic_proposition_value[i] = '0'
                temp_len = len(i)
                if temp_len > maxlen:
                    maxlen = temp_len

    # 基本命題が一つもない場合，エラー
    if not atomic_proposition:
        error_exit(0)
    # print(atomic_proposition)
    # print(atomic_proposition_value)

    amount = len(atomic_proposition)
    le = len(formatted_exps)
    atomic_proposition_exhaustion = exhaustion(
        amount, 1)  # すべての基本命題において，取りうるすべてパターンを入れる
    formatted_exps_value = []  # 取りうるパターン
    formatted_exps_result = []  # そのパターンに対応する真理値
    is_tautology_result = True  # トートロジーがどうかを保存する変数
    maxlen += 2
    output_value = ''
    formation = '{:^' + str(maxlen) + '}'  # format書式
    for i in atomic_proposition_exhaustion:
        # パターンを一ずつ取り出す
        temp = []
        for j in range(amount):
            atomic_proposition_value[atomic_proposition[j]] = i[j]
            output_value += formation.format(i[j])
            temp.append(i[j])

        # パターンを保存
        formatted_exps_value.append(temp)
        # print(atomic_proposition_value)

        # 取り出したパターンを論理式に代入
        temp_formatted_exps = list(formatted_exps)
        for j in range(le):
            flag1 = False
            if temp_formatted_exps[j][0] == '!':
                temp_formatted_exps[j] = temp_formatted_exps[j][1:]
                flag1 = True

            if temp_formatted_exps[j] in atomic_proposition_value:
                temp_formatted_exps[j] = atomic_proposition_value[
                    temp_formatted_exps[j]]
                if flag1:
                    temp_formatted_exps[j] = '!' + temp_formatted_exps[j]
        t = operate_with_brackets(temp_formatted_exps)  # 代入完了した式を計算
        if not t:  # 一つでもfalseがあるなら，トートロジーではない
            is_tautology_result = False
        # パターンに対応する結果を保存
        formatted_exps_result.append(t)
        output_value += ' ' + str(t) + '\n'

        # print(''.join(temp_formatted_exps))
    # print(formatted_exps_result)
    # formatted_exps_value
    # formatted_exps_result

    # 結果の出力
    if is_tautology_result:
        print(''.join(formatted_exps) + 'はトートロジーである')
    else:
        print(''.join(formatted_exps) + 'はトートロジーではない')

    # flagの応じて計算過程を出力
    output_title = ''
    for i in atomic_proposition:
        output_title += formation.format(i)
    output_title += ' ' + ''.join(formatted_exps) + '\n'
    if flag == 'all':
        output = '\n' + output_title + output_value
        print(output)
    elif flag == 'f':
        output_value = ''
        for i in range(2**amount):
            if not formatted_exps_result[i]:
                for j in formatted_exps_value[i]:
                    output_value += formation.format(j)
                output_value += ' ' + str(formatted_exps_result[i]) + '\n'
        output = '\n' + output_title + output_value
        print(output)


# 最初の注意書き
def start():
    print('''------------------------------------
命令と論理式を入力してください
このプログラミングで論理演算子" ¬ ,  ∧ ,  ∨ ,  → ,  ≡"  を  "!, &&, ||, ->, ==" で取り扱う
You can enter "exit()" to get exit
You can enter "-help" to get help''')
    main()


def main():
    exps = input()
    if exps[:3] == 'ope':
        formatted_exps = format_exps(exps[3:])
        reslut = operate_with_brackets(formatted_exps)
        print(reslut)
    elif exps[:7] == 'istauto':
        behind_command = exps[7:]
        flag = behind_command.find('-', 0, 2)
        if flag == -1:
            formatted_exps = format_exps(behind_command)
            is_tautology(formatted_exps, None)
        elif behind_command[flag + 1] == 'f':
            formatted_exps = format_exps(behind_command[flag + 2:])
            is_tautology(formatted_exps, 'f')
        elif behind_command[flag + 1:flag + 4] == 'all':
            formatted_exps = format_exps(behind_command[flag + 4:])
            is_tautology(formatted_exps, 'all')
        else:
            print(
                'This command does not exist. You can enter "-help" to get help'
            )
    elif exps.find('-help') != -1:
        print(HELP_MESSAGE)
    elif exps == 'exit()':
        exit()
    else:
        print('This command does not exist. You can enter "-help" to get help')
    main()


# ただのテストコード
def test():
    # exps = '!1 ||1 && 1 -> 0 ==1'
    # exps2 = '(!1||(!0&&1))->(0==0)'
    exps3 = '(!q1||(!q2&&w))->q3'
    formatted_exps = format_exps(exps3)
    print(exps3)
    print(formatted_exps)
    is_tautology(formatted_exps, 'f')
    # print(operate_with_brackets(formatted_exps))
    # print('\n'.join(formatted_exps))
    # print(operate(formatted_exps))
    # print(exhaustion(2, 1))
    # t = '0000'
    # t = str(int(t[0]) + 1) + t[0 + 1:]
    # print(t)

    # print(operate(exps))
    # print(exps.lower())
    pass


if __name__ == "__main__":
    # test()
    start()

# 古いバージョンのコード
"""
# 括弧なし論理式の計算(最初のバージョン)
def operate_old(exps):
    exps = str(exps).lower()
    le = len(exps)
    for i in range(le - 2, -1, -1):
        # print(i, exps[i:i + 2])

        # 倫理記号のindexを探す
        if exps[i:i + 2] in LOGICAL_SYMBOL:
            # 論理演算子の前か後ろに真理値をがない場合
            if i == 0 or i == le - 2:
                print('error：間違った倫理式')
                exit(1)

            # 倫理記号とその両辺を取り出す
            a = operate(exps[:i])
            b = str_to_bool(exps[i + 2:])
            symbl = exps[i:i + 2]
            # print(a, ',', symbl, ',', b)
            break
    else:
        return str_to_bool(exps)

    if symbl == '&&':
        return a and b
    elif symbl == '||':
        return a or b
    elif symbl == '->':
        return implication(a, b)
    elif symbl == '==':
        return a == b """
