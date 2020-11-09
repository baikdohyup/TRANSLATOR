import pickle, os, random

WLPATH = "Data\\WordList.data"
SLPATH = "Data\\SimilarList.data"

TempWordList = open(WLPATH, "rb")
WordList = pickle.load(TempWordList)

TempSimilarList = open(SLPATH, "rb")
SimilarList = pickle.load(TempSimilarList)

SpecialCase = ["튽", "장"], ["푸", "신"], ["숲", "김"]

def Advice():
    print("[Help]")
    print("1 - 1. 야민정음(\"머전\", \"네넴띤\" 등)과 훈민정음(\"대전\", \"비빔면\" 등)을 번역해드립니다.")
    print("2 - 1. 아래 커맨드를 통해 기능을 사용할 수 있습니다.")
    print("3 - 1. 한글 음절 조합을 입력받으면 그로부터 변형될 수 있는 한글 음절 조합 목록을 생성합니다.")
    print("3 - 2. 목록에 단어들이 존재한다면 단어들을, 그렇지 않다면 목록 중 가능성이 높은 3가지를 추천해드립니다.")
    print("4 - 1. 단어 학습은 \"비빔면\"과 같은 평소에 사용하지만 단어사전에는 존재하지 않는 단어를 학습시킬 수 있는 기능입니다.")
    print("4 - 2. 단어를 많이 학습시킬수록 번역이 정확해집니다.")
    print("5 - 1. 야민정음 퀴즈는 랜덤하게 정해진 답 단어를 야민정음으로 번역하여 사용자에게 제시합니다.")
    print("5 - 2. 사용자가 야민정음을 올바르게 답 단어로 번역하여 입력하면 정답입니다.")
    print("5 - 3. 야민정음 퀴즈는 총 5문제이며, 각 문제의 배점은 20점입니다.")
    print("5 - 4. 난이도에 따라 답 단어와 번역된 야민정음의 유사도가 다릅니다.")
    print("6 - 1. 프로그램을 종료하면 학습시킨 단어가 저장되며 이후 프로그램을 다시 실행시켜도 단어를 기억하고 있습니다.")
    print("7 - 1. 화면 정리는 내역을 모두 지워줍니다.")
    print()
    print("[Command]")
    print("/teach : 단어 학습시키기")
    print("/quiz  : 야민정음 퀴즈")
    print("/quit  : 프로그램 종료")
    print("/cls   : 화면 정리")
    print()
    return

def Intro():
    os.system("cls")
    print("◎ 야민정음 번역기 ◎")
    print()
    return

def IsValid(temp):
    for char in temp:
        if not(ord('가')<=ord(char) and ord(char)<=ord('힣')):
            return 0
    return 1

def Teach():
    print("[Command]")
    print("ENTER : 번역기로 돌아가기")
    print()
    while True:
        temp = input("단어 하나를 입력하세요 : ")
        print()
        if temp == "":
            Intro()
            break
        else:
            if IsValid(temp) == 1:
                word = input("단어를 한번 더 입력하세요 : ")
                print()
                if word == temp:
                    if not word in WordList[len(word)]:
                        WordList[len(word)].append(word)
                        WordList[len(word)].sort()
                        print("{} 학습 하였습니다.".format(word))
                        print()
                    else:
                        print("[ERROR] 이미 알고 있는 단어입니다.")
                        print()
                else:
                    print("[ERROR] 입력된 단어가 서로 다릅니다.")
                    print()
                    continue
            else:
                print("[ERROR] 단어가 아닙니다.")
                print()
    return

def Quit():
    SaveWordList = open(WLPATH, "wb")
    SaveSimilarList = open(SLPATH, "wb")
    pickle.dump(WordList, SaveWordList)
    pickle.dump(SimilarList, SaveSimilarList)
    SaveWordList.close()
    SaveSimilarList.close()
    print("종료합니다.")
    print()
    os.system("pause")
    return

def MakeWords(word):
    words = [""]
    for letter in word:
        temp = []
        for char in MakeLetters([letter]):
            for i in words:
                temp.append(i+char)
        words = temp
    return words

def MakeLetters(letters):
    origin = letters[0]
    result = []
    new = letters[:]
    while True:
        count = 0
        for letter in new:
            for similar in SimilarList:
                if letter in similar:
                    for char in similar:
                        if char not in letters and char not in result:
                            result.append(char)
                            count += 1
                if (ord(letter)-ord('가'))//28//21 != 11:
                    ini = (ord(letter)-ord('가'))//28//21
                    modify = chr(ord(letter) + 588 * (11 - ini))
                    if modify in similar:
                        for char in similar:
                            char = chr(ord(char) + 588 * (ini - 11))
                            if char not in letters and char not in result:
                                result.append(char)
                                count += 1
                if (ord(letter)-16)%28 != 0:
                    end = (ord(letter)-16)%28
                    modify = chr(ord(letter) - end)
                    if modify in similar:
                        for char in similar:
                            if (ord(char)-16)%28 ==0:
                                char = chr(ord(char)+end)
                                if char not in letters and char not in result:
                                    result.append(char)
                                    count += 1
        new = result[:]
        letters += result
        result = []
        if count == 0: break
    for Case in SpecialCase:
        if origin in Case:
            for char in Case:
                if char not in letters:
                    letters.append(char)
    return letters

