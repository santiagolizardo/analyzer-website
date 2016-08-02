
== Analyzer.WS ==

Analyzer.WS is a web application that can be deployed to Google App Engine and which allows you to generate marketing/SEO reports for websites in an automatic manner.

=== Requirements ===

* Google App Engine Python SDK
* Python (mako templates)
* lxml
* Google URL Shortener API enabled
* Alexa AWIS credentials
* Whoapi API key 
* Geo IP database (paid or free versions)

* Domain/Host to be configured with a basename and the following subdomains
** www
** search
** ranking
** stats
** live-report
** report

=== Instructions ===

```
git clone https://github.com/santiagolizardo/analyzer-website.git
cd analyzer-website
git submodule update --init
```

=== How to start it ===

```
dev_appserver.py --clear_datastore --host localhost --port 9090 .
```

=== How to deploy it ===

```
appcfg.py --application=analyzer-website update .
```

