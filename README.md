# Logs Analysis Project
To build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.
This is for Udacity FullStack Web Developer Nanodegree Project.

**Questions to be answered**

What are the most popular three articles of all time?
Who are the most popular article authors of all time?
On which days did more than 1% of requests lead to errors?

**Installation**

* Install VirtualBox: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
* Install Vagrant: https://www.vagrantup.com/downloads.html
* Download the VM Configuration: https://github.com/udacity/fullstack-nanodegree-vm


- Start the VM: vagrant up
- Login to VM: vagrant ssh
- Vagrant Directory: cd /vagrant
- Download the data with the .sql file provided by udacity.
- To load the data: psql -d news -f newsdata.sql
- To run news.py: python3 news.py

**Views:**

path_count:
```
create view path_count as 
select path, count(*) as views 
from articles join log 
on log.path LIKE CONCAT('%', articles.slug) 
group by log.path;
```
titles_views:
```
create view titles_views as 
select articles.title, path_count.views 
from articles join path_count 
on path_count.path LIKE CONCAT ('%', articles.slug);
```
authors_articles:
```
create view authors_articles 
as select authors.name, articles.title 
from authors join articles 
on authors.id = articles.author;
```
authors_views:
```
create view authors_views as 
select name,views 
from authors_articles join titles_views 
on titles_views.title = authors_articles.title;
```
total_requests:
```
create view total_requests as 
select to_char(time, 'Month DD,YYYY') as date, count(status) as requests 
from log 
group by date;
```
total_errors:
```
create view total_errors as 
select to_char(time, 'Month DD,YYYY') as date, count(status) as err 
from log 
where status LIKE '4%' OR status LIKE '5%' group by date;
```
calculate_error:
```
create view calculate_error as 
select total_errors.date,((total_errors.err/total_requests.requests :: float) * 100) as error 
from total_requests join total_errors 
on total_requests.date = total_errors.date;
```
