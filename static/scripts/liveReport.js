
var statuses = {
	good: 0,
	regular: 0,
	bad: 0
};
var totalStatuses = 0;
var channel = null, socket = null;

function addAction( action )
{
	var olEl = document.getElementById( 'priorityActions' );
	
	statuses[ action.status ]++;
	totalStatuses++;

	$( 'div#statuses > div.progress-bar-success' )
		.css( 'width', ( ( statuses.good * 100 ) / totalStatuses ) + '%' );
	$( 'div#statuses > div.progress-bar-warning' )
		.css( 'width', ( ( statuses.regular * 100 ) / totalStatuses ) + '%' );
	$( 'div#statuses > div.progress-bar-danger' )
		.css( 'width', ( ( statuses.bad * 100 ) / totalStatuses ) + '%' );

	$( '#goodStatuses' ).html( statuses.good );
	$( '#regularStatuses' ).html( statuses.regular );
	$( '#badStatuses' ).html( statuses.bad );

	if( 'description' in action )
	{
		$( '<li>' + action.description + '</li>' ).appendTo( olEl );
	}
}

function formatLibraries(libraries) {
    var html = ['<ul>'];
    libraries.forEach(function(library) {
        html.push('<li>' + library.name + '</li>');
    });
    html.push('</ul>');
    return html.join('');
}

var messageHandlers = {
	htmlBody: function( content )
	{
		document.getElementById( 'pageTitle' ).innerHTML = content.pageTitle;
		document.getElementById( 'pageDescription' ).innerHTML = content.pageDescription;
		document.getElementById( 'pageKeywords' ).innerHTML = content.pageKeywords;

		document.getElementById( 'googleAnalytics' ).innerHTML = content.googleAnalytics ? 'Yes' : 'No';
		document.getElementById( 'docType' ).innerHTML = content.docType;
		document.getElementById( 'images' ).innerHTML = content.images;
		document.getElementById( 'headings' ).innerHTML = content.headings;
		document.getElementById( 'softwareStack' ).innerHTML = content.softwareStack;
		document.getElementById( 'pageSize' ).innerHTML = content.pageSize;
		
		document.getElementById( 'textHtmlRatio' ).innerHTML = ( parseFloat( content.textHtmlRatio ) * 100 ).toFixed( 2 ) + '%';
		
		document.getElementById( 'declaredLanguage' ).innerHTML = content.declaredLanguage;

        document.getElementById( 'libraries' ).innerHTML = formatLibraries(content.libraries);
		
		if( content.encoding )
		{
			document.getElementById( 'encoding' ).innerHTML = content.encoding;
		}

		if( content.internalLinks )
		{
			document.getElementById( 'internalLinks' ).innerHTML = content.internalLinks;
		}
		if( content.containsFlash )
		{
			document.getElementById( 'containsFlash' ).innerHTML = content.containsFlash;
		}
		if( content.pageCompression )
		{
			document.getElementById( 'pageCompression' ).innerHTML = content.pageCompression;
		}
		
		document.getElementById( 'emailAddresses' ).innerHTML = content.emailAddresses;
	},
    httpsProtocol: function(content) {
        if(null !== content) { document.getElementById('httpsProtocol').innerHTML = content; }
    },
	domain: function( content )
	{
        if(content) {
		    document.getElementById( 'domainOwner' ).innerHTML = content.owner;
		    document.getElementById( 'domainRegistrationDate' ).innerHTML = content.registrationDate;
		    document.getElementById( 'domainExpirationDate' ).innerHTML = content.expirationDate;
		    document.getElementById( 'serverIp' ).innerHTML = content.serverIp;
        }
	},
	traffic: function( content )
	{
		document.getElementById( 'worldRank' ).innerHTML = content.worldRank;
		document.getElementById( 'loadTime' ).innerHTML = content.loadTime;
		document.getElementById( 'visitorsLocation' ).innerHTML = content.visitorsLocation;
		document.getElementById( 'relatedLinks' ).innerHTML = content.relatedLinks;
	},
	twitterAccount: function( content )
	{
		document.getElementById( 'twitterAccount' ).innerHTML = content;
	},
	robotsTxt: function( content )
	{
		document.getElementById( 'robotsTxt' ).innerHTML = content;
	},
	humansTxt: function( content )
	{
		document.getElementById( 'humansTxt' ).innerHTML = content;
	},
	sitemapXml: function( content )
	{
		document.getElementById( 'sitemapXml' ).innerHTML = content;
	},
	pageFavicon: function( content )
	{
		document.getElementById( 'pageFavicon' ).innerHTML = content;
	},
	custom404: function( content )
	{
		document.getElementById( 'custom404' ).innerHTML = content;
	},
	screenshot: function( content )
	{
		if( null !== content )
		{
			document.getElementById( 'screenshot' ).src = content;
		}
	},
	w3cValidation: function( content )
	{
        if(content) {
    		document.getElementById( 'w3cValidity' ).innerHTML = content.w3cValidation;
        }
	},
	facebook: function( content )
	{
        if(content) {
		    document.getElementById( 'facebookLikes' ).innerHTML = content.facebookLikes;
		    document.getElementById( 'facebookComments' ).innerHTML = content.facebookComments;
		    document.getElementById( 'facebookShares' ).innerHTML = content.facebookShares;
        }
	},
	indexedPages: function( content )
	{
		document.getElementById( 'indexedPages' ).innerHTML = content;
	},
	score: function( content )
	{
		score = content;
		document.getElementById( 'score' ).innerHTML = content;
		socket.close();
	},
};

var reportCompletionPercentage = 0;
var score = null;

function increaseProgressBar()
{
	reportCompletionPercentage += Math.ceil( 100 / numberOfTasks );

	var progressBar = document.getElementById( 'mainProgressBar' );
	if( progressBar )
	{
		var innerBar = progressBar.getElementsByTagName( 'div' )[0];
		innerBar.style.width = reportCompletionPercentage + '%';
	}

	if( reportCompletionPercentage >= 100 )
	{
		$( progressBar ).fadeOut( 'normal', function() { $( this ).remove(); } );
		if( score === null ) $.get( '/calculateScore?domainUrl=' + domainUrl );
	}
}

$( document ).ready( function()
	{
		channel = new goog.appengine.Channel( clientId );

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
		socket = channel.open( handlers );
	}
);

