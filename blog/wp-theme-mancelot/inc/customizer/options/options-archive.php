<?php
/**
 * Customizer option for Archive/Blog
 *
 * @package cenote
 */

// Blog/archive style.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'radio-image',
		'settings' => 'cenote_archive_style',
		'label'    => esc_html__( 'Archive/Blog Style', 'cenote' ),
		'section'  => 'cenote_section_archive',
		'default'  => 'tg-archive-style--masonry',
		'choices'  => array(
			'tg-archive-style--masonry'   => get_template_directory_uri() . '/assets/img/icons/archive--masonry.jpg',
			'tg-archive-style--classic'   => get_template_directory_uri() . '/assets/img/icons/archive--classic.jpg',
			'tg-archive-style--big-block' => get_template_directory_uri() . '/assets/img/icons/archive--big-block.jpg',
		),
	)
);

// Column Control for big block, block and masonry.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'radio-buttonset',
		'settings'        => 'cenote_archive_column',
		'label'           => esc_html__( 'Post Column', 'cenote' ),
		'section'         => 'cenote_section_archive',
		'default'         => 'tg-archive-col--3',
		'choices'         => array(
			'tg-archive-col--2' => esc_attr__( '2', 'cenote' ),
			'tg-archive-col--3' => esc_attr__( '3', 'cenote' ),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_archive_style',
				'value'    => array( 'tg-archive-style--big-block', 'tg-archive-style--masonry' ),
				'operator' => 'in',
			),
		),
	)
);

// Enable/Disable Drop Cap.
Kirki::add_field(
	'cenote_config', array(
		'type'        => 'toggle',
		'settings'    => 'cenote_archive_enable_drop_cap',
		'label'       => esc_html__( 'Enable Drop Cap', 'cenote' ),
		'description' => esc_html__( 'Makes the first letter of the content bigger', 'cenote' ),
		'section'     => 'cenote_section_archive',
		'default'     => '0',
	)
);


// Re-arrange order of archive post.
Kirki::add_field(
	'cenote_config', array(
		'type'        => 'sortable',
		'settings'    => 'cenote_archive_order_layout',
		'label'       => esc_html__( 'Post Content Order', 'cenote' ),
		'description' => esc_html__( 'Drag & Drop items to re-arrange the order', 'cenote' ),
		'section'     => 'cenote_section_archive',
		'default'     => array(
			'thumbnail',
			'meta',
			'title',
			'content',
			'footer',
		),
		'choices'     => array(
			'thumbnail' => esc_attr__( 'Thumbnail', 'cenote' ),
			'meta'      => esc_attr__( 'Meta Tags', 'cenote' ),
			'title'     => esc_attr__( 'Title', 'cenote' ),
			'content'   => esc_attr__( 'Content', 'cenote' ),
			'footer'    => esc_attr__( 'Footer', 'cenote' ),
		),
	)
);
