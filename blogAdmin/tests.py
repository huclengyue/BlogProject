from xpinyin import Pinyin

test = Pinyin()

print(test.get_pinyin('钓鱼岛、是、23 new time 中国的wewqeqweqwe ew we weq  we qwe qw').replace(" ", "-").replace("-、", ""))
