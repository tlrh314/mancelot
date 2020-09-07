<?php
/**
 * Cenote layout control option
 *
 * @package cenote
 */

// Layout style for homepage.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_layout_site',
		'label'    => esc_html__( 'Site Layout', 'cenote' ),
		'section'  => 'cenote_section_layout',
		'default'  => 'layout-site--wide',
		'choices'  => array(
			'layout-site--wide'  => get_template_directory_uri() . '/assets/img/icons/layout--full.jpg',
			'layout-site--boxed' => get_template_directory_uri() . '/assets/img/icons/layout--boxed.jpg',
		),
	)
);

// Layout style for Arvhive/Blog.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_layout_archive',
		'label'    => esc_html__( 'Archive/Blog Layout', 'cenote' ),
		'section'  => 'cenote_section_layout',
		'default'  => 'layout--no-sidebar',
		'choices'  => array(
			'layout--left-sidebar'  => get_template_directory_uri() . '/assets/img/icons/layout--left.jpg',
			'layout--right-sidebar' => get_template_directory_uri() . '/assets/img/icons/layout--right.jpg',
			'layout--no-sidebar'    => get_template_directory_uri() . '/assets/img/icons/layout--full.jpg',
		),
	)
);


// Layout style for Single Post.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_layout_single',
		'label'    => esc_html__( 'Single Post Layout', 'cenote' ),
		'section'  => 'cenote_section_layout',
		'default'  => 'layout--right-sidebar',
		'choices'  => array(
			'layout--left-sidebar'  => get_template_directory_uri() . '/assets/img/icons/layout--left.jpg',
			'layout--right-sidebar' => get_template_directory_uri() . '/assets/img/icons/layout--right.jpg',
			'layout--no-sidebar'    => get_template_directory_uri() . '/assets/img/icons/layout--full.jpg',
		),
	)
);


// Layout style for page.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_layout_page',
		'label'    => esc_html__( 'Page Layout', 'cenote' ),
		'section'  => 'cenote_section_layout',
		'default'  => 'layout--right-sidebar',
		'choices'  => array(
			'layout--left-sidebar'  => get_template_directory_uri() . '/assets/img/icons/layout--left.jpg',
			'layout--right-sidebar' => get_template_directory_uri() . '/assets/img/icons/layout--right.jpg',
			'layout--no-sidebar'    => get_template_directory_uri() . '/assets/img/icons/layout--full.jpg',
		),
	)
);
