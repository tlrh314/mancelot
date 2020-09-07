<?php
/**
 * Shows breadcrumb
 *
 * @package cenote
 */

// If we are front page or blog page, return.
if ( is_front_page() || is_home() ) {
	return;
}

// If file is not already loaded, loaded it now.
if ( ! function_exists( 'breadcrumb_trail' ) ) {
	include get_template_directory() . '/inc/compatibility/breadcrumb.php';
}
?>
<nav id="breadcrumb" class="cenote-breadcrumb cenote-breadcrumb--light">
	<?php
	breadcrumb_trail( array(
		'container'   => 'div',
		'before'      => '<div class="tg-container">',
		'after'       => '</div>',
		'show_browse' => false,
	) );
	?>
</nav>
