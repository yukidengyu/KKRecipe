from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Text
import requests
import re
import datetime
from sqlalchemy.orm import sessionmaker
import time
linklist={
    'new':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=0&orderby=hot&page=',
    'hot':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=102&orderby=tag&page=',
    'cold':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=202&orderby=tag&page=',
    'soup':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=57&orderby=tag&page=',
    'main':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=59&orderby=tag&page=',
    'snake':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=62&orderby=tag&page=',
    'west':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=160&orderby=tag&page=',
    'bake':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=60&orderby=tag&page=',
    'selfmade':'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=69&orderby=tag&page=',
}
DIALECT='mysql'
DRIVER='mysqldb'
USERNAME='root'
PASSWORD='998219'
HOST='127.0.0.1'
PORT='3306'
DATABASE='recipe'
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
engine=create_engine(SQLALCHEMY_DATABASE_URI)
print(engine)
Session=sessionmaker(bind=engine)
session=Session()
Base=declarative_base()
class Recipe(Base):
    __tablename__='recipe'
    id=Column(Integer,primary_key=True)
    uid=Column(String(10))
    name=Column(String(30))
    ingredient=Column(String(200))
    imageurl=Column(Text)
    t=Column(String(20))
def getRecipe():
    for tag,link in linklist.items():
        print(tag)
        for page in range(1,3):
            data=requests.get(link+str(page)).json()
            if "'error': -2" in str(data):
                print('无数据')
                break
            else:
                data=str(data['data'])
                idlist = re.compile("'id': '(\d+)'").findall(data)
                titlelist = re.compile("title': '(.*?)'").findall(data)
                messagelist = re.compile("'message': '(.*?)'").findall(data)
                mainingredientlist = re.compile("'mainingredient': '(.*?)'").findall(data)
                coverlist = re.compile("'cover': '(.*?)'").findall(data)
                for j in range(len(idlist)):
                    print('当前爬取'+tag+'到第' + str(page) + '页')
                    recipe=session.query(Recipe).filter_by(uid=idlist[j]).first()
                    if recipe:
                        print('已经存在这个菜谱！')
                    else:
                        a=Recipe(uid=idlist[j],name=titlelist[j],ingredient=mainingredientlist[j],imageurl=coverlist[j],t=tag)
                        session.add(a)
                        session.commit()

if __name__ == '__main__':
    while True:
        now=datetime.datetime.now()
        if (now.hour==23 or now.hour==12) and now.minute==0:
            getRecipe()
        time.sleep(60)
