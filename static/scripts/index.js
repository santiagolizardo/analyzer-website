
$( document ).ready( function()
	{
		$( 'form' ).submit( function()
			{
				var domainInput = document.getElementById( 'domain' );
				var re = new RegExp( domainInput.getAttribute( 'pattern' ) );
				if( false === re.test( domainInput.value ) )
				{
					$( domainInput ).closest( 'div.input-group' ).addClass( 'has-error' );
					domainInput.focus();
					return false;
				}
			}
		);
	}
);

