<?php
/**
 * Customizer options for footer
 *
 * @package cenote
 */

// Select footer style.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_footer_style',
		'label'    => esc_html__( 'Footer Style', 'cenote' ),
		'section'  => 'cenote_section_footer',
		'default'  => 'tg-site-footer--default',
		'choices'  => array(
			'tg-site-footer--default' => get_template_directory_uri() . '/assets/img/icons/footer--default.jpg',
			'tg-site-footer--light'   => get_template_directory_uri() . '/assets/img/icons/footer--light.jpg',
		),
	)
);

// Enable/Disable back to top.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_footer_enable_back_to_top',
		'label'    => esc_html__( 'Enable Back To Top', 'cenote' ),
		'section'  => 'cenote_section_footer',
		'default'  => '1',
	)
);
