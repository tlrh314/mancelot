<?php
/**
 * Cenote option for breadcrumb
 *
 * @package cenote
 */

// Enable/Disable breadcrumbs.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_breadcrumb',
		'label'    => esc_html__( 'Enable Breadcrumbs', 'cenote' ),
		'section'  => 'cenote_section_breadcrumb',
		'default'  => '1',
	)
);
