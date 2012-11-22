
var messageHandlers = {
	htmlBody: function( body )
	{
		document.getElementById( 'pageTitle' ).innerHTML = body.pageTitle;
		document.getElementById( 'pageDescription' ).innerHTML = body.pageDescription;
		document.getElementById( 'googleAnalytics' ).innerHTML = body.googleAnalytics ? 'Yes' : 'No';
		document.getElementById( 'docType' ).innerHTML = body.docType;
		document.getElementById( 'images' ).innerHTML = body.images;
		document.getElementById( 'headings' ).innerHTML = body.headings;
		document.getElementById( 'softwareStack' ).innerHTML = body.softwareStack;
		document.getElementById( 'pageSize' ).innerHTML = body.pageSize;
		document.getElementById( 'serverIp' ).innerHTML = body.serverIp;
	},
	traffic: function( body )
	{
		document.getElementById( 'worldRank' ).innerHTML = body.worldRank;
		document.getElementById( 'countryRank' ).innerHTML = body.countryRank;
		document.getElementById( 'loadTime' ).innerHTML = body.loadTime;
	},
	twitterAccount: function( body )
	{
		document.getElementById( 'twitterAccount' ).innerHTML = body;
	},
	robotsTxt: function( body )
	{
		document.getElementById( 'robotsTxt' ).innerHTML = body;
	},
	sitemapXml: function( body )
	{
		document.getElementById( 'sitemapXml' ).innerHTML = body;
	},
	screenshot: function( body )
	{
		if( null !== body )
		{
			document.getElementById( 'screenshot' ).src = body;
		}
	},
	w3cValidation: function( body )
	{
		document.getElementById( 'w3cValidity' ).innerHTML = body;
	},
};

var reportCompletionPercentage = 0;
var numSubreports = 6;

function increaseProgressBar()
{
	reportCompletionPercentage += Math.ceil( 100 / numSubreports );

	var progressBar = document.getElementById( 'mainProgressBar' );
	var innerBar = progressBar.getElementsByTagName( 'div' )[0];
	innerBar.style.width = reportCompletionPercentage + '%';

	if( reportCompletionPercentage >= 100 )
	{
		$( progressBar ).fadeOut( 'normal', function() { $( this ).remove(); } );
	}
}

$( document ).ready( function()
	{
		var channel = new goog.appengine.Channel( clientId );
		var handlers = {
			onopen: function()
			{
				$.get( '/initProcessing?domainUrl=' + domainUrl );
			},
			onclose: function()
			{
				//console.log( 'onclose' );
			},
			onmessage: function( message )
			{
				console.dir( message );
				var response = $.parseJSON( message.data );
				if( messageHandlers.hasOwnProperty( response.type ) )
				{
					messageHandlers[ response.type ]( response.body );
					increaseProgressBar();
				}
			},
			onerror: function( data )
			{
				console.error( data );
			}
		};
		var socket = channel.open( handlers );
	}
);