def ExploreDict(words, word):
    results = []
    judge = 0
    for i in words:
        if i in WordList[len(i)]:
            if word != i:
                results.append(i)
                judge = 1
    if judge == 1:
        return (results, judge)
    else:
        return (words, judge)

def ShowResults(word):
    words = MakeWords(word)
    tup = ExploreDict(words, word)
    if tup[1]:
        if len(tup[0]) == 0:
            print("변형될 수 있는 형태가 없습니다.")
        elif len(tup[0]) == 1:
            print("다음 단어와 같이 변형이 가능합니다.")
            print()
            print(tup[0][0])
        else:
            print("다음 단어들과 같이 변형이 가능합니다")
            print()
            for i in tup[0]:
                print(i, end = " ")
            print()
    else:
        if len(words) == 1 and words[0] == word:
            print("변형될 수 있는 형태가 없습니다.")
        elif len(words) == 2:
            print("다음과 같이 변형이 가능합니다.")
            print()
            print(words[0] if words[0] != word else words[1])
        else:
            if len(words) > 4:
                print("다음 목록과 같이 변형될 가능성이 높습니다.")
                print()
                RecommendList = Recommend(param for param in words if param != word)
                for i in RecommendList:
                    print(i, end =" ")
                print("\n")
                print("나머지 목록을 보시려면 [/]를 입력해주세요.")
                print()
                inpu = input("[ENTER to get advice] 입력 : ")
                if inpu == "/":
                    print() 
                    for i in words:
                        if i == word or i in RecommendList: continue
                        print(i, end = " ")
                    print()
                else:
                    return inpu
            else:        
                print("다음 목록과 같이 변형이 가능합니다.")
                print()
                for i in words:
                    if i == word: continue
                    print(i, end = " ")
                print()
    print()
    return ""

def Recommend(words):
    Max = 0
    Letters = {}
    List = []    
    for word in words:
        array = [0 for i in word]
        for letter in word:
            if letter in Letters:
                array[word.index(letter)] = Letters[letter]
            else:
                for j in WordList[len(word)]:
                    if letter in j:
                        array[word.index(letter)] += 1
                Letters[letter] = array[word.index(letter)]
        List.append((word, sum(array)))       
    List.sort(key = lambda x : x[1], reverse = True)            
    return [ele[0] for ele in List[0:3]]

def MakeQuestion(word, level):
    words = MakeWords(word)
    tup = ExploreDict(words, word)
    if tup[1] == 0 and 2**level >= len(tup[0]) and len(tup[0]) >= 2:
        for ele in tup[0]:
            similarlity = 0
            for num in range(len(word)):
                if word[num] == ele[num]: similarlity += 1
            if similarlity == len(word)-level:
                return ele
    return False

def Quiz():
    os.system("cls")
    print("☆ 야민정음 퀴즈 ☆")
    print()
    while True:
        level = input("난이도 선택 [1 ~ 3] ")
        print()
        try:
            if int(level) < 1 or int(level) > 3:
                print("[ERROR] 1 ~ 3 사이의 숫자를 입력하세요")
                print()
            else:
                level = int(level)
                break
        except:
            print("[ERROR] 숫자를 입력하세요")
            print()
    answer, question = "", ""
    score = 0
    for i in range(5):
        while True:
            if level != 3:
                if random.randint(1, 6) <= 5:
                    rand = 2
                else:
                    rand = 3
                answer = WordList[rand][random.randint(0, len(WordList[rand])-1)]
            else:
                answer = WordList[3][random.randint(0, len(WordList[3])-1)] 
            if MakeQuestion(answer, level):
                question = MakeQuestion(answer, level)
                break
        print("\"{}\"을(를) 올바르게 번역하시오. [20점]".format(question), end = " ")
        reply = input()
        print()
        if reply == answer:
            print("정답!")
            print()
            score += 20
        else:
            print("오답! 정답은 {}입니다~".format(answer))
            print()

    print("당신의 점수는 {}점!".format(score))
    print()
    sentence = ["영.. 좋지 못한 점수", "이십 세기가 참 어렵네요", "좌클릭은 치네요", "거의 수험생..", "야민정음 몇 회독...?", "쇠이 창조화 rnasterpiece 그 자체..."]
    print("{}".format(sentence[score//20]))
    print()
    os.system("pause")
    Intro()
    return

Intro()
inpu = ""

while True:
    if not inpu:
        print("[ENTER to get Advice] 입력 : ", end = "")
        temp = input()
    else:
        temp = inpu
        inpu = ""
    print()
    
    if temp == "":
        Advice()
        continue
    elif temp == "/teach":
        Teach()
        continue
    elif temp == "/gram":
        Gram()
        continue
    elif temp == "/quit":
        Quit()
        break
    elif temp == "/quiz":
        Quiz()
        continue
    elif temp == "/cls":
        Intro()
    else:
        if IsValid(temp) == 1:
            inpu = ShowResults(temp)
        else:
            print("[ERROR] 입력 값이 한글 음절의 조합이어야 합니다.")
            print()
        continue
