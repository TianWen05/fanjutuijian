from py2neo import *


def passwordVerify(username, password):
    """
    检验用户名与密码是否匹配
    :param username: 需要检验的用户名
    :param password: 需要检验的密码
    :return: 匹配为Ture，不匹配为False
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123.abc"))
    n = graph.run("match(u:User{username:\"" + username + "\"}) return u.password").data()
    if len(n) == 0:
        return False
    else:
        if password != n[0]["u.password"]:
            return False
    return True


def userExistVerify(username):
    """
    检验用户名是否已经在数据库中了
    :param username: 需要检验的用户名
    :return: 在数据库为True,不在数据库为False
    """
    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123.abc"))
    n = graph.run("match(u:User{username:\"" + username + "\"}) return u.password").data()
    if len(n) == 0:
        return False
    return True
