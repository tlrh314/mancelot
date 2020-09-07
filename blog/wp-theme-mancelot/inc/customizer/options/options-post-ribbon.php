<?php
/**
 * Cenote Post Ribbon option
 *
 * @package cenote
 */

// Post Ribbon display.
Kirki::add_field(
	'cenote_config', array(
		'type'     => 'toggle',
		'settings' => 'cenote_single_post_ribbon_display',
		'label'    => esc_attr__( 'Enable Post Ribbon', 'cenote' ),
		'section'  => 'cenote_section_post_ribbon',
		'default'  => 0,
	)
);

// Display by categories.
Kirki::add_field(
	'cenote_config', array(
		'type'            => 'radio-buttonset',
		'settings'        => 'cenote_post_ribbon_category_select',
		'label'           => esc_html__( 'Category Select', 'cenote' ),
		'section'         => 'cenote_section_post_ribbon',
		'default'         => 'tg-post-latest',
		'choices'         => array(
			'tg-post-category' => esc_attr__( 'Categories', 'cenote' ),
			'tg-post-latest'   => esc_attr__( 'Latest', 'cenote' ),
		),
		'active_callback' => array(
			array(
				'setting'  => 'cenote_single_post_ribbon_display',
				'operator' => '==',
				'value'    => 1,
			),
		),
	)
);

// Categories select option.
$category_choices                        = array();
$categories_lists                        = get_categories();
$category_choices['cenote_all_category'] = esc_html__( ' Display All Category', 'cenote' );
foreach ( $categories_lists as $categories => $category ) {
	$category_choices[ $category->term_id ] = $category->name;
}

Kirki::add_field(
	'cenote_config', array(
		'type'            => 'select',
		'settings'        => 'cenote_post_ribbon_categories',
		'label'           => esc_html__( 'Categories', 'cenote' ),
		'section'         => 'cenote_section_post_ribbon',
		'default'         => 'cenote_all_category',
		'choices'         => $category_choices,
		'active_callback' => array(
			array(
				'setting'  => 'cenote_post_ribbon_category_select',
				'operator' => '==',
				'value'    => 'tg-post-category',
			),
		),
	)
);
