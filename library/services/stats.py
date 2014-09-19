
import datetime

from library.model.stats import HtmlDocumentType, DomainTld

def increase_html_document_type_count( doc_type ):
	now = datetime.date.today()
	model = HtmlDocumentType.gql( 'WHERE code = :1 AND report_date = :2', doc_type, now ).get()
	if model:
		model.count += 1
	else:
		model = HtmlDocumentType( code = doc_type, report_date = now )
	model.put()
	model = HtmlDocumentType.gql( 'WHERE code = :1 AND report_date = NULL', doc_type ).get()
	if model:
		model.count += 1
	else:
		model = HtmlDocumentType( code = doc_type )
	model.put()


def increase_domain_tld_count( tld ):
	now = datetime.date.today()
	model = DomainTld.gql( 'WHERE code = :1 AND report_date = :2', tld, now ).get()
	if model:
		model.count += 1
	else:
		model = DomainTld( code = tld, report_date = now )
	model.put()
	model = HtmlDocumentType.gql( 'WHERE code = :1 AND report_date = NULL', tld ).get()
	if model:
		model.count += 1
	else:
		model = DomainTld( code = tld )
	model.put()

