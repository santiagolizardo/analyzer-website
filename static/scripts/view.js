
var messageHandlers = {
	htmlBody: function( body )
	{
		document.getElementById( 'pageTitle' ).innerHTML = body.pageTitle;
		document.getElementById( 'pageDescription' ).innerHTML = body.pageDescription;
		document.getElementById( 'googleAnalytics' ).innerHTML = body.googleAnalytics ? 'Yes' : 'No';
		document.getElementById( 'docType' ).innerHTML = body.docType;
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
};

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
				}
			},
			onerror: function( data )
			{
				alert( data );
			}
		};
		var socket = channel.open( handlers );
	}
);
