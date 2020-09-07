<?php
/**
 * Template for displaying full screen search form.
 *
 * @package cenote
 */

?>

<div id="search-form" class="cenote-search-form">
	<span class="search-form-close"></span>	
	<div class="tg-container">
		<?php get_search_form(); ?>
		<p class="cenote-search-form__description"><?php esc_html_e( 'Begin typing your search term above and press enter to search. Press ESC to cancel.', 'cenote' ); ?></p>
	</div>
	<!-- /.tg-container -->
</div>
<!-- /.cenote-search-form -->
