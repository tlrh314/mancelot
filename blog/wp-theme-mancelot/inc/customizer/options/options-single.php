<?php
/**
 * Customizer options for single
 *
 * @package cenote
 */

// Re-arrange order of single post item.
Kirki::add_field(
	'cenote_config', array(
		'type'        => 'sortable',
		'settings'    => 'cenote_single_order_layout',
		'label'       => esc_html__( 'Single Post Content Order', 'cenote' ),
		'description' => esc_html__( 'Drag & Drop items to re-arrange the order', 'cenote' ),
		'section'     => 'cenote_section_single',
		'default'     => array(
			'thumbnail',
			'categories',
			'title',
			'meta',
			'content',
			'footer',
		),
		'choices'     => array(
			'thumbnail'  => esc_attr__( 'Thumbnail', 'cenote' ),
			'categories' => esc_attr__( 'Categories', 'cenote' ),
			'title'      => esc_attr__( 'Title', 'cenote' ),
			'meta'       => esc_attr__( 'Meta Tags', 'cenote' ),
			'content'    => esc_attr__( 'Content', 'cenote' ),
			'footer'     => esc_attr__( 'Footer', 'cenote' ),
		),
	)
);

// Enable/Disable Drop Drop.
Kirki::add_field(
	'cenote_config', array(
		'type'        => 'toggle',
		'settings'    => 'cenote_single_enable_drop_cap',
		'label'       => esc_html__( 'Enable Drop Cap', 'cenote' ),
		'description' => esc_html__( 'Makes the first letter of the content bigger', 'cenote' ),
		'section'     => 'cenote_section_single',
		'default'     => '1',
	)
);

// Enable/Disable Author Box.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_single_enable_author_box',
		'label'    => esc_html__( 'Enable Author Box', 'cenote' ),
		'section'  => 'cenote_section_single',
		'default'  => '1',
	)
);

// Enable/Disable Related Post.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_single_enable_related_post',
		'label'    => esc_html__( 'Enable Related Posts', 'cenote' ),
		'section'  => 'cenote_section_single',
		'default'  => '1',
	)
);
