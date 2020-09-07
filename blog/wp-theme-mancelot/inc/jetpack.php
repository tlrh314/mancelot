<?php
/**
 * Jetpack Compatibility File
 *
 * @link    https://jetpack.com/
 *
 * @package cenote
 */

/**
 * Jetpack setup function.
 *
 * See: https://jetpack.com/support/infinite-scroll/
 * See: https://jetpack.com/support/responsive-videos/
 * See: https://jetpack.com/support/content-options/
 */
function cenote_jetpack_setup() {
	// Add theme support for Infinite Scroll.
	add_theme_support( 'infinite-scroll', array(
		'container' => cenote_jetpack_container(),
		'render'    => 'cenote_infinite_scroll_render',
		'footer'    => 'page',
		'wrapper'   => false,
		'type'      => 'click',
	) );

	// Add theme support for Responsive Videos.
	add_theme_support( 'jetpack-responsive-videos' );

	// Add theme support for Content Options.
	add_theme_support( 'jetpack-content-options', array(
		'post-details'    => array(
			'stylesheet' => 'cenote-style',
			'date'       => '.posted-on',
			'categories' => '.cat-links',
			'tags'       => '.tags-links',
			'author'     => '.byline',
			'comment'    => '.comments-link',
		),
		'featured-images' => array(
			'archive' => true,
			'post'    => true,
			'page'    => true,
		),
	) );
}

add_action( 'after_setup_theme', 'cenote_jetpack_setup' );

/**
 * Custom render function for Infinite Scroll.
 */
function cenote_infinite_scroll_render() {
	while ( have_posts() ) {
		the_post();
		if ( is_search() ) :
			get_template_part( 'template-parts/content', 'search' );
		else :
			get_template_part( 'template-parts/content', get_post_format() );
		endif;
	}
}

/**
 * The value of the JetPack container div.
 *
 * @return string The div id to be used for JetPack Infinite Scroll
 */
function cenote_jetpack_container() {
	$wrapper_container = 'main';
	$archive_layout    = get_theme_mod( 'cenote_archive_style', 'tg-archive-style--masonry' );
	if ( 'tg-archive-style--masonry' === $archive_layout ) {
		$wrapper_container = 'cenote-content-masonry';
	}

	return $wrapper_container;
}
