
$( document ).ready(function() {
	var container = document.getElementById( 'htmlDocumentTypesChart' ).getContext( '2d' );
	new Chart( container ).Doughnut( htmlDocumentTypes, {} );
	
	container = document.getElementById( 'domainTlds' ).getContext( '2d' );
	new Chart( container ).Doughnut( domainTlds, {} );
});

