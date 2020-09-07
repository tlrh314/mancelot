<?php
/**
 * Kirki Customizer Options File
 *
 * @package cenote
 */

/**
 * Configuration for Kirki Framework
 */
function cenote_kirki_configuration() {
	return array(
		'url_path' => get_template_directory_uri() . '/inc/kirki/',
	);
}

add_filter( 'kirki/config', 'cenote_kirki_configuration' );

/**
 * Cenote Kirki Config
 */
Kirki::add_config( 'cenote_config', array(
	'capability'  => 'edit_theme_options',
	'option_type' => 'theme_mod',
) );

/**
 * Cenote Kirki Theme Options Panel
 */
Kirki::add_panel( 'cenote_theme_options', array(
	'priority' => 10,
	'title'    => esc_html__( 'Theme Options', 'cenote' ),
) );

/**
 * Cenote Social Options section
 */
Kirki::add_section( 'cenote_section_social', array(
	'title'    => esc_html__( 'Social', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 5,
) );

/**
 * Cenote Top Header Bar Options section
 */
Kirki::add_section( 'cenote_section_top_header', array(
	'title'    => esc_html__( 'Top Header Bar', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 10,
) );

/**
 * Cenote Header Options section
 */
Kirki::add_section( 'cenote_section_header', array(
	'title'    => esc_html__( 'Header', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 15,
) );

/**
 * Cenote Color Option section
 */
Kirki::add_section( 'cenote_section_color', array(
	'title'    => esc_html__( 'Color', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 20,
) );

/**
 * Cenote Post Slider Options section
 */
Kirki::add_section( 'cenote_section_post_slider', array(
	'title'    => esc_html__( 'Post Slider', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Breadcrumbs Options section
 */
Kirki::add_section( 'cenote_section_breadcrumb', array(
	'title'    => esc_html__( 'Breadcrumbs', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Layout Options section
 */
Kirki::add_section( 'cenote_section_layout', array(
	'title'    => esc_html__( 'Layout', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Typography Options section
 */
Kirki::add_section( 'cenote_section_typography', array(
	'title'    => esc_html__( 'Typography', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Blog/Archive Options section
 */
Kirki::add_section( 'cenote_section_archive', array(
	'title'    => esc_html__( 'Archive/Blog', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Page Options section
 */
Kirki::add_section( 'cenote_section_page', array(
	'title'    => esc_html__( 'Page', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Singe Post Options section
 */
Kirki::add_section( 'cenote_section_single', array(
	'title'    => esc_html__( 'Single Post', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Post Ribbon Options section
 */
Kirki::add_section( 'cenote_section_post_ribbon', array(
	'title'    => esc_html__( 'Post Ribbon', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Cenote Footer Options section
 */
Kirki::add_section( 'cenote_section_footer', array(
	'title'    => esc_html__( 'Footer', 'cenote' ),
	'panel'    => 'cenote_theme_options',
	'priority' => 25,
) );

/**
 * Add the required kirki customizer options files
 */
// Cenote social options file goes here.
require get_template_directory() . '/inc/customizer/options/options-social.php';

// Cenote header options file goes here.
require get_template_directory() . '/inc/customizer/options/options-header.php';

// Cenote color options file goes here.
require get_template_directory() . '/inc/customizer/options/options-color.php';

// Cenote post slider options file goes here.
require get_template_directory() . '/inc/customizer/options/options-post-slider.php';

// Cenote breadrumb options file goes here.
require get_template_directory() . '/inc/customizer/options/options-breadcrumb.php';

// Cenote header media options file goes here.
require get_template_directory() . '/inc/customizer/options/options-header-media.php';

// Cenote layout options file goes here.
require get_template_directory() . '/inc/customizer/options/options-layout.php';

// Cenote typography options file goes here.
require get_template_directory() . '/inc/customizer/options/options-typography.php';

// Cenote archive options file goes here.
require get_template_directory() . '/inc/customizer/options/options-archive.php';

// Cenote page options file goes here.
require get_template_directory() . '/inc/customizer/options/options-page.php';

// Cenote single post options file goes here.
require get_template_directory() . '/inc/customizer/options/options-single.php';

// Cenote post ribbon options file goes here.
require get_template_directory() . '/inc/customizer/options/options-post-ribbon.php';

// Cenote footer post options file goes here.
require get_template_directory() . '/inc/customizer/options/options-footer.php';
