#
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import time
import redis_db
import mongo_db

db = redis_db.RedisOrm()
db_mongo = mongo_db.MongoOrm()


#设置浏览器请求头以及部分参数
def request(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'

    #设置不加载图片
    dcap["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS( desired_capabilities = dcap )
    #设置最大加载时间
    driver.set_page_load_timeout(40) #40妙
    driver.get(url)
    #执行js代码
    js_script_scroll = "document.getElementsByClassName('Pagination')[0].scrollIntoView(true)"
    js_script_click = "document.getElementsByClassName('ProfileHeader-contentFooter')[0].getElementsByTagName('button')[0].click()"
    driver.execute_script(js_script_scroll)
    driver.execute_script(js_script_click)
    time.sleep(3)
    print(driver.title)
    print(driver.current_url)
    return driver

'''
*第一部分，采集个人信息和页码，-----------complate
*个人信息存入个人信息数据表，页码URL和解析函数名存入URL_解析函数表
'''
def parse_profile(driver):
    # 执行js
    # 注意document.getElementsByClassName()获取到的是一个list，滑到最后面
    #判断性别
    try:
        sex_m = driver.find_element_by_css_selector('.Icon--male')
    except:
        sex_m = False
    try:
        sex_f = driver.find_element_by_css_selector('.Icon--female')
    except:
        sex_f = False
    if sex_m:
        sex = 'M'
    elif sex_f:
        sex = 'F'
    else:
        sex = 'None'
    # 打印本人详细信息
    details = driver.find_elements_by_css_selector('.ProfileHeader-detail .ProfileHeader-detailItem')
    d = {}
    d['sex'] = sex
    for detail in details:
        title = detail.find_element_by_css_selector('.ProfileHeader-detailLabel').text
        content = detail.find_element_by_css_selector('.ProfileHeader-detailValue').text
        d[title] = content

    # 将个人信息存入mongo,database = zhihu,table = consumer
    db_mongo.insert_into_db(d)
    print('[INFO]:insert into mongo ',str(d))
    #调用find_element_by_css_selector函数按照css样式取出css元素
    #如果该样式不存在，会抛出异常
    #find_elements_by_css_selector是取出所有符合条件的css样式表，返回的数组

    # 打印每个人总共有几页关注
    # 将要爬取的页面取出来，存入redis
    page_num = driver.find_elements_by_css_selector('.Pagination button.Button:nth-last-child(2)')[0].text
    page_num = int(page_num)
    print('base_url:',driver.current_url)
    base_url = driver.current_url
    for i in range(page_num):
        url = base_url+'?page='+str(i+1)+',1'
        db.insert_into_db(url)
        print('[INFO]:insert into redis ',url)
    driver.close()
'''
*第二部分，采集关注的人的信息，----------------------complate
*将采集到的信息存入数据库，分别为URL_解析函数
'''
def parse_follewing(driver):
    follew = driver.find_elements_by_css_selector('.List-item')
    follews = []
    for each in follew:
        name_url = each.find_element_by_css_selector('.ContentItem-head a.UserLink-link')
        ##Popover79-toggle > a:nth-child(1)
        name = name_url.text
        url = name_url.get_attribute('href')+'/following'
        try:
            con = each.find_element_by_css_selector('.ContentItem-head .RichText.ztext')
            text = con.text
        except:
            text = ""
        one = {}
        one['name'] = name
        one['url'] = url
        one['prof'] = text
        redis_insert_url = url+',1'
        db.insert_into_db(redis_insert_url)
        print('[INFO]:insert into redis ',redis_insert_url)
        follews.append(one)
        print(len(follew))
    driver.close()