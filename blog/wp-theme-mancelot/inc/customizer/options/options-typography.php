<?php
/**
 * Customizer option for typography
 *
 * @package cenote
 */

// Body typography.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'typography',
		'settings' => 'cenote_typography_body',
		'label'    => esc_attr__( 'Body', 'cenote' ),
		'section'  => 'cenote_section_typography',
		'default'  => array(
			'font-family' => 'Roboto',
			'variant'     => 'regular',
		),
		'output'   => array(
			array(
				'element' => 'body',
			),
		),
		'choices'  => array(
			'fonts'   => array(
				'google' => array(
					'Roboto',
					'Open Sans',
				),
			),
			'variant' => array(
				'400',
				'700',
			),
		),
	)
);

// Heading.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'typography',
		'settings' => 'cenote_typography_heading',
		'label'    => esc_attr__( 'Heading', 'cenote' ),
		'section'  => 'cenote_section_typography',
		'default'  => array(
			'font-family' => 'Catamaran',
			'variant'     => '700',
		),
		'output'   => array(
			array(
				'element' => array( 'h1, h2, h3, h4, h5, h6' ),
			),
		),
		'choices'  => array(
			'fonts'   => array(
				'google' => array(
					'Catamaran',
					'Playfair Display',
				),
			),
			'variant' => array(
				'700',
			),
		),
	)
);
