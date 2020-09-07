<?php
/**
 * Cenote Admin Class.
 *
 * @author  ThemeGrill
 * @package cenote
 * @since   1.3.3
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! class_exists( 'Cenote_Admin' ) ) :

	/**
	 * Cenote_Admin Class.
	 */
	class Cenote_Admin {

		/**
		 * Constructor.
		 */
		public function __construct() {
			add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_scripts' ) );
		}

		/**
		 * Localize array for import button AJAX request.
		 */
		public function enqueue_scripts() {
			wp_enqueue_style( 'cenote-admin-style', get_template_directory_uri() . '/inc/admin/css/admin.css', array(), CENOTE_THEME_VERSION );

			wp_enqueue_script( 'cenote-plugin-install-helper', get_template_directory_uri() . '/inc/admin/js/plugin-handle.js', array( 'jquery' ), CENOTE_THEME_VERSION, true );

			$welcome_data = array(
				'uri'      => esc_url( admin_url( '/themes.php?page=demo-importer&browse=all&cenote-hide-notice=welcome' ) ),
				'btn_text' => esc_html__( 'Processing...', 'cenote' ),
				'nonce'    => wp_create_nonce( 'cenote_demo_import_nonce' ),
			);

			wp_localize_script( 'cenote-plugin-install-helper', 'cenoteRedirectDemoPage', $welcome_data );
		}
	}

endif;

return new Cenote_Admin();
