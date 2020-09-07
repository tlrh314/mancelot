<?php
/**
 * Cenote available Social Options
 *
 * @package cenote
 */

// Option to add the social links via repeater field.
Kirki::add_field( 'cenote_config', array(
	'type'        => 'repeater',
	'label'       => esc_html__( 'Add Social Profile', 'cenote' ),
	'description' => esc_html__( 'Drag & Drop items to re-arrange the order', 'cenote' ),
	'section'     => 'cenote_section_social',
	'settings'    => 'cenote_social_icons_lists',
	'row_label'   => array(
		'type'  => 'field',
		'value' => esc_html__( 'Social Profile', 'cenote' ),
		'field' => 'social_icon',
	),
	'default'     => array(
		array(
			'social_icon' => 'tg-icon-facebook',
			'social_url'  => '#',
		),
		array(
			'social_icon' => 'tg-icon-twitter',
			'social_url'  => '#',
		),
	),
	'fields'      => array(
		'social_icon' => array(
			'label'   => esc_html__( 'Social Icon', 'cenote' ),
			'type'    => 'select',
			'default' => 'fa-facebook',
			'choices' => array(
				'tg-icon-behance'     => esc_html__( 'Behance', 'cenote' ),
				'tg-icon-blogger'     => esc_html__( 'Blogger', 'cenote' ),
				'tg-icon-codepen'     => esc_html__( 'CodePen', 'cenote' ),
				'tg-icon-delicious'   => esc_html__( 'Delicious', 'cenote' ),
				'tg-icon-deviantart'  => esc_html__( 'DeviantArt', 'cenote' ),
				'tg-icon-dribbble'    => esc_html__( 'Dribbble', 'cenote' ),
				'tg-icon-facebook'    => esc_html__( 'Facebook', 'cenote' ),
				'tg-icon-google-plus' => esc_html__( 'Google Plus', 'cenote' ),
				'tg-icon-instagram'   => esc_html__( 'Instagram', 'cenote' ),
				'tg-icon-linkedin'    => esc_html__( 'LinkedIn', 'cenote' ),
				'tg-icon-medium'      => esc_html__( 'Medium', 'cenote' ),
				'tg-icon-pinterest'   => esc_html__( 'Pinterest', 'cenote' ),
				'tg-icon-quora'       => esc_html__( 'Quora', 'cenote' ),
				'tg-icon-tumblr'      => esc_html__( 'Tumblr', 'cenote' ),
				'tg-icon-twitter'     => esc_html__( 'Twitter', 'cenote' ),
				'tg-icon-vimeo'       => esc_html__( 'Vimeo', 'cenote' ),
				'tg-icon-yelp'        => esc_html__( 'Yelp', 'cenote' ),
				'tg-icon-youtube'     => esc_html__( 'YouTube', 'cenote' ),
			),
		),
		'social_url'  => array(
			'type'    => 'text',
			'label'   => esc_html__( 'Social Link URL', 'cenote' ),
			'default' => '',
		),
	),
) );
