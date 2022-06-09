from py2neo import *


def writeUser(username, password):
    """
    将用户数据写入数据库
    :param username: 要写入数据库的用户名
    :param password: 要写入数据库的密码
    :return: 无
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
    # 为新用户构建新ID
    # 获取总用户的数量
    n = graph.run("match(n:User) return count(n)").data()
    ID = str(n[0]["count(n)"])
    for i in range(5 - len(ID)):
        ID = "0" + ID
    ID = "u" + ID
    # 写入用户信息
    graph.run("create(:User{username:\"" + username + "\",ID:\"" + ID + "\",password:\"" + password + "\"})")


def readAnimationInfo(animation_id):
    """
    传入一个动画的id参数返回关于此动画的所有信息
    :param animation_id: 要查询的动画id
    :return: 返回动画节点信息
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
    n = graph.run("match(n:Animation) where n.ID=\"" + animation_id + "\" return n").data()
    return n


def writeScore(user, aID, score):
    """
    给user，animation创建SCORE关系
    :param user:用户名
    :param aID:动画id
    :param score:用户评分
    :return:无
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
    graph.run(
        "match(u:User{username:\"" + user + "\"}),(a:Animation{ID:\"" + aID + "\"})merge(u)-[:SCORE_ON{score:" + str(
            score) + "}]->(a)")


def readSearchData(keyWord):
    """
    传入关键词，搜索有关关键词的最多24个节点信息，并返回信息这24个节点信息
    :param keyWord: 关键词
    :return: 返回最多24个动画节点信息
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
    n = graph.run("""match (n:Animation) 
                     where n.title_chinese=~'.*""" + keyWord + """.*' or 
                     n.title_foreign=~'.*""" + keyWord + """.*' or 
                     n.introduction=~'.*""" + keyWord + """.*' or 
                     n.label=~'.*""" + keyWord + """.*' 
                     return n order by n.date desc limit 24 
                    """).data()
    return n


def readScore(username, aid):
    """
    获取用户与动画之间的评分数
    :param username: 用户名
    :param aid: 动画id
    :return: 返回评分
    """
    if username is None:
        return -1
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
    r = graph.run("match p=(n:User{username:\"" + username + "\"})-[r:SCORE_ON]-(a:Animation{ID:\"" + aid + "\"})return"
                                                                                                            " r.score").data()
    if len(r) == 0:
        score = 0
    else:
        score = r[0]['r.score']
    return score

