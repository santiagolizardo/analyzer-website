
== DomainGrasp ==

DomainGrasp is a web application that can be deployed to Google App Engine and which allows you to generate marketing/SEO reports for websites in an automatic manner.

=== Requirements ===

* Google App Engine Python SDK
* Python
* lxml
* Google URL Shortener API enabled
* Alexa AWIS credentials
* Whoapi API key 

* Domain/Host to be configured with a basename and the following subdomains
** www
** search
** ranking
** stats
** live-report
** report

=== Instructions ===

git clone url directory
git submodule update --init

=== How to start it ===

dev_appserver.py --clear_datastore --host localhost --port 9090 .

=== How to deploy it ===

appcfg.py --application=analyzer-website update .

