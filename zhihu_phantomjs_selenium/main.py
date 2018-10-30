# 主函数
import start_url_crawl as st
import redis_db
import time
db = redis_db.RedisOrm()
start_url = 'https://www.zhihu.com/people/xiao-hong-76-54/following'
driver = st.request(start_url)
st.parse_profile(driver)
# parse_follewing(driver)
count = 0
sleep_time = 1
while 1:
    base_url = db.select_from_db().split(',')
    if base_url[0]!='None':
        url = base_url[0]
        if 'page=' in url: # 表明需要爬取follwe
            try:
                count_num = db.count_sum()
                if count_num > 5: #为了节省资源，如果代访问的url > 20 条，保持代访问的url在20条以内
                    continue
                driver = st.request(url)
                st.parse_follewing(driver)
            except:
                limit = int(base_url[1])+1
                if limit < 4:
                    url = url+','+str(limit)
                    db.insert_into_db(url)
        else:
            try:
                driver = st.request(url)
                st.parse_profile(driver)
            except:
                limit = int(base_url[1])+1
                if limit < 4:
                    url = url+','+str(url)
                    db.insert_into_db(url)
    else:
        if sleep_time > 33: #等待时间超过30秒，还没有 
            break
        time.sleep(sleep_time)
        sleep_time = sleep_time*2
    
    # 爬取100条信息
    count += 1
    if count > 100:
        break
    print('【info】:',count)