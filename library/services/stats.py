
import datetime

from library.model.stats import StatCounter 

def increase_stat_counter( category, code, report_date ):
	if report_date is None:
		query = StatCounter.gql( 'WHERE category = :1 AND code = :2 AND report_date = NULL', category, code )
	else:
		query = StatCounter.gql( 'WHERE category = :1 AND code = :2 AND report_date = :3', category, code, report_date )
	model = query.get()
	if model:
		model.count += 1
	else:
		model = StatCounter( category = category, code = code, report_date = report_date )
	model.put()

def increase_page_rank_count( page_rank ):
	page_rank = str( page_rank )
	increase_stat_counter( 'page_rank', page_rank, None )

def increase_html_document_type_count( doc_type ):
	now = datetime.date.today()
	increase_stat_counter( 'html_document_type', doc_type, now )
	increase_stat_counter( 'html_document_type', doc_type, None )

def increase_domain_tld_count( tld ):
	now = datetime.date.today()
	increase_stat_counter( 'domain_tld', tld, now )
	increase_stat_counter( 'domain_tld', tld, None )

