<?php
/**
 * Displays mobile menu
 *
 * @package Cenote
 */

?>
<nav id="mobile-navigation" class="cenote-mobile-navigation">
	<?php
	wp_nav_menu( array(
		'theme_location' => 'tg-menu-primary',
		'menu_id'        => 'primary-menu',
	) );
	?>
</nav><!-- #mobile-navigation -->
