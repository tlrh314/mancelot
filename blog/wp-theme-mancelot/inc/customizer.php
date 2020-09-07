<?php
/**
 * Cenote Theme Customizer
 *
 * @package cenote
 */

/**
 * Add postMessage support for site title and description for the Theme Customizer.
 *
 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
 */
function cenote_customize_register( $wp_customize ) {
	$wp_customize->get_setting( 'blogname' )->transport         = 'postMessage';
	$wp_customize->get_setting( 'blogdescription' )->transport  = 'postMessage';
	$wp_customize->get_setting( 'header_textcolor' )->transport = 'postMessage';

	if ( isset( $wp_customize->selective_refresh ) ) {
		$wp_customize->selective_refresh->add_partial( 'blogname', array(
			'selector'        => '.site-title a',
			'render_callback' => 'cenote_customize_partial_blogname',
		) );
		$wp_customize->selective_refresh->add_partial( 'blogdescription', array(
			'selector'        => '.site-description',
			'render_callback' => 'cenote_customize_partial_blogdescription',
		) );
	}

	// Require upsell customizer section class.
	require get_template_directory() . '/inc/class-cenote-upsell-section.php';

	// Register `CENOTE_Upsell_Section` type section.
	$wp_customize->register_section_type( 'CENOTE_Upsell_Section' );

	// Add `CENOTE_Upsell_Section` to display pro link.
	$wp_customize->add_section(
		new CENOTE_Upsell_Section( $wp_customize, 'cenote_upsell_section',
			array(
				'title'      => esc_html__( 'View PRO version', 'cenote' ),
				'url'        => 'https://themegrill.com/themes/cenote/?utm_source=cenote-customizer&utm_medium=view-pro-link&utm_campaign=view-pro#free-vs-pro',
				'capability' => 'edit_theme_options',
				'priority'   => 1,
			)
		)
	);
}

add_action( 'customize_register', 'cenote_customize_register' );

/**
 * Render the site title for the selective refresh partial.
 *
 * @return void
 */
function cenote_customize_partial_blogname() {
	bloginfo( 'name' );
}

/**
 * Render the site tagline for the selective refresh partial.
 *
 * @return void
 */
function cenote_customize_partial_blogdescription() {
	bloginfo( 'description' );
}

/**
 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
 */
function cenote_customize_preview_js() {
	wp_enqueue_script( 'cenote-customizer', get_template_directory_uri() . '/assets/js/customizer.js', array( 'customize-preview' ), '20151215', true );
}

add_action( 'customize_preview_init', 'cenote_customize_preview_js' );

/**
 * Add customize control scripts.
 */
function cenote_customize_controls_scripts() {
	?>
	<style>

		li#accordion-section-cenote_upsell_section h3.accordion-section-title {
			background-color: #de7b85 !important;
			border-left-color: #b3525c !important;
		}

		#accordion-section-cenote_upsell_section h3 a:after {
			content: '\f345';
			color: #fff;
			position: absolute;
			top: 12px;
			right: 10px;
			z-index: 1;
			font: 400 20px/1 dashicons;
			speak: none;
			display: block;
			-webkit-font-smoothing: antialiased;
			-moz-osx-font-smoothing: grayscale;
			text-decoration: none!important;
		}

		li#accordion-section-cenote_upsell_section h3.accordion-section-title a {
			display: block;
			color: #fff !important;
			text-decoration: none;
		}

		li#accordion-section-cenote_upsell_section h3.accordion-section-title a:focus {
			box-shadow: none;
		}

		li#accordion-section-cenote_upsell_section h3.accordion-section-title:hover {
			background-color: #ca6771 !important;
		}

	</style>

	<script>
		( function ( $, api ) {
			api.sectionConstructor['cenote-upsell-section'] = api.Section.extend( {

				// No events for this type of section.
				attachEvents : function () {
				},

				// Always make the section active.
				isContextuallyActive : function () {
					return true;
				}
			} );
		} )( jQuery, wp.customize );

	</script>
	<?php
}

add_action( 'customize_controls_print_scripts', 'cenote_customize_controls_scripts' );

/**
 * Adds custom css in theme.
 *
 * @return void
 */
function cenote_custom_css() {
	$style = get_theme_mod( 'cenote_header_media_style', 'cenote-header-media--center' );
	$css   = '';

	if ( 'cenote-header-media--fullscreen' === $style ) {
		$css .= '.cenote-header-media {
			background-image: url( "' . get_header_image() . '" );
		}';
	} else {
		$css .= '.cenote-header-media .tg-container {
			background-image: url( "' . get_header_image() . '" );
		}';
	}

	wp_add_inline_style( 'cenote-style', $css );
}

add_action( 'wp_enqueue_scripts', 'cenote_custom_css', 10 );
