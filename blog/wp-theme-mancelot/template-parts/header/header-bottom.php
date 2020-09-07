<?php
/**
 * Display header bottom
 *
 * @package Cenote
 */

$header_style = get_theme_mod( 'cenote_header_style', 'tg-site-header--default' );
$header_load  = 'center';

if ( 'tg-site-header--left' === $header_style ) {
	$header_load = 'left';
}

get_template_part( 'template-parts/header/header', $header_load );
