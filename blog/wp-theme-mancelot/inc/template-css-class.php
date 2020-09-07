<?php
/**
 * Handles addition or removal of css class to elements
 *
 * @package cenote
 */

/**
 * Adds custom classes to the array of body classes.
 *
 * @param array $classes Classes for the body element.
 *
 * @return array
 */
function cenote_body_classes( $classes ) {
	global $post;

	// Adds a class of site layout.
	$classes[] = get_theme_mod( 'cenote_layout_site', 'layout-site--wide' );

	// Adds a class of hfeed to non-singular pages.
	if ( ! is_singular() ) {
		$classes[] = 'hfeed';
	}

	// Adds a class of post style to archive pages.
	if ( is_archive() || is_home() ) {
		$classes[] = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );
		$classes[] = get_theme_mod( 'cenote_layout_archive', 'layout--no-sidebar' );

		if ( 'tg-archive-style--classic' !== get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' ) ) {
			$classes[] = get_theme_mod( 'cenote_archive_column', 'tg-archive-col--3' );
		}
	} elseif ( is_single() ) {
		// Adds a class to single post.
		$layout = get_post_meta( $post->ID, 'cenote_post_layout', true );

		// If individual layout is set.
		if ( ! empty( $layout ) ) {
			$classes[] = $layout;
		} else {
			// if individual layout is not set add global one.
			$classes[] = get_theme_mod( 'cenote_layout_single', 'layout--right-sidebar' );
		}
	} elseif ( is_page() ) {
		// Adds a class to page.
		$layout = get_post_meta( $post->ID, 'cenote_post_layout', true );

		// If individual layout is set.
		if ( ! empty( $layout ) ) {
			$classes[] = $layout;
		} else {
			// if individual layout is not set add global one.
			$classes[] = get_theme_mod( 'cenote_layout_page', 'layout--right-sidebar' );
		}
	}

	return $classes;
}

add_filter( 'body_class', 'cenote_body_classes' );

/**
 * Adds css class to header
 */
function cenote_header_class() {
	$classes = array();

	// Add header layout class.
	$classes[] = get_theme_mod( 'cenote_header_style', 'tg-site-header--default' );

	echo esc_attr( join( ' ', $classes ) );
}

/**
 * Adds css class to footer
 */
function cenote_footer_class() {
	$classes = array();

	// Add footer layout class.
	$classes[] = get_theme_mod( 'cenote_footer_style', 'tg-site-footer--default' );

	echo esc_attr( join( ' ', $classes ) );
}

/**
 * Adds css class to main navigation
 */
function cenote_navigation_class() {
	$classes = array();

	$classes[] = get_theme_mod( 'cenote_menu_style', 'tg-site-menu--default' );

	echo esc_attr( join( ' ', $classes ) );
}
