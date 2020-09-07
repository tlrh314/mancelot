<?php
/**
 * Displays header menu
 *
 * @package Cenote
 */

?>
<nav class="tg-header-navigation">
	<?php
	wp_nav_menu( array(
		'theme_location' => 'tg-menu-header-top',
		'menu_id'        => 'header-menu',
		'fallback_cb'    => false,
	) );
	?>
</nav><!-- /.tg-header-navigation -->
