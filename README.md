# School Result Django Application
**Django School Basic Result Application

*You can input your subject result and get you result sheet **pdf format** individually.
# main featurs
* Institute wise result and ranked
* Class wise and ranked
* Subject Analysis
* Individually Result Print

**search result in your institute**

![image](https://github.com/asadlive84/schoolresult/blob/master/school/media/Screenshot%20from%202018-07-23%2011-55-26.png)


![image](https://github.com/asadlive84/schoolresult/blob/master/school/media/Screenshot%20from%202018-07-23%2012-18-59.png)


**Rank list in you school**

![image](https://github.com/asadlive84/schoolresult/blob/master/school/media/Screenshot%20from%202018-07-23%2012-19-13.png)


**class analysis**

![image](https://github.com/asadlive84/schoolresult/blob/master/school/media/Screenshot%20from%202018-07-23%2012-19-35.png)

**Subject analysis**

![image](https://github.com/asadlive84/schoolresult/blob/master/school/media/Screenshot%20from%202018-07-23%2012-20-16.png)




```python
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver

```

When you add you marks and student details. Then you will put a command for data save in all model (database)

```python
python3 manage.py class "class name"
python3 manage.py rank "class name"
```
