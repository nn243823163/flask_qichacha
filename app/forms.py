#coding:utf-8

from flask_wtf import Form

from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    #使用中文前用u格式化
    username = StringField(label=u'用户名',validators=[DataRequired()])
    password = PasswordField(label=u'密码',validators=[DataRequired()])
    submit = SubmitField(label=u'提交')
