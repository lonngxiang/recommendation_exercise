import os

def get_item_info(input_file):
    if not os.path.exists(input_file):
        return {}
    item_info = {}
    linenum = 0
    fp = open(input_file,"r",encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum +=1
            continue
        item = line.strip().split(",")
        if len(item )<3:
            continue
        elif len(item) ==3:
            itemid,title,genre = item[0],item[1],item[2]
        elif len(item) >3:
            itemid = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])
        item_info[itemid] = [title,genre]
    fp.close()
    return item_info

def get_ave_score(input_file):
    """
    获得每个电影的平均打分，以字典形式返回
    :param input_file:
    :return:
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    fp = open(input_file,"r",encoding="utf-8")
    for line in fp:
        if linenum ==0:
            linenum +=1
            continue
        item = line.strip().split(",")
        if len(item)<4:
            continue
        userid,itemid,rating = item[0],item[1],float(item[2])
        if itemid not in record_dict:
            record_dict[itemid] = [0,0]
        record_dict[itemid][0] +=1
        record_dict[itemid][1] += rating
    fp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0],3)
    return score_dict

def get_train_data(input_file):
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)
    neg_dict = {}
    pos_dict = {}
    linenum = 0
    score_thr =4
    train_data = []
    fp = open(input_file,"r",encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum +=1
            continue
        item = line.strip().split(",")
        if len(item) <4:
            continue
        userid ,itemid,rating = item[0],item[1],float(item[2])
        if userid not in pos_dict:
            pos_dict[userid] = []
        if userid not in neg_dict:
            neg_dict[userid] = []
        if rating >= score_thr:
            pos_dict[userid].append((itemid,1)) #正样本，label
        else:
            score = score_dict.get(itemid,0)#负样本，用户对他的打分
            neg_dict[userid].append((itemid,score)) #负样本，存储的平均评分

    fp.close()
    #训练样本
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]),len(neg_dict.get(userid,[])))
        if data_num >0: #训练样本>0
            #正样本的训练数据
            train_data += [(userid,zuhe[0],zuhe[1]) for zuhe in pos_dict[userid]][:data_num]
        else:
            continue
        #uer_id 负样本排序（按照得分排序，逆序）
        sorted_neg_list = sorted(neg_dict[userid],key= lambda element:element[1],reverse=True)[:data_num]
        train_data += [(userid,zuhe[0],0 )for zuhe in sorted_neg_list]
    return train_data

# if __name__ == "__main__":
#     train_data = get_train_data("data/ratings.txt")
#     print(train_data)

