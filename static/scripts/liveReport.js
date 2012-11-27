
var statuses = {
	good: 0,
	regular: 0,
	bad: 0
};
var totalStatuses = 0;

function addAction( action )
{
	var olEl = document.getElementById( 'priorityActions' );
	
	statuses[ action.status ]++;
	totalStatuses++;

	$( 'div#statuses > div.bar-success' )
		.css( 'width', ( ( statuses['good'] * 100 ) / totalStatuses ) + '%' );
	$( 'div#statuses > div.bar-warning' )
		.css( 'width', ( ( statuses['regular'] * 100 ) / totalStatuses ) + '%' );
	$( 'div#statuses > div.bar-danger' )
		.css( 'width', ( ( statuses['bad'] * 100 ) / totalStatuses ) + '%' );

	$( '#goodStatuses' ).html( statuses['good'] );
	$( '#regularStatuses' ).html( statuses['regular'] );
	$( '#badStatuses' ).html( statuses['bad'] );

	if( 'description' in action )
	{
		$( '<li>' + action.description + '</li>' ).appendTo( olEl );
	}
}

var messageHandlers = {
	htmlBody: function( content )
	{
		document.getElementById( 'pageTitle' ).innerHTML = content.pageTitle;
		document.getElementById( 'pageDescription' ).innerHTML = content.pageDescription;
		document.getElementById( 'googleAnalytics' ).innerHTML = content.googleAnalytics ? 'Yes' : 'No';
		document.getElementById( 'docType' ).innerHTML = content.docType;
		document.getElementById( 'images' ).innerHTML = content.images;
		document.getElementById( 'headings' ).innerHTML = content.headings;
		document.getElementById( 'softwareStack' ).innerHTML = content.softwareStack;
		document.getElementById( 'pageSize' ).innerHTML = content.pageSize;
		document.getElementById( 'serverIp' ).innerHTML = content.serverIp;
	},
	domain: function( content )
	{
		document.getElementById( 'domainOwner' ).innerHTML = content.owner;
		document.getElementById( 'domainRegistrationDate' ).innerHTML = content.registrationDate;
		document.getElementById( 'domainExpirationDate' ).innerHTML = content.expirationDate;
	},
	traffic: function( content )
	{
		document.getElementById( 'worldRank' ).innerHTML = content.worldRank;
		document.getElementById( 'countryRank' ).innerHTML = content.countryRank;
		document.getElementById( 'loadTime' ).innerHTML = content.loadTime;
	},
	twitterAccount: function( content )
	{
		document.getElementById( 'twitterAccount' ).innerHTML = content.twitterAccount;
	},
	robotsTxt: function( content )
	{
		document.getElementById( 'robotsTxt' ).innerHTML = content.robotsTxt;
	},
	sitemapXml: function( content )
	{
		document.getElementById( 'sitemapXml' ).innerHTML = content.sitemapXml;
	},
	screenshot: function( content )
	{
		if( null !== content )
		{
			document.getElementById( 'screenshot' ).src = content.screenshot;
		}
	},
	w3cValidation: function( content )
	{
		document.getElementById( 'w3cValidity' ).innerHTML = content;
	},
	facebook: function( content )
	{
		document.getElementById( 'facebookLikes' ).innerHTML = content.facebookLikes;
		document.getElementById( 'facebookComments' ).innerHTML = content.facebookComments;
		document.getElementById( 'facebookShares' ).innerHTML = content.facebookShares;
	},
	score: function( content )
	{
		score = content;
		document.getElementById( 'score' ).innerHTML = content;
	},
};

var reportCompletionPercentage = 0;
var numSubreports = 0;
for( var key in messageHandlers )
{
	numSubreports += ( messageHandlers.hasOwnProperty( key ) ? 1 : 0 );
}
numSubreports--; // score does not count.
var score = null;

function increaseProgressBar()
{
	reportCompletionPercentage += Math.ceil( 100 / numSubreports );

	var progressBar = document.getElementById( 'mainProgressBar' );
	if( progressBar )
	{
		var innerBar = progressBar.getElementsByTagName( 'div' )[0];
		innerBar.style.width = reportCompletionPercentage + '%';
	}

	if( reportCompletionPercentage >= 100 )
	{
		$( progressBar ).fadeOut( 'normal', function() { $( this ).remove(); } );
		if( score == null ) $.get( '/calculateScore?domainUrl=' + domainUrl );
	}
}

$( document ).ready( function()
	{
		var channel = new goog.appengine.Channel( clientId );
		var handlers = {
			onopen: function()
			{
				$.get( '/launchSubreports?domainUrl=' + domainUrl );
			},
			onclose: function()
			{
				//console.log( 'onclose' );
			},
			onmessage: function( message )
			{
				var response = $.parseJSON( message.data );
				if( messageHandlers.hasOwnProperty( response.name ) )
				{
					messageHandlers[ response.name ]( response.content );

					increaseProgressBar();

					for( var i = 0; i < response.actions.length; i++ )
					{
						addAction( response.actions[i] );
					}
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
