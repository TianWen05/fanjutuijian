# 番剧推荐网站项目
### 简介：
这是一个小小的番剧推荐网站项目，只是实现了简单的**协同过滤**算法，以及一些**随机推荐**功能和**新番推荐**功能的小网站，用的是python的**Flask框架**来实现的前后端逻辑
### python环境搭建：
在**终端**（cmd）依次输入一下代码即可自动配置环境，当然前提必须要先**安装python**，我用的是**3.9**版本的python，应该用其他版本也行
```
pip install flask
```
```
pip install py2neo
```

### 代码文档介绍：
- 数据库
    - 环境搭建
        在本文件下的data文件内有本项目所用到的**所有数据**，而如果要运行此项目，则**必须**要先进行数据库数据的载入。这里使用的是**neo4j数据库**，可以去[官方网站](https://neo4j.com/)进行下载，我用到的版本号是**4.2.15**。此外neo4j要用到**java**，也可以到[官网下载](https://www.oracle.com/cn/java/),最好下载**12版本**以上的java，建议使用java12，因为这是官方长期更新的版本。然后就是neo4j和java的**环境变量**的设置，设置环境变量为了让计算机能够找到这些应用，并能在终端中使用。如何配置环境请点击[这里](https://zhuanlan.zhihu.com/p/425239440#:~:text=Neo4j%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%201.%E5%87%86%E5%A4%87java%E7%8E%AF%E5%A2%83%20%E2%80%A2jdk15%E4%B8%8B%E8%BD%BD%20%28%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80%29%E2%80%A2%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE%20%23%E6%B7%BB%E5%8A%A0%E7%B3%BB%E7%BB%9F%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%20JAVA_HOME%20%3D%20%E5%AE%89%E8%A3%85%E8%B7%AF%E5%BE%84,%23%E5%9C%A8Path%E4%B8%AD%E6%B7%BB%E5%8A%A0%20%25JAVA_HOME%25bin%20%23%E6%A3%80%E6%9F%A5%E7%8E%AF%E5%A2%83%20java%20-version%202.%E5%AE%89%E8%A3%85Neo4j%E5%90%AF%E5%8A%A8%20%E2%80%A2Neo4j%E4%B8%8B%E8%BD%BD%20%28%E5%9C%B0%E5%9D%80%29%E2%80%A2%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)
    - data内文件介绍
        - Bangumi_data.csv
        动画数据文件，里面包含有**5916条**动画数据，其中包括动画的中文名、外文名、集数、日期、制作者、评分、评分人数、海报链接、标签和简介信息
        预览：
        ![动画数据预览](/img/bangumiData.png)
        - ci.csv
        标签数据文件，里面筛选出的一些常用标签，并且统计出来了该标签**出现的频率**
        预览：
        ![标签数据预览](/img/label.png)
        - uname.csv
        随机生成的用户数据，生成包括了用户的**uid、用户名和密码**，密码统一为123456
        预览：
        ![用户数据预览](/img/user.png)
        - lianxi.csv
        随机生成的用户评分数据，以领接矩阵的形式转化成表格保存，保存了**打分用户的uid、被打分动画id和所打分数**
        预览：
        ![用户评分数据预览](/img/score.png)
    - 数据的导入
        1. 启动数据库
            终端输入：
            ```
            neo4j.bat console
            ```
            网页打开 http://localhost:7474/ 默认登录名和密码是**neo4j**
        2. 数据导入
            首先先将data内文件放到neo4j根文件夹下的**import文件**
            比如我的就在：
            ![路径](/img/lujing.png)
            **注意！！！** 我将文件放在了CSV文件下了，如果你想直接使用我接下来用的代码建议也**新建一个CSV文件再将文件放入**或**修改以下代码的路径**
            请依次在neo4j输入框下输入以下代码并运行：
            ```cypher
            //加载动画数据
            load CSV with headers from "file:///CSV/Bangumi_data.csv" as list
            create(:Animation{title_chinese:list.title1,
            ID:list.id,
            title_foreign:list.title2,
            episode:list.Episode,
            date:list.date,
            worker:list.worker,
            score:list.score,
            number_of_rater:list.s_number,
            image_url:list.image_url,
            label:list.label,
            introduction:list.txtl})
            ```
            ```cypher
            //加载用户数据
            load csv with headers from "file:///CSV/uname.csv" as list
            create(:User{username:list.name,ID:list.uid,password:list.mima})
            ```
            ```cypher
            //加载评分数据
            load csv with headers from "file:///CSV/lianxi.csv" as list
            match(u:User),(a:Animation)
            where u.ID = list.uid and a.ID = list.id
            with u,a,list
            create (u)-[:SCORE_ON{score:list.score}]->(a)
            ```
            运行完后数据导入就完成了，**注意在运行网站时需要访问数据库，请不要关闭数据库！**
- 前端代码
    - html
        在**templates文件夹**下放入了所有的html模板，现对这些文件进行解释
        - base.html
            基础网页模板，所有其他页面都是由**它继承而来**，主要就是写了所有网页都一样的结构内容，比如网站头部和尾部。
        - drama_home.html
            主页网页模板，主要展示了**个性推荐、随机推荐和新番推荐**三种推荐模式的展示。
        - drama_login.html
            登录页网页模板，实现了一个很普通的登录页
        - drama_register.html
            注册页网页模板
        - search.html
            搜索页网页模板
        - animation_detail.html
            动画详情页模板，实现了前后端交互用户**打分**的功能
    - css
        在**static文件夹**下的css文件夹里，此外static文件夹下其他文件仅仅只是素材文件，现对css文件夹下的文件做简单的介绍
        - base.css
            对基础网页的样式表，设计并实现了基础网页的布局
        - card.css
            对动画资料卡的样式表，设计并实现了网站弹出的动画资料卡的样式
        - detail.css
            对动画详情页的样式表，设计并实现了动画详情页的布局
        - home.css
            对主页的样式表，设计并实现了主页的布局
        - login.css
            对登录页样式表，设计并实现了登录页的布局
        - register.css
            对注册页的样式表，设计并实现了注册页的布局
        - search.css
            对搜索页的样式表，设计并实现了搜索页的布局
- 后端代码
    - python
    在这里我会介绍同级文件下的py文件
        - drama_recommended
            此模块为项目运行的**主模块**，若一切准备就绪，直接运行该文件就可以看到效果，运行后点击编译器弹出的[地址](http://127.0.0.1:5000/)就可以访问该网站了。在此函数模块内实现各种与**前后端交互**等内容，但大多数数据处理在其他模块，此模块**只负责提交并提取数据**。**注意修改程序里的neo4j库访问密码与自己neo4j库密码一致**，分别在**此模块**、**recommend模块**和**RWData模块**都有。
        - recommend
            推荐函数模块，此模块包含了所有的**推荐函数**。为此推荐系统的核心
            1. recommendRandom函数
                随机推荐函数，可以返回任意数量的动画节点信息，以列表的形式返回。
                ```python
                def recommendRandom(num):
                    """
                    随机推荐番剧函数，从数据库中随机找num个节点列表并返回
                    :param num:需要返回的节点数
                    :return: 函num个动画信息的节点列表
                    """
                    # 连接到数据库
                    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
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
                ```
            2. recommendXinfan函数
                新番推荐函数，以时间为降序，返回任意数量的动画节点信息
                ```python
                def recommendXinfan(num):
                    """
                    新番推荐函数，返回num个新番节点信息
                    :param num:需要返回的节点数
                    :return: 一个新番节点列表
                    """
                    # 请求数据库
                    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
                    a = graph.run("""match(n:Animation)
                                with n
                                order by n.date desc
                                return n limit """ + str(num)).data()
                    return a
                ```
            3. recommendPersonality函数
                个性推荐函数，基于**协同过滤**算法，用的是**余弦相似度**，返回任意数量的动画节点信息
                ```python
                def recommendPersonality(username, num):
                    """
                    个性番剧推荐，根据用户信息进行推荐，会返回num个节点信息
                    :param num: 需要返回的节点数
                    :param username: 需要推荐的用户名
                    :return: 返回num个番剧节点信息
                    """
                    graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))
                    # 为用户建立相似度关系
                    username = "username:\"" + username + "\""
                    # 构建余弦相似度关系
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
                ```
        - listTodire
            是一个工具模块，主要处理动画节点数据。有两个函数：
            1. listToDireAnima函数
                将输入的列表动画节点放在一个网页可用的字典数据类型
            2. transformDate函数
                将纯数字的date值变成标准的xxxx年xx月xx形式
        - verify
            校验信息模块，用来校验用户信息模块，有两个函数
            1. passwordVerify函数
                用来校验用户密码信息是否正确
            2. userExistVerify函数
                用来校验新创建用户名是否在数据库
        - RWData
            专门访问数据库函数的模块，对数据库信息进行读写操作，5个函数
            1. writeUser函数
                用来写入新用户的数据
            2. readAnimationInfo函数
                用来查询传入动画id的动画信息
            3. writeScore函数
                用来写入用户打分数据
            4. readSearchData
                用来获取与传入关键词有关的动画节点数据的
            4. readScore
                用来获取用户与动画的打分数据函数