
import gettext
import config

gettext_instance = gettext.translation( 'messages', 'locales', [ config.current_instance['language'] ] )
_ = gettext_instance.ugettext

reportSections = (
	{
		'id': 'priority-actions',
		'label': _('Priority Actions'),
		'keywords': _('Suggestions to improve the site'),
	},
	{
		'id': 'domain',
		'label': _('URL'),
		'keywords': _('Facts about the domain and URL structure'),
	},
	{
		'id': 'page-metadata',
		'label': _('Page Metadata'),
		'keywords': _('Data for crawlers, search engines and directories'),
	},
	{
		'id': 'visitors',
		'label': _('Visitors'),
		'keywords': _('Traits and volume of visits'),
	},
	{
		'id': 'social-monitoring',
		'label': _('Social Metrics'),
		'keywords': _('User interaction outside the website'),
	},
	{
		'id': 'content-optimization',
		'label': _('Content'),
		'keywords': _('Value and style'),
	},
	{
		'id': 'usability',
		'label': _('Usability'),
		'keywords': _('Ease of use and compatibility'),
	},
	{
		'id': 'seo-authority',
		'label': _('Domain Authority'),
		'keywords': _('The influence the site respect others'),
	},
	{
		'id': 'seo-backlinks',
		'label': _('Links'),
		'keywords': _('Juice flow between pages'),
	},
	{
		'id': 'security',
		'label': _('Security'),
		'keywords': _('Threats and the use of safe practices'),
	},
	{
		'id': 'technologies',
		'label': _('Technology'),
		'keywords': 'Responsiveness and other characteristics',
	},
)

