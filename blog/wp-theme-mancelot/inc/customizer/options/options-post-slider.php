<?php
/**
 * Cenote post slider Option
 *
 * @package cenote
 */

// Enable Slider.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_post_slider_enabled',
		'label'    => esc_html__( 'Enable post slider', 'cenote' ),
		'section'  => 'cenote_section_post_slider',
		'default'  => false,
	)
);

// Post slider.
// Category select.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'radio-buttonset',
		'settings'        => 'cenote_post_slide_category',
		'label'           => esc_html__( 'Category select', 'cenote' ),
		'section'         => 'cenote_section_post_slider',
		'default'         => 'latest-post',
		'choices'         => array(
			'latest-post' => esc_attr__( 'Latest Post', 'cenote' ),
			'category'    => esc_attr__( 'Category', 'cenote' ),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_post_slider_enabled',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);

$category_choices = array();
$categories_lists = get_categories();
foreach ( $categories_lists as $categories => $category ) {
	$category_choices[ $category->term_id ] = $category->name;
}

Kirki::add_field(
	'cenote_config', array(
		'type'            => 'select',
		'settings'        => 'cenote_post_slide_category_select',
		'label'           => esc_html__( 'Categories', 'cenote' ),
		'section'         => 'cenote_section_post_slider',
		'default'         => 'uncategorized',
		'choices'         => $category_choices,
		'active_callback' => array(
			array(
				'setting'  => 'cenote_post_slide_category',
				'operator' => '==',
				'value'    => 'category',
			),
			array(
				'setting'  => 'cenote_post_slider_enabled',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);
