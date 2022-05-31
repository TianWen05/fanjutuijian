import random

from py2neo import *


def recommendRandom(num):
    """
    随机推荐番剧函数，从数据库中随机找num个节点列表并返回
    :param num:需要返回的节点数
    :return: 函num个动画信息的节点列表
    """
    # 连接到数据库
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123.abc"))
    ID_list = []
    # 随机生成6个id
    e = 0
    while True:
        ID1 = str(int(random.random() * 5916 + 1))
        for j in range(5 - len(ID1)):
            ID1 = "0" + ID1
        ID1 = "a" + ID1
        # 判重过滤
        if ID1 not in ID_list:
            ID_list.append(ID1)
            e += 1
        if e == num:
            break
    n_list = []
    # 获取随机节点
    for i in range(num):
        n = graph.run("match (n:Animation{ID:\"" + ID_list[i] + "\"}) return n").data()
        n_list.append(n[0])
    return n_list


def recommendXinfan(num):
    """
    新番推荐函数，返回num个新番节点信息
    :param num:需要返回的节点数
    :return: 一个新番节点列表
    """
    # 请求数据库
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123.abc"))
    a = graph.run("""match(n:Animation)
                   with n
                   order by n.date desc
                   return n limit """ + str(num)).data()
    return a


def recommendPersonality(username, num):
    """
    个性番剧推荐，根据用户信息进行推荐，会返回num个节点信息
    :param num: 需要返回的节点数
    :param username: 需要推荐的用户名
    :return: 返回num个番剧节点信息
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123.abc"))
    # 为用户建立相似度关系
    username = "username:\"" + username + "\""

    graph.run("""match(u1:User{""" + username + """})-[r1:SCORE_ON]-(a:Animation)-[r2:SCORE_ON]-(u2:User)
                 with u1,u2,count(a) as animation_common,
                 sum(r1.score * r2.score)/(sqrt(sum(r1.score^2)) * sqrt(sum(r2.score^2))) AS sim
                 where animation_common>=2 and sim >0.9
                 merge(u1)-[s:SIMILARITY]-(u2)
                 set s.sim = sim
                 """)
    n = graph.run("""match(u1:User{""" + username + """})-[s:SIMILARITY]-(u2:User)
                     with u1,u2,s
                     order by s.sim desc limit 10
                     match(n:Animation)-[r:SCORE_ON]-(u2)
                     with n
                     where toFloat(n.score)>7.5
                     return n limit 
                     """ + str(num)).data()
    return n
