# GloudCMS
### University Project @ CODE University of Applied Sciences | 13.10.2019


## Description

GloudCMS is a headless content management system that runs on Google Cloud.

The admin interface and the REST API both run on GKE.
The example-blog runs on GAE.

## Usage

You can access the admin interface @ https://philipbizimis.com (make sure it is https).

You can access the REST API @ https://api.philipbizimis.com/v1/ (make sure it is https).

There is a test account that has about 10 articles. Feel free to add, update and delete.
```bash
Account Info:
gloudtest123@gmail.com
CODE123@
```

There is an example-blog that makes REST API calls for you (only to the test account).
It runs on Google App Engine and is @ gloudcms-123.appspot.com

## Instructions
There are three things that you can do on the admin interface.

After the login please go to the "Articles" page (/dashboard/articles).

To write a new article, click on the blue plus button to see a link that contains a template.

Follow the link and copy the text. Now go to docs.google.com, create a new document and paste the template.

After editing the content, please give your document a unique title.

Then you can copy the link and paste it into the form field that says "Insert Link".
A success message should appear.

You can now head to gloudcms.appspot.com and find your article on top.

If you want to edit your article, just edit the body and paste the link again. It needs to be the same title otherwise there will be a new article created. To delete an article paste the article URL into the delete form.

## REST API
There are different API calls you can do.

All endpoints have the prefix https://api.philipbizimis.com/v1/<apiid>

You can find your "apiid" on the dashboard if you click on your profile picture.
```
Available Endpoints:

/account - get account info
/stats - get account stats

/search
  /keyword/<keyword> - get all articles that contain the keyword in either title or body
  /tags/<tag1,tag2,tag...>/<i/n> - get all articles that have one of the tags (n) or that have intersecting tags (i)

/articles
  /date/<1/-1> - get all articles ordered by date in either ascending (1) or descending (-1) order
  /modified/<1/-1> - get all articles ordered by 'last modified' in either ascending (1) or descending (-1) order
  /article/<article_url> - get a specific article
  /titles - get all article titles
  /length/<1/-1> - get all articles ordered by length in either ascending (1) or descending (-1) order

/authors - get all authors and their articles
  /<author>/<1/-1> - get all articles by one author (type the name with spaces) ordered by date in either ascending (1) or descending (-1) 
                     order
example:  https://api.philipbizimis.com/v1/myapiid/articles/modified/1
```

Please let me know if there is anything not working.