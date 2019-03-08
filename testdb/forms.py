#!/usr/bin/env python
# -*-encoding:UTF-8-*-

# 两个作用①对于表单的各个字段进行检验，②用于生成HTML代码
from django import forms
class MyForm(forms.Form):
    # 系统首先是先调用系统的各个字段值的判断，然后再会调用用户自定义的校验方法进行判断
    name = forms.CharField(max_length=10,min_length=5,label='姓名')  # 限制输入框的输入最小值和最大值
    email = forms.EmailField(required=False,widget=forms.DateInput,label='邮件地址')
    message = forms.CharField(widget=forms.Textarea,label='信息')   # 设置输入文本框为Textarea # 改变字段的显示风格
    # 自定义教研规则
    # 自定义规则的命名是按照一种组合的名字的，前面是你想要干什么，后面接的是对应字段名的名称
    def clean_message(self):
        message = self.cleaned_data['message']  # 先要获取字段值message，然后进行判断
        print(message)
        # 通过拆分验证文本框里面有多少个单词,注意：split()方法的使用，它的划分方法是按照空格来的,页面里面的message值要用空格分开
        num_words = len(message.split())
        print(num_words)
        if num_words < 4:
            raise forms.ValidationError('单词数不能小于4')
        return message
    #def clean_name(self):
    #    pass


'''
# 控制台实验结果
Django 1.11.20
from testdb.forms import MyForm
my = MyForm()
print(my)
<tr><th><label for="id_name">Name:</label></th><td><input type="text" name="name" required id="id_name" /></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" name="email" id="id_email" /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" required id="id_message" /></td></tr>
print(my.as_ul())
<li><label for="id_name">Name:</label> <input type="text" name="name" required id="id_name" /></li>
<li><label for="id_email">Email:</label> <input type="email" name="email" id="id_email" /></li>
<li><label for="id_message">Message:</label> <input type="text" name="message" required id="id_message" /></li>
print(my.as_p())
<p><label for="id_name">Name:</label> <input type="text" name="name" required id="id_name" /></p>
<p><label for="id_email">Email:</label> <input type="email" name="email" id="id_email" /></p>
<p><label for="id_message">Message:</label> <input type="text" name="message" required id="id_message" /></p>
print(my['name'])   # 打印出name的对应值
<input type="text" name="name" required id="id_name" />
print(my['message'])
<input type="text" name="message" required id="id_message" />
my1 = MyForm({'name':'Hello','email':'abcd@126.com','message':'abcd'})  # 没有问题的情况下会通过
my1.is_valid()
True
my2 = MyForm({'name':'Hello','message':'abcd'})
my2.is_valid()
True
my3 = MyForm({'name':'Hello','email':'abcd','message':'abcd'})
my3.is_valid()
False
my4 = MyForm({'email':'abcd','message':'abcd'})
my4.is_valid()
False
my4['name'].errors   # 由于名字字段没给出，所以会报错
[u'This field is required.']
my4['email'].errors
[u'Enter a valid email address.']   # 邮箱的格式不正确会出现报错
my4['message'].errors               
[]
my4.errors                          # 打印出所有的错误信息
{'name': [u'This field is required.'], 'email': [u'Enter a valid email address.']}

'''

