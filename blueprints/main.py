from flask import Blueprint,render_template,url_for,redirect,request,flash
from extensions import db
from model import Recipe
import requests
import re
from lxml import etree
from utils import redirect_back
import time
from sqlalchemy.sql.expression import func
main_bp=Blueprint('main',__name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Recipe.query.filter_by(t='new').order_by(func.random()).paginate(page, per_page=20)
    recipes = pagination.items
    count=Recipe.query.count()
    return render_template('index.html',pagination=pagination,recipes=recipes,count=count)

@main_bp.route('/new-recipe')
def new_recipe():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='new').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/new.html',pagination=pagination,recipes=recipes)


@main_bp.route('/hot')
def hot():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='hot').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/hot.html',pagination=pagination,recipes=recipes)
@main_bp.route('/cold')
def cold():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='cold').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/cold.html',pagination=pagination,recipes=recipes)
@main_bp.route('/main')
def main():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='main').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/main.html',pagination=pagination,recipes=recipes)
@main_bp.route('/soup')
def soup():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='soup').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/soup.html',pagination=pagination,recipes=recipes)
@main_bp.route('/snack')
def snack():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='snake').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/snack.html',pagination=pagination,recipes=recipes)

@main_bp.route('/west')
def west():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='west').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/west.html',pagination=pagination,recipes=recipes)
@main_bp.route('/bake')
def bake():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='bake').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/bake.html',pagination=pagination,recipes=recipes)
@main_bp.route('/selfmade')
def selfmade():
    page=request.args.get('page',1,type=int)
    pagination=Recipe.query.filter_by(t='selfmade').order_by(func.random()).paginate(page,per_page=20)
    recipes=pagination.items
    return render_template('t/selfmade.html',pagination=pagination,recipes=recipes)


@main_bp.route('/detail/<uid>')
def detail(uid):
     headers={
          'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
          'authority':'home.meishichina.com',
     }
     recipe=Recipe.query.filter_by(uid=uid).first()
     url='https://home.meishichina.com/recipe-'+str(uid)+'.html'
     data=requests.get(url,headers=headers).content.decode('utf-8')
     step=re.compile('<div class="recipeStep">([\s\S]*?)</div>\n<div class="mo">').findall(data)
     ingredient = recipe.ingredient.split('、')
     message = re.compile('<span class="txt_tart">“</span>(.*?)<span class="txt_end">”').findall(data)
     imageurl = re.compile('<span></span><img src="(.*?)" alt').findall(data)
     print(message)
     if (len(message)) == 0:
         message = '无介绍'
     else:
         message = message[0]
     if len(step)!=0:
          step='<div class="recipeStep">'+step[0]+'</div>'
          return render_template('detail.html',step=step,ingredient=ingredient,recipe=recipe,message=message,imageurl=imageurl[0])
     else:
          print('第一次获取数据失败！')
          print(recipe.uid)
          step = re.compile('<div class="recipeStep">([\s\S]*?)</div>\n<div class="recipeTip mt16').findall(data)
          step = '<div class="recipeStep">' + step[0] + '</div>'
          if len(step)==0:
             flash('数据获取失败！','info')
             return redirect_back()
          else:
              return render_template('detail.html', step=step, ingredient=ingredient, recipe=recipe, message=message,imageurl=imageurl[0])
     #print(data.text)
     #step=re.compile('<div class="recipeStep">(.*?)</div>').findall(data.text)
     #a=etree.html(data.text)

     #return render_template('detail.html')



@main_bp.route('/search')
def search():
     q=request.args.get('q')
     if q=='':
          flash('请重新输入！','info')
          return redirect_back()

     page = request.args.get('page', 1, type=int)
     pagination=Recipe.query.whooshee_search(q).paginate(page,per_page=20)
     results=pagination.items
     return render_template('search.html',pagination=pagination,results=results,q=q)

