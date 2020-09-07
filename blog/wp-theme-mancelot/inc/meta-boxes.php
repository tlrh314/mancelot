<?php
/**
 * Script to add Meta Boxes
 *
 * @package cenote
 */

/**
 * Registers metaboxes.
 */
function cenote_register_metaboxes() {
	add_meta_box( 'cenote_post_layout', esc_html__( 'Choose Layout', 'cenote' ), 'cenote_layout_cb', array( 'post', 'page' ), 'side' );
}
add_action( 'add_meta_boxes', 'cenote_register_metaboxes' );

/**
 * Callback for layout option.
 * Shows radio button to choose layout
 *
 * @param array $post current post information.
 */
function cenote_layout_cb( $post ) {

	// Use nonce for form verification.
	wp_nonce_field( basename( __FILE__ ), 'cenote_meta_nonce' );

	$layout = get_post_meta( $post->ID, 'cenote_post_layout', true );

	// Set default value if metabox returns empty.
	if ( empty( $layout ) ) {
		$layout = 'layout--default';
	}
	?>
		<input type="radio" name="cenote_post_layout" id="cenote-post-layout" value="layout--no-sidebar" <?php checked( $layout, 'layout--no-sidebar' ); ?>> <?php esc_html_e( 'Full Width', 'cenote' ); ?> <br>
		<input type="radio" name="cenote_post_layout" id="cenote-post-layout" value="layout--left-sidebar" <?php checked( $layout, 'layout--left-sidebar' ); ?>> <?php esc_html_e( 'Left Sidebar', 'cenote' ); ?> <br>
		<input type="radio" name="cenote_post_layout" id="cenote-post-layout" value="layout--right-sidebar" <?php checked( $layout, 'layout--right-sidebar' ); ?>> <?php esc_html_e( 'Right Sidebar', 'cenote' ); ?> <br>
		<input type="radio" name="cenote_post_layout" id="cenote-post-layout" value="layout--default" <?php checked( $layout, 'layout--default' ); ?>> <?php esc_html_e( 'Default', 'cenote' ); ?> <br>
	<?php
}

/**
 * Saves metaboxes value to database
 *
 * @param int $post_id current post id.
 */
function cenote_save_metaboxes( $post_id ) {
	global $post;

	// verify nonce.
	$cenote_meta_nonce = '';
	if ( isset( $_POST['cenote_meta_nonce'] ) && ! wp_verify_nonce( 'cenote_meta_nonce', basename( __FILE__ ) ) ) {
		$cenote_meta_nonce = sanitize_text_field( wp_unslash( $_POST['cenote_meta_nonce'] ) );
	}
	if ( ! $cenote_meta_nonce ) {
		return;
	}

	// Stop wp from clearing custom fields on autosave.
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}

	// check user role.
	$cenote_post_type = '';
	if ( isset( $_POST['post_type'] ) ) {
		$cenote_post_type = sanitize_text_field( wp_unslash( $_POST['post_type'] ) );
	}

	if ( in_array( $cenote_post_type, array( 'post', 'pages' ), true ) ) {
		if ( ! current_user_can( 'edit_post', $post_id ) || ! current_user_can( 'edit_page', $post_id ) ) {
			return $post_id;
		}
	}

	$cenote_post_layout = '';
	if ( isset( $_POST['cenote_post_layout'] ) ) {
		$cenote_post_layout = sanitize_text_field( wp_unslash( $_POST['cenote_post_layout'] ) );
	}

	// Only save to database if the layout is not default.
	if ( $cenote_post_layout && 'layout--default' !== $cenote_post_layout ) {
		$old_value = $cenote_post_layout;
		$new_value = sanitize_text_field( $old_value );

		if ( $new_value ) {
			update_post_meta( $post_id, 'cenote_post_layout', $new_value );
		}
	} else {
		delete_post_meta( $post_id, 'cenote_post_layout' );
	}
}

add_action( 'save_post', 'cenote_save_metaboxes' );
