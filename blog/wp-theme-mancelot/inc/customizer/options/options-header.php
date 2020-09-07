<?php
/**
 * Cenote available Header Options
 *
 * @package cenote
 */

// Enable/Disable Header top.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_enable_header_top',
		'label'    => esc_html__( 'Enable Header Top Bar', 'cenote' ),
		'section'  => 'cenote_section_header',
		'default'  => '1',
	)
);

// Re-arrange order of header top items.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'sortable',
		'settings'        => 'cenote_order_header_top_items',
		'label'           => esc_html__( 'Header Top Item Order', 'cenote' ),
		'description'     => esc_html__( 'Drag & Drop items to re-arrange the order', 'cenote' ),
		'section'         => 'cenote_section_header',
		'default'         => array(
			'menu',
			'contact-info',
		),
		'choices'         => array(
			'menu'         => esc_attr__( 'Menu', 'cenote' ),
			'contact-info' => esc_attr__( 'Contact Info', 'cenote' ),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_enable_header_top',
				'operator' => '==',
				'value'    => '1',
			),
		),
	)
);

// Contact info phone.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'text',
		'settings'        => 'cenote_header_contact_phone',
		'label'           => esc_html__( 'Phone Number', 'cenote' ),
		'section'         => 'cenote_section_header',
		'default'         => '(123)456-7890',
		'transport'       => 'postMessage',
		'js_vars'         => array(
			array(
				'element'  => '.tg-contact-info .tg-contact-info__phone span',
				'function' => 'html',
			),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_order_header_top_items',
				'operator' => 'in',
				'value'    => 'contact-info',
			),
			array(
				'setting'  => 'cenote_enable_header_top',
				'operator' => '==',
				'value'    => '1',
			),
		),
	)
);

// Contact info email.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'text',
		'settings'        => 'cenote_header_contact_email',
		'label'           => esc_html__( 'Email Address', 'cenote' ),
		'section'         => 'cenote_section_header',
		'default'         => 'example@domain.com',
		'transport'       => 'postMessage',
		'js_vars'         => array(
			array(
				'element'  => '.tg-contact-info .tg-contact-info__email span',
				'function' => 'html',
			),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_order_header_top_items',
				'operator' => 'in',
				'value'    => 'contact-info',
			),
			array(
				'setting'  => 'cenote_enable_header_top',
				'operator' => '==',
				'value'    => '1',
			),
		),
	)
);

// Enable/disable the sticky header.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_header_sticky_option',
		'label'    => esc_html__( 'Enable Sticky Header', 'cenote' ),
		'section'  => 'cenote_section_header',
		'default'  => '1',
	)
);

// Select header style.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_header_style',
		'label'    => esc_html__( 'Header Layout', 'cenote' ),
		'section'  => 'cenote_section_header',
		'default'  => 'tg-site-header--default',
		'choices'  => array(
			'tg-site-header--default'  => get_template_directory_uri() . '/assets/img/icons/header--default.jpg',
			'tg-site-header--bordered' => get_template_directory_uri() . '/assets/img/icons/header--bordered.jpg',
			'tg-site-header--left'     => get_template_directory_uri() . '/assets/img/icons/header--left.jpg',
		),
	)
);

// Show/Hide search icon in header.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_search_icon_option',
		'label'    => esc_html__( 'Enable Search Icon', 'cenote' ),
		'section'  => 'cenote_section_header',
		'default'  => '1',
	)
);
