#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def popular_articles():
    db = psycopg2.connect(database = DBNAME)
    c = db.cursor()
    c.execute("create view path_count as select path, count(*) as views from articles join log on log.path LIKE CONCAT('%', articles.slug) group by log.path;")
    c.execute("create view titles_views as select articles.title, path_count.views from articles join path_count on path_count.path LIKE CONCAT ('%', articles.slug);")
    c.execute("select title, views from titles_views order by views desc limit 3;")
    articles = c.fetchall()
    print("\nMost Popular Articles")
    for article in articles[:3]:
        print("\n * {:} ---  {:} views\n" .format(article[0], article[1]))
    db.close()

def popular_authors():
    db = psycopg2.connect(database = DBNAME)
    c = db.cursor()
    c.execute("create view authors_articles as select authors.name, articles.title from authors join articles on authors.id = articles.author;")
    c.execute("create view path_count as select path, count(*) as views from articles join log on log.path LIKE CONCAT('%', articles.slug) group by log.path;")
    c.execute("create view titles_views as select articles.title, path_count.views from articles join path_count on path_count.path LIKE CONCAT ('%', articles.slug);")
    c.execute("create view authors_views as select name,views from authors_articles join titles_views on titles_views.title = authors_articles.title;")
    c.execute("select name, sum(views) as views from authors_views group by name order by views DESC;")
    authors = c.fetchall()
    print("\nMost Popular Authors")
    for author in authors[:4]:
        print("\n * {:} ---  {:} views\n" .format(author[0], author[1]))
    db.close()

def requests_errors():
    db = psycopg2.connect(database = DBNAME)
    c = db.cursor()
    c.execute("create view total_requests as select to_char(time, 'Month DD,YYYY') as date, count(status) as requests from log group by date;")
    c.execute("create view total_errors as select to_char(time, 'Month DD,YYYY') as date, count(status) as err from log where status LIKE '4%' OR status LIKE '5%' group by date;")
    c.execute("create view calculate_error as select total_errors.date,((total_errors.err/total_requests.requests :: float) * 100) as error from total_requests join total_errors on total_requests.date = total_errors.date;")
    c.execute("select date, error as error_more_than_one_percent from calculate_error where error > 1;")
    errors = c.fetchall()
    print("\nOn which days did more than 1% of requests lead to errors:")
    for error in errors[:1]:
        print("\n * {:12} ---  {:03.1f}% errors\n" .format(error[0], error[1]))
    db.close()



if __name__ == "__main__":
    popular_articles()
    popular_authors()
    requests_errors()
