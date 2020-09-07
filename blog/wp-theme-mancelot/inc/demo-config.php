<?php
/**
 * Functions for configuring demo importer.
 *
 * @author   ThemeGrill
 * @category Admin
 * @package  Importer/Functions
 * @since    1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Setup demo importer packages.
 *
 * @param array $packages The list of theme demo packages.
 *
 * @return array
 */
function cenote_demo_importer_packages( $packages ) {
	$new_packages = array(
		'cenote-free'    => array(
			'name'    => esc_html__( 'Cenote', 'cenote' ),
			'preview' => 'https://demo.themegrill.com/cenote/',
		),
		'cenote-fashion' => array(
			'name'    => esc_html__( 'Cenote Fashion', 'cenote' ),
			'preview' => 'https://demo.themegrill.com/cenote-fashion/',
		),
		'cenote-tech'    => array(
			'name'    => esc_html__( 'Cenote Tech', 'cenote' ),
			'preview' => 'https://demo.themegrill.com/cenote-tech/',
		),
	);

	return array_merge( $new_packages, $packages );
}

add_filter( 'themegrill_demo_importer_packages', 'cenote_demo_importer_packages' );
