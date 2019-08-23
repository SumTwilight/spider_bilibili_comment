- 如何从复杂的json文件中进行信息提取
- 两个循环字典中存储东西，主字典的类容总是会被覆盖
```python
    dict_comment = {}
    dict_temp = {}
    for i in range(20):
        dict_temp['mid'] = comment_dict[i]['mid']     # 用户id
        dict_temp['uname'] = comment_dict[i]['member']['uname']   # 用户名
        dict_temp['sex'] = comment_dict[i]['member']['sex']   # 用户性别
        dict_temp['sign'] = comment_dict[i]['member']['sign']     # 用户签名
        dict_temp['current_level'] = comment_dict[i]['member']['level_info']['current_level']  # 用户当前等级
        dict_temp['vipType'] = comment_dict[i]['member']['vip']['vipType']    # 用户vip类型 type=1 月费 type=2 年费
        dict_temp['vipDueDate'] = comment_dict[i]['member']['vip']['vipDueDate']    # 用户vip到期时间
        dict_temp['ctime'] = comment_dict[i]['ctime']     # 用户评论时间
        dict_temp['rcount'] = comment_dict[i]['count']    # 其他用户回复此评论数
        dict_temp['message'] = comment_dict[i]['content']['message']    # 用户评论
        dict_comment.update({i: dict_temp})
```
![01](./problem/01.jpg)


