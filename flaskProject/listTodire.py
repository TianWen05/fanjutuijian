def listToDireAnima(x, filter_tags=False):
    """
    将输入的列表节点放在一个网页可用的字典数据类型
    :param filter_tags: bool值，选择是否要过滤字符长度大于2的标签
    :param x: 列表节点
    :return: 装有所有节点信息的字典
    """
    if len(x) == 0:
        return []
    animation_info = {"ID": [],
                      "中文名": [],
                      "外国名": [],
                      "海报链接": [],
                      "出版日期": [],
                      "集数": [],
                      "员工": [],
                      "bangumi评分人数": [],
                      "bangumi评分": [],
                      "标签": [],
                      "简介": []}
    for i in range(len(x)):
        animation_info["ID"].append(x[i]["n"]["ID"])
        animation_info["中文名"].append(x[i]["n"]["title_chinese"])
        animation_info["外国名"].append(x[i]["n"]["title_foreign"])
        animation_info["海报链接"].append(x[i]["n"]["image_url"])
        new_date = transformDate(x[i]["n"]["date"])
        animation_info["出版日期"].append(new_date)
        animation_info["集数"].append(x[i]["n"]["episode"])
        if isinstance(x[i]["n"]["worker"], str):
            temp = x[i]["n"]["worker"].split(";")
            animation_info["员工"].append(temp)
        else:
            animation_info["员工"].append(["无"])
        animation_info["bangumi评分人数"].append(x[i]["n"]["number_of_rater"])
        animation_info["bangumi评分"].append(x[i]["n"]["score"])
        temp = x[i]["n"]["label"].split(" ")
        temp_label = []
        for j in range(len(temp)):
            if filter_tags:
                if len(temp[j]) == 2:
                    temp_label.append(temp[j])
            else:
                temp_label.append(temp[j])
        animation_info["标签"].append(temp_label)
        temp_introduction = x[i]["n"]["introduction"].split(" ")
        temp = []
        for j in range(len(temp_introduction)):
            temp.append(temp_introduction[j])
        animation_info["简介"].append(temp)
    return animation_info


def transformDate(date):
    """
    将纯数字的date值变成标准的xxxx年xx月xx形式
    :param date: 纯数字date
    :return: xxxx年xx月xx形式date，如果传入data日期为0，则返回无
    """
    if date == 0:
        return "无"
    day = date % 100
    date = date // 100
    mouth = date % 100
    year = date // 100
    new_date = f"{year}年{mouth}月{day}日"
    return new_date
