<?php
/**
 * Cenote Heder media options
 *
 * @package cenote
 */

// Option to enable/disable the header media section.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_header_media_enable_desc',
		'label'    => esc_html__( 'Enable media info box', 'cenote' ),
		'section'  => 'header_image',
		'default'  => '1',
	)
);

// Option to select header media section layout.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_header_media_style',
		'label'    => esc_html__( 'Header Media Layout', 'cenote' ),
		'section'  => 'header_image',
		'default'  => 'cenote-header-media--center',
		'choices'  => array(
			'cenote-header-media--center'     => get_template_directory_uri() . '/assets/img/icons/header-media--center.jpg',
			'cenote-header-media--fullscreen' => get_template_directory_uri() . '/assets/img/icons/header-media--fullscreen.jpg',
		),
	)
);

// Header media Heading.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'text',
		'settings'        => 'cenote_header_media_title',
		'label'           => esc_html__( 'Title', 'cenote' ),
		'section'         => 'header_image',
		'default'         => 'Hi, I am Header Media Title',
		'transport'       => 'postMessage',
		'js_vars'         => array(
			array(
				'element'  => '.cenote-header-media .cenote-header-media__title',
				'function' => 'html',
			),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_header_media_enable_desc',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);

// Header Media Content.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'text',
		'settings'        => 'cenote_header_media_text',
		'label'           => esc_html__( 'Text', 'cenote' ),
		'section'         => 'header_image',
		'default'         => 'I am description of header media. You can write short text to give me more info.',
		'transport'       => 'postMessage',
		'js_vars'         => array(
			array(
				'element'  => '.cenote-header-media .cenote-header-media__text',
				'function' => 'html',
			),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_header_media_enable_desc',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);

// Header Media Button text.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'text',
		'settings'        => 'cenote_header_media_button_text',
		'label'           => esc_html__( 'Button Text', 'cenote' ),
		'section'         => 'header_image',
		'default'         => 'Take action',
		'transport'       => 'postMessage',
		'js_vars'         => array(
			array(
				'element'  => '.cenote-header-media .cenote-header-media__button',
				'function' => 'html',
			),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_header_media_enable_desc',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);

// Header Media Button LInk.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'url',
		'settings'        => 'cenote_header_media_url',
		'label'           => esc_html__( 'Button URL', 'cenote' ),
		'section'         => 'header_image',
		'default'         => '#',
		'active_callback' => array(
			array(
				'setting'  => 'cenote_header_media_enable_desc',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);
