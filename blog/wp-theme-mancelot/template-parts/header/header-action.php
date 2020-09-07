<?php
/**
 * Displays header action like cart and search
 *
 * @package Cenote
 */

?>
<nav class="tg-header-action-navigation">
	<ul class="tg-header-action-menu">
		<?php if ( true === get_theme_mod( 'cenote_search_icon_option', true ) ) : ?>
			<li class="tg-search-toggle"><i class="tg-icon-search"></i></li>
		<?php endif; ?>

		<li class="tg-mobile-menu-toggle">
			<span></span>
		</li>
	</ul><!-- .tg-header-action-menu -->
</nav>
<!-- /.tg-header-action-navigation -->
