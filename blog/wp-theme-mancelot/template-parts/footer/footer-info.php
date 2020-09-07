<?php
/**
 * Displays footer information like copyright
 *
 * @package Cenote
 */

?>
<div class="site-info">
	<?php
		/* translators: 1: Current Year, 2: Blog Name 3: Theme Developer 4: WordPress. */
		printf( esc_html__( 'Copyright %1$s %2$s All Right Reserved. Theme By %3$s. Proudly powered by %4$s', 'cenote' ), esc_attr( date( 'Y' ) ), esc_html( get_bloginfo( 'name' ) ), '<a href="https://themegrill.com/themes/cenote">ThemeGrill</a>', '<a href="https://wordpress.org">WordPress</a>' );
	?>
</div><!-- .site-info -->
