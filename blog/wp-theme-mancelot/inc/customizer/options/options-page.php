<?php
/**
 * Customizer option for page
 *
 * @package cenote
 */

// Re-arrange order of page item.
Kirki::add_field(
	'cenote_config', array(
		'type'        => 'sortable',
		'settings'    => 'cenote_page_order_layout',
		'label'       => esc_html__( 'Page Content Order', 'cenote' ),
		'description' => esc_html__( 'Drag & Drop items to re-arrange the order', 'cenote' ),
		'section'     => 'cenote_section_page',
		'default'     => array(
			'title',
			'thumbnail',
			'content',
			'footer',
		),
		'choices'     => array(
			'title'     => esc_attr__( 'Title', 'cenote' ),
			'thumbnail' => esc_attr__( 'Thumbnail', 'cenote' ),
			'content'   => esc_attr__( 'Content', 'cenote' ),
			'footer'    => esc_attr__( 'Footer', 'cenote' ),
		),
	)
);
